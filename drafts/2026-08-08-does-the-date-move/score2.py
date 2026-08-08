"""Scores PREREGISTRATION-2.md against census.json. Writes scored-2.json and prints a report.

Denominator rule from the pre-registration: errored queries are excluded from percentages and
counted separately; zero-capture URLs stay in every denominator.
"""
import json, statistics as st

BASE = "/home/user/field-research/drafts/2026-08-08-does-the-date-move"
c = json.load(open(f"{BASE}/census.json"))
AUTH = c["authorities"]
SAMPLED = [k for k in AUTH if k != "receiver"]


def clean(key):
    return [r for r in AUTH[key] if "error" not in r]


def errs(key):
    return [r for r in AUTH[key] if "error" in r]


def pct(a, b):
    return None if not b else round(100.0 * a / b, 1)


def quantile(xs, q):
    if not xs:
        return None
    xs = sorted(xs)
    i = q * (len(xs) - 1)
    lo, hi = int(i), min(int(i) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


pool = [r for k in SAMPLED for r in clean(k)]
out = {"per_authority": {}, "pooled": {}, "predictions": {}}

for k in list(AUTH):
    rs = clean(k)
    n12 = [r["n12"] for r in rs]
    out["per_authority"][k] = {
        "sampled": len(AUTH[k]), "measured": len(rs), "errors": len(errs(k)),
        "zero_capture_24m": sum(1 for r in rs if r["n24"] == 0),
        "zero_capture_24m_pct": pct(sum(1 for r in rs if r["n24"] == 0), len(rs)),
        "n12_median": st.median(n12) if n12 else None,
        "n12_mean": round(st.mean(n12), 2) if n12 else None,
        "n12_p90": quantile(n12, 0.90),
        "n12_max": max(n12) if n12 else None,
        "months12_median": st.median([r["months12"] for r in rs]) if rs else None,
        "months12_ge6": sum(1 for r in rs if r["months12"] >= 6),
        "months12_ge6_pct": pct(sum(1 for r in rs if r["months12"] >= 6), len(rs)),
        "months12_ge2": sum(1 for r in rs if r["months12"] >= 2),
        "pairable": sum(1 for r in rs if r["pairable"]),
        "pairable_pct": pct(sum(1 for r in rs if r["pairable"]), len(rs)),
        "truncated": sum(1 for r in rs if r.get("truncated")),
    }

n12p = [r["n12"] for r in pool]
out["pooled"] = {
    "measured": len(pool), "errors": sum(len(errs(k)) for k in SAMPLED),
    "n12_median": st.median(n12p) if n12p else None,
    "n12_p90": quantile(n12p, 0.90),
    "months12_ge6": sum(1 for r in pool if r["months12"] >= 6),
    "months12_ge6_pct": pct(sum(1 for r in pool if r["months12"] >= 6), len(pool)),
    "pairable": sum(1 for r in pool if r["pairable"]),
    "pairable_pct": pct(sum(1 for r in pool if r["pairable"]), len(pool)),
    "zero_capture_24m": sum(1 for r in pool if r["n24"] == 0),
    "zero_capture_24m_pct": pct(sum(1 for r in pool if r["n24"] == 0), len(pool)),
}

P = out["predictions"]
P["P5"] = {"claim": "pooled median n12 <= 4", "value": out["pooled"]["n12_median"],
           "verdict": "HELD" if (out["pooled"]["n12_median"] or 0) <= 4 else "NOT HELD"}
P["P6"] = {"claim": "< 25% of document pages have months12 >= 6",
           "value": out["pooled"]["months12_ge6_pct"],
           "verdict": "HELD" if (out["pooled"]["months12_ge6_pct"] or 0) < 25 else "NOT HELD"}
best = max(((k, out["per_authority"][k]["pairable"]) for k in SAMPLED), key=lambda x: x[1],
           default=(None, 0))
P["P7"] = {"claim": ">= 1 authority with >= 30 pairable document pages",
           "value": f"{best[0]}={best[1]}",
           "verdict": "HELD" if best[1] >= 30 else "NOT HELD"}
P["P8"] = {"claim": "pooled p90 of n12 < 42 (increment 1's smallest index-page count)",
           "value": out["pooled"]["n12_p90"],
           "verdict": "HELD" if (out["pooled"]["n12_p90"] or 0) < 42 else "NOT HELD"}
P["P9"] = {"claim": "FALSIFIER: >= 50% of document pages have months12 >= 6 -> D4 withdrawn",
           "value": out["pooled"]["months12_ge6_pct"],
           "verdict": "FIRED" if (out["pooled"]["months12_ge6_pct"] or 0) >= 50 else "did not fire"}
rp = out["per_authority"].get("receiver")
P["P10"] = {"claim": "< 50% of the receiver's own pages are pairable",
            "value": rp and rp["pairable_pct"],
            "verdict": None if not rp else ("HELD" if (rp["pairable_pct"] or 0) < 50 else "NOT HELD")}

json.dump(out, open(f"{BASE}/scored-2.json", "w"), indent=1)
print(json.dumps(out, indent=1))
