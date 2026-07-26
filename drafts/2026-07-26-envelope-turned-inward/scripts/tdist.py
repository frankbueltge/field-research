"""
scripts/tdist.py — PREREGISTRATION.md §4: the Student-t quantile, computed numerically.

Stdlib only (math.lgamma/exp/log + bisection). No table lookup: every t-critical value
used anywhere in this draft is produced by `t_quantile` below, not hardcoded, per §4's
"t critical values are computed, not quoted."

Method: the regularized incomplete beta function I_x(a, b), evaluated by the standard
continued-fraction expansion (Lentz's algorithm, as in Numerical Recipes' `betacf`/`betai`),
gives the two-sided Student-t CDF via the identity

    F(t; df) = 1 - 0.5 * I_{df/(df+t^2)}(df/2, 1/2)   for t >= 0
    F(t; df) = 0.5 * I_{df/(df+t^2)}(df/2, 1/2)        for t < 0

`t_quantile(p, df)` then bisects on t >= 0 for the value solving F(t) = p (only p >= 0.5 is
ever requested by this draft — always the upper/two-sided-0.975 quantile — but the bisection
itself is symmetric and would work for p < 0.5 too, returning a negative t).
"""
import math

_FPMIN = 1e-300
_EPS = 3e-14
_MAXIT = 300


def _betacf(a, b, x):
    """Continued-fraction evaluation used inside the regularized incomplete beta
    function (Lentz's algorithm)."""
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < _FPMIN:
        d = _FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, _MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < _FPMIN:
            d = _FPMIN
        c = 1.0 + aa / c
        if abs(c) < _FPMIN:
            c = _FPMIN
        d = 1.0 / d
        h *= d * c

        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < _FPMIN:
            d = _FPMIN
        c = 1.0 + aa / c
        if abs(c) < _FPMIN:
            c = _FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < _EPS:
            break
    return h


def regularized_incomplete_beta(x, a, b):
    """I_x(a, b), for 0 <= x <= 1, a > 0, b > 0."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    ln_bt = (
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + a * math.log(x) + b * math.log(1.0 - x)
    )
    bt = math.exp(ln_bt)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    else:
        return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_cdf(t, df):
    """Two-sided Student-t CDF, F(t; df) = P(T <= t)."""
    if df <= 0:
        raise ValueError("df must be positive")
    x = df / (df + t * t)
    ibeta = regularized_incomplete_beta(x, df / 2.0, 0.5)
    if t >= 0:
        return 1.0 - 0.5 * ibeta
    else:
        return 0.5 * ibeta


def t_quantile(p, df, lo=0.0, hi=1.0, tol=1e-12, max_iter=200):
    """Bisection inverse of t_cdf for p >= 0.5 (the only regime this draft ever calls):
    the smallest t >= 0 with t_cdf(t, df) == p. Expands `hi` until it brackets p, then
    bisects to `tol` in t or `max_iter` iterations, whichever binds first."""
    if not (0.5 <= p < 1.0):
        raise ValueError("t_quantile implemented for p in [0.5, 1.0) only")
    if df <= 0:
        raise ValueError("df must be positive")
    while t_cdf(hi, df) < p:
        hi *= 2.0
        if hi > 1e12:
            raise RuntimeError("t_quantile failed to bracket target probability")
    for _ in range(max_iter):
        mid = (lo + hi) / 2.0
        if t_cdf(mid, df) < p:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2.0


def t975(df):
    """Convenience wrapper: t(0.975, df), the two-sided-95% critical value used
    throughout §4/§6/§7/§9."""
    return t_quantile(0.975, df)


if __name__ == "__main__":
    for df, expected in [(10, 2.2281), (13, 2.1604), (14, 2.1448), (30, 2.0423), (60, 2.0003)]:
        got = t975(df)
        print(f"t(0.975, {df}) = {got:.4f}  (table: {expected})")
