#!/usr/bin/env python3
"""autoloop — the statistics, in pure Python (no numpy/scipy in this environment).

Two tests only, chosen by the outcome's type, exactly as pre-registered:
  * numeric outcome  -> Mann-Whitney U, normal approximation with tie correction, two-sided
  * binary outcome   -> two-proportion z-test, pooled variance, two-sided

No continuity correction is applied; that is stated in METHOD.md. Both p-values come
from the normal tail via math.erfc, so nothing here depends on a library.
"""

import math


def normal_two_sided_p(z):
    return math.erfc(abs(z) / math.sqrt(2.0))


def average_ranks(values):
    """Ranks 1..n with ties averaged. Returns (ranks_in_input_order, tie_correction_term)."""
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    tie_term = 0.0
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j + 2) / 2.0                     # ranks are 1-based
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        t = j - i + 1
        if t > 1:
            tie_term += t ** 3 - t
        i = j + 1
    return ranks, tie_term


def mannwhitney_from_ranks(rank_sum_group1, n1, n2, tie_term):
    """Mann-Whitney U from a precomputed rank sum. Returns (u1, z, p, rank_biserial)."""
    n = n1 + n2
    if n1 == 0 or n2 == 0:
        return None, None, None, None
    u1 = rank_sum_group1 - n1 * (n1 + 1) / 2.0
    mu = n1 * n2 / 2.0
    if n < 2:
        return u1, None, None, None
    var = (n1 * n2 / 12.0) * ((n + 1) - tie_term / (n * (n - 1.0)))
    if var <= 0:
        return u1, None, None, None
    z = (u1 - mu) / math.sqrt(var)
    return u1, z, normal_two_sided_p(z), (2.0 * u1) / (n1 * n2) - 1.0


def two_proportion(x1, n1, x2, n2):
    """Pooled two-proportion z-test. Returns (z, p, risk_difference_in_points)."""
    if n1 == 0 or n2 == 0:
        return None, None, None
    p1, p2 = x1 / n1, x2 / n2
    pool = (x1 + x2) / (n1 + n2)
    if pool <= 0 or pool >= 1:
        return None, None, (p1 - p2) * 100.0
    se = math.sqrt(pool * (1 - pool) * (1.0 / n1 + 1.0 / n2))
    if se == 0:
        return None, None, (p1 - p2) * 100.0
    z = (p1 - p2) / se
    return z, normal_two_sided_p(z), (p1 - p2) * 100.0


def benjamini_hochberg(pvalues, q=0.05):
    """Returns the set of indices rejected at false-discovery rate q."""
    idx = [i for i, p in enumerate(pvalues) if p is not None]
    m = len(idx)
    if m == 0:
        return set()
    ordered = sorted(idx, key=lambda i: pvalues[i])
    cutoff = -1
    for rank, i in enumerate(ordered, start=1):
        if pvalues[i] <= rank / m * q:
            cutoff = rank
    return set(ordered[:cutoff]) if cutoff > 0 else set()
