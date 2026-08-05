from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
AVG_CSV = BASE_DIR / "stage3_results_avg.csv"
PLOTS_DIR = BASE_DIR / "plots_stage3"

SCENARIO_ORDER = [
    "hdd_mirror2x2",
    "hdd_raidz1_4",
    "ssd_mirror3",
    "ssd_raidz1_3",
    "combined_hdd_mirror2x2",
    "combined_ssd_mirror3",
]

SCENARIO_LABELS = {
    "hdd_mirror2x2": "HDD mirror2x2",
    "hdd_raidz1_4": "HDD raidz1_4",
    "ssd_mirror3": "SSD mirror3",
    "ssd_raidz1_3": "SSD raidz1_3",
    "combined_hdd_mirror2x2": "Combined-HDD",
    "combined_ssd_mirror3": "Combined-SSD",
}

CARDS = ["refurb", "clone"]
CARD_COLORS = {
    "refurb": "#1f77b4",  # blue
    "clone": "#2ca02c",   # green
}

# One chart per metric, as requested.
PLOTS = [
    ("seq-read", "read_bw_MBps_mean", "Sequential Read Throughput", "MB/s"),
    ("seq-write", "write_bw_MBps_mean", "Sequential Write Throughput", "MB/s"),
    ("rand-read-q1", "read_iops_mean", "Random Read IOPS (Q1)", "IOPS"),
    ("rand-read-q16", "read_iops_mean", "Random Read IOPS (Q16)", "IOPS"),
    ("rand-read-q32", "read_iops_mean", "Random Read IOPS (Q32)", "IOPS"),
    ("rand-write-q16", "write_iops_mean", "Random Write IOPS (Q16)", "IOPS"),
    (
        "rand-mixed-70r30w-q16",
        "read_iops_mean",
        "Random Mixed 70R/30W — Read IOPS (Q16)",
        "Read IOPS",
    ),
    (
        "rand-mixed-70r30w-q16",
        "write_iops_mean",
        "Random Mixed 70R/30W — Write IOPS (Q16)",
        "Write IOPS",
    ),
]


def main() -> None:
    if not AVG_CSV.exists():
        raise RuntimeError(f"Missing {AVG_CSV}. Run stage3_aggregate_runs.py first.")

    df = pd.read_csv(AVG_CSV)
    PLOTS_DIR.mkdir(exist_ok=True)

    for test, metric_col, title, ylabel in PLOTS:
        sub = df[df["test"] == test].copy()
        if sub.empty:
            print(f"[skip] no data for {test}")
            continue

        scenarios = [s for s in SCENARIO_ORDER if s in set(sub["scenario"])]
        if not scenarios:
            print(f"[skip] no scenarios found for {test}")
            continue

        x = np.arange(len(scenarios))
        width = 0.36

        fig, ax = plt.subplots(figsize=(11, 5))

        for i, card in enumerate(CARDS):
            vals = []
            errs = []
            offset = -width / 2 if i == 0 else width / 2
            for scenario in scenarios:
                row = sub[(sub["scenario"] == scenario) & (sub["card"] == card)]
                if row.empty:
                    vals.append(np.nan)
                    errs.append(0.0)
                else:
                    vals.append(row.iloc[0][metric_col])
                    std_col = metric_col.replace("_mean", "_std")
                    errs.append(float(row.iloc[0].get(std_col, 0.0) or 0.0))
            ax.bar(
                x + offset,
                vals,
                width=width,
                label=card,
                color=CARD_COLORS[card],
                yerr=errs,
                capsize=3,
                alpha=0.92,
            )

        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels([SCENARIO_LABELS.get(s, s) for s in scenarios], rotation=20, ha="right")
        ax.grid(axis="y", alpha=0.25)
        ax.legend()
        fig.tight_layout()

        out = PLOTS_DIR / f"stage3_{test}_{metric_col.replace('_mean','')}.png"
        fig.savefig(out, dpi=150)
        plt.close(fig)
        print(f"Saved {out}")

    # Optional quick temperature summary chart from temps.md is left manual by design.
    # You are using temps.md as source-of-truth notes, and values are sparse/manual.


if __name__ == "__main__":
    main()
