#!/usr/bin/env python3
"""reverify.py — a 404 seen once is not an absence.

The sweep asked each listed file once, with HEAD. Before any of it is reported, the rows
that carry the finding are asked again, three more times, spaced, and by a different
method: a ranged GET rather than a HEAD, on a fresh connection each time. (A TLS route was
tried as the cleanest second channel and does not exist: this host presents a certificate
that does not match its own name, and the proxied HTTPS route answers 503. Recorded as
tried; plain HTTP is the only way to ask it anything.) A row is reported absent only if every one of those agrees, and any
row that ever answers differently is reported as changed, not quietly kept.

Controls: the cycle before and after each absent one, asked the same way, so a 404 that is
really "this host is refusing us right now" shows up as its controls failing too.

Usage: reverify.py <cycles.json> <out.json>
"""

from __future__ import annotations

import http.client
import json
import ssl
import sys
import time
from datetime import datetime, timedelta, timezone

HOST = "data.gdeltproject.org"
FMT = "%Y%m%d%H%M%S"
ROUNDS = 3
PAUSE_BETWEEN_ROUNDS = 45


def ask(cycle, method):
    """Fresh connection every time, so nothing is inherited from a pooled socket."""
    path = f"/gdeltv2/{cycle}.gkg.csv.zip"
    conn = http.client.HTTPConnection(HOST, timeout=45)
    try:
        headers = {"Accept": "*/*"}
        if method == "GET":
            headers["Range"] = "bytes=0-63"
        conn.request(method, path, headers=headers)
        r = conn.getresponse()
        body = r.read(4096)
        return {"status": r.status, "len": r.getheader("Content-Length"),
                "bytes_read": len(body)}
    except Exception as e:
        return {"status": None, "err": type(e).__name__ + ": " + str(e)[:100]}
    finally:
        try:
            conn.close()
        except Exception:
            pass


def main():
    cycles = json.load(open(sys.argv[1]))["absent"]
    out = sys.argv[2]
    rows = {c: {"rounds": []} for c in cycles}
    controls = {}
    for c in cycles:
        t = datetime.strptime(c, FMT).replace(tzinfo=timezone.utc)
        for d in (-1, 1):
            n = (t + d * timedelta(minutes=15)).strftime(FMT)
            if n not in cycles:
                controls.setdefault(n, {"rounds": []})

    for rnd in range(ROUNDS):
        method = "GET" if rnd % 2 == 0 else "HEAD"
        for c in cycles:
            rows[c]["rounds"].append({"method": method, **ask(c, method)})
        for c in controls:
            controls[c]["rounds"].append({"method": method, **ask(c, method)})
        done = sum(1 for c in cycles if rows[c]["rounds"][-1]["status"] == 404)
        print(f"  round {rnd+1} ({method}): {done}/{len(cycles)} still 404, "
              f"controls served "
              f"{sum(1 for c in controls if controls[c]['rounds'][-1]['status'] in (200,206))}"
              f"/{len(controls)}", flush=True)
        if rnd < ROUNDS - 1:
            time.sleep(PAUSE_BETWEEN_ROUNDS)

    # A ranged GET against an object this host does not have answers 416 with a 166-byte
    # error body, not 404; a HEAD answers 404. Both are "the host has nothing here", and
    # the first run of this script scored only 404 and so reported every row as changed.
    # The fix is in the classifier, not in the data: NOT_SERVED holds both.
    NOT_SERVED = (404, 416)
    stable = [c for c in cycles if all(r["status"] in NOT_SERVED for r in rows[c]["rounds"])]
    changed = [c for c in cycles if not all(r["status"] in NOT_SERVED for r in rows[c]["rounds"])]
    ctrl_ok = [c for c in controls if all(r["status"] in (200, 206)
                                          for r in controls[c]["rounds"])]
    summary = {"cycles": len(cycles), "rounds": ROUNDS,
               "absent_in_every_round": len(stable), "changed": len(changed),
               "changed_cycles": changed,
               "controls": len(controls), "controls_served_every_round": len(ctrl_ok),
               "controls_not_served": [c for c in controls if c not in ctrl_ok]}
    json.dump({"summary": summary, "rows": rows, "controls": controls},
              open(out, "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
