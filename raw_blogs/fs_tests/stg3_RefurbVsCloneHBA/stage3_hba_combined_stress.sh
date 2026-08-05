#!/usr/bin/env bash
set -euo pipefail

# Stage 3 optional: saturate BOTH HBA SAS chains at once (HDD pool + SSD pool, parallel fio).
# Keep disk IDs in sync with stage3_hba_compare.sh.

PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH}"
export PATH

POOL_HDD="stage3pool_mix_hdd"
POOL_SSD="stage3pool_mix_ssd"
DS_HDD="${POOL_HDD}/test"
DS_SSD="${POOL_SSD}/test"
MP_HDD="/${POOL_HDD}/test"
MP_SSD="/${POOL_SSD}/test"
RUNROOT="stage3-logs-combined"

CARD=""
RUNTIME=90
ALLOW_DESTROY=0
PREFLIGHT_ONLY=0
DETACH=0
THERMAL_INTERVAL=10
THERMAL_PID="" # set when thermal sampler starts; cleanup must tolerate early exit (set -u)
POOLS_CREATED=0

usage() {
  cat <<'EOF'
Usage:
  stage3_hba_combined_stress.sh --card <refurb|clone> [options]

Options:
  --runtime-sec <n>        Per-job runtime for time-based fio tests (default: 90)
  --thermal-interval <s>   Seconds between thermal snapshots (default: 10)
  --detach                 run in background via nohup; monitor with run.log
  --allow-destroy          REQUIRED for pool create / labelclear (destructive)
  --preflight-only         Inventory + checks only
  --help                   Show this help

Layouts (fixed):
  HDD: mirror pair + mirror pair (same four disks as hdd_mirror2x2)
  SSD: 3-way mirror (same three disks as ssd_mirror3)

Outputs under stage3-logs-combined/<card>/<timestamp>/:
  run.log, thermal.log, dmesg-tail.txt, hdd/*.json, ssd/*.json, inventory.txt

Notes:
  - Run as root. For adapter chip temperature, install lm-sensors and run sensors-detect,
    or continue external IR readings; this script logs sysfs thermal zones + sensors if present.
  - Interpret combined runs as stress/saturation — compare refurb vs clone using the same script.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --card) CARD="${2:-}"; shift 2 ;;
    --runtime-sec) RUNTIME="${2:-}"; shift 2 ;;
    --thermal-interval) THERMAL_INTERVAL="${2:-}"; shift 2 ;;
    --detach) DETACH=1; shift ;;
    --allow-destroy) ALLOW_DESTROY=1; shift ;;
    --preflight-only) PREFLIGHT_ONLY=1; shift ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown: $1" >&2; usage; exit 1 ;;
  esac
done

[[ "$CARD" == "refurb" || "$CARD" == "clone" ]] || { usage; exit 1; }
[[ "$RUNTIME" =~ ^[0-9]+$ ]] || { echo "runtime must be integer" >&2; exit 1; }
[[ "$THERMAL_INTERVAL" =~ ^[0-9]+$ ]] || { echo "thermal-interval must be integer" >&2; exit 1; }

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }
}
for cmd in zpool zfs fio lsblk lspci smartctl awk mkdir date; do
  require_cmd "$cmd"
done

# --- Disk IDs (sync with stage3_hba_compare.sh) ---
HDD1="/dev/disk/by-id/ata-ST4000VN008-2DR166_ZM41ATFP"
HDD2="/dev/disk/by-id/ata-ST4000VN008-2DR166_ZDHA5A7S"
HDD3="/dev/disk/by-id/ata-ST4000VN008-2DR166_ZDHA5GF5"
HDD4="/dev/disk/by-id/ata-ST4000VN008-2DR166_ZGY7WERC"
SSD1="/dev/disk/by-id/ata-Samsung_SSD_860_EVO_500GB_S3Z2NB1K910954L"
SSD2="/dev/disk/by-id/ata-Samsung_SSD_870_EVO_500GB_S7EWNL0X514734N"
SSD3="/dev/disk/by-id/ata-CT500MX500SSD1_2239E66B6612"

DISKS_HDD=("$HDD1" "$HDD2" "$HDD3" "$HDD4")
DISKS_SSD=("$SSD1" "$SSD2" "$SSD3")

mkdir -p "$RUNROOT"
if [[ -n "${STAGE3_OUTDIR:-}" ]]; then
  OUTDIR="$STAGE3_OUTDIR"
  LOGFILE="${OUTDIR}/run.log"
  THERMAL_LOG="${OUTDIR}/thermal.log"
elif [[ "$DETACH" -eq 1 && "${STAGE3_DETACHED:-0}" != "1" ]]; then
  TS="$(date +%Y%m%d-%H%M%S)"
  OUTDIR="${RUNROOT}/${CARD}/${TS}"
  mkdir -p "$OUTDIR/hdd" "$OUTDIR/ssd"
  LOGFILE="${OUTDIR}/run.log"
  THERMAL_LOG="${OUTDIR}/thermal.log"
  ABS_OUT="$(cd "$OUTDIR" && pwd)"
  echo "Detaching combined run."
  echo "  Log file:    ${LOGFILE}"
  echo "  Output dir:  ${ABS_OUT}"
  echo "  Monitor:     tail -f \"${LOGFILE}\""
  STAGE3_DETACHED=1 STAGE3_OUTDIR="$OUTDIR" nohup "$0" \
    --card "$CARD" \
    --runtime-sec "$RUNTIME" \
    --thermal-interval "$THERMAL_INTERVAL" \
    $([[ "$ALLOW_DESTROY" -eq 1 ]] && echo "--allow-destroy") \
    $([[ "$PREFLIGHT_ONLY" -eq 1 ]] && echo "--preflight-only") \
    >"$LOGFILE" 2>&1 < /dev/null &
  worker_pid=$!
  echo "$worker_pid" > "${OUTDIR}/run.pid"
  echo "Started worker PID ${worker_pid} (saved ${OUTDIR}/run.pid)"
  exit 0
else
  TS="$(date +%Y%m%d-%H%M%S)"
  OUTDIR="${RUNROOT}/${CARD}/${TS}"
  mkdir -p "$OUTDIR/hdd" "$OUTDIR/ssd"
  LOGFILE="${OUTDIR}/run.log"
  THERMAL_LOG="${OUTDIR}/thermal.log"
fi

log() {
  local line="[$(date '+%F %T')] $*"
  if [[ "${STAGE3_DETACHED:-0}" == "1" ]] || [[ ! -t 1 ]]; then
    echo "$line" >> "$LOGFILE"
  else
    echo "$line" | tee -a "$LOGFILE"
  fi
}

thermal_loop() {
  local stop="$1"
  while [[ ! -f "$stop" ]]; do
    {
      echo "=== $(date -Is) ==="
      if command -v sensors >/dev/null 2>&1; then
        sensors || true
      else
        echo "(sensors not installed — apt install lm-sensors)"
      fi
      for z in /sys/class/thermal/thermal_zone*/temp; do
        [[ -r "$z" ]] || continue
        printf '%s %s\n' "$z" "$(cat "$z" 2>/dev/null)"
      done
      echo
    } >>"$THERMAL_LOG" 2>&1 || true
    sleep "$THERMAL_INTERVAL"
  done
}

