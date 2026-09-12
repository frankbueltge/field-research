#!/usr/bin/env python3
"""Post-hoc, declared: how much of 'this description identifies its record' is just catalogue size?

Session 158, cycle 003. This file is NOT part of the pre-registered analysis. It was written after
the pre-registered numbers were seen, to measure a confound this practice found in its own
Instrument 1 during the session: the narrowing set is an intersection of posting lists inside the
catalogue itself, so the SAME text identifies its record less often in a bigger catalogue.

The pre-registered scoring lives in tools/identify/score.py and is untouched by this file. Nothing
computed here scores a prediction.

Method: draw seeded random subsamples of data.gov.uk at a ladder of sizes, re-run the frozen
narrowing instrument (identical parameters: df cutoff 0.10, 3 rarest tokens) inside each subsample,
and report the share of records that fail to identify themselves. The home arm (N = 521) is the
comparison point at the bottom of the ladder.

Extended 2026-09-12, after an adversary objected that the page asserted the screen's duplicate rule
was size-dependent too, by analogy, having measured only the narrowing instrument. The same ladder
now also recomputes R4 and hollow_broad inside each subsample, rules untouched.

No model is called anywhere in this file. Standard library only.

Usage:
    python3 tools/identify/sizecurve.py --cache /path/to/cache
"""

from __future__ import annotations

import argparse
import json
import os
import random
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from identify import narrowing, N_RAREST, COMMON_DF_FRACTION  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hollow"))
import hollow  # noqa: E402

OUT = "artifacts/cycle-003/2026-09-12-what-a-description-is-for/data"
SEED = 20260912
LADDER = [521, 1000, 2000, 4000, 8000, 16000, 32000, 67205]
REPEATS = 5


def load_masked(cache: str, arm: str) -> list[str]:
    out = []
    with open(os.path.join(cache, f"{arm}-recs.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                out.append(json.loads(line)["masked"])
    return out


def load_raw(cache: str, arm: str) -> list[dict]:
    out = []
    with open(os.path.join(cache, f"{arm}-recs.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                r = json.loads(line)
                out.append({"text": r["text"], "r1": r["r1_chrome"], "r2": r["r2_truncated_tail"],
                            "r3": r["r3_truncated_head"]})
    return out


def screen_rates(sub: list[dict]) -> tuple[float, float]:
    """R4 and hollow_broad recomputed INSIDE the subsample, rules untouched.

    R4 is a duplicate test against the catalogue, so it must be recomputed against the subsample —
    which is the whole point: the question is whether the rule's rate depends on how many records
    are in the room. R1-R3 are properties of the value alone and are carried unchanged.
    """
    dupes = hollow.duplicate_keys([r["text"] for r in sub])
    n = len(sub)
    r4 = sum(1 for r in sub if hollow.norm(r["text"]).casefold() in dupes)
    broad = sum(1 for r in sub if r["r1"] or r["r2"] or r["r3"]
                or hollow.norm(r["text"]).casefold() in dupes)
    return 100.0 * r4 / n, 100.0 * broad / n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    args = ap.parse_args()

    uk = load_masked(args.cache, "uk")
    atlas = load_masked(args.cache, "atlas")
    uk_raw = load_raw(args.cache, "uk")

    rows = []
    for n in LADDER:
        if n > len(uk):
            continue
        reps = 1 if n == len(uk) else REPEATS
        vals, nothing, r4s, broads = [], [], [], []
        for r in range(reps):
            idx = (random.Random(SEED + 31 * r).sample(range(len(uk)), n)
                   if n < len(uk) else list(range(len(uk))))
            nr = narrowing([uk[i] for i in idx])
            vals.append(100.0 * sum(1 for x in nr if not x["identifies_uniquely"]) / n)
            nothing.append(100.0 * sum(1 for x in nr if x["identifies_nothing"]) / n)
            a, b = screen_rates([uk_raw[i] for i in idx])
            r4s.append(a)
            broads.append(b)
        rows.append({
            "n": n, "repeats": reps,
            "not_unique_pct": round(statistics.mean(vals), 2),
            "not_unique_pct_sd": round(statistics.stdev(vals), 3) if reps > 1 else None,
            "identifies_nothing_pct": round(statistics.mean(nothing), 2),
            "r4_duplicate_pct": round(statistics.mean(r4s), 2),
            "hollow_broad_pct": round(statistics.mean(broads), 2),
        })
        print(f"  uk n={n:>6}  not-unique {rows[-1]['not_unique_pct']:>6} %  "
              f"R4 {rows[-1]['r4_duplicate_pct']:>6} %  broad {rows[-1]['hollow_broad_pct']:>6} %",
              file=sys.stderr)

    home = narrowing(atlas)
    home_row = {"n": len(atlas), "repeats": 1,
                "not_unique_pct": round(100.0 * sum(1 for x in home
                                                    if not x["identifies_uniquely"]) / len(atlas), 2),
                "identifies_nothing_pct": round(100.0 * sum(1 for x in home
                                                            if x["identifies_nothing"]) / len(atlas), 2)}

    at_521 = next((r for r in rows if r["n"] == 521), None)
    top = rows[-1]
    out = {
        "_status": "POST-HOC, DECLARED. Written after the pre-registered numbers were seen. "
                   "Scores no prediction. The pre-registered analysis is tools/identify/score.py.",
        "_question": "How much of Instrument 1's reading is catalogue size rather than description "
                     "quality?",
        "params": {"seed": SEED, "repeats_per_size": REPEATS,
                   "common_df_fraction": COMMON_DF_FRACTION, "n_rarest": N_RAREST},
        "uk_ladder": rows,
        "home_at_its_own_size": home_row,
        "comparison_at_n_521": {
            "uk_subsampled": at_521["not_unique_pct"] if at_521 else None,
            "uk_subsampled_sd": at_521["not_unique_pct_sd"] if at_521 else None,
            "home": home_row["not_unique_pct"],
            "uk_at_full_size": top["not_unique_pct"] if rows else None,
        },
        "is_the_screen_itself_size_dependent": {
            "_why": "An adversary objected on 2026-09-12 that the page asserted 'so is duplication' "
                    "by analogy, having measured only the narrowing instrument. So it is measured "
                    "here, on the same ladder, with the frozen rules untouched.",
            "r4_duplicate_pct_at_521": at_521["r4_duplicate_pct"] if at_521 else None,
            "r4_duplicate_pct_at_full": top["r4_duplicate_pct"],
            "r4_ratio_full_over_521": (round(top["r4_duplicate_pct"] / at_521["r4_duplicate_pct"], 2)
                                       if at_521 and at_521["r4_duplicate_pct"] else None),
            "hollow_broad_pct_at_521": at_521["hollow_broad_pct"] if at_521 else None,
            "hollow_broad_pct_at_full": top["hollow_broad_pct"],
            "r1_r3_are_size_free": "R1, R2 and R3 are properties of a single value and cannot move "
                                   "with catalogue size; any movement in hollow_broad across the "
                                   "ladder is R4's alone.",
        },
    }
    json.dump(out, open(os.path.join(OUT, "size-curve.json"), "w"), indent=2, ensure_ascii=False)
    print(json.dumps(out["comparison_at_n_521"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
