#!/usr/bin/env python3
"""autoloop — the dial.

Session 150 read one point off a curve and called it a dial: "the loop manufactures findings
because it asks 66 questions and for no other reason." This turns the dial. It runs the same
battery of tests over question SETS of varying size k, in two families that hold k fixed and
vary only how much the questions repeat each other, against a corpus and against a null world
in which every grouping-outcome association has been destroyed by permutation.

Two corpora, two spaces, one architecture:
  arxiv     - session 150's space, reproduced verbatim from loop.py (K2 checks that it is)
  crossref  - a new space of identical shape over an entirely different literature

Both spaces are 8 groupings x 9 outcomes minus the 6 self-pairs = 66 questions resting on 51
distinct unordered variable pairs. Everything below is fixed in PREREGISTRATION.md.

Every stage failure is appended to the break log instead of raising.

Usage:
  python3 tools/autoloop/dial.py --corpus <corpus.json> --space arxiv|crossref \
      --out <sweep.json> [--replicates 400] [--seed 20260904]
"""

import argparse
import json
import random
import statistics
import sys
import time

from stats import (average_ranks, benjamini_hochberg, mannwhitney_from_ranks,
                   two_proportion)

ALPHA = 0.05
BH_Q = 0.05
K_VALUES = [4, 8, 15, 22, 30, 40, 51, 66]          # PREREGISTRATION.md §4

# --- the two spaces --------------------------------------------------------------------
#
# Each grouping is (predicate, prose, canonical variable). The canonical variable is what
# makes two questions the SAME question: (a,b) and (b,a) rest on one unordered pair {a,b}
# and, when both are binary, on one 2x2 table.

SPACES = {
    "arxiv": {
        "groupings": {
            "weekend":          (lambda r: r["published_weekday"] >= 5, "published at a weekend (UTC)", "published_weekday"),
            "has_doi":          (lambda r: r["has_doi"], "carries a DOI", "has_doi"),
            "has_journal_ref":  (lambda r: r["has_journal_ref"], "carries a journal reference", "has_journal_ref"),
            "has_comment":      (lambda r: r["has_comment"], "carries an author comment", "has_comment"),
            "revised":          (lambda r: r["revised"], "was revised after posting", "revised"),
            "cross_listed":     (lambda r: r["category_count"] > 1, "is cross-listed", "category_count"),
            "large_team":       (lambda r: r["author_count"] >= 5, "has five or more authors", "author_count"),
            "night_submission": (lambda r: r["published_hour_utc"] >= 22 or r["published_hour_utc"] < 6,
                                 "was posted between 22:00 and 06:00 UTC", "published_hour_utc"),
        },
        "numeric": {
            "title_words": "title length in words",
            "abstract_words": "abstract length in words",
            "author_count": "number of authors",
            "category_count": "number of categories",
            "comment_pages": "page count stated in the author comment",
            "published_hour_utc": "hour of posting (UTC)",
        },
        "binary": {
            "has_doi": "carrying a DOI",
            "has_journal_ref": "carrying a journal reference",
            "revised": "having been revised after posting",
        },
        "excluded": {
            ("has_doi", "has_doi"),
            ("has_journal_ref", "has_journal_ref"),
            ("revised", "revised"),
            ("cross_listed", "category_count"),
            ("large_team", "author_count"),
            ("night_submission", "published_hour_utc"),
        },
        "stratum_field": "primary_category",
    },
    "crossref": {
        "groupings": {
            "open_licence":      (lambda r: r["has_license"], "records a licence", "has_license"),
            "has_abstract":      (lambda r: r["has_abstract"], "deposits an abstract", "has_abstract"),
            "has_orcid":         (lambda r: r["has_orcid"], "has an author with an ORCID", "has_orcid"),
            "funded":            (lambda r: r["has_funder"], "records a funder", "has_funder"),
            "large_team":        (lambda r: r["author_count"] >= 5, "has five or more authors", "author_count"),
            "long_bibliography": (lambda r: (r["reference_count"] or 0) >= 30, "cites thirty or more references", "reference_count"),
            "cited":             (lambda r: (r["cited_by_count"] or 0) > 0, "has been cited at least once", "cited_by_count"),
            "has_fulltext_link": (lambda r: r["has_fulltext_link"], "deposits a full-text link", "has_fulltext_link"),
        },
        "numeric": {
            "title_words": "title length in words",
            "abstract_words": "abstract length in words",
            "author_count": "number of authors",
            "reference_count": "number of references",
            "cited_by_count": "number of citations received",
            "published_doy": "day of year of the issue date",
        },
        "binary": {
            "has_license": "recording a licence",
            "has_abstract": "depositing an abstract",
            "has_orcid": "having an author with an ORCID",
        },
        "excluded": {
            ("open_licence", "has_license"),
            ("has_abstract", "has_abstract"),
            ("has_orcid", "has_orcid"),
            ("large_team", "author_count"),
            ("long_bibliography", "reference_count"),
            ("cited", "cited_by_count"),
        },
        "stratum_field": "member",
    },
}


