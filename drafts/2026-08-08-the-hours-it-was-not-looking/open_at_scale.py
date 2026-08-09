#!/usr/bin/env python3
"""open_at_scale.py — increment 2: open GDELT's 15-minute GKG files at scale.

Runs the sampling design fixed in PREREGISTRATION-2.md (committed before this file was
written) and measures, per sampled cycle: HTTP status, bytes received, MD5 of the bytes
received against the manifest's published MD5, whether the zip opens, the byte length of
the inner CSV, the number of records in it, and — for sample D only — the set of
DocumentIdentifier values, so that a cycle which republishes its predecessor can be told
from one that reports a new quarter-hour.

Nothing is written to disk except the result JSON: every archive is opened in memory and
discarded.

Usage: python3 open_at_scale.py <manifest.txt> <draft_dir> <out.json>
"""

from __future__ import annotations

import hashlib
import io
import json
import random
import sys
import time
import urllib.error
import urllib.request
import zipfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

SEED = 20260809          # fixed in the pre-registration
N_A = 80                 # collapsed cycles
N_C = 80                 # random unflagged cycles
N_D = 30                 # consecutive unflagged pairs
MATCH_DAYS = 7           # control must lie within 7 days before its collapsed cycle
MIN_PER_YEAR = 4         # stratification floor for sample A
DOCID_COL = 4            # GKG 2.1: GKGRECORDID, DATE, SourceCollectionIdentifier,
                         # SourceCommonName, DocumentIdentifier, ...
THREADS = 8
TIMEOUT = 120
STEP = timedelta(minutes=15)


