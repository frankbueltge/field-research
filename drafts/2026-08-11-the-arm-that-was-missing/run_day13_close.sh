#!/bin/sh
# The post-run pipeline for DAY 13, written BEFORE the run closes so no step is improvised at the
# edge of a session. Session 134, 2026-08-24, written at 03:44Z with the probe 3 minutes in.
#
# The comparison day is 2026-08-23 — the last completed measurement day, one run file, no double
# probe. The interval is 1.0000 days from its start second: the sixth one-day interval in a row.
#
# Day 13 is OUTSIDE the pre-registered window and no pre-registered test is scored on it.
#
# WHAT IS DELIBERATELY ABSENT, AND IT IS STILL THE POINT: there is no `build_letter.py` step here
# and there must not be. `CONDITIONS-128.md`'s stop — left unchanged by item 1 of
# `CONDITIONS-131.md`, `-132.md` and `-133.md` — forbids this arc any delivery object, repair pass,
# gauntlet or packet before 2026-09-05, and a build step quietly inherited from an earlier day's
# script is exactly how a stop stops being one. This file is day 12's pipeline with the dates moved
# and nothing else moved; that is the whole of the diff and it is stated so that nobody has to take
# it on trust.
#
# ON THE INTERVAL SERIES: the ten day-to-day intervals before today ran 1, 4, 2, 1, 4, 1, 5, 2, 0, 4.
# Whatever day 13 returns — a zero, a four, or anything else — `CONDITIONS-132.md` item 5 and
# downstream condition 30(b) bind this session as they bound the last two: NO TREND IS CLAIMED AND NO
# TEST IS SCORED. This arc has published against itself that six events is not a rate.
set -e
D12=ledger/run-2026-08-23T0341Z.json
D13=ledger/run-2026-08-24T0341Z.json

test -f "$D13" || { echo "day 13 has no completed run file - a .partial is never a run" >&2; exit 1; }

python3 ledger_diff.py "$D12" "$D13" ledger/diff-day12-day13.json
python3 ledger_diff.py "$D12" "$D13" ledger/diff-day12-day13-overlay.json --corrections
python3 confirm_transition.py ledger/diff-day12-day13.json ledger/transition-confirm-2026-08-24.json
python3 confirmation_record_121.py
python3 window_status.py window-status-134.json
python3 interval_metrics.py "$D12" "$D13" ledger/diff-day12-day13.json \
    ledger/transition-confirm-2026-08-24.json -o interval-metrics-134.json \
    --note "day 13: the sixth run outside the pre-registered window, 1.0000 days after the last completed run (2026-08-23). No pre-registered test is scored on it. Run under the stop of CONDITIONS-128.md, unchanged by CONDITIONS-131.md, -132.md and -133.md: the instrument keeps measuring, and nothing is built to send. It is the third consecutive day delivered by a session that happened to open inside the licensed five minutes, and that is luck about when sessions open, not a cadence this practice controls (downstream condition 29)."
