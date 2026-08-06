#!/usr/bin/env python3
"""analyse_2.py — score G1..G6 and the continuation test of PREREGISTRATION-2.md.

Arm B (chrome-filtered, amendment 4) is the scored arm. Arm A (as first pre-registered) is
computed alongside for every headline figure; disagreement between the arms is defect D7.
EC is a re-analysis of the locked session-94 signals, never a re-collection.
Writes results-2.json.
"""

from __future__ import annotations

import datetime as dt
import json
import statistics

DAY = 86400.0


def iso(v):
    return dt.datetime.fromisoformat(v) if v else None


def pct(n, d):
    return None if not d else round(100.0 * n / d, 1)


def profile(rows, run_started):
    """The citer profile of one arm: what share of successfully fetched pages carries each signal."""
    ok = [r for r in rows if r["fetch"] == "OK"]
    n = len(ok)
    with_h = [r for r in ok if r.get("h")]
    with_s = [r for r in ok if r.get("s")]
    with_v = [r for r in ok if r.get("v")]
    fresh = [r for r in with_h if (run_started - iso(r["h"])).total_seconds() < DAY]
    both_sv = [r for r in ok if r.get("s") and r.get("v")]
    agree = [r for r in both_sv if iso(r["s"]).date() == iso(r["v"]).date()]
    both_hs = [r for r in ok if r.get("h") and r.get("s")]
    gaps = [abs((iso(r["h"]) - iso(r["s"])).total_seconds()) / DAY for r in both_hs]
    return {
        "n_fetched": len(rows), "n_ok": n, "n_netfail": len(rows) - n,
        "h_n": len(with_h), "h_share": pct(len(with_h), n),
        "s_n": len(with_s), "s_share": pct(len(with_s), n),
        "v_n": len(with_v), "v_share": pct(len(with_v), n),
        "h_fresh_24h_n": len(fresh), "h_fresh_24h_share_of_h": pct(len(fresh), len(with_h)),
        "sv_both_n": len(both_sv), "sv_agree_to_day_n": len(agree),
        "sv_agree_share": pct(len(agree), len(both_sv)),
        "hs_both_n": len(both_hs),
        "hs_gap_days_median": round(statistics.median(gaps), 2) if gaps else None,
        "hs_gap_over_1d_n": sum(1 for g in gaps if g > 1.0),
        "hs_gap_over_1d_share": pct(sum(1 for g in gaps if g > 1.0), len(gaps)),
    }


