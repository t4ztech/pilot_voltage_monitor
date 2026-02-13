# Independent 230V Voltage Observability — Pilot

## Purpose
This pilot provides independent, read-only monitoring of a 230V power supply
to detect early signs of instability before failures occur.

The system does NOT control equipment, modify PLC logic, or interact with
safety functions. It exists solely to observe, analyze, and report.

---

## Problem Addressed
Intermittent voltage instability can cause:
- unexplained equipment resets
- sporadic electronic faults
- alarms that trigger only after downtime has occurred

Traditional systems often react too late and without historical context.

---

## What This Pilot Does
- Monitors RMS voltage behavior over time
- Detects drift, noise, spikes, and data dropouts
- Differentiates between normal, warning, and alarm states
- Generates alerts and summary reports

---

## What This Pilot Does NOT Do
- No real-time control
- No PLC program changes
- No interaction with safety systems
- No automatic corrective actions

Safety systems retain full authority.

---

## Deliverables
- alerts.log — timestamped event log
- summary.json — statistical summary and counts
- Interpretation and recommendations

---

## Design Principle
"I don’t build smarter control systems.
I build systems that understand themselves before they fail."

---

## Typical Pilot Duration
2–4 weeks, depending on data availability.

---

## Design Principle
"I don’t build smarter control systems.
I build systems that understand themselves before they fail."

---

## Typical Pilot Duration
2–4 weeks, depending on data availability and system behavior.

---

## Next Steps
If value is demonstrated, the system can:
- remain active as a monitoring service
- be extended with additional signals
- be integrated into regular operational reporting

---


## Quick Start
Simulated run:
`python3 monitor.py --simulate --minutes 2 --out output_example`

CSV run:
`python3 monitor.py --csv sample_data/voltage_sample.csv --out output_example`
