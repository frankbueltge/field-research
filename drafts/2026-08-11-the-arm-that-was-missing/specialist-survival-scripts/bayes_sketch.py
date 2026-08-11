#!/usr/bin/env python3
"""
Q5 sketch: does honestly propagating parameter uncertainty (instead of
plugging in the point MLE) move P(zero) and the resulting likelihood ratio,
and in which direction? Uses the profile-likelihood curve already computed
for (k, lambda) as an (improper-flat-prior) importance-weighted approximation
to the posterior -- explicitly labelled as a sketch, not a rigorous Bayesian
analysis (no proper prior elicited; this is illustrative of DIRECTION and
ROUGH MAGNITUDE only).
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

def loglik_weibull(rows, lam, k):
    if lam <= 0 or k <= 0: return -1e18
    ll = 0.0
    for r in rows:
        x = (lam*r["age_y"])**k
        if x > 700: x = 700.0
        if r["alive"]: ll -= x
        else:
            if x < 1e-12: return -1e18
            ll += math.log1p(-math.exp(-x)) if x < 30 else 0.0
    return ll

def golden(f, lo, hi, iters=150):
    gr=(math.sqrt(5)-1)/2
    a,b=lo,hi
    c,d=b-gr*(b-a),a+gr*(b-a)
    fc,fd=f(c),f(d)
    for _ in range(iters):
        if fc>fd:
            b,d,fd=d,c,fc; c=b-gr*(b-a); fc=f(c)
        else:
            a,c,fc=c,d,fd; d=a+gr*(b-a); fd=f(d)
        if b-a<1e-10: break
    return (a+b)/2

def fit_lambda(rows,k,lo=1e-6,hi=5.0):
    g=lambda ll: loglik_weibull(rows, math.exp(ll), k)
    loglam=golden(g, math.log(lo), math.log(hi))
    lam=math.exp(loglam)
    return lam, loglik_weibull(rows,lam,k)

def h_weibull_day(t,lam,k):
    return k*(lam**k)*(t**(k-1))/365.25

steps=1500
k_lo,k_hi=0.05,6.0
curve=[]
for i in range(steps+1):
    k = math.exp(math.log(k_lo)+(math.log(k_hi)-math.log(k_lo))*i/steps)
    lam, ll = fit_lambda(rows,k)
    curve.append((k,lam,ll))
ll_max = max(c[2] for c in curve)

# weighted average of P(zero|k,lambda(k)) under the profile-likelihood "posterior"
# restricted to a broad, defensible support -- k in [0.05,6] (already very wide)
num_p0 = 0.0
num_E  = 0.0
den = 0.0
for k,lam,ll in curve:
    w = math.exp(ll-ll_max)
    if w < 1e-12: continue
    E = sum(D_INTERVALS*h_weibull_day(r["age_y"],lam,k) for r in live_rows)
    p0 = math.exp(-E)
    num_p0 += w*p0
    num_E  += w*E
    den    += w

Ep0_weighted = num_p0/den
E_weighted = num_E/den

E_point = 1.309048  # session's point estimate (reproduced above)
p0_point = math.exp(-E_point)

print("=== Q5 sketch: plug-in point estimate vs profile-weighted average ===")
print(f"P(zero) at point MLE (k=0.696, session's number)      = {p0_point:.4f}")
print(f"E_theta[ P(zero|theta) ] over the profile-likelihood   = {Ep0_weighted:.4f}")
print(f"  (weight w(k) = exp(loglik(k) - loglik_max), i.e. an improper-flat-prior-on-k")
print(f"   importance sketch -- NOT a proper posterior; illustrative of direction only)")
print(f"ratio: weighted/point = {Ep0_weighted/p0_point:.4f}")
print()
print("Jensen's-inequality direction check: exp(-E) is convex in E, so averaging over")
print("parameter uncertainty should push P(zero) UP relative to the point estimate,")
print(f"which weakens (not strengthens) the case for churn. Observed direction: "
      f"{'UP (weaker churn signal)' if Ep0_weighted>p0_point else 'DOWN (stronger churn signal)'}")

# LR framing recompute
print("\n=== LR framing ===")
print(f"LR (session's framing, point-vs-point) = 1 / {p0_point:.4f} = {1/p0_point:.3f} : 1")
print(f"LR using profile-weighted P(zero)       = 1 / {Ep0_weighted:.4f} = {1/Ep0_weighted:.3f} : 1")
