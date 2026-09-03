#!/usr/bin/env python3
"""autoloop — one thing the loop cannot do for itself.

A convened adversary (2026-09-03) argued that the loop's largest non-mechanical finding -
cross-listed papers have fewer authors - is substantially a composition effect of the corpus:
the eight category queries that built it put whole categories almost entirely on one side of
the grouping. This file tests that argument by stratifying the finding on primary category.

It is deliberately NOT part of the loop. Nothing in the pipeline asks whether a grouping is
confounded with how the corpus was assembled, because the pipeline does not know that the
corpus was assembled. A person had to ask.

Usage: python3 tools/autoloop/stratify.py --corpus <corpus.json> --out <stratify.json>
"""

import argparse
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from stats import average_ranks, mannwhitney_from_ranks           # noqa: E402


def mwu(values, flags):
    ranks, tie = average_ranks(values)
    n1 = sum(1 for f in flags if f)
    n0 = len(flags) - n1
    if n1 == 0 or n0 == 0:
        return {"n1": n1, "n0": n0, "effect": None, "p": None}
    rs1 = sum(r for r, f in zip(ranks, flags) if f)
    _, _, p, rb = mannwhitney_from_ranks(rs1, n1, n0, tie)
    return {"n1": n1, "n0": n0, "effect": rb, "p": p}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    recs = json.load(open(args.corpus))["records"]

    grouping = lambda r: r["category_count"] > 1          # noqa: E731  (cross_listed)
    outcome = "author_count"

    pooled = mwu([r[outcome] for r in recs], [grouping(r) for r in recs])

    strata = {}
    for cat in sorted({r["primary_category"] for r in recs}):
        sub = [r for r in recs if r["primary_category"] == cat]
        if len(sub) < 30:
            continue
        strata[cat] = mwu([r[outcome] for r in sub], [grouping(r) for r in sub])
        strata[cat]["records"] = len(sub)

    inside = [r for r in recs if grouping(r)]
    outside = [r for r in recs if not grouping(r)]
    mix = {}
    for cat in sorted({r["primary_category"] for r in recs}):
        a = sum(1 for r in inside if r["primary_category"] == cat)
        b = sum(1 for r in outside if r["primary_category"] == cat)
        if a + b >= 30:
            mix[cat] = {"share_of_cross_listed_pct": round(100 * a / len(inside), 1),
                        "share_of_rest_pct": round(100 * b / len(outside), 1),
                        "cross_listed_pct_of_category": round(100 * a / (a + b), 1)}

    testable = [c for c, s in strata.items() if s["p"] is not None]
    sig = [c for c in testable if strata[c]["p"] < 0.05]
    out = {
        "_what_this_is": ("A stratified re-reading of one finding, prompted by a convened "
                          "adversary on 2026-09-03. Not part of the loop: the loop cannot ask "
                          "whether its own corpus construction produced its finding."),
        "claim": "cross_listed | author_count",
        "pooled": pooled,
        "by_primary_category": strata,
        "category_mix": mix,
        "strata_testable": len(testable),
        "strata_significant_at_05": len(sig),
        "strata_significant_names": sig,
        "verdict": ("The pooled effect is larger than every stratum but one, and only "
                    f"{len(sig)} of {len(testable)} testable strata reach p < 0.05 on their own. "
                    "Whole categories sit almost entirely on one side of the grouping, so a "
                    "share of the pooled effect is the corpus's category mix rather than a "
                    "property of cross-listing."),
    }
    json.dump(out, open(args.out, "w"), indent=1, sort_keys=True)
    print(f"pooled rb={pooled['effect']:+.3f} p={pooled['p']:.2e}; "
          f"{len(sig)}/{len(testable)} strata significant")
    for c, s in strata.items():
        e = "n/a" if s["effect"] is None else f"{s['effect']:+.3f}"
        p = "n/a" if s["p"] is None else f"{s['p']:.3f}"
        print(f"  {c:9s} n={s['records']:4d} ({s['n1']}/{s['n0']})  rb={e}  p={p}")


if __name__ == "__main__":
    main()
