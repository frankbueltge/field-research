#!/usr/bin/env python3
"""episode_structure - the receiver's own record, read over its WHOLE length.

Session 129, 2026-08-21. This is the licensed move of `CONDITIONS-128.md`, "Binding on the next
session", item 2: the receiver's own record read properly - the error-episode structure, and the
absent-row control. It is analysis of evidence already held. It builds no delivery object.

WHY THIS EXISTS
---------------
Session 128 extracted these series correctly and printed, for every one of the eleven, a field
`error_days` between 14 and 20 - and nobody asked WHEN those days were. The ninth gauntlet's
adversary asked, and the answer refuted the object's central sentence. This script asks the
question the derivation should have asked on the day it was written, and asks it of the whole
record rather than of its last fortnight.

WHAT IT COMPUTES, AND WHAT EACH THING CAN AND CANNOT SUPPORT
------------------------------------------------------------
1. `date_index` - for every calendar date that appears anywhere in the record, how many series
   carry a row that day and what state each is in. This is a description of the file. It is not a
   description of what the people running the page did.

2. `episodes` - maximal runs of consecutive RECORDED dates on which every series that has a row
   that day is in `Error`. "Consecutive recorded dates" is deliberate: a gap in the record is not
   evidence of continuation and is not evidence of interruption, and this script refuses to guess
   which.

3. `absent_row_control` - the finding this practice took from an adversary at the ninth gauntlet
   and recorded as CLAIMED-AND-UNREPRODUCED (`CONDITIONS-128.md`, finding 15(i)): that an
   unchecked day appears in the record as a MISSING ROW rather than as `Error`. What can actually
   be established from the page alone is narrower than that claim, and the script reports the
   narrower thing plus what would be needed to close the gap. See `absent_row_control.limits`.

4. `series_coverage` - each series' first and last recorded date, because the eleven do not all
   start together and any "all eleven" statement over the early record would be false.

Input is the extractor's output (`receiver-series-2026-08-19.json`), whose own provenance is the
saved page `receiver-dashboard-2026-08-19.html`. Status codes are never assumed: they are read
through each chart's own `y_axis_labels`, and the script fails if two charts disagree about the
mapping.

USAGE
    python3 episode_structure.py [series.json] [-o out.json]
"""
import argparse
import datetime
import json
import sys


def load_series(path):
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    return doc


def code_map(chart):
    """The status mapping, taken from the chart's own axis and never assumed."""
    labels = chart["y_axis_labels"]
    return {int(v): t for v, t in zip(labels["tickvals"], labels["ticktext"])}


def as_date(s):
    return datetime.date.fromisoformat(s[:10])


def build(doc):
    videos = doc["videos"]
    mapping = None
    per_series = {}

    for v in videos:
        vid = v["video_id"]
        charts = [c for c in v["charts"] if c.get("x") and c.get("y")]
        if len(charts) != 1:
            raise SystemExit("video %s has %d usable charts, expected 1" % (vid, len(charts)))
        ch = charts[0]
        m = code_map(ch)
        if mapping is None:
            mapping = m
        elif m != mapping:
            raise SystemExit("charts disagree about the status mapping: %r vs %r" % (mapping, m))
        rows = {}
        for x, y in zip(ch["x"], ch["y"]):
            d = as_date(x)
            if d in rows and rows[d] != mapping[int(y)]:
                raise SystemExit("video %s has two different states on %s" % (vid, d))
            rows[d] = mapping[int(y)]
        per_series[vid] = rows

    return mapping, per_series


def date_index(per_series):
    all_dates = sorted({d for rows in per_series.values() for d in rows})
    index = []
    for d in all_dates:
        states = {vid: rows[d] for vid, rows in per_series.items() if d in rows}
        counts = {}
        for s in states.values():
            counts[s] = counts.get(s, 0) + 1
        index.append({
            "date": d.isoformat(),
            "n_series_with_a_row": len(states),
            "counts": counts,
            "all_rows_error": len(states) > 0 and set(states.values()) == {"Error"},
        })
    return all_dates, index


