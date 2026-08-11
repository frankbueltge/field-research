#!/usr/bin/env python3
"""Manifest for the SECOND baseline run of session 111 — the round-2 identifiers.

Round 1 collected from three wikis before its budget ran out; round 2 went to the eighteen
wikis it never reached and to the twenty-nine editions round 1 lost to HTTP 429. Those
identifiers are collected but unmeasured, and an unmeasured identifier carries no baseline —
so it carries no exposure in the pre-registered window either.

Excludes everything already under observation: session 110's run, and the round-1 baseline
this session already measured. Capped by wall clock on the same rule and the same measured
1.80 s per request, so the run lands before 00:00Z; the cap's arithmetic is written into the
manifest and the dropped identifiers stay in the collection file rather than vanishing.
"""
import json
import os
import random
import sys
import time

SEED = 20260811_1112
SEC_PER_REQUEST = 1.85   # measured on this session's own round-1 run: 100 units in 185 s


def main(deadline_utc_hhmm, out="expansion-111/manifest-baseline2-111.json"):
    already = {str(o["vid"]) for o in
               json.load(open("ledger/run-2026-08-11T1124Z.json"))["observations"]}
    if os.path.exists("expansion-111/baseline-run.json"):
        already |= {str(o["vid"]) for o in
                    json.load(open("expansion-111/baseline-run.json"))["observations"]}

    d = json.load(open("expansion-111/corpus-round2.json"))
    units = {}
    for r in d["rows"]:
        v = str(r["vid"])
        if v not in already:
            units[v] = {"vid": v, "handle": r["handle"],
                        "arm": "A2" if r.get("ns") else "A-new"}

    all_units = list(units.values())
    random.Random(SEED).shuffle(all_units)

    hh, mm = int(deadline_utc_hhmm[:2]), int(deadline_utc_hhmm[2:])
    now = time.gmtime()
    budget_s = max(0.0, (hh - now.tm_hour) * 3600 + (mm - now.tm_min) * 60 - now.tm_sec)
    cap = int(budget_s / SEC_PER_REQUEST)
    kept = all_units[:cap]

    man = {
        "run_id": time.strftime("%Y-%m-%dT%H%MZ", time.gmtime()),
        "purpose": "session 111 SECOND baseline — the round-2 identifiers, before day 2 opens",
        "seed": SEED,
        "cap": {"deadline_utc": f"{deadline_utc_hhmm[:2]}:{deadline_utc_hhmm[2:]}Z",
                "budget_seconds": round(budget_s, 1),
                "seconds_per_request_assumed": SEC_PER_REQUEST,
                "cap_units": cap, "collected_new": len(all_units),
                "kept": len(kept), "dropped_by_cap": len(all_units) - len(kept),
                "selection": "seeded shuffle, then first `cap`",
                "note": "dropped identifiers remain in expansion-111/corpus-round2.json and "
                        "may open a separately dated arm in a later session; they cannot "
                        "carry this window's intervals"},
        "arms": {"round2": {k: v for k, v in d["meta"].items() if k != "log"}},
        "units": kept,
    }
    json.dump(man, open(out, "w"), indent=1)
    by_arm = {}
    for u in kept:
        by_arm[u["arm"]] = by_arm.get(u["arm"], 0) + 1
    print(json.dumps({"collected_new": len(all_units), "kept": len(kept),
                      "dropped_by_cap": len(all_units) - len(kept),
                      "by_arm": by_arm, "budget_s": round(budget_s, 1), "cap": cap}))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "2348")
