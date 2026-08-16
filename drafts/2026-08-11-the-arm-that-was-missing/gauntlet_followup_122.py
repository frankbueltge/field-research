#!/usr/bin/env python3
"""Every figure this session published in answer to its own gauntlet, computed to a file.

Session 122, 2026-08-16, written after `VERIFIER-122.md` and `INTERLOCUTOR-14.md`.

It exists because of the session's own erratum E1 and the rule that follows it: a number in prose
that lives only in a shell one-liner is a number that cannot be re-checked, and this arc has now
published three of those. `ERRATA-122.md` and `CONDITIONS-122.md` quote the crossover family, the
across-day stability movement, the receiver-eleven drift at the withdrawn threshold, and the
adversary's mixed-list reproduction. Until this script, none of them had a machine source.

    python3 gauntlet_followup_122.py [--out gauntlet-followup-122.json]

Nothing here re-measures anything: it is arithmetic over run files already on disk and over the
two `expectation.json` variants. No request leaves the machine.
"""
import argparse
import calendar
import json
import re
import sys
import time

import drift_122 as D

sys.path.insert(0, "deliverable/tools")
import presence_check as P  # noqa: E402

CORRECTED = "deliverable/reference-baseline-CORRECTED-2026-08-16.json"


def crossover_family(units, days, newest):
    """Interlocutor 14 finding 4. The crossover is not one number; it is a family, and which
    member you get depends entirely on how the bookkeeping half's effect is measured. v0.3.0
    hard-coded the most forgiving member and called the threshold measured."""
    tf, td = D.t(days[0]["utc_start"]), D.t(newest["utc_start"])
    tbl_f, _ = D.table_at(units, newest, tf)
    tbl_t, _ = D.table_at(units, newest, td)
    panel = [u["vid"] for u in units.values() if u["created"] is not None]

    def E(t, tbl):
        return D.expectation_from(D.hist_at(panel, t), tbl)["expected_absent_rate"]

    deltas = [abs(tbl_t[b]["absent_rate"] - tbl_f[b]["absent_rate"]) * 100 for b in tbl_f]
    comparands = {
        "worst_single_band_rate_cell": max(deltas),
        "mean_band_rate_cell": sum(deltas) / len(deltas),
        "effect_on_the_printed_expectation": abs(100 * (E(td, tbl_t) - E(tf, tbl_f))),
        "effect_on_the_pooled_rate": 0.0,
    }
    b0 = E(td, tbl_t)
    out = {}
    for name, th in comparands.items():
        row = {"comparand_pp": th, "crossover_days": None, "drift_at_crossover_pp": None}
        for dd in range(0, 1200):
            drift = 100 * abs(E(td + dd * 86400, tbl_t) - b0)
            if drift > th:
                row["crossover_days"] = dd
                row["drift_at_crossover_pp"] = drift
                break
        out[name] = row
    out["_which_one_is_like_for_like"] = (
        "effect_on_the_printed_expectation. The drift is measured ON the printed expectation, so "
        "the bookkeeping half's effect on that same quantity is what it must be weighed against. "
        "It is the strictest member and v0.3.1 uses it, having withdrawn the claim that the "
        "26-day figure was 'measured rather than picked'.")
    return out


def across_day_stability():
    """Interlocutor 14 finding 7. The column DRIFT-122.md §2 omitted and §6 declined to analyse."""
    old = json.load(open("deliverable/expectation.json"))
    new = json.load(open("deliverable/expectation-CORRECTED-2026-08-16.json"))
    rows = {}
    for k, a in old["across_day_stability"].items():
        b = new["across_day_stability"][k]
        ra, rb = 100 * a["range"], 100 * b["range"]
        rows[k] = {"range_pp_as_shipped": ra, "range_pp_corrected": rb,
                   "change_pct": None if ra == 0 else (rb - ra) / ra * 100}
    # The mechanism, rather than the movement: under per-day banding the cells are no longer the
    # same set of units on every day, so the spread mixes rate change with band migration.
    per_day = {}
    for lbl, d in (("as_shipped", old), ("corrected", new)):
        pd = d["per_day"]
        per_day[lbl] = {day: pd[day]["by_age_band"].get("5y+") for day in sorted(pd)}
    return {"by_band": rows, "the_5y_plus_cell_day_by_day": per_day,
            "mechanism": (
                "cohort migration, not instability. Under per-day banding the 5y+ cell GROWS "
                "across the panel while its absent count stays at 68, so its rate falls "
                "monotonically by construction and the range widens. The consequence is a real "
                "methodological cost of the V1 repair: the by-band across-day spread is no longer "
                "a test-retest measure of the same units. Neither banding is simply better, and "
                "any across-day stability claim from this arc must now say which one it used.")}


