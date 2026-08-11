#!/usr/bin/env python3
"""
Cohort-invariance robustness check: refit the Weibull shape/scale using only
recent-cohort data (2023-2026: less time for arm-A link pruning and citation
attrition to have acted) vs. the full 2018-2026 pool the session used, and see
how much k, lambda, and the headline E move.
"""
import json, math, calendar, time

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
        rows.append({"alive": 1 if o["state"]=="RETRIEVABLE" else 0, "age_y": age_s/YEAR_S,
                     "year": time.gmtime(created).tm_year})
    return rows

rows = load()

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
        if fc>fd: b,d,fd=d,c,fc; c=b-gr*(b-a); fc=f(c)
        else: a,c,fc=c,d,fd; d=a+gr*(b-a); fd=f(d)
        if b-a<1e-10: break
    return (a+b)/2

def fit_lambda(rows,k,lo=1e-6,hi=5.0):
    g=lambda ll: loglik_weibull(rows, math.exp(ll), k)
    loglam=golden(g, math.log(lo), math.log(hi))
    return math.exp(loglam), loglik_weibull(rows, math.exp(loglam), k)

def fit(rows, k_lo=0.05, k_hi=6.0, steps=1500):
    best=None; curve=[]
    for i in range(steps+1):
        k=math.exp(math.log(k_lo)+(math.log(k_hi)-math.log(k_lo))*i/steps)
        lam,ll=fit_lambda(rows,k)
        curve.append((k,lam,ll))
        if best is None or ll>best[2]: best=(k,lam,ll)
    return best,curve

def profile_ci(curve,best,crit=3.841458821):
    thr=best[2]-crit/2
    ks=[k for (k,_,ll) in curve if ll>=thr]
    return (min(ks),max(ks)) if ks else (None,None)

def h_day(t,lam,k): return k*(lam**k)*(t**(k-1))/365.25

for label, subset in [
    ("FULL (2018-2026, session's own set)", rows),
    ("RECENT ONLY (2023-2026)", [r for r in rows if r["year"]>=2023]),
    ("OLD ONLY (2018-2022)", [r for r in rows if r["year"]<=2022]),
]:
    n=len(subset); alive=sum(r["alive"] for r in subset)
    best,curve=fit(subset)
    klo,khi=profile_ci(curve,best)
    k,lam,ll=best
    live_sub=[r for r in subset if r["alive"]]
    E = sum(D_INTERVALS*h_day(r["age_y"],lam,k) for r in live_sub)
    print(f"{label}")
    print(f"  n={n} alive={alive} ({alive/n:.4f})")
    print(f"  k={k:.4f} CI95=[{klo:.4f},{khi:.4f}]  lambda={lam:.5f}/yr")
    print(f"  E on this subset's own live pop (n={len(live_sub)}) = {E:.4f}  P(zero)={math.exp(-E):.4f}")
    print()
