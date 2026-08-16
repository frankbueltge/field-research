#!/usr/bin/env python3
"""The frozen-reference drift, measured rather than described (session 122, 2026-08-16).

Conditions V1 and V2 of the session-120 gauntlet, carried unrepaired across two sessions and
made binding on this one by `CONDITIONS-121.md`. The reviewer's own words for it: it is the
defect that would *"quietly move somebody else's number"*.

THE DEFECT HAS TWO HALVES AND THEY ARE NOT THE SAME KIND OF THING.

**Half one — bookkeeping (V1).** `build_deliverable.py` line 179 computes every unit's age once,
against `days[0]["utc_start"]` — the *first* day of the panel, 2026-08-11T11:24:06Z — and line 364
then declares the reference table's `t_ref_utc` to be `newest["utc_start"]`, 2026-08-14T03:43:47Z.
The band a unit sits in is therefore its band on one date while the table says it is its band on
another, **2.6803 days** later — computed by this script, not carried over from the errata, which
say "three days apart". The field carrying the ages is honestly named `age_y_at_baseline`; the
table that ships as the yardstick is not.

**Half two — design.** `presence_check.py` ages a caller's list at the moment the caller runs it
(`t_ref = now`, line 513) and then looks those ages up in a table whose bands were fixed on a day
in the past. Nothing re-measures. So the older the tool gets on a shelf, the further the
expectation it prints moves away from anything that was ever observed — while every number in the
output keeps the same names and the same number of decimal places. v0.2.1 discloses the age of the
reference table (`baseline_currency`). Disclosure is not a size. This script measures the size.

Nothing here changes any archived run file, and nothing here edits the reviewed bundle. It writes
one JSON of measurements; what the session does with them is a separate, dated act.

Usage:  python3 drift_122.py [--out drift-122.json]
"""
import argparse
import calendar
import json
import os
import time

import power_audit as pa

YEAR_S = 365.25 * 86400.0
BASELINE = "ledger/baseline-union.json"
CORRECTIONS = "ledger/corrections.json"
AGE_BANDS = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 99)]
STRATUM = {"A": "W-article", "A-new": "W-article", "A2": "W-other-ns", "B": "F-forum"}

# Horizons, in days after the reference table's own declared time, at which the caller-side
# drift is evaluated. Chosen before any number was computed: one day, one week, the age the
# table already had when the bundle was assembled, a month, a quarter, half a year, a year.
HORIZONS = [0, 1, 7, 30, 90, 180, 365, 730]


def band_label(lo, hi):
    return f"{lo}-{hi}y" if hi < 99 else f"{lo}y+"


def band_of(age_y):
    if age_y is None:
        return None
    for lo, hi in AGE_BANDS:
        if lo <= age_y < hi:
            return band_label(lo, hi)
    return None


def cell(n, absent):
    if n == 0:
        return {"n": 0, "absent": 0, "absent_rate": None, "absent_ci": [None, None]}
    lo, hi = pa.wilson(absent, n)
    return {"n": n, "absent": absent, "absent_rate": absent / n, "absent_ci": [lo, hi]}


def t(s):
    return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))


def discover_runs():
    out = []
    for name in sorted(os.listdir("ledger")):
        if not name.startswith("run-") or not name.endswith(".json"):
            continue
        p = os.path.join("ledger", name)
        d = json.load(open(p))
        if d.get("partial") or d.get("schema", "").endswith("/partial"):
            continue
        out.append((p, d))
    out.sort(key=lambda x: x[1]["run_utc_start"])
    return out


def load_days(cutoff):
    """The panel exactly as `build_deliverable.py` assembles it, to the same stated cut-off.

    The cut-off matters: the bundle under review was frozen at the last complete run through
    2026-08-14, and a drift measured against a panel this session has since extended would not
    be a measurement of the shipped artifact. It is passed in, never discovered.
    """
    base = json.load(open(BASELINE))
    days = [{"label": "baseline", "file": BASELINE, "utc_start": base["run_utc_start"],
             "obs": base["observations"]}]
    for p, d in discover_runs():
        if d["run_utc_start"] <= base["run_utc_start"]:
            continue
        if d["run_utc_start"] > cutoff:
            continue
        days.append({"label": d["run_utc_start"][:10], "file": p,
                     "utc_start": d["run_utc_start"], "obs": d["observations"]})
    return days


