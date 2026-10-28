"""Session 236: date FEWS NET's 2025 dark window from its own data warehouse.

Inputs (not committed; fetched 2026-10-28, sha256 in sources.json):
  sd.json  = https://fdw.fews.net/api/ipcphase/?format=json&country_code=SD
  win.json = https://fdw.fews.net/api/ipcphase/?format=json&start_date=2024-01-01&end_date=2025-12-31&fields=simple
Usage: python3 -I analyze.py sd.json win.json > results.json
"""
import json, sys, collections, datetime as dt

sd = json.load(open(sys.argv[1]))
win = json.load(open(sys.argv[2]))

def months(rows):
    return sorted(set(r["reporting_date"] for r in rows))

# D1: Sudan, from the full Sudan series
sd_months = months(sd)
after = [m for m in sd_months if m >= "2025-01-01"]
before = [m for m in sd_months if m < "2025-01-01"]
last_before, first_after = before[-1], after[0]
gap_days = (dt.date.fromisoformat(first_after) - dt.date.fromisoformat(last_before)).days
created = collections.defaultdict(list)
for r in sd:
    created[r["reporting_date"]].append(r["created"][:10])
created_span = {m: [min(created[m]), max(created[m])] for m in sd_months if m >= "2024-06-01"}
docs = collections.Counter((r["reporting_date"], r["source_document"]) for r in sd if r["reporting_date"] in (last_before, first_after))

# D2: every country with a classification reported in 2024
by_c = collections.defaultdict(set)
names = {}
for r in win:
    by_c[r["country_code"]].add(r["reporting_date"])
    names[r["country_code"]] = r["country"]
c2024 = sorted(c for c, ms in by_c.items() if any(m.startswith("2024") for m in ms))
inside = lambda m: last_before < m < first_after
per_country = {}
for c in c2024:
    ms = sorted(by_c[c])
    b = [m for m in ms if m <= "2024-12-31"]
    a = [m for m in ms if m >= "2025-01-01"]
    per_country[c] = {
        "country": names[c],
        "last_2024": b[-1] if b else None,
        "first_2025": a[0] if a else None,
        "months_inside_sudan_window": [m for m in ms if inside(m)],
    }
dark = [c for c in c2024 if not per_country[c]["months_inside_sudan_window"]]
all_inside = collections.Counter(m for c in c2024 for m in per_country[c]["months_inside_sudan_window"])

json.dump({
    "sudan": {"rows": len(sd), "last_before": last_before, "first_after": first_after,
              "gap_days": gap_days, "months_strictly_inside": sum(1 for m in sd_months if last_before < m < first_after),
              "documents_at_edges": [[k[0], k[1], v] for k, v in docs.items()],
              "created_span_by_reporting_month": created_span},
    "countries_2024": len(c2024),
    "dark_in_sudan_window": len(dark),
    "share_dark": round(len(dark) / len(c2024), 3),
    "reporting_months_inside_window_across_countries": dict(sorted(all_inside.items())),
    "per_country": per_country,
}, sys.stdout, indent=1)
