#!/bin/sh
# The post-run pipeline for DAY 10, written BEFORE the run closes so no step is improvised.
# Session 129, 2026-08-21.
#
# The comparison day is 2026-08-20 - the last completed measurement day and the only run file of
# that date. The interval is 1.0000 days from its start second, the third one-day interval in a row.
#
# Day 10 is OUTSIDE the pre-registered window (see run_day10.sh) and no pre-registered test is
# scored on it. What it can move is the confirmation record, which is why this pipeline recomputes
# that record from the sidecars rather than letting any document carry a figure across.
#
# WHAT IS DELIBERATELY ABSENT, AND IT IS THE POINT: day 9's pipeline ended by gating `build_letter.py`.
# There is no such step here and there must not be. `CONDITIONS-128.md`'s stop forbids this arc any
# delivery object, repair pass, gauntlet or packet before 2026-09-05, and a build step quietly
# inherited from the previous day's script is exactly how a stop stops being one.
set -e
D9=ledger/run-2026-08-20T0341Z.json
D10=ledger/run-2026-08-21T0341Z.json

test -f "$D10" || { echo "day 10 has no completed run file - a .partial is never a run" >&2; exit 1; }

python3 ledger_diff.py "$D9" "$D10" ledger/diff-day9-day10.json
python3 ledger_diff.py "$D9" "$D10" ledger/diff-day9-day10-overlay.json --corrections
python3 confirm_transition.py ledger/diff-day9-day10.json ledger/transition-confirm-2026-08-21.json
python3 confirmation_record_121.py
python3 window_status.py window-status-129.json
python3 interval_metrics.py "$D9" "$D10" ledger/diff-day9-day10.json \
    ledger/transition-confirm-2026-08-21.json -o interval-metrics-129.json \
    --note "day 10: the third run outside the pre-registered window, 1.0000 days after the last completed run (2026-08-20). No pre-registered test is scored on it. Run under the stop of CONDITIONS-128.md: the instrument keeps measuring, and nothing is built to send."
