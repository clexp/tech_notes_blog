#!/bin/bash
set -euo pipefail

ARCH="${1:-}"

if [[ -z "$ARCH" ]]; then
    echo "ERROR: Architecture name required."
    exit 1
fi

command -v fio >/dev/null 2>&1 || { echo "ERROR: fio not installed"; exit 1; }

TS=$(date +%Y%m%d-%H%M%S)
OUTDIR="logs/$ARCH"
mkdir -p "$OUTDIR"
SUMMARY="$OUTDIR/summary.md"

DATASET="/benchpool/test"

# ------------------------------------------------------------
# Metadata capture (NEW)
# ------------------------------------------------------------
META="$OUTDIR/${TS}-run-meta.txt"

echo "ARCH=$ARCH" > "$META"
echo "TIMESTAMP=$TS" >> "$META"
echo "HOST=$(hostname)" >> "$META"
echo "KERNEL=$(uname -r)" >> "$META"
echo "DATASET=$DATASET" >> "$META"
echo "DISKS=${ZFS_TEST_DISKS}" >> "$META"
echo "" >> "$META"

TESTFILE="${DATASET}/fio-testfile"


if [[ ! -d "$DATASET" ]]; then
    echo "ERROR: Dataset path does not exist: $DATASET"
    exit 1
fi

echo "Running ZFS architecture test for: $ARCH"
echo "Output directory: $OUTDIR"

{
    echo "timestamp=$TS"
    echo "arch=$ARCH"
    echo "host=$(hostname)"
    echo "dataset=$DATASET"
    echo "testfile=$TESTFILE"
    echo "fio_version=$(fio --version)"
    echo
    echo "[zpool list]"
    zpool list
    echo
    echo "[zpool status]"
    zpool status benchpool
    echo
    echo "[zfs list]"
    zfs list
} > "$META"

run_fio() {
    local name="$1"
    shift
    local file="$OUTDIR/${TS}-${name}.json"

    echo "Running fio job: $name"
    fio \
        --name="$name" \
        --filename="$TESTFILE" \
        --output-format=json \
        --output="$file" \
        --ioengine=libaio \
        --direct=1 \
        --time_based=1 \
        --runtime=60 \
        --group_reporting=1 \
        "$@"
}

# -------------------------------------------------------------------
# 0. Pre-fill test file
# -------------------------------------------------------------------
# Ensures read tests actually read something real.
# 16G is large enough to avoid tiny-cache silliness, but still practical.
echo "Pre-filling test file..."
fio \
    --name="prefill" \
    --filename="$TESTFILE" \
    --output-format=json \
    --output="$OUTDIR/${TS}-prefill.json" \
    --ioengine=libaio \
    --direct=1 \
    --rw=write \
    --bs=1M \
    --iodepth=16 \
    --size=16G \
    --numjobs=1 \
    --group_reporting=1

sync
sleep 3

# -------------------------------------------------------------------
# 1. Sequential throughput
# -------------------------------------------------------------------
echo "Running sequential throughput tests..."

run_fio "seq-read" \
    --rw=read \
    --bs=1M \
    --iodepth=16 \
    --numjobs=1 \
    --size=16G

run_fio "seq-write" \
    --rw=write \
    --bs=1M \
    --iodepth=16 \
    --numjobs=1 \
    --size=16G

sync
sleep 3

# -------------------------------------------------------------------
# 2. Random IOPS / latency
# -------------------------------------------------------------------
echo "Running random IOPS tests..."

run_fio "rand-read" \
    --rw=randread \
    --bs=4k \
    --iodepth=16 \
    --numjobs=4 \
    --size=8G

run_fio "rand-write" \
    --rw=randwrite \
    --bs=4k \
    --iodepth=16 \
    --numjobs=4 \
    --size=8G

run_fio "rand-mixed-70r30w" \
    --rw=randrw \
    --rwmixread=70 \
    --bs=4k \
    --iodepth=16 \
    --numjobs=4 \
    --size=8G

sync
sleep 3

# -------------------------------------------------------------------
# 3. Append summary index
# -------------------------------------------------------------------
{
    echo "## Test Run: $ARCH — $TS"
    echo
    echo "- Meta: ${TS}-run-meta.txt"
    echo "- Prefill: ${TS}-prefill.json"
    echo "- Sequential read: ${TS}-seq-read.json"
    echo "- Sequential write: ${TS}-seq-write.json"
    echo "- Random read: ${TS}-rand-read.json"
    echo "- Random write: ${TS}-rand-write.json"
    echo "- Mixed 70/30: ${TS}-rand-mixed-70r30w.json"
    echo
} >> "$SUMMARY"

echo "Test suite completed for: $ARCH"
