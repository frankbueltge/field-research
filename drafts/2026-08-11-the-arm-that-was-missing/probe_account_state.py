#!/usr/bin/env python3
"""The mechanism, measured instead of inferred — and the prediction is written here first.

Session 114. DEVIATION D19 from PREREGISTRATION-114.md §5, declared in this file before it was
run and committed before the first request:

  §5 authorised 24 requests to establish WHETHER the account dimension is observable
  credential-free. It is: the page is a generic shell for every handle alike (24/24 HTTP 200,
  362-366 kB, identical <title>), but it carries an embedded state field, and on the two
  handles inspected under D18 that field separated a handle whose every corpus video is gone
  (statusCode 10221, no user object) from one whose every video is retrievable (statusCode 0,
  uniqueId matching the cited handle).

  D19 therefore (a) completes the inspection over the SAME 24 pre-selected handles — no new
  handles in that group, one further request each — because the first pass stored 200 bytes of
  a 362 kB answer and could not answer its own question; and (b) adds a third group of 12
  MIXED handles (some corpus videos gone, some retrievable), which §5 did not select and
  without which the two original groups differ in more than one respect. 36 requests, one per
  second, same endpoint, same vantage.

THE PREDICTION, WRITTEN BEFORE THE RUN (P8, P9, P10):

  P8  Of the 12 all-gone handles, a MAJORITY return a non-zero statusCode with no user object,
      i.e. the account itself is unreachable. This is the mechanism claim: the videos went
      because the account went.
  P9  Of the 12 all-present handles, ALL 12 return statusCode 0 with a user object.
  P10 Of the 12 mixed handles, ALL 12 return statusCode 0 with a user object — a live account
      that has lost individual videos. If mixed handles were also account-dead, the corpus
      states would be incoherent and the whole reading would be wrong.

What is NOT claimed and cannot be: that a non-zero status means banned, deleted, renamed,
region-blocked or private. The platform publishes no code table we could find, so the state is
reported as the number the page carries and nothing is read into it beyond "the account object
is not served". Nothing here reclassifies any ledger unit (K5).

Copyright hygiene: only marker presence, the numeric status field, the returned uniqueId and
the byte count are stored. No third party's page text is written to this repository.

Usage: python3 probe_account_state.py [run.json]
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request

from cluster_model import load, groups

UA = "field-research/1.0 (independent research instrument; sequential, 1 req/s)"
DELAY = 1.0
TIMEOUT = 25
MARKERS = ["__UNIVERSAL_DATA_FOR_REHYDRATION__", "userInfo", "uniqueId", "secUid",
           "followerCount"]


def pick(g, n=12):
    gone, present, mixed = [], [], []
    for h, v in g.items():
        if len(v) < 2:
            continue
        a = sum(r["absent"] for r in v)
        if a == len(v):
            gone.append((len(v), h))
        elif a == 0:
            present.append((len(v), h))
        else:
            mixed.append((len(v), h))
    for lst in (gone, present, mixed):
        lst.sort(reverse=True)
    return ([{"handle": h, "k": k, "group": "all-gone"} for k, h in gone[:n]]
            + [{"handle": h, "k": k, "group": "all-present"} for k, h in present[:n]]
            + [{"handle": h, "k": k, "group": "mixed"} for k, h in mixed[:n]])


def probe(handle):
    req = urllib.request.Request(f"https://www.tiktok.com/@{handle}",
                                 headers={"User-Agent": UA})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            b = r.read().decode("utf-8", "replace")
            http = r.status
    except urllib.error.HTTPError as e:
        b, http = "", e.code
    except Exception as e:
        return {"http": None, "error": type(e).__name__ + ": " + str(e)[:120],
                "seconds": round(time.time() - t0, 2)}
    m = re.search(r'"statusCode"\s*:\s*(-?\d+)', b)
    u = re.search(r'"uniqueId"\s*:\s*"([^"]{1,40})"', b)
    return {"http": http, "bytes": len(b.encode()),
            "seconds": round(time.time() - t0, 2),
            "status_field": int(m.group(1)) if m else None,
            "unique_id_returned": u.group(1) if u else None,
            "markers": {k: (k in b) for k in MARKERS}}


def main(run_path):
    d, rows, excl, key = load(run_path)
    targets = pick(groups(rows))
    out = []
    for t in targets:
        r = probe(t["handle"])
        r.update(t)
        out.append(r)
        print(json.dumps({k: r.get(k) for k in
                          ("group", "handle", "k", "http", "status_field",
                           "unique_id_returned")}))
        time.sleep(DELAY)
    tab = {}
    for r in out:
        g = r["group"]
        s = r.get("status_field")
        tab.setdefault(g, {})
        tab[g][str(s)] = tab[g].get(str(s), 0) + 1
    payload = {
        "schema": "field-research/account-state-probe/1", "session": 114,
        "deviation": "D19 — see probe_account_state.py docstring, committed before the run",
        "run_source": run_path,
        "collected_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "endpoint": "https://www.tiktok.com/@<handle>", "user_agent": UA,
        "delay_s": DELAY, "timeout_s": TIMEOUT, "requests": len(out),
        "status_field_by_group": tab,
        "no_code_table_published": ("This practice found no published table mapping the "
                                    "numeric state to a cause; nothing is read into it beyond "
                                    "'the account object is not served'."),
        "results": out,
    }
    json.dump(payload, open("account-state-probe-114.json", "w"), indent=1)
    print("status field by group:", json.dumps(tab))
    print("wrote account-state-probe-114.json")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ledger/run-2026-08-12T0341Z.json")
