"""
scripts/stats.py — shared, deterministic statistics helpers (stdlib only).

Used by metrics.py (Zipf-tail slope) and envelope.py (the ordinary-drift envelope and its
quadratic sensitivity check). No randomness, no hash-order dependence: all reductions are
over sequences in caller-supplied, already-deterministic order.
"""
import math


def ols_simple(xs, ys):
    """Ordinary least squares simple linear regression y = a + b*x.

    Returns (intercept_a, slope_b, xbar, sxx, ss_res).
    """
    n = len(xs)
    if n < 2:
        raise ValueError("ols_simple requires at least 2 points")
    xbar = sum(xs) / n
    ybar = sum(ys) / n
    sxx = sum((x - xbar) ** 2 for x in xs)
    if sxx == 0:
        raise ValueError("ols_simple requires variance in x")
    sxy = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    b = sxy / sxx
    a = ybar - b * xbar
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    return a, b, xbar, sxx, ss_res


def predict_linear(a, b, x):
    return a + b * x


def _solve_linear_system(matrix, rhs):
    """Solve A x = b via Gaussian elimination with partial pivoting. Stdlib only."""
    n = len(matrix)
    aug = [row[:] + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot_row][col]) < 1e-15:
            raise ValueError("singular matrix")
        aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
        pivot_val = aug[col][col]
        aug[col] = [v / pivot_val for v in aug[col]]
        for r in range(n):
            if r != col:
                factor = aug[r][col]
                aug[r] = [rv - factor * cv for rv, cv in zip(aug[r], aug[col])]
    return [row[-1] for row in aug]


def _invert_matrix(matrix):
    n = len(matrix)
    aug = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot_row = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot_row][col]) < 1e-15:
            raise ValueError("singular matrix")
        aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
        pivot_val = aug[col][col]
        aug[col] = [v / pivot_val for v in aug[col]]
        for r in range(n):
            if r != col:
                factor = aug[r][col]
                aug[r] = [rv - factor * cv for rv, cv in zip(aug[r], aug[col])]
    return [row[n:] for row in aug]


def ols_poly(xs, ys, degree):
    """Fit y = sum_j c_j * x**j (j=0..degree) by OLS normal equations.

    Returns (coeffs, ss_res, xtx_inv) where xtx_inv is the (degree+1)x(degree+1)
    inverse of X^T X, needed for the general OLS prediction-interval formula.
    """
    n = len(xs)
    p = degree + 1
    if n <= p:
        raise ValueError("ols_poly requires more points than parameters")
    design = [[x ** j for j in range(p)] for x in xs]
    xtx = [[sum(design[i][r] * design[i][c] for i in range(n)) for c in range(p)] for r in range(p)]
    xty = [sum(design[i][r] * ys[i] for i in range(n)) for r in range(p)]
    coeffs = _solve_linear_system(xtx, xty)
    xtx_inv = _invert_matrix(xtx)
    ss_res = sum((ys[i] - sum(coeffs[j] * design[i][j] for j in range(p))) ** 2 for i in range(n))
    return coeffs, ss_res, xtx_inv


def predict_poly(coeffs, x):
    return sum(c * (x ** j) for j, c in enumerate(coeffs))


def poly_pred_se(s, xtx_inv, x, degree):
    """General OLS prediction-interval standard error: s * sqrt(1 + x0^T (X'X)^-1 x0).

    This is the same formula that PREREGISTRATION.md §4 states in its degree-1
    specialization (SE = s*sqrt(1 + 1/n + (x*-xbar)^2/Sxx)); used here only for the
    non-decisional quadratic sensitivity table (§4 "Sensitivity").
    """
    x0 = [x ** j for j in range(degree + 1)]
    var = 0.0
    for i in range(len(x0)):
        for j in range(len(x0)):
            var += x0[i] * xtx_inv[i][j] * x0[j]
    return s * math.sqrt(1 + var)


def mean(values):
    values = list(values)
    return sum(values) / len(values)
