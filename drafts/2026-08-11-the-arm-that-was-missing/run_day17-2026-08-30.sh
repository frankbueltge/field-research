#!/bin/sh
# DAY 17 OF THE SERIES — the eleventh run outside the pre-registered window. Session 139, 2026-08-30.
#
# THIS IS THE SESSION'S FIRST ACT: `CONDITIONS-138.md` item 9 firing as written — "If a session
# opens near 03:41:00Z, the run is its first act." This session opened at 03:36:24Z, under five
# minutes before the hour. The reservation is taken before the hold, in the same process, so a
# session opening during the hold sees a live lock and refuses.
#
# THE DAY NUMBER. The series numbers MEASUREMENT DAYS, not calendar days (`window_status.py`,
# `DAY_NUMBERING`). `interval-metrics-138.json` records day 16 for 2026-08-29. This run is DAY 17.
#
# THE COMPARISON DAY IS 2026-08-29 (day 16), the last COMPLETED run, and the interval is 1.0000
# day. The interval before it was also 1.0000 day, so for the first time in four intervals the two
# are of equal exposure — which is a fact about the exposure, NOT a licence to read a trend across
# them. No pre-registered test is scored on a day outside the window, and this arc has published
# against itself that six events is not a rate and that eleven are not either.
#
# The hour is NOT moved and no substitute measurement is taken at a different hour
# (`CONDITIONS-138.md` item 8). Launched at 03:41:00Z.
#
# The arc's delivery objects remain stopped (`POST-MORTEM.md`, `CONDITIONS-128.md`, and items 1 of
# `CONDITIONS-131.md` through `-138.md` item 10). The stop is on building things to send, not on
# measuring: "a dark instrument is a finding to record, never a silence." This run is the instrument
# continuing under that clause and nothing else.
exec python3 run_window_day.py manifest-day2-onward.json \
    ledger/run-2026-08-30T0341Z.json 2026-08-30T03:41:00Z
