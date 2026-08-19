#!/bin/sh
# The post-run pipeline for DAY 8, written BEFORE the run closes so no step is improvised.
# Session 127, 2026-08-19.
#
# The comparison day is 2026-08-18 - the last COMPLETED measurement day, and the only run file of
# that date. The interval is 1.0000 days from its start second, which is the first one-day
# interval since the aborted day 7 forced a two-day one.
#
# Day 8 is OUTSIDE the pre-registered window (see run_day8.sh). No pre-registered test is scored
# on it. What it can move is the confirmation record, which is why this pipeline recomputes that
# record from the sidecars rather than letting any document carry a figure across.
set -e
D7=ledger/run-2026-08-18T0341Z.json
D8=ledger/run-2026-08-19T0341Z.json

test -f "$D8" || { echo "day 8 has no completed run file - a .partial is never a run" >&2; exit 1; }

python3 ledger_diff.py "$D7" "$D8" ledger/diff-day7-day8.json
python3 ledger_diff.py "$D7" "$D8" ledger/diff-day7-day8-overlay.json --corrections
python3 confirm_transition.py ledger/diff-day7-day8.json ledger/transition-confirm-2026-08-19.json
python3 confirmation_record_121.py
python3 window_status.py window-status-127.json
python3 interval_metrics.py "$D7" "$D8" ledger/diff-day7-day8.json \
    ledger/transition-confirm-2026-08-19.json -o interval-metrics-127.json --note "day 8: the first run OUTSIDE the pre-registered window, 1.0000 days after the last completed run (2026-08-18). No pre-registered test is scored on it."
