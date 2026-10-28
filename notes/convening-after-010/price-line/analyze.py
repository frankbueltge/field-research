"""Session 237: score P1-P4 (PREDICTIONS.md) and describe the warehouse's entry dark.
Usage: python3 -I analyze.py warehouse.json pages.json > scores.json
P4's second half (a 2025 Price Watch page names Sudan) is read first-hand; the passage is in sources.json."""
import json, sys
w = json.load(open(sys.argv[1])); pg = json.load(open(sys.argv[2]))
C = w["countries"]
has = lambda c, k: (C[c]["months"].get(k) or {}).get("price", 0) > 0
months = lambda a, b: [f"{y}-{m:02d}" for y in (2024, 2025, 2026) for m in range(1, 13) if a <= f"{y}-{m:02d}" <= b]
dark25 = months("2025-01", "2025-08")
p1 = pg["price_bulletin_last_any"] <= "2024-10"
sd = {k: (C["SD"]["months"].get(k) or {}).get("price", 0) for k in dark25}
p2 = all(sd.values())
c24 = [c for c in C if any(has(c, k) for k in months("2024-01", "2024-12"))]
after = [c for c in c24 if any(has(c, k) for k in months("2025-07", "2026-09"))]
p3 = len(after) >= len(c24) / 2
pw_after = [k for k in pg["price_watch"] if k > "2024-10"]
p4 = bool(pw_after)  # and the first-hand Sudan passage of Oct 2025, sources.json
# entry dark: in which months were any prices entered at all, all countries pooled
ent = {}
for c in C:
    for v in C[c]["months"].values():
        for k, n in v["entered"].items():
            ent[k] = ent.get(k, 0) + n
span = months("2024-01", "2026-10")
zero_entry = [k for k in span if not ent.get(k)]
# per country: share of prices measured Oct 2024 - Jan 2026 that were entered more than 3 months late
late = {}
for c in c24:
    tot = sum((C[c]["months"].get(k) or {}).get("price", 0) for k in months("2024-10", "2026-01"))
    lt = sum((C[c]["months"].get(k) or {}).get("late", 0) for k in months("2024-10", "2026-01"))
    late[c] = {"name": C[c]["name"], "prices": tot, "late": lt, "share": round(lt / tot, 3) if tot else None}
sdm = C["SD"]["months"]
fam = {k: (sdm.get(k) or {}).get("source", {}).get("FAMIS, Sudan", 0) for k in months("2024-07", "2026-09")}
out = {"session": 237, "predictions": {
    "P1": {"held": p1, "last_price_bulletin": pg["price_bulletin_last_any"]},
    "P2": {"held": p2, "sudan_prices_by_month": sd},
    "P3": {"held": p3, "countries_2024": len(c24), "with_prices_after_2025_06": len(after),
           "without": sorted(C[c]["name"] for c in c24 if c not in after)},
    "P4": {"held": p4, "price_watch_after_2024_10": pw_after, "price_watch_gap": pg["price_watch_gap"]}},
    "held": sum([p1, p2, p3, p4]), "of": 4,
    "entered_per_month_all_countries": {k: ent.get(k, 0) for k in span},
    "months_with_no_price_entered": zero_entry,
    "late_share_oct2024_jan2026": late,
    "sudan_famis_prices_by_month": fam}
tot = sum(v["prices"] for v in late.values()); lt = sum(v["late"] for v in late.values())
out["pooled_late"] = {"prices": tot, "late": lt, "share": round(lt / tot, 3)}
json.dump(out, sys.stdout, indent=1)
