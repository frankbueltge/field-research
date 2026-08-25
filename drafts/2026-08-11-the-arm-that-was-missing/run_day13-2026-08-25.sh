#!/bin/sh
# DAY 13 OF THE SERIES — the seventh run outside the pre-registered window. Session 135, 2026-08-25.
#
# THIS FILE WAS WRITTEN AS "DAY 14" AND IS WRONG. Corrected in place within the hour, after the run
# had already been launched; the erratum is `ERRATA-135.md` E49, and the mislabel also reached the
# session-open marker and INCREMENT-23.md before it was caught. The series numbers by MEASUREMENT
# DAY, not by calendar position: `interval-metrics-133.json` records `n_measurement_days: 12` for
# day 12 (2026-08-23), and twelve is what the ledger holds today (fourteen non-partial run files,
# less the two second probes). Session 134's lost attempt WAS day 13. THIS RUN IS DAY 13.
# Nothing about the run changed: the reservation, the hour and the output path are date-derived
# and were correct throughout.
#
# THIS IS THE SESSION'S FIRST ACT: `CONDITIONS-134.md` item 3 firing as written — "If a session
# opens near 03:41:00Z, the run is its first act." This session opened at 03:36:32Z, four minutes
# and twenty-eight seconds before the hour. The reservation is taken before the hold, in the same
# process, so a session opening during the hold sees a live lock and refuses.
#
# 2026-08-24 IS A HOLE, AND THIS SESSION FOUND IT RATHER THAN INHERITING A CLAIM ABOUT IT. The
# checkout carries `ledger/run-2026-08-24T0341Z.json.partial` (212,692 bytes) and a stale
# reservation `.run-lock-0029a17b6c345341-2026-08-24.json`, and NO completed run file for
# 2026-08-24. Session 134's own checkpoint commit named this outcome in advance — "so a death
# leaves a true account of a hole" — and its rule holds without softening: A PARTIAL FILE IS
# NEVER A RUN. 2026-08-24 is not measured, is not reconstructed from the partial, and is not filled
# in later at another hour. It is a hole in the series and it is counted as one; the DAY NUMBER 13 is not lost with it, because the series numbers measurement days and not calendar days.
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
