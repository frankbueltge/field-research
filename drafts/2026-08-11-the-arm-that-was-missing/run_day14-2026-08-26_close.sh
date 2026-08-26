#!/bin/sh
# The post-run pipeline for DAY 14 (2026-08-26), written BEFORE the run closes so no step is
# improvised at the edge of a session. Session 136, 2026-08-26, written at 03:50Z with the probe
# nine minutes in.
#
# WHY IT IS WRITTEN EARLY, AND IT IS STILL NOT A GUARANTEE. Session 134 wrote its close pipeline
# early and then died before its probe finished; its run left a .partial and no run file, and
# 2026-08-24 is a hole. Writing this early does not prevent that. It only guarantees that if this
# session dies the same way, the next one inherits a written pipeline instead of a reconstruction.
#
# THE DAY NUMBER. This is DAY 14. The series numbers MEASUREMENT DAYS: `series-stability-136.json`
# enumerates the thirteen completed run files by pattern and prints their hours, and 2026-08-17 and
# 2026-08-24 are holes with a .partial and no run file. A partial is never a run.
#
# THE COMPARISON DAY IS 2026-08-25 (day 13), the last COMPLETED measurement day, and the interval is
# 1.0000 day. THE INTERVAL BEFORE IT WAS 2.0000 DAYS AND IS NOT COMPARABLE TO IT. Nothing in this
# day's record may read a transition count against the previous interval's, in either direction.
#
# NO TREND IS CLAIMED AND NO TEST IS SCORED. `CONDITIONS-132.md` item 5 and downstream condition
# 30(b) bind this day as they bound the last four. Day 14 is OUTSIDE the pre-registered window.
# The twelve raw day-to-day change counts before today run 1, 1, 4, 2, 0, 4, 1, 4, 2, 0, 3, 2
# (`series-stability-136.json`, encyclopedia arms only, raw and unconfirmed). This arc has published
# against itself that six events is not a rate and that eleven are not either.
#
# WHAT IS DELIBERATELY ABSENT, AND IT IS STILL THE POINT: there is no `build_letter.py` step here
# and there must not be. `CONDITIONS-128.md`'s stop stands whole. Session 135 measured it against
# the constitution's clock and held it; THIS session was asked to license one narrow attempt, and
# under the architect's standing rule of 2026-07-17 decided the question itself and REFUSED
# (`INCREMENT-24.md`). A build step quietly inherited from an earlier day's script is exactly how a
# stop stops being one. This file is day 13's pipeline with the dates and the comparison day moved
# and nothing else moved; that is the whole of the diff and it is stated so nobody takes it on trust.
set -e
PREV=ledger/run-2026-08-25T0341Z.json
CUR=ledger/run-2026-08-26T0341Z.json

test -f "$CUR" || { echo "day 14 has no completed run file - a .partial is never a run" >&2; exit 1; }

python3 ledger_diff.py "$PREV" "$CUR" ledger/diff-day13-day14.json
python3 ledger_diff.py "$PREV" "$CUR" ledger/diff-day13-day14-overlay.json --corrections
python3 confirm_transition.py ledger/diff-day13-day14.json ledger/transition-confirm-2026-08-26.json
python3 confirmation_record_121.py
python3 window_status.py window-status-136.json
python3 interval_metrics.py "$PREV" "$CUR" ledger/diff-day13-day14.json \
    ledger/transition-confirm-2026-08-26.json -o interval-metrics-136.json \
    --note "day 14: the eighth run outside the pre-registered window, 1.0000 day after day 13 (2026-08-25). The interval BEFORE this one was 2.0000 days because 2026-08-24 is a hole, and the two are NOT comparable - a transition count over one day may not be read against a count over two, in either direction. No pre-registered test is scored, no trend is claimed. Run under the stop of CONDITIONS-128.md, which stands whole: session 135 measured it and held it, and session 136 answered the licence question it had put to the architect - under his standing rule of 2026-07-17 - by REFUSING the narrow attempt against its own disclosed interest (INCREMENT-24.md). The instrument keeps measuring and nothing is built to send."
