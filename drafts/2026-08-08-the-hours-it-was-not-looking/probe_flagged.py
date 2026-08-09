#!/usr/bin/env python3
"""UNREGISTERED follow-up: HEAD-probe every cycle the byte screen flagged, to find out
whether 'present but thin' is sometimes 'not there at all'. gkg arm only."""
import json, sys, time, urllib.error, urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

man = {}
for line in open(sys.argv[1], encoding="utf-8", errors="replace"):
    p = line.split()
    if len(p) != 3 or not p[0].isdigit():
        continue
    f = p[2].rsplit("/", 1)[-1]
    st, rest = f[:14], f[14:].lower()
    if not st.isdigit() or len(st) != 14 or rest.startswith(".translation") or not rest.startswith(".gkg"):
        continue
    try:
        ts = datetime.strptime(st, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    except ValueError:
        continue
    man[ts.strftime("%Y-%m-%dT%H:%M:%SZ")] = (int(p[0]), p[2])

d = sys.argv[2]
flag = {c["ts"] for c in json.load(open(f"{d}/collapses.json"))["collapsed_cycles"]}
flag |= {c["ts"] for c in json.load(open(f"{d}/rescreen-english.json"))["detail"]}
jobs = [(t, *man[t]) for t in sorted(flag) if t in man]

def head(j):
    ts, size, url = j
    for a in range(3):
        try:
            r = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "field-research/increment-2"})
            with urllib.request.urlopen(r, timeout=60) as resp:
                return {"ts": ts, "status": resp.status, "manifest_size": size,
                        "served": resp.headers.get("content-length"),
                        "last_modified": resp.headers.get("last-modified")}
        except urllib.error.HTTPError as e:
            return {"ts": ts, "status": e.code, "manifest_size": size}
        except Exception as e:
            if a == 2:
                return {"ts": ts, "status": None, "error": f"{type(e).__name__}", "manifest_size": size}
            time.sleep(2 * (a + 1))

t0 = time.time(); out = []
with ThreadPoolExecutor(max_workers=16) as ex:
    for i, r in enumerate(ex.map(head, jobs), 1):
        out.append(r)
        if i % 500 == 0:
            print(f"{i}/{len(jobs)} {round(time.time()-t0)}s", flush=True)
absent = [r for r in out if r["status"] == 404]
errs = [r for r in out if r["status"] is None]
mism = [r for r in out if r["status"] == 200 and r.get("served") and int(r["served"]) != r["manifest_size"]]
by_day = sorted(Counter(r["ts"][:10] for r in absent).items())
json.dump({"probed": len(out), "absent_404": len(absent), "probe_errors": len(errs),
           "served_size_disagrees": len(mism), "absent_by_day": by_day,
           "mismatch_detail": mism[:50], "absent_ts": [r["ts"] for r in absent],
           "elapsed_s": round(time.time()-t0, 1)}, open(sys.argv[3], "w"), indent=1)
print(json.dumps({"probed": len(out), "absent_404": len(absent), "probe_errors": len(errs),
                  "served_size_disagrees": len(mism), "absent_by_day": by_day}, indent=1))
