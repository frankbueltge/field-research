#!/usr/bin/env python3
"""D1 of the object question: what the series can still yield before the reading day.

`PREREGISTRATION-112.md` §0a fixes this test before any of today's numbers exist. It asks one
thing: **over the arc's whole remaining life — 2026-08-12 through 2026-09-05, 24 daily intervals —
how many dated transitions does the corpus as it stands expect to produce?** Not over the
seven-interval kill window, which is a promise about a criterion; over the time this arc actually
has.

The rule, written down before the answer:

    E >= 3 under the LEAST favourable specification  -> the series can carry an artifact of its own
    E <  1 under the MOST  favourable specification  -> it cannot, whatever else is true of it
    otherwise                                        -> real, but not the sole object

Everything is imported from `power_audit.py` — the same fitter, the same dating rule, the same
exclusions, the same hazard — so this figure and the seven-interval figures are comparable by
construction rather than by assertion. The specifications are exactly the ones session 111's
cohort-invariance rule produced (`power-audit-expanded-range.json`): the pooled MLE, both profile
bounds, and the two sub-window fits with their own bounds. K3 fired there, so the governing answer
here is a **range** as well.
"""
import importlib.util
import json
import math
import time

spec = importlib.util.spec_from_file_location("pa", "power_audit.py")
pa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pa)

spec2 = importlib.util.spec_from_file_location("re_", "recompute_expanded.py")
re_ = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(re_)

D_REMAINING = 24        # 2026-08-12 .. 2026-09-05 inclusive of both endpoints as run days
D_WINDOW = 7            # the pre-registered kill window, for the side-by-side


def main():
    rows, exc, _ = re_.rows_from("ledger/baseline-union.json")
    live = sum(r["alive"] for r in rows)

    ks = sorted(float(k) for k in json.load(open("power-audit-expanded-range.json")))
    specs = []
    for k in ks:
        lam, ll = pa.fit_lambda(rows, k)
        specs.append({
            "k": k, "lambda_per_year": lam,
            "E_window_7": pa.expected_transitions(rows, lam, k, days=D_WINDOW),
            "E_remaining_24": pa.expected_transitions(rows, lam, k, days=D_REMAINING),
        })
    for s in specs:
        s["p_zero_remaining"] = math.exp(-s["E_remaining_24"])
        s["expected_events_per_interval"] = s["E_remaining_24"] / D_REMAINING

    lo = min(s["E_remaining_24"] for s in specs)
    hi = max(s["E_remaining_24"] for s in specs)
    verdict = ("SERIES CAN CARRY AN ARTIFACT OF ITS OWN — E >= 3 under the least favourable "
               "specification" if lo >= 3 else
               "SERIES CANNOT BE THE OBJECT — E < 1 under the most favourable specification"
               if hi < 1 else
               "REAL BUT NOT THE SOLE OBJECT — the range straddles the thresholds")

    out = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "population": {"file": "ledger/baseline-union.json", "analysable": len(rows),
                          "live_dated": live, "excluded": exc,
                          "note": ("The dated population, on power_audit's own rule: 19-digit "
                                   "identifiers with a positive decoded age, B-truncated and "
                                   "INDETERMINATE excluded. It is smaller than the live corpus "
                                   "because two retrievable identifiers do not date.")},
           "intervals": {"remaining_to_reading_day": D_REMAINING, "kill_window": D_WINDOW,
                         "reading_day": "2026-09-05"},
           "specifications": specs,
           "range_E_remaining": [lo, hi],
           "rule": {"artifact_threshold_least_favourable": 3, "cannot_threshold_most_favourable": 1},
           "D1_verdict": verdict}
    json.dump(out, open("d1-yield.json", "w"), indent=2)

    print(f"population: {len(rows)} dated analysable, {live} live")
    print(f"{'k':>8} {'lambda/yr':>10} {'E(7)':>8} {'E(24)':>8} {'P0(24)':>8} {'events/day':>11}")
    for s in specs:
        print(f"{s['k']:8.4f} {s['lambda_per_year']:10.5f} {s['E_window_7']:8.4f} "
              f"{s['E_remaining_24']:8.4f} {s['p_zero_remaining']:8.4f} "
              f"{s['expected_events_per_interval']:11.4f}")
    print(f"\nE over the remaining 24 intervals: {lo:.3f} to {hi:.3f}")
    print("D1:", verdict)


if __name__ == "__main__":
    main()
