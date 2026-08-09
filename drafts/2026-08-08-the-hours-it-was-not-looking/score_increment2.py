#!/usr/bin/env python3
"""score_increment2.py — score PREREGISTRATION-2.md against the run of open_at_scale.py.

Reads the run payload, computes Q1-Q8 exactly as the pre-registration words them, and
writes a scored summary. No threshold in this file was changed after a number existed;
where the pre-registration is ambiguous the stricter reading is used and the choice is
printed.

Usage: python3 score_increment2.py <opened.json> <out.json>
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict

COLLAPSE_FRAC = 0.20      # pre-registered in Q1 and Q4
DUP_FRAC = 0.50           # pre-registered in Q6
MB = 1024 * 1024


def main():
    payload = json.load(open(sys.argv[1]))
    out_path = sys.argv[2]
    recs = {r["ts"]: r for r in payload["downloads"]}
    samples = payload["samples"]

    ok = [r for r in recs.values() if r.get("zip_opens") and r.get("http_status") == 200]
    failed = [r for r in recs.values() if not (r.get("zip_opens") and r.get("http_status") == 200)]

    # ---- Q7: listed but absent ---------------------------------------------------
    q7 = {"attempted": len(recs), "failed": len(failed),
          "detail": [{"ts": r["ts"], "status": r.get("http_status"), "error": r.get("error")}
                     for r in failed]}

    # ---- Q5: integrity -----------------------------------------------------------
    size_ok = [r for r in ok if r["size_matches_manifest"]]
    md5_ok = [r for r in ok if r["md5_matches_manifest"]]
    both_ok = [r for r in ok if r["size_matches_manifest"] and r["md5_matches_manifest"]]
    q5 = {"downloaded_ok": len(ok), "size_and_md5_match": len(both_ok),
          "rate": round(len(both_ok) / len(ok), 6) if ok else None,
          "size_mismatches": [{"ts": r["ts"], "manifest": r["manifest_size"],
                               "received": r["bytes_received"]}
                              for r in ok if not r["size_matches_manifest"]],
          "md5_mismatches": [{"ts": r["ts"], "manifest": r["manifest_md5"],
                              "received": r["md5_received"]}
                             for r in ok if not r["md5_matches_manifest"]]}

    # ---- Q1 and Q2: the collapsed sample against its matched control --------------
    pairs, q1_hits, q1_scored = [], 0, 0
    for a_ts, b_ts in samples["B"]:
        a, b = recs.get(a_ts), recs.get(b_ts)
        if not a or not b or not a.get("zip_opens") or not b.get("zip_opens"):
            continue
        q1_scored += 1
        hit = a["records"] < COLLAPSE_FRAC * b["records"]
        q1_hits += hit
        pairs.append({"collapsed": a_ts, "control": b_ts,
                      "collapsed_records": a["records"], "control_records": b["records"],
                      "collapsed_bytes": a["bytes_received"], "control_bytes": b["bytes_received"],
                      "ratio": round(a["records"] / b["records"], 5) if b["records"] else None,
                      "below_threshold": hit})
    q1 = {"scored_pairs": q1_scored, "below_20pct_of_control": q1_hits,
          "rate": round(q1_hits / q1_scored, 4) if q1_scored else None}

    a_ok = [recs[t] for t in samples["A"] if recs[t].get("zip_opens")]
    zeros = [r for r in a_ok if r["records"] == 0]
    empty_inner = [r for r in a_ok if r["inner_bytes"] == 0]
    q2 = {"sample_a_opened": len(a_ok), "zero_record_files": len(zeros),
          "rate": round(len(zeros) / len(a_ok), 4) if a_ok else None,
          "zero_byte_inner_files": len(empty_inner),
          "detail": [{"ts": r["ts"], "zip_bytes": r["bytes_received"],
                      "inner_bytes": r["inner_bytes"]} for r in zeros]}

    # ---- the unflagged corpus: B + C + D, deduplicated ---------------------------
    unflagged_ts = set()
    unflagged_ts.update(b for _, b in samples["B"])
    unflagged_ts.update(samples["C"])
    for r in recs.values():
        if any(s in ("D1", "D2") for s in r["samples"]):
            unflagged_ts.add(r["ts"])
    unflagged = [recs[t] for t in unflagged_ts
                 if recs[t].get("zip_opens") and recs[t]["records"] > 0]

    per_year = defaultdict(list)
    for r in unflagged:
        per_year[r["ts"][:4]].append(r["records"] / (r["bytes_received"] / MB))
    year_median = {y: statistics.median(v) for y, v in per_year.items()}
    year_n = {y: len(v) for y, v in per_year.items()}

    years = sorted(year_median)
    q3 = {"records_per_MB_median_by_year": {y: round(year_median[y], 2) for y in years},
          "n_by_year": year_n,
          "earliest_year": years[0] if years else None,
          "latest_year": years[-1] if years else None,
          "factor": round(max(year_median[years[0]], year_median[years[-1]])
                          / min(year_median[years[0]], year_median[years[-1]]), 3)
          if years else None,
          "min_year_median": round(min(year_median.values()), 2) if years else None,
          "max_year_median": round(max(year_median.values()), 2) if years else None,
          "max_over_min_factor": round(max(year_median.values()) / min(year_median.values()), 3)
          if years else None}

    # ---- Q4: a normal-sized unflagged file whose contents are not normal ----------
    q4_rows, q4_hits = [], 0
    for t in samples["C"]:
        r = recs[t]
        if not r.get("zip_opens"):
            continue
        yr = t[:4]
        if yr not in year_median:
            continue
        # leave-one-out median, so a cycle is never scored against itself
        others = [v for i, v in enumerate(per_year[yr])
                  if abs(v - r["records"] / (r["bytes_received"] / MB)) > 1e-12 or True]
        loo = [x["records"] / (x["bytes_received"] / MB)
               for x in unflagged if x["ts"][:4] == yr and x["ts"] != t]
        med = statistics.median(loo) if loo else year_median[yr]
        predicted = med * (r["bytes_received"] / MB)
        ratio = r["records"] / predicted if predicted else None
        hit = ratio is not None and ratio < COLLAPSE_FRAC
        q4_hits += hit
        q4_rows.append({"ts": t, "bytes": r["bytes_received"], "records": r["records"],
                        "year_median_records_per_MB_loo": round(med, 2),
                        "predicted_records": round(predicted, 1),
                        "ratio_actual_to_predicted": round(ratio, 4) if ratio else None,
                        "below_threshold": hit})
    ratios = [row["ratio_actual_to_predicted"] for row in q4_rows
              if row["ratio_actual_to_predicted"] is not None]
    q4 = {"scored": len(q4_rows), "below_20pct_of_predicted": q4_hits,
          "min_ratio": min(ratios) if ratios else None,
          "max_ratio": max(ratios) if ratios else None,
          "median_ratio": round(statistics.median(ratios), 4) if ratios else None,
          "n_below_half": sum(1 for x in ratios if x < 0.5),
          "n_above_double": sum(1 for x in ratios if x > 2.0)}

    # ---- Q6: consecutive-pair duplication ----------------------------------------
    q6_rows, q6_hits = [], 0
    from datetime import datetime, timedelta, timezone
    for t in samples["D_pair_first"]:
        nxt = (datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
               + timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%SZ")
        a, b = recs.get(t), recs.get(nxt)
        if not a or not b or "docids" not in a or "docids" not in b:
            continue
        sa, sb = set(a["docids"]), set(b["docids"])
        overlap = len(sa & sb) / len(sb) if sb else None
        hit = overlap is not None and overlap >= DUP_FRAC
        q6_hits += hit
        q6_rows.append({"first": t, "second": nxt,
                        "first_records": a["records"], "second_records": b["records"],
                        "first_docids": len(sa), "second_docids": len(sb),
                        "shared": len(sa & sb),
                        "overlap_of_second": round(overlap, 5) if overlap is not None else None,
                        "above_threshold": hit})
    ov = [r["overlap_of_second"] for r in q6_rows if r["overlap_of_second"] is not None]
    q6 = {"pairs_scored": len(q6_rows), "pairs_over_50pct": q6_hits,
          "max_overlap": max(ov) if ov else None,
          "median_overlap": round(statistics.median(ov), 5) if ov else None,
          "mean_dup_within_file": None}

    # duplicate DocumentIdentifiers *within* a single file (unregistered, reported apart)
    dup_within = []
    for r in recs.values():
        if "docids" in r and r["records"]:
            dup_within.append({"ts": r["ts"], "records": r["records"],
                               "distinct_docids": len(r["docids"]),
                               "dup_fraction": round(1 - len(r["docids"]) / r["records"], 5)})

    q8 = payload["q8_manifest_stability"]

    verdicts = {
        "Q1": "HELD" if q1["rate"] is not None and q1["rate"] >= 0.90 else "NOT HELD",
        "Q2": "HELD" if q2["rate"] is not None and q2["rate"] >= 0.05 else "NOT HELD",
        "Q3": "HELD" if q3["factor"] is not None and q3["factor"] >= 2.0 else "NOT HELD",
        "Q4": "HELD" if q4["below_20pct_of_predicted"] >= 1 else "NOT HELD",
        "Q5": "HELD" if q5["rate"] is not None and q5["rate"] >= 0.99 else "NOT HELD",
        "Q6": "HELD" if q6["pairs_over_50pct"] >= 1 else "NOT HELD",
        "Q7": "HELD" if q7["failed"] >= 1 else "NOT HELD",
        "Q8": "HELD" if q8["checked"] == 3137 and q8["identical"] == 3137 else "NOT HELD",
    }
    kill = (verdicts["Q1"] == "HELD" and verdicts["Q4"] == "NOT HELD"
            and verdicts["Q6"] == "NOT HELD" and verdicts["Q7"] == "NOT HELD"
            and q5["rate"] == 1.0)

    res = {"run_utc": payload["run_utc"], "seed": payload["seed"],
           "downloads": len(recs), "opened_ok": len(ok),
           "Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5, "Q6": q6, "Q7": q7, "Q8": q8,
           "verdicts": verdicts,
           "kill_criterion_fires": kill,
           "pairs_detail": pairs, "q4_detail": q4_rows, "q6_detail": q6_rows,
           "within_file_duplicate_docids": dup_within}
    json.dump(res, open(out_path, "w"), indent=1)
    print(json.dumps({"verdicts": verdicts, "kill_criterion_fires": kill,
                      "Q1": {k: q1[k] for k in ("scored_pairs", "below_20pct_of_control", "rate")},
                      "Q2": {k: q2[k] for k in ("sample_a_opened", "zero_record_files", "rate",
                                                "zero_byte_inner_files")},
                      "Q3": {k: q3[k] for k in ("records_per_MB_median_by_year", "n_by_year",
                                                "factor", "max_over_min_factor")},
                      "Q4": q4, "Q5": {k: q5[k] for k in ("downloaded_ok", "size_and_md5_match", "rate")},
                      "Q6": {k: q6[k] for k in ("pairs_scored", "pairs_over_50pct",
                                                "max_overlap", "median_overlap")},
                      "Q7": {k: q7[k] for k in ("attempted", "failed")},
                      "Q8": {k: q8[k] for k in ("checked", "identical")}}, indent=1))


if __name__ == "__main__":
    main()
