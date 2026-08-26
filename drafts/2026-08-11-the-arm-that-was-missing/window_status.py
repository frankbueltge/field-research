#!/usr/bin/env python3
"""window_status - the state of the measurement window, read from the ledger and never remembered.

Session 126, 2026-08-18. Written because of erratum E21: the previous session launched day 7 of
the pre-registered window, ended before the run closed at 600 of 3,869 units, and reported the day
as complete and the window as closed - in the same file that had, four hours earlier, stated the
rule it broke.

THE RULE THIS ENFORCES
----------------------
**A `.partial` is never a run.** This practice wrote that sentence in three consecutive sessions
and each time enforced it by hand. Enforcing a rule by hand is how a rule survives until the
session that is tired, or in a hurry, or convinced by its own opening paragraph. A day counts as
measured here only if a NON-PARTIAL run file exists for it and parses. Nothing else counts: not a
scheduled run, not a launched run, not a run whose checkpoint is large, not a run this session
watched start.

WHAT IT REPORTS
---------------
- Every completed run, with its start time and how many units it actually measured.
- Every partial with no completed run beside it - **named as a HOLE, with how far it got.**
- The intervals between consecutive completed runs, in days, so a two-day gap cannot be reported
  as a daily cadence by anybody quoting a count.
- Whether the pre-registered window (seven consecutive daily runs) is met - which is a conjunction
  of two things, the count AND the consecutiveness, and E21 happened partly because those two were
  carried in one word.

It deliberately does not know what the pre-registration says beyond the two constants below; a
guard that reasons about intent is a guard that can be talked round.
"""
import glob
import json
import os
import sys
import time

import run_lock

REQUIRED_RUNS = 7
DAILY_TOLERANCE = 0.10          # a "daily" interval is 1.00 +/- this, in days

# THE DAY-NUMBERING CONVENTION, WRITTEN DOWN AT LAST. Session 136, 2026-08-26, closing item 5 of
# `CONDITIONS-135.md`: "THE SERIES NUMBERS MEASUREMENT DAYS, NOT CALENDAR DAYS, AND NOTHING STATES
# THAT... The rule lives in a JSON field and in prose that contradicts itself. A one-line statement
# beside window_status.py closes it." The rule was being applied and never stated, and its absence
# cost session 135 two published figures - one of them pushed to origin (`ERRATA-135.md` E49) - when
# a session took the calendar position for the day number after a session died mid-run. It is now
# emitted into every window-status file this script writes, so a reader of the output never has to
# find this comment.
DAY_NUMBERING = (
    "Day N is the Nth MEASUREMENT DAY, not the Nth calendar day since the series began. A "
    "measurement day is a date with a non-partial run file that parses. A hole - a date with a "
    ".partial and no run file - consumes NO ordinal: the next completed run takes the number the "
    "lost attempt was reaching for. A same-day second probe is not a measurement day either. "
    "n_measurement_days below is therefore the number of the most recent completed day, and the "
    "count of dates in measurement_days is the only thing that determines it."
)
LEDGER = "ledger"


def _start_of(run):
    for k in ("run_utc_start", "run_id", "started_utc"):
        v = run.get(k)
        if isinstance(v, str) and len(v) >= 20 and v[4] == "-":
            return v[:20]
    return None


