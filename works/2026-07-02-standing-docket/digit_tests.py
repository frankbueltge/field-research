"""
digit_tests.py -- Instrument 009, "The Standing Docket"

Pure Python 3 stdlib implementation of three classic digit-based fraud
detection tests (Benford first-digit, second-digit, and last-digit
uniformity), plus a self-written regularized incomplete gamma function
used to compute chi-squared p-values without any statistics library.

No numpy, no scipy. Only `math` and `random` (random is used by callers
for synthetic controls, not by this module itself).

--------------------------------------------------------------------
Chi-squared p-values via the regularized incomplete gamma function
--------------------------------------------------------------------

This follows the standard Numerical-Recipes-style method: the lower
regularized incomplete gamma function P(a,x) is evaluated either via
its power series (for x < a+1) or, by complementarity, via a continued
fraction for Q(a,x) = 1 - P(a,x) (for x >= a+1). ln(Gamma(a)) is
supplied by the stdlib (`math.lgamma`) rather than reimplemented.

The chi-squared survival function (the p-value for a chi-squared
statistic, i.e. P(X > x)) is:

    chi2_sf(x, df) = Q(df/2, x/2)

This implementation is unit-tested in test_digit_tests.py against
textbook chi-squared critical values. It is NOT a validated statistics
library -- that limitation is disclosed in the rendered work and in
README.md.
"""

import math

ITMAX = 200          # maximum iterations for series / continued fraction
EPS = 3.0e-12         # relative precision target
FPMIN = 1.0e-300      # smallest usable float, to avoid division by zero

ALPHA = 0.05          # chi2 flag threshold (p < ALPHA => flagged)
MAD_FIRST_DIGIT_CUTOFF = 0.015  # Nigrini's conventional first-digit MAD nonconformity cutoff (disclosed convention, see README)
N_GATE_LOW = 100
N_GATE_HIGH = 10000
LAST_DIGIT_MIN_VALUE = 1000  # last-digit test only uses values >= this


# ---------------------------------------------------------------------
# Regularized incomplete gamma function (gammp = P, gammq = Q = 1 - P)
# ---------------------------------------------------------------------

def _gser(a, x):
    """Series representation of P(a,x). Valid for x < a+1."""
    gln = math.lgamma(a)
    if x <= 0.0:
        return 0.0, gln
    ap = a
    total = 1.0 / a
    delta = total
    for _ in range(ITMAX):
        ap += 1.0
        delta *= x / ap
        total += delta
        if abs(delta) < abs(total) * EPS:
            break
    return total * math.exp(-x + a * math.log(x) - gln), gln


