#!/usr/bin/env python3
"""sweep_unlisted.py — the other half of the negative, which increment 3 did not run.

The adversary of gate session 3 refuted the exhaustive-negative claim on its population,
not on its arithmetic: `sweep.py` asked about every cycle the index **lists**, and the
larger phenomenon this arc measured at increment 1 is the cycles the index does **not**
list at all — 7,286 English and 12,546 Translingual quarter-hours, of which exactly one
window (1,665 cycles) had ever been asked of the host. The counter-example it produced by
hand — a 167-cycle, 41.75-hour silence in October 2015 — came out of this practice's own
increment-1 file, unopened all session.

This asks the host about every one of them, all three types, both streams, so that the
negative covers the whole expected grid and not the convenient half.

Universe: for each stream, every quarter-hour from the first to the last cycle the index
lists, that the index does **not** list.

Usage: sweep_unlisted.py <manifest> <prefix-suffixes-comma-sep> <out.jsonl> [--workers N]
"""

from __future__ import annotations

import http.client
import json
import queue
import re
import sys
import threading
import time
from datetime import datetime, timedelta, timezone

HOST = "data.gdeltproject.org"
TIMEOUT = 45
MAX_TRIES = 3
FMT = "%Y%m%d%H%M%S"
STEP = timedelta(minutes=15)
TS = re.compile(r"/(\d{14})[.]")


def listed(manifest, suffix):
    out = set()
    for line in open(manifest, encoding="utf-8", errors="replace"):
        p = line.split()
        if len(p) == 3 and p[0].isdigit() and p[2].endswith(suffix):
            m = TS.search(p[2])
            if m:
                out.add(m.group(1))
    return out


class Worker(threading.Thread):
    def __init__(self, q, fh, lock, stats, backoff):
        super().__init__(daemon=True)
        self.q, self.fh, self.lock, self.stats, self.backoff = q, fh, lock, stats, backoff
        self.conn = None

    def connect(self):
        if self.conn:
            try:
                self.conn.close()
            except Exception:
                pass
        self.conn = http.client.HTTPConnection(HOST, timeout=TIMEOUT)

    def run(self):
        while True:
            item = self.q.get()
            if item is None:
                self.q.task_done()
                return
            cycle, suffix = item
            path = f"/gdeltv2/{cycle}{suffix}"
            status = cl = None
            err = None
            for attempt in range(MAX_TRIES):
                while True:
                    with self.lock:
                        wait = self.backoff[0] - time.time()
                    if wait <= 0:
                        break
                    time.sleep(min(wait, 5))
                try:
                    if self.conn is None:
                        self.connect()
                    self.conn.request("HEAD", path, headers={"Host": HOST, "Accept": "*/*"})
                    r = self.conn.getresponse()
                    r.read()
                    status = r.status
                    c = r.getheader("Content-Length")
                    cl = int(c) if c is not None else None
                    err = None
                    if status in (429, 500, 502, 503, 504):
                        with self.lock:
                            self.backoff[0] = time.time() + 10 * (attempt + 1)
                            self.stats["throttled"] += 1
                        self.connect()
                        continue
                    break
                except Exception as e:
                    err = type(e).__name__ + ": " + str(e)[:120]
                    status = None
                    self.connect()
                    time.sleep(0.5 * (attempt + 1))
            with self.lock:
                self.stats["done"] += 1
                if status == 404:
                    self.stats["absent"] += 1
                elif status == 200:
                    self.stats["SERVED_BUT_UNLISTED"] += 1
                    self.fh.write(json.dumps({"c": cycle, "suffix": suffix, "s": 200,
                                              "cl": cl, "k": "served-but-not-listed"}) + "\n")
                elif status is None:
                    self.stats["unresolved"] += 1
                    self.fh.write(json.dumps({"c": cycle, "suffix": suffix, "s": None,
                                              "k": "unresolved", "err": err}) + "\n")
                else:
                    self.stats["other"] += 1
                    self.fh.write(json.dumps({"c": cycle, "suffix": suffix, "s": status,
                                              "k": "other-status"}) + "\n")
                if self.stats["done"] % 2000 == 0:
                    self.fh.flush()
            self.q.task_done()


def main():
    manifest, suffixes, out = sys.argv[1], sys.argv[2].split(","), sys.argv[3]
    workers = 16
    if "--workers" in sys.argv:
        workers = int(sys.argv[sys.argv.index("--workers") + 1])

    base = listed(manifest, suffixes[0])
    ts = sorted(datetime.strptime(c, FMT).replace(tzinfo=timezone.utc) for c in base)
    first, last = ts[0], ts[-1]
    missing = []
    t = first
    while t <= last:
        s = t.strftime(FMT)
        if s not in base:
            missing.append(s)
        t += STEP
    print(f"listed {len(base)}  expected grid {int((last-first)/STEP)+1}  "
          f"not listed {len(missing)}", flush=True)

    stats = {"done": 0, "absent": 0, "SERVED_BUT_UNLISTED": 0, "unresolved": 0,
             "other": 0, "throttled": 0}
    lock, backoff = threading.Lock(), [0.0]
    q = queue.Queue(maxsize=workers * 8)
    fh = open(out, "w", encoding="utf-8")
    fh.write(json.dumps({"k": "header", "manifest": manifest, "suffixes": suffixes,
                         "listed_cycles": len(base), "unlisted_cycles": len(missing),
                         "grid_first": first.strftime(FMT), "grid_last": last.strftime(FMT),
                         "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}) + "\n")
    ws = [Worker(q, fh, lock, stats, backoff) for _ in range(workers)]
    for w in ws:
        w.start()
    t0 = time.time()
    n = 0
    for c in missing:
        for s in suffixes:
            q.put((c, s))
            n += 1
            if n % 10000 == 0:
                with lock:
                    print(f"  {stats['done']}/{len(missing)*len(suffixes)} "
                          f"served-but-unlisted={stats['SERVED_BUT_UNLISTED']} "
                          f"unres={stats['unresolved']}", flush=True)
    for _ in ws:
        q.put(None)
    q.join()
    stats["total"] = len(missing) * len(suffixes)
    stats["elapsed_s"] = round(time.time() - t0, 1)
    stats["unlisted_cycles"] = len(missing)
    fh.write(json.dumps({"k": "footer", **stats,
                         "finished": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}) + "\n")
    fh.close()
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
