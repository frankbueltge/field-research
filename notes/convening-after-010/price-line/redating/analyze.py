"""Session 239: which streams of FEWS NET's warehouse were re-dated, and what that does to session 237's late counts.

Input (not committed; fetched 2026-10-29, sha256 per file in sources.json): one file per country,
https://fdw.fews.net/api/marketpricefacts/?format=json&country_code=<CC>&start_date=2024-01-01&end_date=2026-10-29
Usage: python3 -I analyze.py <dir with CC.json files> > results.json
Definitions are those fixed in PREDICTIONS.md: a stream is (country, source_organization); a stream is re-dated
when the median entry lag of its prices for periods 2024-01..2024-06 exceeds 6 months; late = entered more than
three calendar months after the period month. A row "has a price" when value is not null. Entry = created.
"""
import json, sys, os, hashlib, collections
D = sys.argv[1]
mi = lambda s: int(s[:4]) * 12 + int(s[5:7]) - 1
DARK = ("2024-10", "2026-01")          # session 237's span for late shares
H1 = ("2024-01", "2024-06")            # the window that decides re-dating
inside = lambda m, w: w[0] <= m <= w[1]
files, streams, rows_all = {}, {}, []
for f in sorted(os.listdir(D)):
    if not f.endswith(".json") or len(f) != 7:
        continue
    raw = open(os.path.join(D, f), "rb").read()
    rows = json.loads(raw)
    files[f[:2]] = {"rows": len(rows), "sha256": hashlib.sha256(raw).hexdigest()}
    for x in rows:
        if x["value"] is None:
            continue
        p, c = x["period_date"][:7], x["created"][:10]
        rows_all.append((f[:2], x["source_organization"], p, c, mi(c[:7]) - mi(p)))

# re-dating per stream
by = collections.defaultdict(list)
for cc, s, p, c, lag in rows_all:
    by[(cc, s)].append((p, c, lag))
for (cc, s), v in sorted(by.items()):
    h1 = sorted(l for p, c, l in v if inside(p, H1))
    med = h1[len(h1) // 2] if h1 else None
    first = min(c for p, c, l in v)
    streams[f"{cc}|{s}"] = {"prices": len(v), "h1_2024_prices": len(h1), "h1_median_lag": med,
                            "earliest_entry": first, "redated": med is not None and med > 6}
red = {k for k, v in streams.items() if v["redated"]}

def late(pred):
    n = l = 0
    for cc, s, p, c, lag in rows_all:
        if inside(p, DARK) and pred(cc, s):
            n += 1; l += lag > 3
    return {"prices": n, "late": l, "share": round(l / n, 4) if n else None}

def entry_months(pred, lo="2025-02", hi="2025-05"):
    return sum(1 for cc, s, p, c, lag in rows_all if pred(cc, s) and lo <= c[:7] <= hi)

isred = lambda cc, s: f"{cc}|{s}" in red
sd = [r for r in rows_all if r[0] == "SD"]
sd_late = [r for r in sd if inside(r[2], DARK) and r[4] > 3]
famis = [r for r in sd if r[1] == "FAMIS, Sudan"]
famis_dark = [r for r in famis if inside(r[2], DARK)]
wfp_h1 = sorted(r[3] for r in sd if r[1] == "WFP" and inside(r[2], H1))
countries_with_red = sorted({k.split("|")[0] for k in red})
countries_33 = sorted({r[0] for r in rows_all if r[2].startswith("2024")})

res = {
    "R1": {"wfp_sd_h1_prices": len(wfp_h1), "median_entry": wfp_h1[len(wfp_h1) // 2] if wfp_h1 else None,
           "held": bool(wfp_h1) and wfp_h1[len(wfp_h1) // 2][:7] >= "2026-06"},
    "R2": {"sd_late": len(sd_late), "wfp_late": sum(1 for r in sd_late if r[1] == "WFP")},
    "R3": {"famis_entered_in_gap": sum(1 for r in famis if "2024-10-01" <= r[3] <= "2026-02-02"),
           "famis_dark_prices": len(famis_dark), "famis_dark_late": sum(1 for r in famis_dark if r[4] > 3)},
    "R4": {"countries_with_prices_2024": len(countries_33), "countries_with_redated_stream": countries_with_red},
    "R5": {"all": late(lambda cc, s: cc in countries_33), "not_redated": late(lambda cc, s: cc in countries_33 and not isred(cc, s)),
           "redated": late(lambda cc, s: cc in countries_33 and isred(cc, s))},
    "R6": {"entries_2025_02_to_05_all": entry_months(lambda cc, s: True),
           "entries_2025_02_to_05_not_redated": entry_months(lambda cc, s: not isred(cc, s))},
}
r2 = res["R2"]; r2["share"] = round(r2["wfp_late"] / r2["sd_late"], 4) if r2["sd_late"] else None
r2["held"] = r2["share"] is not None and 0.70 <= r2["share"] <= 0.85
r3 = res["R3"]; r3["held"] = r3["famis_entered_in_gap"] == 0 and r3["famis_dark_prices"] > 0 and r3["famis_dark_late"] / r3["famis_dark_prices"] >= 0.90
res["R4"]["held"] = len(countries_with_red) >= 5
r5 = res["R5"]; r5["held"] = r5["not_redated"]["share"] is not None and r5["not_redated"]["share"] < 0.25
res["R6"]["held"] = res["R6"]["entries_2025_02_to_05_not_redated"] == 0
# streams with no H1-2024 prices cannot be judged by the rule; count their dark-span prices separately
unj = [k for k, v in streams.items() if v["h1_median_lag"] is None]
res["unjudged_streams"] = {"n": len(unj), "dark_prices": late(lambda cc, s: f"{cc}|{s}" in unj and cc in countries_33)}
# per country and measured month: [prices, late] in streams kept, then in re-dated streams (for the page)
grid = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 0, 0]))
for cc, s, p, c, lag in rows_all:
    g = grid[cc][p]; i = 2 if isred(cc, s) else 0
    g[i] += 1; g[i + 1] += lag > 3
json.dump({"session": 239, "files": files, "results": res, "streams": streams,
           "grid": {cc: dict(sorted(v.items())) for cc, v in sorted(grid.items())}}, sys.stdout, indent=1)