def build_units(days):
    """Units with their raw and overlay-corrected state per day — `build_deliverable.py` §series."""
    corr = json.load(open(CORRECTIONS)) if os.path.exists(CORRECTIONS) else {"corrections": []}
    overlay = {(c["run_file"], str(c["vid"])): c for c in corr["corrections"]}
    units = {}
    for day in days:
        for o in day["obs"]:
            vid = str(o["vid"])
            u = units.setdefault(vid, {"vid": vid, "arm": o["arm"], "states": {},
                                       "states_corrected": {}})
            u["states"][day["label"]] = o["state"]
            c = overlay.get((day["file"], vid))
            if c and o["state"] == c["state_in_run_file"]:
                u["states_corrected"][day["label"]] = c["corrected_state"]
            else:
                u["states_corrected"][day["label"]] = o["state"]
    for u in units.values():
        u["stratum"] = STRATUM.get(u["arm"], u["arm"])
        u["created"] = (int(u["vid"]) >> 32) if len(u["vid"]) == 19 else None
    return units


def table_at(units, day, t_ref, state_key="states"):
    """The `by_age_band` table of one day's observations, with ages taken at `t_ref`.

    Every exclusion rule is `build_deliverable.py`'s, unchanged: arm B-truncated out, an
    INDETERMINATE reading out, an undatable identifier out of the age table only.
    """
    rows = []
    for o in day["obs"]:
        u = units[str(o["vid"])]
        state = u[state_key].get(day["label"])
        if o["arm"] == "B-truncated" or state == "INDETERMINATE":
            continue
        age = None
        if u["created"] is not None:
            a = (t_ref - u["created"]) / YEAR_S
            age = a if a > 0 else None
        rows.append({"absent": 1 if state == "NOT-RETRIEVABLE" else 0, "band": band_of(age)})
    buckets = {}
    for r in rows:
        if r["band"] is None:
            continue
        buckets.setdefault(r["band"], []).append(r)
    return ({b: cell(len(v), sum(x["absent"] for x in v)) for b, v in sorted(buckets.items())},
            cell(len(rows), sum(r["absent"] for r in rows)))


def expectation_from(hist, table):
    """`presence_check.expectation`, isolated: the age histogram weighted through the table."""
    tot = sum(hist.values())
    if not tot:
        return None
    point = lo = hi = 0.0
    covered = 0
    for b, w in hist.items():
        c = table.get(b)
        if not c or not c["n"]:
            continue
        covered += w
        point += (w / tot) * c["absent_rate"]
        lo += (w / tot) * c["absent_ci"][0]
        hi += (w / tot) * c["absent_ci"][1]
    return {"expected_absent_rate": point, "expected_lo": lo, "expected_hi": hi,
            "n_dated": tot, "n_weighted_into_a_populated_cell": covered}


def read_list(path):
    """The identifiers of a caller's list file, by `presence_check.parse_line`'s modern-scheme
    rule only — this script measures ages, it does not measure anything over the network."""
    import re
    out = []
    for raw in open(path, encoding="utf-8"):
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        m = re.search(r"/video/(\d+)", s) or re.search(r"(\d{1,25})", s)
        if m:
            out.append(m.group(1))
    return out


