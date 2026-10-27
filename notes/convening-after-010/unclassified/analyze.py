"""Unclassified areas in the IPC's open area table (answers ho-2026-10-26-atelier-1).

Usage: python3 -I analyze.py ipc_global_area_long.csv ipc_global_national_long.csv [pre|amended] > results-<def>.json
Definitions and predictions: PREDICTIONS.md (fixed before this script ran on the full table).
"""
import csv, collections, json, sys
from datetime import datetime

area_csv, nat_csv = sys.argv[1], sys.argv[2]

def num(s):
    return int(round(float(s))) if s not in ("", None) else 0

def year(d):
    return datetime.strptime(d, "%b %Y").year

g = collections.defaultdict(dict)
dupes = 0
for r in csv.DictReader(open(area_csv, newline="")):
    if year(r["Date of analysis"]) < 2017:
        continue
    k = (r["Date of analysis"], r["Country"], r["Validity period"], r["Level 1"], r["Area"])
    if r["Phase"] in g[k]:
        dupes += 1
    g[k][r["Phase"]] = num(r["Number"])

nat = {}
for r in csv.DictReader(open(nat_csv, newline="")):
    nat[(r["Date of analysis"], r["Country"], r["Validity period"], r["Phase"])] = num(r["Number"])

PH = {"1", "2", "3", "4", "5"}
analyses = collections.defaultdict(lambda: collections.defaultdict(dict))
for (d, c, vp, l1, a), v in g.items():
    analyses[(d, c)][vp][(l1, a)] = v

# DEFINITION "pre": unclassified = an `all` row and no phase rows (as fixed in PREDICTIONS.md).
# DEFINITION "amended" (after reading Sudan Sep 2025 row by row): unclassified = phases 1-5 sum to 0,
# whether the phase rows are missing or present as zeros. Selected by the third argument.
DEF = sys.argv[3] if len(sys.argv) > 3 else "pre"

def classified(v):
    if DEF == "pre":
        return PH <= set(v)
    return sum(v.get(p, 0) for p in PH) > 0

# P1, P2: unclassified area-periods
unc = [(k, v) for k, v in g.items() if not classified(v)]
unc_analyses = sorted({(k[0], k[1]) for k, _ in unc})
unc_zero = sum(1 for _, v in unc if v.get("all", 0) == 0)

# Dropped areas: classified in current, unclassified (in place) or absent in a projection
drops = []
for (d, c), periods in analyses.items():
    cur = {a: v for a, v in periods.get("current", {}).items() if classified(v)}
    if not cur:
        continue
    for vp in ("first projection", "second projection"):
        if vp not in periods:
            continue
        proj = periods[vp]
        if not any(classified(v) for v in proj.values()):
            continue  # projection not published at area level at all
        for a, v in cur.items():
            if a not in proj:
                kind = "absent"
            elif not classified(proj[a]):
                kind = "unclassified"
            else:
                continue
            drops.append(dict(analysis=d, country=c, projection=vp, level1=a[0], area=a[1], kind=kind,
                              current_pop=v.get("all", 0), current_p5=v.get("5", 0),
                              current_p4plus=v.get("4", 0) + v.get("5", 0),
                              projection_pop=proj.get(a, {}).get("all")))

def pooled(kinds):
    sel = [x for x in drops if x["kind"] in kinds]
    per = collections.defaultdict(dict)
    for x in sel:  # an area dropped in both projections counts once per analysis
        per[(x["analysis"], x["country"])][(x["level1"], x["area"])] = x
    dp = d5 = d45 = tp = t5 = t45 = 0
    rows = []
    for (d, c), areas in sorted(per.items()):
        cur = [v for v in analyses[(d, c)]["current"].values() if classified(v)]
        T = sum(v.get("all", 0) for v in cur); T5 = sum(v.get("5", 0) for v in cur)
        T45 = sum(v.get("4", 0) + v.get("5", 0) for v in cur)
        P = sum(x["current_pop"] for x in areas.values()); P5 = sum(x["current_p5"] for x in areas.values())
        P45 = sum(x["current_p4plus"] for x in areas.values())
        dp += P; d5 += P5; d45 += P45; tp += T; t5 += T5; t45 += T45
        rows.append(dict(analysis=d, country=c, areas=len(areas), pop=P, pop_total=T, p5=P5, p5_total=T5,
                         p4plus=P45, p4plus_total=T45))
    r5 = (d5 / t5) / (dp / tp) if t5 and dp else None
    r45 = (d45 / t45) / (dp / tp) if t45 and dp else None
    return dict(analyses=len(per), dropped_pop=dp, total_pop=tp, dropped_p5=d5, total_p5=t5,
                dropped_p4plus=d45, total_p4plus=t45, ratio_p5=r5, ratio_p4plus=r45, per_analysis=rows)

# P4: national 'all' of the projection vs current, where an area was dropped in place
p4 = []
for (d, c, vp) in sorted({(x["analysis"], x["country"], x["projection"]) for x in drops if x["kind"] == "unclassified"}):
    a0, a1 = nat.get((d, c, "current", "all")), nat.get((d, c, vp, "all"))
    dropped = sum(x["current_pop"] for x in drops if (x["analysis"], x["country"], x["projection"], x["kind"]) == (d, c, vp, "unclassified"))
    p4.append(dict(analysis=d, country=c, projection=vp, national_current=a0, national_projection=a1,
                   fall=(a0 - a1) if a0 is not None and a1 is not None else None, dropped_current_pop=dropped))
p4_lower = sum(1 for x in p4 if x["fall"] is not None and x["fall"] > 0)
p4_known = sum(1 for x in p4 if x["fall"] is not None)

out = dict(definition=DEF,
    unclassified_pop_positive=sum(1 for _, v in unc if v.get("all", 0) > 0),
    unclassified_pop_positive_people=sum(v.get("all", 0) for _, v in unc),
    area_periods=len(g), duplicate_phase_rows=dupes, analyses=len(analyses),
    unclassified_area_periods=len(unc), unclassified_analyses=len(unc_analyses),
    unclassified_pop_zero=unc_zero,
    unclassified_by_country=collections.Counter(k[1] for k, _ in unc).most_common(),
    drops_total=len(drops), drops_by_kind=collections.Counter(x["kind"] for x in drops),
    pooled_in_place=pooled({"unclassified"}), pooled_all=pooled({"unclassified", "absent"}),
    p4=dict(cases=len(p4), known=p4_known, national_lower=p4_lower, rows=p4),
    drops_in_place=[x for x in drops if x["kind"] == "unclassified"],
)
json.dump(out, sys.stdout, indent=1, default=str)
