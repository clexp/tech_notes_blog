import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
SINGLE_DIR = BASE_DIR / "stage3-logs"
COMBINED_DIR = BASE_DIR / "stage3-logs-combined"

# Workloads we care about for final comparison.
SINGLE_TESTS = {
    "seq-read",
    "seq-write",
    "rand-read-q1",
    "rand-read-q16",
    "rand-read-q32",
    "rand-write-q16",
    "rand-mixed-70r30w-q16",
}
COMBINED_TESTS = {
    "seq-read",
    "seq-write",
    "rand-read-q16",
    "rand-write-q16",
}


def parse_fio_json(json_file: Path) -> dict:
    data = json.loads(json_file.read_text())
    job = data["jobs"][0]

    read_ns = job.get("read", {}).get("clat_ns", {})
    write_ns = job.get("write", {}).get("clat_ns", {})

    def pick_pct(src: dict, key: str):
        pct = src.get("percentile", {})
        if not pct:
            return float("nan")
        return pct.get(key, float("nan"))

    return {
        "read_bw_MBps": job["read"]["bw"] / 1024.0,  # fio bw is KiB/s
        "write_bw_MBps": job["write"]["bw"] / 1024.0,
        "read_iops": float(job["read"]["iops"]),
        "write_iops": float(job["write"]["iops"]),
        "read_clat_p50_ns": pick_pct(read_ns, "50.000000"),
        "read_clat_p95_ns": pick_pct(read_ns, "95.000000"),
        "read_clat_p99_ns": pick_pct(read_ns, "99.000000"),
        "write_clat_p50_ns": pick_pct(write_ns, "50.000000"),
        "write_clat_p95_ns": pick_pct(write_ns, "95.000000"),
        "write_clat_p99_ns": pick_pct(write_ns, "99.000000"),
    }


def collect_single(records: list[dict]) -> None:
    # structure: stage3-logs/<card>/<scenario>/<timestamp>/*.json
    if not SINGLE_DIR.exists():
        return
    for card_dir in SINGLE_DIR.iterdir():
        if not card_dir.is_dir():
            continue
        card = card_dir.name
        for scenario_dir in card_dir.iterdir():
            if not scenario_dir.is_dir():
                continue
            scenario = scenario_dir.name
            for run_dir in scenario_dir.iterdir():
                if not run_dir.is_dir():
                    continue
                timestamp = run_dir.name
                for jf in run_dir.glob("*.json"):
                    test = jf.stem
                    if test not in SINGLE_TESTS:
                        continue
                    try:
                        rec = parse_fio_json(jf)
                    except Exception as exc:
                        print(f"[warn] failed parsing {jf}: {exc}")
                        continue
                    rec.update(
                        {
                            "source": "single",
                            "card": card,
                            "scenario": scenario,
                            "timestamp": timestamp,
                            "test": test,
                            "run_path": str(run_dir.relative_to(BASE_DIR)),
                        }
                    )
                    records.append(rec)


def collect_combined(records: list[dict]) -> None:
    # structure: stage3-logs-combined/<card>/<timestamp>/{hdd,ssd}/*.json
    if not COMBINED_DIR.exists():
        return
    for card_dir in COMBINED_DIR.iterdir():
        if not card_dir.is_dir():
            continue
        card = card_dir.name
        for run_dir in card_dir.iterdir():
            if not run_dir.is_dir():
                continue
            timestamp = run_dir.name
            for medium, scenario in (("hdd", "combined_hdd_mirror2x2"), ("ssd", "combined_ssd_mirror3")):
                medium_dir = run_dir / medium
                if not medium_dir.exists():
                    continue
                for jf in medium_dir.glob("*.json"):
                    test = jf.stem
                    if test not in COMBINED_TESTS:
                        continue
                    try:
                        rec = parse_fio_json(jf)
                    except Exception as exc:
                        print(f"[warn] failed parsing {jf}: {exc}")
                        continue
                    rec.update(
                        {
                            "source": "combined",
                            "card": card,
                            "scenario": scenario,
                            "timestamp": timestamp,
                            "test": test,
                            "run_path": str(run_dir.relative_to(BASE_DIR)),
                        }
                    )
                    records.append(rec)


def main() -> None:
    records: list[dict] = []
    collect_single(records)
    collect_combined(records)

    if not records:
        raise RuntimeError("No Stage 3 JSON data found under stage3-logs / stage3-logs-combined")

    df = pd.DataFrame(records)
    df["timestamp_dt"] = pd.to_datetime(df["timestamp"], format="%Y%m%d-%H%M%S", errors="coerce")
    df = df.sort_values(["source", "card", "scenario", "test", "timestamp_dt"])

    runs_csv = BASE_DIR / "stage3_results_runs.csv"
    df.to_csv(runs_csv, index=False)
    print(f"Saved {runs_csv}")

    metric_cols = [
        "read_bw_MBps",
        "write_bw_MBps",
        "read_iops",
        "write_iops",
        "read_clat_p50_ns",
        "read_clat_p95_ns",
        "read_clat_p99_ns",
        "write_clat_p50_ns",
        "write_clat_p95_ns",
        "write_clat_p99_ns",
    ]

    grp_keys = ["source", "card", "scenario", "test"]
    avg_df = (
        df.groupby(grp_keys, as_index=False)[metric_cols]
        .mean(numeric_only=True)
        .rename(columns={c: f"{c}_mean" for c in metric_cols})
    )
    cnt_df = (
        df.groupby(grp_keys, as_index=False)
        .size()
        .rename(columns={"size": "n_runs"})
    )
    std_df = (
        df.groupby(grp_keys, as_index=False)[metric_cols]
        .std(numeric_only=True)
        .rename(columns={c: f"{c}_std" for c in metric_cols})
    )

    out_df = avg_df.merge(std_df, on=grp_keys, how="left").merge(cnt_df, on=grp_keys, how="left")
    out_df = out_df.sort_values(["source", "scenario", "test", "card"])

    avg_csv = BASE_DIR / "stage3_results_avg.csv"
    out_df.to_csv(avg_csv, index=False)
    print(f"Saved {avg_csv}")


if __name__ == "__main__":
    main()
