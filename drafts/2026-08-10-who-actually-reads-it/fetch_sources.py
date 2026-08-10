#!/usr/bin/env python3
"""Download every candidate's source from the registry itself and unpack it.
Nothing is executed at this stage; the archives are read as text."""
import json, os, urllib.request, tarfile, zipfile, io, hashlib

FALSE_POSITIVES = {"logdelta", "pgdelta"}   # substring collisions, not consumers
rows = json.load(open("census-pypi-meta.json"))
os.makedirs("src", exist_ok=True)
log = []
for r in rows:
    n = r["name"]
    if n.lower() in FALSE_POSITIVES:
        log.append({"name": n, "skipped": "substring collision, not a consumer"}); continue
    url = r["sdist_url"] or r["wheel_url"]
    if not url:
        log.append({"name": n, "error": "no distribution"}); continue
    req = urllib.request.Request(url, headers={"User-Agent": "field-research-census/1"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        blob = resp.read()
    dest = os.path.join("src", n)
    os.makedirs(dest, exist_ok=True)
    try:
        if url.endswith((".tar.gz", ".tgz")):
            tarfile.open(fileobj=io.BytesIO(blob)).extractall(dest, filter="data")
        else:
            zipfile.ZipFile(io.BytesIO(blob)).extractall(dest)
    except Exception as e:
        log.append({"name": n, "error": f"unpack: {e}"}); continue
    nfiles = sum(len(f) for _, _, f in os.walk(dest))
    log.append({"name": n, "url": url, "sha256": hashlib.sha256(blob).hexdigest(),
                "bytes": len(blob), "files": nfiles})
json.dump(log, open("source-fetch-log.json", "w"), indent=1)
for e in log:
    print(e.get("name"), "->", e.get("files", e.get("error", e.get("skipped"))))