def _gcf(a, x):
    """Continued-fraction representation of Q(a,x). Valid for x >= a+1."""
    gln = math.lgamma(a)
    b = x + 1.0 - a
    c = 1.0 / FPMIN
    d = 1.0 / b
    h = d
    for i in range(1, ITMAX + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < FPMIN:
            d = FPMIN
        c = b + an / c
        if abs(c) < FPMIN:
            c = FPMIN
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < EPS:
            break
    return math.exp(-x + a * math.log(x) - gln) * h, gln


def gammp(a, x):
    """Regularized lower incomplete gamma function P(a,x)."""
    if x < 0.0 or a <= 0.0:
        raise ValueError("invalid arguments in gammp: a=%r x=%r" % (a, x))
    if x == 0.0:
        return 0.0
    if x < a + 1.0:
        p, _ = _gser(a, x)
        return p
    q, _ = _gcf(a, x)
    return 1.0 - q


def gammq(a, x):
    """Regularized upper incomplete gamma function Q(a,x) = 1 - P(a,x)."""
    if x < 0.0 or a <= 0.0:
        raise ValueError("invalid arguments in gammq: a=%r x=%r" % (a, x))
    if x == 0.0:
        return 1.0
    if x < a + 1.0:
        p, _ = _gser(a, x)
        return 1.0 - p
    q, _ = _gcf(a, x)
    return q


def chi2_sf(x, df):
    """Survival function (upper-tail p-value) of the chi-squared distribution."""
    if x <= 0:
        return 1.0
    return gammq(df / 2.0, x / 2.0)


# ---------------------------------------------------------------------
# Digit extraction
# ---------------------------------------------------------------------

def leading_digit(value):
    """First significant (non-zero) digit of abs(value). None if value == 0."""
    v = abs(value)
    if v == 0:
        return None
    s = "%.6e" % v          # e.g. "1.234560e+05"
    return int(s[0])


def second_digit(value):
    """Second significant digit of abs(value). None if value == 0."""
    v = abs(value)
    if v == 0:
        return None
    s = "%.6e" % v          # "d.dddddde+NN" -- index 2 is the digit after the point
    return int(s[2])


def last_digit(value):
    """Last digit of the integer part of abs(value)."""
    v = int(abs(value))
    return v % 10


# ---------------------------------------------------------------------
# Expected distributions
# ---------------------------------------------------------------------

def benford_first_digit_expected():
    """p_d = log10(1 + 1/d) for d = 1..9."""
    return [math.log10(1.0 + 1.0 / d) for d in range(1, 10)]


def benford_second_digit_expected():
    """p_d2 = sum over d1=1..9 of log10(1 + 1/(10*d1+d2)), for d2 = 0..9."""
    out = []
    for d2 in range(0, 10):
        p = sum(math.log10(1.0 + 1.0 / (10 * d1 + d2)) for d1 in range(1, 10))
        out.append(p)
    return out


def uniform_digit_expected():
    """0.1 for each digit 0..9 (last-digit uniformity null)."""
    return [0.1] * 10


# ---------------------------------------------------------------------
# Generic chi-squared goodness-of-fit
# ---------------------------------------------------------------------

def chi_square_gof(observed_counts, expected_props, n):
    """
    observed_counts: list of observed category counts
    expected_props:  list of expected category proportions (sum to 1)
    n:               total observations (sum of observed_counts)
    Returns (stat, df, p).
    """
    expected_counts = [p * n for p in expected_props]
    stat = 0.0
    for o, e in zip(observed_counts, expected_counts):
        if e > 0:
            stat += (o - e) ** 2 / e
    df = len(observed_counts) - 1
    p = chi2_sf(stat, df)
    return stat, df, p


def mean_absolute_deviation(observed_counts, expected_props, n):
    """MAD = mean(|observed_proportion - expected_proportion|) over categories."""
    observed_props = [o / n for o in observed_counts]
    deviations = [abs(op - ep) for op, ep in zip(observed_props, expected_props)]
    return sum(deviations) / len(deviations)


def mad_conformity_label(mad):
    """Nigrini's four-tier conformity scale for the first-digit MAD (disclosed convention)."""
    if mad < 0.006:
        return "close conformity"
    if mad < 0.012:
        return "acceptable conformity"
    if mad < MAD_FIRST_DIGIT_CUTOFF:
        return "marginally acceptable"
    return "nonconformity"


# ---------------------------------------------------------------------
# N-gate
# ---------------------------------------------------------------------

def n_gate_status(n):
    if N_GATE_LOW <= n <= N_GATE_HIGH:
        return "IN-SPEC"
    return "OUT-OF-SPEC"


# ---------------------------------------------------------------------
# The three tests, bundled
# ---------------------------------------------------------------------

def run_first_digit_test(values):
    """Benford first-digit chi2 test + MAD, over all nonzero values."""
    digits = [leading_digit(v) for v in values if v != 0]
    n = len(digits)
    counts = [digits.count(d) for d in range(1, 10)]
    expected = benford_first_digit_expected()
    stat, df, p = chi_square_gof(counts, expected, n)
    mad = mean_absolute_deviation(counts, expected, n)
    chi2_result = {
        "stat": stat,
        "df": df,
        "p": p,
        "flagged": p < ALPHA,
    }
    mad_result = {
        "stat": mad,
        "cutoff": MAD_FIRST_DIGIT_CUTOFF,
        "conformity_label": mad_conformity_label(mad),
        "flagged": mad > MAD_FIRST_DIGIT_CUTOFF,
    }
    return n, chi2_result, mad_result


def run_second_digit_test(values):
    """Benford second-digit chi2 test, over all nonzero values."""
    digits = [second_digit(v) for v in values if v != 0]
    n = len(digits)
    counts = [digits.count(d) for d in range(0, 10)]
    expected = benford_second_digit_expected()
    stat, df, p = chi_square_gof(counts, expected, n)
    return {
        "n": n,
        "stat": stat,
        "df": df,
        "p": p,
        "flagged": p < ALPHA,
    }


def run_last_digit_test(values):
    """Last-digit uniformity chi2 test, restricted to values >= LAST_DIGIT_MIN_VALUE."""
    filtered = [v for v in values if abs(v) >= LAST_DIGIT_MIN_VALUE]
    digits = [last_digit(v) for v in filtered]
    n = len(digits)
    counts = [digits.count(d) for d in range(0, 10)]
    expected = uniform_digit_expected()
    stat, df, p = chi_square_gof(counts, expected, n)
    return {
        "n": n,
        "n_excluded_below_1000": len(values) - n,
        "stat": stat,
        "df": df,
        "p": p,
        "flagged": p < ALPHA,
    }


def run_all_tests(values):
    """
    Run all three digit tests on a series of positive numeric values.
    Returns (n, n_gate, tests_dict, chi2_mad_disagree).
    n is the series' total count (used for the N-gate stamp).
    """
    n = len(values)
    n_gate = n_gate_status(n)
    fd_n, fd_chi2, fd_mad = run_first_digit_test(values)
    sd = run_second_digit_test(values)
    ld = run_last_digit_test(values)
    tests = {
        "first_digit_chi2": fd_chi2,
        "first_digit_mad": fd_mad,
        "second_digit_chi2": sd,
        "last_digit_chi2": ld,
    }
    chi2_mad_disagree = fd_chi2["flagged"] != fd_mad["flagged"]
    return n, n_gate, tests, chi2_mad_disagree
