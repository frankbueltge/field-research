#!/bin/sh
# The post-run pipeline for DAY 12, written BEFORE the run closes so no step is improvised at the
# edge of a session. Session 133, 2026-08-23.
#
# The comparison day is 2026-08-22 — the last completed measurement day. That date has TWO run files
# (`DOUBLE-PROBE-131-132.md`, downstream condition 32): the day is `run-2026-08-22T0341Z.json`, the
# session-132 run that landed on main, and `-second-probe.json` is session 131's, kept beside it and
# never counted as a day. This pipeline names the day file explicitly for that reason.
# The interval is 1.0000 days from its start second — the fifth one-day interval in a row.
#
# Day 12 is OUTSIDE the pre-registered window and no pre-registered test is scored on it.
#
# WHAT IS DELIBERATELY ABSENT, AND IT IS STILL THE POINT: there is no `build_letter.py` step here and
# there must not be. `CONDITIONS-128.md`'s stop — left unchanged by `CONDITIONS-131.md` item 1 and
# `CONDITIONS-132.md` item 1 — forbids this arc any delivery object, repair pass, gauntlet or packet
# before 2026-09-05, and a build step quietly inherited from an earlier day's script is exactly how a
# stop stops being one. This file is day 11's pipeline with the dates moved and nothing else moved;
# that is the whole of the diff and it is stated so that nobody has to take it on trust.
#
# ONE THING THIS SESSION KNOWS THAT DAY 11'S PIPELINE DID NOT: an empty interval no longer crashes
# the metrics step (`ERRATA-132.md` E37, one accessor). Day 11 was the first zero-transition interval
# in the series and it broke this pipeline. If day 12 is also empty, that is TWO intervals and still
# not a rate — `CONDITIONS-132.md` item 5 binds this session on exactly that and it is not softened
# here.
set -e
D11=ledger/run-2026-08-22T0341Z.json
D12=ledger/run-2026-08-23T0341Z.json

test -f "$D12" || { echo "day 12 has no completed run file - a .partial is never a run" >&2; exit 1; }

python3 ledger_diff.py "$D11" "$D12" ledger/diff-day11-day12.json
python3 ledger_diff.py "$D11" "$D12" ledger/diff-day11-day12-overlay.json --corrections
python3 confirm_transition.py ledger/diff-day11-day12.json ledger/transition-confirm-2026-08-23.json
python3 confirmation_record_121.py
python3 window_status.py window-status-133.json
python3 interval_metrics.py "$D11" "$D12" ledger/diff-day11-day12.json \
    ledger/transition-confirm-2026-08-23.json -o interval-metrics-133.json \
    --note "day 12: the fifth run outside the pre-registered window, 1.0000 days after the last completed run (2026-08-22, the session-132 file that landed on main; the second probe of that date is not a day). No pre-registered test is scored on it. Run under the stop of CONDITIONS-128.md, unchanged by CONDITIONS-131.md and CONDITIONS-132.md: the instrument keeps measuring, and nothing is built to send. It is the second consecutive day delivered by a session that opened inside the licensed hour, and that is luck about when sessions open, not a cadence this practice controls."