def episodes(index):
    """Maximal runs of consecutive RECORDED dates on which every row present is Error."""
    out = []
    run = []
    for entry in index:
        if entry["all_rows_error"]:
            run.append(entry)
        else:
            if run:
                out.append(run)
            run = []
    if run:
        out.append(run)

    episodes_out = []
    for run in out:
        first, last = run[0], run[-1]
        i_first = index.index(first)
        i_last = index.index(last)
        before = index[i_first - 1] if i_first > 0 else None
        after = index[i_last + 1] if i_last + 1 < len(index) else None
        d0, d1 = as_date(first["date"]), as_date(last["date"])
        episodes_out.append({
            "first_recorded_date": first["date"],
            "last_recorded_date": last["date"],
            "n_recorded_dates_in_episode": len(run),
            "calendar_span_days": (d1 - d0).days + 1,
            "n_series_with_a_row_on_first_date": first["n_series_with_a_row"],
            "n_series_with_a_row_on_last_date": last["n_series_with_a_row"],
            "state_of_the_record_before": None if before else "episode begins the record",
            "recorded_date_before": before["date"] if before else None,
            "counts_before": before["counts"] if before else None,
            "recorded_date_after": after["date"] if after else None,
            "counts_after": after["counts"] if after else None,
            "cleared": after is not None,
            "days_to_next_recorded_date": (
                (as_date(after["date"]) - d1).days if after else None),
        })
    return episodes_out


def absent_row_control(all_dates, index, per_series):
    """What the page alone can and cannot establish about an unchecked day.

    The adversary's claim (CONDITIONS-128.md finding 15(i)) is that an unchecked day is an ABSENT
    ROW, not an `Error` row, and therefore that the terminal run of `Error` days is a run of checks
    that ran and failed. Two separable things are in that claim:

      (A) The record CAN represent a day with no row at all. This is checkable and is checked.
      (B) An unchecked day IS represented that way rather than as `Error`. This is NOT checkable
          from the page: it is a statement about what the code that writes the page does, and this
          practice has never seen that code.

    (A) makes (B) available as a reading. It does not establish it.
    """
    first, last = all_dates[0], all_dates[-1]
    full = set()
    d = first
    while d <= last:
        full.add(d)
        d += datetime.timedelta(days=1)
    present = set(all_dates)
    missing = sorted(full - present)

    # Per-series holes: a date inside a series' own span with no row for that series, while other
    # series do have a row that day. This is the sharper form of (A).
    per_series_holes = {}
    for vid, rows in per_series.items():
        ds = sorted(rows)
        span = set()
        d = ds[0]
        while d <= ds[-1]:
            span.add(d)
            d += datetime.timedelta(days=1)
        holes = sorted(span - set(ds))
        covered = [h for h in holes if h in present]
        per_series_holes[vid] = {
            "n_holes_inside_own_span": len(holes),
            "n_of_those_on_dates_other_series_do_record": len(covered),
            "examples": [h.isoformat() for h in covered[:5]],
        }

    return {
        "record_first_date": first.isoformat(),
        "record_last_date": last.isoformat(),
        "calendar_days_in_span": (last - first).days + 1,
        "recorded_dates": len(all_dates),
        "dates_missing_from_the_whole_record": [d.isoformat() for d in missing],
        "n_dates_missing_from_the_whole_record": len(missing),
        "per_series_holes": per_series_holes,
        "established": (
            "(A) The record can and does represent a date with no row: %d calendar dates inside "
            "the record's own span carry no row for any series." % len(missing)),
        "not_established": (
            "(B) That an unchecked day is written as a missing row RATHER THAN as `Error`. That is "
            "a statement about the code that writes this page. This practice has not seen that "
            "code and cannot see it from the page. The adversary's inference - that the terminal "
            "`Error` days are checks that ran and failed - is AVAILABLE on this evidence and is "
            "NOT ESTABLISHED by it."),
        "what_would_close_it": (
            "The page's own source, or a statement by its authors about how a skipped check is "
            "recorded. Neither is in this practice's hands."),
    }


