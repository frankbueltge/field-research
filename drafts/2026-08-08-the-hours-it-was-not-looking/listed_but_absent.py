#!/usr/bin/env python3
"""listed_but_absent.py — follow-up to increment 2, UNREGISTERED.

Increment 2's pre-registered Q7 asked only whether at least one file listed in GDELT's
published manifest fails to download. It did: five of 294, all on the same day. Q7 is
scored on that. Everything this file measures is an unregistered follow-up, run to find
out how large the class is, and is reported apart from the scored table.

Three probes:
  1. the five failures re-probed, to rule out a transient error;
  2. every manifest entry (all three file types) for a named window, exhaustively;
  3. a seeded uniform sample of manifest entries across the whole series, to estimate the
     rate of listed-but-absent files outside that window.

HEAD requests only; nothing is downloaded.

Usage: python3 listed_but_absent.py <manifest.txt> <out.json>
"""

from __future__ import annotations

import json
import random
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

SEED = 20260809
SWEEP_N = 3000                       # uniform sample across the whole series
WINDOW = ("2022-11-01", "2022-11-30")  # the month the five failures fall in
THREADS = 16
TIMEOUT = 60
RETRIES = 2

FAILED_FIVE = ["2022-11-11T04:30:00Z", "2022-11-11T06:15:00Z", "2022-11-11T10:00:00Z",
               "2022-11-11T11:15:00Z", "2022-11-11T17:15:00Z"]


def parse(path):
    """ts -> {type: (size, md5, url)} for the English series."""
    out = defaultdict(dict)
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            p = line.split()
            if len(p) != 3 or not p[0].isdigit():
                continue
            fname = p[2].rsplit("/", 1)[-1]
            stamp, rest = fname[:14], fname[14:].lower()
            if not stamp.isdigit() or len(stamp) != 14 or rest.startswith(".translation"):
                continue
            kind = ("gkg" if rest.startswith(".gkg") else
                    "export" if rest.startswith(".export") else
                    "mentions" if rest.startswith(".mentions") else None)
            if kind is None:
                continue
            try:
                ts = datetime.strptime(stamp, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            out[ts.strftime("%Y-%m-%dT%H:%M:%SZ")][kind] = (int(p[0]), p[1], p[2])
    return out


def head(job):
    ts, kind, size, md5, url = job
    for attempt in range(RETRIES + 1):
        try:
            req = urllib.request.Request(url, method="HEAD",
                                         headers={"User-Agent": "field-research/increment-2"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return {"ts": ts, "kind": kind, "status": resp.status,
                        "content_length": resp.headers.get("content-length"),
                        "last_modified": resp.headers.get("last-modified"),
                        "manifest_size": size, "attempts": attempt + 1}
        except urllib.error.HTTPError as exc:
            return {"ts": ts, "kind": kind, "status": exc.code,
                    "manifest_size": size, "attempts": attempt + 1}
        except Exception as exc:                                  # noqa: BLE001
            if attempt == RETRIES:
                return {"ts": ts, "kind": kind, "status": None,
                        "error": f"{type(exc).__name__}: {exc}",
                        "manifest_size": size, "attempts": attempt + 1}
            time.sleep(1.5 * (attempt + 1))
    return None


def run(jobs, label):
    t0 = time.time()
    res = []
    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        for i, r in enumerate(ex.map(head, jobs), 1):
            res.append(r)
            if i % 500 == 0:
                print(f"  {label} {i}/{len(jobs)} {round(time.time()-t0)}s", flush=True)
    print(f"  {label}: {len(res)} probes in {round(time.time()-t0)}s", flush=True)
    return res


def main():
    man = parse(sys.argv[1])
    out_path = sys.argv[2]

    # 1 — the five, re-probed on all three file types
    jobs = []
    for ts in FAILED_FIVE:
        for kind, (size, md5, url) in sorted(man[ts].items()):
            jobs.append((ts, kind, size, md5, url))
    reprobe = run(jobs, "re-probe")

    # 2 — the whole month, exhaustively, all three file types
    jobs = []
    for ts in sorted(man):
        if WINDOW[0] <= ts[:10] <= WINDOW[1]:
            for kind, (size, md5, url) in sorted(man[ts].items()):
                jobs.append((ts, kind, size, md5, url))
    month = run(jobs, "month")

    # 3 — uniform sweep over the whole series, gkg only
    rng = random.Random(SEED)
    all_gkg = [ts for ts in sorted(man) if "gkg" in man[ts] and not (WINDOW[0] <= ts[:10] <= WINDOW[1])]
    picks = rng.sample(all_gkg, min(SWEEP_N, len(all_gkg)))
    jobs = [(ts, "gkg", *man[ts]["gkg"][:2], man[ts]["gkg"][2]) for ts in sorted(picks)]
    sweep = run(jobs, "sweep")

    def summarise(rows):
        by = defaultdict(int)
        for r in rows:
            by[str(r["status"])] += 1
        absent = [r for r in rows if r["status"] == 404]
        errors = [r for r in rows if r["status"] is None]
        mismatch = [r for r in rows if r["status"] == 200 and r.get("content_length")
                    and int(r["content_length"]) != r["manifest_size"]]
        return {"probed": len(rows), "by_status": dict(by), "absent_404": len(absent),
                "probe_errors": len(errors),
                "size_disagrees_with_manifest": len(mismatch),
                "absent_detail": sorted({(r["ts"], r["kind"]) for r in absent}),
                "mismatch_detail": [{"ts": r["ts"], "kind": r["kind"],
                                     "manifest": r["manifest_size"],
                                     "served": int(r["content_length"])} for r in mismatch]}

    payload = {
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "seed": SEED, "threads": THREADS, "retries": RETRIES,
        "note": "UNREGISTERED follow-up to the pre-registered Q7; scored nowhere.",
        "reprobe_of_the_five": summarise(reprobe),
        "exhaustive_month_2022_11": summarise(month),
        "uniform_sweep_rest_of_series": summarise(sweep),
    }
    json.dump(payload, open(out_path, "w"), indent=1)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk not in ("absent_detail", "mismatch_detail")}
                      for k, v in payload.items() if isinstance(v, dict)}, indent=1))


if __name__ == "__main__":
    main()
