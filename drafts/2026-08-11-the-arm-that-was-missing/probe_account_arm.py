#!/usr/bin/env python3
"""Is the account dimension observable at all without credentials?

Session 114, pre-registered as PREREGISTRATION-114.md §5. At most 24 requests, one per
second, to public account pages — NOT to the video endpoint, and NOT to the window ledger's
population. Writes its own file; nothing here can alter a ledger run.

Twelve handles where every unit in the corpus is NOT-RETRIEVABLE, twelve where every unit is
RETRIEVABLE, largest handle first in each group, from the day-2 run. If the account route
answers differently for the two groups, the mechanism behind a missing video is observable
credential-free. If it refuses both alike, it is not, and the structure of the losses is the
only route left.

Usage: python3 probe_account_arm.py [run.json] [n_per_group]
"""
import json
import sys
import time
import urllib.error
import urllib.request

from cluster_model import load, groups

UA = "field-research/1.0 (independent research instrument; sequential, 1 req/s)"
DELAY = 1.0
TIMEOUT = 25


def pick(g, n):
    allgone, allthere = [], []
    for h, v in g.items():
        if len(v) < 2:
            continue
        a = sum(r["absent"] for r in v)
        if a == len(v):
            allgone.append((len(v), h))
        elif a == 0:
            allthere.append((len(v), h))
    allgone.sort(reverse=True)
    allthere.sort(reverse=True)
    return ([{"handle": h, "k": k, "group": "all-gone"} for k, h in allgone[:n]],
            [{"handle": h, "k": k, "group": "all-present"} for k, h in allthere[:n]])


def request(handle):
    url = f"https://www.tiktok.com/@{handle}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read()
            return {"url": url, "http": r.status, "bytes": len(body),
                    "seconds": round(time.time() - t0, 2),
                    "final_url": r.geturl(),
                    "body_head": body[:200].decode("utf-8", "replace")}
    except urllib.error.HTTPError as e:
        body = b""
        try:
            body = e.read()
        except Exception:
            pass
        return {"url": url, "http": e.code, "bytes": len(body),
                "seconds": round(time.time() - t0, 2),
                "body_head": body[:200].decode("utf-8", "replace")}
    except Exception as e:
        return {"url": url, "http": None, "error": type(e).__name__ + ": " + str(e)[:120],
                "seconds": round(time.time() - t0, 2)}


def main(run_path, n):
    d, rows, excl, key = load(run_path)
    gone, there = pick(groups(rows), n)
    targets = gone + there
    out = []
    for t in targets:
        r = request(t["handle"])
        r.update(t)
        out.append(r)
        print(json.dumps({k: r[k] for k in ("handle", "group", "k", "http", "bytes")}))
        time.sleep(DELAY)
    payload = {
        "schema": "field-research/account-route-probe/1",
        "session": 114, "run_source": run_path,
        "collected_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "endpoint": "https://www.tiktok.com/@<handle>", "user_agent": UA,
        "delay_s": DELAY, "timeout_s": TIMEOUT,
        "requests": len(out), "results": out,
    }
    json.dump(payload, open("account-route-probe-114.json", "w"), indent=1)
    codes = {}
    for r in out:
        codes[str(r.get("http"))] = codes.get(str(r.get("http")), 0) + 1
    print("status codes:", json.dumps(codes))
    print("wrote account-route-probe-114.json")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ledger/run-2026-08-12T0341Z.json",
         int(sys.argv[2]) if len(sys.argv) > 2 else 12)
