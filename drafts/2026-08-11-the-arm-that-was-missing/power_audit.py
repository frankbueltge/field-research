#!/usr/bin/env python3
"""Power audit of the retrievability ledger's pre-registered seven-day window.

Session 111, 2026-08-11. Method fixed in PREREGISTRATION-111.md before this file was
written to produce any figure. Pure standard library: no numpy, no scipy on this machine.

Question: given the disappearance rate implied by the corpus we already hold, would the
pre-registered seven-run window produce any state transition at all if that rate were real?

Input : ledger/run-2026-08-11T1124Z.json  (session 110, 2,904 observations)
Output: power-audit.json  (every figure this session publishes)
"""

import json
import math
import sys

RUN = "ledger/run-2026-08-11T1124Z.json"
OUT = "power-audit.json"

# Age reference: the midpoint of run 2, fixed in the pre-registration.
T_REF = 1786_000_000  # placeholder, replaced below by the computed epoch
# 2026-08-11T12:00:00Z as a unix timestamp, computed rather than asserted:
import calendar
T_REF = calendar.timegm((2026, 8, 11, 12, 0, 0, 0, 0, 0))

YEAR_S = 365.25 * 86400.0
D_INTERVALS = 6  # seven daily runs bind six one-day intervals


# ---------------------------------------------------------------- data loading

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
        st = o["state"]
        if st == "INDETERMINATE":
            excluded["indeterminate"] += 1
            continue
        vid = str(o["vid"])
        if len(vid) != 19:
            # PREREGISTRATION-111 §2: the id>>32 dating rule holds only in the modern
            # scheme; session 110 proved it breaks outside it.
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
            "alive": 1 if st == "RETRIEVABLE" else 0,
            "created": created,
            "age_y": age_s / YEAR_S,
        })
    return d, rows, excluded


# ------------------------------------------------------------------ statistics

def wilson(k, n, z=1.959963985):
    if n == 0:
        return (None, None)
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


def loglik(rows, lam, k):
    """Weibull survival S(t) = exp(-(lam*t)^k), Bernoulli outcome per identifier."""
    if lam <= 0 or k <= 0:
        return -1e18
    ll = 0.0
    for r in rows:
        x = (lam * r["age_y"]) ** k
        if x > 700:
            x = 700.0
        if r["alive"]:
            ll -= x
        else:
            # log(1 - exp(-x)), numerically safe for small x
            if x < 1e-12:
                return -1e18
            ll += math.log1p(-math.exp(-x)) if x < 30 else 0.0
    return ll


def fit_lambda(rows, k, lo=1e-5, hi=5.0):
    """Golden-section maximisation of the log-likelihood in lambda at fixed k."""
    gr = (math.sqrt(5) - 1) / 2
    a, b = math.log(lo), math.log(hi)
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = loglik(rows, math.exp(c), k), loglik(rows, math.exp(d), k)
    for _ in range(120):
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = loglik(rows, math.exp(c), k)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = loglik(rows, math.exp(d), k)
        if b - a < 1e-9:
            break
    lam = math.exp((a + b) / 2)
    return lam, loglik(rows, lam, k)


def fit(rows, k_lo=0.05, k_hi=6.0, steps=1200):
    """Profile over k on a log grid; return MLE and the profile curve."""
    curve = []
    best = None
    for i in range(steps + 1):
        k = math.exp(math.log(k_lo) + (math.log(k_hi) - math.log(k_lo)) * i / steps)
        lam, ll = fit_lambda(rows, k)
        curve.append((k, lam, ll))
        if best is None or ll > best[2]:
            best = (k, lam, ll)
    return best, curve


def profile_ci(curve, best, crit=3.841458821):
    """{k : 2(LLmax - LLprofile(k)) <= 3.841} — the 95% profile-likelihood interval."""
    thr = best[2] - crit / 2
    ks = [k for (k, _, ll) in curve if ll >= thr]
    if not ks:
        return (None, None)
    return (min(ks), max(ks))


# --------------------------------------------------------------- the power part

def hazard_per_day(lam, k, t_y):
    """Weibull hazard in years, converted to a per-day rate."""
    return k * (lam ** k) * (t_y ** (k - 1)) / 365.25


def expected_transitions(rows, lam, k, days=D_INTERVALS):
    """Sum the per-day hazard over identifiers currently retrievable."""
    e = 0.0
    for r in rows:
        if r["alive"]:
            e += days * hazard_per_day(lam, k, r["age_y"])
    return e


def n_needed(rows, lam, k, days=D_INTERVALS, target_p_zero=0.05):
    """Multiplier on the live corpus that drives P(zero) to the target."""
    e = expected_transitions(rows, lam, k, days)
    if e <= 0:
        return None
    need_e = -math.log(target_p_zero)
    live = sum(1 for r in rows if r["alive"])
    return {"multiplier": need_e / e, "live_now": live,
            "live_needed": int(math.ceil(live * need_e / e))}


