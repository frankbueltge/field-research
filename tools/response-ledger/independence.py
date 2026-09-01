#!/usr/bin/env python3
"""Independence audit of the response-ledger cohort.

Written 2026-09-01 (session 145) after two sibling practices, working
independently from the same shipped row file, arrived at the same place:

  * The Studio measured how papers under a single concern notice resolve, and
    found them resolving together far more often than independence allows.
  * The Atelier asked what our resampling scheme holds invariant, on the
    ground that whatever a resampling holds fixed is a class of finding the
    test can never produce.

Both questions are about the same object: the dependence structure inside the
1,277-paper mature cohort of `2026-09-01-how-long-a-warning-stands`. This
script measures it, and states for each resampling scheme what it holds fixed.

Input:  artifacts/cycle-001/2026-09-01-how-long-a-warning-stands/data/cohort.csv
Output: JSON on stdout, or to the path given as argv[2].

Usage:
    python3 tools/response-ledger/independence.py <cohort.csv> [out.json]
    python3 tools/response-ledger/independence.py <cohort.csv> <out.json> --check
"""

import collections
import csv
import json
import random
import statistics
import sys

SEED = 20260901
DRAWS = 2000
PERM_DRAWS = 50000
SENTINEL = "unavailable"  # Retraction Watch writes this where it has no notice DOI


def load(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r["in_mature_cohort"] == "1"]


def resolved(row):
    return row["resolved_within_5y"] == "1"


def days(row):
    return int(row["days_to_retraction"]) if row["days_to_retraction"] else None


# ---------------------------------------------------------------- clusterings

def key_paper(row, _i):
    return "p:" + row["original_doi"]


def key_notice_shipped(row, i):
    """Exactly the grouping `ledger.py:notice_level` used in the shipped page.

    An empty notice DOI becomes a singleton; the literal string 'unavailable'
    does not, and so every paper whose notice DOI is unknown is collapsed into
    one 48-paper pseudo-notice. That is the defect this audit found.
    """
    k = row["concern_notice_doi"].strip().lower()
    return k or "no-doi:" + row["original_doi"]


def key_notice_fixed(row, i):
    """The same grouping with the sentinel treated as missing, not as a name."""
    k = row["concern_notice_doi"].strip().lower()
    if not k or k == SENTINEL:
        return "no-doi:" + row["original_doi"]
    return k


def key_day(row, _i):
    return "d:" + row["concern_date"]


SCHEMES = [
    ("paper", key_paper,
     "nothing beyond the cohort's size; every paper is its own unit"),
    ("notice_shipped", key_notice_shipped,
     "the composition of each notice, including one 48-paper pseudo-notice "
     "built from a missing-value sentinel"),
    ("notice", key_notice_fixed,
     "the composition of each real notice; papers with no known notice are "
     "singletons"),
    ("day", key_day,
     "the entire composition of every issuance day, so any question about "
     "variation *within* a day is invisible to this interval"),
]


def cluster(rows, keyfn):
    groups = collections.defaultdict(list)
    for i, r in enumerate(rows):
        groups[keyfn(r, i)].append(r)
    return list(groups.values())


# ---------------------------------------------------------------- bootstrap

def bootstrap(groups, draws, seed):
    """Resample clusters with replacement; report share resolved and median."""
    rng = random.Random(seed)
    n = len(groups)
    shares, medians = [], []
    for _ in range(draws):
        sample = [groups[rng.randrange(n)] for _ in range(n)]
        flat = [r for g in sample for r in g]
        if not flat:
            continue
        shares.append(100.0 * sum(1 for r in flat if resolved(r)) / len(flat))
        d = [days(r) for r in flat if resolved(r) and days(r) is not None]
        if d:
            medians.append(statistics.median(d))
    return shares, medians


def pct(values, lo=2.5, hi=97.5):
    """Linear-interpolated percentiles — the estimator the shipped page used.

    Nearest-index selection was tried first here and moved the day-level upper
    bound by 0.2 points, which is enough to stop this audit reproducing the
    published interval exactly. Interpolation does reproduce it.
    """
    if not values:
        return [None, None]
    s = sorted(values)
    def at(p):
        pos = p / 100 * (len(s) - 1)
        lo_i = int(pos)
        hi_i = min(lo_i + 1, len(s) - 1)
        frac = pos - lo_i
        return s[lo_i] + (s[hi_i] - s[lo_i]) * frac
    return [round(at(lo), 1), round(at(hi), 1)]