def enumerate_questions(space):
    """Stage QUESTION. Canonical order: groupings in declaration order, then outcomes."""
    out = []
    for g in space["groupings"]:
        for o in list(space["numeric"]) + list(space["binary"]):
            if (g, o) in space["excluded"]:
                continue
            out.append((g, o))
    return out


def var_pair(space, g, o):
    """The unordered pair of variables a question rests on."""
    gv = space["groupings"][g][2]
    return tuple(sorted((gv, o)))


# --- the two selection families --------------------------------------------------------

def select_lean(space, pairs, k):
    """No unordered variable pair twice, canonical order otherwise."""
    seen, out = set(), []
    for q in pairs:
        vp = var_pair(space, *q)
        if vp in seen:
            continue
        seen.add(vp)
        out.append(q)
        if len(out) == k:
            return out
    for q in pairs:                                  # k > distinct pairs: fill with the rest
        if q not in out:
            out.append(q)
            if len(out) == k:
                break
    return out


def select_dense(space, pairs, k):
    """Repeatable questions first, in matched (a,b),(b,a) couples; then canonical order."""
    by_vp = {}
    for q in pairs:
        by_vp.setdefault(var_pair(space, *q), []).append(q)
    couples = [v for v in by_vp.values() if len(v) > 1]
    couples.sort(key=lambda v: pairs.index(v[0]))
    out = []
    for c in couples:
        for q in c:
            if len(out) < k:
                out.append(q)
    for q in pairs:
        if len(out) >= k:
            break
        if q not in out:
            out.append(q)
    return out[:k]


def redundancy(space, qs):
    """r = 1 - distinct unordered variable pairs / questions asked."""
    if not qs:
        return 0.0
    return 1.0 - len({var_pair(space, *q) for q in qs}) / len(qs)


# --- one test (session 150's, unchanged) -----------------------------------------------

def value(rec, name):
    v = rec.get(name)
    if isinstance(v, bool):
        return 1 if v else 0
    return v


def prepare_outcome(space, records, outcome):
    idx = [i for i, r in enumerate(records) if value(r, outcome) is not None]
    vals = [value(records[i], outcome) for i in idx]
    if outcome in space["numeric"]:
        ranks, tie_term = average_ranks(vals)
        return {"idx": idx, "vals": vals, "ranks": ranks, "tie": tie_term, "kind": "numeric"}
    return {"idx": idx, "vals": vals, "ranks": None, "tie": None, "kind": "binary"}


def run_test(prep, groups):
    idx, vals, kind = prep["idx"], prep["vals"], prep["kind"]
    g1 = [k for k, i in enumerate(idx) if groups[i]]
    g0 = [k for k, i in enumerate(idx) if not groups[i]]
    n1, n0 = len(g1), len(g0)
    if kind == "numeric":
        ranks = prep["ranks"]
        rs1 = 0.0
        for k in g1:
            rs1 += ranks[k]
        _u1, z, p, rb = mannwhitney_from_ranks(rs1, n1, n0, prep["tie"])
        med1 = statistics.median([vals[k] for k in g1]) if n1 else None
        med0 = statistics.median([vals[k] for k in g0]) if n0 else None
        return {"test": "mann-whitney-u", "n1": n1, "n0": n0, "z": z, "p": p, "effect": rb,
                "effect_kind": "rank-biserial", "summary1": med1, "summary0": med0,
                "summary_kind": "median", "distinct_values": len(set(vals)),
                "events1": None, "events0": None}
    x1 = sum(vals[k] for k in g1)
    x0 = sum(vals[k] for k in g0)
    z, p, rd = two_proportion(x1, n1, x0, n0)
    return {"test": "two-proportion-z", "n1": n1, "n0": n0, "z": z, "p": p, "effect": rd,
            "effect_kind": "risk-difference-points",
            "summary1": (100.0 * x1 / n1 if n1 else None),
            "summary0": (100.0 * x0 / n0 if n0 else None),
            "summary_kind": "percent", "distinct_values": len(set(vals)),
            "events1": x1, "events0": x0}


def preconditions(space, res, n_total, n_corpus):
    fails = []
    if res["n1"] < 30 or res["n0"] < 30:
        fails.append("c1 group smaller than 30")
    if res["test"] == "two-proportion-z":
        if res["events1"] is None or min(res["events1"], res["n1"] - res["events1"],
                                         res["events0"], res["n0"] - res["events0"]) < 10:
            fails.append("c2 fewer than 10 events or non-events in a group")
    else:
        if res["distinct_values"] < 5:
            fails.append("c3 fewer than 5 distinct outcome values")
    if n_total < 0.5 * n_corpus:
        fails.append("c4 outcome missing for more than half the corpus")
    return fails


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return ((c - h) / d, (c + h) / d)