cleanup() {
  touch "${OUTDIR}/.thermal_stop" 2>/dev/null || true
  if [[ -n "${THERMAL_PID:-}" ]]; then
    kill "$THERMAL_PID" 2>/dev/null || true
    wait "$THERMAL_PID" 2>/dev/null || true
  fi
  rm -f "${OUTDIR}/.thermal_stop" 2>/dev/null || true
  if [[ "${SKIP_DESTROY:-0}" -eq 1 || "$POOLS_CREATED" -ne 1 ]]; then
    return
  fi
  for p in "$POOL_HDD" "$POOL_SSD"; do
    if zpool list -H -o name 2>/dev/null | awk -v n="$p" '$1==n{m=1}END{exit m?0:1}'; then
      log "Destroying pool ${p}"
      zpool destroy "$p" || true
    fi
  done
}

trap cleanup EXIT INT TERM

LSPCI_ALL="$(lspci -nn)"
echo "$LSPCI_ALL" >"${OUTDIR}/lspci.txt"
lspci -tv >"${OUTDIR}/lspci-tree.txt" 2>&1 || true
if ! echo "$LSPCI_ALL" | grep -Eiq 'LSI|Broadcom|SAS2308'; then
  echo "Expected LSI/Broadcom SAS2308 not found." >&2
  exit 1
fi

for d in "${DISKS_HDD[@]}" "${DISKS_SSD[@]}"; do
  [[ -e "$d" ]] || { echo "Missing disk: $d" >&2; exit 1; }
done

{
  echo "=== TIMESTAMP ==="; date
  echo "=== CARD ==="; echo "$CARD"
  echo "=== COMBINED STRESS ==="; echo "HDD pool=$POOL_HDD (2x mirror vdev)"; echo "SSD pool=$POOL_SSD (3-way mirror)"
  echo "=== LSBLK ==="; lsblk -o NAME,TYPE,SIZE,MODEL,SERIAL,TRAN,MOUNTPOINTS
} >"${OUTDIR}/inventory.txt"

