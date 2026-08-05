# Stage 3 — HBA temperature log

External IR readings (Linux does not expose SAS2308 junction temp on this host). Record **ambient** every run so **Δ vs room** is comparable across cards and days.

## Measurement protocol

| Field              | How to record                                                                                                                                                           |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **IR spot**        | Same physical point on heatsink/PCB each time (note in _Notes_).                                                                                                        |
| **Ambient**        | Room air at start; same thermometer position for all runs.                                                                                                              |
| **At rest**        | HBA after idle ≥ 10 min, no fio/ZFS stress.                                                                                                                             |
| **During test**    | Peak (or spot-check) IR; ideally log every **60 s** in a second shell: `while true; do date -Is; sensors 2>/dev/null \| head -5; sleep 60; done >> thermal-samples.log` |
| **End of run**     | IR within **2 min** of `run.log` “benchmark completed”.                                                                                                                 |
| **Cooling / case** | Fan curve, side panel open/closed — keep consistent between refurb and clone.                                                                                           |

**Δ ambient** = reading − ambient (°C).

---

## Refurb card

| Scenario / run folder | Date (start) | Ambient °C | At rest °C | Peak / during °C | CPU temp °C | Δ end vs amb | NVME °C |
| --------------------- | ------------ | ---------- | ---------- | ---------------- | ----------- | ------------ | ------- |
| `hdd_mirror2x2`       | 6/5/26       | 18.0       | 77.2       | 77.2             | 38.0        | 59.2         | 47.9    |
| `hdd_raidz1_4`        | 7/5/26       | 17.8       | 76.4       | 76.6             | 39.0        | 58.8         | 48.9    |
| `ssd_mirror3`         | 7/5/26       | 18.0       | 76.6       | 78.4             | 42.0        | 60.4         | 48.9    |
| `ssd_raidz1_3`        | 8/5/26       | 19.0       | 78.2       | 78.2             | 43.0        | 59.2         | 49.9    |
| `combined`            | 8/5/26       | 19.0       | 79.8       | 79.0             | 43.0        | 60.0         | 49.9    |

---

## Clone card

| Scenario / run folder | Date (start) | Ambient °C | At rest °C | Peak / during °C | CPU temp °C | Δ end vs amb | NVME °C |
| --------------------- | ------------ | ---------- | ---------- | ---------------- | ----------- | ------------ | ------- |
| `ssd_mirror3`         | 2/5/26       | 20.0       | 78.6       | 79.6             | 40.0        | 59.6         | 47.9    |
| `hdd_mirror2x2`       | 6/5/26       | 18.4       | 78.6       | 78.6             | 38.0        | 60.2         | 46.9    |
| `hdd_raidz1_4`        | 4/5/26       | 18.0       | 78.0       | 78.2             | 38.0        | 60.2         | 47.9    |
| `ssd_raidz1_3`        | 3/5/26       | 19.0       | 78.0       | 78.6             | 39.0        | 59.6         | 46.9    |
| `combined`            | 4/5/26       | 18.2       | 77.0       | 78.8             | 35.0        | 60.6         | 47.9    |

### Logged readings (migrate as you fill the table)

- _At rest:_ 78.6 °C with room **20.0 °C** (Δ end vs amb **58.6 °C**) — _card label TBD if this was refurb or clone; fill when known._
- _During `ssd_mirror3`:_ **79.6 °C** with room **20.0 °C** (Δ **59.6 °C**); run ~**2 h 15 min**; ~**+1.0 °C** vs at rest on that day.

---

## Retest checklist (HDD + ambient)

- [ ] Ambient recorded at **start** of HDD run (and optional end).
- [ ] HBA **at rest** before `hdd_mirror2x2` / `hdd_raidz1_4`.
- [ ] Optional **peak** during heaviest phase (e.g. `rand-write-q16` or RAID-Z seq write).
- [ ] **End** IR aligned with `run.log` completion.
- [ ] Same IR spot and case/fan conditions as SSD leg.

---

## Optional host context (same timestamp as IR peak)

```text
sensors
```

Paste a one-line summary in _Notes_ if useful (CPU package / NVMe — not HBA die).
