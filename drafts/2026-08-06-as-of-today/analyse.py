#!/usr/bin/env python3
"""analyse.py — score the four pre-registered predictions, and nothing else as a result.

Reads signals.json. Writes results.json and prints the table that FINDINGS.md quotes.

Everything under "unpredicted" is exactly that: observed after the run, reported as an
observation and never scored as a hit. The four predictions are scored by the rules in
PREREGISTRATION.md and a killed prediction is printed in the same form as one that holds.
"""

from __future__ import annotations

import datetime as dt
import json
import statistics

DAY = 86400.0


def iso(v):
    return dt.datetime.fromisoformat(v) if v else None


def main() -> int:
    d = json.load(open("signals.json"))
    run = iso(d["run_started_utc"])
    rows = d["rows"]

    ok = [r for r in rows if r["fetch"] == "OK"]
    netfail = [r for r in rows if r["fetch"] != "OK"]

    with_h = [r for r in ok if r["h"]]
    with_s = [r for r in ok if r["s"]]
    with_v = [r for r in ok if r["v"]]
    both = [r for r in ok if r["h"] and r["s"]]

    # P1 — H within 24h of the run timestamp
    h_age_h = {r["url"]: (run - iso(r["h"])).total_seconds() / 3600.0 for r in with_h}
    p1_hits = [u for u, a in h_age_h.items() if a < 24]
    p1_share = len(p1_hits) / len(with_h) if with_h else 0.0

    # P2 — median |H - S| in days, over rows with both
    gaps = sorted(abs((iso(r["h"]) - iso(r["s"])).total_seconds()) / DAY for r in both)
    p2_median = statistics.median(gaps) if gaps else None

    # P3 — S older than 180 days while H younger than 24h
    p3_hits = [r["url"] for r in both
               if (run - iso(r["s"])).total_seconds() / DAY > 180
               and (run - iso(r["h"])).total_seconds() / 3600.0 < 24]
    p3_share = len(p3_hits) / len(both) if both else 0.0

    # P4 — a visible date on fewer than half the fetched pages
    p4_share = len(with_v) / len(ok) if ok else 0.0

    preds = [
        {"id": "P1", "claim": "≥80% of URLs with a Last-Modified header carry one younger than 24h",
         "threshold": ">= 0.80", "observed": round(p1_share, 4),
         "n": f"{len(p1_hits)}/{len(with_h)}", "verdict": "HELD" if p1_share >= 0.80 else "KILLED"},
        {"id": "P2", "claim": "median |H - S| exceeds 30 days",
         "threshold": "> 30 days", "observed": round(p2_median, 2) if p2_median is not None else None,
         "n": f"{len(both)} pairs", "verdict": "HELD" if (p2_median or 0) > 30 else "KILLED"},
        {"id": "P3", "claim": "≥25% of pairs have S older than 180d while H is younger than 24h",
         "threshold": ">= 0.25", "observed": round(p3_share, 4),
         "n": f"{len(p3_hits)}/{len(both)}", "verdict": "HELD" if p3_share >= 0.25 else "KILLED"},
        {"id": "P4", "claim": "a visible date is found on fewer than half the pages",
         "threshold": "< 0.50", "observed": round(p4_share, 4),
         "n": f"{len(with_v)}/{len(ok)}", "verdict": "HELD" if p4_share < 0.50 else "KILLED"},
    ]

    # --- unpredicted observations, scored as nothing ---------------------------------
    sv = [r for r in ok if r["s"] and r["v"]]
    sv_same_day = [r for r in sv if r["s"][:10] == r["v"][:10]]
    # section landing page = exactly one path segment after /en/ ; post-hoc split, disclosed
    def depth(u):
        return len([p for p in u.split("/en/", 1)[1].split("/") if p])
    landing = [r for r in ok if depth(r["url"]) == 1]
    item = [r for r in ok if depth(r["url"]) > 1]
    s_ages = sorted((run - iso(r["s"])).total_seconds() / DAY for r in with_s)
    v_ages = sorted((run - iso(r["v"])).total_seconds() / DAY for r in with_v)

    unpredicted = {
        "sitemap_coverage": {"in_sitemap": len(with_s), "of": len(ok),
                             "share": round(len(with_s) / len(ok), 4)},
        "visible_date_coverage": {"with_v": len(with_v), "of": len(ok),
                                  "share": round(len(with_v) / len(ok), 4)},
        "S_and_V_agree_to_the_day": {"agree": len(sv_same_day), "of": len(sv),
                                     "share": round(len(sv_same_day) / len(sv), 4) if sv else None,
                                     "disagreements": [
                                         {"url": r["url"], "s": r["s"][:10], "v": r["v"][:10]}
                                         for r in sv if r["s"][:10] != r["v"][:10]]},
        "median_age_days": {"S": round(statistics.median(s_ages), 1) if s_ages else None,
                            "V": round(statistics.median(v_ages), 1) if v_ages else None,
                            "H_hours": round(statistics.median(list(h_age_h.values())), 2) if h_age_h else None},
        "H_age_hours_max": round(max(h_age_h.values()), 2) if h_age_h else None,
        "post_hoc_split_landing_vs_item": {
            "note": "one path segment after /en/ = section landing page; two or more = item page. "
                    "Defined after the run, reported as an observation, not a scored result.",
            "landing": {"n": len(landing),
                        "with_s": sum(1 for r in landing if r["s"]),
                        "with_v": sum(1 for r in landing if r["v"])},
            "item": {"n": len(item),
                     "with_s": sum(1 for r in item if r["s"]),
                     "with_v": sum(1 for r in item if r["v"])}},
        "P3_phenomenon_measured_against_V_instead_of_S": {
            "note": "NOT a prediction and NOT scored. P3 could only be scored where S exists, and S "
                    "exists for none of the /news/ or /library/ items — i.e. the scoring set "
                    "excluded most of the corpus's older documents. This is the same count run "
                    "against the visible date V, computed after the run and reported as an "
                    "observation. It is a defect of the pre-registered rule (D2), reported, not "
                    "repaired.",
            "hits": [{"url": r["url"], "v": r["v"][:10],
                      "v_age_days": round((run - iso(r["v"])).total_seconds() / DAY, 1)}
                     for r in with_v
                     if (run - iso(r["v"])).total_seconds() / DAY > 180
                     and r["h"] and (run - iso(r["h"])).total_seconds() / 3600.0 < 24],
            "of_pairs": len([r for r in with_v if r["h"]]),
        },
        # Item pages only (depth > 1). The section LANDING page (/en/news, /en/library, /en/policies)
        # shares its section's name at depth 1; counting it in the denominator inflated
        # library, news and policies by one each in the first cut of this run. Found by the
        # Verifier, session 94, and fixed here at the root (see FINDINGS.md, D7).
        "sitemap_coverage_by_section": {
            sec: {"in_sitemap": sum(1 for r in ok if r["s"] and depth(r["url"]) > 1
                                    and r["url"].split("/en/")[1].split("/")[0] == sec),
                  "item_pages": sum(1 for r in ok if depth(r["url"]) > 1
                                    and r["url"].split("/en/")[1].split("/")[0] == sec)}
            for sec in sorted({r["url"].split("/en/")[1].split("/")[0] for r in ok if depth(r["url"]) > 1})
        },
        "pages_with_no_date_signal_but_H": [
            r["url"] for r in ok if not r["s"] and not r["v"] and r["h"]],
        "v_rule_used": {k: sum(1 for r in ok if r["v_rule"] == k)
                        for k in sorted({r["v_rule"] for r in ok}, key=lambda x: (x is None, x))},
        "sitemap_pagination": {
            "pages_requested": len(d["sitemap_pages_read"]),
            "identical_bytes_every_page": len({p.get("bytes") for p in d["sitemap_pages_read"]}) == 1,
            "urls_indexed": d["sitemap_urls_indexed"],
            "reading": "?page=N returned byte-identical content to page 1 on every request, so the "
                       "site serves one sitemap of this size and does not paginate it. The 39 extra "
                       "requests were wasted and are disclosed as an instrument defect (D1)."},
    }

    out = {
        "instrument": "as-of-today",
        "run_started_utc": d["run_started_utc"],
        "corpus_size": len(rows),
        "fetched_ok": len(ok),
        "netfail": [r["url"] for r in netfail],
        "predictions": preds,
        "unpredicted_observations": unpredicted,
    }
    with open("results.json", "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    print(f"run {d['run_started_utc']}  corpus {len(rows)}  ok {len(ok)}  netfail {len(netfail)}")
    for p in preds:
        print(f"  {p['id']} {p['verdict']:6} observed={p['observed']} ({p['n']})  rule {p['threshold']}")
    print(json.dumps(unpredicted, indent=1)[:1400])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
