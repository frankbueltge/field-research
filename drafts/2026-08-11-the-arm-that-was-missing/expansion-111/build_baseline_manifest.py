#!/usr/bin/env python3
"""Manifest for the session-111 baseline run of the expanded corpus.

Two new arms, both credential-free, both collected tonight:

* **A-new** — language editions of the same encyclopedia that session 109 did not query.
  Article space, same instrument, same query. Volume only; no new design property.
* **A2** — the SAME wikis session 109 used, outside article space (talk, user, project,
  draft, template, category, portal). Same operator and editors, **no link-maintenance
  regime**. This is the control the pruning confound named in `PREREGISTRATION-111.md` §4
  has been missing, and it is why the expansion went here rather than wherever identifiers
  were cheapest.

Identifiers already under observation in the session-110 run are excluded: adding an
identifier twice would inflate the corpus without adding exposure.

The manifest is CAPPED by wall-clock so the baseline lands before 00:00Z on 2026-08-12 —
the instant after which a new identifier can no longer carry the same six intervals as the
rest of the corpus. The cap is a stated rule with its arithmetic printed, never a silent
truncation: identifiers are ordered by a seeded shuffle so the kept set is not the
alphabetically or chronologically lucky one.
"""
import json
import os
import random
import sys
import time

SEED = 20260811_111
SEC_PER_REQUEST = 1.80   # measured: session 110 ran 2,904 requests in 5,127.8 s


def main(deadline_utc_hhmm, out="expansion-111/manifest-baseline-111.json"):
    led = json.load(open("ledger/run-2026-08-11T1124Z.json"))
    already = {str(o["vid"]) for o in led["observations"]}

    units, sources = {}, {}

    p = "expansion-111/new-editions.json"
    if os.path.exists(p):
        d = json.load(open(p))
        for r in d["rows"]:
            if str(r["vid"]) not in already:
                units.setdefault(str(r["vid"]),
                                 {"vid": str(r["vid"]), "handle": r["handle"], "arm": "A-new"})
        sources["A-new"] = d["meta"]

    p = "expansion-111/corpus-A2-namespaces.json"
    if os.path.exists(p):
        d = json.load(open(p))
        for r in d["rows"]:
            v = str(r["vid"])
            if v not in already and v not in units:
                units.setdefault(v, {"vid": v, "handle": r["handle"], "arm": "A2"})
        sources["A2"] = {k: v for k, v in d["meta"].items() if k != "log"}
        sources["A2"]["log_entries"] = len(d["meta"].get("log", []))

    all_units = list(units.values())
    random.Random(SEED).shuffle(all_units)

    # --- the wall-clock cap, computed and printed rather than guessed
    hh, mm = int(deadline_utc_hhmm[:2]), int(deadline_utc_hhmm[2:])
    now = time.gmtime()
    deadline = time.time() + ((hh - now.tm_hour) * 3600 + (mm - now.tm_min) * 60
                              - now.tm_sec)
    budget_s = max(0.0, deadline - time.time())
    cap = int(budget_s / SEC_PER_REQUEST)
    kept = all_units[:cap]
    dropped = len(all_units) - len(kept)

    manifest = {
        "run_id": time.strftime("%Y-%m-%dT%H%MZ", time.gmtime()),
        "purpose": "session 111 baseline of the expanded corpus, before day 2 opens",
        "seed": SEED,
        "cap": {"deadline_utc": f"{deadline_utc_hhmm[:2]}:{deadline_utc_hhmm[2:]}Z",
                "budget_seconds": round(budget_s, 1),
                "seconds_per_request_assumed": SEC_PER_REQUEST,
                "cap_units": cap, "collected": len(all_units),
                "kept": len(kept), "dropped_by_cap": dropped,
                "selection": "seeded shuffle, then first `cap` — not the alphabetically "
                             "or chronologically lucky ones",
                "note": "dropped identifiers are kept in the collected corpus files and "
                        "may enter a later run; they simply cannot carry this window's "
                        "six intervals"},
        "arms": sources,
        "units": kept,
    }
    json.dump(manifest, open(out, "w"), indent=1)
    by_arm = {}
    for u in kept:
        by_arm[u["arm"]] = by_arm.get(u["arm"], 0) + 1
    print(json.dumps({"collected_new": len(all_units), "kept": len(kept),
                      "dropped_by_cap": dropped, "by_arm": by_arm,
                      "budget_s": round(budget_s, 1), "cap": cap}))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "2350")
