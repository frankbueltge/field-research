"""Per-analysis count of the three ways the IPC area table writes an unclassified area-period.

Usage: python3 -I summarize.py ipc_global_area_long.csv ipc_global_national_long.csv > summary.json
A: an `all` row only, population 0.  B: phase rows present, all zero, population 0.
C: phase rows present, all zero, population kept (people listed in no phase).
"""
import csv, collections, json, sys
from datetime import datetime

g = collections.defaultdict(dict)
for r in csv.DictReader(open(sys.argv[1], newline="")):
    if datetime.strptime(r["Date of analysis"], "%b %Y").year < 2017:
        continue
    g[(r["Date of analysis"], r["Country"], r["Validity period"], r["Level 1"], r["Area"])][r["Phase"]] = \
        int(round(float(r["Number"] or 0)))
nat = {}
for r in csv.DictReader(open(sys.argv[2], newline="")):
    nat[(r["Date of analysis"], r["Country"], r["Validity period"], r["Phase"])] = int(round(float(r["Number"] or 0)))

PH = "12345"
per = collections.defaultdict(lambda: dict(A=0, B=0, C=0, C_people=0, area_periods=0))
for (d, c, vp, l1, a), v in g.items():
    x = per[(d, c)]
    x["area_periods"] += 1
    if sum(v.get(p, 0) for p in PH) > 0:
        continue
    if not any(p in v for p in PH):
        x["A"] += 1
    elif v.get("all", 0) == 0:
        x["B"] += 1
    else:
        x["C"] += 1
        x["C_people"] += v["all"]

rows = [dict(analysis=d, country=c, **x) for (d, c), x in per.items()]
rows.sort(key=lambda r: (-(r["A"] + r["B"] + r["C"]), r["country"], r["analysis"]))

# Sudan, Sep 2025: the six areas the IPC names as not classified in the second projection
cur = {k[3:]: v for k, v in g.items() if k[:3] == ("Sep 2025", "SDN", "current")}
sp2 = {k[3:]: v for k, v in g.items() if k[:3] == ("Sep 2025", "SDN", "second projection")}
six = []
for a, v in cur.items():
    w = sp2.get(a, {})
    if sum(v.get(p, 0) for p in PH) > 0 and sum(w.get(p, 0) for p in PH) == 0:
        six.append(dict(level1=a[0], area=a[1], current_pop=v["all"], current_p5=v.get("5", 0),
                        current_p4=v.get("4", 0), projection_all=w.get("all"),
                        encoding="A" if not any(p in w for p in PH) else ("B" if w.get("all", 0) == 0 else "C")))
sudan = dict(areas=six, people=sum(s["current_pop"] for s in six), p5=sum(s["current_p5"] for s in six),
             national_p5_current=nat[("Sep 2025", "SDN", "current", "5")],
             national_all_current=nat[("Sep 2025", "SDN", "current", "all")],
             national_all_second=nat[("Sep 2025", "SDN", "second projection", "all")],
             national_p5_second=nat[("Sep 2025", "SDN", "second projection", "5")])
json.dump(dict(analyses=len(rows), with_any=sum(1 for r in rows if r["A"] + r["B"] + r["C"]),
               totals={k: sum(r[k] for r in rows) for k in ("A", "B", "C", "C_people", "area_periods")},
               sudan_sep2025=sudan, rows=rows), sys.stdout, indent=1)
