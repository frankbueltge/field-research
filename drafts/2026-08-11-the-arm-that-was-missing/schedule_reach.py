#!/usr/bin/env python3
"""schedule_reach - how far the instrument's daily hour sits from the session that must reach it.

Session 131, 2026-08-22. Written because this session could not reach the instrument's licensed
hour and wanted the reason computed rather than asserted.

WHAT THIS IS AND IS NOT
-----------------------
It is bookkeeping about the instrument's own schedule, computed from files already committed to
this repository: the eleven run files under `ledger/`, and the opening times the journal entries
state about themselves. It builds nothing to send and reads nothing new from the network.

It is NOT a claim about an "hour effect" on what the probe measures. Start hour and calendar day
stand in bijection in this record - one run per date - so no procedure here or anywhere else can
separate them, and none is attempted. The quantity computed is a different one and it is not
confounded: the distance in seconds between two recorded timestamps, the session's opening and
the run's start.

SOURCES, AND WHY NOTHING IS TYPED
---------------------------------
Opening times are EXTRACTED by regular expression from `journal/*.md`, not transcribed, so the
figures are read out of the record rather than retyped into it. The convention of stating the
opening time in the opening record begins at 2026-08-16; entries before that date state no
opening time and are reported as unknown rather than guessed. The running session's own opening
is supplied on the command line, because it is not yet in any journal, and is labelled as such.

    python3 schedule_reach.py --today-open 2026-08-22T00:23:16Z \\
        --today-due 2026-08-22T03:41:00Z -o schedule-reach-131.json
"""
import argparse
import calendar
import glob
import json
import os
import re
import statistics
import time

# "opened at 03:36:38Z", "this session opened at 03:35Z", "this one opened at 14:30Z",
# "opened at **03:36:39Z**" - and the same sentence broken across a line, hence the whitespace
# class rather than a literal space.
OPEN_RE = re.compile(r"opened\s+at\s+\*{0,2}(\d{2}:\d{2}(?::\d{2})?)\*{0,2}Z")
# "# Session 129 — 2026-08-21", including the "(second session of the same date)" variants.
SESSION_RE = re.compile(r"^#\s+Session\s+(\d+)\s+", re.MULTILINE)


def ts(s):
    return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))


