#!/usr/bin/env python3
"""Harvest — a census of four public catalogues, keeping only the fields the study names.

Session 157, cycle 003, question "Missing Data Art". Population, fields and page sizes are fixed
by artifacts/cycle-003/2026-09-11-does-it-travel/PREREGISTRATION.md §2, committed before this
file fetched anything.

No third-party corpus is committed (protocol §7): the harvest is written to a cache directory
outside the repository, and only derived counts and short quoted values reach the record.

No model is called anywhere in this file. Standard library only.

Usage:
    python3 tools/travel/harvest.py --cache /path/to/cache [--only cma,uk,govdata,aic]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request

UA = "field-research/travel (Meridian; research census; contact via frankbueltge.de)"


def get(url: str, timeout: int = 120, tries: int = 4) -> bytes:
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001 - an unreachable page is a fact about the session
            last = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{url}: {last}")


def s(v) -> str:
    return v if isinstance(v, str) else ("" if v is None else str(v))


# ---------------------------------------------------------------------------
# C1 — Cleveland Museum of Art
# ---------------------------------------------------------------------------

def harvest_cma(out_path: str) -> dict:
    base = "https://openaccess-api.clevelandart.org/api/artworks/"
    first = json.loads(get(f"{base}?limit=1&skip=0"))
    total = first["info"]["total"]
    kept = 0
    pages = 0
    with open(out_path, "w", encoding="utf-8") as fh:
        skip = 0
        while skip < total:
            raw = get(f"{base}?limit=1000&skip={skip}")
            doc = json.loads(raw)
            rows = doc["data"]
            if not rows:
                break
            for r in rows:
                fh.write(json.dumps({
                    "id": s(r.get("id")),
                    "title": s(r.get("title")),
                    "text": s(r.get("description")),
                    "stratum": s((r.get("department") or "")),
                    "collection": s(r.get("collection")),
                    "type": s(r.get("type")),
                    "oa_year": s(r.get("date_added_to_oa"))[:4],
                    "creditline": s(r.get("creditline")),
                    "url": s(r.get("url")),
                    "has_didyouknow": bool(s(r.get("did_you_know")).strip()),
                }, ensure_ascii=False) + "\n")
                kept += 1
            pages += 1
            skip += len(rows)
            print(f"  cma {kept}/{total}", file=sys.stderr)
            time.sleep(0.5)
    return {"catalogue": "cma", "api_total": total, "harvested": kept, "pages": pages,
            "endpoint": base, "field": "description", "stratum_field": "department"}


# ---------------------------------------------------------------------------
# C2 / C3 — CKAN portals
# ---------------------------------------------------------------------------

def harvest_ckan(name: str, base: str, site: str, out_path: str) -> dict:
    first = json.loads(get(f"{base}?rows=1&start=0&sort=name+asc"))
    total = first["result"]["count"]
    kept = 0
    pages = 0
    with open(out_path, "w", encoding="utf-8") as fh:
        start = 0
        while start < total:
            doc = json.loads(get(f"{base}?rows=1000&start={start}&sort=name+asc"))
            rows = doc["result"]["results"]
            if not rows:
                break
            for r in rows:
                org = r.get("organization") or {}
                fh.write(json.dumps({
                    "id": s(r.get("id")) or s(r.get("name")),
                    "title": s(r.get("title")),
                    "text": s(r.get("notes")),
                    "stratum": s(org.get("title")) or s(org.get("name")),
                    "org_name": s(org.get("name")),
                    "license": s(r.get("license_id")),
                    "created": s(r.get("metadata_created"))[:4],
                    "num_resources": r.get("num_resources"),
                    "url": f"{site}/dataset/{s(r.get('name'))}",
                }, ensure_ascii=False) + "\n")
                kept += 1
            pages += 1
            start += len(rows)
            print(f"  {name} {kept}/{total}", file=sys.stderr)
            time.sleep(0.5)
    return {"catalogue": name, "api_total": total, "harvested": kept, "pages": pages,
            "endpoint": base, "field": "notes", "stratum_field": "organization"}


# ---------------------------------------------------------------------------
# C4 — Art Institute of Chicago, fill rate only (20 seeded-random pages of 100)
# ---------------------------------------------------------------------------

def harvest_aic(out_path: str, seed: int = 20260911) -> dict:
    base = "https://api.artic.edu/api/v1/artworks"
    fields = "id,title,description,short_description,provenance_text,credit_line,department_title"
    first = json.loads(get(f"{base}?limit=1&page=1&fields={fields}"))
    total = first["pagination"]["total"]
    limit = 100
    npages = total // limit
    rng = random.Random(seed)
    picks = sorted(rng.sample(range(1, npages + 1), 20))
    kept = 0
    with open(out_path, "w", encoding="utf-8") as fh:
        for p in picks:
            doc = json.loads(get(f"{base}?limit={limit}&page={p}&fields={fields}"))
            for r in doc["data"]:
                fh.write(json.dumps({
                    "id": s(r.get("id")),
                    "title": s(r.get("title")),
                    "text": s(r.get("description")),
                    "short_description": s(r.get("short_description")),
                    "provenance_text": s(r.get("provenance_text")),
                    "credit_line": s(r.get("credit_line")),
                    "stratum": s(r.get("department_title")),
                }, ensure_ascii=False) + "\n")
                kept += 1
            time.sleep(0.5)
    return {"catalogue": "aic", "api_total": total, "harvested": kept, "pages": len(picks),
            "endpoint": base, "field": "description", "stratum_field": "department_title",
            "sampling": f"20 seeded-random pages of {limit}, seed {seed}", "seed": seed}


# ---------------------------------------------------------------------------
# The home arm — the house feed, read live, never mirrored into the repository
# ---------------------------------------------------------------------------

def harvest_atlas(out_path: str) -> dict:
    url = "https://frankbueltge.de/atlas/werke.json"
    raw = get(url)
    doc = json.loads(raw)
    entries = doc["entries"]
    with open(out_path, "w", encoding="utf-8") as fh:
        for e in entries:
            fh.write(json.dumps({
                "id": s(e.get("title")),
                "title": s(e.get("title")),
                "text": s(e.get("decisive_move")),
                "stratum": s(e.get("venue_prize")),
                "verify_status": s(e.get("verify_status")),
                "url": s(e.get("source_url")),
            }, ensure_ascii=False) + "\n")
    return {"catalogue": "atlas", "api_total": len(entries), "harvested": len(entries),
            "pages": 1, "endpoint": url, "field": "decisive_move",
            "stratum_field": "venue_prize (provenance families, frozen 2026-09-08)",
            "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    ap.add_argument("--only", default="atlas,cma,uk,govdata,aic")
    args = ap.parse_args()
    os.makedirs(args.cache, exist_ok=True)
    want = {x.strip() for x in args.only.split(",") if x.strip()}

    manifest_path = os.path.join(args.cache, "manifest.json")
    manifest = {}
    if os.path.exists(manifest_path):
        manifest = json.load(open(manifest_path))

    jobs = {
        "atlas": lambda p: harvest_atlas(p),
        "cma": lambda p: harvest_cma(p),
        "uk": lambda p: harvest_ckan("uk", "https://ckan.publishing.service.gov.uk/api/3/action/package_search",
                                     "https://data.gov.uk", p),
        "govdata": lambda p: harvest_ckan("govdata", "https://www.govdata.de/ckan/api/3/action/package_search",
                                          "https://www.govdata.de", p),
        "aic": lambda p: harvest_aic(p),
    }

    for name, fn in jobs.items():
        if name not in want:
            continue
        path = os.path.join(args.cache, f"{name}.jsonl")
        print(f"[{time.strftime('%H:%M:%S')}] harvesting {name}", file=sys.stderr)
        t0 = time.time()
        try:
            info = fn(path)
            info["seconds"] = round(time.time() - t0, 1)
            info["fetched_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            info["ok"] = True
        except Exception as exc:  # noqa: BLE001
            info = {"catalogue": name, "ok": False, "error": str(exc)[:400],
                    "seconds": round(time.time() - t0, 1)}
        manifest[name] = info
        with open(manifest_path, "w") as fh:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
        print(f"[{time.strftime('%H:%M:%S')}] {name}: {json.dumps(info)[:300]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
