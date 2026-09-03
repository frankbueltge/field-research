#!/usr/bin/env python3
"""autoloop — stage REVIEW, written as a second implementation rather than a second run.

The point of this file is that it shares no code with loop.py or stats.py. It reads the
committed corpus and the committed results and re-derives, by a different algorithm:

  * the group sizes, medians, event counts and percentages of every claim;
  * Mann-Whitney U by direct pairwise counting (O(n1*n2)) instead of by rank sums;
  * the normal tail by a rational approximation instead of the C library's erfc;
  * every number that appears in a written claim sentence, checked against the
    re-derivation (the drift check the WRITE stage cannot perform on itself);
  * the redundancy of the hypothesis space: pairs of questions that are the same
    question with the roles of the two variables swapped.

Disagreement is reported, never repaired (pre-registration, kill condition K3).

Usage: python3 tools/autoloop/review.py --corpus <corpus.json> --results <results.json>
                                        --out <review.json>
"""

import argparse
import json
import math
import re
import statistics

GROUP_RULES = {
    "weekend":          lambda r: r["published_weekday"] >= 5,
    "has_doi":          lambda r: bool(r["has_doi"]),
    "has_journal_ref":  lambda r: bool(r["has_journal_ref"]),
    "has_comment":      lambda r: bool(r["has_comment"]),
    "revised":          lambda r: bool(r["revised"]),
    "cross_listed":     lambda r: r["category_count"] > 1,
    "large_team":       lambda r: r["author_count"] >= 5,
    "night_submission": lambda r: r["published_hour_utc"] >= 22 or r["published_hour_utc"] < 6,
}
BINARY = {"has_doi", "has_journal_ref", "revised"}
# The variable each grouping is a dichotomisation of — used for the redundancy audit.
SOURCE_VAR = {
    "weekend": "published_weekday", "has_doi": "has_doi", "has_journal_ref": "has_journal_ref",
    "has_comment": "has_comment", "revised": "revised", "cross_listed": "category_count",
    "large_team": "author_count", "night_submission": "published_hour_utc",
}


def normal_tail(z):
    """Two-sided normal tail by Abramowitz & Stegun 7.1.26 - not the C library's erfc."""
    x = abs(z) / math.sqrt(2.0)
    t = 1.0 / (1.0 + 0.3275911 * x)
    poly = t * (0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429))))
    return poly * math.exp(-x * x)          # = erfc(x) to ~1.5e-7 absolute


