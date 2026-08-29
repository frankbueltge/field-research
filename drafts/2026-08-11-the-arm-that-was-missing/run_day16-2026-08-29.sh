#!/bin/sh
# DAY 16 OF THE SERIES — the tenth run outside the pre-registered window. Session 138, 2026-08-29.
#
# THIS IS THE SESSION'S FIRST ACT: `CONDITIONS-137.md` item 5 firing as written — "If a session
# opens near 03:41:00Z, the run is its first act." This session opened at 03:36:09Z, under five
# minutes before the hour. The reservation is taken before the hold, in the same process, so a
# session opening during the hold sees a live lock and refuses.
#
# THE DAY NUMBER. The series numbers MEASUREMENT DAYS, not calendar days (`window_status.py`,
# `DAY_NUMBERING`). `interval-metrics-137.json` records day 15 for 2026-08-28. This run is DAY 16.
#
# THE COMPARISON DAY IS 2026-08-28 (day 15), the last COMPLETED run, and the interval is 1.0000
# day. THE INTERVAL BEFORE IT WAS 2.0000 DAYS AND IS NOT COMPARABLE TO THIS ONE; nothing in this
# run's record may read the two against each other, in either direction. This is the same
# non-comparability day 15 carried, with the arithmetic reversed again.
#
# The hour is NOT moved and no substitute measurement is taken at a different hour
# (`CONDITIONS-137.md` item 4). Launched at 03:41:00Z.
#
# The arc's delivery objects remain stopped (`POST-MORTEM.md`, `CONDITIONS-128.md`, and items 1 of
# `CONDITIONS-131.md` through `-137.md` item 6). The stop is on building things to send, not on
# measuring: "a dark instrument is a finding to record, never a silence." This run is the instrument
# continuing under that clause and nothing else.
exec python3 run_window_day.py manifest-day2-onward.json \
    ledger/run-2026-08-29T0341Z.json 2026-08-29T03:41:00Z
