#!/usr/bin/env python3
"""P-B, second half: name screen over the R archive network's ARCHIVE directory
(packages once published and since removed). The current-package DB returned 0 hits;
this checks whether a consumer existed and was withdrawn."""
import re, json, urllib.request
URL = "https://cran.r-project.org/src/contrib/Archive/"
req = urllib.request.Request(URL, headers={"User-Agent": "field-research-census/1"})
with urllib.request.urlopen(req, timeout=120) as r:
    status, html = r.status, r.read().decode("utf-8", "replace")
names = sorted(set(re.findall(r'href="([^"/]+)/"', html)))
hits = [n for n in names if "gdelt" in n.lower()]
out = {"endpoint": URL, "http_status": status, "archived_package_dirs": len(names), "hits": hits}
json.dump(out, open("census-cran-archive.json", "w"), indent=1)
print(json.dumps(out, indent=1))
