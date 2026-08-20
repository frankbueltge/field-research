#!/bin/sh
# The post-run pipeline for DAY 9, written BEFORE the run closes so no step is improvised.
# Session 128, 2026-08-20.
#
# The comparison day is 2026-08-19 - the last completed measurement day and the only run file of
# that date. The interval is 1.0000 days from its start second, the second one-day interval in a
# row after the abandoned day 7 forced a two-day one.
#
# Day 9 is OUTSIDE the pre-registered window (see run_day9.sh) and no pre-registered test is
# scored on it. What it can move is the confirmation record, which is why this pipeline recomputes
# that record from the sidecars rather than letting any document carry a figure across - and why
# `build_letter.py` refuses to run at all until this has happened, since it reads the record's
# coverage against the ledger.
set -e
D8=ledger/run-2026-08-19T0341Z.json
D9=ledger/run-2026-08-20T0341Z.json

test -f "$D9" || { echo "day 9 has no completed run file - a .partial is never a run" >&2; exit 1; }

python3 ledger_diff.py "$D8" "$D9" ledger/diff-day8-day9.json
python3 ledger_diff.py "$D8" "$D9" ledger/diff-day8-day9-overlay.json --corrections
python3 confirm_transition.py ledger/diff-day8-day9.json ledger/transition-confirm-2026-08-20.json
python3 confirmation_record_121.py
python3 window_status.py window-status-128.json
python3 interval_metrics.py "$D8" "$D9" ledger/diff-day8-day9.json \
    ledger/transition-confirm-2026-08-20.json -o interval-metrics-128.json \
    --note "day 9: the second run outside the pre-registered window, 1.0000 days after the last completed run (2026-08-19). No pre-registered test is scored on it."