def hms(seconds):
    seconds = int(round(seconds))
    sign = "-" if seconds < 0 else ""
    seconds = abs(seconds)
    return "%s%dh %02dm %02ds" % (sign, seconds // 3600, (seconds % 3600) // 60, seconds % 60)


def journal_openings(journal_dir):
    """One row per SESSION, not per mention of an opening time.

    The first version of this function matched the whole file and returned a row per match. That
    is wrong twice over in the record it was pointed at: session 123 states its own opening at two
    places in `journal/2026-08-16.md` (lines 180 and 263) and session 130 states its own at two
    places in `journal/2026-08-21.md` (lines 242 and 337), so a date with three sessions was
    reported as having two and a date with two as having three. Found by reading the rows against
    the journals' own `# Session` headings; corrected here rather than in the prose that quotes it.

    So: split each journal on its session headings, and take the FIRST stated opening inside each
    session's own block. A session that states none is returned with `utc: None` and counted, not
    dropped - a silence about the opening hour is itself part of what this file measures.
    """
    out = {}
    for path in sorted(glob.glob(os.path.join(journal_dir, "2026-*.md"))):
        date = os.path.basename(path)[:-3]
        text = open(path, encoding="utf-8").read()
        heads = list(SESSION_RE.finditer(text))
        if not heads:
            continue
        rows = []
        for i, h in enumerate(heads):
            start = h.start()
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            block = text[start:end]
            m = OPEN_RE.search(block)
            row = {"session": int(h.group(1)), "utc": None, "source": None,
                   "stated_precision": None, "quoted": None}
            if m:
                clock = m.group(1)
                row["stated_precision"] = "second" if len(clock) == 8 else "minute"
                if row["stated_precision"] == "minute":
                    clock += ":00"
                line = text.count("\n", 0, start + m.start()) + 1
                row["utc"] = date + "T" + clock + "Z"
                row["source"] = "journal/%s.md:%d" % (date, line)
                row["quoted"] = " ".join(block[max(0, m.start() - 40):m.end() + 4].split())
            rows.append(row)
        out[date] = rows
    return out


def runs(ledger_dir):
    """Every completed run file. A .partial is never a run and is not read here."""
    out = []
    for path in sorted(glob.glob(os.path.join(ledger_dir, "run-*.json"))):
        d = json.load(open(path, encoding="utf-8"))
        out.append({
            "file": os.path.basename(path),
            "date": d["run_utc_start"][:10],
            "start": d["run_utc_start"],
            "end": d["run_utc_end"],
            "seconds": d["seconds"],
            "requested": d["requested"],
            "planned": d["planned"],
            "stopped": d["stopped"],
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--journal-dir", default="../../journal")
    ap.add_argument("--ledger-dir", default="ledger")
    ap.add_argument("--today-open", required=True)
    ap.add_argument("--today-due", required=True)
    ap.add_argument("-o", "--out", default="schedule-reach-131.json")
    a = ap.parse_args()

    openings = journal_openings(a.journal_dir)
    rr = runs(a.ledger_dir)

    # One row per date that states an opening. The first stated opening of a date is the session
    # that could have taken that date's run; a second session of the same date opens after the
    # day's hour has passed and is reported, not silently merged.
    by_date_runs = {}
    for r in rr:
        by_date_runs.setdefault(r["date"], []).append(r)

    rows, lags, spans = [], [], []
    for date in sorted(openings):
        for i, op in enumerate(openings[date]):
            # A date's run belongs to whichever session of that date actually started it. The run
            # is attributed to the session whose stated opening is the latest one at or before the
            # run's start second - not to the first session of the date, which on 2026-08-16
            # scheduled the run and ended before it fired.
            day_runs = by_date_runs.get(date, [])
            if day_runs and op["utc"]:
                first_start = sorted(r["start"] for r in day_runs)[0]
                later = [o for o in openings[date]
                         if o["utc"] and o["utc"] <= first_start]
                owner = max(later, key=lambda o: o["utc"]) if later else None
                if owner is not op:
                    day_runs = []
            elif not op["utc"]:
                day_runs = []
            row = {
                "date": date,
                "session": op["session"],
                "session_index_on_date": i + 1,
                "session_open_utc": op["utc"],
                "opening_source": op["source"],
                "stated_precision": op["stated_precision"],
                "run_started_utc": None,
                "run_ended_utc": None,
                "lag_open_to_run_seconds": None,
                "session_span_lower_bound_seconds": None,
            }
            if day_runs:
                first = sorted(day_runs, key=lambda x: x["start"])[0]
                row["run_started_utc"] = first["start"]
                row["run_ended_utc"] = first["end"]
                row["run_file"] = first["file"]
                row["runs_on_this_date"] = len(day_runs)
                lag = ts(first["start"]) - ts(op["utc"])
                span = ts(first["end"]) - ts(op["utc"])
                row["lag_open_to_run_seconds"] = lag
                row["lag_open_to_run"] = hms(lag)
                # The session demonstrably lived at least from its opening to the moment its run
                # closed: it wrote the closed run file. This is a floor, never the session's length.
                row["session_span_lower_bound_seconds"] = span
                row["session_span_lower_bound"] = hms(span)
                lags.append(lag)
                spans.append(span)
            rows.append(row)

    durations = [r["seconds"] for r in rr if r["stopped"] is None and r["planned"] == r["requested"]]
    full_panel = [r for r in rr if r["requested"] == 3869]
    full_durations = [r["seconds"] for r in full_panel]

    open_ts, due_ts = ts(a.today_open), ts(a.today_due)
    wait = due_ts - open_ts
    med = statistics.median(full_durations)
    required = wait + med
    longest_span = max(spans) if spans else None

    # Intervals actually present in this series, so a claim about what is or is not an unusual
    # interval is read off the record rather than remembered.
    starts = sorted(r["start"] for r in rr)
    intervals = []
    for p, c in zip(starts, starts[1:]):
        if p == c:
            continue  # the two probes of 2026-08-16 share a start second (DOUBLE-PROBE-122.md)
        intervals.append(round((ts(c) - ts(p)) / 86400.0, 4))

    out = {
        "schema": "field-research/schedule-reach/1",
        "computed_by": "schedule_reach.py, session 131",
        "computed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "what_this_is": (
            "the distance between the session opening the record states and the second the "
            "instrument's run actually started, for every date whose journal states an opening. "
            "It is not a claim about any effect of the hour on what the probe measures: start "
            "hour and calendar day are in bijection in this record and cannot be separated."
        ),
        "opening_times_extracted_not_typed": True,
        "dates_before_2026_08_16_state_no_opening_time": True,
        "rows": rows,
        "lag_open_to_run": {
            "n": len(lags),
            "min_seconds": min(lags) if lags else None,
            "median_seconds": statistics.median(lags) if lags else None,
            "max_seconds": max(lags) if lags else None,
            "all_within_ten_minutes": all(0 <= l <= 600 for l in lags) if lags else None,
        },
        "session_span_lower_bounds": {
            "n": len(spans),
            "min": hms(min(spans)) if spans else None,
            "max": hms(longest_span) if spans else None,
            "max_seconds": longest_span,
            "note": "a floor per session, derived from the run file it closed; never its length",
        },
        "run_duration_seconds_full_panel": {
            "n": len(full_durations),
            "min": min(full_durations),
            "median": med,
            "max": max(full_durations),
        },
        "series_intervals_days": intervals,
        "today": {
            "session_open_utc": a.today_open,
            "opening_source": "supplied by the running session; not yet in any journal",
            "run_due_utc": a.today_due,
            "wait_seconds": wait,
            "wait": hms(wait),
            "required_session_span_seconds": required,
            "required_session_span": hms(required),
            "required_over_longest_documented_span": (
                round(required / longest_span, 2) if longest_span else None
            ),
        },
    }
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({k: out[k] for k in
                      ["lag_open_to_run", "session_span_lower_bounds",
                       "run_duration_seconds_full_panel", "series_intervals_days", "today"]},
                     indent=1))


if __name__ == "__main__":
    main()
