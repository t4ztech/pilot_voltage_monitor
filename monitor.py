#!/usr/bin/env python3

from dataclasses import dataclass

from pathlib import Path
from datetime import datetime, timedelta, timezone
import argparse
import csv
import json
import random
import statistics
import sys
import hashlib
VERSION = "1.0.0"


@dataclass
class Thresholds:
    ok_min: float = 220.0
    ok_max: float = 240.0
    alarm_min: float = 210.0
    alarm_max: float = 250.0


@dataclass
class Sample:
    timestamp: str
    voltage: float


@dataclass
class Alert:
    timestamp: str
    voltage: float
    level: str
    reason: str


def classify_voltage(v: float, t: Thresholds):
    if v < t.alarm_min or v > t.alarm_max:
        return "ALARM", "outside alarm limits"
    if v < t.ok_min or v > t.ok_max:
        return "WARN", "outside normal range"
    return "OK", "within normal range"


def simulate_data(minutes: int):
    random.seed(1)
    samples = []
    now = datetime.now(timezone.utc)
    for i in range(minutes * 60):
        ts = now + timedelta(seconds=i)
        base = 230.0
        noise = random.uniform(-2.0, 2.0)

        if random.random() < 0.02:
            noise += random.choice([-25, 25])

        samples.append(Sample(ts.isoformat() + "Z", base + noise))
    return samples


def load_csv(path: Path):
    samples = []
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            samples.append(Sample(row["timestamp"], float(row["voltage"])))
    return samples


def analyze(samples, thresholds: Thresholds):
    alerts = []
    voltages = []

    for s in samples:
        voltages.append(s.voltage)
        level, reason = classify_voltage(s.voltage, thresholds)
        if level != "OK":
            alerts.append(Alert(s.timestamp, s.voltage, level, reason))

    summary = {
        "count": len(samples),
        "min": min(voltages) if voltages else None,
        "max": max(voltages) if voltages else None,
        "avg": statistics.mean(voltages) if voltages else None,
        "alerts": {
            "WARN": sum(1 for a in alerts if a.level == "WARN"),
            "ALARM": sum(1 for a in alerts if a.level == "ALARM"),
        },
    }

    return alerts, summary


def write_outputs(alerts, summary, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    alerts_path = out_dir / "alerts.log"
    summary_path = out_dir / "summary.json"

    with alerts_path.open("w") as f:
        for a in alerts:
            f.write(f"{a.timestamp} | {a.level} | {a.voltage:.2f}V | {a.reason}\n")

    with summary_path.open("w") as f:
        json.dump(summary, f, indent=2)

    print(f"✅ Wrote: {alerts_path}")
    print(f"✅ Wrote: {summary_path}")

    def sha256_file(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
             for chunk in iter(lambda: f.read(8192), b""):
                 h.update(chunk)
        return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_run_metadata(out_dir: Path, mode: str, input_hash: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "input_hash": input_hash,
        "mode": mode,
    }

    meta_path = out_dir / "run_metadata.json"
    with meta_path.open("w") as f:
        json.dump(meta, f, indent=2)

    print(f"✅ Wrote: {meta_path}")



def main():
    parser = argparse.ArgumentParser(description="Independent Voltage Monitor")
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--minutes", type=int, default=2)
    parser.add_argument("--csv", type=Path)
    parser.add_argument("--out", type=Path, required=True)

    args = parser.parse_args()

    thresholds = Thresholds()

    if args.simulate:
        mode = "simulate"
        input_hash = sha256_text(f"simulate:{args.minutes}")
        samples = simulate_data(args.minutes)
    elif args.csv:
        mode = "csv"
        input_hash = sha256_file(args.csv)
        samples = load_csv(args.csv)
    else:
        print("❌ Either --simulate or --csv is required")
        sys.exit(1)


    alerts, summary = analyze(samples, thresholds)
    write_outputs(alerts, summary, args.out)
    write_run_metadata(args.out, mode, input_hash)



if __name__ == "__main__":
    main()
