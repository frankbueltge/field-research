#!/bin/sh
# The post-run pipeline for day 7, written BEFORE the run closed so no step is improvised at
# 05:30Z. Session 125. Each step writes a file; every figure the day-7 record quotes is read
# from one of them by day7_metrics.py, never typed.
#
# The day-6 side is the CANONICAL run file, not the second probe of that date
# (DOUBLE-PROBE-122.md): the diff must compare one measurement day to one measurement day.
set -e
D6=ledger/run-2026-08-16T0337Z.json
D7=ledger/run-2026-08-17T0337Z.json

test -f "$D7" || { echo "day 7 has no completed run file - a .partial is never a run" >&2; exit 1; }

python3 ledger_diff.py "$D6" "$D7" ledger/diff-day6-day7.json
python3 ledger_diff.py "$D6" "$D7" ledger/diff-day6-day7-overlay.json --corrections
python3 confirm_transition.py ledger/diff-day6-day7.json ledger/transition-confirm-2026-08-17.json
python3 confirmation_record_121.py
python3 day7_metrics.py
