"""Retry pass: the archive reset the connection on the last 84 queries of the census run (all of
energy.gov and the tail of GOV.UK) -- a rate limit reached after ~250 requests, not a property of
those URLs. Single-threaded, with a pause, so the retry is not the same mistake again."""
import json, time, sys
sys.path.insert(0, "/home/user/field-research/drafts/2026-08-08-does-the-date-move")
from census_timemap import measure, BASE

cache = json.load(open(f"{BASE}/census-timemap-partial.json"))
bad = [u for u, r in cache.items() if "error" in r]
print(f"{len(bad)} URLs to retry", flush=True)
fixed = 0
for i, u in enumerate(bad, 1):
    r = measure(u)
    cache[u] = r
    if "error" not in r:
        fixed += 1
    if i % 10 == 0:
        json.dump(cache, open(f"{BASE}/census-timemap-partial.json", "w"))
        print(f"  [{i}/{len(bad)}] fixed={fixed}", flush=True)
    time.sleep(1.5)
json.dump(cache, open(f"{BASE}/census-timemap-partial.json", "w"))
print(f"retry done: {fixed}/{len(bad)} recovered", flush=True)
