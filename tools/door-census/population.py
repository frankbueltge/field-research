#!/usr/bin/env python3
"""Rebuild the door census population exactly as drawn on 2026-09-01.

The draw is deterministic: census = the 30 publishers with the most expressions of
concern in the session-143 cohort; tail sample = 10 of the remaining 70, drawn with
random.Random(20260901) — the seed is the measurement date, fixed before the draw.

Usage:
    python3 tools/door-census/population.py            # write population.json
    python3 tools/door-census/population.py --check    # verify the committed file
"""
import collections
import csv
import json
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
COHORT = ROOT / "artifacts/cycle-001/2026-09-01-how-long-a-warning-stands/data/cohort.csv"
OUT = ROOT / "artifacts/cycle-001/2026-09-01-a-door-to-knock-on/data/population.json"
SEED = 20260901


def build():
    rows = list(csv.DictReader(COHORT.open()))
    counts = collections.Counter(r["publisher"] for r in rows)
    total = sum(counts.values())
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    census, tail = ranked[:30], ranked[30:]
    sample = sorted(random.Random(SEED).sample(tail, 10), key=lambda kv: (-kv[1], kv[0]))
    return {
        "generated": "2026-09-01",
        "cohort_rows": len(rows),
        "distinct_publishers": len(counts),
        "census_share_of_concerns": round(100 * sum(n for _, n in census) / total, 1),
        "seed": SEED,
        "census": [{"publisher": p, "concerns": n, "stratum": "census"} for p, n in census],
        "tail_sample": [{"publisher": p, "concerns": n, "stratum": "tail"} for p, n in sample],
    }


if __name__ == "__main__":
    built = build()
    if "--check" in sys.argv:
        have = json.loads(OUT.read_text())
        if have == built:
            print("population.json: reproduces from the cohort under seed %d" % SEED)
        else:
            print("population.json: DOES NOT reproduce — the draw or the cohort has changed")
            sys.exit(1)
    else:
        OUT.write_text(json.dumps(built, indent=2, ensure_ascii=False) + "\n")
        print("wrote", OUT)
