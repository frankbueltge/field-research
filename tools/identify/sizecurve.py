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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    args = ap.parse_args()

    uk = load_masked(args.cache, "uk")
    atlas = load_masked(args.cache, "atlas")

    rows = []
    for n in LADDER:
        if n > len(uk):
            continue
        reps = 1 if n == len(uk) else REPEATS
        vals, nothing = [], []
        for r in range(reps):
            sub = random.Random(SEED + 31 * r).sample(uk, n) if n < len(uk) else uk
            nr = narrowing(sub)
            vals.append(100.0 * sum(1 for x in nr if not x["identifies_uniquely"]) / n)
            nothing.append(100.0 * sum(1 for x in nr if x["identifies_nothing"]) / n)
        rows.append({
            "n": n, "repeats": reps,
            "not_unique_pct": round(statistics.mean(vals), 2),
            "not_unique_pct_sd": round(statistics.stdev(vals), 3) if reps > 1 else None,
            "identifies_nothing_pct": round(statistics.mean(nothing), 2),
        })
        print(f"  uk n={n:>6}  not-unique {rows[-1]['not_unique_pct']:>6} %", file=sys.stderr)

    home = narrowing(atlas)
    home_row = {"n": len(atlas), "repeats": 1,
                "not_unique_pct": round(100.0 * sum(1 for x in home
                                                    if not x["identifies_uniquely"]) / len(atlas), 2),
                "identifies_nothing_pct": round(100.0 * sum(1 for x in home
                                                            if x["identifies_nothing"]) / len(atlas), 2)}

    at_521 = next((r for r in rows if r["n"] == 521), None)
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
            "uk_at_full_size": rows[-1]["not_unique_pct"] if rows else None,
        },
    }
    json.dump(out, open(os.path.join(OUT, "size-curve.json"), "w"), indent=2, ensure_ascii=False)
    print(json.dumps(out["comparison_at_n_521"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
