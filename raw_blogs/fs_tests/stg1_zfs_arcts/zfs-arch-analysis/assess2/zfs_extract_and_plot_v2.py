import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path("../../logs")

ARCH_ORDER = [
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
    # expected style: 20260327-205526-rand-read.json
    parts = fname.split("-")
    if len(parts) >= 2:
        return f"{parts[0]}-{parts[1]}"
    return "unknown"


def extract_metrics(json_file: Path, arch: str, test: str):
    with open(json_file) as f:
        data = json.load(f)

    job = data["jobs"][0]

    read_bw = job["read"]["bw"]      # KiB/s
    write_bw = job["write"]["bw"]    # KiB/s
    read_iops = job["read"]["iops"]
    write_iops = job["write"]["iops"]

    family, variant = split_architecture(arch)
    timestamp = extract_timestamp(json_file.name)

    return {
        "arch": arch,
        "arch_family": family,
        "arch_variant": variant,
        "timestamp": timestamp,
        "test": test,
        "read_bw_MBps": read_bw / 1024,
        "write_bw_MBps": write_bw / 1024,
        "read_iops": read_iops,
        "write_iops": write_iops,
    }


# ------------------------------------------------------------
# Walk logs
# ------------------------------------------------------------
for arch_dir in BASE_DIR.iterdir():
    if not arch_dir.is_dir():
        continue

    arch = arch_dir.name

    # ignore obvious junk/test folders if present
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

# Stable ordering
df["arch_family"] = pd.Categorical(df["arch_family"], categories=ARCH_ORDER, ordered=True)

# Save run-level table
df.to_csv("zfs_results_runs.csv", index=False)
print("Saved zfs_results_runs.csv")

# ------------------------------------------------------------
# Summary tables
# ------------------------------------------------------------
summary = (
    df.groupby(["arch_family", "test"], as_index=False)
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
      .sort_values(["arch_family", "test"])
)

summary.to_csv("zfs_results_summary.csv", index=False)
print("Saved zfs_results_summary.csv")


# ------------------------------------------------------------
# Plot helpers
# ------------------------------------------------------------
def plot_main_metric(summary_df, test, metric_mean, title, ylabel, outfile):
    subset = summary_df[summary_df["test"] == test].copy()
    subset = subset.sort_values("arch_family")

    plt.figure(figsize=(8, 5))
    plt.bar(subset["arch_family"].astype(str), subset[metric_mean])
    plt.xticks(rotation=45)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outfile, dpi=150)
    plt.close()
    print(f"Saved {outfile}")


def plot_errorbar_metric(df_runs, family, test, metric, title, ylabel, outfile):
    subset = df_runs[
        (df_runs["arch_family"] == family) &
        (df_runs["test"] == test)
    ].copy()

    # one point per variant
    grouped = (
        subset.groupby("arch_variant", as_index=False)
              .agg(
                  mean_value=(metric, "mean"),
                  std_value=(metric, "std"),
                  n=("arch", "count")
              )
              .sort_values("arch_variant")
    )

    plt.figure(figsize=(8, 5))
    plt.bar(
        grouped["arch_variant"],
        grouped["mean_value"],
        yerr=grouped["std_value"].fillna(0),
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
plot_main_metric(
    summary, "rand-read", "read_iops_mean",
    "Random Read IOPS by Architecture Family",
    "Read IOPS", "rand_read_iops_main.png"
)

plot_main_metric(
    summary, "rand-write", "write_iops_mean",
    "Random Write IOPS by Architecture Family",
    "Write IOPS", "rand_write_iops_main.png"
)

plot_main_metric(
    summary, "seq-read", "read_bw_MBps_mean",
    "Sequential Read Throughput by Architecture Family",
    "MB/s", "seq_read_bw_main.png"
)

plot_main_metric(
    summary, "seq-write", "write_bw_MBps_mean",
    "Sequential Write Throughput by Architecture Family",
    "MB/s", "seq_write_bw_main.png"
)

# ------------------------------------------------------------
# Robustness plots for mirror2 family
# ------------------------------------------------------------
plot_errorbar_metric(
    df, "mirror2", "rand-read", "read_iops",
    "mirror2 Robustness Check: Random Read IOPS",
    "Read IOPS", "mirror2_rand_read_errorbars.png"
)

plot_errorbar_metric(
    df, "mirror2", "seq-read", "read_bw_MBps",
    "mirror2 Robustness Check: Sequential Read Throughput",
    "MB/s", "mirror2_seq_read_errorbars.png"
)

print("All plots generated.")
