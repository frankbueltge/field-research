"""Session 237: price products on fews.net by month, from its sitemap (urls.txt, not committed; sha256 in sources.json).
Usage: python3 -I pages.py urls.txt > pages.json"""
import json, re, sys, collections
MON = "january february march april may june july august september october november december".split()
pat = re.compile(r"https://fews\.net/([a-z-]+)/([a-z-]+)/([a-z-]+)/(" + "|".join(MON) + r")-(20\d\d)(?:-\d+)?$")
bull = collections.defaultdict(set); watch = set(); last = {}
for u in open(sys.argv[1]).read().split():
    w = re.match(r"https://fews\.net/global/price-watch/(" + "|".join(MON) + r")-(20\d\d)(?:-\d+)?$", u)
    if w:
        watch.add(f"{w.group(2)}-{MON.index(w.group(1)) + 1:02d}")
    m = pat.match(u)
    if not m:
        continue
    reg, c, t, mon, y = m.groups()
    k = f"{y}-{MON.index(mon) + 1:02d}"
    if t == "price-bulletin":
        bull[k].add(c); last[c] = max(last.get(c, ""), k)
ks = [k for k in sorted(set(bull) | watch) if k >= "2024-01"]
json.dump({"price_bulletin_countries": {k: sorted(bull[k]) for k in sorted(bull) if k >= "2024-01"},
           "price_bulletin_last_any": max(last.values()),
           "price_watch": sorted(k for k in watch if k >= "2024-01"),
           "price_watch_gap": [f"{y}-{m:02d}" for y in (2024, 2025) for m in range(1, 13)
                               if "2024-10" < f"{y}-{m:02d}" < "2025-10" and f"{y}-{m:02d}" not in watch]},
          sys.stdout, indent=1)
