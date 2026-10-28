"""Session 236: products per country and month on fews.net, from its own sitemap.

Input (not committed; fetched 2026-10-28, sha256 in sources.json): urls.txt, every <loc> of
https://fews.net/sitemap.xml?page=1..N. A product URL is /<region>/<country>/<type>/<month>-<year>[-k].
Usage: python3 -I timeline.py urls.txt results.json > timeline.json
"""
import json, re, sys, collections
MON = "january february march april may june july august september october november december".split()
pat = re.compile(r"https://fews\.net/([a-z-]+)/([a-z-]+)/([a-z-]+)/(" + "|".join(MON) + r")-(20\d\d)(?:-\d+)?$")
months = [f"{y}-{m:02d}" for y in (2024, 2025, 2026) for m in range(1, 13)][6:24]  # 2024-07 .. 2025-12
# analysis = a food-security judgement; monitor = remote sensing, prices, calendars (no judgement)
MONITOR = {"seasonal-monitor", "price-bulletin", "seasonal-calendar", "agroclimatology", "livelihood-zone-map"}
kind = lambda t: "monitor" if t in MONITOR else "analysis"
cells = collections.defaultdict(lambda: collections.defaultdict(list))
regions = {}
for u in open(sys.argv[1]).read().split():
    m = pat.match(u)
    if not m:
        continue
    reg, c, t, mon, y = m.groups()
    if c in ("global", "special-report") or reg == "global":
        continue
    k = f"{y}-{MON.index(mon) + 1:02d}"
    if k in months:
        cells[c][k].append(t)
        regions[c] = reg
res = json.load(open(sys.argv[2]))
wh = {v["country"].lower().replace(" ", "-"): v for v in res["per_country"].values()}
rows = []
for c in sorted(cells, key=lambda c: (regions[c], c)):
    ms = [k for k in months if cells[c].get(k)]
    in25 = [k for k in ms if k.startswith("2025")]
    rows.append({"country": c, "region": regions[c],
                 "products": {k: sorted(cells[c][k]) for k in months if cells[c].get(k)},
                 "first_2025": in25[0] if in25 else None,
                 "warehouse_first_2025": (wh.get(c) or {}).get("first_2025")})
def has(r, k, kd):
    return any(kind(t) == kd for t in r["products"].get(k, []))
for r in rows:
    a25 = [k for k in months if k.startswith("2025") and has(r, k, "analysis")]
    r["first_2025_analysis"] = a25[0] if a25 else None
    r["last_2024_analysis"] = ([k for k in months if k.startswith("2024") and has(r, k, "analysis")] or [None])[-1]
counts = {k: {"analysis": sum(has(r, k, "analysis") for r in rows),
              "monitor": sum(has(r, k, "monitor") for r in rows)} for k in months}
types = collections.Counter(t for r in rows for ts in r["products"].values() for t in ts)
json.dump({"months": months, "countries": len(rows), "monitor_types": sorted(MONITOR),
           "types": dict(types.most_common()), "countries_with_product": counts,
           "first_2025_analysis_counts": collections.Counter(r["first_2025_analysis"] for r in rows),
           "first_2025_counts": collections.Counter(r["first_2025"] for r in rows),
           "rows": rows}, sys.stdout, indent=1)
