#!/usr/bin/env python3
"""What the pre-registered window is worth on the corpus that will actually run.

`power_audit.py` audited the corpus as session 110 left it. This recomputes the same
quantities on the corpus **after** the session-111 expansion — the union of session 110's
run and every session-111 baseline run — because that is the population §5a will be applied
to on 2026-08-18.

The fitter, the exclusions, the dating rule, the hazard and the exposure accounting are
`power_audit.py`'s, imported rather than re-implemented, so the two numbers are comparable
by construction. The governing window is **seven intervals** (`POWER-AUDIT.md` §8a).

Also runs the standing method rule adopted this session: every shape parameter carries a
cohort-sub-window refit beside it, and K3 is scored against every specification run.
"""
import calendar
import glob
import importlib.util
import json
import math
import os
import time

spec = importlib.util.spec_from_file_location("pa", "power_audit.py")
pa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pa)

T_REF = calendar.timegm((2026, 8, 11, 12, 0, 0, 0, 0, 0))
YEAR_S = 365.25 * 86400.0
D = 7  # the governing reading: seven runs, 2026-08-12 .. 2026-08-18


def rows_from(path):
    d = json.load(open(path))
    out, exc = [], {"B_truncated": 0, "indeterminate": 0, "not_19": 0, "nonpositive": 0}
    for o in d["observations"]:
        if o["arm"] == "B-truncated":
            exc["B_truncated"] += 1
            continue
        if o["state"] == "INDETERMINATE":
            exc["indeterminate"] += 1
            continue
        v = str(o["vid"])
        if len(v) != 19:
            exc["not_19"] += 1
            continue
        age_s = T_REF - (int(v) >> 32)
        if age_s <= 0:
            exc["nonpositive"] += 1
            continue
        out.append({"vid": v, "arm": o["arm"], "alive": 1 if o["state"] == "RETRIEVABLE" else 0,
                    "created": T_REF - age_s, "age_y": age_s / YEAR_S})
    return out, exc, d


