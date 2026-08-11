#!/usr/bin/env python3
"""
Specialist review script for session 111's power audit.
Pure standard library. Re-derives the session's own numbers from the raw
ledger file (not from power-audit.json, to catch any transcription error),
then extends into frailty models and exactness checks the session did not run.
"""
import json, math, calendar, time

RUN = "/home/user/field-research/drafts/2026-08-11-the-arm-that-was-missing/ledger/run-2026-08-11T1124Z.json"
YEAR_S = 365.25 * 86400.0
D_INTERVALS = 6
T_REF = calendar.timegm((2026, 8, 11, 12, 0, 0, 0, 0, 0))

def load():
    d = json.load(open(RUN))
    rows = []
    excluded = {"arm_B_truncated": 0, "indeterminate": 0, "not_19_digit": 0, "nonpositive_age": 0}
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
            excluded["not_19_digit"] += 1
            continue
        created = int(vid) >> 32
        age_s = T_REF - created
        if age_s <= 0:
            excluded["nonpositive_age"] += 1
            continue
        rows.append({"vid": vid, "arm": arm, "alive": 1 if st == "RETRIEVABLE" else 0,
                     "created": created, "age_y": age_s / YEAR_S})
    return rows, excluded

rows, excluded = load()
live = sum(r["alive"] for r in rows)
print("=== SANITY: reproduce session's own load ===")
print("n analysed:", len(rows), "excluded:", excluded)
print("live:", live, "frac:", live/len(rows))
print("mean age:", sum(r["age_y"] for r in rows)/len(rows))
print("min age (days):", min(r["age_y"] for r in rows)*365.25)
print("min age among ALIVE (days):", min(r["age_y"] for r in rows if r["alive"])*365.25)
print("max age (years):", max(r["age_y"] for r in rows))

# ---------------------------------------------------------------- Weibull MLE
def loglik_weibull(rows, lam, k):
    if lam <= 0 or k <= 0:
        return -1e18
    ll = 0.0
    for r in rows:
        x = (lam * r["age_y"]) ** k
        if x > 700: x = 700.0
        if r["alive"]:
            ll -= x
        else:
            if x < 1e-12: return -1e18
            ll += math.log1p(-math.exp(-x)) if x < 30 else 0.0
    return ll

def golden(f, lo, hi, iters=200):
    gr = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - gr*(b-a), a + gr*(b-a)
    fc, fd = f(c), f(d)
    for _ in range(iters):
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - gr*(b-a); fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + gr*(b-a); fd = f(d)
        if b - a < 1e-11: break
    return (a+b)/2

def fit_lambda_weibull(rows, k, lo=1e-6, hi=5.0):
    g = lambda logl: loglik_weibull(rows, math.exp(logl), k)
    loglam = golden(g, math.log(lo), math.log(hi))
    lam = math.exp(loglam)
    return lam, loglik_weibull(rows, lam, k)

def fit_weibull(rows, k_lo=0.05, k_hi=6.0, steps=2000):
    curve = []
    best = None
    for i in range(steps+1):
        k = math.exp(math.log(k_lo) + (math.log(k_hi)-math.log(k_lo))*i/steps)
        lam, ll = fit_lambda_weibull(rows, k)
        curve.append((k, lam, ll))
        if best is None or ll > best[2]:
            best = (k, lam, ll)
    return best, curve

def profile_ci(curve, best, crit=3.841458821):
    thr = best[2] - crit/2
    ks = [k for (k,_,ll) in curve if ll >= thr]
    return (min(ks), max(ks)) if ks else (None, None)

best, curve = fit_weibull(rows)
klo, khi = profile_ci(curve, best)
print("\n=== Weibull MLE (reproduction) ===")
print(f"k = {best[0]:.4f}  CI95 [{klo:.4f},{khi:.4f}]  lambda = {best[1]:.5f}  loglik={best[2]:.4f}")

k_fit, lam_fit, ll_fit = best

def hazard_weibull(lam, k, t):
    return k * (lam**k) * (t**(k-1)) / 365.25  # per day

def E_from_hazard(hfun, rows, days=D_INTERVALS):
    return sum(days*hfun(r["age_y"]) for r in rows if r["alive"])

E_fit = E_from_hazard(lambda t: hazard_weibull(lam_fit, k_fit, t), rows)
print(f"E (Weibull point est) = {E_fit:.4f}  P(zero) = {math.exp(-E_fit):.4f}")
print("(session reported E=1.3090, P0=0.2701 -- match check above)")
