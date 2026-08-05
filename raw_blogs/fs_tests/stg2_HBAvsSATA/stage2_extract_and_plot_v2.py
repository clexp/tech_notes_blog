import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent / "controller-logs"

records = []

SCENARIO_ORDER = [
    "6hdd_mirror3x2",
    "6hdd_raidz2_6",
    "2ssd_mirror2",
]

SCENARIO_LABELS = {
    "6hdd_mirror3x2": "6hdd_mirror",
    "6hdd_raidz2_6": "6hdd_raidz",
    "2ssd_mirror2": "2ssd_mirror",
}

TESTS = [
    ("seq-read", "read_bw_MBps", "Sequential Read Throughput", "MB/s"),
    ("seq-write", "write_bw_MBps", "Sequential Write Throughput", "MB/s"),
    ("rand-read-q1", "read_iops", "Random Read IOPS (q1)", "Read IOPS"),
    ("rand-read-q16", "read_iops", "Random Read IOPS (q16)", "Read IOPS"),
    ("rand-read-q32", "read_iops", "Random Read IOPS (q32)", "Read IOPS"),
    ("rand-write-q16", "write_iops", "Random Write IOPS (q16)", "Write IOPS"),
]


def detect_test(fname: str):
    name = fname.replace(".json", "")
    if name in {test_name for test_name, _, _, _ in TESTS}:
        return name
    return None


def extract_metrics(json_file: Path, controller: str, scenario: str, timestamp: str, test: str):
    with open(json_file) as f:
        data = json.load(f)

    job = data["jobs"][0]

    return {
        "controller": controller,
        "scenario": scenario,
        "timestamp": timestamp,
        "test": test,
        "read_bw_MBps": job["read"]["bw"] / 1024,   # fio reports KiB/s
        "write_bw_MBps": job["write"]["bw"] / 1024,
        "read_iops": job["read"]["iops"],
        "write_iops": job["write"]["iops"],
    }


# ------------------------------------------------------------
# Walk controller-logs
# Structure expected:
# controller-logs/<controller>/<scenario>/<timestamp>/*.json
# ------------------------------------------------------------
for controller_dir in BASE_DIR.iterdir():
    if not controller_dir.is_dir():
        continue

    controller = controller_dir.name

    for scenario_dir in controller_dir.iterdir():
        if not scenario_dir.is_dir():
            continue

        scenario = scenario_dir.name

        for run_dir in scenario_dir.iterdir():
            if not run_dir.is_dir():
                continue

            timestamp = run_dir.name

            for json_file in run_dir.glob("*.json"):
                test = detect_test(json_file.name)
                if test is None:
                    continue

                try:
                    records.append(
                        extract_metrics(json_file, controller, scenario, timestamp, test)
                    )
                except Exception as e:
                    print(f"Error reading {json_file}: {e}")

df = pd.DataFrame(records)

if df.empty:
    raise RuntimeError(f"No JSON benchmark files found under {BASE_DIR}")

df["scenario"] = pd.Categorical(df["scenario"], categories=SCENARIO_ORDER, ordered=True)

df.to_csv("stage2_results_runs.csv", index=False)
print("Saved stage2_results_runs.csv")


# ------------------------------------------------------------
# For now, use the latest run per controller+scenario+test
# ------------------------------------------------------------
df["timestamp_dt"] = pd.to_datetime(df["timestamp"], format="%Y%m%d-%H%M%S")

latest_df = (
    df.sort_values("timestamp_dt")
      .groupby(["controller", "scenario", "test"], as_index=False)
      .tail(1)
      .drop(columns=["timestamp_dt"])
      .sort_values(["controller", "scenario", "test"])
)

latest_df.to_csv("stage2_results_latest.csv", index=False)
print("Saved stage2_results_latest.csv")


def select_controllers(df_subset):
    controllers = sorted(df_subset["controller"].unique())
    lower = {name.lower(): name for name in controllers}

    asm = next((lower[name] for name in lower if "asm" in name), None)
    lsi = next((lower[name] for name in lower if "lsi" in name), None)

    if asm and lsi:
        return [asm, lsi]

    return controllers


def plot_scenario_comparison(latest_df, scenario, outfile):
    scenario_df = latest_df[latest_df["scenario"] == scenario].copy()
    if scenario_df.empty:
        print(f"Skipping {outfile}: no data for {scenario}")
        return

    controllers = select_controllers(scenario_df)
    if not controllers:
        print(f"Skipping {outfile}: no controllers found for {scenario}")
        return

    fig, axes = plt.subplots(3, 2, figsize=(12, 12))
    axes = axes.flatten()

    for idx, (test, metric, title, ylabel) in enumerate(TESTS):
        ax = axes[idx]
        test_df = scenario_df[scenario_df["test"] == test]

        values = []
        for controller in controllers:
            row = test_df[test_df["controller"] == controller]
            if row.empty:
                values.append(float("nan"))
            else:
                values.append(row[metric].iloc[0])

        ax.bar(controllers, values)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.tick_params(axis="x", rotation=20)

    label = SCENARIO_LABELS.get(scenario, scenario)
    fig.suptitle(f"Stage 2: ASM1166 vs LSI HBA ({label})")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(outfile, dpi=150)
    plt.close(fig)
    print(f"Saved {outfile}")


for scenario in SCENARIO_ORDER:
    label = SCENARIO_LABELS.get(scenario, scenario)
    plot_scenario_comparison(
        latest_df,
        scenario,
        f"stage2_compare_{label}.png",
    )

print("All Stage 2 comparison plots generated.")
