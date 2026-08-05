#!/usr/bin/env bash
set -euo pipefail

# Non-login SSH shells often omit /usr/sbin; smartctl/zpool/live tools live there on Debian/Proxmox.
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH}"
export PATH

# Stage 3: Refurb vs Clone LSI HBA comparison runner
# - Builds a ZFS pool for the selected scenario
# - Runs repeatable fio jobs
# - Captures host/controller/inventory/SMART metadata
# - Can self-detach so runs continue after SSH disconnect

POOL="stage3pool"
DATASET="${POOL}/test"
MOUNTPOINT="/${POOL}/test"
RUNROOT="stage3-logs"

CARD=""
SCENARIO=""
RUNTIME=90
DETACH=0
NO_CLEANUP=0
ALLOW_DESTROY=0
PREFLIGHT_ONLY=0

usage() {
  cat <<'EOF'
Usage:
  stage3_hba_compare.sh --card <refurb|clone> --scenario <hdd_mirror2x2|hdd_raidz1_4|ssd_mirror3|ssd_raidz1_3> [options]

Options:
  --runtime-sec <n>   fio runtime in seconds for time-based tests (default: 90)
  --detach            run in background via nohup, safe across SSH disconnect
  --no-cleanup        keep pool after completion (default destroys pool)
  --allow-destroy     REQUIRED to wipe labels/create test pool on selected disks
  --preflight-only    collect inventory and safety checks only, no destructive ops
  --help              show this help

Notes:
  1) Edit disk IDs in the "Disk inventory" section before first run.
  2) Keep physical wiring identical between refurb and clone card runs.
  3) For fair adapter testing, use the same scenario + same drives + same cabling.
  4) Run as root for full benchmarks (zpool create / labelclear need root). If smartctl was
     "missing" as a normal user, PATH lacked /usr/sbin — this script fixes that; disk access may
     still require root or membership in group "disk".
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --card)
      CARD="${2:-}"
      shift 2
      ;;
    --scenario)
      SCENARIO="${2:-}"
      shift 2
      ;;
    --runtime-sec)
      RUNTIME="${2:-}"
      shift 2
      ;;
    --detach)
      DETACH=1
      shift
      ;;
    --no-cleanup)
      NO_CLEANUP=1
      shift
      ;;
    --allow-destroy)
      ALLOW_DESTROY=1
      shift
      ;;
    --preflight-only)
      PREFLIGHT_ONLY=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

[[ "$CARD" == "refurb" || "$CARD" == "clone" ]] || { usage; exit 1; }
case "$SCENARIO" in
  hdd_mirror2x2|hdd_raidz1_4|ssd_mirror3|ssd_raidz1_3) ;;
  *) usage; exit 1 ;;
esac
[[ "$RUNTIME" =~ ^[0-9]+$ ]] || { echo "runtime must be integer seconds" >&2; exit 1; }

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }
}

for cmd in zpool zfs fio lsblk lspci smartctl awk sed nohup; do
  require_cmd "$cmd"
done

mkdir -p "$RUNROOT"

# Detach bugfix: the worker must reuse the parent's OUTDIR. Otherwise nohup redirects
# stdout/stderr to parent_timestamp/run.log while lspci/inventory/fio write under a
# new child_timestamp/, so nothing matches and it looks like "no activity".
if [[ -n "${STAGE3_OUTDIR:-}" ]]; then
  OUTDIR="$STAGE3_OUTDIR"
  LOGFILE="${OUTDIR}/run.log"
elif [[ "$DETACH" -eq 1 && "${STAGE3_DETACHED:-0}" != "1" ]]; then
  TS="$(date +%Y%m%d-%H%M%S)"
  OUTDIR="${RUNROOT}/${CARD}/${SCENARIO}/${TS}"
  mkdir -p "$OUTDIR"
  LOGFILE="${OUTDIR}/run.log"
  ABS_OUT="$(cd "$OUTDIR" && pwd)"
  echo "Detaching run."
  echo "  Log file:    ${LOGFILE}"
  echo "  Output dir:  ${ABS_OUT}"
  echo "  Monitor:     tail -f \"${LOGFILE}\""
  STAGE3_DETACHED=1 STAGE3_OUTDIR="$OUTDIR" nohup "$0" \
    --card "$CARD" \
    --scenario "$SCENARIO" \
    --runtime-sec "$RUNTIME" \
    $([[ "$NO_CLEANUP" -eq 1 ]] && echo "--no-cleanup") \
    $([[ "$ALLOW_DESTROY" -eq 1 ]] && echo "--allow-destroy") \
    $([[ "$PREFLIGHT_ONLY" -eq 1 ]] && echo "--preflight-only") \
    >"$LOGFILE" 2>&1 < /dev/null &
  worker_pid=$!
  echo "$worker_pid" > "${OUTDIR}/run.pid"
  echo "Started worker PID ${worker_pid} (saved ${OUTDIR}/run.pid)"
  exit 0
