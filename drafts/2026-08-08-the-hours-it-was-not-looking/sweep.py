#!/usr/bin/env python3
"""sweep.py — the complete negative: ask the host about every listed cycle.

Increment 3, session 105. Specified in PREREGISTRATION-3.md before the first request.

For every entry of a given type in the master file list, one HTTP HEAD. Two products
from one pass, as the pre-registration says:

  (1) the complete negative  — which listed files the host does not serve;
  (2) the complete disagreement — which listed files the host serves at a size other
      than the one the index declares (a HEAD returns Content-Length).

Rules that bind this run, from the pre-registration:
  * bounded concurrency; on 429/5xx back off and record;
  * every non-200/404 outcome retried up to three times, and if it never resolves it is
    recorded as UNRESOLVED — never inferred in either direction;
  * a run that does not complete reports the fraction it covered; partial is partial.

Output is JSONL, streamed, one line per probe, so a killed run keeps what it measured.
Only rows that are interesting (not a clean 200 with matching size) carry detail; clean
rows are counted and a sample is kept, because 395k clean rows are not evidence of
anything a count does not carry.

Usage: sweep.py <manifest> <suffix> <out.jsonl> [--limit N] [--workers N] [--offset N]
"""

from __future__ import annotations

import http.client
import json
import queue
import re
import sys
import threading
import time

HOST = "data.gdeltproject.org"
TIMEOUT = 45
MAX_TRIES = 3
CLEAN_SAMPLE_EVERY = 500          # keep every 500th clean row as a witness

TS = re.compile(r"/(\d{14})[.]")


def parse(manifest: str, suffix: str):
    out = []
    with open(manifest, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            p = line.split()
            if len(p) != 3 or not p[0].isdigit() or not p[2].endswith(suffix):
                continue
            m = TS.search(p[2])
            if not m:
                continue
            out.append((m.group(1), int(p[0]), p[1], p[2]))
    return out


class Worker(threading.Thread):
    def __init__(self, q, results, lock, stats, backoff):
        super().__init__(daemon=True)
        self.q, self.results, self.lock, self.stats, self.backoff = q, results, lock, stats, backoff
        self.conn = None

    def connect(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception:
                pass
        self.conn = http.client.HTTPConnection(HOST, timeout=TIMEOUT)

    def head(self, path):
        if self.conn is None:
            self.connect()
        self.conn.request("HEAD", path, headers={"Host": HOST, "Accept": "*/*"})
        r = self.conn.getresponse()
        r.read()
        cl = r.getheader("Content-Length")
        return r.status, (int(cl) if cl is not None else None), r.getheader("Last-Modified")

    def run(self):
        while True:
            item = self.q.get()
            if item is None:
                self.q.task_done()
                return
            idx, (cycle, declared, md5, url) = item
            path = url.split(HOST, 1)[1] if HOST in url else url
            status = cl = lm = None
            err = None
            for attempt in range(MAX_TRIES):
                # a backoff set by any worker pauses all of them
                while True:
                    with self.lock:
                        wait = self.backoff[0] - time.time()
                    if wait <= 0:
                        break
                    time.sleep(min(wait, 5))
                try:
                    status, cl, lm = self.head(path)
                    err = None
                    if status in (429, 500, 502, 503, 504):
                        with self.lock:
                            self.backoff[0] = time.time() + 10 * (attempt + 1)
                            self.stats["throttled"] += 1
                        self.connect()
                        continue
                    break
                except Exception as e:                       # reset, timeout, DNS
                    err = type(e).__name__ + ": " + str(e)[:120]
                    status = None
                    self.connect()
                    time.sleep(0.5 * (attempt + 1))
            with self.lock:
                self.stats["done"] += 1
                row = None
                if status == 200 and cl == declared:
                    self.stats["ok"] += 1
                    if idx % CLEAN_SAMPLE_EVERY == 0:
                        row = {"c": cycle, "s": 200, "cl": cl, "d": declared, "k": "clean-sample"}
                elif status == 200:
                    self.stats["mismatch"] += 1
                    row = {"c": cycle, "s": 200, "cl": cl, "d": declared, "md5": md5,
                           "lm": lm, "k": "size-mismatch", "url": url}
                elif status == 404:
                    self.stats["absent"] += 1
                    row = {"c": cycle, "s": 404, "d": declared, "md5": md5,
                           "k": "absent", "url": url}
                elif status is None:
                    self.stats["unresolved"] += 1
                    row = {"c": cycle, "s": None, "d": declared, "k": "unresolved",
                           "err": err, "url": url}
                else:
                    self.stats["other"] += 1
                    row = {"c": cycle, "s": status, "cl": cl, "d": declared,
                           "k": "other-status", "url": url}
                if row is not None:
                    self.results.write(json.dumps(row) + "\n")
                    if self.stats["done"] % 2000 == 0:
                        self.results.flush()
            self.q.task_done()


def main():
    manifest, suffix, out = sys.argv[1], sys.argv[2], sys.argv[3]
    limit = workers = offset = None
    for i, a in enumerate(sys.argv):
        if a == "--limit":
            limit = int(sys.argv[i + 1])
        if a == "--workers":
            workers = int(sys.argv[i + 1])
        if a == "--offset":
            offset = int(sys.argv[i + 1])
    workers = workers or 24
    entries = parse(manifest, suffix)
    entries.sort(key=lambda e: e[0])
    if offset:
        entries = entries[offset:]
    if limit:
        entries = entries[:limit]

    stats = {"done": 0, "ok": 0, "absent": 0, "mismatch": 0, "unresolved": 0,
             "other": 0, "throttled": 0}
    lock = threading.Lock()
    backoff = [0.0]
    q = queue.Queue(maxsize=workers * 8)
    fh = open(out, "w", encoding="utf-8")
    fh.write(json.dumps({"k": "header", "manifest": manifest, "suffix": suffix,
                         "total": len(entries), "workers": workers,
                         "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}) + "\n")
    ws = [Worker(q, fh, lock, stats, backoff) for _ in range(workers)]
    for w in ws:
        w.start()
    t0 = time.time()
    for i, e in enumerate(entries):
        q.put((i, e))
        if i % 20000 == 0 and i:
            with lock:
                el = time.time() - t0
                print(f"  {stats['done']}/{len(entries)}  {stats['done']/el:.0f}/s  "
                      f"absent={stats['absent']} mismatch={stats['mismatch']} "
                      f"unres={stats['unresolved']} thr={stats['throttled']}", flush=True)
    for _ in ws:
        q.put(None)
    q.join()
    el = time.time() - t0
    stats["elapsed_s"] = round(el, 1)
    stats["rate_per_s"] = round(stats["done"] / el, 1)
    stats["total"] = len(entries)
    fh.write(json.dumps({"k": "footer", **stats,
                         "finished": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}) + "\n")
    fh.close()
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
