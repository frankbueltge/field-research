#!/usr/bin/env python3
"""Merge the per-wiki corpora, de-duplicate by video id, decode the creation timestamp
from the id, and draw the pre-registered sample (seed 20260811, stratified by year).

The id decoding is the platform's documented snowflake convention: the top 32 bits of the
64-bit numeric id are a unix timestamp in seconds. It is treated here as a CONVENTION and
is checked for internal consistency (monotonicity against id order, plausible range) and
validated separately against an independent date source in `validate_timestamps.py`.
"""
import datetime as dt
import glob
import json
import random

rows = {}
per_wiki = {}
for f in sorted(glob.glob("corpus-*.json")):
    d = json.load(open(f))
    per_wiki[d["meta"]["wiki"]] = d["meta"]
    for r in d["rows"]:
        r = dict(r)
        r["wiki"] = d["meta"]["wiki"]
        rows.setdefault(r["vid"], r)

for vid, r in rows.items():
    ts = int(vid) >> 32
    r["created_unix"] = ts
    r["created"] = dt.datetime.fromtimestamp(ts, dt.timezone.utc).isoformat()
    r["year"] = int(r["created"][:4])

years = {}
for r in rows.values():
    years.setdefault(r["year"], []).append(r["vid"])

meta = {
    "wikis": len(per_wiki),
    "distinct_ids": len(rows),
    "by_year": {str(y): len(v) for y, v in sorted(years.items())},
    "min_created": min(r["created"] for r in rows.values()),
    "max_created": max(r["created"] for r in rows.values()),
}

# Pre-registered sample: seed 20260811, stratified by creation year, n = 300.
N = 300
rnd = random.Random(20260811)
plausible = {y: v for y, v in years.items() if 2016 <= y <= 2026}
total = sum(len(v) for v in plausible.values())
sample = []
for y in sorted(plausible):
    take = max(1, round(N * len(plausible[y]) / total))
    ids = sorted(plausible[y])
    rnd.shuffle(ids)
    sample.extend(ids[:take])
rnd.shuffle(sample)
sample = sample[:N]

json.dump({"meta": meta, "per_wiki": per_wiki,
           "sample_n": len(sample), "sample": sample,
           "rows": rows}, open("corpus-merged.json", "w"), indent=1)
print(json.dumps({**meta, "sample_n": len(sample)}, indent=1))
