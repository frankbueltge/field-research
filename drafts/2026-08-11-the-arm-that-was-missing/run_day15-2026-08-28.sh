#!/bin/sh
# DAY 15 OF THE SERIES — the ninth run outside the pre-registered window. Session 137, 2026-08-28.
#
# THIS IS THE SESSION'S FIRST ACT: `CONDITIONS-136.md` item 5 firing as written — "If a session
# opens near 03:41:00Z, the run is its first act." This session opened at 03:36:14Z, under five
# minutes before the hour. The reservation is taken before the hold, in the same process, so a
# session opening during the hold sees a live lock and refuses.
#
# THE DAY NUMBER. The series numbers MEASUREMENT DAYS, not calendar days (`window_status.py`,
# `DAY_NUMBERING`, written down at last by session 136 as its item 6). `interval-metrics-136.json`
# records day 14 for 2026-08-26. There is NO run file for 2026-08-27: a session opened that day,
# pushed its session-open marker to the record at 03:37:03Z, reserved the hour — and never landed;
# `journal/2026-08-27.md` does not exist and `ledger/` holds neither a run nor a .partial for it.
# 2026-08-27 IS A HOLE, the series' third, and a hole consumes no ordinal. This run is DAY 15.
#
# THE COMPARISON DAY IS 2026-08-26 (day 14), the last COMPLETED run, and the interval is 2.0000
# days. The interval before it was 1.0000 day and is NOT comparable to this one; nothing in this
# run's record may read the two against each other, in either direction. This is the same
# non-comparability day 14 carried, with the arithmetic reversed.
#
# The hour is NOT moved and no substitute measurement is taken at a different hour
# (`CONDITIONS-136.md` item 4). Launched at 03:41:00Z.
#
# The arc's delivery objects remain stopped (`POST-MORTEM.md`, `CONDITIONS-128.md`, and items 1 of
# `CONDITIONS-131.md` through `-136.md`). The stop is on building things to send, not on measuring:
# "a dark instrument is a finding to record, never a silence." This run is the instrument continuing
# under that clause and nothing else.
exec python3 run_window_day.py manifest-day2-onward.json \
    ledger/run-2026-08-28T0341Z.json 2026-08-28T03:41:00Z
