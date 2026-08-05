import json
import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = "../../logs"

records = []

def extract_metrics(json_file, arch, test):
    with open(json_file) as f:
        data = json.load(f)

    job = data["jobs"][0]

    read_bw = job["read"]["bw"]      # KB/s
    write_bw = job["write"]["bw"]    # KB/s
    read_iops = job["read"]["iops"]
    write_iops = job["write"]["iops"]

    return {
        "arch": arch,
        "test": test,
        "read_bw_MBps": read_bw / 1024,
        "write_bw_MBps": write_bw / 1024,
        "read_iops": read_iops,
        "write_iops": write_iops
    }

# ------------------------------------------------------------
# Walk logs
# ------------------------------------------------------------
for arch in os.listdir(BASE_DIR):
    arch_dir = os.path.join(BASE_DIR, arch)
    if not os.path.isdir(arch_dir):
        continue

    for fname in os.listdir(arch_dir):
        if not fname.endswith(".json"):
            continue

        path = os.path.join(arch_dir, fname)

        if "seq-read" in fname:
            test = "seq-read"
        elif "seq-write" in fname:
            test = "seq-write"
        elif "rand-read" in fname and "mixed" not in fname:
            test = "rand-read"
        elif "rand-write" in fname:
            test = "rand-write"
        elif "rand-mixed" in fname:
            test = "rand-mixed"
        else:
            continue

        try:
            rec = extract_metrics(path, arch, test)
            records.append(rec)
        except Exception as e:
            print(f"Error reading {path}: {e}")

df = pd.DataFrame(records)

# Save CSV
df.to_csv("zfs_results.csv", index=False)

print("Saved zfs_results.csv")

# ------------------------------------------------------------
# Plot helpers
# ------------------------------------------------------------
def plot_metric(df, test, metric, title, outfile):
    subset = (
        df[df["test"] == test]
        .groupby("arch", as_index=False)
        .mean(numeric_only=True)
    )
    plt.figure()
    plt.bar(subset["arch"], subset[metric])
    plt.xticks(rotation=45)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outfile)
    plt.close()

# ------------------------------------------------------------
# Generate plots
# ------------------------------------------------------------

plot_metric(df, "rand-read", "read_iops",
            "Random Read IOPS by Architecture",
            "rand_read_iops.png")

plot_metric(df, "rand-write", "write_iops",
            "Random Write IOPS by Architecture",
            "rand_write_iops.png")

plot_metric(df, "seq-read", "read_bw_MBps",
            "Sequential Read MB/s by Architecture",
            "seq_read_bw.png")

plot_metric(df, "seq-write", "write_bw_MBps",
            "Sequential Write MB/s by Architecture",
            "seq_write_bw.png")

print("Plots generated.")
