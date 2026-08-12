#!/usr/bin/env python3
"""The window's arithmetic assumed seven FULL intervals. Interval 1 was not one.

Committed at session 112 as condition 1 of `INTERLOCUTOR-4.md`: the exposure correction in
`INCREMENT-2.md` §3a was computed in a session heredoc, which made it the one set of headline
figures in a document whose own methodological claim is that every figure comes from a committed
script. The adversary reproduced the numbers independently (its own weighting gave 5.82–14.93
against the published 5.83–14.96) — so the defect was traceability, not correctness, and this file
closes it rather than changing anything.

WHAT THE CORRECTION IS. The corpus was baselined at staggered times on 2026-08-11 — arms A and B
at 11:24Z, the session-111 expansion arms at 22:31Z, 22:51Z and 23:05Z — while the day-2 run began
at 03:40Z on the 12th. Per-identifier exposure over interval 1 is therefore 0.191 to 0.678 days,
not 1.0. Session 111 published the seven-interval window as 6.6 : 1 to 18.0 : 1 on the assumption
of seven full days; the honest figure sums interval 1's actual exposure and six full intervals.

The fitter, the dating rule, the exclusions and the hazard are `power_audit.py`'s, imported rather
than re-implemented, so the corrected figures and the published ones differ only in exposure.
"""
import calendar
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

BASE = "ledger/baseline-union.json"
DAY2 = "ledger/run-2026-08-12T0341Z.json"
REMAINING_FULL_INTERVALS = 6      # 12->13 ... 17->18, once interval 1 is counted at its own length


def main():
    base = json.load(open(BASE))
    run = json.load(open(DAY2))
    starts = {c["path"]: calendar.timegm(time.strptime(c["start"], "%Y-%m-%dT%H:%M:%SZ"))
              for c in base["components"]}
    t2 = calendar.timegm(time.strptime(run["run_utc_start"], "%Y-%m-%dT%H:%M:%SZ"))
    exposure = {str(o["vid"]): (t2 - starts[o["baseline_from"]]) / 86400.0
                for o in base["observations"]}

    rows, _, _ = re_.rows_from(BASE)                 # the dated population the fit uses
    live = [r for r in rows if r["alive"]]
    published = json.load(open("power-audit-expanded-range.json"))

    ident_days = sum(exposure[r["vid"]] for r in live)
    out = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "exposure": {"identifier_days_interval_1": ident_days,
                        "identifier_days_if_full_day": len(live),
                        "fraction_of_a_full_interval": ident_days / len(live),
                        "per_identifier_days_min": min(exposure[r["vid"]] for r in live),
                        "per_identifier_days_max": max(exposure[r["vid"]] for r in live)},
           "specifications": {}}

    for kk in sorted(published, key=float):
        k = float(kk)
        lam, _ = pa.fit_lambda(rows, k)
        e1 = sum(exposure[r["vid"]] * pa.hazard_per_day(lam, k, r["age_y"]) for r in live)
        eday = sum(pa.hazard_per_day(lam, k, r["age_y"]) for r in live)
        ecorr = e1 + REMAINING_FULL_INTERVALS * eday
        out["specifications"][kk] = {
            "lambda": lam, "E_interval1": e1, "E_per_full_day": eday,
            "E_window_corrected": ecorr, "p_zero": math.exp(-ecorr),
            "p_at_least_one": 1 - math.exp(-ecorr),
            "LR_corrected": 1 / math.exp(-ecorr),
            "E_window_published": published[kk]["E"],
            "LR_published": published[kk]["LR"]}

    lrs = [v["LR_corrected"] for v in out["specifications"].values()]
    p1s = [v["p_at_least_one"] for v in out["specifications"].values()]
    out["governing_range_corrected"] = [min(lrs), max(lrs)]
    out["governing_range_published_session_111"] = [6.59677036921249, 17.96785154173053]
    out["p_at_least_one_over_window"] = [min(p1s), max(p1s)]
    out["direction"] = "against the arc — the window is worth less than session 111 published"
    json.dump(out, open("window-exposure-correction.json", "w"), indent=1)

    e = out["exposure"]
    print(f"interval 1 exposure: {e['identifier_days_interval_1']:.1f} identifier-days against "
          f"{e['identifier_days_if_full_day']} for a full interval "
          f"({e['fraction_of_a_full_interval']:.3f} of a day); per identifier "
          f"{e['per_identifier_days_min']:.3f}–{e['per_identifier_days_max']:.3f} days")
    print(f"{'k':>8} {'E published':>12} {'E corrected':>12} {'LR pub':>9} {'LR corr':>9}")
    for kk, v in out["specifications"].items():
        print(f"{float(kk):8.4f} {v['E_window_published']:12.4f} {v['E_window_corrected']:12.4f} "
              f"{v['LR_published']:9.2f} {v['LR_corrected']:9.2f}")
    print(f"\ncorrected governing range: {min(lrs):.2f} : 1 to {max(lrs):.2f} : 1")
    print(f"published at session 111:  6.60 : 1 to 17.97 : 1")
    print(f"P(at least one transition over the window): {min(p1s):.4f} to {max(p1s):.4f}")


if __name__ == "__main__":
    main()
