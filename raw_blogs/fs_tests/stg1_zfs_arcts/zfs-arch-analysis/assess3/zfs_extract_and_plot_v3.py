import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path("../../logs")

CORE_ARCH_ORDER = [
    "single",
    "mirror2",
    "mirror2x2",
    "mirror3x2",
    "raidz1_3",
    "raidz2_4",
    "raidz2_6",
]

records = []


def split_architecture(arch_name: str):
    if arch_name == "mirror2":
        return "mirror2", "baseline"

    if arch_name.startswith("mirror2_"):
        return "mirror2", arch_name.replace("mirror2_", "", 1)

    return arch_name, "baseline"


def detect_test(fname: str):
    if "seq-read" in fname:
        return "seq-read"
    if "seq-write" in fname:
        return "seq-write"
    if "rand-read" in fname and "mixed" not in fname:
        return "rand-read"
    if "rand-write" in fname:
        return "rand-write"
    if "rand-mixed" in fname:
        return "rand-mixed"
    return None


def extract_timestamp(fname: str):
    parts = fname.split("-")
    if len(parts) >= 2:
        return f"{parts[0]}-{parts[1]}"
    return "unknown"


def extract_metrics(json_file: Path, arch: str, test: str):
    with open(json_file) as f:
        data = json.load(f)

    job = data["jobs"][0]
    family, variant = split_architecture(arch)
    timestamp = extract_timestamp(json_file.name)

    return {
        "arch": arch,
        "arch_family": family,
        "arch_variant": variant,
        "timestamp": timestamp,
        "test": test,
        "read_bw_MBps": job["read"]["bw"] / 1024,     # fio bw is KiB/s
        "write_bw_MBps": job["write"]["bw"] / 1024,
        "read_iops": job["read"]["iops"],
        "write_iops": job["write"]["iops"],
    }


# ------------------------------------------------------------
# Read all JSON runs
# ------------------------------------------------------------
for arch_dir in BASE_DIR.iterdir():
    if not arch_dir.is_dir():
        continue

    arch = arch_dir.name
    if arch == "test":
        continue

    for path in arch_dir.glob("*.json"):
        test = detect_test(path.name)
        if test is None:
            continue

        try:
            records.append(extract_metrics(path, arch, test))
        except Exception as e:
            print(f"Error reading {path}: {e}")

df = pd.DataFrame(records)

if df.empty:
    raise RuntimeError(f"No benchmark JSON files found under {BASE_DIR}")

# Save all raw extracted rows
df.to_csv("zfs_results_runs.csv", index=False)
print("Saved zfs_results_runs.csv")

# ------------------------------------------------------------
# Main architecture dataset:
# keep only the latest run for each exact arch + test pair
# ------------------------------------------------------------
core_df = df[df["arch"].isin(CORE_ARCH_ORDER)].copy()

core_df["timestamp_dt"] = pd.to_datetime(core_df["timestamp"], format="%Y%m%d-%H%M%S")
core_df = (
    core_df.sort_values("timestamp_dt")
           .groupby(["arch", "test"], as_index=False)
           .tail(1)
           .drop(columns=["timestamp_dt"])
)

core_df["arch"] = pd.Categorical(core_df["arch"], categories=CORE_ARCH_ORDER, ordered=True)
core_df = core_df.sort_values(["arch", "test"])

core_df.to_csv("zfs_results_core_latest.csv", index=False)
print("Saved zfs_results_core_latest.csv")

# ------------------------------------------------------------
# Robustness dataset:
# all mirror2 family runs, including baseline and variants
# ------------------------------------------------------------
mirror2_df = df[df["arch_family"] == "mirror2"].copy()
mirror2_df.to_csv("zfs_results_mirror2_robustness.csv", index=False)
print("Saved zfs_results_mirror2_robustness.csv")

mirror2_summary = (
    mirror2_df.groupby(["arch_variant", "test"], as_index=False)
              .agg(
                  read_bw_MBps_mean=("read_bw_MBps", "mean"),
                  read_bw_MBps_std=("read_bw_MBps", "std"),
                  write_bw_MBps_mean=("write_bw_MBps", "mean"),
                  write_bw_MBps_std=("write_bw_MBps", "std"),
                  read_iops_mean=("read_iops", "mean"),
                  read_iops_std=("read_iops", "std"),
                  write_iops_mean=("write_iops", "mean"),
                  write_iops_std=("write_iops", "std"),
                  n_runs=("arch", "count"),
              )
              .sort_values(["arch_variant", "test"])
)

mirror2_summary.to_csv("zfs_results_mirror2_summary.csv", index=False)
print("Saved zfs_results_mirror2_summary.csv")


# ------------------------------------------------------------
# Plot helpers
# ------------------------------------------------------------
def plot_core_metric(core_df, test, metric, title, ylabel, outfile):
    subset = core_df[core_df["test"] == test].copy()
    subset = subset.sort_values("arch")

    plt.figure(figsize=(8, 5))
    plt.bar(subset["arch"].astype(str), subset[metric])
    plt.xticks(rotation=45)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outfile, dpi=150)
    plt.close()
    print(f"Saved {outfile}")


def plot_mirror2_errorbars(summary_df, test, metric_mean, metric_std, title, ylabel, outfile):
    subset = summary_df[summary_df["test"] == test].copy()

    # nicer order for variants
    variant_order = ["baseline", "fast_fast", "fast_slow", "slow_slow", "laptop_fast"]
    subset["arch_variant"] = pd.Categorical(
        subset["arch_variant"],
        categories=variant_order,
        ordered=True
    )
    subset = subset.sort_values("arch_variant")

    plt.figure(figsize=(8, 5))
    plt.bar(
        subset["arch_variant"].astype(str),
        subset[metric_mean],
        yerr=subset[metric_std].fillna(0),
        capsize=5
    )
    plt.xticks(rotation=45)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outfile, dpi=150)
    plt.close()
    print(f"Saved {outfile}")


# ------------------------------------------------------------
# Main architecture plots
# ------------------------------------------------------------
plot_core_metric(
    core_df, "rand-read", "read_iops",
    "Random Read IOPS by Architecture",
    "Read IOPS", "rand_read_iops_main.png"
)

plot_core_metric(
    core_df, "rand-write", "write_iops",
    "Random Write IOPS by Architecture",
    "Write IOPS", "rand_write_iops_main.png"
)

plot_core_metric(
    core_df, "seq-read", "read_bw_MBps",
    "Sequential Read Throughput by Architecture",
    "MB/s", "seq_read_bw_main.png"
)

plot_core_metric(
    core_df, "seq-write", "write_bw_MBps",
    "Sequential Write Throughput by Architecture",
    "MB/s", "seq_write_bw_main.png"
)

# ------------------------------------------------------------
# mirror2 robustness plots
# ------------------------------------------------------------
plot_mirror2_errorbars(
    mirror2_summary, "rand-read",
    "read_iops_mean", "read_iops_std",
    "mirror2 Robustness Check: Random Read IOPS",
    "Read IOPS", "mirror2_rand_read_errorbars.png"
)

plot_mirror2_errorbars(
    mirror2_summary, "seq-read",
    "read_bw_MBps_mean", "read_bw_MBps_std",
    "mirror2 Robustness Check: Sequential Read Throughput",
    "MB/s", "mirror2_seq_read_errorbars.png"
)

print("All plots generated.")