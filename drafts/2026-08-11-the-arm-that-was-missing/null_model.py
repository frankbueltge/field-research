#!/usr/bin/env python3
"""The public-presence null model: retrievability as a function of video age.

Session 113, 2026-08-12 (evening). Method fixed in PREREGISTRATION-113.md, committed at
a316c86 before this file was written to produce any figure.

WHAT THIS MEASURES, stated in the code because it is the thing most easily lost:
public retrievability of a video identifier, from ONE network vantage, through ONE
endpoint, on ONE day. Session 109's three-arm control with twenty synthetic identifiers
established that this endpoint's HTTP 400 is semantically empty - a video that never
existed returns the same code as a video removed yesterday. NOT-RETRIEVABLE therefore
does not mean deleted, and nothing downstream of this file may say that it does.

Input : ledger/run-2026-08-12T0341Z.json   (session 112, day 2 of the window, 3,869 units)
Output: presence-baseline.json             (every figure this session publishes)

The exclusion rules and the dating rule are power_audit.py's, session 111, reproduced here
against a different run file and a different reference epoch. power_audit.wilson is
imported rather than re-implemented so the intervals are the same function the arc has
been publishing since session 111.
"""

import calendar
import json
import math
import time
import hashlib

import power_audit as pa

RUN = "ledger/run-2026-08-12T0341Z.json"
OUT = "presence-baseline.json"

# Age reference: the start of the day-2 run, fixed in the pre-registration (§2.1).
T_REF = calendar.timegm((2026, 8, 12, 3, 40, 0, 0, 0, 0))
YEAR_S = pa.YEAR_S

# PREREGISTRATION-113 §1.2 read: the manifest's own arms, grouped into strata that are
# clean cuts of source and namespace. Every raw arm is ALSO reported separately below, so
# the grouping hides nothing.
#
# CORRECTED AFTER CHECKING THE CODE THAT ASSIGNED THE LABELS, not after assuming: the
# pre-registration expected `round2` and `round3` to appear as unit labels and planned a
# fourth, namespace-mixed stratum for them. They are not unit labels. The manifest's
# `arms` dict carries six PROVENANCE blocks, but every unit carries one of five labels,
# because expansion-111/build_baseline_manifest{2,3}.py assign
#     "arm": "A2" if r.get("ns") else "A-new"
# - i.e. rounds 2 and 3 were split BY NAMESPACE into the existing arms, not kept as rounds.
# So A-new is article space throughout and A2 is non-article space throughout, the clean
# cut holds, and no mixed stratum exists. The two dead keys are kept below with this note
# rather than deleted, so the divergence from the pre-registration stays legible.
STRATUM = {
    "A": "W-article",       # MediaWiki article space, 21 editions (session 109)
    "A-new": "W-article",   # MediaWiki article space, further editions + rounds 2-3 (ns 0)
    "A2": "W-other-ns",     # MediaWiki non-article namespaces + rounds 2-3 (ns != 0)
    "round2": "W-mixed",    # never appears as a unit label - see note above
    "round3": "W-mixed",    # never appears as a unit label - see note above
    "B": "F-forum",         # technology forum public search API
}
CLEAN_STRATA = ["W-article", "W-other-ns", "F-forum"]

AGE_BANDS = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 99)]


def band_label(lo, hi):
    return f"{lo}-{hi}y" if hi < 99 else f"{lo}y+"


def load():
    d = json.load(open(RUN))
    rows = []
    excluded = {"arm_B_truncated": 0, "indeterminate": 0, "not_19_digit": 0,
                "nonpositive_age": 0}
    for o in d["observations"]:
        arm = o["arm"]
        if arm == "B-truncated":
            excluded["arm_B_truncated"] += 1
            continue
        if o["state"] == "INDETERMINATE":
            excluded["indeterminate"] += 1
            continue
        vid = str(o["vid"])
        if len(vid) != 19:
            excluded["not_19_digit"] += 1
            continue
        created = int(vid) >> 32
        age_s = T_REF - created
        if age_s <= 0:
            excluded["nonpositive_age"] += 1
            continue
        rows.append({
            "vid": vid,
            "arm": arm,
            "stratum": STRATUM[arm],
            "alive": 1 if o["state"] == "RETRIEVABLE" else 0,
            "created": created,
            "year": time.gmtime(created).tm_year,
            "age_y": age_s / YEAR_S,
        })
    return d, rows, excluded


