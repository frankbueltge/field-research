#!/usr/bin/env python3
"""P-B: full-text screen over the R archive network's own complete package database.

Fetches the network's machine-readable package database (all current packages,
with Title and Description) and screens name+title+description case-insensitively.
Exhaustive over that database. Pre-registered as population P-B.
"""
import json, urllib.request, sys

TOKEN = "gdelt"
URL = "https://crandb.r-pkg.org/-/desc"   # complete current-package descriptor DB

req = urllib.request.Request(URL, headers={"User-Agent": "field-research-census/1"})
with urllib.request.urlopen(req, timeout=180) as r:
    status, raw = r.status, r.read()
print("HTTP", status, len(raw), "bytes", file=sys.stderr)
d = json.loads(raw)
hits = []
for name, meta in d.items():
    blob = " ".join(str(meta.get(k, "")) for k in ("Package", "Title", "Description"))
    if TOKEN in (name + " " + blob).lower():
        hits.append({"name": name, "version": meta.get("Version"),
                     "title": meta.get("Title"), "date": meta.get("Date/Publication")})
out = {"endpoint": URL, "http_status": status, "total_packages": len(d),
       "token": TOKEN, "fields": ["Package", "Title", "Description"], "hits": hits}
json.dump(out, open("census-cran.json", "w"), indent=1)
print(json.dumps(out, indent=1)[:2000])
