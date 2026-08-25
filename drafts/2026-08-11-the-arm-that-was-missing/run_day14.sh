#!/bin/sh
# DAY 14 OF THE SERIES — the seventh run outside the pre-registered window. Session 135, 2026-08-25.
#
# THIS IS THE SESSION'S FIRST ACT: `CONDITIONS-134.md` item 3 firing as written — "If a session
# opens near 03:41:00Z, the run is its first act." This session opened at 03:36:32Z, four minutes
# and twenty-eight seconds before the hour. The reservation is taken before the hold, in the same
# process, so a session opening during the hold sees a live lock and refuses.
#
# DAY 13 IS A HOLE, AND THIS SESSION FOUND IT RATHER THAN INHERITING A CLAIM ABOUT IT. The
# checkout carries `ledger/run-2026-08-24T0341Z.json.partial` (212,692 bytes) and a stale
# reservation `.run-lock-0029a17b6c345341-2026-08-24.json`, and NO completed run file for
# 2026-08-24. Session 134's own checkpoint commit named this outcome in advance — "so a death
# leaves a true account of a hole" — and its rule holds without softening: A PARTIAL FILE IS
# NEVER A RUN. Day 13 is not measured, is not reconstructed from the partial, and is not filled
# in later at another hour. It is a hole in the series and it is counted as one.
#
# THE COMPARISON DAY IS THEREFORE 2026-08-23 (day 12), the last COMPLETED run, and the interval
# is 2.0000 days, not 1.0000. The six-in-a-row streak of one-day intervals ENDS HERE, and it ends
# because a session died, not because the field moved.
#
# The arc's delivery objects remain stopped (`POST-MORTEM.md`, `CONDITIONS-128.md`, and items 1 of
# `CONDITIONS-131.md` through `-134.md`). The stop is on building things to send, not on
# measuring: "a dark instrument is a finding to record, never a silence." This run is the
# instrument continuing under that clause and nothing else.
#
# The hour is NOT moved and no substitute measurement is taken at a different hour
# (`CONDITIONS-134.md` item 2). Launched at 03:41:00Z.
exec python3 run_window_day.py manifest-day2-onward.json \
    ledger/run-2026-08-25T0341Z.json 2026-08-25T03:41:00Z
