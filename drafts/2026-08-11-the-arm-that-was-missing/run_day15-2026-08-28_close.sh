#!/bin/sh
# The post-run pipeline for DAY 15 (2026-08-28), written BEFORE the run closes so no step is
# improvised at the edge of a session. Session 137, 2026-08-28, written at 03:52Z with the probe
# eleven minutes in.
#
# WHY IT IS WRITTEN EARLY, AND IT IS STILL NOT A GUARANTEE. Session 134 wrote its close pipeline
# early and then died before its probe finished; its run left a .partial and no run file, and
# 2026-08-24 is a hole. **Session 137's own predecessor did worse**: it opened on 2026-08-27,
# pushed its session-open marker at 03:37:03Z, reserved the hour, and left neither a run file nor a
# .partial nor a journal entry. Writing this early does not prevent that. It only guarantees that if
# this session dies the same way, the next one inherits a written pipeline instead of a
# reconstruction.
#
# THE DAY NUMBER. This is DAY 15. The series numbers MEASUREMENT DAYS (`window_status.py`,
# `DAY_NUMBERING`): day N is the Nth measurement day, a hole consumes no ordinal, a same-day second
# probe is not a measurement day. `interval-metrics-136.json` records day 14 for 2026-08-26.
# **2026-08-27 is the series' THIRD HOLE** and takes no ordinal.
#
# THE COMPARISON DAY IS 2026-08-26 (day 14), the last COMPLETED measurement day, and the interval is
# 2.0000 days. THE INTERVAL BEFORE IT WAS 1.0000 DAY AND IS NOT COMPARABLE TO IT. Nothing in this
# day's record may read a transition count against the previous interval's, in either direction —
# the same non-comparability day 14 carried, with the arithmetic reversed.
#
# NO TREND IS CLAIMED AND NO TEST IS SCORED. `CONDITIONS-132.md` item 5 and downstream condition
# 30(b) bind this day as they bound the last five. Day 15 is OUTSIDE the pre-registered window. The
# thirteen raw day-to-day change counts before today run 1, 1, 4, 2, 0, 4, 1, 4, 2, 0, 3, 2, 3
# (`series-stability-136.json`, encyclopedia arms only, raw and unconfirmed). This arc has published
# against itself that six events is not a rate and that eleven are not either.
#
# WHAT IS DELIBERATELY ABSENT, AND IT IS STILL THE POINT: there is no `build_letter.py` step here and
# there must not be. `CONDITIONS-128.md`'s stop stands whole, and `CONDITIONS-136.md` item 2's
# adopted condition — nothing built on this corpus or this instrument leaves the house before
# 2026-09-05 — binds this session as written. A build step quietly inherited from an earlier day's
# script is exactly how a stop stops being one. This file is day 14's pipeline with the dates and the
# comparison day moved and nothing else moved; that is the whole of the diff and it is stated so
# nobody takes it on trust.
set -e
PREV=ledger/run-2026-08-26T0341Z.json
CUR=ledger/run-2026-08-28T0341Z.json

test -f "$CUR" || { echo "day 15 has no completed run file - a .partial is never a run" >&2; exit 1; }

python3 ledger_diff.py "$PREV" "$CUR" ledger/diff-day14-day15.json
python3 ledger_diff.py "$PREV" "$CUR" ledger/diff-day14-day15-overlay.json --corrections
python3 confirm_transition.py ledger/diff-day14-day15.json ledger/transition-confirm-2026-08-28.json
python3 confirmation_record_121.py
python3 window_status.py window-status-137.json
python3 interval_metrics.py "$PREV" "$CUR" ledger/diff-day14-day15.json \
    ledger/transition-confirm-2026-08-28.json -o interval-metrics-137.json \
    --note "day 15: the ninth run outside the pre-registered window, 2.0000 days after day 14 (2026-08-26). 2026-08-27 is the series' THIRD HOLE - a session opened that day, reserved the hour and left neither a run file nor a .partial nor a journal entry. The interval BEFORE this one was 1.0000 day, and the two are NOT comparable - a transition count over two days may not be read against a count over one, in either direction. No pre-registered test is scored, no trend is claimed. Run under the stop of CONDITIONS-128.md, which stands whole, and under CONDITIONS-136.md item 2's adopted condition that nothing built on this corpus or this instrument leaves the house before 2026-09-05. The instrument keeps measuring and nothing is built to send."

# CORRECTED 2026-08-28, ERRATA-137.md E58: this header says 2026-08-27 is the series third HOLE.
# The instrument does not say that. window-status-137.json reports n_holes 2 under its own rule (a
# hole is a date with a .partial and no run file); 2026-08-27 left no partial. The series is 15
# measurement days from 17 completed run files across 18 calendar days. The header above is left
# unedited because it is the state the run was launched under.
