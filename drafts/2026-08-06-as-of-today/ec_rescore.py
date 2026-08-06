#!/usr/bin/env python3
"""ec_rescore.py — answer to the session-95 Interlocutor, charge 3.

The chrome control (amendment 3) found 4 of EC's locked 40 corpus URLs to be chrome. Session 94's
P1-P4 were scored on all 40 and have never been re-examined against the standard this session
imposed on the new authorities. This recomputes P1-P4 on EC's item-only subset (36) from the LOCKED
signals.json. It does not alter signals.json, FINDINGS.md or any shipped verdict; it reports
whether any verdict would move. Writes ec-rescore.json.
"""
import datetime as dt, json, statistics
DAY = 86400.0
def iso(v): return dt.datetime.fromisoformat(v) if v else None
ec = json.load(open("signals.json"))
run = iso(ec["run_started_utc"])
chrome = {u.rstrip("/") for u in json.load(open("chrome-2.json"))["authorities"]["EC"]["chrome"]}
chrome.add("https://digital-strategy.ec.europa.eu")
def score(rows, label):
    ok = [r for r in rows if r.get("fetch") == "OK"]
    h = [r for r in ok if r.get("h")]
    p1n = sum(1 for r in h if (run - iso(r["h"])).total_seconds() < DAY)
    hs = [abs((iso(r["h"]) - iso(r["s"])).total_seconds())/DAY for r in ok if r.get("h") and r.get("s")]
    p3 = [r for r in ok if r.get("h") and r.get("s")
          and (run - iso(r["s"])).total_seconds() > 180*DAY
          and (run - iso(r["h"])).total_seconds() < DAY]
    v = [r for r in ok if r.get("v")]
    return {
        "arm": label, "n_ok": len(ok),
        "P1_share_h_under_24h": round(100*p1n/len(h), 1) if h else None,
        "P1_verdict": "HELD" if h and 100*p1n/len(h) >= 80 else "KILLED",
        "P2_median_hs_gap_days": round(statistics.median(hs), 2) if hs else None,
        "P2_verdict": "HELD" if hs and statistics.median(hs) > 30 else "KILLED",
        "P3_stale_s_fresh_h_n": len(p3), "P3_pairs_n": len(hs),
        "P3_share": round(100*len(p3)/len(hs), 1) if hs else None,
        "P3_verdict": "HELD" if hs and 100*len(p3)/len(hs) >= 25 else "KILLED",
        "P4_v_n": len(v), "P4_share": round(100*len(v)/len(ok), 1) if ok else None,
        "P4_verdict": "HELD" if ok and len(v)/len(ok) < 0.5 else "KILLED",
    }
alls = score(ec["rows"], "A (all 40, as scored in session 94)")
items = score([r for r in ec["rows"] if r["url"].rstrip("/") not in chrome], "B (items only, 36)")
moved = [k for k in ("P1_verdict","P2_verdict","P3_verdict","P4_verdict") if alls[k] != items[k]]
out = {"purpose": "re-score of session 94's P1-P4 on EC's item-only subset; locked data unchanged",
       "chrome_excluded": sorted(chrome - {"https://digital-strategy.ec.europa.eu"}),
       "arm_a": alls, "arm_b": items, "verdicts_that_move": moved}
json.dump(out, open("ec-rescore.json","w"), indent=1, ensure_ascii=False); open("ec-rescore.json","a").write("\n")
print(json.dumps(out, indent=1))
