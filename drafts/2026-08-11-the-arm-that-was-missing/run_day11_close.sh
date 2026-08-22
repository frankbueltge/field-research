#!/bin/sh
# The post-run pipeline for DAY 11, written BEFORE the run closes so no step is improvised.
# Session 132, 2026-08-22.
#
# The comparison day is 2026-08-21 - the last completed measurement day and the only run file of
# that date. The interval is 1.0000 days from its start second, the fourth one-day interval in a row.
#
# Day 11 is OUTSIDE the pre-registered window (see run_day11.sh) and no pre-registered test is
# scored on it. What it can move is the confirmation record, which is why this pipeline recomputes
# that record from the sidecars rather than letting any document carry a figure across.
#
# WHAT IS DELIBERATELY ABSENT, AND IT IS STILL THE POINT: day 9's pipeline ended by gating
# `build_letter.py`. There is no such step here and there must not be. `CONDITIONS-128.md`'s stop -
# left unchanged and unsoftened by `CONDITIONS-131.md` item 1 - forbids this arc any delivery object,
# repair pass, gauntlet or packet before 2026-09-05, and a build step quietly inherited from an
# earlier day's script is exactly how a stop stops being one. This file is day 10's pipeline with the
# dates moved and nothing else moved; that is the whole of the diff and it is stated so that nobody
# has to take it on trust.
set -e
D10=ledger/run-2026-08-21T0341Z.json
D11=ledger/run-2026-08-22T0341Z.json

test -f "$D11" || { echo "day 11 has no completed run file - a .partial is never a run" >&2; exit 1; }

python3 ledger_diff.py "$D10" "$D11" ledger/diff-day10-day11.json
python3 ledger_diff.py "$D10" "$D11" ledger/diff-day10-day11-overlay.json --corrections
python3 confirm_transition.py ledger/diff-day10-day11.json ledger/transition-confirm-2026-08-22.json
python3 confirmation_record_121.py
python3 window_status.py window-status-132.json
python3 interval_metrics.py "$D10" "$D11" ledger/diff-day10-day11.json \
    ledger/transition-confirm-2026-08-22.json -o interval-metrics-132.json \
    --note "day 11: the fourth run outside the pre-registered window, 1.0000 days after the last completed run (2026-08-21). No pre-registered test is scored on it. Run under the stop of CONDITIONS-128.md, unchanged by CONDITIONS-131.md: the instrument keeps measuring, and nothing is built to send. It is the first day of the series delivered by a session that opened inside the licensed hour rather than one that had named the hour hours earlier."
