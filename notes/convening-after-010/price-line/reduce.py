"""Session 237: FEWS NET data-warehouse market prices, per country and month, with the month each row was entered.

Input (not committed; fetched 2026-10-28, sha256 per file in sources.json): one file per country,
https://fdw.fews.net/api/marketpricefacts/?format=json&country_code=<CC>&start_date=2024-01-01&end_date=2026-10-28
Usage: python3 -I reduce.py <dir with CC.json files> > warehouse.json
A row "has a price" when value is not null. Entry month = created[:7]. Lag = entry month minus period month.
"""
import json, sys, os, collections, hashlib
D = sys.argv[1]
mi = lambda s: int(s[:4]) * 12 + int(s[5:7]) - 1
out = {"files": {}, "countries": {}}
for f in sorted(os.listdir(D)):
    if not f.endswith(".json") or len(f) != 7:
        continue
    raw = open(os.path.join(D, f), "rb").read()
    rows = json.loads(raw)
    cc = f[:2]
    out["files"][cc] = {"rows": len(rows), "sha256": hashlib.sha256(raw).hexdigest()}
    if not rows:
        continue
    months = collections.defaultdict(lambda: {"price": 0, "status": collections.Counter(), "source": collections.Counter(),
                                              "entered": collections.Counter(), "markets": set()})
    for x in rows:
        k = x["period_date"][:7]
        m = months[k]
        if x["value"] is None:
            m["status"][x["status"]] += 1
            continue
        m["price"] += 1
        m["source"][x["source_organization"]] += 1
        m["entered"][x["created"][:7]] += 1
        m["markets"].add(x["market"])
    res = {}
    for k in sorted(months):
        m = months[k]
        lags = sorted(mi(e) - mi(k) for e, n in m["entered"].items() for _ in range(n))
        res[k] = {"price": m["price"], "markets": len(m["markets"]), "missing": dict(m["status"]),
                  "source": dict(m["source"]), "entered": dict(sorted(m["entered"].items())),
                  "lag_median": lags[len(lags) // 2] if lags else None,
                  "late": sum(1 for l in lags if l > 3)}
    out["countries"][cc] = {"name": rows[0]["country"], "months": res}
json.dump(out, sys.stdout, indent=1)
