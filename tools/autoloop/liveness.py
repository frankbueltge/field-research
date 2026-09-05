#!/usr/bin/env python3
"""autoloop — stage PRE-CHECK: which of the loop's questions can produce a claim at all.

WHY THIS EXISTS
---------------
The loop divides a count by a number of questions in three places — the null-world per-test
rejection rate, the Benjamini-Hochberg denominator, and the reported yield — and until
2026-09-05 it had never been asked which questions belong in any of them.

On 2026-09-04 nine of the Crossref space's 66 questions turned out to be incapable of ever
firing: the grouping `has_fulltext_link` is true for 2,400 of 2,400 records, so it divides the
corpus into everything and nothing and its test returns no p-value at all. Averaging a rejection
rate over nine questions that are not tests is not a calibration figure. A convened adversary
then destroyed the post-hoc repair that session offered: trimming the same number of
*lowest-rate* questions for no reason at all moves the rate as much.

So the repair cannot be a better trim. It has to be a rule that names the impossible questions
BEFORE any test is run, from quantities that carry no association whatever.

THE RULE
--------
A question is a (grouping, outcome) pair. Its MARGINS on a corpus are:

    N  records in the corpus
    G  records where the grouping is true
    V  the multiset of outcome values over the m records where the outcome is not missing

These are exactly what a permutation of the grouping column leaves unchanged, and they say
nothing about the association between the two variables.

The REACHABLE FLOOR F(q) is the smallest p-value the loop's own test can return for q over every
assignment of grouping labels consistent with those margins. A question is

    ASLEEP  iff  F(q) >= alpha       (no labelling of any world can make it fire)
    AWAKE   otherwise

THE INVARIANCE THIS RESTS ON
----------------------------
`null_world()` permutes the grouping block across the whole corpus. That preserves N, G and V.
Liveness is therefore identical in the real world and in every null replicate, and can be
decided before either is run. K2 of the session's pre-registration tests this empirically rather
than taking it on trust.

CONSERVATIVE BY CONSTRUCTION
----------------------------
A question is marked asleep only when NO admissible labelling reaches alpha. A question marked
awake may still be nearly dead. That asymmetry is deliberate: ASLEEP is a claim of
impossibility, and impossibility is the only thing a denominator may exclude without an argument
about what is interesting.

WHAT IT DOES NOT DO
-------------------
It separates the impossible from the possible. It says nothing about whether an awake question
is worth asking, which is the boundary this practice has been circling since 2026-09-03 and is
untouched by anything here.

USAGE
    python3 tools/autoloop/liveness.py --corpus <corpus.json> --space arxiv|crossref \
        [--out <liveness.json>]
"""

from __future__ import annotations

import argparse
import bisect
import json
import math
import sys

from stats import average_ranks, normal_two_sided_p

ALPHA = 0.05


def value(rec, name):
    v = rec.get(name)
    if isinstance(v, bool):
        return 1 if v else 0
    return v


def admissible_n1(m, N, G):
    """Group-1 count among the m non-missing rows, over every permutation of the grouping."""
    lo = max(0, m - (N - G))
    hi = min(m, G)
    return lo, hi


def _mwu_extremes(sa, m, n1):
    """(U_max, U_min) reachable with n1 rows in group 1, ties counted at one half.

    `sa` is the outcome values sorted ascending. U is maximised by giving group 1 the n1
    largest values and minimised by giving it the n1 smallest; the boundary tie block is split
    by whatever n1 forces, and each tied cross pair contributes one half exactly as
    `average_ranks` does.
    """
    n0 = m - n1
    # --- top n1 in group 1
    vstar = sa[m - n1]
    lt = bisect.bisect_left(sa, vstar)
    eq = bisect.bisect_right(sa, vstar) - lt
    gt = m - lt - eq
    j = n1 - gt                      # copies of vstar that fall in group 1
    u_max = gt * n0 + j * lt + 0.5 * j * (eq - j)
    # --- bottom n1 in group 1
    vstar2 = sa[n1 - 1]
    lt2 = bisect.bisect_left(sa, vstar2)
    eq2 = bisect.bisect_right(sa, vstar2) - lt2
    j2 = n1 - lt2
    u_min = 0.5 * j2 * (eq2 - j2)
    return u_max, u_min


