"""List unclassified area-periods per case analysis, with encoding (answers ho-2026-10-27-atelier-1).

Usage: python3 -I cases.py ipc_global_area_long.csv > cases.json
Encodings as in ../README.md: A = 'all' row 0 and no phase rows; B = phase rows sum 0 and 'all' 0;
C = phase rows sum 0 and 'all' > 0. Case selection fixed in PREDICTIONS.md.
"""
import csv, collections, json, sys
from datetime import datetime

CH = {"NGA", "GHA", "BEN", "BFA", "MLI", "NER", "TCD", "SEN", "MRT", "GIN", "SLE", "LBR", "TGO", "CIV",
      "GMB", "GNB", "CMR", "CPV"}
PH = {"1", "2", "3", "4", "5"}
g = collections.defaultdict(dict)
for r in csv.DictReader(open(sys.argv[1], newline="")):
    if datetime.strptime(r["Date of analysis"], "%b %Y").year < 2017 or r["Country"] in CH:
        continue
    k = (r["Date of analysis"], r["Country"], r["Validity period"], r["Level 1"], r["Area"])
    g[k][r["Phase"]] = int(round(float(r["Number"]))) if r["Number"] else 0

def enc(v):
    if sum(v.get(p, 0) for p in PH) > 0:
        return None
    if not (PH & set(v)):
        return "A" if v.get("all", 0) == 0 else "A+"  # A+ : people, no phase rows (not seen in s234)
    return "B" if v.get("all", 0) == 0 else "C"

per = collections.defaultdict(list)
for (d, c, vp, l1, a), v in g.items():
    e = enc(v)
    if e:
        per[(d, c)].append(dict(period=vp, level1=l1, area=a, encoding=e, all=v.get("all", 0)))

cases = []
for (d, c), rows in sorted(per.items(), key=lambda x: (x[0][1], datetime.strptime(x[0][0], "%b %Y"))):
    n = collections.Counter(r["encoding"] for r in rows)
    if (d, c) == ("Sep 2025", "SDN"):
        continue
    if n["B"] >= 1 or 1 <= n["A"] <= 10 or 1 <= n["C"] <= 10:
        cases.append(dict(analysis=d, country=c, counts=n, mixed=len(n) > 1, rows=rows))
json.dump(dict(cases=len(cases), single_encoding=sum(1 for x in cases if not x["mixed"]), list=cases),
          sys.stdout, indent=1)