# ------------------------------------------------------------------------- main

def main():
    raw, rows, excluded = load()
    out = {
        "session": 111,
        "date": "2026-08-11",
        "input": {"file": RUN, "run_id": raw["run_id"],
                  "run_utc_start": raw["run_utc_start"],
                  "run_utc_end": raw["run_utc_end"],
                  "observations_in_file": len(raw["observations"])},
        "age_reference_utc": "2026-08-11T12:00:00Z",
        "excluded": excluded,
        "n_analysed": len(rows),
    }

    live = sum(r["alive"] for r in rows)
    out["overall"] = {
        "n": len(rows), "retrievable": live, "not_retrievable": len(rows) - live,
        "fraction": live / len(rows) if rows else None,
        "mean_age_years": sum(r["age_y"] for r in rows) / len(rows) if rows else None,
    }

    # ---- K1
    out["K1"] = {
        "threshold": 1500, "value": live,
        "fires": live < 1500,
        "meaning": "fewer than 1,500 determinate, datable, currently-retrievable "
                   "identifiers would make the power question moot",
    }
    if out["K1"]["fires"]:
        json.dump(out, open(OUT, "w"), indent=2)
        print("K1 FIRES — stopping per the pre-registration.")
        return

    # ---- cohort table (yearly, per arm and pooled)
    import time
    def year_of(r):
        return time.gmtime(r["created"]).tm_year

    cohorts = {}
    for r in rows:
        y = year_of(r)
        for key in ("pooled", r["arm"]):
            c = cohorts.setdefault(key, {}).setdefault(y, [0, 0])
            c[0] += 1
            c[1] += r["alive"]
    out["cohorts"] = {}
    for key, d in sorted(cohorts.items()):
        out["cohorts"][key] = []
        for y in sorted(d):
            n, a = d[y]
            lo, hi = wilson(a, n)
            out["cohorts"][key].append({
                "year": y, "n": n, "retrievable": a, "fraction": a / n,
                "wilson95": [lo, hi],
                "mean_age_years": None,
            })
    for c in out["cohorts"]["pooled"]:
        ages = [r["age_y"] for r in rows if year_of(r) == c["year"]]
        c["mean_age_years"] = sum(ages) / len(ages)

    # ---- K2
    big = [c for c in out["cohorts"]["pooled"] if c["n"] >= 100]
    out["K2"] = {
        "threshold": "6 yearly cohorts with n >= 100",
        "value": len(big), "fires": len(big) < 6,
        "cohorts_over_100": [c["year"] for c in big],
    }

    # ---- naive constant-hazard estimate
    mean_age = out["overall"]["mean_age_years"]
    s_bar = out["overall"]["fraction"]
    lam_naive = -math.log(s_bar) / mean_age
    out["naive_constant_hazard"] = {
        "lambda_per_year": lam_naive,
        "method": "-ln(S_bar)/t_bar — reported for comparison and labelled naive",
        "daily": lam_naive / 365.25,
        "expected_transitions_6_intervals": live * D_INTERVALS * lam_naive / 365.25,
    }

    # ---- Weibull ML fit, pooled and per arm
    out["fits"] = {}
    for key, sub in (("pooled", rows),
                     ("A", [r for r in rows if r["arm"] == "A"]),
                     ("B", [r for r in rows if r["arm"] == "B"])):
        if len(sub) < 30:
            out["fits"][key] = {"n": len(sub), "fitted": False,
                                "reason": "fewer than 30 observations"}
            continue
        best, curve = fit(sub)
        klo, khi = profile_ci(curve, best)
        out["fits"][key] = {
            "n": len(sub),
            "deaths": len(sub) - sum(r["alive"] for r in sub),
            "fitted": True,
            "k": best[0], "lambda_per_year": best[1], "loglik": best[2],
            "k_ci95_profile": [klo, khi],
            "median_life_years": (math.log(2) ** (1 / best[0])) / best[1],
            "annual_hazard_at_mean_age": best[0] * (best[1] ** best[0])
                                         * ((sum(r["age_y"] for r in sub) / len(sub))
                                            ** (best[0] - 1)),
        }
        if key == "pooled":
            out["_pooled_curve_sample"] = [
                {"k": k, "lambda": l, "loglik": ll}
                for (k, l, ll) in curve[::60]
            ]

    p = out["fits"]["pooled"]

    # ---- K3
    klo, khi = p["k_ci95_profile"]
    out["K3"] = {
        "k_ci95": [klo, khi],
        "includes_1": (klo is not None and klo <= 1.0 <= khi),
        "wider_than_0.5_2.0": (klo is not None and (klo < 0.5 or khi > 2.0)),
        "fires": (klo is not None and klo <= 1.0 <= khi and (klo < 0.5 or khi > 2.0)),
    }

    # ---- expected transitions and P(zero)
    e_fit = expected_transitions(rows, p["lambda_per_year"], p["k"])
    out["power"] = {
        "intervals_days": D_INTERVALS,
        "live_identifiers": live,
        "expected_transitions_fitted": e_fit,
        "p_zero_fitted": math.exp(-e_fit),
        "expected_transitions_naive": out["naive_constant_hazard"][
            "expected_transitions_6_intervals"],
        "p_zero_naive": math.exp(-out["naive_constant_hazard"][
            "expected_transitions_6_intervals"]),
        "same_day_pair_hours": 7.3,
        "expected_transitions_in_the_pair_already_run":
            expected_transitions(rows, p["lambda_per_year"], p["k"], days=7.3 / 24.0),
    }

    # ---- K4
    out["K4"] = {
        "threshold": 10, "value": e_fit, "fires": e_fit > 10,
        "meaning": "above 10 expected transitions the design is amply powered and "
                   "this session's premise is wrong",
    }

    # ---- sensitivity band
    band = []
    for k_fix in (0.5, 0.75, 1.0, p["k"]):
        lam_k, _ = fit_lambda(rows, k_fix)
        e = expected_transitions(rows, lam_k, k_fix)
        band.append({
            "k": k_fix, "lambda_per_year": lam_k,
            "expected_transitions": e, "p_zero": math.exp(-e),
            "corpus_for_p_zero_0.05": n_needed(rows, lam_k, k_fix),
            "days_for_p_zero_0.05_at_current_corpus":
                (-math.log(0.05) / (e / D_INTERVALS)) if e > 0 else None,
        })
    out["sensitivity"] = band

    # ---- the arm comparison behind P6: age gradient per arm
    out["age_gradient_by_arm"] = {}
    for key in ("A", "B"):
        f = out["fits"].get(key, {})
        if f.get("fitted"):
            out["age_gradient_by_arm"][key] = {
                "k": f["k"], "k_ci95": f["k_ci95_profile"],
                "lambda_per_year": f["lambda_per_year"],
                "annual_hazard_at_mean_age": f["annual_hazard_at_mean_age"],
            }

    json.dump(out, open(OUT, "w"), indent=2)

    # ---- human-readable summary to stdout
    print(f"n analysed        : {len(rows)}  (excluded: {excluded})")
    print(f"retrievable       : {live} / {len(rows)} = {live/len(rows):.4f}")
    print(f"mean age (years)  : {mean_age:.3f}")
    print(f"naive lambda/yr   : {lam_naive:.5f}")
    print(f"Weibull pooled    : k = {p['k']:.4f}  CI95 [{klo:.4f}, {khi:.4f}]"
          f"   lambda = {p['lambda_per_year']:.5f}/yr")
    print(f"median life (yr)  : {p['median_life_years']:.2f}")
    print(f"E[transitions] fit: {e_fit:.4f}   P(zero) = {math.exp(-e_fit):.4f}")
    print(f"E[transitions] nai: {out['naive_constant_hazard']['expected_transitions_6_intervals']:.4f}")
    print("K1 fires:", out["K1"]["fires"], "| K2 fires:", out["K2"]["fires"],
          "| K3 fires:", out["K3"]["fires"], "| K4 fires:", out["K4"]["fires"])
    print("\ncohort table (pooled):")
    for c in out["cohorts"]["pooled"]:
        print(f"  {c['year']}  n={c['n']:5d}  alive={c['retrievable']:5d}  "
              f"{c['fraction']:.4f}  [{c['wilson95'][0]:.4f}, {c['wilson95'][1]:.4f}]  "
              f"age={c['mean_age_years']:.2f}y")
    print("\nsensitivity:")
    for b in band:
        nn = b["corpus_for_p_zero_0.05"]
        print(f"  k={b['k']:.4f} lam={b['lambda_per_year']:.5f}  E={b['expected_transitions']:.3f}"
              f"  P0={b['p_zero']:.4f}  need_live={nn['live_needed'] if nn else None}"
              f"  or days={b['days_for_p_zero_0.05_at_current_corpus']:.0f}")
    print("\nper-arm fits:")
    for key in ("A", "B"):
        f = out["fits"].get(key, {})
        if f.get("fitted"):
            print(f"  {key}: n={f['n']} deaths={f['deaths']} k={f['k']:.4f} "
                  f"CI[{f['k_ci95_profile'][0]:.4f},{f['k_ci95_profile'][1]:.4f}] "
                  f"lam={f['lambda_per_year']:.5f} h(mean age)={f['annual_hazard_at_mean_age']:.5f}/yr")
        else:
            print(f"  {key}: not fitted — {f.get('reason')}")


if __name__ == "__main__":
    main()