def receiver_eleven_at_the_withdrawn_threshold(baseline):
    """Interlocutor 14 finding 6, and the one figure where our recomputation disagrees with the
    reviewer's. Their report gives -0.0037 pp; ours gives -0.00032514. Both are published."""
    t_decl = calendar.timegm(time.strptime(baseline["t_ref_utc"], "%Y-%m-%dT%H:%M:%SZ"))
    vids = []
    for raw in open("receiver-list.txt", encoding="utf-8"):
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        m = re.search(r"/video/(\d+)", s) or re.search(r"(\d{1,25})", s)
        if m:
            vids.append(m.group(1))
    out = {}
    for dd in (0, 25, 26, 27, 30, 60, 90, 365):
        now = t_decl + dd * 86400
        rows = [{"vid": v, "band": P.band_of((now - (int(v) >> 32)) / P.YEAR_S)} for v in vids]
        d = P.drift(rows, baseline, now)
        out[str(dd)] = {"drift_pp": d["drift_pp"], "comparable": d["comparable"],
                        "fired_under_the_withdrawn_26_day_rule": dd > 26}
    out["_disagreement_with_the_reviewer"] = {
        "reviewer_reported_pp_at_day_26_and_27": -0.0037,
        "our_recomputation_pp": out["26"]["drift_pp"],
        "note": ("we cannot reconstruct the reviewer's figure and publish both. The charge is "
                 "unaffected and is stronger with ours: the drift at the withdrawn threshold is "
                 "negative and roughly 560 times smaller than the 0.1826 pp the warning named."),
    }
    return out


def adversary_cases(baseline):
    """Interlocutor 14 findings 1 and 2, reproduced against v0.3.1 rather than described."""
    t_decl = calendar.timegm(time.strptime(baseline["t_ref_utc"], "%Y-%m-%dT%H:%M:%SZ"))
    now = t_decl + 400 * 86400

    def mk(days_before):
        return str((int(t_decl - days_before * 86400) << 32) | 1)

    def rows_for(vids):
        return [{"vid": v, "band": P.band_of((now - (int(v) >> 32)) / P.YEAR_S)} for v in vids]

    all_new = P.drift(rows_for([mk(-50 - i * 10) for i in range(5)]), baseline, now)
    mixed_rows = rows_for([mk(800 + i * 300) for i in range(5)]
                          + [mk(-50 - i * 10) for i in range(5)])
    mixed = P.drift(mixed_rows, baseline, now)
    # v0.3.0's arithmetic, RECOMPUTED rather than copied from the adversary's console: the
    # today-aged expectation over the whole list minus the reference-time expectation over the
    # old half, which is what v0.3.0 printed as "drift".
    _now_exp = P.expectation(mixed_rows, baseline)
    _ref_exp = P.expectation(P.rebanded(mixed_rows, t_decl), baseline)
    v030_printed = 100 * (_now_exp["expected_absent_rate"] - _ref_exp["expected_absent_rate"])
    return {
        "finding_1_list_entirely_postdates_the_table": {
            "v0_3_0_behaviour": "drift() returned None; the printer silently fell through to the "
                                "today-aged figure, unlabelled",
            "v0_3_1_drift_pp": all_new["drift_pp"],
            "v0_3_1_comparable": all_new["comparable"],
            "v0_3_1_reason": all_new["why_the_drift_is_not_reported"],
            "n_at_the_reference_time": all_new["n_dated_at_the_reference_time"],
            "n_at_now": all_new["n_dated_at_now"],
        },
        "finding_2_mixed_list": {
            "v0_3_0_printed_drift_pp": v030_printed,
            "v0_3_0_printed_drift_pp_source": ("recomputed here, not copied: the today-aged "
                                               "expectation over all 10 units minus the "
                                               "reference-time expectation over the 5 datable "
                                               "then. The adversary reported -4.8752"),
            "v0_3_1_drift_pp": mixed["drift_pp"],
            "v0_3_1_comparable": mixed["comparable"],
            "v0_3_1_reason": mixed["why_the_drift_is_not_reported"],
            "n_at_the_reference_time": mixed["n_dated_at_the_reference_time"],
            "n_at_now": mixed["n_dated_at_now"],
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="gauntlet-followup-122.json")
    ap.add_argument("--cutoff", default="2026-08-14T23:59:59Z")
    a = ap.parse_args()

    days = D.load_days(a.cutoff)
    units = D.build_units(days)
    baseline, why = P.load_baseline(CORRECTED)
    if not baseline:
        raise SystemExit(f"the corrected reference table did not load: {why}")

    out = {
        "schema": "field-research/gauntlet-followup/1",
        "written_by": "gauntlet_followup_122.py, session 122, 2026-08-16",
        "why_this_exists": (
            "erratum E1 of this session: three counts were published from a run that was never "
            "captured. Every figure ERRATA-122.md and CONDITIONS-122.md state in answer to the "
            "gauntlet is computed here so it has a machine source and can be re-checked."),
        "reviewed_state": "95ab278 (both reports); the repairs measured here are v0.3.1 and carry "
                          "no verdict",
        "crossover_family": crossover_family(units, days, days[-1]),
        "across_day_stability": across_day_stability(),
        "receiver_eleven_drift": receiver_eleven_at_the_withdrawn_threshold(baseline),
        "adversary_cases_reproduced_against_v0_3_1": adversary_cases(baseline),
        "comparand_used_by_v0_3_1": P.BOOKKEEPING_COMPARAND_PP,
    }
    json.dump(out, open(a.out, "w"), indent=1)
    fam = out["crossover_family"]
    print(json.dumps({k: v["crossover_days"] for k, v in fam.items() if k[0] != "_"}, indent=1))
    print("comparand used by v0.3.1:", out["comparand_used_by_v0_3_1"])
    print("5y+ across-day spread:",
          round(out["across_day_stability"]["by_band"]["5y+"]["range_pp_as_shipped"], 4), "->",
          round(out["across_day_stability"]["by_band"]["5y+"]["range_pp_corrected"], 4), "pp")


if __name__ == "__main__":
    main()