def hist_at(vids, t_ref):
    h = {}
    for v in vids:
        if len(v) != 19:
            continue
        a = (t_ref - (int(v) >> 32)) / YEAR_S
        b = band_of(a if a > 0 else None)
        if b:
            h[b] = h.get(b, 0) + 1
    return h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="drift-122.json")
    ap.add_argument("--cutoff", default="2026-08-14T23:59:59Z",
                    help="the bundle's own stated freeze; the panel is read to here and no further")
    a = ap.parse_args()

    days = load_days(a.cutoff)
    units = build_units(days)
    newest = days[-1]
    t_frozen = t(days[0]["utc_start"])      # what the shipped ages were actually computed against
    t_declared = t(newest["utc_start"])     # what the shipped table says they were computed against

    shipped = json.load(open("deliverable/reference-baseline.json"))

    # ---- half one: the bookkeeping error, cell by cell --------------------------------------
    tbl_frozen, pooled_frozen = table_at(units, newest, t_frozen)
    tbl_true, pooled_true = table_at(units, newest, t_declared)

    # Reproduce the shipped file first. A correction nobody can tie to the artifact it corrects
    # is a claim, not a repair.
    reproduces = all(
        shipped["by_age_band"].get(b, {}).get("n") == c["n"]
        and shipped["by_age_band"].get(b, {}).get("absent") == c["absent"]
        for b, c in tbl_frozen.items()) and set(shipped["by_age_band"]) == set(tbl_frozen)

    moved = []
    for b in sorted(set(tbl_frozen) | set(tbl_true)):
        f, tt = tbl_frozen.get(b), tbl_true.get(b)
        if not f or not tt or (f["n"], f["absent"]) != (tt["n"], tt["absent"]):
            moved.append({"band": b,
                          "as_shipped": f, "at_the_declared_reference_time": tt,
                          "delta_n": (tt or {}).get("n", 0) - (f or {}).get("n", 0),
                          "delta_absent": (tt or {}).get("absent", 0) - (f or {}).get("absent", 0),
                          "delta_rate": (None if not f or not tt or f["absent_rate"] is None
                                         or tt["absent_rate"] is None
                                         else tt["absent_rate"] - f["absent_rate"])})

    # How many individual units change band over those 3.01 days, and in which direction.
    crossers = []
    for o in newest["obs"]:
        u = units[str(o["vid"])]
        if u["created"] is None:
            continue
        af = (t_frozen - u["created"]) / YEAR_S
        at = (t_declared - u["created"]) / YEAR_S
        bf, bt = band_of(af if af > 0 else None), band_of(at if at > 0 else None)
        if bf != bt:
            crossers.append({"vid": u["vid"], "from": bf, "to": bt,
                             "age_y_as_shipped": round(af, 5),
                             "age_y_at_declared": round(at, 5)})

    # ---- half two: the caller-side drift ----------------------------------------------------
    # The table stays exactly as it is. Only the clock the CALLER's list is aged at moves — which
    # is precisely what the tool does when it is run months after the table was built.
    lists = {}
    for name, path in (("receiver_eleven", "receiver-list.txt"),):
        vids = read_list(path)
        rows = []
        for dd in HORIZONS:
            h = hist_at(vids, t_declared + dd * 86400)
            e = expectation_from(h, tbl_true)
            rows.append({"days_after_t_ref": dd, "age_histogram": h,
                         "expected_absent_rate": None if not e else e["expected_absent_rate"],
                         "expected_lo": None if not e else e["expected_lo"],
                         "expected_hi": None if not e else e["expected_hi"]})
        base_rate = rows[0]["expected_absent_rate"]
        for r in rows:
            r["drift_pp_from_day0"] = (None if r["expected_absent_rate"] is None or base_rate is None
                                       else 100 * (r["expected_absent_rate"] - base_rate))
        lists[name] = {"source_file": path, "n_lines_with_an_identifier": len(vids),
                       "n_datable_19_digit": sum(1 for v in vids if len(v) == 19),
                       "horizons": rows}

    # The same drift for the reference population itself, as the largest list on disk. It is
    # the population the table was fitted on, so this is the drift of the yardstick against
    # itself — the cleanest possible statement of the design defect, with no second population
    # in the way.
    panel_vids = [u["vid"] for u in units.values() if u["created"] is not None]
    rows = []
    for dd in HORIZONS:
        h = hist_at(panel_vids, t_declared + dd * 86400)
        e = expectation_from(h, tbl_true)
        rows.append({"days_after_t_ref": dd, "age_histogram": h,
                     "expected_absent_rate": e["expected_absent_rate"],
                     "expected_lo": e["expected_lo"], "expected_hi": e["expected_hi"]})
    b0 = rows[0]["expected_absent_rate"]
    for r in rows:
        r["drift_pp_from_day0"] = 100 * (r["expected_absent_rate"] - b0)
    lists["reference_population_itself"] = {
        "source_file": "the panel of this arc's own window, from the run files",
        "n_lines_with_an_identifier": len(panel_vids),
        "n_datable_19_digit": len(panel_vids), "horizons": rows}

    # Is the drift monotone? The table's own rates are not: the 3-4y cell sits fractionally
    # ABOVE the 4-5y cell, so a list crossing four years old can move the expectation DOWN.
    ordered = [band_label(*b) for b in AGE_BANDS]
    rates = [(b, tbl_true[b]["absent_rate"]) for b in ordered if b in tbl_true]
    inversions = [{"from": rates[i][0], "to": rates[i + 1][0],
                   "rate_from": rates[i][1], "rate_to": rates[i + 1][1]}
                  for i in range(len(rates) - 1) if rates[i + 1][1] < rates[i][1]]

    # ---- the one number that compares the two halves ----------------------------------------
    # The bookkeeping half is a fixed, one-off displacement: it is as large as it will ever be
    # the moment the file is written. The design half starts at zero and grows every day the
    # tool is not rebuilt. So the honest comparison is not "which is bigger" — at a horizon of a
    # year the answer is arithmetic — but WHEN the growing one overtakes the fixed one. Measured
    # by stepping one day at a time, on the reference population itself.
    worst_bookkeeping_pp = max(
        (abs(100 * m["delta_rate"]) for m in moved if m.get("delta_rate") is not None),
        default=0.0)
    crossover = None
    for dd in range(0, 1096):
        h = hist_at(panel_vids, t_declared + dd * 86400)
        e = expectation_from(h, tbl_true)
        if 100 * abs(e["expected_absent_rate"] - b0) > worst_bookkeeping_pp:
            crossover = {"days": dd,
                         "drift_pp": 100 * (e["expected_absent_rate"] - b0),
                         "worst_bookkeeping_pp": worst_bookkeeping_pp}
            break

    out = {
        "schema": "field-research/frozen-reference-drift/1",
        "written_by": "drift_122.py, session 122, 2026-08-16",
        "what_this_is": ("a measurement of the two halves of the frozen-reference defect (V1, V2 "
                         "of the session-120 gauntlet). Nothing here is a repair; a repair is a "
                         "separate dated act. No archived run file is read for anything but its "
                         "recorded observations, and none is written."),
        "panel_cutoff": a.cutoff,
        "days_in_panel": [d["label"] for d in days],
        "reference_times": {
            "ages_were_actually_computed_against": days[0]["utc_start"],
            "table_declares": newest["utc_start"],
            "gap_days": round((t_declared - t_frozen) / 86400.0, 4),
            "source_of_the_error": ("build_deliverable.py line 179 uses days[0] for the ages and "
                                    "line 364 uses the newest day for t_ref_utc"),
        },
        "shipped_table_reproduced_from_the_run_files": reproduces,
        "half_one_bookkeeping": {
            "pooled_as_shipped": pooled_frozen,
            "pooled_at_the_declared_reference_time": pooled_true,
            "bands_that_move": moved,
            "n_units_changing_band": len(crossers),
            "units_changing_band": crossers,
        },
        "half_two_caller_side_drift": {
            "how_it_was_measured": ("the reference table is held fixed at the corrected ages; only "
                                    "the clock at which a caller's list is aged advances, which is "
                                    "exactly what presence_check.py does when it is run later"),
            "horizons_days": HORIZONS,
            "lists": lists,
            "band_rate_inversions_in_the_table": inversions,
            "when_the_design_half_overtakes_the_bookkeeping_half": crossover,
        },
        "what_this_measurement_does_not_reach": [
            ("the baseline union is itself 11 h 41 m wide (2026-08-11T11:24:06Z to 23:05:18Z, four "
             "component runs), so 'the ages were computed at days[0]' is already an approximation "
             "of a moving reference, and this script inherits that approximation rather than "
             "removing it"),
            ("within any one run the units are probed over roughly 1.9 hours, so a unit's true age "
             "at ITS OWN measurement differs from its age at the run's start by up to that much; "
             "the effect is confined to units within 1.9 h of a band boundary and is not corrected "
             "here"),
            ("the caller-side drift is arithmetic on a fixed table, NOT a forecast of retrievability. "
             "It says how far the printed expectation moves from what was measured, and says "
             "nothing about whether the world moved the same way — the reference population has "
             "not been re-measured at any of these horizons and this arc cannot say what it would "
             "show"),
            ("the horizons beyond 7 days are counterfactual by construction: this arc is 5 days "
             "into its window, and every figure past that is what the tool WOULD print, not what "
             "anything was observed to be"),
        ],
    }
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps({"reproduces_shipped_table": reproduces,
                      "gap_days": out["reference_times"]["gap_days"],
                      "bands_that_move": len(moved),
                      "units_changing_band": len(crossers),
                      "panel_drift_365d_pp": round(
                          lists["reference_population_itself"]["horizons"][-2]["drift_pp_from_day0"], 4),
                      "inversions": len(inversions)}, indent=1))


if __name__ == "__main__":
    main()