else
  TS="$(date +%Y%m%d-%H%M%S)"
  OUTDIR="${RUNROOT}/${CARD}/${SCENARIO}/${TS}"
  mkdir -p "$OUTDIR"
  LOGFILE="${OUTDIR}/run.log"
fi

log() {
  local line="[$(date '+%F %T')] $*"
  # Avoid duplicate lines when stdout is already redirected to LOGFILE (detached worker).
  if [[ "${STAGE3_DETACHED:-0}" == "1" ]] || [[ ! -t 1 ]]; then
    echo "$line" >> "$LOGFILE"
  else
    echo "$line" | tee -a "$LOGFILE"
  fi
}

# ------------------------------------------------------------
# Disk inventory - EDIT THESE IDs FOR YOUR HOST
# ------------------------------------------------------------
HDD1="/dev/disk/by-id/ata-ST4000VN008-2DR166_ZM41ATFP"
HDD2="/dev/disk/by-id/ata-ST4000VN008-2DR166_ZDHA5A7S"
HDD3="/dev/disk/by-id/ata-ST4000VN008-2DR166_ZDHA5GF5"
HDD4="/dev/disk/by-id/ata-ST4000VN008-2DR166_ZGY7WERC"

SSD1="/dev/disk/by-id/ata-Samsung_SSD_860_EVO_500GB_S3Z2NB1K910954L"
SSD2="/dev/disk/by-id/ata-Samsung_SSD_870_EVO_500GB_S7EWNL0X514734N"
SSD3="/dev/disk/by-id/ata-CT500MX500SSD1_2239E66B6612"

cleanup() {
  if [[ "$NO_CLEANUP" -eq 1 ]]; then
    log "Skipping cleanup due to --no-cleanup"
    return
  fi
  if zpool list -H -o name 2>/dev/null | awk '$1 == "'"$POOL"'" { found=1 } END { exit(found?0:1) }'; then
    log "Destroying pool ${POOL}"
    zpool destroy "$POOL" || true
  fi
}
trap cleanup EXIT INT TERM

LSPCI_ALL="$(lspci -nn)"
echo "$LSPCI_ALL" > "${OUTDIR}/lspci.txt"
lspci -tv > "${OUTDIR}/lspci-tree.txt" 2>&1 || true

if ! echo "$LSPCI_ALL" | grep -Eiq 'LSI|Broadcom|SAS2308'; then
  echo "Expected LSI/Broadcom SAS2308 not found in lspci output." >&2
  exit 1
fi

case "$SCENARIO" in
  hdd_mirror2x2)
    DISKS=("$HDD1" "$HDD2" "$HDD3" "$HDD4")
    POOLCMD=(zpool create -f "$POOL" mirror "${DISKS[0]}" "${DISKS[1]}" mirror "${DISKS[2]}" "${DISKS[3]}")
    ;;
  hdd_raidz1_4)
    DISKS=("$HDD1" "$HDD2" "$HDD3" "$HDD4")
    POOLCMD=(zpool create -f "$POOL" raidz1 "${DISKS[0]}" "${DISKS[1]}" "${DISKS[2]}" "${DISKS[3]}")
    ;;
  ssd_mirror3)
    DISKS=("$SSD1" "$SSD2" "$SSD3")
    POOLCMD=(zpool create -f "$POOL" mirror "${DISKS[0]}" "${DISKS[1]}" "${DISKS[2]}")
    ;;
  ssd_raidz1_3)
    DISKS=("$SSD1" "$SSD2" "$SSD3")
    POOLCMD=(zpool create -f "$POOL" raidz1 "${DISKS[0]}" "${DISKS[1]}" "${DISKS[2]}")
    ;;
esac

for d in "${DISKS[@]}"; do
  [[ -e "$d" ]] || { echo "Disk path not found: $d" >&2; exit 1; }
done

log "Running preflight checks"
ACTIVE_POOLS_FILE="${OUTDIR}/active-pools.txt"
zpool list -H -o name > "$ACTIVE_POOLS_FILE" 2>/dev/null || true

