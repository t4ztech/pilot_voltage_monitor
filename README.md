# Voltage Observability Monitor (230V RMS) — CLI Analysis Utility

A small, read-only command-line tool for offline analysis of 230V RMS voltage data.  
It detects threshold violations (WARN/ALARM) and optional step-based drift, then produces structured logs and summaries for troubleshooting and validation.

## Why this exists

Voltage instability can cause:
- sporadic electronic faults and resets
- nuisance alarms during downtime/startup
- missing context when commissioning or diagnosing issues

This tool provides independent observability **without changing PLC logic**.

## Features

- CSV analysis (`--csv`) or synthetic simulation (`--simulate`)
- WARN / ALARM classification using thresholds
- Optional DRIFT detection (`--drift`, `--drift-threshold`)
- Outputs:
  - `alerts.log` (chronological events)
  - `summary.json` (stats + counts)
  - `run_metadata.json` (run context + SHA256 integrity hash)

## Usage

### Simulated run
```bash
python monitor.py --simulate --minutes 1 --out output_sim

python monitor.py --simulate --minutes 1 --drift --out output_sim

python monitor.py --simulate --minutes 1 --drift --drift-threshold 3.0 --out output_sim

python monitor.py --csv sample_data/voltage_sample.csv --out output_csv

Roadmap (Phase 4 ideas)

rolling window trends (moving average / min / max)

drift accumulation and “slow decay” detection

noise profiling / variance metrics

config profiles via JSON (threshold sets)

export format suitable for dashboards

Author

Electrical field technician transitioning into software/automation, focusing on practical observability tooling for real industrial environments.
---