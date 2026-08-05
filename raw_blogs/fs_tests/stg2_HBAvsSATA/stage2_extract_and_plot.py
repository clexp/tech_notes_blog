import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path("controller-logs")

records = []

SCENARIO_ORDER = [
    "6hdd_mirror3x2",
    "6hdd_raidz2_6",
    "2ssd_mirror2",
]


def detect_test(fname: str):
    name = fname.replace(".json", "")
    if name in {
        "prefill",
        "seq-read",
        "seq-write",
        "rand-read-q1",
        "rand-read-q16",
        "rand-read-q32",
        "rand-write-q16",
        "rand-mixed-70r30w-q16",
    }:
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


# ------------------------------------------------------------
# Plot helper
# ------------------------------------------------------------
def plot_metric(latest_df, test, metric, title, ylabel, outfile):
    subset = latest_df[latest_df["test"] == test].copy()
    if subset.empty:
        print(f"Skipping {outfile}: no data for {test}")
        return

    # x-axis labels like lsi-import\n6hdd_mirror3x2
    subset["label"] = (
        subset["controller"].astype(str) + "\n" + subset["scenario"].astype(str)
    )

    plt.figure(figsize=(10, 5))
    plt.bar(subset["label"], subset[metric])
    plt.xticks(rotation=45, ha="right")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outfile, dpi=150)
    plt.close()
    print(f"Saved {outfile}")


# ------------------------------------------------------------
# Core plots
# ------------------------------------------------------------
plot_metric(
    latest_df, "seq-read", "read_bw_MBps",
    "Stage 2: Sequential Read Throughput",
    "MB/s", "stage2_seq_read_bw.png"
)

plot_metric(
    latest_df, "seq-write", "write_bw_MBps",
    "Stage 2: Sequential Write Throughput",
    "MB/s", "stage2_seq_write_bw.png"
)

plot_metric(
    latest_df, "rand-read-q16", "read_iops",
    "Stage 2: Random Read IOPS (q16)",
    "Read IOPS", "stage2_rand_read_q16_iops.png"
)

plot_metric(
    latest_df, "rand-read-q1", "read_iops",
    "Stage 2: Random Read IOPS (q1)",
    "Read IOPS", "stage2_rand_read_q1_iops.png"
)

plot_metric(
    latest_df, "rand-read-q32", "read_iops",
    "Stage 2: Random Read IOPS (q32)",
    "Read IOPS", "stage2_rand_read_q32_iops.png"
)

plot_metric(
    latest_df, "rand-write-q16", "write_iops",
    "Stage 2: Random Write IOPS (q16)",
    "Write IOPS", "stage2_rand_write_q16_iops.png"
)

print("All Stage 2 plots generated.")
