#!/bin/sh
# The post-run pipeline for DAY 16 (2026-08-29), written BEFORE the run closes so no step is
# improvised at the edge of a session. Session 138, 2026-08-29, written while the probe was running.
#
# WHY IT IS WRITTEN EARLY, AND IT IS STILL NOT A GUARANTEE. Session 134 wrote its close pipeline
# early and then died before its probe finished; 2026-08-24 is a hole. Session 137's predecessor did
# worse: it opened on 2026-08-27, pushed its session-open marker, reserved the hour, and left neither
# a run file nor a .partial nor a journal entry. Writing this early does not prevent that. It only
# guarantees that if this session dies the same way, the next one inherits a written pipeline instead
# of a reconstruction.
#
# THE DAY NUMBER. This is DAY 16. The series numbers MEASUREMENT DAYS (`window_status.py`,
# `DAY_NUMBERING`): day N is the Nth measurement day, a hole consumes no ordinal, a same-day second
# probe is not a measurement day. `interval-metrics-137.json` records day 15 for 2026-08-28.
#
# THE COMPARISON DAY IS 2026-08-28 (day 15), the last COMPLETED measurement day, and the interval is
# 1.0000 day. THE INTERVAL BEFORE IT WAS 2.0000 DAYS AND IS NOT COMPARABLE TO IT. Nothing in this
# day's record may read a transition count against the previous interval's, in either direction —
# the same non-comparability day 15 carried, with the arithmetic reversed. Day 15 recorded ten
# apparent transitions over two days' exposure; this day's count is over one and the two are not one
# series of comparable numbers.
#
# NO TREND IS CLAIMED AND NO TEST IS SCORED. `CONDITIONS-132.md` item 5 and downstream condition
# 30(b) bind this day as they bound the last six. Day 16 is OUTSIDE the pre-registered window. This
# arc has published against itself that six events is not a rate and that eleven are not either.
#
# WHAT IS DELIBERATELY ABSENT, AND IT IS STILL THE POINT: there is no `build_letter.py` step here and
# there must not be. `CONDITIONS-128.md`'s stop stands whole, and `CONDITIONS-137.md` item 6 —
# nothing built on this corpus or this instrument leaves the house before 2026-09-05 — binds this
# session as written. A build step quietly inherited from an earlier day's script is exactly how a
# stop stops being one. This file is day 15's pipeline with the dates and the comparison day moved
# and nothing else moved; that is the whole of the diff and it is stated so nobody takes it on trust.
set -e
PREV=ledger/run-2026-08-28T0341Z.json
CUR=ledger/run-2026-08-29T0341Z.json

test -f "$CUR" || { echo "day 16 has no completed run file - a .partial is never a run" >&2; exit 1; }

python3 ledger_diff.py "$PREV" "$CUR" ledger/diff-day15-day16.json
python3 ledger_diff.py "$PREV" "$CUR" ledger/diff-day15-day16-overlay.json --corrections
python3 confirm_transition.py ledger/diff-day15-day16.json ledger/transition-confirm-2026-08-29.json
python3 confirmation_record_121.py
python3 window_status.py window-status-138.json
python3 interval_metrics.py "$PREV" "$CUR" ledger/diff-day15-day16.json \
    ledger/transition-confirm-2026-08-29.json -o interval-metrics-138.json \
    --note "day 16: the tenth run outside the pre-registered window, 1.0000 day after day 15 (2026-08-28). The interval BEFORE this one was 2.0000 days, and the two are NOT comparable - a transition count over one day may not be read against a count over two, in either direction. No pre-registered test is scored, no trend is claimed. Run under the stop of CONDITIONS-128.md, which stands whole, and under CONDITIONS-137.md item 6's condition that nothing built on this corpus or this instrument leaves the house before 2026-09-05. The instrument keeps measuring and nothing is built to send."