# ------------------------------------------------------- uniformity of a notice

def uniformity(groups, seed, draws):
    """How often do papers under one notice share an outcome?

    Null: outcomes reassigned at random across the whole cohort, cluster sizes
    held fixed — the same test the Studio ran, run here on the full mature
    cohort rather than on the multi-paper notices alone.
    """
    multi = [g for g in groups if len(g) > 1]
    sizes = [len(g) for g in multi]
    covered = sum(sizes)
    obs = sum(1 for g in multi
              if len(set(resolved(r) for r in g)) == 1)
    outcomes = [resolved(r) for g in groups for r in g]
    rng = random.Random(seed)
    ge = 0
    pool = list(outcomes)
    for _ in range(draws):
        rng.shuffle(pool)
        pos = 0
        u = 0
        for s in sizes:
            chunk = pool[pos:pos + s]
            pos += s
            if len(set(chunk)) == 1:
                u += 1
        if u >= obs:
            ge += 1
    return {
        "multi_paper_notices": len(multi),
        "papers_they_cover": covered,
        "uniform_observed": obs,
        "uniform_share": round(100.0 * obs / len(multi), 1) if multi else None,
        "permutation_draws": draws,
        "draws_at_or_above_observed": ge,
        "largest_notice": max(sizes) if sizes else 0,
    }


def main():
    path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
    check = "--check" in sys.argv

    rows = load(path)
    n = len(rows)
    result = {
        "generated": "2026-09-01",
        "source": path,
        "mature_cohort": n,
        "resolved": sum(1 for r in rows if resolved(r)),
        "seed": SEED,
        "draws": DRAWS,
        "schemes": [],
    }
    result["share"] = round(100.0 * result["resolved"] / n, 1)

    paper_width = None
    for name, keyfn, invariant in SCHEMES:
        groups = cluster(rows, keyfn)
        shares, medians = bootstrap(groups, DRAWS, SEED)
        ci = pct(shares)
        width = round(ci[1] - ci[0], 1)
        if name == "paper":
            paper_width = width
        entry = {
            "scheme": name,
            "units": len(groups),
            "largest_unit": max(len(g) for g in groups),
            "share_ci": ci,
            "ci_width": width,
            # Design effect on the variance scale: (width / paper width)^2.
            "design_effect": round((width / paper_width) ** 2, 2) if paper_width else None,
            "effective_n": None,
            "median_ci": pct(medians),
            "holds_invariant": invariant,
        }
        if entry["design_effect"]:
            entry["effective_n"] = int(round(n / entry["design_effect"]))
        result["schemes"].append(entry)

    fixed = cluster(rows, key_notice_fixed)
    result["uniformity"] = uniformity(fixed, SEED, PERM_DRAWS)

    shipped = cluster(rows, key_notice_shipped)

    def notice_share(groups):
        full = sum(1 for g in groups if all(resolved(r) for r in g))
        return round(100.0 * full / len(groups), 1), full

    share_shipped, full_shipped = notice_share(shipped)
    share_fixed, full_fixed = notice_share(fixed)
    result["sentinel_defect"] = {
        "sentinel": SENTINEL,
        "papers_collapsed": sum(1 for r in rows
                                if r["concern_notice_doi"].strip().lower() == SENTINEL),
        "units_shipped": len(shipped),
        "units_corrected": len(fixed),
        "largest_unit_shipped": max(len(g) for g in shipped),
        "largest_unit_corrected": max(len(g) for g in fixed),
        "notice_level_share_shipped": share_shipped,
        "notice_level_fully_resolved_shipped": full_shipped,
        "notice_level_share_corrected": share_fixed,
        "notice_level_fully_resolved_corrected": full_fixed,
    }

    text = json.dumps(result, indent=2)
    if out_path:
        if check:
            with open(out_path, encoding="utf-8") as fh:
                if fh.read().strip() != text.strip():
                    print("MISMATCH: recomputation differs from stored file", file=sys.stderr)
                    return 1
            print("check ok")
            return 0
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
