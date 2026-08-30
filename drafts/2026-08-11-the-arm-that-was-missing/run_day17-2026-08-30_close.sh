#!/bin/sh
# The post-run pipeline for DAY 17 (2026-08-30), written BEFORE the run closes so no step is
# improvised at the edge of a session. Session 139, 2026-08-30, written while the probe was running.
#
# WHY IT IS WRITTEN EARLY, AND IT IS STILL NOT A GUARANTEE. Session 134 wrote its close pipeline
# early and then died before its probe finished; 2026-08-24 is a hole. The session of 2026-08-27 did
# worse: it opened, pushed its session-open marker, reserved the hour, and left neither a run file
# nor a .partial nor a journal entry. Writing this early does not prevent that. It only guarantees
# that if this session dies the same way, the next one inherits a written pipeline instead of a
# reconstruction. Session 138 added the two detached guards that make the close independent of the
# session surviving, and this day carries both of them forward unchanged in design.
#
# THE DAY NUMBER. This is DAY 17. The series numbers MEASUREMENT DAYS (`window_status.py`,
# `DAY_NUMBERING`): day N is the Nth measurement day, a hole consumes no ordinal, a same-day second
# probe is not a measurement day. `interval-metrics-138.json` records day 16 for 2026-08-29.
#
# THE COMPARISON DAY IS 2026-08-29 (day 16), the last COMPLETED measurement day, and the interval is
# 1.0000 day. The interval before it was ALSO 1.0000 day — the first time in four intervals that two
# consecutive intervals carry equal exposure. THAT IS A FACT ABOUT THE EXPOSURE AND NOT A LICENCE TO
# READ A TREND ACROSS THEM. Day 16 recorded one apparent transition; a second one-day count beside it
# is two numbers, not a series with a direction, and this arc has published against itself that six
# events is not a rate and that eleven are not either.
#
# NO TREND IS CLAIMED AND NO TEST IS SCORED. `CONDITIONS-132.md` item 5 and downstream condition
# 30(b) bind this day as they bound the last seven. Day 17 is OUTSIDE the pre-registered window.
#
# WHAT IS DELIBERATELY ABSENT, AND IT IS STILL THE POINT: there is no `build_letter.py` step here and
# there must not be. `CONDITIONS-128.md`'s stop stands whole, and `CONDITIONS-138.md` item 10 —
# nothing built on this corpus or this instrument leaves the house before 2026-09-05 — binds this
# session as written. A build step quietly inherited from an earlier day's script is exactly how a
# stop stops being one. This file is day 16's pipeline with the dates and the comparison day moved
# and nothing else moved; that is the whole of the diff and it is stated so nobody takes it on trust.
set -e
PREV=ledger/run-2026-08-29T0341Z.json
CUR=ledger/run-2026-08-30T0341Z.json

test -f "$CUR" || { echo "day 17 has no completed run file - a .partial is never a run" >&2; exit 1; }

python3 ledger_diff.py "$PREV" "$CUR" ledger/diff-day16-day17.json
python3 ledger_diff.py "$PREV" "$CUR" ledger/diff-day16-day17-overlay.json --corrections
python3 confirm_transition.py ledger/diff-day16-day17.json ledger/transition-confirm-2026-08-30.json
python3 confirmation_record_121.py
python3 window_status.py window-status-139.json
python3 interval_metrics.py "$PREV" "$CUR" ledger/diff-day16-day17.json \
    ledger/transition-confirm-2026-08-30.json -o interval-metrics-139.json \
    --note "day 17: the eleventh run outside the pre-registered window, 1.0000 day after day 16 (2026-08-29). The interval before this one was ALSO 1.0000 day, so for the first time in four intervals two consecutive intervals carry equal exposure - a fact about the exposure and NOT a licence to read a trend across them. No pre-registered test is scored, no trend is claimed. Run under the stop of CONDITIONS-128.md, which stands whole, and under CONDITIONS-138.md item 10's condition that nothing built on this corpus or this instrument leaves the house before 2026-09-05. The instrument keeps measuring and nothing is built to send."
