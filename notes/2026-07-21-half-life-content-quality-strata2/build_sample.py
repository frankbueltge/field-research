#!/usr/bin/env python3
"""Pre-registered sample builder — content-quality gate part 2 (Telegram + news/org).
Deterministic: fixed seed, sorted input, one RNG per stratum. Committed BEFORE any
snapshot is fetched. Reads the session-41 CDX census (frozen) and selects, per stratum,
a seeded sample of citation URLs with an in-window capture, choosing for each the
status-200 capture nearest the report's Oct-2024 publication (session-45 method)."""
import json, random, hashlib, os

SEED = 20260721               # the session date; noted so the sample is reproducible
N = 25                        # per stratum
TARGET = "20241001000000"     # report published Oct 2024; pick capture nearest this
WINDOW_LO, WINDOW_HI = "20231001000000", "20250101000000"
CDX = "../2026-07-16-half-life-archival-probe/cdx_results.json"
STRATA = ["telegram", "news-org-other"]

def nearest_in_window(caps):
    cand = [c for c in caps if c[1] == "200" and WINDOW_LO <= c[0] < WINDOW_HI]
    if not cand:
        return None
    t = int(TARGET)
    return min(cand, key=lambda c: abs(int(c[0]) - t))[0]

here = os.path.dirname(os.path.abspath(__file__))
recs = json.load(open(os.path.join(here, CDX)))

out = {"seed": SEED, "n_requested_per_stratum": N, "target_capture": TARGET,
       "window": [WINDOW_LO, WINDOW_HI], "strata": {}}

for stratum in STRATA:
    pool = []
    for r in recs:
        if r.get("stratum") != stratum or r.get("outcome") != "covered_in_window":
            continue
        ts = nearest_in_window(r.get("captures", []))
        if ts is None:
            continue
        pool.append({"url": r["url"], "capture": ts, "source": r.get("source")})
    pool.sort(key=lambda x: x["url"])          # deterministic order before sampling
    rng = random.Random(SEED)                  # one fresh RNG per stratum
    sample = rng.sample(pool, min(N, len(pool)))
    sample.sort(key=lambda x: x["url"])
    digest = hashlib.sha256(json.dumps(sample, sort_keys=True).encode()).hexdigest()
    out["strata"][stratum] = {"n_pool": len(pool), "n_sample": len(sample),
                              "sample_sha256": digest, "sample": sample}
    print(f"{stratum}: pool={len(pool)} sample={len(sample)} sha256={digest}")

json.dump(out, open(os.path.join(here, "sample.json"), "w"), indent=1)