for d in "${DISKS[@]}"; do
  zpool status -P 2>/dev/null | grep -Fq "$d" && {
    echo "Refusing to proceed: disk appears in active zpool status: $d" >&2
    echo "See ${OUTDIR}/active-pools.txt and zpool status output." >&2
    exit 1
  }
done

{
  echo "=== TIMESTAMP ==="
  date
  echo
  echo "=== HOST ==="
  hostname
  uname -a
  echo
  echo "=== CARD LABEL ==="
  echo "$CARD"
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

if [[ "$PREFLIGHT_ONLY" -eq 1 ]]; then
  log "Preflight-only mode complete. No disk labels touched, no fio run."
  exit 0
fi

if [[ "$ALLOW_DESTROY" -ne 1 ]]; then
  echo "Safety stop: refusing destructive run without --allow-destroy" >&2
  echo "This test clears labels and creates a temporary ZFS pool on selected disks." >&2
  echo "Use --preflight-only first, then rerun with --allow-destroy when ready." >&2
  exit 1
fi

for d in "${DISKS[@]}"; do
  base="$(basename "$d")"
  smartctl -a "$d" > "${OUTDIR}/${base}.smart.before.txt" 2>&1 || true
done

for d in "${DISKS[@]}"; do
  zpool labelclear -f "$d" 2>/dev/null || true
done

log "Starting Stage 3 benchmark"
log "Card: $CARD"
log "Scenario: $SCENARIO"
log "Creating pool: ${POOLCMD[*]}"
"${POOLCMD[@]}"

zfs set compression=off "$POOL"
zfs set atime=off "$POOL"
zfs create -o mountpoint="$MOUNTPOINT" "$DATASET"
mkdir -p "$MOUNTPOINT"

zpool status "$POOL" > "${OUTDIR}/zpool-status-before.txt"
zfs list > "${OUTDIR}/zfs-list-before.txt"

TESTFILE="${MOUNTPOINT}/fio-testfile"

run_fio() {
  local name="$1"
  shift
  local file="${OUTDIR}/${name}.json"
  log "Running fio job: ${name}"
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

run_fio prefill \
  --rw=write \
  --bs=1M \
  --iodepth=16 \
  --numjobs=1 \
  --size=24G

sync
sleep 3

run_fio seq-read \
  --time_based=1 \
  --runtime="$RUNTIME" \
  --rw=read \
  --bs=1M \
  --iodepth=16 \
  --numjobs=1 \
  --size=24G

run_fio seq-write \
  --time_based=1 \
  --runtime="$RUNTIME" \
  --rw=write \
  --bs=1M \
  --iodepth=16 \
  --numjobs=1 \
  --size=24G

sync
sleep 3

run_fio rand-read-q1 \
  --time_based=1 \
  --runtime="$RUNTIME" \
  --rw=randread \
  --bs=4k \
  --iodepth=1 \
  --numjobs=1 \
  --size=8G

run_fio rand-read-q16 \
  --time_based=1 \
  --runtime="$RUNTIME" \
  --rw=randread \
  --bs=4k \
  --iodepth=16 \
  --numjobs=4 \
  --size=8G

run_fio rand-write-q16 \
  --time_based=1 \
  --runtime="$RUNTIME" \
  --rw=randwrite \
  --bs=4k \
  --iodepth=16 \
  --numjobs=4 \
  --size=8G

run_fio rand-mixed-70r30w-q16 \
  --time_based=1 \
  --runtime="$RUNTIME" \
  --rw=randrw \
  --rwmixread=70 \
  --bs=4k \
  --iodepth=16 \
  --numjobs=4 \
  --size=8G

run_fio rand-read-q32 \
  --time_based=1 \
  --runtime="$RUNTIME" \
  --rw=randread \
  --bs=4k \
  --iodepth=32 \
  --numjobs=8 \
  --size=8G

sync
sleep 5

for d in "${DISKS[@]}"; do
  base="$(basename "$d")"
  smartctl -a "$d" > "${OUTDIR}/${base}.smart.after.txt" 2>&1 || true
done

dmesg | tail -n 300 > "${OUTDIR}/dmesg-tail.txt" 2>&1 || true
zpool status "$POOL" > "${OUTDIR}/zpool-status-after.txt"
zfs list > "${OUTDIR}/zfs-list-after.txt"

log "Stage 3 benchmark completed. Output: ${OUTDIR}"
