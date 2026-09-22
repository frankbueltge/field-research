#!/usr/bin/env python3
"""Assemble the committed evidence of session 167 from the 32 scored variants.

Usage: analyse.py <runs_dir> <variants_index.json> <spdx_dir> <c2_dir> <out_dir>

Writes lattice.json, interactions.json, headline.json, corpora.json. The
adjudication, the quoted evidence, the predictions and the sources are written by
hand beside these and are NOT derived here — a reading is not a computation.

Nothing here calls a model or the network.
"""
import itertools
import json
import os
import sys

REPAIRS = ["R1", "R4", "R5", "R6", "R7"]
SHIPPED_V = "00000"


def vid(combo):
    return "".join("1" if r in combo else "0" for r in REPAIRS)


def main():
    runs, vindex, spdx_dir, c2_dir, out = sys.argv[1:6]
    idx = json.load(open(vindex))
    by = {}
    for row in idx["variants"]:
        d = json.load(open(os.path.join(runs, row["variant"] + ".json")))
        by[row["variant"]] = d
    ship = by[SHIPPED_V]
    ship_set = set(ship["real_corpus"]["delivering_repos"])

    lattice = []
    for row in sorted(idx["variants"], key=lambda r: (r["n_repairs"], r["variant"])):
        v = row["variant"]
        d = by[v]
        s = set(d["real_corpus"]["delivering_repos"])
        lattice.append({
            "variant": v,
            "repairs": row["repairs"],
            "n_repairs": row["n_repairs"],
            "digests": row["digests"],
            "fixtures_failed": d["fixtures"]["failed_ids"],
            "n_fixtures_failed": d["fixtures"]["n_fail"],
            "mutants_surviving_unexpectedly": d["mutation"]["unexpected_survivors"],
            "n_mutants_surviving_unexpectedly": len(d["mutation"]["unexpected_survivors"]),
            "decision_changing_by_relation": {
                k: n for k, n in d["metamorphic"]["decision_changing"].items() if k != "M9"},
            "decision_changing_total": d["metamorphic"]["scored_decision_total"],
            "control_M4": d["metamorphic"]["control_M4_decision"],
            "description_only_total": sum(
                n for k, n in d["metamorphic"]["description_only"].items() if k != "M9"),
            "headline_k": d["real_corpus"]["headline"]["k"],
            "headline_n": d["real_corpus"]["headline"]["n"],
            "headline_pct": d["real_corpus"]["headline"]["pct"],
            "L2": d["real_corpus"]["L2"],
            "no_holder_repos": d["real_corpus"]["no_holder_repos"],
            "delivering_gained_vs_shipped": sorted(s - ship_set),
            "delivering_lost_vs_shipped": sorted(ship_set - s),
            "delivering_symmetric_difference": len(s ^ ship_set),
        })

    # ---------------------------------------------------------------- interactions
    def val(combo, field):
        return by[vid(combo)][field[0]][field[1]] if isinstance(field, tuple) else None

    def dec(combo):
        return by[vid(combo)]["metamorphic"]["scored_decision_total"]

    def head(combo):
        return by[vid(combo)]["real_corpus"]["headline"]["k"]

    def nfix(combo):
        return by[vid(combo)]["fixtures"]["n_fail"]

    def nmut(combo):
        return len(by[vid(combo)]["mutation"]["unexpected_survivors"])

    base = {"dec": dec(()), "head": head(()), "nfix": nfix(()), "nmut": nmut(())}
    pairs = []
    for a, b in itertools.combinations(REPAIRS, 2):
        row = {"pair": [a, b]}
        for name, fn in (("dec", dec), ("head", head), ("nfix", nfix), ("nmut", nmut)):
            e_a = fn((a,)) - fn(())
            e_b = fn((b,)) - fn(())
            e_ab = fn((a, b)) - fn(())
            row[name] = {"alone_a": e_a, "alone_b": e_b, "joint": e_ab,
                         "additive_prediction": e_a + e_b,
                         "interaction": e_ab - (e_a + e_b),
                         "value_none": fn(()), "value_a": fn((a,)),
                         "value_b": fn((b,)), "value_ab": fn((a, b))}
        pairs.append(row)

    # marginal effect of each repair in every context, on the violation total
    marginals = []
    for r in REPAIRS:
        others = [x for x in REPAIRS if x != r]
        rows = []
        for k in range(len(others) + 1):
            for ctx in itertools.combinations(others, k):
                rows.append({"context": list(ctx),
                             "without": dec(ctx),
                             "with": dec(tuple(sorted(set(ctx) | {r}))),
                             "marginal": dec(tuple(sorted(set(ctx) | {r}))) - dec(ctx)})
        vals = sorted({x["marginal"] for x in rows})
        marginals.append({"repair": r, "n_contexts": len(rows),
                          "distinct_marginal_values": vals,
                          "min": min(vals), "max": max(vals),
                          "sign_changes": not (all(v <= 0 for v in vals)
                                               or all(v >= 0 for v in vals)),
                          "contexts": rows})

    inter = {
        "note": "Session 167. Interaction is measured as joint effect minus the sum of the two "
                "single effects, on each of four outcomes. A repair whose effect depends on "
                "which other repairs are applied is not a local change to a rule.",
        "baseline_no_repair": base,
        "pairs": pairs,
        "marginal_effects_on_violations": marginals,
    }

    # ---------------------------------------------------------------- headline table
    groups = {}
    for row in lattice:
        key = (row["headline_k"], tuple(row["delivering_gained_vs_shipped"]),
               tuple(row["delivering_lost_vs_shipped"]))
        groups.setdefault(key, []).append(row["variant"])
    headline = {
        "note": "Session 167. The published headline of 2026-09-18 under every repair subset. "
                "The number and the membership are reported separately: a subset can leave the "
                "count untouched and change which repositories it counts.",
        "published_2026_09_18": {"k": 100, "n": 105, "pct": 95.2},
        "distinct_outcomes": [
            {"k": k, "pct": round(100.0 * k / 105, 1),
             "gained_vs_shipped": list(g), "lost_vs_shipped": list(l),
             "n_variants": len(vs), "variants": sorted(vs)}
            for (k, g, l), vs in sorted(groups.items(), key=lambda x: (-x[0][0], x[0]))
        ],
    }

    c1 = json.load(open(os.path.join(spdx_dir, "manifest.json")))
    c2 = json.load(open(os.path.join(c2_dir, "manifest.json")))
    corpora = {
        "note": "Session 167. Both corpora re-fetched tonight and checked against the digests "
                "pinned on 2026-09-19 (C1) and 2026-09-18 (C2). No licence body is committed.",
        "C1": {"source": c1["source"], "license_list_version": c1["license_list_version"],
               "n": c1["fetched_ids"], "texts_ok": c1["texts_ok"],
               "corpus_digest": c1["corpus_digest"],
               "corpus_digest_2026_09_20": "73363f6622045c5a4cebc39af0bedf3bbe5cc5f212549a56aae249cdcf8315ec"},
        "C2": {"n_pinned": c2["n_pinned"], "n_fetched": c2["n_fetched"],
               "n_digest_matches": c2["n_digest_matches"], "excluded": c2["excluded"],
               "corpus_digest": c2["corpus_digest"],
               "corpus_digest_2026_09_20": "6ef7a964dd960b957ce07668f5f7e78b3e4af6ae6db824f4cda637e87ed43a31"},
        "total_inputs": c1["fetched_ids"] + c2["n_digest_matches"],
    }

    os.makedirs(out, exist_ok=True)
    for name, obj in (("lattice.json", {
            "note": "Session 167. Every repair subset of the 2026-09-18 licence rule, through "
                    "all four test regimes of the pre-registration. Variant ids read "
                    "R1,R4,R5,R6,R7 left to right; 00000 is the shipped rule with the pipeline "
                    "block installed and every flag off, verified output-identical to the "
                    "shipped file over all 896 inputs.",
            "repairs": REPAIRS, "shipped_digests": idx["shipped_digests"],
            "n_variants": len(lattice), "variants": lattice}),
            ("interactions.json", inter), ("headline.json", headline),
            ("corpora.json", corpora)):
        json.dump(obj, open(os.path.join(out, name), "w"), indent=1, ensure_ascii=False)

    print(json.dumps({
        "variants": len(lattice),
        "violation_totals": sorted({r["decision_changing_total"] for r in lattice}),
        "headline_values": sorted({r["headline_k"] for r in lattice}),
        "distinct_headline_outcomes": len(headline["distinct_outcomes"]),
        "repairs_with_sign_changing_marginals": [m["repair"] for m in marginals
                                                 if m["sign_changes"]],
        "pairs_with_nonzero_dec_interaction": [
            p["pair"] for p in pairs if p["dec"]["interaction"] != 0],
        "pairs_with_nonzero_mut_interaction": [
            p["pair"] for p in pairs if p["nmut"]["interaction"] != 0],
    }, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
