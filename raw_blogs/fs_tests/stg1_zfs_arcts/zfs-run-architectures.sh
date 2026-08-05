#!/bin/bash
set -euo pipefail

source ./architectures.sh
TESTSCRIPT="./zfs-arch-test.sh"
POOL="benchpool"
DATASET="${POOL}/test"
MOUNTPOINT="/benchpool/test"
RUNLOG="arch_run-$(date +%Y%m%d-%H%M).log"

DISK1="/dev/disk/by-id/ata-Hitachi_HTS547550A9E384_J2160051E1A4ZD"
DISK2="/dev/disk/by-id/ata-ST3500312CS_5VVRKGAV"
DISK3="/dev/disk/by-id/ata-ST3500418AS_Z2ACPF1Z"
DISK4="/dev/disk/by-id/ata-ST500DM002-1BD142_Z2AFGE69"
DISK5="/dev/disk/by-id/ata-ST500DM002-1BD142_W3TQFS8T"
DISK6="/dev/disk/by-id/ata-ST500DM002-1BD142_W3TQ01LD"

log() {
  echo "[$(date '+%F %T')] $1" | tee -a "$RUNLOG"
}

cleanup() {
  if zpool list -H -o name 2>/dev/null | grep -qx "$POOL"; then
    log "Cleanup: destroying leftover pool $POOL"
    zpool destroy "$POOL" || true
  fi
}
trap cleanup EXIT INT TERM

require_file() {
  [[ -f "$1" ]] || { echo "Missing required file: $1" >&2; exit 1; }
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { echo "Missing command: $1" >&2; exit 1; }
}

require_file ./architectures.sh
require_file "$TESTSCRIPT"
require_cmd zpool
require_cmd zfs
require_cmd fio

for d in "$DISK1" "$DISK2" "$DISK3" "$DISK4" "$DISK5" "$DISK6"; do
  [[ -e "$d" ]] || { echo "Disk path not found: $d" >&2; exit 1; }
done

for ARCH in "${ARCH_LIST[@]}"; do
  log "========== Starting architecture: $ARCH =========="
  log "Disk set:"
  log "  $DISK1"
  log "  $DISK2"
  log "  $DISK3"
  log "  $DISK4"
  log "  $DISK5"
  log "  $DISK6"

  if zpool list -H -o name 2>/dev/null | grep -qx "$POOL"; then
    log "Destroying existing pool $POOL before new run"
    zpool destroy "$POOL"
  fi

  case "$ARCH" in
    single)
      POOLCMD=(zpool create -f "$POOL" "$DISK1")
      ;;
    mirror2)
      POOLCMD=(zpool create -f "$POOL" mirror "$DISK1" "$DISK2")
      ;;
    mirror2x2)
      POOLCMD=(zpool create -f "$POOL" mirror "$DISK1" "$DISK2") 
      ;;
    mirror3x2)
      POOLCMD=(
        zpool create -f "$POOL"
        mirror "$DISK1" "$DISK2"
        mirror "$DISK3" "$DISK4"
        mirror "$DISK5" "$DISK6"
      )
      ;;
    raidz1_3)
      POOLCMD=(zpool create -f "$POOL" raidz1 "$DISK1" "$DISK2" "$DISK3")
      ;;
    raidz2_4)
      POOLCMD=(zpool create -f "$POOL" raidz2 "$DISK1" "$DISK2" "$DISK3" "$DISK4")
      ;;
    raidz2_6)
      POOLCMD=(zpool create -f "$POOL" raidz2 "$DISK1" "$DISK2" "$DISK3" "$DISK4" "$DISK5" "$DISK6")
      ;;
    mirror2_fast_fast)
      POOLCMD=(
        zpool create -f "$POOL"
        mirror "$DISK5" "$DISK6"
      )
      ;;
    mirror2_slow_slow)
      POOLCMD=(
        zpool create -f "$POOL"
        mirror "$DISK2" "$DISK3"
      )
      ;;
    mirror2_fast_slow)
      POOLCMD=(
        zpool create -f "$POOL"
        mirror "$DISK2" "$DISK5"
      )
      ;;
    mirror2_laptop_fast)
      POOLCMD=(
        zpool create -f "$POOL"
        mirror "$DISK1" "$DISK6"
      )
      ;;
    *)
      echo "Unknown architecture: $ARCH" >&2
      exit 1
      ;;
  esac

  for d in "$DISK1" "$DISK2" "$DISK3" "$DISK4" "$DISK5" "$DISK6"; do
    zpool labelclear -f "$d" 2>/dev/null || true
  done

  log "Creating pool: ${POOLCMD[*]}"
  "${POOLCMD[@]}"

  zfs set compression=off "$POOL"
  zfs set atime=off "$POOL"

  if zfs list -H -o name "$DATASET" >/dev/null 2>&1; then
    zfs destroy "$DATASET"
  fi

  zfs create -o mountpoint="$MOUNTPOINT" "$DATASET"
  mkdir -p "$MOUNTPOINT"

  log "zpool status for $ARCH:"
  zpool status "$POOL" | tee -a "$RUNLOG"

  log "Running performance tests for $ARCH"
  
  export ZFS_TEST_DISKS="$DISK1 $DISK2 $DISK3 $DISK4 $DISK5 $DISK6"
  "$TESTSCRIPT" "$ARCH"

  sync
  sleep 5

  log "Destroying pool for $ARCH"
  zpool destroy "$POOL"

  log "========== Completed: $ARCH =========="
done

log "All architectures tested."