def parse_manifest(path):
    """ts -> (size, md5, url) for the English GKG series."""
    out = {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            p = line.split()
            if len(p) != 3 or not p[0].isdigit():
                continue
            fname = p[2].rsplit("/", 1)[-1]
            stamp, rest = fname[:14], fname[14:].lower()
            if not stamp.isdigit() or len(stamp) != 14:
                continue
            if rest.startswith(".translation"):
                continue
            if not rest.startswith(".gkg"):
                continue
            try:
                ts = datetime.strptime(stamp, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
            except ValueError:
                continue
            out[ts] = (int(p[0]), p[1], p[2])
    return out


def load_flags(draft):
    a = {c["ts"] for c in json.load(open(f"{draft}/collapses.json"))["collapsed_cycles"]}
    b = {c["ts"] for c in json.load(open(f"{draft}/rescreen-english.json"))["detail"]}
    return a, b


def fetch_one(item):
    """item: dict with ts, url, manifest size/md5, sample tag. Returns it, measured."""
    rec = dict(item)
    t0 = time.time()
    try:
        req = urllib.request.Request(item["url"], headers={"User-Agent": "field-research/increment-2"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read()
            rec["http_status"] = resp.status
    except urllib.error.HTTPError as exc:
        rec["http_status"] = exc.code
        rec["error"] = f"HTTPError {exc.code}"
        rec["seconds"] = round(time.time() - t0, 2)
        return rec
    except Exception as exc:                                     # noqa: BLE001
        rec["http_status"] = None
        rec["error"] = f"{type(exc).__name__}: {exc}"
        rec["seconds"] = round(time.time() - t0, 2)
        return rec

    rec["bytes_received"] = len(body)
    rec["md5_received"] = hashlib.md5(body).hexdigest()
    rec["size_matches_manifest"] = (len(body) == item["manifest_size"])
    rec["md5_matches_manifest"] = (rec["md5_received"] == item["manifest_md5"])
    try:
        zf = zipfile.ZipFile(io.BytesIO(body))
        names = zf.namelist()
        rec["zip_opens"] = True
        rec["inner_names"] = names
        if not names:
            rec["inner_bytes"] = 0
            rec["records"] = 0
        else:
            raw = zf.read(names[0])
            rec["inner_bytes"] = len(raw)
            text = raw.decode("utf-8", errors="replace")
            lines = [ln for ln in text.split("\n") if ln.strip()]
            rec["records"] = len(lines)
            if item.get("collect_docids"):
                ids = set()
                for ln in lines:
                    cols = ln.split("\t")
                    if len(cols) > DOCID_COL:
                        ids.add(cols[DOCID_COL])
                rec["docids"] = sorted(ids)
    except Exception as exc:                                     # noqa: BLE001
        rec["zip_opens"] = False
        rec["error"] = f"zip: {type(exc).__name__}: {exc}"
    rec["seconds"] = round(time.time() - t0, 2)
    return rec


def main():
    manifest_path, draft, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    man = parse_manifest(manifest_path)
    screen_a, screen_b = load_flags(draft)
    both = screen_a & screen_b
    either = screen_a | screen_b

    present = sorted(man)
    def key(ts):
        return ts.strftime("%Y-%m-%dT%H:%M:%SZ")

    unflagged = [t for t in present if key(t) not in either]
    unflagged_set = set(unflagged)

    # ---- Q8: does the re-fetched manifest still say the same about the past? -------
    old = {c["ts"]: c["gkg_bytes"]
           for c in json.load(open(f"{draft}/collapses.json"))["collapsed_cycles"]}
    q8_checked = q8_same = 0
    q8_diffs, q8_absent = [], []
    for ts_s, old_bytes in old.items():
        ts = datetime.strptime(ts_s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if ts not in man:
            q8_absent.append(ts_s)
            continue
        q8_checked += 1
        if man[ts][0] == old_bytes:
            q8_same += 1
        else:
            q8_diffs.append({"ts": ts_s, "yesterday": old_bytes, "today": man[ts][0]})

    # ---- sampling, in the pre-registered draw order A, C, D -----------------------
    rng = random.Random(SEED)

    by_year = defaultdict(list)
    for ts_s in sorted(both):
        by_year[ts_s[:4]].append(ts_s)
    chosen, pool = [], []
    for yr in sorted(by_year):
        members = sorted(by_year[yr])
        take = min(MIN_PER_YEAR, len(members))
        picks = rng.sample(members, take)
        chosen.extend(picks)
        pool.extend([m for m in members if m not in set(picks)])
    remainder = max(0, N_A - len(chosen))
    chosen.extend(rng.sample(pool, min(remainder, len(pool))))
    sample_a = sorted(chosen)

    # sample B: nearest preceding unflagged cycle within MATCH_DAYS
    sample_b, unmatched = [], []
    for ts_s in sample_a:
        ts = datetime.strptime(ts_s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        found, cur, limit = None, ts - STEP, ts - timedelta(days=MATCH_DAYS)
        while cur >= limit:
            if cur in unflagged_set:
                found = cur
                break
            cur -= STEP
        if found is None:
            unmatched.append(ts_s)
        else:
            sample_b.append((ts_s, key(found)))

    sample_c = sorted(key(t) for t in rng.sample(unflagged, min(N_C, len(unflagged))))

    pair_pool = [t for t in unflagged if (t + STEP) in unflagged_set]
    sample_d = sorted(key(t) for t in rng.sample(pair_pool, min(N_D, len(pair_pool))))

    # ---- build the work list -----------------------------------------------------
    jobs, seen = [], {}
    def add(ts_s, tag, docids=False):
        ts = datetime.strptime(ts_s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        size, md5, url = man[ts]
        if ts_s in seen:
            seen[ts_s]["samples"].append(tag)
            seen[ts_s]["collect_docids"] = seen[ts_s]["collect_docids"] or docids
            return
        job = {"ts": ts_s, "url": url, "manifest_size": size, "manifest_md5": md5,
               "samples": [tag], "collect_docids": docids}
        seen[ts_s] = job
        jobs.append(job)

    for t in sample_a:
        add(t, "A")
    for a_ts, b_ts in sample_b:
        add(b_ts, "B")
    for t in sample_c:
        add(t, "C")
    for t in sample_d:
        add(t, "D1", docids=True)
        nxt = key(datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) + STEP)
        add(nxt, "D2", docids=True)

    print(f"manifest gkg cycles: {len(man)}  unflagged: {len(unflagged)}", flush=True)
    print(f"sample A {len(sample_a)}  B {len(sample_b)} (unmatched {len(unmatched)})  "
          f"C {len(sample_c)}  D {len(sample_d)} pairs  -> {len(jobs)} distinct downloads",
          flush=True)

    t0 = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=THREADS) as pool_ex:
        for i, rec in enumerate(pool_ex.map(fetch_one, jobs), 1):
            results.append(rec)
            if i % 25 == 0:
                print(f"  {i}/{len(jobs)}  {round(time.time()-t0)}s", flush=True)

    payload = {
        "run_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "seed": SEED,
        "manifest": {"path": manifest_path, "gkg_cycles": len(man)},
        "screens": {"pre_registered": len(screen_a), "same_minute": len(screen_b),
                    "intersection": len(both), "either": len(either),
                    "unflagged_present": len(unflagged)},
        "q8_manifest_stability": {"checked": q8_checked, "identical": q8_same,
                                  "differing": q8_diffs,
                                  "absent_from_new_manifest": q8_absent},
        "samples": {"A": sample_a, "B": sample_b, "B_unmatched": unmatched,
                    "C": sample_c, "D_pair_first": sample_d},
        "downloads": results,
        "elapsed_seconds": round(time.time() - t0, 1),
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1)
    print(json.dumps({"downloads": len(results),
                      "q8": payload["q8_manifest_stability"]["checked"],
                      "q8_identical": q8_same,
                      "elapsed_s": payload["elapsed_seconds"]}, indent=1))


if __name__ == "__main__":
    main()