def cell(rows):
    n = len(rows)
    k = sum(r["alive"] for r in rows)
    if n == 0:
        return {"n": 0, "retrievable": 0, "rate": None, "ci": [None, None]}
    lo, hi = pa.wilson(k, n)
    return {"n": n, "retrievable": k, "rate": k / n, "ci": [lo, hi],
            "absent_rate": 1 - k / n, "absent_ci": [1 - hi, 1 - lo]}


def disjoint(a, b):
    """True if two Wilson intervals do not overlap at all."""
    if a["n"] == 0 or b["n"] == 0:
        return False
    return a["ci"][1] < b["ci"][0] or b["ci"][1] < a["ci"][0]


def by_key(rows, keyfn):
    out = {}
    for r in rows:
        out.setdefault(keyfn(r), []).append(r)
    return {k: cell(v) for k, v in sorted(out.items())}


def expected_absence(weights, table):
    """The transfer function, PREREGISTRATION-113 §2.3.

    weights: {band_label: w}, normalised here. table: {band_label: cell}.
    Returns the point estimate and the band implied by the per-cohort Wilson bounds.
    Bands with no data in `table` are reported as uncovered rather than imputed.
    """
    tot = sum(weights.values())
    if tot <= 0:
        return None
    point = lo = hi = 0.0
    uncovered = 0.0
    for b, w in weights.items():
        c = table.get(b)
        if not c or c["n"] == 0 or c["rate"] is None:
            uncovered += w / tot
            continue
        point += (w / tot) * c["absent_rate"]
        lo += (w / tot) * c["absent_ci"][0]
        hi += (w / tot) * c["absent_ci"][1]
    return {"point": point, "lo": lo, "hi": hi, "uncovered_weight": uncovered}


