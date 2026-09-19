#!/usr/bin/env python3
"""Harvest the SPDX License List canonical texts.

Session 164, 2026-09-19. The corpus is a FEED, not a copy: no licence text is
committed to this repository. What is committed is, per entry, the identifier,
the SHA-256 of the exact bytes scored, its length, and short quoted lines where
a quotation is load-bearing.

Source: https://github.com/spdx/license-list-data  (index json/licenses.json,
per-entry json/details/<id>.json). Read once, digested, and the version string
of the list is recorded with the digest.
"""
import concurrent.futures as cf
import hashlib
import json
import os
import sys
import urllib.request

RAW = "https://raw.githubusercontent.com/spdx/license-list-data/main/json"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/spdx"


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={
        "User-Agent": "field-research/meridian (research measurement; contact via repository)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    os.makedirs(OUT, exist_ok=True)
    index = json.loads(get(f"{RAW}/licenses.json"))
    version = index["licenseListVersion"]
    ids = [e["licenseId"] for e in index["licenses"]]
    deprecated = {e["licenseId"]: e["isDeprecatedLicenseId"] for e in index["licenses"]}
    names = {e["licenseId"]: e["name"] for e in index["licenses"]}
    print(f"list version {version}, {len(ids)} identifiers", file=sys.stderr)

    texts, errors = {}, {}

    def one(lid):
        try:
            d = json.loads(get(f"{RAW}/details/{lid}.json"))
            return lid, d.get("licenseText"), None
        except Exception as exc:                       # recorded, never invented
            return lid, None, f"{type(exc).__name__}: {exc}"

    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        for lid, text, err in ex.map(one, ids):
            if err or text is None:
                errors[lid] = err or "no licenseText field"
            else:
                texts[lid] = text

    manifest = {
        "source": "https://github.com/spdx/license-list-data",
        "license_list_version": version,
        "fetched_ids": len(ids),
        "texts_ok": len(texts),
        "errors": errors,
        "entries": sorted(
            [{"id": lid,
              "name": names[lid],
              "deprecated": bool(deprecated[lid]),
              "bytes": len(texts[lid].encode("utf-8")),
              "sha256": hashlib.sha256(texts[lid].encode("utf-8")).hexdigest()}
             for lid in texts], key=lambda e: e["id"]),
    }
    manifest["corpus_digest"] = hashlib.sha256(
        "".join(f"{e['id']}:{e['sha256']}\n" for e in manifest["entries"]).encode()).hexdigest()

    with open(os.path.join(OUT, "texts.json"), "w") as fh:
        json.dump(texts, fh)                            # scratch only, never committed
    with open(os.path.join(OUT, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
    print(json.dumps({k: v for k, v in manifest.items() if k != "entries"}, indent=1))


if __name__ == "__main__":
    main()
