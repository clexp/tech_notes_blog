#!/bin/bash

OUTPUT="smart-summary-$(date +%Y%m%d-%H%M).txt"
echo "ZFS Test Disk SMART Summary - $(date)" > "$OUTPUT"
echo "==========================================" >> "$OUTPUT"
echo "" >> "$OUTPUT"

# Identify all SATA disks (exclude NVMe)
DISKS=$(lsblk -nd -o NAME | grep -E '^sd')

for DISK in $DISKS; do
    DEVICE="/dev/$DISK"
    echo "Collecting SMART data for $DEVICE..." >> "$OUTPUT"
    echo "------------------------------------------" >> "$OUTPUT"

    smartctl -a "$DEVICE" | awk '
        /Device Model:/ {print "Model: " $3, $4, $5}
        /Serial Number:/ {print "Serial: " $3}
        /SATA Version is:/ {print "SATA Version: " $0}
        /Power_On_Hours/ {print "Power-On Hours: " $10}
        /Power_Cycle_Count/ {print "Power Cycle Count: " $10}
        /Reallocated_Sector_Ct/ {print "Reallocated Sectors: " $10}
        /Current_Pending_Sector/ {print "Pending Sectors: " $10}
        /SMART overall-health/ {print "Overall SMART Status: " $0}
        /Self-test execution status/ {print "Last Self-Test: " $0}
    ' >> "$OUTPUT"

    echo "" >> "$OUTPUT"
done

echo "SMART summary written to $OUTPUT"

