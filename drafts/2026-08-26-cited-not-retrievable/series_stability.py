#!/usr/bin/env python3
"""series_stability - is the encyclopedia's absent share a stock or a flow?

Session 136, 2026-08-26. The temporal limb of the increment, computed OFFLINE from the completed
run files already committed in this repository (`PREREGISTRATION-136.md` K-B).

WHAT IT ANSWERS
    Across every completed measurement day of the instrument, restricted to the encyclopedia arms
    (A, A-new, A2): what share of identifiers is NOT-RETRIEVABLE, and how many identifiers change
    state from one measurement day to the next?

A DEFECT THIS FILE EXISTS TO NOT REPEAT. The first version of this computation, written at the
shell, globbed `run-*T0341Z.json` and so silently dropped five measurement days - the founding
census at 1124Z and the four days the series ran at 0427Z, 0343Z and 0337Z before the hour settled.
It reported eight days as if they were the series. Nothing was published from it. This script
therefore enumerates run files by pattern `run-<DATE>T<TIME>Z.json` with NO hour filter, prints the
hour of each day it uses, and prints the count so a reader can check it against the record's own
"13 measurement days".

WHAT IS EXCLUDED, AND WHY
    *.partial                   a partial is never a run (the instrument's own rule)
    *-second-probe.json         a deliberate same-day replicate, not a measurement day
                                (`DOUBLE-PROBE-122.md`, `DOUBLE-PROBE-131-132.md`)

WHAT A "CHANGE" HERE IS, AND WHAT IT IS NOT
    A change is counted only between two determinate readings of the same identifier on
    consecutive measurement days. Readings touching INDETERMINATE are excluded from the change
    count and reported separately. THESE ARE RAW APPARENT CHANGES. They are NOT the instrument's
    confirmed transitions: the confirmation step re-requests each apparent change five times before
    believing it, and it has refuted six of sixteen apparent disappearances across the series
    (`../2026-08-11-the-arm-that-was-missing/confirmation-record-121.json`). Nothing in this file
    may be read as a transition count, and nothing here scores a test or claims a trend -
    `CONDITIONS-132.md` item 5 binds this computation as it binds the day records.

    The intervals between these days are ALSO not equal - the series has two holes and ran at four
    different hours before settling. A gap column is printed for every pair so no reader can take
    the rows for a daily sequence.

Usage:  python3 series_stability.py [-o out.json]
Offline. Reads committed files only, makes no request.
"""
import argparse
import calendar
import collections
import glob
import hashlib
import json
import os
import re
import time

ARC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "2026-08-11-the-arm-that-was-missing")
WIKI_ARMS = ("A", "A-new", "A2")
RUN_RE = re.compile(r"run-(\d{4}-\d{2}-\d{2})T(\d{4})Z\.json$")


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def measurement_days():
    days = []
    for p in sorted(glob.glob(os.path.join(ARC, "ledger", "run-*.json"))):
        m = RUN_RE.search(os.path.basename(p))
        if not m:
            continue                      # -second-probe and anything else non-canonical
        days.append((m.group(1), m.group(2), p))
    return days


