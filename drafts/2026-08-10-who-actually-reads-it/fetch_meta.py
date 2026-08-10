#!/usr/bin/env python3
"""Fetch registry metadata for every P-A hit, first-hand from the index's own JSON API."""
import json, urllib.request, urllib.error

hits = json.load(open("census-pypi-names.json"))["hits"]
rows = []
for n in hits:
    url = f"https://pypi.org/pypi/{n}/json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "field-research-census/1"})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        rows.append({"name": n, "error": f"HTTP {e.code}"}); continue
    info = d["info"]
    rel = d["releases"]
    dates = []
    for v, files in rel.items():
        for f in files:
            if f.get("upload_time_iso_8601"):
                dates.append(f["upload_time_iso_8601"])
    last = max(dates) if dates else None
    sd = [f for f in d["urls"] if f["packagetype"] == "sdist"]
    wh = [f for f in d["urls"] if f["packagetype"] == "bdist_wheel"]
    rows.append({
        "name": info["name"], "version": info["version"],
        "summary": (info.get("summary") or "")[:160],
        "home_page": info.get("home_page") or (info.get("project_urls") or {}),
        "last_upload": last, "n_releases": len(rel),
        "sdist_url": sd[0]["url"] if sd else None,
        "wheel_url": wh[0]["url"] if wh else None,
        "requires_dist": info.get("requires_dist"),
    })
json.dump(rows, open("census-pypi-meta.json", "w"), indent=1, default=str)
for r in rows:
    print(f'{r.get("name"):18} {str(r.get("version")):10} {str(r.get("last_upload"))[:10]:11} rel={r.get("n_releases")}  {r.get("summary","")[:70]}')
