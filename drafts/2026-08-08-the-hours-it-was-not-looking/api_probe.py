#!/usr/bin/env python3
"""api_probe.py — C-IV: does a free second copy of the same instrument show the absence?

The adversary's condition C-IV names one second copy (a commercial cloud data warehouse)
that this practice has no credential for. The condition's actual question is broader, and
this asks it of a copy anyone can reach with no credential at all: the organisation's own
public article-index API, which returns a timeline at 15-minute resolution for short
spans and, as measured here, simply omits quarter-hours it has no rows for.

Two uses:
  * `window`  — the timeline across a named window, listing which quarter-hours the API
                returns and which it omits;
  * `sweep`   — walk a long period in fixed-length spans and collect every omitted
                quarter-hour, to test whether the *complete* negative is free as well.

Politeness: this host rate-limits (observed HTTP 429 on the second call of the session).
One request at a time, a fixed pause between calls, exponential backoff on 429, and every
unresolved call recorded rather than inferred.

Usage: api_probe.py window <startYYYYMMDDHHMMSS> <end> <out.json> [query]
       api_probe.py sweep  <start> <end> <span_hours> <out.json> [query]
"""

from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.gdeltproject.org/api/v2/doc/doc"
PAUSE = 6.0            # seconds between calls, deliberately slow
MAX_TRIES = 5
FMT = "%Y%m%d%H%M%S"


def call(start, end, query, mode):
    qs = urllib.parse.urlencode({"query": query, "mode": mode, "startdatetime": start,
                                 "enddatetime": end, "format": "json"})
    url = f"{API}?{qs}"
    for attempt in range(MAX_TRIES):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read().decode("utf-8", "replace")
            time.sleep(PAUSE)
            return json.loads(body), None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(PAUSE * (attempt + 2))
                continue
            return None, f"HTTP {e.code}"
        except Exception as e:
            time.sleep(PAUSE * (attempt + 1))
            err = type(e).__name__ + ": " + str(e)[:120]
    return None, err if 'err' in dir() else "unresolved"


def buckets(start, end):
    t = datetime.strptime(start, FMT).replace(tzinfo=timezone.utc)
    e = datetime.strptime(end, FMT).replace(tzinfo=timezone.utc)
    out = []
    while t <= e:
        out.append(t.strftime(FMT))
        t += timedelta(minutes=15)
    return out


def present_set(doc):
    got = set()
    res = (doc.get("query_details") or {}).get("date_resolution")
    for s in doc.get("timeline", []):
        for x in s.get("data", []):
            got.add(x["date"].replace("T", "").replace("Z", ""))
    return got, res


def main():
    cmd = sys.argv[1]
    if cmd == "window":
        start, end, out = sys.argv[2], sys.argv[3], sys.argv[4]
        query = sys.argv[5] if len(sys.argv) > 5 else "news"
        doc, err = call(start, end, query, "timelinevolraw")
        if doc is None:
            doc, err2 = call(start, end, query, "timelinevol")
            mode = "timelinevol"
        else:
            mode = "timelinevolraw"
        if doc is None:
            json.dump({"error": err, "start": start, "end": end}, open(out, "w"), indent=1)
            print("UNRESOLVED", err)
            return
        got, res = present_set(doc)
        exp = buckets(start, end)
        missing = [b for b in exp if b not in got]
        json.dump({"start": start, "end": end, "query": query, "mode": mode,
                   "date_resolution": res, "expected": len(exp), "returned": len(got),
                   "missing_count": len(missing), "missing": missing,
                   "raw_series": doc.get("timeline", [])},
                  open(out, "w"), indent=1)
        print(f"{start}->{end} res={res} expected={len(exp)} returned={len(got)} "
              f"missing={len(missing)}")
        if missing:
            print("  first/last missing:", missing[0], missing[-1])
    elif cmd == "sweep":
        start, end, span_h, out = sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
        query = sys.argv[6] if len(sys.argv) > 6 else "news"
        t = datetime.strptime(start, FMT).replace(tzinfo=timezone.utc)
        e = datetime.strptime(end, FMT).replace(tzinfo=timezone.utc)
        rows, missing_all, unresolved = [], [], []
        fh = open(out, "w", encoding="utf-8")
        n = 0
        while t < e:
            t2 = min(t + timedelta(hours=span_h), e)
            s1, s2 = t.strftime(FMT), t2.strftime(FMT)
            doc, err = call(s1, s2, query, "timelinevolraw")
            if doc is None:
                unresolved.append([s1, s2, err])
                fh.write(json.dumps({"k": "unresolved", "start": s1, "end": s2, "err": err}) + "\n")
            else:
                got, res = present_set(doc)
                exp = buckets(s1, s2)
                miss = [b for b in exp if b not in got]
                fh.write(json.dumps({"k": "span", "start": s1, "end": s2, "res": res,
                                     "expected": len(exp), "returned": len(got),
                                     "missing": miss}) + "\n")
                missing_all.extend(miss)
                if res != "15m":
                    fh.write(json.dumps({"k": "warn", "start": s1, "res": res}) + "\n")
            n += 1
            if n % 20 == 0:
                fh.flush()
                print(f"  {s1} spans={n} missing_so_far={len(missing_all)} "
                      f"unresolved={len(unresolved)}", flush=True)
            t = t2
        fh.write(json.dumps({"k": "footer", "spans": n, "missing_total": len(missing_all),
                             "unresolved": len(unresolved)}) + "\n")
        fh.close()
        print(json.dumps({"spans": n, "missing_total": len(missing_all),
                          "unresolved": len(unresolved)}, indent=1))


if __name__ == "__main__":
    main()