log "Preflight: checking disks not busy in zpool status"
for d in "${DISKS_HDD[@]}" "${DISKS_SSD[@]}"; do
  zpool status -P 2>/dev/null | grep -Fq "$d" && {
    echo "Disk in use: $d" >&2
    exit 1
  }
done

if [[ "$PREFLIGHT_ONLY" -eq 1 ]]; then
  log "Preflight-only done."
  SKIP_DESTROY=1
  exit 0
fi

if [[ "$ALLOW_DESTROY" -ne 1 ]]; then
  echo "Refusing destructive run without --allow-destroy" >&2
  exit 1
fi

rm -f "${OUTDIR}/.thermal_stop"
thermal_loop "${OUTDIR}/.thermal_stop" &
THERMAL_PID=$!

finish_thermal() {
  touch "${OUTDIR}/.thermal_stop"
}

run_dual_fio() {
  local name="$1"
  shift
  log "Combined phase: ${name} (parallel HDD + SSD)"
  set +e
  fio \
    --name="${name}_hdd" \
    --filename="${FILE_HDD}" \
    --output-format=json \
    --output="${OUTDIR}/hdd/${name}.json" \
    --ioengine=libaio \
    --direct=1 \
    --group_reporting=1 \
    "$@" &
  pid_a=$!
  fio \
    --name="${name}_ssd" \
    --filename="${FILE_SSD}" \
    --output-format=json \
    --output="${OUTDIR}/ssd/${name}.json" \
    --ioengine=libaio \
    --direct=1 \
    --group_reporting=1 \
    "$@" &
  pid_b=$!
  wait "$pid_a"
  code_a=$?
  wait "$pid_b"
  code_b=$?
  set -e
  if [[ "$code_a" -ne 0 || "$code_b" -ne 0 ]]; then
    log "ERROR: fio phase ${name} failed (hdd_exit=${code_a} ssd_exit=${code_b})"
    exit 1
  fi
}

log "Creating pools"
for d in "${DISKS_HDD[@]}" "${DISKS_SSD[@]}"; do
  zpool labelclear -f "$d" 2>/dev/null || true
done

zpool create -f "$POOL_HDD" mirror "$HDD1" "$HDD2" mirror "$HDD3" "$HDD4"
zpool create -f "$POOL_SSD" mirror "$SSD1" "$SSD2" "$SSD3"
POOLS_CREATED=1

zfs set compression=off "$POOL_HDD" "$POOL_SSD"
zfs set atime=off "$POOL_HDD" "$POOL_SSD"
zfs create -o mountpoint="$MP_HDD" "$DS_HDD"
zfs create -o mountpoint="$MP_SSD" "$DS_SSD"
mkdir -p "$MP_HDD" "$MP_SSD"

FILE_HDD="${MP_HDD}/fio-testfile"
FILE_SSD="${MP_SSD}/fio-testfile"

zpool status "$POOL_HDD" "$POOL_SSD" >"${OUTDIR}/zpool-status-before.txt"
zfs list >"${OUTDIR}/zfs-list-before.txt"

run_dual_fio prefill \
  --rw=write \
  --bs=1M \
  --iodepth=16 \
  --numjobs=1 \
  --size=24G

sync
sleep 3

run_dual_fio seq-read \
  --time_based=1 \
  --runtime="$RUNTIME" \
  --rw=read \
  --bs=1M \
  --iodepth=16 \
  --numjobs=1 \
  --size=24G

run_dual_fio seq-write \
  --time_based=1 \
  --runtime="$RUNTIME" \
  --rw=write \
  --bs=1M \
  --iodepth=16 \
  --numjobs=1 \
  --size=24G

sync
sleep 3

run_dual_fio rand-read-q16 \
  --time_based=1 \
  --runtime="$RUNTIME" \
  --rw=randread \
  --bs=4k \
  --iodepth=16 \
  --numjobs=4 \
  --size=8G

run_dual_fio rand-write-q16 \
  --time_based=1 \
  --runtime="$RUNTIME" \
  --rw=randwrite \
  --bs=4k \
  --iodepth=16 \
  --numjobs=4 \
  --size=8G

sync
sleep 5

zpool status "$POOL_HDD" "$POOL_SSD" >"${OUTDIR}/zpool-status-after.txt"
zfs list >"${OUTDIR}/zfs-list-after.txt"
dmesg | tail -n 400 >"${OUTDIR}/dmesg-tail.txt" 2>&1 || true

finish_thermal
wait "$THERMAL_PID" 2>/dev/null || true
THERMAL_PID=""

log "Combined stress completed: ${OUTDIR}"