def floor_numeric(vals, tie_term, N, G):
    """Smallest reachable two-sided Mann-Whitney p over all admissible labellings."""
    m = len(vals)
    if m < 2:
        return 1.0
    sa = sorted(vals)
    lo, hi = admissible_n1(m, N, G)
    best = 1.0
    for n1 in range(lo, hi + 1):
        n0 = m - n1
        if n1 == 0 or n0 == 0:
            continue
        var = (n1 * n0 / 12.0) * ((m + 1) - tie_term / (m * (m - 1.0)))
        if var <= 0:
            continue
        mu = n1 * n0 / 2.0
        u_max, u_min = _mwu_extremes(sa, m, n1)
        z = max(abs(u_max - mu), abs(u_min - mu)) / math.sqrt(var)
        p = normal_two_sided_p(z)
        if p < best:
            best = p
    return best


def floor_binary(vals, N, G):
    """Smallest reachable two-sided two-proportion p over all admissible labellings."""
    m = len(vals)
    if m < 2:
        return 1.0
    x = sum(vals)
    pool = x / m
    if pool <= 0 or pool >= 1:
        return 1.0                       # the loop's own test returns no p-value at all
    lo, hi = admissible_n1(m, N, G)
    best = 1.0
    for n1 in range(lo, hi + 1):
        n0 = m - n1
        if n1 == 0 or n0 == 0:
            continue
        se = math.sqrt(pool * (1 - pool) * (1.0 / n1 + 1.0 / n0))
        if se == 0:
            continue
        for x1 in (min(n1, x), max(0, x - n0)):
            x0 = x - x1
            z = (x1 / n1 - x0 / n0) / se
            p = normal_two_sided_p(z)
            if p < best:
                best = p
    return best


def assess(records, groupings, numeric_outcomes, binary_outcomes, questions, alpha=ALPHA):
    """PRE-CHECK. Returns the liveness verdict for every question, from margins alone.

    `groupings` maps a grouping name to its predicate. `questions` is a list of (g, o) pairs.
    Nothing here reads the joint distribution of a grouping and an outcome.
    """
    N = len(records)
    gcount = {g: sum(1 for r in records if fn(r)) for g, fn in groupings.items()}
    prepared = {}
    for o in {o for _, o in questions}:
        vals = [value(r, o) for r in records]
        vals = [v for v in vals if v is not None]
        if o in numeric_outcomes:
            _ranks, tie = average_ranks(vals)
            prepared[o] = ("numeric", vals, tie)
        else:
            prepared[o] = ("binary", vals, None)

    out = {}
    for g, o in questions:
        kind, vals, tie = prepared[o]
        G = gcount[g]
        f = floor_numeric(vals, tie, N, G) if kind == "numeric" else floor_binary(vals, N, G)
        lo, hi = admissible_n1(len(vals), N, G)
        out[f"{g}|{o}"] = {
            "grouping": g, "outcome": o, "kind": kind,
            "N": N, "G": G, "m": len(vals),
            "n1_range": [lo, hi],
            "reachable_floor": f,
            "awake": bool(f < alpha),
        }
    awake = sorted(k for k, v in out.items() if v["awake"])
    asleep = sorted(k for k, v in out.items() if not v["awake"])
    return {
        "alpha": alpha,
        "questions_total": len(out),
        "awake_count": len(awake),
        "asleep_count": len(asleep),
        "awake": awake,
        "asleep": asleep,
        "detail": out,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--space", default="arxiv", choices=["arxiv", "crossref"])
    ap.add_argument("--out")
    args = ap.parse_args()

    from dial import SPACES, enumerate_questions
    space = SPACES[args.space]
    records = json.load(open(args.corpus))["records"]
    qs = enumerate_questions(space)
    res = assess(records, {g: v[0] for g, v in space["groupings"].items()},
                 space["numeric"], space["binary"], qs)
    if args.out:
        json.dump(res, open(args.out, "w"), indent=1, sort_keys=True)
    print(f"PRE-CHECK: {res['awake_count']} awake, {res['asleep_count']} asleep "
          f"of {res['questions_total']}", file=sys.stderr)
    for k in res["asleep"]:
        d = res["detail"][k]
        print(f"  asleep {k}  floor={d['reachable_floor']:.4g}  G={d['G']}/{d['N']}  m={d['m']}",
              file=sys.stderr)


if __name__ == "__main__":
    main()
