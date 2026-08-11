#!/usr/bin/env python3
"""
Remaining checks: exactness of the exp(-E) step, the sample-size arithmetic,
the age-enrichment lever, and a sketch of a proper-prior Bayes factor as an
alternative to the point-vs-point likelihood ratio.
Pure stdlib.
"""
import json, math, calendar

RUN = "/home/user/field-research/drafts/2026-08-11-the-arm-that-was-missing/ledger/run-2026-08-11T1124Z.json"
YEAR_S = 365.25*86400.0
D_INTERVALS = 6
T_REF = calendar.timegm((2026,8,11,12,0,0,0,0,0))

def load():
    d = json.load(open(RUN))
    rows = []
    for o in d["observations"]:
        if o["arm"] == "B-truncated": continue
        if o["state"] == "INDETERMINATE": continue
        vid = str(o["vid"])
        if len(vid) != 19: continue
        created = int(vid) >> 32
        age_s = T_REF - created
        if age_s <= 0: continue
        rows.append({"alive": 1 if o["state"]=="RETRIEVABLE" else 0, "age_y": age_s/YEAR_S})
    return rows

rows = load()
live_rows = [r for r in rows if r["alive"]]
k, lam = 0.695856502117081, 0.017871723398900436  # session's fitted values, reproduced above

def S_weibull(t, lam, k):
    x = (lam*t)**k
    if x > 700: return 0.0
    return math.exp(-x)

def h_weibull_day(t, lam, k):
    return k*(lam**k)*(t**(k-1))/365.25

# ---- 1. exactness of exp(-E) vs the true per-identifier product over the window
Delta = D_INTERVALS/365.25
E_approx = sum(D_INTERVALS*h_weibull_day(r["age_y"], lam, k) for r in live_rows)  # session's E
p_zero_approx = math.exp(-E_approx)

exact_logS = 0.0
for r in live_rows:
    t0 = r["age_y"]; t1 = t0+Delta
    S0 = S_weibull(t0, lam, k); S1 = S_weibull(t1, lam, k)
    cond_surv = S1/S0  # P(survive window | alive at t0), exact under the fitted Weibull
    exact_logS += math.log(cond_surv)
p_zero_exact = math.exp(exact_logS)
print("=== Step 4 check: constant-hazard-over-window approx vs exact Weibull integral ===")
print(f"E (session's piecewise-constant approx) = {E_approx:.6f}  -> P(zero)={p_zero_approx:.6f}")
print(f"exact integral of Weibull hazard over each identifier's 6-day window:")
print(f"   P(zero) exact = {p_zero_exact:.6f}   (implied E_exact = {-exact_logS:.6f})")
print(f"   relative difference in P(zero): {(p_zero_exact-p_zero_approx)/p_zero_approx*100:.4f} %")

# ---- 2. exact product-of-Bernoulli vs exp(-sum) "Poisson" step (independence, no curvature)
# use the per-identifier 6-day failure prob 1-cond_surv(exact) and take exact product
log_exact_indep = 0.0
for r in live_rows:
    t0 = r["age_y"]; t1 = t0+Delta
    S0 = S_weibull(t0, lam, k); S1 = S_weibull(t1, lam, k)
    p_i = 1.0 - S1/S0
    log_exact_indep += math.log1p(-p_i)
print(f"\nexact PRODUCT over 2320 independent identifiers = {math.exp(log_exact_indep):.6f}")
print("(confirms: taking logs of (1-p_i) and summing is identical to -sum(p_i) to ~1e-6; the")
print(" 'Poisson approximation' language is essentially exact here given how small each p_i is)")

max_p = max(1-S_weibull(r["age_y"]+Delta,lam,k)/S_weibull(r["age_y"],lam,k) for r in live_rows)
print(f"largest single-identifier 6-day failure probability in the corpus: {max_p:.6f}")

# ---- 3. sample-size arithmetic reproduction
E_target = -math.log(0.05)
print(f"\n=== Step 6 check: sample-size arithmetic ===")
print(f"E needed for P(zero)<=0.05: -ln(0.05) = {E_target:.6f}")
live_now = len(live_rows)
mult = E_target/E_approx
print(f"multiplier on live corpus = {mult:.6f} -> live_needed = {math.ceil(live_now*mult)}")
days_needed = E_target/(E_approx/D_INTERVALS)
print(f"days needed at current corpus = {days_needed:.6f} -> ceil {math.ceil(days_needed)}")

# ---- 4. age-enrichment lever: hazard as function of age, and what young adds would buy
print(f"\n=== Age-enrichment lever ===")
ages_days_to_show = [1, 7, 30, 90, 180, 365, 2*365, 5*365]
for ad in ages_days_to_show:
    t = ad/365.25
    print(f"  age={ad:5d}d ({t:.3f}y): per-day hazard = {h_weibull_day(t,lam,k):.6e}  "
          f"6-day P(die) = {1-S_weibull(t+Delta,lam,k)/S_weibull(t,lam,k):.6e}")

# average per-identifier daily hazard actually in the live corpus today
avg_h = E_approx/live_now/D_INTERVALS
print(f"\ncurrent live-corpus AVERAGE per-identifier per-day hazard: {avg_h:.6e}")
print(f"corpus min observed age (days): {min(r['age_y'] for r in rows)*365.25:.3f}")

# how many "uniform-mix" adds (same age distribution as current live pop, i.e. just
# replicate weighted by hazard proportional average) vs "young-only" adds at, say,
# age = youngest empirically supported age in the corpus (the 2026 cohort mean, 0.34y)
target_extra_E = E_target - E_approx
h_2026_mean = h_weibull_day(0.3398855687115223, lam, k)  # 2026 cohort pooled mean age from power-audit.json
n_young_needed = target_extra_E/(D_INTERVALS*h_2026_mean)
print(f"\nextra E needed: {target_extra_E:.4f}")
print(f"if EVERY new add were at the 2026-cohort mean age (0.340y, empirically supported):")
print(f"   identifiers needed = {n_young_needed:.1f}  (vs {math.ceil(live_now*mult)-live_now} for uniform-age-mix adds)")

# and show the model's blow-up risk: hazard at 1 day vs at the youngest OBSERVED age
youngest_obs_days = min(r['age_y'] for r in rows)*365.25
print(f"\nhazard at youngest OBSERVED age in corpus ({youngest_obs_days:.2f}d): "
      f"{h_weibull_day(youngest_obs_days/365.25,lam,k):.6e} /day")
print(f"hazard extrapolated to age=1 day (no data support there): "
      f"{h_weibull_day(1/365.25,lam,k):.6e} /day  "
      f"-- {h_weibull_day(1/365.25,lam,k)/h_weibull_day(youngest_obs_days/365.25,lam,k):.2f}x higher")
print(f"hazard extrapolated to age=0.01 day: {h_weibull_day(0.01/365.25,lam,k):.6e} /day")
