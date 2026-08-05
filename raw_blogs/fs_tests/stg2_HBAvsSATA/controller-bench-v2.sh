#!/bin/bash
set -euo pipefail

POOL="ctrlpool"
DATASET="${POOL}/test"
MOUNTPOINT="/ctrlpool/test"

CONTROLLER=""
SCENARIO=""
RUNROOT="controller-logs"

usage() {
  echo "Usage: $0 --controller <lsi-import|asm1166|lsi-refurb> --scenario <6hdd_mirror3x2|6hdd_raidz2_6|2ssd_mirror2>"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --controller)
      CONTROLLER="$2"
      shift 2
      ;;
    --scenario)
      SCENARIO="$2"
      shift 2
      ;;
    *)
      usage
      ;;
  esac
done

[[ -n "$CONTROLLER" ]] || usage
[[ -n "$SCENARIO" ]] || usage

case "$CONTROLLER" in
  lsi-import|asm1166|lsi-refurb) ;;
  *) usage ;;
esac

case "$SCENARIO" in
  6hdd_mirror3x2|6hdd_raidz2_6|2ssd_mirror2) ;;
  *) usage ;;
esac

TS=$(date +%Y%m%d-%H%M%S)
OUTDIR="${RUNROOT}/${CONTROLLER}/${SCENARIO}/${TS}"
mkdir -p "$OUTDIR"

log() {
  echo "[$(date '+%F %T')] $1" | tee -a "${OUTDIR}/run.log"
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }
}

for cmd in zpool zfs fio lsblk lspci smartctl; do
  require_cmd "$cmd"
done

cleanup() {
  if zpool list -H -o name 2>/dev/null | grep -qx "$POOL"; then
    log "Cleanup: destroying leftover pool $POOL"
    zpool destroy "$POOL" || true
  fi
}
trap cleanup EXIT INT TERM

# ------------------------------------------------------------
# Disk definitions
# EDIT SSD IDs TO MATCH THE J4005 BOX
# ------------------------------------------------------------

HDD1="/dev/disk/by-id/ata-Hitachi_HTS547550A9E384_J2160051E1A4ZD"
HDD2="/dev/disk/by-id/ata-ST3500312CS_5VVRKGAV"
HDD3="/dev/disk/by-id/ata-ST3500418AS_Z2ACPF1Z"
HDD4="/dev/disk/by-id/ata-ST500DM002-1BD142_Z2AFGE69"
HDD5="/dev/disk/by-id/ata-ST500DM002-1BD142_W3TQFS8T"
HDD6="/dev/disk/by-id/ata-ST500DM002-1BD142_W3TQ01LD"

SSD1="/dev/disk/by-id/ata-REPLACE_ME_SSD1"
SSD2="/dev/disk/by-id/ata-REPLACE_ME_SSD2"

# ------------------------------------------------------------
# Expected controller presence check
# ------------------------------------------------------------

LSPCI_ALL="$(lspci -nn)"
echo "$LSPCI_ALL" > "${OUTDIR}/lspci.txt"

case "$CONTROLLER" in
  lsi-import|lsi-refurb)
    echo "$LSPCI_ALL" | grep -Eiq 'LSI|Broadcom|SAS2308' || {
      echo "Expected LSI/Broadcom controller not found in lspci" >&2
      exit 1
    }
    ;;
  asm1166)
    echo "$LSPCI_ALL" | grep -Eiq 'ASMedia|ASM116' || {
      echo "Expected ASMedia controller not found in lspci" >&2
      exit 1
    }
    ;;
esac

# ------------------------------------------------------------
# Select disks and layout
# ------------------------------------------------------------

case "$SCENARIO" in
  6hdd_mirror3x2)
    DISKS=("$HDD1" "$HDD2" "$HDD3" "$HDD4" "$HDD5" "$HDD6")
    POOLCMD=(
      zpool create -f "$POOL"
      mirror "${DISKS[0]}" "${DISKS[1]}"
      mirror "${DISKS[2]}" "${DISKS[3]}"
      mirror "${DISKS[4]}" "${DISKS[5]}"
    )
    ;;
  6hdd_raidz2_6)
    DISKS=("$HDD1" "$HDD2" "$HDD3" "$HDD4" "$HDD5" "$HDD6")
    POOLCMD=(
      zpool create -f "$POOL"
      raidz2 "${DISKS[0]}" "${DISKS[1]}" "${DISKS[2]}" "${DISKS[3]}" "${DISKS[4]}" "${DISKS[5]}"
    )
    ;;
  2ssd_mirror2)
    DISKS=("$SSD1" "$SSD2")
    POOLCMD=(
      zpool create -f "$POOL"
      mirror "${DISKS[0]}" "${DISKS[1]}"
    )
    ;;
