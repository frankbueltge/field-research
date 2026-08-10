#!/usr/bin/env python3
"""P-A: exhaustive name screen over the public Python package index.

Fetches the index's own simple endpoint (PEP 691 JSON), screens package NAMES
case-insensitively for the object's project token. Exhaustive over names; blind
to any package that consumes the object without naming it. Pre-registered in
PREREGISTRATION-1.md as population P-A.
"""
import json, urllib.request, sys

TOKEN = "gdelt"
URL = "https://pypi.org/simple/"

req = urllib.request.Request(URL, headers={
    "Accept": "application/vnd.pypi.simple.v1+json",
    "User-Agent": "field-research-census/1 (consumer census, one request)",
})
with urllib.request.urlopen(req, timeout=180) as r:
    status = r.status
    raw = r.read()
print("HTTP", status, len(raw), "bytes", file=sys.stderr)
d = json.loads(raw)
names = [p["name"] for p in d["projects"]]
hits = sorted(n for n in names if TOKEN in n.lower())
out = {"endpoint": URL, "http_status": status, "bytes": len(raw),
       "total_project_names": len(names), "token": TOKEN, "hits": hits}
json.dump(out, open("census-pypi-names.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "hits"}, indent=1))
print("HITS:", hits)
