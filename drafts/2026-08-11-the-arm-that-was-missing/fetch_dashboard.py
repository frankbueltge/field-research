#!/usr/bin/env python3
"""fetch_dashboard - read the receiver's public dashboard and record the read, not just the bytes.

Session 128, 2026-08-20. The letter says "we read it this morning". Session 128's first read of the
day was made by hand with a command-line fetch and left no record of when, with what status, or
from where — so the sentence was true and unevidenced. This script exists so that it is evidenced:
it writes the bytes and a sidecar naming the URL, the UTC second of the request, the HTTP status,
the byte count and the digest.

It fetches ONE public page and nothing else. It is not the panel probe and does not touch the
platform endpoint.

    python3 fetch_dashboard.py -o receiver-dashboard-2026-08-20.html
"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.request

URL = "https://playground.tiktok-audit.com/api-na/"
UA = "field-research/1.0 (independent research instrument; one request)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--url", default=URL)
    a = ap.parse_args()

    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    req = urllib.request.Request(a.url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        status = r.status
        body = r.read()
        headers = {k.lower(): v for k, v in r.headers.items()}
    finished = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    with open(a.out, "wb") as f:
        f.write(body)
    rec = {
        "schema": "field-research/dashboard-fetch/1",
        "url": a.url,
        "requested_utc": started,
        "finished_utc": finished,
        "http_status": status,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "saved_to": os.path.basename(a.out),
        "user_agent": UA,
        "response_headers_kept": {k: headers.get(k) for k in
                                  ("last-modified", "etag", "date", "content-type",
                                   "content-length", "server", "cache-control")},
        "what_this_is_not": ("one read of one public page from one machine. It says nothing "
                             "about what the page serves anyone else, or at any other moment."),
    }
    side = os.path.splitext(a.out)[0] + "-fetch.json"
    with open(side, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("%s %d bytes, http %d, sha256 %s\nrecord: %s"
          % (a.out, len(body), status, rec["sha256"][:16], side))
    return 0


if __name__ == "__main__":
    sys.exit(main())