esac

for d in "${DISKS[@]}"; do
  [[ -e "$d" ]] || { echo "Disk path not found: $d" >&2; exit 1; }
done

# ------------------------------------------------------------
# Inventory + SMART capture
# ------------------------------------------------------------

{
  echo "=== TIMESTAMP ==="
  date
  echo
  echo "=== HOST ==="
  hostname
  uname -a
  echo
  echo "=== CONTROLLER LABEL ==="
  echo "$CONTROLLER"
  echo
  echo "=== SCENARIO ==="
  echo "$SCENARIO"
  echo
  echo "=== LSBLK ==="
  lsblk -o NAME,TYPE,SIZE,MODEL,SERIAL,TRAN,MOUNTPOINTS
  echo
  echo "=== SELECTED DISKS ==="
  printf '%s\n' "${DISKS[@]}"
  echo
  echo "=== POOL COMMAND ==="
  printf '%q ' "${POOLCMD[@]}"
  echo
} > "${OUTDIR}/inventory.txt"

for d in "${DISKS[@]}"; do
  base=$(basename "$d")
  smartctl -a "$d" > "${OUTDIR}/${base}.smart.txt" 2>&1 || true
done

# ------------------------------------------------------------
# Clear old labels
# ------------------------------------------------------------

for d in "${DISKS[@]}"; do
  zpool labelclear -f "$d" 2>/dev/null || true
done

# ------------------------------------------------------------
# Create pool
# ------------------------------------------------------------

log "Starting controller benchmark"
log "Controller: $CONTROLLER"
log "Scenario: $SCENARIO"
log "Creating pool: ${POOLCMD[*]}"
"${POOLCMD[@]}"

zfs set compression=off "$POOL"
zfs set atime=off "$POOL"
zfs create -o mountpoint="$MOUNTPOINT" "$DATASET"
mkdir -p "$MOUNTPOINT"

zpool status "$POOL" > "${OUTDIR}/zpool-status-before.txt"
zfs list > "${OUTDIR}/zfs-list-before.txt"

# ------------------------------------------------------------
# fio helpers
# ------------------------------------------------------------

TESTFILE="${MOUNTPOINT}/fio-testfile"

run_fio() {
  local name="$1"
  shift
  local file="${OUTDIR}/${name}.json"

  log "Running fio job: $name"
  fio \
    --name="$name" \
    --filename="$TESTFILE" \
    --output-format=json \
    --output="$file" \
    --ioengine=libaio \
    --direct=1 \
    --group_reporting=1 \
    "$@"
}

# ------------------------------------------------------------
# Workload suite
# ------------------------------------------------------------

# prefill
run_fio prefill \
  --rw=write \
  --bs=1M \
  --iodepth=16 \
  --numjobs=1 \
  --size=16G

sync
sleep 3

# sequential throughput
run_fio seq-read \
  --time_based=1 \
  --runtime=60 \
  --rw=read \
  --bs=1M \
  --iodepth=16 \
  --numjobs=1 \
  --size=16G

run_fio seq-write \
  --time_based=1 \
  --runtime=60 \
  --rw=write \
  --bs=1M \
  --iodepth=16 \
  --numjobs=1 \
  --size=16G

sync
sleep 3

# random / latency / concurrency
run_fio rand-read-q16 \
  --time_based=1 \
  --runtime=60 \
  --rw=randread \
  --bs=4k \
  --iodepth=16 \
  --numjobs=4 \
  --size=8G

run_fio rand-write-q16 \
  --time_based=1 \
  --runtime=60 \
  --rw=randwrite \
  --bs=4k \
  --iodepth=16 \
  --numjobs=4 \
  --size=8G

run_fio rand-mixed-70r30w-q16 \
  --time_based=1 \
  --runtime=60 \
  --rw=randrw \
  --rwmixread=70 \
  --bs=4k \
  --iodepth=16 \
  --numjobs=4 \
  --size=8G

run_fio rand-read-q1 \
  --time_based=1 \
  --runtime=60 \
  --rw=randread \
  --bs=4k \
  --iodepth=1 \
  --numjobs=1 \
  --size=8G

run_fio rand-read-q32 \
  --time_based=1 \
  --runtime=60 \
  --rw=randread \
  --bs=4k \
  --iodepth=32 \
  --numjobs=8 \
  --size=8G

sync
sleep 5

zpool status "$POOL" > "${OUTDIR}/zpool-status-after.txt"
zfs list > "${OUTDIR}/zfs-list-after.txt"

log "Destroying pool"
zpool destroy "$POOL"

log "Completed controller benchmark"