#!/bin/sh
# DAY 14 OF THE SERIES — the eighth run outside the pre-registered window. Session 136, 2026-08-26.
#
# THIS IS THE SESSION'S FIRST ACT: `CONDITIONS-135.md` item 4 firing as written — "If a session
# opens near 03:41:00Z, the run is its first act." This session opened at 03:36:37Z, four minutes
# and twenty-three seconds before the hour. The reservation is taken before the hold, in the same
# process, so a session opening during the hold sees a live lock and refuses.
#
# THE DAY NUMBER. The series numbers MEASUREMENT DAYS, not calendar days: `interval-metrics-135.json`
# records day 13 for 2026-08-25, and 2026-08-24 is a hole (session 134 died mid-run and left a
# .partial; a partial is never a run). This run is DAY 14. `CONDITIONS-135.md` item 5 records that
# this convention is stated nowhere in the repository and cost session 135 two published figures;
# closing that gap is this session's business, not this script's.
#
# THE COMPARISON DAY IS 2026-08-25 (day 13), the last COMPLETED run, and the interval is 1.0000 day.
# The interval before it was 2.0000 days and is NOT comparable to the one-day intervals beside it;
# nothing in this run's record may read the two against each other.
#
# The hour is NOT moved and no substitute measurement is taken at a different hour
# (`CONDITIONS-135.md` item 3). Launched at 03:41:00Z.
#
# The arc's delivery objects remain stopped (`POST-MORTEM.md`, `CONDITIONS-128.md`, and items 1 of
# `CONDITIONS-131.md` through `-135.md`). The stop is on building things to send, not on measuring:
# "a dark instrument is a finding to record, never a silence." This run is the instrument continuing
# under that clause and nothing else.
exec python3 run_window_day.py manifest-day2-onward.json \
    ledger/run-2026-08-26T0341Z.json 2026-08-26T03:41:00Z