def build():
    days = measurement_days()
    rows, prev, prev_date = [], None, None
    for (date, hhmm, path) in days:
        run = json.load(open(path))
        st = {o["vid"]: o["state"] for o in run["observations"]
              if o.get("arm") in WIKI_ARMS}
        ret = sum(1 for v in st.values() if v == "RETRIEVABLE")
        nor = sum(1 for v in st.values() if v == "NOT-RETRIEVABLE")
        det = ret + nor
        row = {
            "date": date, "hour_utc": hhmm[:2] + ":" + hhmm[2:],
            "run_file": os.path.basename(path), "run_file_sha256": sha256(path),
            "n_identifiers": len(st),
            "RETRIEVABLE": ret, "NOT-RETRIEVABLE": nor,
            "INDETERMINATE": len(st) - det, "determinate": det,
            "absent_share": nor / det if det else None,
        }
        if prev is not None:
            common = set(st) & set(prev)
            det_both = [v for v in common
                        if st[v] != "INDETERMINATE" and prev[v] != "INDETERMINATE"]
            changed = [v for v in det_both if st[v] != prev[v]]
            gap = (calendar.timegm(time.strptime(date, "%Y-%m-%d"))
                   - calendar.timegm(time.strptime(prev_date, "%Y-%m-%d"))) / 86400.0
            row["vs_previous_measurement_day"] = {
                "previous": prev_date,
                "calendar_days_between": gap,
                "identifiers_determinate_in_both": len(det_both),
                "apparent_changes_raw": len(changed),
                "apparent_change_share": len(changed) / len(det_both) if det_both else None,
                "to_NOT-RETRIEVABLE": sum(1 for v in changed if st[v] == "NOT-RETRIEVABLE"),
                "to_RETRIEVABLE": sum(1 for v in changed if st[v] == "RETRIEVABLE"),
                "identifiers_touching_INDETERMINATE": len(common) - len(det_both),
            }
        rows.append(row)
        prev, prev_date = st, date

    shares = [r["absent_share"] for r in rows if r["absent_share"] is not None]
    changes = [r["vs_previous_measurement_day"]["apparent_changes_raw"]
               for r in rows if "vs_previous_measurement_day" in r]

    # THE FIRST DAY IS NOT ON THE SAME CORPUS AND MUST NOT BE RANGED WITH THE REST. The founding
    # census of 2026-08-11 ran before the corpus expansion; `manifest-day2-onward.json` superseded
    # it that night ("every run from 2026-08-12 onward must use this manifest"). Ranging its share
    # against the others would report a corpus change as a movement in the field. The modal
    # identifier count is computed rather than typed, and the days outside it are named.
    modal_n = collections.Counter(r["n_identifiers"] for r in rows).most_common(1)[0][0]
    fixed = [r for r in rows if r["n_identifiers"] == modal_n]
    off = [{"date": r["date"], "n_identifiers": r["n_identifiers"]}
           for r in rows if r["n_identifiers"] != modal_n]
    fshares = [r["absent_share"] for r in fixed]

    return {
        "schema": "field-research/series-stability/1",
        "built_by": "series_stability.py, session 136, 2026-08-26",
        "offline": True,
        "arms_included": list(WIKI_ARMS),
        "n_measurement_days": len(rows),
        "hours_used": sorted({r["hour_utc"] for r in rows}),
        "holes_note": "2026-08-17 and 2026-08-24 have a .partial and no run file. A partial is "
                      "never a run; they are holes and consume no ordinal.",
        "all_days": {
            "absent_share_min": min(shares), "absent_share_max": max(shares),
            "absent_share_range_pp": (max(shares) - min(shares)) * 100,
        },
        "fixed_manifest_days_only": {
            "modal_n_identifiers": modal_n,
            "n_days": len(fixed),
            "days_excluded": off,
            "why_excluded": "a different corpus, not a different field: the founding census ran "
                            "before the expansion of 2026-08-11 and manifest-day2-onward.json "
                            "superseded it the same night",
            "absent_share_min": min(fshares), "absent_share_max": max(fshares),
            "absent_share_range_pp": (max(fshares) - min(fshares)) * 100,
        },
        "apparent_changes_raw_per_interval": changes,
        "apparent_changes_raw_total": sum(changes),
        "not_a_transition_count": "These are RAW apparent changes between consecutive measurement "
                                  "days. The instrument's confirmation step re-requests each five "
                                  "times before believing it. Across the ENCYCLOPEDIA ARMS ONLY - "
                                  "the arms this file counts - it has refuted 5 of 15 RAW apparent "
                                  "disappearances, identically for GENUINE transitions "
                                  "(confirmation-by-arm-136.json). The whole-series figure of 6 of "
                                  "16 includes a public forum's arm that this file excludes. No "
                                  "trend is claimed and no test is scored on these numbers.",
        "days": rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    out = build()
    text = json.dumps(out, indent=1, ensure_ascii=False)
    if a.out:
        open(a.out, "w").write(text + "\n")
        print("wrote %s" % a.out)
    print("%d measurement days, hours used: %s"
          % (out["n_measurement_days"], ", ".join(out["hours_used"])))
    print("%-11s %-6s %6s %6s %6s %8s  %s"
          % ("date", "hour", "det", "absent", "ind", "absent%", "raw changes vs prev (gap d)"))
    for r in out["days"]:
        v = r.get("vs_previous_measurement_day")
        tail = ("  %3d  (%.0f d, to-absent %d / to-present %d)"
                % (v["apparent_changes_raw"], v["calendar_days_between"],
                   v["to_NOT-RETRIEVABLE"], v["to_RETRIEVABLE"])) if v else "   -"
        print("%-11s %-6s %6d %6d %6d %7.2f%%%s"
              % (r["date"], r["hour_utc"], r["determinate"], r["NOT-RETRIEVABLE"],
                 r["INDETERMINATE"], 100 * r["absent_share"], tail))
    a, f = out["all_days"], out["fixed_manifest_days_only"]
    print("absent share, all %d days:            %.2f%% - %.2f%%  (range %.2f pp)"
          % (out["n_measurement_days"], 100 * a["absent_share_min"],
             100 * a["absent_share_max"], a["absent_share_range_pp"]))
    print("absent share, %d days on one corpus:  %.2f%% - %.2f%%  (range %.2f pp)   excluded: %s"
          % (f["n_days"], 100 * f["absent_share_min"], 100 * f["absent_share_max"],
             f["absent_share_range_pp"],
             ", ".join(d["date"] for d in f["days_excluded"]) or "none"))
    print("raw apparent changes, %d intervals: %s  total %d"
          % (len(out["apparent_changes_raw_per_interval"]),
             out["apparent_changes_raw_per_interval"], out["apparent_changes_raw_total"]))


if __name__ == "__main__":
    main()