def _epoch(ts):
    return time.mktime(time.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")) - time.timezone


def _live_reservation(ledger, partial_path):
    """The reservation holding this partial, if a live process holds one for its UTC day.

    Liveness is `run_lock`'s own test and inherits its stated limit: it asks whether a process
    with that pid exists, not whether it is this probe. A recycled pid reads as live.
    """
    base = os.path.basename(partial_path)
    try:
        day = base.split("run-")[1][:10]
    except (IndexError, ValueError):
        return None
    for lock_path in sorted(glob.glob(os.path.join(ledger, ".run-lock-*.json"))):
        try:
            held = json.load(open(lock_path))
        except Exception:
            continue
        if held.get("utc_day") != day:
            continue
        if not run_lock._alive(held.get("pid")):
            continue
        return {"lock_file": lock_path, "pid": held.get("pid"),
                "started_utc": held.get("started_utc"),
                "out_path": held.get("out_path"),
                "liveness_test": "run_lock._alive: a process with this pid exists"}
    return None


def scan(ledger=LEDGER):
    completed, holes, in_flight = [], [], []

    for path in sorted(glob.glob(os.path.join(ledger, "run-*.json"))):
        if path.endswith(".partial"):
            continue
        try:
            run = json.load(open(path))
        except Exception as exc:                      # a file that will not parse is not a run
            holes.append({"file": path, "why": "does not parse: " + str(exc)})
            continue
        if run.get("partial"):
            holes.append({"file": path, "why": "the file declares itself partial"})
            continue
        obs = run.get("observations")
        completed.append({
            "file": path,
            "start_utc": _start_of(run),
            "n_observations": len(obs) if isinstance(obs, list) else None,
            "n_planned": run.get("planned"),
        })

    for path in sorted(glob.glob(os.path.join(ledger, "run-*.json.partial"))):
        done = path[: -len(".partial")]
        if os.path.exists(done):
            continue                                  # a checkpoint beside its finished run
        try:
            p = json.load(open(path))
        except Exception:
            p = {}
        obs = p.get("observations")
        entry = {
            "file": path,
            "run_id_it_claims": p.get("run_id"),
            "n_observations": len(obs) if isinstance(obs, list) else p.get("requested"),
            "n_planned": p.get("planned"),
        }
        holder = _live_reservation(ledger, path)
        if holder:
            # SESSION 127. A partial being written RIGHT NOW by a live process is not an
            # abandoned day, and calling it one puts a false sentence about this practice's own
            # instrument into anything built while a run is in flight - which is exactly what
            # happened when the short object was first built at 03:46Z on 2026-08-19. It is
            # still NOT a measurement day: the rule is unchanged and a .partial is still never a
            # run. It is reported apart from the holes because "started and abandoned" and
            # "measuring at this moment" are different facts about the instrument.
            entry["why"] = ("a partial being written by a live reservation - the day is IN "
                            "FLIGHT, not abandoned, and is not counted as measured either way")
            entry["reservation"] = holder
            in_flight.append(entry)
        else:
            entry["why"] = ("a partial with no completed run beside it - the day was started "
                            "and not taken")
            holes.append(entry)

    completed.sort(key=lambda r: r["start_utc"] or "")

    # A MEASUREMENT DAY IS NOT A RUN FILE. On 2026-08-16 two complete probes ran over the same
    # manifest at the same second, from two sessions that could not see each other
    # (DOUBLE-PROBE-122.md); both are preserved and both are legitimate files, but they are ONE
    # measurement day and counting them as two would overstate the window by exactly the kind of
    # bookkeeping error this guard exists to prevent. The first run of a UTC day is the day; any
    # further completed run of the same day is reported separately as an extra pass.
    days, extra_passes = [], []
    for r in completed:
        key = (r["start_utc"] or "")[:10]
        if days and (days[-1]["start_utc"] or "")[:10] == key:
            extra_passes.append(r)
        else:
            days.append(r)

    intervals = []
    for a, b in zip(days, days[1:]):
        if not (a["start_utc"] and b["start_utc"]):
            intervals.append(None)
            continue
        d = (_epoch(b["start_utc"]) - _epoch(a["start_utc"])) / 86400.0
        intervals.append({
            "from": a["start_utc"], "to": b["start_utc"], "days": round(d, 4),
            "is_daily": abs(d - 1.0) <= DAILY_TOLERANCE,
        })

    non_daily = [i for i in intervals if i and not i["is_daily"]]
    n = len(days)
    return {
        "schema": "field-research/window-status/1",
        "computed_by": "window_status.py",
        "rule": "a .partial is never a run; a day counts only if a non-partial run file exists",
        "day_numbering_convention": DAY_NUMBERING,
        "n_measurement_days": n,
        "measurement_days": days,
        "n_completed_run_files": len(completed),
        "n_extra_passes_same_day": len(extra_passes),
        "extra_passes_same_day": extra_passes,
        "n_holes": len(holes),
        "holes": holes,
        "n_in_flight": len(in_flight),
        "in_flight": in_flight,
        "in_flight_note": (
            "a run being written by a live reservation at the moment of this scan. Never counted "
            "as a measurement day - the rule is unchanged - and never reported as an abandoned "
            "day either. A status file written during a run says so; one written after it does "
            "not, and the two are not in conflict."),
        "intervals_days": intervals,
        "n_intervals_not_daily": len(non_daily),
        "intervals_not_daily": non_daily,
        "required_runs": REQUIRED_RUNS,
        "count_requirement_met": n >= REQUIRED_RUNS,
        "consecutive_daily": bool(intervals) and not non_daily,
        "preregistered_window_met": n >= REQUIRED_RUNS and bool(intervals) and not non_daily,
        "why_two_conditions": (
            "'seven consecutive daily runs' is a conjunction: the COUNT and the CONSECUTIVENESS. "
            "Erratum E21 reported the window closed while neither held. They are reported "
            "separately here so a later session cannot collapse them into one word again."
        ),
    }


def main(argv):
    # NOT window-status-126.json: that file is session 126's landed record and this script must
    # not overwrite a previous session's committed artifact when it is re-run.
    out = argv[0] if argv else "window-status.json"
    st = scan()
    json.dump(st, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in st.items()
                      if k not in ("measurement_days", "extra_passes_same_day", "holes",
                                   "intervals_days")}, indent=1))
    for f in st["in_flight"]:
        print("IN FLIGHT: " + f["file"] + " - pid " + str(f["reservation"]["pid"])
              + " (" + str(f.get("n_observations")) + " of " + str(f.get("n_planned")) + ")")
    for h in st["holes"]:
        print("HOLE: " + h["file"] + " - " + h["why"]
              + (" (" + str(h.get("n_observations")) + " of " + str(h.get("n_planned")) + ")"
                 if h.get("n_planned") else ""))
    for i in st["intervals_not_daily"]:
        print("NOT DAILY: " + i["from"] + " -> " + i["to"] + " = " + str(i["days"]) + " days")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