def main():
    d, rows, excluded = load()

    for r in rows:
        for lo, hi in AGE_BANDS:
            if lo <= r["age_y"] < hi:
                r["band"] = band_label(lo, hi)
                break

    pooled = cell(rows)
    by_year = by_key(rows, lambda r: str(r["year"]))
    by_band = by_key(rows, lambda r: r["band"])
    by_stratum = by_key(rows, lambda r: r["stratum"])
    by_arm = by_key(rows, lambda r: r["arm"])

    # per-stratum curves
    strat_year = {}
    strat_band = {}
    for s in sorted({r["stratum"] for r in rows}):
        sub = [r for r in rows if r["stratum"] == s]
        strat_year[s] = by_key(sub, lambda r: str(r["year"]))
        strat_band[s] = by_key(sub, lambda r: r["band"])

    # ---------------------------------------------------------------- criteria
    # K1: any two year cohorts (n >= 30) with disjoint Wilson intervals?
    ys = [y for y, c in by_year.items() if c["n"] >= 30]
    k1_pairs = [[a, b] for i, a in enumerate(ys) for b in ys[i + 1:]
                if disjoint(by_year[a], by_year[b])]
    k1_fires = len(k1_pairs) == 0

    # K2: in cohorts where >= 2 CLEAN strata have n >= 30, are the strata mutually
    # disjoint in a majority of those cohorts?
    k2_rows = []
    for y in sorted(by_year):
        present = [s for s in CLEAN_STRATA
                   if strat_year.get(s, {}).get(y, {"n": 0})["n"] >= 30]
        if len(present) < 2:
            continue
        pairs = [(a, b) for i, a in enumerate(present) for b in present[i + 1:]]
        alld = all(disjoint(strat_year[a][y], strat_year[b][y]) for a, b in pairs)
        anyd = any(disjoint(strat_year[a][y], strat_year[b][y]) for a, b in pairs)
        k2_rows.append({"year": y, "strata": present,
                        "all_disjoint": alld, "any_disjoint": anyd})
    k2_fires = bool(k2_rows) and sum(r["all_disjoint"] for r in k2_rows) > len(k2_rows) / 2

    # K3: pooled absence rate in the youngest band (< 1 year) above 12.5 %?
    young = by_band.get("0-1y", {"n": 0, "absent_rate": None})
    k3_fires = bool(young["n"]) and young["absent_rate"] > 0.125

    # ------------------------------------------------------------- predictions
    # P4: a corpus entirely under one year old, under every clean stratum.
    p4 = {}
    for s in CLEAN_STRATA:
        p4[s] = expected_absence({"0-1y": 1.0}, strat_band[s])
    p4["pooled"] = expected_absence({"0-1y": 1.0}, by_band)

    # P5: a corpus whose mass sits in the >= 3y bands, weighted as our own population is.
    old_bands = ["3-4y", "4-5y", "5y+"]
    w_old = {b: by_band[b]["n"] for b in old_bands if b in by_band}
    p5 = {s: expected_absence(w_old, strat_band[s]) for s in CLEAN_STRATA}
    p5["pooled"] = expected_absence(w_old, by_band)
    mean_age_old = (sum(r["age_y"] for r in rows if r["band"] in old_bands)
                    / max(1, sum(1 for r in rows if r["band"] in old_bands)))

    # P2: monotonicity across year cohorts with n >= 30 (older year = lower rate).
    ordered = sorted(ys)                       # ascending calendar year = descending age
    inversions = [[ordered[i], ordered[i + 1]]
                  for i in range(len(ordered) - 1)
                  if by_year[ordered[i]]["rate"] > by_year[ordered[i + 1]]["rate"]]
    # an inversion of the age-monotone claim is a LATER year with a LOWER rate
    age_inversions = [[ordered[i], ordered[i + 1]]
                      for i in range(len(ordered) - 1)
                      if by_year[ordered[i + 1]]["rate"] < by_year[ordered[i]]["rate"]]

    out = {
        "schema": "field-research/public-presence-null/1",
        "written_by": "session 113, 2026-08-12",
        "preregistration": "PREREGISTRATION-113.md @ a316c86",
        "what_this_measures": (
            "public retrievability of a video identifier from one network vantage, "
            "through one endpoint (oembed), on one day. The endpoint's HTTP 400 is "
            "semantically empty (session 109, three-arm control with 20 synthetic "
            "identifiers): a video that never existed returns the same code as a video "
            "removed yesterday. NOT-RETRIEVABLE DOES NOT MEAN DELETED."
        ),
        "source_run": {
            "file": RUN,
            "run_id": d["run_id"],
            "run_utc_start": d["run_utc_start"],
            "run_utc_end": d["run_utc_end"],
            "vantage_asn": d["vantage"]["asn"],
            "vantage_country": d["vantage"]["country"],
            "planned": d["planned"], "requested": d["requested"],
        },
        "t_ref_utc": "2026-08-12T03:40:00Z",
        "population": {"analysable": len(rows), "excluded": excluded},
        "pooled": pooled,
        "by_year": by_year,
        "by_age_band": by_band,
        "by_stratum": by_stratum,
        "by_raw_arm": by_arm,
        "by_stratum_year": strat_year,
        "by_stratum_band": strat_band,
        "criteria": {
            "K1_curve_flat": {"fires": k1_fires, "cohorts_n_ge_30": ys,
                              "disjoint_pairs": k1_pairs},
            "K2_arms_untransferable": {"fires": k2_fires, "rows": k2_rows},
            "K3_null_swallows_claim": {"fires": k3_fires,
                                       "youngest_band": "0-1y",
                                       "cell": young},
        },
        "predictions": {
            "P1_pooled_rate_85_92": {"rate": pooled["rate"],
                                     "holds": 0.85 <= pooled["rate"] <= 0.92},
            "P2_monotone_at_most_one_inversion": {
                "cohorts": ordered,
                "rates": [by_year[y]["rate"] for y in ordered],
                "inversions": age_inversions,
                "holds": len(age_inversions) <= 1},
            "P4_young_corpus_below_12.5pct": {
                "by_spec": p4,
                "holds": all(v is not None and v["point"] < 0.125 for v in p4.values())},
            "P5_old_corpus_above_12.5pct": {
                "mean_age_y": mean_age_old,
                "weights": w_old,
                "by_spec": p5,
                "holds": any(v is not None and v["point"] > 0.125
                             for v in p5.values())},
        },
        "transfer_function": {
            "formula": "expected_absence(w) = sum_i w_i * (1 - p_i)",
            "note": ("w is the READER'S OWN age histogram over the bands below, "
                     "normalised to 1. p_i is this run's per-band public-presence rate. "
                     "The interval comes from the per-band Wilson bounds. This practice "
                     "does not supply w for anyone else's corpus."),
            "bands": list(by_band.keys()),
        },
    }

    json.dump(out, open(OUT, "w"), indent=1)
    src = open(__file__, "rb").read()
    print(f"script sha256 {hashlib.sha256(src).hexdigest()[:16]}")
    print(f"analysable {len(rows)}  excluded {excluded}")
    print(f"pooled {pooled['retrievable']}/{pooled['n']} = {pooled['rate']:.4f} "
          f"CI [{pooled['ci'][0]:.4f}, {pooled['ci'][1]:.4f}]")
    print("\nby age band:")
    for b in [band_label(*x) for x in AGE_BANDS]:
        c = by_band.get(b)
        if not c:
            continue
        print(f"  {b:>5}  n={c['n']:>4}  present={c['rate']:.4f} "
              f"[{c['ci'][0]:.4f},{c['ci'][1]:.4f}]  absent={c['absent_rate']:.4f}")
    print("\nby year cohort:")
    for y in sorted(by_year):
        c = by_year[y]
        print(f"  {y}  n={c['n']:>4}  present={c['rate']:.4f} "
              f"[{c['ci'][0]:.4f},{c['ci'][1]:.4f}]")
    print("\nby stratum:")
    for s in sorted(by_stratum):
        c = by_stratum[s]
        print(f"  {s:>12}  n={c['n']:>4}  present={c['rate']:.4f} "
              f"[{c['ci'][0]:.4f},{c['ci'][1]:.4f}]")
    print("\nby raw arm:")
    for a in sorted(by_arm):
        c = by_arm[a]
        print(f"  {a:>8}  n={c['n']:>4}  present={c['rate']:.4f} "
              f"[{c['ci'][0]:.4f},{c['ci'][1]:.4f}]")
    print(f"\nK1 curve flat        fires={k1_fires}  ({len(k1_pairs)} disjoint pairs)")
    print(f"K2 arms untransfer.  fires={k2_fires}  rows={len(k2_rows)}")
    print(f"K3 null swallows     fires={k3_fires}  youngest band absent="
          f"{young.get('absent_rate')}")
    print("\nP1", out["predictions"]["P1_pooled_rate_85_92"]["holds"])
    print("P2", out["predictions"]["P2_monotone_at_most_one_inversion"]["holds"],
          "inversions", age_inversions)
    print("P4", out["predictions"]["P4_young_corpus_below_12.5pct"]["holds"],
          {k: (None if v is None else round(v["point"], 4)) for k, v in p4.items()})
    print("P5", out["predictions"]["P5_old_corpus_above_12.5pct"]["holds"],
          f"mean_age={mean_age_old:.2f}",
          {k: (None if v is None else round(v["point"], 4)) for k, v in p5.items()})


if __name__ == "__main__":
    main()
