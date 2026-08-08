"""UNREGISTERED PROBE (session 102) — not part of PREREGISTRATION-3B.md scoring.
Does NIST's printed-date clustering hold on a larger sample of the same frame?
250 further URLs from frames.json['nist'] (3,339 URLs), disjoint from the 80 scored.
"""
import json, random, time, re, gzip, zlib, datetime as dt, urllib.request
BASE = "/home/user/field-research/drafts/2026-08-08-does-the-date-move"
exec(open(f"{BASE}/measure3b.py").read().replace("\nmain()\n", "\n"))  # reuse fetch/parse

frame = json.load(open(f"{BASE}/frames.json"))["nist"]
scored = {r["url"] for r in json.load(open(f"{BASE}/observations-3b.json"))["rows"]
          if r["authority"] == "nist"}
pool = sorted(set(frame) - scored)
rng = random.Random(20260808)
sample = rng.sample(pool, 250)

out = {"probe": "nist printed-date clustering at larger n (UNREGISTERED)",
       "frame_size": len(frame), "pool": len(pool), "n": len(sample),
       "seed": 20260808, "fetch_date_utc": dt.date.today().isoformat(), "rows": []}
for i, url in enumerate(sample, 1):
    rec = {"url": url}
    try:
        st, body, hdr = fetch(url)
        got = parse(body.decode("utf-8", "replace"), "nist")
        rec["status"] = "MEASURED" if got else "UNMEASURED-SELECTOR-NOT-FOUND"
        if got:
            rec.update({k: got[k] for k in ("v_updated", "v_published")})
    except Exception as e:
        rec["status"] = "UNMEASURED-FETCH-FAILED"
        rec["error"] = repr(e)[:160]
    out["rows"].append(rec)
    if i % 50 == 0:
        print(i, flush=True)
    time.sleep(0.7)
json.dump(out, open(f"{BASE}/probe-nist-scale.json", "w"), indent=1)
print("done", sum(1 for r in out["rows"] if r["status"] == "MEASURED"), "/", len(sample), flush=True)
