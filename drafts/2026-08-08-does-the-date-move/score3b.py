"""Scores PREREGISTRATION-3B.md exactly as written. Writes scored-3b.json."""
import json, collections, datetime as dt

BASE = "/home/user/field-research/drafts/2026-08-08-does-the-date-move"
obs = json.load(open(f"{BASE}/observations-3b.json"))
FETCH = obs["fetch_date_utc"]

by = collections.defaultdict(list)
for r in obs["rows"]:
    if r["status"] == "MEASURED" and r.get("v_updated"):
        by[r["authority"]].append(r)

out = {"fetch_date_utc": FETCH, "authorities": {}, "predictions": {}}

for auth, rows in by.items():
    n = len(rows)
    vals = [r["v_updated"] for r in rows]
    cnt = collections.Counter(vals)
    modal_val, modal_n = cnt.most_common(1)[0]

    # cross-year sharing: page shares its v_updated with >=1 other page whose own
    # published/created year differs from this page's published/created year
    year_by_val = collections.defaultdict(list)
    for r in rows:
        py = (r.get("v_published") or "")[:4]
        year_by_val[r["v_updated"]].append(py)
    cross = 0
    for r in rows:
        py = (r.get("v_published") or "")[:4]
        peers = year_by_val[r["v_updated"]]
        if any(p and py and p != py for p in peers):
            cross += 1

    future = sum(1 for r in rows if r["v_updated"] > FETCH)
    before_pub = sum(1 for r in rows
                     if r.get("v_published") and r["v_updated"] < r["v_published"])

    out["authorities"][auth] = {
        "measured_with_date": n,
        "sampled": sum(1 for r in obs["rows"] if r["authority"] == auth),
        "distinct_values": len(cnt),
        "distinct_value_ratio": round(len(cnt) / n, 4),
        "modal_value": modal_val,
        "modal_n": modal_n,
        "modal_share": round(modal_n / n, 4),
        "top5": cnt.most_common(5),
        "cross_year_sharing": round(cross / n, 4),
        "cross_year_n": cross,
        "v_updated_in_future": future,
        "v_updated_before_published": before_pub,
        "validity_violation_share": round((future + before_pub) / n, 4),
        "published_year_range": sorted({(r.get("v_published") or "?")[:4] for r in rows}),
    }

A = out["authorities"]
P = out["predictions"]
P["Q1 EPA cross-year sharing >= 50%"] = {
    "value": A["epa"]["cross_year_sharing"], "threshold": 0.50,
    "verdict": "HELD" if A["epa"]["cross_year_sharing"] >= 0.50 else "NOT HELD"}
P["Q2 EPA modal share >= 20%"] = {
    "value": A["epa"]["modal_share"], "threshold": 0.20,
    "verdict": "HELD" if A["epa"]["modal_share"] >= 0.20 else "NOT HELD"}
P["Q3 NIST cross-year sharing >= 40%"] = {
    "value": A["nist"]["cross_year_sharing"], "threshold": 0.40,
    "verdict": "HELD" if A["nist"]["cross_year_sharing"] >= 0.40 else "NOT HELD"}
P["Q4 distinct-value ratio < 0.6 on NIST and EPA"] = {
    "nist": A["nist"]["distinct_value_ratio"], "epa": A["epa"]["distinct_value_ratio"],
    "threshold": 0.60,
    "verdict": "HELD" if (A["nist"]["distinct_value_ratio"] < 0.60
                          and A["epa"]["distinct_value_ratio"] < 0.60) else "NOT HELD"}
P["Q5 control: GOV.UK ratio > 0.8 and modal share < 10%"] = {
    "ratio": A["govuk"]["distinct_value_ratio"], "modal_share": A["govuk"]["modal_share"],
    "verdict": "HELD" if (A["govuk"]["distinct_value_ratio"] > 0.80
                          and A["govuk"]["modal_share"] < 0.10) else "NOT HELD"}
P["Q6 validity violations < 2%"] = {
    "nist": A["nist"]["validity_violation_share"], "epa": A["epa"]["validity_violation_share"],
    "govuk": A["govuk"]["validity_violation_share"], "threshold": 0.02,
    "verdict": "HELD" if all(A[a]["validity_violation_share"] < 0.02
                             for a in ("nist", "epa", "govuk")) else "NOT HELD"}
q7 = all(A[a]["distinct_value_ratio"] >= 0.90 and A[a]["modal_share"] < 0.05
         for a in ("nist", "epa"))
P["Q7 falsifier: date is document-specific on NIST and EPA"] = {
    "verdict": "FIRED — the test finds nothing" if q7 else "did not fire"}

# the largest cluster's members, for the Q8 hand-check
out["largest_cluster_members"] = {}
for auth in ("nist", "epa"):
    mv = A[auth]["modal_value"]
    out["largest_cluster_members"][auth] = [
        {"url": r["url"], "v_published": r.get("v_published"), "v_updated": r["v_updated"]}
        for r in by[auth] if r["v_updated"] == mv]

json.dump(out, open(f"{BASE}/scored-3b.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out["authorities"].items()}, indent=1))
print(json.dumps(P, indent=1))