def main():
    sources = ["ledger/run-2026-08-11T1124Z.json"] + sorted(
        glob.glob("expansion-111/baseline-run*.json"))
    sources = [s for s in sources if os.path.exists(s)]

    seen, rows, per_source = set(), [], []
    for s in sources:
        r, exc, d = rows_from(s)
        fresh = [x for x in r if x["vid"] not in seen]
        for x in fresh:
            seen.add(x["vid"])
        rows.extend(fresh)
        per_source.append({"file": s, "run_id": d.get("run_id"),
                           "run_utc_start": d.get("run_utc_start"),
                           "vantage_asn": d.get("vantage", {}).get("asn"),
                           "observations": len(d["observations"]),
                           "analysable_new": len(fresh), "excluded": exc})

    live = sum(r["alive"] for r in rows)
    out = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "governing_intervals": D,
           "sources": per_source,
           "union": {"n": len(rows), "retrievable": live,
                     "fraction": live / len(rows),
                     "mean_age_years": sum(r["age_y"] for r in rows) / len(rows)}}

    # vantage guard: every run must share one autonomous system or the runs are flagged
    asns = {p["vantage_asn"] for p in per_source}
    out["vantage_guard"] = {"autonomous_systems": sorted(a for a in asns if a),
                            "verdict": "COMPARABLE" if len(asns) == 1 else
                                       "FLAGGED — vantage moved between runs"}

    best, curve = pa.fit(rows)
    klo, khi = pa.profile_ci(curve, best)
    k, lam = best[0], best[1]
    E = pa.expected_transitions(rows, lam, k, days=D)
    out["fit_expanded"] = {"k": k, "k_ci95": [klo, khi], "lambda_per_year": lam,
                           "ci_excludes_1": not (klo <= 1 <= khi)}
    out["power_expanded"] = {"live": live, "E": E, "p_zero": math.exp(-E),
                             "likelihood_ratio": 1 / math.exp(-E)}

    # the same quantities on session 110's corpus alone, for the comparison
    base_rows, _, _ = rows_from("ledger/run-2026-08-11T1124Z.json")
    bbest, bcurve = pa.fit(base_rows)
    bE = pa.expected_transitions(base_rows, bbest[1], bbest[0], days=D)
    out["power_before_expansion"] = {
        "live": sum(r["alive"] for r in base_rows), "k": bbest[0],
        "lambda_per_year": bbest[1], "E": bE, "p_zero": math.exp(-bE),
        "likelihood_ratio": 1 / math.exp(-bE)}

    # the target the audit named
    need_E = -math.log(0.05)
    out["target"] = {"p_zero_target": 0.05, "E_needed": need_E,
                     "fraction_of_target_reached": E / need_E,
                     "further_live_identifiers_needed":
                         max(0, int(math.ceil(live * (need_E / E - 1)))) if E > 0 else None}

    # STANDING METHOD RULE: sub-window refits, K3 scored against every specification
    def yr(r):
        return time.gmtime(r["created"]).tm_year
    out["sub_window_refits"] = []
    for label, sub in (("pooled", rows),
                       ("recent 2023-2026", [r for r in rows if yr(r) >= 2023]),
                       ("old 2018-2022", [r for r in rows if yr(r) < 2023])):
        if len(sub) < 50:
            out["sub_window_refits"].append({"window": label, "n": len(sub),
                                             "fitted": False})
            continue
        b, c = pa.fit(sub)
        lo, hi = pa.profile_ci(c, b)
        out["sub_window_refits"].append({
            "window": label, "n": len(sub),
            "deaths": len(sub) - sum(r["alive"] for r in sub),
            "k": b[0], "k_ci95": [lo, hi], "lambda_per_year": b[1],
            "ci_includes_1": lo <= 1 <= hi})
    fired = [w for w in out["sub_window_refits"]
             if w.get("fitted", True) and w.get("ci_includes_1")]
    out["K3_across_specifications"] = {
        "specifications_run": len(out["sub_window_refits"]),
        "specifications_whose_CI_includes_1": [w["window"] for w in fired],
        "verdict": ("K3 FIRES on at least one specification — shape not determined across "
                    "specifications; power figures published as a range"
                    if fired else "K3 does not fire on any specification run")}

    json.dump(out, open("power-audit-expanded.json", "w"), indent=2)

    print(f"sources: {len(sources)}")
    for p in per_source:
        print(f"  {p['file']}  obs={p['observations']:5d}  new analysable={p['analysable_new']:5d}"
              f"  asn={p['vantage_asn']}")
    print(f"vantage guard: {out['vantage_guard']['verdict']}")
    u = out["union"]
    print(f"union: n={u['n']}  retrievable={u['retrievable']} ({u['fraction']:.4f})"
          f"  mean age={u['mean_age_years']:.3f}y")
    b4 = out["power_before_expansion"]
    print(f"BEFORE: live={b4['live']}  k={b4['k']:.4f} lam={b4['lambda_per_year']:.5f}"
          f"  E={b4['E']:.4f}  P0={b4['p_zero']:.4f}  LR={b4['likelihood_ratio']:.2f}:1")
    f, p = out["fit_expanded"], out["power_expanded"]
    print(f"AFTER : live={p['live']}  k={f['k']:.4f} CI[{f['k_ci95'][0]:.4f},{f['k_ci95'][1]:.4f}]"
          f" lam={f['lambda_per_year']:.5f}  E={p['E']:.4f}  P0={p['p_zero']:.4f}"
          f"  LR={p['likelihood_ratio']:.2f}:1")
    t = out["target"]
    print(f"target E for P0<=0.05 = {t['E_needed']:.3f};  reached "
          f"{t['fraction_of_target_reached']*100:.1f}% of it;  still short by "
          f"{t['further_live_identifiers_needed']} live identifiers")
    print("sub-window refits (the standing method rule):")
    for w in out["sub_window_refits"]:
        if w.get("fitted", True):
            print(f"  {w['window']:<18} n={w['n']:5d} deaths={w['deaths']:4d} k={w['k']:.4f}"
                  f" CI[{w['k_ci95'][0]:.4f},{w['k_ci95'][1]:.4f}] includes1={w['ci_includes_1']}")
    print("K3:", out["K3_across_specifications"]["verdict"])


if __name__ == "__main__":
    main()