def main() -> int:
    sig2 = json.load(open("signals-2.json"))
    run_started = iso(sig2["run_started_utc"])
    chrome = json.load(open("chrome-2.json"))["authorities"]

    out = {
        "instrument": "as-of-today", "stage": "analysis, proof session 2",
        "preregistration": "PREREGISTRATION-2.md (amendments 1-4)",
        "run_started_utc": sig2["run_started_utc"],
        "scored_arm": "B (chrome-filtered, amendment 4)",
        "authorities": {},
    }

    for key, a in sig2["authorities"].items():
        rows = a["rows"]
        out["authorities"][key] = {
            "seed": a["seed"],
            "sitemap": {k: v for k, v in a["sitemap"].items() if k != "log"},
            "arm_b": profile([r for r in rows if r["arm_b"]], run_started),
            "arm_a": profile([r for r in rows if r["arm_a"]], run_started),
            "inconclusive_n_under_15": len([r for r in rows if r["arm_b"]]) < 15,
        }

    # EC — re-analysis of the locked session-94 signals. Not re-collected.
    ec = json.load(open("signals.json"))
    ec_run = iso(ec["run_started_utc"])
    ec_chrome = set(chrome["EC"]["chrome"]) | {"https://digital-strategy.ec.europa.eu"}
    ec_rows = []
    for r in ec["rows"]:
        rr = dict(r)
        rr["fetch"] = "OK" if r.get("fetch") == "OK" else "NETFAIL"
        ec_rows.append(rr)
    def norm(u):
        return u.rstrip("/")
    ec_items = [r for r in ec_rows if norm(r["url"]) not in {norm(u) for u in ec_chrome}]
    out["authorities"]["EC"] = {
        "seed": "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai",
        "source": "locked session-94 signals.json, re-analysed; NOT re-collected",
        "locked_run_started_utc": ec["run_started_utc"],
        "arm_b": profile(ec_items, ec_run),
        "arm_a": profile(ec_rows, ec_run),
        "inconclusive_n_under_15": len(ec_items) < 15,
    }

    A = out["authorities"]
    SCORED = [k for k in ("EC", "NIST", "IE") if k in A]        # GOVUK: n=7, inconclusive
    arm = "arm_b"

    def spread(field):
        vals = {k: A[k][arm][field] for k in SCORED if A[k][arm][field] is not None}
        if len(vals) < 2:
            return None, vals
        return round(max(vals.values()) - min(vals.values()), 1), vals

    g = {}

    # G1 — GOVUK < 10 % H (NOT RESOLVABLE: inconclusive) and NIST > 90 % H
    nist_h = A["NIST"][arm]["h_share"]
    g["G1"] = {
        "statement": "H present on <10 % of GOVUK and >90 % of NIST",
        "govuk_h_share": A["GOVUK"][arm]["h_share"],
        "govuk_verdict": "NOT RESOLVABLE — GOVUK inconclusive at n=7 (C2-RULE-4, amendment 2)",
        "nist_h_share": nist_h,
        "nist_verdict": "HELD" if nist_h is not None and nist_h > 90 else "KILLED",
        "verdict": ("HELD (NIST half only; GOVUK half not resolvable)"
                    if nist_h is not None and nist_h > 90
                    else "KILLED (NIST half; GOVUK half not resolvable)"),
    }

    # G2 — designated known mechanism, scores nothing
    g2 = {}
    for k in SCORED + ["GOVUK"]:
        p = A[k][arm]
        if p["h_n"] >= 10:
            g2[k] = {"h_n": p["h_n"], "fresh_share": p["h_fresh_24h_share_of_h"],
                     "verdict": "HELD" if p["h_fresh_24h_share_of_h"] >= 80 else "KILLED"}
        else:
            g2[k] = {"h_n": p["h_n"], "verdict": "NOT APPLICABLE (fewer than 10 H)"}
    g["G2"] = {"statement": "where H exists, >=80 % younger than 24 h — KNOWN MECHANISM, SCORES NOTHING",
               "per_authority": g2, "counts_toward_continuation": False}

    # G3 — on at least one new authority, S<->V agreement < 80 %
    g3 = {k: {"both_n": A[k][arm]["sv_both_n"], "agree_share": A[k][arm]["sv_agree_share"]}
          for k in ("NIST", "IE")}
    under = [k for k, v in g3.items() if v["agree_share"] is not None and v["agree_share"] < 80]
    g["G3"] = {"statement": "S and V agree to the day on <80 % for at least one new authority",
               "per_authority": g3, "below_80": under,
               "verdict": "HELD" if under else "KILLED",
               "ec_baseline": {"both_n": A["EC"][arm]["sv_both_n"],
                               "agree_share": A["EC"][arm]["sv_agree_share"]}}

    # G4 — S coverage < 100 % on NIST (GOVUK half not resolvable)
    nist_s = A["NIST"][arm]["s_share"]
    g["G4"] = {"statement": "sitemap coverage of the hub's own outbound corpus is < 100 %",
               "nist_s_share": nist_s, "ie_s_share": A["IE"][arm]["s_share"],
               "govuk_verdict": "NOT RESOLVABLE — inconclusive at n=7",
               "verdict": "HELD" if nist_s is not None and nist_s < 100 else "KILLED"}

    # G5 — largest pairwise S-coverage difference across the scored authorities > 25 points
    s_spread, s_vals = spread("s_share")
    g["G5"] = {"statement": "largest pairwise difference in S-coverage > 25 points",
               "s_shares": s_vals, "spread_points": s_spread,
               "verdict": "HELD" if s_spread is not None and s_spread > 25 else "KILLED"}

    # G6 — pooled over the two new measurable authorities, |H-S| > 1 day for >= 60 %
    pooled = []
    for k in ("NIST", "IE"):
        rows = [r for r in sig2["authorities"][k]["rows"] if r["arm_b"] and r["fetch"] == "OK"]
        for r in rows:
            if r.get("h") and r.get("s"):
                pooled.append(abs((iso(r["h"]) - iso(r["s"])).total_seconds()) / DAY)
    over = sum(1 for x in pooled if x > 1.0)
    g["G6"] = {"statement": "|H-S| > 1 day for >=60 % of URLs where both exist (INFORMED BY EC)",
               "pooled_n": len(pooled), "over_1d_n": over,
               "over_1d_share": pct(over, len(pooled)),
               "median_gap_days": round(statistics.median(pooled), 2) if pooled else None,
               "verdict": ("NOT RESOLVABLE (fewer than 10 pairs)" if len(pooled) < 10
                           else "HELD" if pct(over, len(pooled)) >= 60 else "KILLED")}

    out["predictions"] = g

    # Continuation test
    scoring = ["G1", "G3", "G4", "G5", "G6"]
    holds = [k for k in scoring if g[k]["verdict"].startswith("HELD")]
    spreads = {f: spread(f)[0] for f in ("h_share", "s_share", "v_share")}
    clause_b = any(v is not None and v > 25 for v in spreads.values())
    out["continuation_test"] = {
        "clause_a_at_least_one_of_G1_G3_G4_G5_G6_holds": bool(holds), "holds": holds,
        "clause_b_profile_spread_over_25_points": clause_b, "profile_spreads": spreads,
        "citer_profiles": {k: {f: A[k][arm][f] for f in ("h_share", "s_share", "v_share")}
                           for k in SCORED},
        "verdict": "CONTINUE" if holds and clause_b else "DO NOT CONTINUE",
    }

    # D7 — do the arms disagree?
    d7 = {}
    for k in SCORED:
        if k == "EC":
            continue
        d7[k] = {f: {"arm_b": A[k]["arm_b"][f], "arm_a": A[k]["arm_a"][f]}
                 for f in ("h_share", "s_share", "v_share", "sv_agree_share")}
    out["d7_arm_disagreement"] = d7

    with open("results-2.json", "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    print(json.dumps({"predictions": {k: v.get("verdict") for k, v in g.items()},
                      "continuation": out["continuation_test"]["verdict"],
                      "profiles": out["continuation_test"]["citer_profiles"],
                      "spreads": spreads}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
