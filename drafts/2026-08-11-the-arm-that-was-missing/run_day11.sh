#!/bin/sh
# DAY 11 OF THE SERIES — the fourth run outside the pre-registered window. Session 132, 2026-08-22.
#
# THIS IS THE SESSION'S FIRST ACT, and that is `CONDITIONS-131.md`'s binding item 3 firing exactly
# as written: "If a session opens near 03:41:00Z, the run is its first act — the reservation is
# cheap, reversible and holds the day against nothing else." This session opened at 03:35:54Z, five
# minutes and six seconds before the hour. Session 131 opened three hours and eighteen minutes
# before it and could not reach it; this one can, and reaching it is the whole of what the arc is
# licensed to do.
#
# The arc's delivery objects are stopped (`POST-MORTEM.md`, `CONDITIONS-128.md`, `CONDITIONS-131.md`
# item 1). The stop is on building things to send, not on measuring: "a dark instrument is a finding
# to record, never a silence." This run is the instrument continuing under that clause and nothing
# else.
#
# The hour is NOT moved and no substitute measurement is taken at a different hour
# (`CONDITIONS-131.md` item 2). Launched at 03:41:00Z, exactly 1.0000 days after the last completed
# run's start second (2026-08-21T03:41:00Z) — the fourth one-day interval in a row.
#
# A partial file is never a run: if this session ends before it closes, day 11 is a hole and this
# comment is not a substitute for the data.
exec python3 run_window_day.py manifest-day2-onward.json \
    ledger/run-2026-08-22T0341Z.json 2026-08-22T03:41:00Z