def error_runs(per_series):
    """Per-series maximal runs of consecutive RECORDED dates in `Error`.

    This is the quantity the persistence claim actually rests on, and this arc never computed it.
    The trailing run - the one the record ends inside - is reported separately, because it is
    right-censored: the record stops while it is still running, so its length is a lower bound and
    not a duration.
    """
    closed, trailing = [], []
    for vid, rows in per_series.items():
        ds = sorted(rows)
        run = []
        runs = []
        for d in ds:
            if rows[d] == "Error":
                run.append(d)
            else:
                if run:
                    runs.append(run)
                run = []
        if run:
            runs.append(run)
        for r in runs:
            rec = {
                "video_id": vid,
                "first": r[0].isoformat(),
                "last": r[-1].isoformat(),
                "n_recorded_dates": len(r),
                "calendar_span_days": (r[-1] - r[0]).days + 1,
            }
            if r[-1] == ds[-1]:
                rec["right_censored"] = True
                trailing.append(rec)
            else:
                closed.append(rec)

    hist = {}
    for r in closed:
        hist[r["n_recorded_dates"]] = hist.get(r["n_recorded_dates"], 0) + 1
    return {
        "closed_runs": {
            "n": len(closed),
            "length_histogram_recorded_dates": {str(k): hist[k] for k in sorted(hist)},
            "longest": max((r["n_recorded_dates"] for r in closed), default=0),
            "runs": sorted(closed, key=lambda r: (-r["n_recorded_dates"], r["first"])),
        },
        "trailing_runs_right_censored": {
            "n": len(trailing),
            "lengths_recorded_dates": sorted({r["n_recorded_dates"] for r in trailing}),
            "runs": sorted(trailing, key=lambda r: r["first"]),
            "why_separate": (
                "The record ends inside these runs. Their length is a LOWER BOUND on how long the "
                "state lasted, never a duration, and this practice has not observed what happened "
                "after the last recorded date."),
        },
    }


def error_breadth_histogram(index, cutoff):
    """How many dates carry how many simultaneous `Error` rows, before a cutoff date."""
    hist = {}
    dates_by_n = {}
    for e in index:
        if e["date"] >= cutoff:
            continue
        n = e["counts"].get("Error", 0)
        hist[n] = hist.get(n, 0) + 1
        dates_by_n.setdefault(n, []).append(e["date"])
    return {
        "cutoff_exclusive": cutoff,
        "n_dates_considered": sum(hist.values()),
        "n_simultaneous_errors_to_n_dates": {str(k): hist[k] for k in sorted(hist)},
        "dates_with_four_or_more": {
            str(k): dates_by_n[k] for k in sorted(dates_by_n) if k >= 4},
    }


def series_coverage(per_series):
    out = {}
    for vid, rows in per_series.items():
        ds = sorted(rows)
        counts = {}
        for s in rows.values():
            counts[s] = counts.get(s, 0) + 1
        out[vid] = {
            "first_recorded_date": ds[0].isoformat(),
            "last_recorded_date": ds[-1].isoformat(),
            "n_recorded_days": len(ds),
            "state_counts": counts,
        }
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("series", nargs="?", default="receiver-series-2026-08-19.json")
    ap.add_argument("-o", "--out", default="episode-structure-129.json")
    a = ap.parse_args(argv)

    doc = load_series(a.series)
    mapping, per_series = build(doc)
    all_dates, index = date_index(per_series)
    eps = episodes(index)

    result = {
        "schema": "field-research/episode-structure/1",
        "generated_by": "episode_structure.py, session 129, 2026-08-21",
        "input": {
            "series_file": a.series,
            "series_source_file": doc.get("source", {}).get("file")
            if isinstance(doc.get("source"), dict) else doc.get("source"),
            "extractor": doc.get("extractor"),
        },
        "status_mapping_read_from_the_charts_own_axis": {str(k): v for k, v in mapping.items()},
        "series_coverage": series_coverage(per_series),
        "absent_row_control": absent_row_control(all_dates, index, per_series),
        "all_rows_error_episodes": eps,
        "n_episodes": len(eps),
        "error_runs": error_runs(per_series),
        "error_breadth_before_the_final_episode": error_breadth_histogram(
            index, eps[-1]["first_recorded_date"] if eps else "9999-12-31"),
        "date_index": index,
        "what_this_is_not": (
            "A statement about anyone's conduct, or about why any state was written. It is a "
            "description of one saved copy of one public page. This practice has not seen the "
            "code that writes it and does not claim to know what any state means to its authors."),
    }
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    print("record %s .. %s, %d recorded dates, %d dates missing from the span"
          % (result["absent_row_control"]["record_first_date"],
             result["absent_row_control"]["record_last_date"],
             result["absent_row_control"]["recorded_dates"],
             result["absent_row_control"]["n_dates_missing_from_the_whole_record"]))
    print("%d all-rows-Error episodes:" % len(eps))
    for e in eps:
        print("  %s .. %s  (%d recorded dates, %d calendar days, %d series with a row)  %s"
              % (e["first_recorded_date"], e["last_recorded_date"],
                 e["n_recorded_dates_in_episode"], e["calendar_span_days"],
                 e["n_series_with_a_row_on_first_date"],
                 ("cleared to %s" % e["counts_after"]) if e["cleared"]
                 else "NEVER CLEARED - the record ends inside it"))
    print("wrote " + a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
