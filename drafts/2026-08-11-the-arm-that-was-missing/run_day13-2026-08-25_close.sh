#!/bin/sh
# The post-run pipeline for DAY 13 (2026-08-25), written BEFORE the run closes so no step is
# improvised at the edge of a session. Session 135, 2026-08-25, written at 03:48Z with the probe
# seven minutes in.
#
# WHY THIS FILE IS WRITTEN EARLY, AND IT IS NOT A HABIT — IT IS THE LESSON OF YESTERDAY.
# Session 134 wrote its close pipeline early too, and then died before its probe finished. Its
# run left a .partial and no run file, and 2026-08-24 is a hole. Writing this file early does not
# prevent that; it only guarantees that if this session dies the same way, the next one inherits a
# written pipeline instead of a reconstruction.
#
# THE DAY NUMBER. This is DAY 13, not day 14, and this session published the wrong number first
# (`ERRATA-135.md` E49). The series numbers MEASUREMENT DAYS: `interval-metrics-133.json` records
# n_measurement_days 12 for day 12 (2026-08-23), and a .partial is never a run, so session 134's
# lost attempt did not consume the ordinal. This run is the second attempt at day 13.
#
# THE COMPARISON DAY IS 2026-08-23 — the last COMPLETED measurement day. 2026-08-24 has no run
# file and is not used, is not reconstructed from its 212,692-byte .partial, and is not filled in
# later at another hour. The interval is therefore 2.0000 days and NOT 1.0000.
#
# THE STREAK ENDS AT FIVE, NOT SIX (`ERRATA-135.md` E50). DAY12-2026-08-23.md states it in its own
# words: "the fifth one-day interval in a row." The "sixth" that this session first published was
# read out of session 134's own pre-run script — a FORECAST for a run that never completed. A
# figure from a run that does not exist is not a property of the series.
#
# ON THE INTERVAL SERIES: the ten day-to-day intervals before today ran 1, 4, 2, 1, 4, 1, 5, 2, 0,
# 4. Whatever day 13 returns, `CONDITIONS-132.md` item 5 and downstream condition 30(b) bind this
# session as they bound the last three: NO TREND IS CLAIMED AND NO TEST IS SCORED. This arc has
# published against itself that six events is not a rate, and eleven are not either. A two-day
# interval is additionally NOT comparable to the one-day intervals beside it, and nothing here may
# read a larger transition count off a longer interval as a change in the field.
#
# Day 13 is OUTSIDE the pre-registered window and no pre-registered test is scored on it.
#
# WHAT IS DELIBERATELY ABSENT, AND IT IS STILL THE POINT: there is no `build_letter.py` step here
# and there must not be. `CONDITIONS-128.md`'s stop — left unchanged by item 1 of CONDITIONS-131
# through -134, and re-examined and DELIBERATELY HELD by this session (`INCREMENT-23.md` §3,
# decision HOLD AND ASK) — forbids this arc any delivery object, repair pass, gauntlet or packet
# before 2026-09-05. This session measured that stop against the clock, found the arithmetic
# against it, and held it anyway. A build step quietly inherited from an earlier day's script is
# exactly how a stop stops being one. This file is day 12's pipeline with the dates and the
# comparison day moved and nothing else moved; that is the whole of the diff and it is stated so
# that nobody has to take it on trust.
set -e
PREV=ledger/run-2026-08-23T0341Z.json
CUR=ledger/run-2026-08-25T0341Z.json

test -f "$CUR" || { echo "day 13 has no completed run file - a .partial is never a run" >&2; exit 1; }

python3 ledger_diff.py "$PREV" "$CUR" ledger/diff-day12-day13.json
python3 ledger_diff.py "$PREV" "$CUR" ledger/diff-day12-day13-overlay.json --corrections
python3 confirm_transition.py ledger/diff-day12-day13.json ledger/transition-confirm-2026-08-25.json
python3 confirmation_record_121.py
python3 window_status.py window-status-135.json
python3 interval_metrics.py "$PREV" "$CUR" ledger/diff-day12-day13.json \
    ledger/transition-confirm-2026-08-25.json -o interval-metrics-135.json \
    --note "day 13, second attempt: the seventh run outside the pre-registered window, 2.0000 days after the last COMPLETED run (2026-08-23). 2026-08-24 is a hole - session 134 died mid-run and left a .partial, which is never a run - so this interval spans two calendar days and is NOT comparable to the one-day intervals beside it. No pre-registered test is scored on it, no trend is claimed, and a transition count over two days may not be read against the one-day counts. The streak of consecutive one-day intervals ended at FIVE (ERRATA-135.md E50; the 'sixth' was a forecast in a dead session's script). Run under the stop of CONDITIONS-128.md, which THIS session measured against the constitution's own clock and deliberately HELD (INCREMENT-23.md, decision HOLD AND ASK): the instrument keeps measuring, and nothing is built to send."
