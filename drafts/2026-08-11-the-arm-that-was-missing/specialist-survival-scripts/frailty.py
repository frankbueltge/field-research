#!/usr/bin/env python3
"""
Frailty extension. Pure stdlib.
Fits:
  (1) Gamma-frailty, constant individual baseline hazard lambda0, frailty
      variance theta (Vaupel-Manton-Stallard 1979 form):
        S(t) = (1 + theta*lambda0*t)^(-1/theta)   [theta->0 => exp(-lambda0 t)]
        marginal hazard h(t) = lambda0 / (1 + theta*lambda0*t)
  (2) Two-point discrete mixture, each subpopulation with its OWN constant
      (exponential) hazard:
        S(t) = p*exp(-lamH*t) + (1-p)*exp(-lamL*t)
        marginal hazard h(t) = [p*lamH*exp(-lamH t) + (1-p)*lamL*exp(-lamL t)] / S(t)
Both are fit by direct maximum likelihood on the SAME current-status
(binary alive/dead at one snapshot) data the session used, then their
marginal hazard functions are evaluated at the exact ages of the 2,320
currently-alive identifiers to get an alternative E, exactly parallel to
the session's own E = sum(D * h(t_i)).
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
N = len(rows)
print(f"n={N}, alive={len(live_rows)}")

def golden_max(f, lo, hi, iters=200):
    gr = (math.sqrt(5)-1)/2
    a,b = lo,hi
    c,d = b-gr*(b-a), a+gr*(b-a)
    fc,fd = f(c),f(d)
    for _ in range(iters):
        if fc>fd:
            b,d,fd = d,c,fc
            c = b-gr*(b-a); fc=f(c)
        else:
            a,c,fc = c,d,fd
            d = a+gr*(b-a); fd=f(d)
        if b-a < 1e-12: break
    x=(a+b)/2
    return x, f(x)

# ---------------------------------------------------------- (1) gamma frailty
def S_gamma_frailty(t, lam0, theta):
    if theta < 1e-9:
        return math.exp(-lam0*t)
    base = 1.0 + theta*lam0*t
    if base <= 0: return 0.0
    return base ** (-1.0/theta)

def loglik_gf(rows, lam0, theta):
    if lam0 <= 0 or theta < 0: return -1e18
    ll = 0.0
    for r in rows:
        S = S_gamma_frailty(r["age_y"], lam0, theta)
        S = min(max(S, 1e-300), 1.0)
        if r["alive"]:
            ll += math.log(S)
        else:
            v = 1.0 - S
            if v <= 0: return -1e18
            ll += math.log(v)
    return ll

def fit_gf(rows, theta_lo=1e-6, theta_hi=20.0, steps=1500, lam_lo=1e-6, lam_hi=5.0):
    curve = []
    best = None
    for i in range(steps+1):
        theta = math.exp(math.log(theta_lo) + (math.log(theta_hi)-math.log(theta_lo))*i/steps)
        loglam, ll = golden_max(lambda ll_: loglik_gf(rows, math.exp(ll_), theta),
                                 math.log(lam_lo), math.log(lam_hi))
        lam0 = math.exp(loglam)
        curve.append((theta, lam0, ll))
        if best is None or ll > best[2]:
            best = (theta, lam0, ll)
    return best, curve

def profile_ci(curve, best, crit=3.841458821):
    thr = best[2]-crit/2
    xs = [x for (x,_,ll) in curve if ll>=thr]
    return (min(xs), max(xs)) if xs else (None,None)

best_gf, curve_gf = fit_gf(rows)
theta_hat, lam0_hat, ll_gf = best_gf
tlo, thi = profile_ci(curve_gf, best_gf)
print("\n=== (1) Gamma-frailty, constant baseline hazard ===")
print(f"theta = {theta_hat:.5f}  (CI95 on theta [{tlo:.5f},{thi:.5f}])")
print(f"lambda0 (baseline/'frail unit' hazard) = {lam0_hat:.5f} /yr")
print(f"loglik = {ll_gf:.4f}   (Weibull loglik was -899.2760, 2 free params either way)")
print(f"AIC gamma-frailty = {2*2-2*ll_gf:.4f}   AIC Weibull = {2*2-2*(-899.2760):.4f}")

def h_gf(lam0, theta, t):
    if theta < 1e-9:
        return lam0/365.25
    return (lam0/(1.0+theta*lam0*t))/365.25

E_gf = sum(D_INTERVALS*h_gf(lam0_hat, theta_hat, r["age_y"]) for r in live_rows)
print(f"E under gamma-frailty marginal hazard = {E_gf:.4f}   P(zero)={math.exp(-E_gf):.4f}")

# what the *individual* (non-selected) hazard would need to be interpreted as:
print(f"NOTE: lambda0 is the hazard of a 'typical' (Z=1) individual under this model.")
print(f"      Individual hazard is CONSTANT at lambda0*Z per unit (not declining);")
print(f"      only the population-average hazard of survivors declines, via selection.")

# ---------------------------------------------------------- (2) two-point mixture
def S_mix(t, p, lamH, lamL):
    return p*math.exp(-lamH*t) + (1-p)*math.exp(-lamL*t)

def loglik_mix(rows, p, lamH, lamL):
    if not (0 < p < 1) or lamH <= 0 or lamL <= 0: return -1e18
    ll = 0.0
    for r in rows:
        S = S_mix(r["age_y"], p, lamH, lamL)
        S = min(max(S, 1e-300), 1.0)
        if r["alive"]:
            ll += math.log(S)
        else:
            v = 1.0-S
            if v <= 0: return -1e18
            ll += math.log(v)
    return ll

def fit_mix(rows, iters=40):
    # block coordinate ascent from multiple starts to avoid local optima
    best_overall = None
    starts = [(0.2,1.0,0.02), (0.1,2.0,0.01), (0.3,0.5,0.03), (0.5,0.3,0.01), (0.05,3.0,0.02)]
    for p0,lamH0,lamL0 in starts:
        p, lamH, lamL = p0, lamH0, lamL0
        for _ in range(iters):
            p,_ = golden_max(lambda pp: loglik_mix(rows, pp, lamH, lamL), 1e-4, 1-1e-4)
            loglamH,_ = golden_max(lambda x: loglik_mix(rows, p, math.exp(x), lamL), math.log(1e-5), math.log(50))
            lamH = math.exp(loglamH)
            loglamL,_ = golden_max(lambda x: loglik_mix(rows, p, lamH, math.exp(x)), math.log(1e-6), math.log(5))
            lamL = math.exp(loglamL)
        ll = loglik_mix(rows, p, lamH, lamL)
        if lamL > lamH:  # canonicalize: H = higher hazard
            lamH, lamL = lamL, lamH
            p = 1-p
        if best_overall is None or ll > best_overall[3]:
            best_overall = (p, lamH, lamL, ll)
    return best_overall

p_hat, lamH_hat, lamL_hat, ll_mix = fit_mix(rows)
print("\n=== (2) Two-point exponential mixture ===")
print(f"p(frail)={p_hat:.4f}  lambda_frail={lamH_hat:.5f}/yr  lambda_durable={lamL_hat:.5f}/yr")
print(f"loglik = {ll_mix:.4f}   AIC (3 params) = {2*3-2*ll_mix:.4f}")

def h_mix(t, p, lamH, lamL):
    S = S_mix(t, p, lamH, lamL)
    num = p*lamH*math.exp(-lamH*t) + (1-p)*lamL*math.exp(-lamL*t)
    return (num/max(S,1e-300))/365.25

E_mix = sum(D_INTERVALS*h_mix(r["age_y"], p_hat, lamH_hat, lamL_hat) for r in live_rows)
print(f"E under two-point-mixture marginal hazard = {E_mix:.4f}   P(zero)={math.exp(-E_mix):.4f}")

print("\n=== SUMMARY: E and P(zero) across the three fitted models ===")
print(f"{'model':30s} {'loglik':>10s} {'AIC':>8s} {'E':>8s} {'P(zero)':>9s}")
print(f"{'Weibull (session)':30s} {-899.2760:10.4f} {2*2-2*(-899.2760):8.4f} {1.3090:8.4f} {0.2701:9.4f}")
print(f"{'Gamma-frailty':30s} {ll_gf:10.4f} {2*2-2*ll_gf:8.4f} {E_gf:8.4f} {math.exp(-E_gf):9.4f}")
print(f"{'Two-point mixture':30s} {ll_mix:10.4f} {2*3-2*ll_mix:8.4f} {E_mix:8.4f} {math.exp(-E_mix):9.4f}")