# --- the sweep --------------------------------------------------------------------------

def null_sweep(space, records, cells, preps, group_cols, replicates, seed, breaks):
    """One permutation stream, shared by every cell, so the cells are paired.

    On each replicate the whole grouping block is permuted once and every cell is scored
    against that same permuted world. Correlations among groupings and among outcomes
    survive; every grouping-outcome association is destroyed.
    """
    rng = random.Random(seed)
    n = len(records)
    order = list(range(n))
    counts = {name: [] for name in cells}
    per_cell_test_hits = {name: 0 for name in cells}
    all_q = sorted({q for qs in cells.values() for q in qs})
    per_question_hits = {f"{g}|{o}": 0 for g, o in all_q}
    t0 = time.time()
    for rep in range(replicates):
        rng.shuffle(order)
        permuted = {g: [col[order[i]] for i in range(n)] for g, col in group_cols.items()}
        hit = {}
        for g, o in all_q:
            try:
                res = run_test(preps[o], permuted[g])
            except Exception as e:
                breaks.append({"stage": "EXPERIMENT", "kind": "null_test_error",
                               "where": f"{g}|{o}@rep{rep}", "detail": str(e)[:160]})
                hit[(g, o)] = False
                continue
            hit[(g, o)] = res["p"] is not None and res["p"] < ALPHA
            if hit[(g, o)]:
                per_question_hits[f"{g}|{o}"] += 1
        for name, qs in cells.items():
            h = sum(1 for q in qs if hit.get(q))
            counts[name].append(h)
            per_cell_test_hits[name] += h
    out = {}
    for name, qs in cells.items():
        c = counts[name]
        mean = sum(c) / len(c)
        var = statistics.pvariance(c)
        tests_total = replicates * len(qs)
        lo, hi = wilson(per_cell_test_hits[name], tests_total)
        out[name] = {
            "questions": len(qs),
            "mean": mean,
            "variance": var,
            "overdispersion": (var / mean) if mean > 0 else None,
            "binomial_variance": len(qs) * ALPHA * (1 - ALPHA),
            "p_at_least_one": sum(1 for h in c if h >= 1) / len(c),
            "p_at_least_one_independent": 1 - (1 - ALPHA) ** len(qs),
            "max": max(c), "min": min(c),
            "histogram": {str(k): c.count(k) for k in sorted(set(c))},
            "rejections_total": per_cell_test_hits[name],
            "tests_total": tests_total,
            "per_test_rate": per_cell_test_hits[name] / tests_total,
            "per_test_ci95": [lo, hi],
            # the whole count vector, in replicate order: every cell was scored against the
            # SAME permuted world on every replicate, so any two cells can be compared paired.
            "counts": c,
        }
    per_question = {k: v / replicates for k, v in per_question_hits.items()}
    return out, per_question, round(time.time() - t0, 1)


def real_battery(space, records, questions, breaks, label):
    preps = {o: prepare_outcome(space, records, o) for o in {o for _, o in questions}}
    group_cols = {g: [bool(space["groupings"][g][0](r)) for r in records] for g in space["groupings"]}
    out = {}
    for g, o in questions:
        key = f"{g}|{o}"
        try:
            res = run_test(preps[o], group_cols[g])
        except Exception as e:
            breaks.append({"stage": "EXPERIMENT", "kind": "test_error",
                           "where": f"{key}@{label}", "detail": str(e)[:160]})
            continue
        res["failures"] = preconditions(space, res, len(preps[o]["idx"]), len(records))
        res["var_pair"] = list(var_pair(space, g, o))
        out[key] = res
    return out, preps, group_cols


