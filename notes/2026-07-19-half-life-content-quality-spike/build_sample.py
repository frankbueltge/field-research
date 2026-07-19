#!/usr/bin/env python3
"""Pre-registered sample builder for the Half-Life X/Twitter content-quality spike.
Deterministic: fixed seed, sorted input. Committed BEFORE any snapshot is fetched.
Reads the session-41 CDX census (frozen, sha256-checkable) and selects a seeded sample
of X/Twitter citation URLs that had an in-window capture, choosing for each the status-200
capture nearest the report's Oct-2024 publication."""
import json, random, hashlib

SEED = 20260719               # the session date; noted so the sample is reproducible
N = 25                        # sample size for the feasibility spike
TARGET = "20241001000000"     # report published Oct 2024; pick capture nearest this
WINDOW_LO, WINDOW_HI = "20231001000000", "20250101000000"
CDX = "../2026-07-16-half-life-archival-probe/cdx_results.json"

def nearest_in_window(caps):
    # caps: list of [timestamp, status]; keep status-200 in-window; nearest to TARGET
    cand = [c for c in caps if c[1] == "200" and WINDOW_LO <= c[0] < WINDOW_HI]
    if not cand:
        return None
    t = int(TARGET)
    return min(cand, key=lambda c: abs(int(c[0]) - t))[0]

import os
here = os.path.dirname(os.path.abspath(__file__))
recs = json.load(open(os.path.join(here, CDX)))
pool = []
for r in recs:
    if r.get("stratum") != "x-twitter":
        continue
    if r.get("outcome") != "covered_in_window":
        continue
    ts = nearest_in_window(r.get("captures", []))
    if ts is None:
        continue
    pool.append({"url": r["url"], "capture": ts, "source": r.get("source")})

pool.sort(key=lambda x: x["url"])          # deterministic order before sampling
rng = random.Random(SEED)
sample = rng.sample(pool, min(N, len(pool)))
sample.sort(key=lambda x: x["url"])

out = {
    "seed": SEED, "n_requested": N, "n_pool": len(pool), "n_sample": len(sample),
    "target_capture": TARGET, "window": [WINDOW_LO, WINDOW_HI],
    "sample": sample,
}
digest = hashlib.sha256(json.dumps(out["sample"], sort_keys=True).encode()).hexdigest()
out["sample_sha256"] = digest
json.dump(out, open(os.path.join(here, "sample.json"), "w"), indent=1)
print("pool size (in-window X/Twitter, 200):", len(pool))
print("sample size:", len(sample))
print("sample_sha256:", digest)
for s in sample:
    print(" ", s["capture"], s["url"])