def u_pairwise(a, b):
    """U for sample a against sample b by direct comparison; ties count a half."""
    b_sorted = sorted(b)
    n = len(b_sorted)
    u = 0.0
    import bisect
    for v in a:
        lo = bisect.bisect_left(b_sorted, v)
        hi = bisect.bisect_right(b_sorted, v)
        u += lo + 0.5 * (hi - lo)
    return u, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--results", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    corpus = json.load(open(args.corpus))["records"]
    res = json.load(open(args.results))
    disagreements, checks = [], 0

    def note(key, what, mine, theirs):
        disagreements.append({"claim": key, "quantity": what, "review": mine, "loop": theirs})

    for c in res["claims"]:
        g, o = c["grouping"], c["outcome"]
        rule = GROUP_RULES[g]
        rows = [r for r in corpus if r.get(o) is not None]
        g1 = [r for r in rows if rule(r)]
        g0 = [r for r in rows if not rule(r)]
        checks += 2
        if len(g1) != c["n1"]:
            note(c["key"], "n1", len(g1), c["n1"])
        if len(g0) != c["n0"]:
            note(c["key"], "n0", len(g0), c["n0"])

        if o in BINARY:
            x1 = sum(1 for r in g1 if r[o])
            x0 = sum(1 for r in g0 if r[o])
            checks += 2
            if c["events1"] is not None and x1 != c["events1"]:
                note(c["key"], "events1", x1, c["events1"])
            if c["events0"] is not None and x0 != c["events0"]:
                note(c["key"], "events0", x0, c["events0"])
            if len(g1) and len(g0):
                p1, p0 = x1 / len(g1), x0 / len(g0)
                pool = (x1 + x0) / (len(g1) + len(g0))
                checks += 1
                if 0 < pool < 1:
                    se = math.sqrt(pool * (1 - pool) * (1 / len(g1) + 1 / len(g0)))
                    z = (p1 - p0) / se
                    if c["z"] is not None and abs(z - c["z"]) > 1e-9:
                        note(c["key"], "z", z, c["z"])
        else:
            v1 = [r[o] for r in g1]
            v0 = [r[o] for r in g0]
            if v1 and v0:
                m1, m0 = statistics.median(v1), statistics.median(v0)
                checks += 2
                if c["summary1"] is not None and abs(m1 - c["summary1"]) > 1e-9:
                    note(c["key"], "median(group)", m1, c["summary1"])
                if c["summary0"] is not None and abs(m0 - c["summary0"]) > 1e-9:
                    note(c["key"], "median(rest)", m0, c["summary0"])
                # U by pairwise counting, then the rank-biserial that follows from it
                u1, _ = u_pairwise(v1, v0)
                rb = 2.0 * u1 / (len(v1) * len(v0)) - 1.0
                checks += 1
                if c["effect"] is not None and abs(rb - c["effect"]) > 1e-9:
                    note(c["key"], "rank-biserial (pairwise U)", rb, c["effect"])
                # z re-derived from the pairwise U and a tie count taken by frequency table,
                # not from the loop's rank sums. Added 2026-09-03 after a convened adversary
                # found that this file had been taking the loop's own z on trust for every
                # numeric claim - so a fault in the shared variance formula could not surface.
                n1_, n0_, n_ = len(v1), len(v0), len(v1) + len(v0)
                counts = {}
                for v in v1 + v0:
                    counts[v] = counts.get(v, 0) + 1
                tie_term = sum(t ** 3 - t for t in counts.values() if t > 1)
                var = (n1_ * n0_ / 12.0) * ((n_ + 1) - tie_term / (n_ * (n_ - 1.0)))
                checks += 1
                if var > 0:
                    z_here = (u1 - n1_ * n0_ / 2.0) / math.sqrt(var)
                    if c["z"] is not None and abs(z_here - c["z"]) > 1e-9:
                        note(c["key"], "z (pairwise U, independent tie count)", z_here, c["z"])
                elif c["z"] is not None:
                    note(c["key"], "z: variance non-positive here but the loop reported a z", None, c["z"])

        # the review pre-conditions, re-applied from the numbers just re-derived rather than
        # trusted from the loop's own verdict (same adversary finding)
        fails_here = []
        if len(g1) < 30 or len(g0) < 30:
            fails_here.append("c1")
        if o in BINARY:
            x1 = sum(1 for r in g1 if r[o])
            x0 = sum(1 for r in g0 if r[o])
            if min(x1, len(g1) - x1, x0, len(g0) - x0) < 10:
                fails_here.append("c2")
        else:
            if len({r[o] for r in rows}) < 5:
                fails_here.append("c3")
        if len(rows) < 0.5 * len(corpus):
            fails_here.append("c4")
        checks += 1
        theirs = sorted({f.split()[0] for f in c["failures"]})
        if sorted(fails_here) != theirs:
            note(c["key"], "review pre-conditions re-applied", fails_here, theirs)

        # the p-value, from the loop's own z but this file's normal tail
        if c["z"] is not None and c["p"] is not None:
            checks += 1
            p_here = normal_tail(c["z"])
            if c["p"] > 1e-6 and abs(p_here - c["p"]) > 2e-6:
                note(c["key"], "p from z (independent tail)", p_here, c["p"])

        # every number written in the claim sentence must be a number we just re-derived
        if c["sentence"]:
            allowed = {f"{c['n1']}", f"{c['n0']}"}
            if c["summary1"] is not None:
                allowed |= {f"{c['summary1']:g}", f"{c['summary1']:.1f}"}
            if c["summary0"] is not None:
                allowed |= {f"{c['summary0']:g}", f"{c['summary0']:.1f}"}
            if c["effect"] is not None:
                allowed |= {f"{abs(c['effect']):.3f}", f"{abs(c['effect']):.1f}"}
            for tok in re.findall(r"\d+\.\d+|\d+", c["sentence"]):
                checks += 1
                if tok in allowed:
                    continue
                # "p = <0.0001" is a threshold notation, not a measured quantity. The first
                # run of this file (data/review-run1-unrepaired.json, 2026-09-03) flagged all
                # five instances of it as unre-derivable numbers; the fault was here, not in
                # the WRITE stage. Repaired, dated, and both runs are committed.
                if tok in {"0", "0001", "0.0001"} and c["p"] is not None and c["p"] < 1e-4:
                    continue
                if c["p"] is not None and tok in f"{c['p']:.4f}":
                    continue
                note(c["key"], "number in the written sentence not re-derivable", tok, c["sentence"])

    # --- redundancy audit: the same question asked twice ------------------------------
    seen, mirrors = {}, []
    for c in res["claims"]:
        pair = tuple(sorted([SOURCE_VAR[c["grouping"]], c["outcome"]]))
        seen.setdefault(pair, []).append(c["key"])
    for pair, keys in sorted(seen.items()):
        if len(keys) > 1:
            mirrors.append({"underlying_pair": list(pair), "asked_as": keys,
                            "both_significant": all(any(cc["key"] == k and cc["significant"]
                                                        for cc in res["claims"]) for k in keys)})

    sig = [c for c in res["claims"] if c["significant"]]
    sig_pairs = {tuple(sorted([SOURCE_VAR[c["grouping"]], c["outcome"]])) for c in sig}
    bh = [c for c in res["claims"] if c["bh_survivor"]]
    bh_pairs = {tuple(sorted([SOURCE_VAR[c["grouping"]], c["outcome"]])) for c in bh}

    out = {
        "checks_performed": checks,
        "disagreements": disagreements,
        "verdict": "agrees" if not disagreements else "DISAGREES",
        "redundancy": {
            "questions_asked": res["hypotheses"],
            "distinct_underlying_variable_pairs": len(seen),
            "mirrored_questions": mirrors,
            "raw_findings": len(sig),
            "distinct_pairs_among_raw_findings": len(sig_pairs),
            "bh_survivors": len(bh),
            "distinct_pairs_among_bh_survivors": len(bh_pairs),
        },
    }
    json.dump(out, open(args.out, "w"), indent=1, sort_keys=True)
    print(f"REVIEW: {checks} checks, {len(disagreements)} disagreements, "
          f"{len(seen)} distinct variable pairs behind {res['hypotheses']} questions, "
          f"{len(bh_pairs)} behind {len(bh)} BH survivors")


if __name__ == "__main__":
    main()
