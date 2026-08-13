#!/usr/bin/env python3
"""Scoring the session-115 predictions against the day-3 run.

Written and committed **before the day-3 run finished**, so the scoring rule cannot be adjusted
to the answer. `PREREGISTRATION-115.md` §3 fixes P1–P7; P1–P5 are scored here from the run files,
P6 and P7 were scored by `restatement_115.py` / `restatement_115b.py` before any of this ran.

Usage: python3 score_115.py <day3-run.json> <diff-day2-day3.json>
"""
import json
import sys

DAY2 = "ledger/run-2026-08-12T0341Z.json"
GRIMHOUND = "grimhoundgaming"
RETURNED = "7446448990935354670"        # iidahmer, the interval-1 return


def states(run):
    return {o["vid"]: o for o in run["observations"]}


def main(day3_path, diff_path):
    d2 = json.load(open(DAY2))
    d3 = json.load(open(day3_path))
    diff = json.load(open(diff_path))
    s2, s3 = states(d2), states(d3)

    out = {"session": 115, "day3_run": day3_path, "diff": diff_path,
           "day3_vantage_asn": d3["vantage"]["asn"],
           "day3_requested": d3["requested"], "day3_planned": d3["planned"],
           "day3_stopped": d3["stopped"], "day3_counts": d3["counts"]}

    # ---- K1 / K2: is the day scorable at all? -------------------------------------------
    unmeasured = d3["planned"] - d3["requested"]
    out["K1"] = ("DOES NOT FIRE — complete run"
                 if unmeasured <= 0.10 * d3["planned"] else
                 f"FIRES — {unmeasured} of {d3['planned']} unmeasured; the day is dark, "
                 "interval 2 is not scored")
    out["K2"] = ("DOES NOT FIRE — same autonomous system as days 1 and 2"
                 if d3["vantage"]["asn"] == "AS396982" else
                 f"FIRES — vantage moved to {d3['vantage']['asn']}; the run is flagged and not "
                 "diffed")

    # ---- P1: transitions in interval 2, grimhoundgaming counted separately ---------------
    trans = diff["transitions"]
    grim_vids = {v for v, o in s2.items() if (o.get("handle") or "").lower() == GRIMHOUND}
    other = [t for t in trans if t["vid"] not in grim_vids]
    grim_trans = [t for t in trans if t["vid"] in grim_vids]
    out["P1"] = {"prediction": "0, 1 or 2 confirmed transitions, grimhoundgaming excluded",
                 "transitions_total": len(trans),
                 "transitions_excluding_grimhoundgaming": len(other),
                 "transitions_in_grimhoundgaming": len(grim_trans),
                 "detail": other,
                 "verdict": "HOLDS" if len(other) <= 2 else "FAILS"}

    # ---- P2: grimhoundgaming, and K5's three-way rule ------------------------------------
    rows = []
    for v in sorted(grim_vids):
        rows.append({"vid": v, "day2": s2[v]["state"],
                     "day3": s3[v]["state"] if v in s3 else "NOT MEASURED",
                     "day3_http": s3[v].get("http") if v in s3 else None})
    turned = sum(1 for r in rows if r["day2"] == "RETRIEVABLE"
                 and r["day3"] == "NOT-RETRIEVABLE")
    absent3 = sum(1 for r in rows if r["day3"] == "NOT-RETRIEVABLE")
    n = len(rows)
    if absent3 == n:
        p2 = "HOLDS — all seven not retrievable; account death propagated within one day"
        k5 = "P2 CONFIRMED"
    elif absent3 == sum(1 for r in rows if r["day2"] == "NOT-RETRIEVABLE"):
        p2 = "FAILS — nothing turned; the two interfaces disagree"
        k5 = ("K5: 0 of 7 turned — propagation within one day is REFUTED, and the disagreement "
              "between the account route and the video route is the finding")
    else:
        p2 = f"FAILS — {absent3} of {n} not retrievable, not all seven"
        k5 = ("K5: partial — recorded as NOT ESTABLISHED; the mechanism claim is not made in "
              "either direction")
    out["P2"] = {"prediction": "all 7 grimhoundgaming videos NOT-RETRIEVABLE on day 3",
                 "account_state_at_2026-08-12T~23:45Z": "status field 10221, no userInfo served",
                 "videos": rows, "turned_this_interval": turned,
                 "not_retrievable_on_day3": absent3, "n": n,
                 "verdict": p2, "K5": k5}

    # ---- P3: does the interval-1 return persist? ----------------------------------------
    r2 = s2.get(RETURNED, {}).get("state")
    r3 = s3.get(RETURNED, {}).get("state")
    out["P3"] = {"prediction": f"{RETURNED} still RETRIEVABLE on day 3",
                 "day2": r2, "day3": r3,
                 "verdict": "HOLDS" if r3 == "RETRIEVABLE" else f"FAILS — day 3 is {r3}"}

    # ---- P4: the pooled determinate rate -------------------------------------------------
    def rate(run):
        c = {}
        for o in run["observations"]:
            c[o["state"]] = c.get(o["state"], 0) + 1
        det = c.get("RETRIEVABLE", 0) + c.get("NOT-RETRIEVABLE", 0)
        return 100 * c.get("RETRIEVABLE", 0) / det, det, c
    r2p, det2, c2 = rate(d2)
    r3p, det3, c3 = rate(d3)
    out["P4"] = {"prediction": "day-3 pooled determinate retrievability within +-0.40 pp of 82.1624",
                 "day2_pct": round(r2p, 4), "day2_determinate": det2,
                 "day3_pct": round(r3p, 4), "day3_determinate": det3,
                 "delta_pp": round(r3p - r2p, 4),
                 "verdict": "HOLDS" if abs(r3p - r2p) <= 0.40 else "FAILS"}

    # ---- P5: does indeterminacy churn? ---------------------------------------------------
    ind2 = {v for v, o in s2.items() if o["state"] == "INDETERMINATE"}
    ind3 = {v for v, o in s3.items() if o["state"] == "INDETERMINATE"}
    overlap = len(ind2 & ind3)
    in_range = 15 <= len(ind3) <= 70
    churned = overlap < len(ind2) / 2
    out["P5"] = {"prediction": "day-3 INDETERMINATE in 15-70, and fewer than half of day 2's 40 "
                               "identifiers indeterminate again",
                 "day2_indeterminate": len(ind2), "day3_indeterminate": len(ind3),
                 "same_identifiers": overlap,
                 "verdict": ("HOLDS" if in_range and churned else
                             "FAILS" if not in_range and not churned else
                             "PART-HOLDS — " + ("count in range, " if in_range else
                                                "count out of range, ")
                             + ("churned" if churned else "did not churn"))}

    json.dump(out, open("score-115.json", "w"), indent=1, ensure_ascii=False)
    for k in ("K1", "K2"):
        print(f"{k}: {out[k]}")
    for k in ("P1", "P2", "P3", "P4", "P5"):
        print(f"{k}: {out[k]['verdict']}")
    print(json.dumps({"P2_videos": out["P2"]["videos"], "P2_K5": out["P2"]["K5"],
                      "P4": {x: out["P4"][x] for x in ("day2_pct", "day3_pct", "delta_pp")},
                      "P5": {x: out["P5"][x] for x in ("day2_indeterminate",
                                                       "day3_indeterminate",
                                                       "same_identifiers")}},
                     indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