def bh_over(full, keys):
    ks = [k for k in keys if full.get(k) and full[k]["p"] is not None and not full[k]["failures"]]
    ps = [full[k]["p"] for k in ks]
    return {ks[i] for i in benjamini_hochberg(ps, BH_Q)}, len(ks)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--space", required=True, choices=sorted(SPACES))
    ap.add_argument("--out", required=True)
    ap.add_argument("--replicates", type=int, default=400)
    ap.add_argument("--seed", type=int, default=20260904)
    args = ap.parse_args()

    space = SPACES[args.space]
    with open(args.corpus) as f:
        corpus = json.load(f)
    records = corpus["records"]
    breaks = []

    questions = enumerate_questions(space)
    distinct_full = len({var_pair(space, *q) for q in questions})
    print(f"QUESTION: {len(questions)} questions on {distinct_full} distinct variable pairs",
          file=sys.stderr)

    cells = {}
    for k in K_VALUES:
        cells[f"lean@{k}"] = select_lean(space, questions, k)
        cells[f"dense@{k}"] = select_dense(space, questions, k)
    cell_meta = {name: {"k": len(qs), "distinct_pairs": len({var_pair(space, *q) for q in qs}),
                        "redundancy": redundancy(space, qs),
                        "questions": [f"{g}|{o}" for g, o in qs]}
                 for name, qs in cells.items()}

    # --- the real world, whole space, once -------------------------------------------
    full, preps, group_cols = real_battery(space, records, questions, breaks, "full")
    all_keys = [f"{g}|{o}" for g, o in questions]
    raw = [k for k in all_keys if full.get(k) and full[k]["p"] is not None
           and full[k]["p"] < ALPHA and not full[k]["failures"]]
    bh_all, n_all = bh_over(full, all_keys)

    # P4: the same evidence, corrected over the deduplicated space. The representative of
    # each unordered pair is its FIRST appearance in canonical order - fixed by the order,
    # not by which of the two has the smaller p.
    seen, dedup_keys = set(), []
    for g, o in questions:
        vp = var_pair(space, g, o)
        if vp in seen:
            continue
        seen.add(vp)
        dedup_keys.append(f"{g}|{o}")
    bh_dedup, n_dedup = bh_over(full, dedup_keys)

    # --- the real world, per cell ------------------------------------------------------
    real_cells = {}
    for name, qs in cells.items():
        keys = [f"{g}|{o}" for g, o in qs]
        bh_c, n_c = bh_over(full, keys)
        real_cells[name] = {
            "raw_findings": sum(1 for k in keys if k in raw),
            "bh_survivors": len(bh_c),
            "bh_denominator": n_c,
        }

    nulls, per_question_null, null_seconds = null_sweep(space, records, cells, preps, group_cols,
                                                        args.replicates, args.seed, breaks)

    # --- K2, the comparability check --------------------------------------------------
    k2 = {
        "questions_is_66": len(questions) == 66,
        "distinct_pairs_is_51": distinct_full == 51,
        "full_space_per_test_rate": nulls["lean@66"]["per_test_rate"],
        "session150_ci": [0.0466, 0.0512],
        "inside_session150_ci": 0.0466 <= nulls["lean@66"]["per_test_rate"] <= 0.0512,
    }

    results = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "space": args.space,
        "corpus": {"records": len(records), "fetched_utc": corpus["fetched_utc"],
                   "source": corpus["source"], "per_stratum": corpus["returned_per_category"]},
        "questions": len(questions),
        "distinct_pairs": distinct_full,
        "alpha": ALPHA, "bh_q": BH_Q,
        "replicates": args.replicates, "seed": args.seed,
        "null_seconds": null_seconds,
        "k_values": K_VALUES,
        "cells": cell_meta,
        "null": nulls,
        "real": real_cells,
        "real_full_space": {
            "raw_findings": len(raw),
            "bh_survivors_all66": len(bh_all),
            "bh_denominator_all66": n_all,
            "bh_survivors_dedup51": len(bh_dedup),
            "bh_denominator_dedup51": n_dedup,
            "dedup_only": sorted(bh_dedup - bh_all),
            "all66_only": sorted(bh_all - bh_dedup),
            # P4's real question: how many DISTINCT claims survive, either way.
            "distinct_pairs_among_bh_all66": len({var_pair(space, *k.split("|")) for k in bh_all}),
            "distinct_pairs_among_bh_dedup51": len({var_pair(space, *k.split("|")) for k in bh_dedup}),
            "distinct_pairs_among_raw": len({var_pair(space, *k.split("|")) for k in raw}),
        },
        "per_question_null_rate": per_question_null,
        "review_kills": sum(1 for k in all_keys if full.get(k) and full[k]["failures"]),
        "K2": k2,
        "breaks": breaks,
        "tests": {k: {kk: v[kk] for kk in ("test", "n1", "n0", "z", "p", "effect", "effect_kind",
                                           "summary1", "summary0", "summary_kind", "failures",
                                           "var_pair")}
                  for k, v in full.items()},
    }
    with open(args.out, "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    print(f"real: {len(raw)} raw, BH {len(bh_all)}/{n_all} all-66 vs {len(bh_dedup)}/{n_dedup} dedup-51 · "
          f"null@66 {nulls['lean@66']['mean']:.2f}/run ({nulls['lean@66']['per_test_rate']*100:.2f} %) · "
          f"K2 {k2['inside_session150_ci']} · breaks {len(breaks)} · {null_seconds}s",
          file=sys.stderr)


if __name__ == "__main__":
    main()
