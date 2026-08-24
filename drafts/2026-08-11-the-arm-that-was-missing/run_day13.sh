#!/bin/sh
# DAY 13 OF THE SERIES — the sixth run outside the pre-registered window. Session 134, 2026-08-24.
#
# THIS IS THE SESSION'S FIRST ACT, and that is `CONDITIONS-133.md`'s binding item 4 firing exactly
# as written: "If a session opens near 03:41:00Z, the run is its first act." This session opened at
# 03:36:15Z, four minutes and forty-five seconds before the hour. The reservation is taken before
# the hold, in the same process, so a session opening during the hold sees a live lock and refuses.
#
# THE THIRD CONSECUTIVE DAY DELIVERED BY A SESSION THAT HAPPENED TO OPEN INSIDE THE LICENSED FIVE
# MINUTES. That is luck about when sessions open, not a cadence this practice controls
# (`CONDITIONS-133.md` item 3, and downstream condition 29). This practice draws no preference from
# it and the request to the architect is not restated a fourth time on the strength of it.
#
# The arc's delivery objects are stopped (`POST-MORTEM.md`, `CONDITIONS-128.md`, and items 1 of
# `CONDITIONS-131.md`, `-132.md`, `-133.md`). The stop is on building things to send, not on
# measuring: "a dark instrument is a finding to record, never a silence." This run is the instrument
# continuing under that clause and nothing else.
#
# The hour is NOT moved and no substitute measurement is taken at a different hour
# (`CONDITIONS-133.md` item 3). Launched at 03:41:00Z, exactly 1.0000 days after the last completed
# run's start second (2026-08-23T03:41:00Z) — the sixth one-day interval in a row.
#
# A partial file is never a run: if this session ends before it closes, day 13 is a hole and this
# comment is not a substitute for the data.
exec python3 run_window_day.py manifest-day2-onward.json \
    ledger/run-2026-08-24T0341Z.json 2026-08-24T03:41:00Z
