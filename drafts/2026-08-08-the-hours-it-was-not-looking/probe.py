#!/usr/bin/env python3
"""probe.py — the two pre-registered controls (C-A, C-B) against the host itself.

The manifest is GDELT's self-report. These probes ask the file host directly, because
"the manifest does not list it" and "the instrument published nothing" are two different
claims and only the second is worth reporting.

  C-A  40 manifest entries drawn at random (fixed seed) -> HTTP HEAD, compare the host's
       content-length to the size the manifest claims.
  C-B  20 missing cycles drawn at random (fixed seed)   -> HTTP HEAD on the .export.CSV.zip
       URL the cycle would have had. Not-found means the omission is a real absence.
  C-C  every 15-minute cycle of the longest gap is probed exhaustively, not sampled,
       because a single load-bearing window deserves a census of its own.

Specified in PREREGISTRATION-1.md (C-A, C-B) before any number was computed; C-C was added
after the census located the longest gap and is labelled as such — it is a verification of
one window, not a scored prediction.

Usage: python3 probe.py <manifest> <census-dir> <out.json>
"""

from __future__ import annotations

import json
import random
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

SEED = 20260808          # fixed before the draw
BASE = "http://data.gdeltproject.org/gdeltv2/"
TIMEOUT = 45


def head(url):
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return {"url": url, "status": r.status,
                    "content_length": int(r.headers.get("content-length", -1)),
                    "last_modified": r.headers.get("last-modified")}
    except urllib.error.HTTPError as e:
        return {"url": url, "status": e.code, "content_length": None, "last_modified": None}
    except Exception as e:                                  # network/DNS/reset
        return {"url": url, "status": None, "error": type(e).__name__ + ": " + str(e)[:120]}


def main():
    manifest, census_dir, out = sys.argv[1], sys.argv[2], sys.argv[3]
    rng = random.Random(SEED)

    # ---- C-A: does the host agree with the manifest? -----------------------------------
    entries = []
    with open(manifest, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            p = line.split()
            if len(p) == 3 and p[0].isdigit():
                entries.append((int(p[0]), p[2]))
    sample_a = rng.sample(entries, 40)
    with ThreadPoolExecutor(max_workers=8) as ex:
        got_a = list(ex.map(lambda e: head(e[1]), sample_a))
    ca = []
    for (claimed, url), r in zip(sample_a, got_a):
        ca.append({**r, "claimed_bytes": claimed,
                   "match": r.get("status") == 200 and r.get("content_length") == claimed})
    ca_ok = sum(1 for r in ca if r["match"])
    ca_err = sum(1 for r in ca if r.get("status") is None)

    # ---- C-B: is a missing manifest line a missing file? --------------------------------
    census = json.load(open(f"{census_dir}/census.json"))
    gaps = json.load(open(f"{census_dir}/gaps.json"))["gap_runs"]
    first = datetime.strptime(census["first_cycle"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    missing = []
    for g in gaps:
        s = datetime.strptime(g["start"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        for i in range(g["cycles"]):
            missing.append(s + timedelta(minutes=15 * i))
    assert missing and first <= missing[0]
    sample_b = rng.sample(missing, 20)
    urls_b = [BASE + t.strftime("%Y%m%d%H%M%S") + ".export.CSV.zip" for t in sample_b]
    with ThreadPoolExecutor(max_workers=8) as ex:
        cb = list(ex.map(head, urls_b))
    cb_absent = sum(1 for r in cb if r.get("status") in (403, 404))
    cb_present = sum(1 for r in cb if r.get("status") == 200)
    cb_err = sum(1 for r in cb if r.get("status") is None)

    # ---- C-C: the longest gap, exhaustively ---------------------------------------------
    lg = census["longest_gap"]
    s = datetime.strptime(lg["start"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    cc_urls = []
    for i in range(lg["cycles"]):
        t = s + timedelta(minutes=15 * i)
        cc_urls.append(BASE + t.strftime("%Y%m%d%H%M%S") + ".export.CSV.zip")
    with ThreadPoolExecutor(max_workers=12) as ex:
        cc = list(ex.map(head, cc_urls))
    cc_absent = sum(1 for r in cc if r.get("status") in (403, 404))
    cc_present = sum(1 for r in cc if r.get("status") == 200)
    cc_err = sum(1 for r in cc if r.get("status") is None)

    # boundary check: the cycles either side of the gap must be present on the host
    edge = [head(BASE + (s - timedelta(minutes=15)).strftime("%Y%m%d%H%M%S") + ".export.CSV.zip"),
            head(BASE + (s + timedelta(minutes=15 * lg["cycles"])).strftime("%Y%m%d%H%M%S")
                 + ".export.CSV.zip")]

    result = {
        "seed": SEED,
        "C_A": {"n": len(ca), "size_matches": ca_ok, "probe_failures": ca_err, "detail": ca},
        "C_B": {"n": len(cb), "absent": cb_absent, "present": cb_present,
                "probe_failures": cb_err, "detail": cb},
        "C_C": {"window": lg, "n": len(cc), "absent": cc_absent, "present": cc_present,
                "probe_failures": cc_err,
                "present_detail": [r for r in cc if r.get("status") == 200][:20],
                "error_detail": [r for r in cc if r.get("status") is None][:10]},
        "gap_edges": {"cycle_before": edge[0], "cycle_after": edge[1]},
    }
    json.dump(result, open(out, "w"), indent=1)
    print(json.dumps({k: (v if k in ("seed", "gap_edges") else
                          {kk: vv for kk, vv in v.items() if not kk.endswith("detail")})
                      for k, v in result.items()}, indent=1))


if __name__ == "__main__":
    main()
