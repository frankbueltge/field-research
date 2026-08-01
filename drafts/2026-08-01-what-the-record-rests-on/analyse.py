#!/usr/bin/env python3
"""
Turns the inventory and the dated probe into results, with the estimation discipline the
design's own pre-read made blocking.

The sample is stratified with EQUAL allocation (20 report records per publication-year
stratum), and the strata are wildly unequal in the population (112 to 1,448). So a raw
sample percentage is not a corpus rate, and a weighted corpus rate is less precise than its
sample size suggests. Every corpus-wide number here therefore carries: per-stratum counts,
the weights, a stratified confidence interval with a finite-population correction, the
weighting design effect, and the effective sample size.

Usage:  python3 analyse.py --probe probe-2026-08-01.json --out results.json
"""

import argparse
import collections
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
Z = 1.96


def stratified(sample_rows, indicator, strata_sizes):
    """Weighted estimate of a proportion under stratified sampling without replacement.

    indicator(row) -> True / False / None.  None means the row is out of scope for this
    question and is dropped from BOTH numerator and denominator of its stratum.
    """
    per = {}
    for row in sample_rows:
        v = indicator(row)
        if v is None:
            continue
        d = per.setdefault(row["stratum"], {"n": 0, "k": 0})
        d["n"] += 1
        d["k"] += 1 if v else 0

    N = sum(strata_sizes[h] for h in per)
    if not per or N == 0:
        return {"estimable": False, "reason": "no in-scope observations"}

    est, var, sum_w2, sum_w = 0.0, 0.0, 0.0, 0.0
    rows = {}
    for h, d in per.items():
        Nh, nh, k = strata_sizes[h], d["n"], d["k"]
        ph = k / nh
        Wh = Nh / N
        est += Wh * ph
        if nh > 1:
            fpc = max(0.0, 1.0 - nh / Nh)
            var += (Wh ** 2) * fpc * ph * (1 - ph) / (nh - 1)
        w = Nh / nh                      # sampling weight of one drawn record
        sum_w += nh * w
        sum_w2 += nh * (w ** 2)
        rows[h] = {"stratum_population": Nh, "sampled": nh, "with_property": k,
                   "rate_in_stratum": round(ph, 4), "weight": round(Wh, 5)}

    n_total = sum(d["n"] for d in per.values())
    se = math.sqrt(var)
    # Kish's design effect from unequal weighting alone.
    deff = (n_total * sum_w2 / (sum_w ** 2)) if sum_w else float("nan")
    return {
        "estimable": True,
        "weighted_estimate": round(est, 4),
        "standard_error": round(se, 4),
        "ci95": [round(max(0.0, est - Z * se), 4), round(min(1.0, est + Z * se), 4)],
        "sample_n_in_scope": n_total,
        "unweighted_sample_rate": round(sum(d["k"] for d in per.values()) / n_total, 4),
        "design_effect_from_weighting": round(deff, 3),
        "effective_sample_size": round(n_total / deff, 1) if deff else None,
        "per_stratum": dict(sorted(rows.items())),
        "population_covered": N,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", required=True)
    ap.add_argument("--out", default="results.json")
    args = ap.parse_args()

    inv = json.load(open(os.path.join(HERE, "inventory.json"), encoding="utf-8"))
    smp = json.load(open(os.path.join(HERE, "sample.json"), encoding="utf-8"))
    pr = json.load(open(os.path.join(HERE, args.probe), encoding="utf-8"))

    strata_sizes = inv["strata"]["sizes_in_population"]
    live = {r["report_number"]: r for r in pr["live"]}
    arch = {r["report_number"]: r for r in pr["archive"]}
    calib = {r["report_number"]: r for r in pr.get("calibration", [])}

    rows = []
    for s in smp["reports"]:
        n = s["report_number"]
        rows.append({**s, "live": live.get(n, {}), "arch": arch.get(n, {}), "calib": calib.get(n, {})})

    def l1(r):
        return r["live"].get("l1_class")

    def l3(r):
        return r["live"].get("l3_class")

    counts = {
        "l1_class": dict(collections.Counter(l1(r) for r in rows).most_common()),
        "l1_class_on_self_identifying_retry": dict(collections.Counter(
            r["live"].get("retry_l1_class") for r in rows if r["live"].get("retry_l1_class")).most_common()),
        "l3_class": dict(collections.Counter(l3(r) for r in rows).most_common()),
        "l2_class": dict(collections.Counter(r["arch"].get("l2_class") for r in rows).most_common()),
        "l3c_class": dict(collections.Counter(r["calib"].get("l3c_class") for r in rows
                                              if r["calib"]).most_common()),
    }

    GONE_HARD = {"HTTP_404", "HTTP_410", "DNS_FAIL"}
    ANSWERS = {"HTTP_200", "REDIRECT_TO_ROOT"}
    WITHHELD = {"HTTP_401", "HTTP_402", "HTTP_403", "HTTP_451"}

    def in_l3_scope(r):
        """L3 can only speak about a page that actually served this vantage a document."""
        if l1(r) not in ANSWERS:
            return False
        if l3(r) in ("REGISTER_STAND_IN", "BOT_WALL", "NO_HELD_TEXT", "NON_HTML", "UNDECODABLE"):
            return False
        return True

    estimates = {
        "citation_does_not_answer_200": stratified(
            rows, lambda r: l1(r) not in ANSWERS if l1(r) else None, strata_sizes),
        "citation_is_hard_gone_404_410_or_no_dns": stratified(
            rows, lambda r: l1(r) in GONE_HARD if l1(r) else None, strata_sizes),
        "citation_withheld_from_this_vantage_401_402_403_451": stratified(
            rows, lambda r: l1(r) in WITHHELD if l1(r) else None, strata_sizes),
        "citation_redirected_to_site_root": stratified(
            rows, lambda r: l1(r) == "REDIRECT_TO_ROOT" if l1(r) else None, strata_sizes),
        "among_pages_that_served_a_document_the_stored_passage_is_gone": stratified(
            rows, lambda r: (l3(r) == "ABSENT") if in_l3_scope(r) else None, strata_sizes),
        "among_pages_that_served_a_document_the_stored_passage_still_holds": stratified(
            rows, lambda r: (l3(r) == "HOLDS") if in_l3_scope(r) else None, strata_sizes),
        "citation_still_delivers_the_stored_passage_to_this_vantage": stratified(
            rows, lambda r: (l1(r) in ANSWERS and l3(r) == "HOLDS") if l1(r) else None, strata_sizes),
        "public_archive_holds_at_least_one_capture": stratified(
            rows, lambda r: (r["arch"].get("l2_class") == "CAPTURED")
            if r["arch"].get("l2_class") in ("CAPTURED", "NO_CAPTURE") else None, strata_sizes),
        "archive_holds_a_capture_at_or_before_the_registers_download_date": stratified(
            rows, lambda r: r["arch"].get("capture_at_or_before_register_download")
            if (r["arch"].get("l2_class") in ("CAPTURED", "NO_CAPTURE")
                and not r["flag_date_published_after_downloaded"]
                and r["arch"].get("capture_at_or_before_register_download") is not None) else None,
            strata_sizes),
    }

    # The control layer, reported as counts rather than as a rate: it is run only on the
    # cases where the live page did not clearly hold the passage, so it is not a sample of
    # anything and must never be read as one.
    calib_rows = [r for r in rows if r["calib"]]
    calibration = {
        "what_it_is": pr.get("l3c"),
        "run_on": "only the cases where the live page did not clearly still hold the stored passage",
        "not_a_sample": ("These counts are a control on the instrument, not an estimate of any "
                         "population. No rate here may be read as a corpus rate."),
        "n": len(calib_rows),
        "by_live_class": {},
    }
    for r in calib_rows:
        b = calibration["by_live_class"].setdefault(l3(r) or "UNKNOWN", collections.Counter())
        b[r["calib"].get("l3c_class")] += 1
    calibration["by_live_class"] = {k: dict(v) for k, v in calibration["by_live_class"].items()}

    decided = [r for r in calib_rows
               if r["calib"].get("l3c_class") in ("ARCHIVED_COPY_HOLDS", "ARCHIVED_COPY_PARTIAL",
                                                  "ARCHIVED_COPY_ABSENT")]
    calibration["decidable_cases"] = len(decided)
    calibration["archived_copy_holds_the_stored_passage"] = sum(
        1 for r in decided if r["calib"]["l3c_class"] == "ARCHIVED_COPY_HOLDS")
    calibration["reading"] = (
        "Where the archived capture taken at or before the register's own download date still "
        "contains the stored passage, the extractor and the stored copy agree, and the loss "
        "measured on the live page today is a loss on the live web. Where it does not, the "
        "mismatch predates today and cannot be called drift."
    )

    out = {
        "work": "What the Record Rests On",
        "built": "2026-08-01",
        "status": "DRAFT — not shipped, no gauntlet verdict",
        "inputs": {"snapshot_sha256": inv["snapshot"]["sha256"],
                   "probe_file": args.probe,
                   "probe_started_utc": pr["probe_started_utc"],
                   "probe_finished_utc": pr["probe_finished_utc"],
                   "vantage": pr["vantage"]},
        "population": inv["population"],
        "sample": {"seed": smp["seed"], "n": smp["n"],
                   "allocation": inv["sampling"]["allocation"],
                   "strata_population_sizes": strata_sizes},
        "counts_in_sample": counts,
        "estimates_for_the_population_of_sourced_report_records": estimates,
        "calibration_control": calibration,
        "standing_scope_exclusions": [
            "No claim is made about why any document stopped answering. Nothing here can "
            "distinguish an ordinary expiry from a deliberate removal, and no such claim is made.",
            "There is no control corpus of contemporaneous citations on other subjects, so nothing "
            "here says whether citations about AI harm decay faster or slower than citations in "
            "general.",
            "Every live number is what one datacenter vantage saw on one day. Classes that record "
            "refusal to this vantage are reported separately and are never counted as removal.",
            "Lexical overlap measures words, not meaning. A rewritten or translated page that says "
            "the same thing scores as loss, and that is a limit of the measure, not a finding.",
        ],
    }
    with open(os.path.join(HERE, args.out), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("wrote", args.out)
    for k, v in estimates.items():
        if v.get("estimable"):
            print(f"  {k}: {v['weighted_estimate']:.3f} "
                  f"[{v['ci95'][0]:.3f}, {v['ci95'][1]:.3f}]  n={v['sample_n_in_scope']} "
                  f"deff={v['design_effect_from_weighting']} n_eff={v['effective_sample_size']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
