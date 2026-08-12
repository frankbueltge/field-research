#!/usr/bin/env python3
"""K4 — an unreproduced transition is not an event.

`PREREGISTRATION-112.md` §4: *fires on any transition that does not survive an immediate
re-request. It is then recorded as an instrument artefact with its raw bodies, and not counted in
the window.* This is the script that applies it, and it keeps **every raw body** rather than a
classification, because the whole point of the criterion is that the classifier is what is on
trial.

Five re-requests, one per identifier per pass, at the instrument's own 1.0 s spacing. Five rather
than one because a single confirmation cannot distinguish a stable new state from a coin flip:
session 109's three-arm control showed the platform's 400 is semantically empty, and an endpoint
that answers differently to identical requests is a hypothesis this arc has never tested on a
transition (it had none to test).

The probe is `ledger.py`'s, imported and not re-implemented.
"""
import importlib.util
import json
import sys
import time

spec = importlib.util.spec_from_file_location("ledger", "ledger.py")
ledger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)

PASSES = 5


def main(diff_path, out_path):
    diff = json.load(open(diff_path))
    trans = diff.get("transitions") or []
    if not trans:
        json.dump({"K4": "VACUOUS — no transitions to confirm; recorded as vacuous, not as passed",
                   "n_transitions": 0}, open(out_path, "w"), indent=1)
        print("K4 VACUOUS — nothing to confirm")
        return 0

    van = ledger.vantage()
    results = []
    for t in trans:
        passes = []
        for i in range(PASSES):
            rec = ledger.probe_one(t["vid"], t["handle"])
            rec["state"] = ledger.classify(rec)
            rec["pass"] = i + 1
            rec["utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            passes.append(rec)
            time.sleep(ledger.DELAY)
        states = [p["state"] for p in passes]
        agreed = all(s == t["to"] for s in states)
        results.append({
            "vid": t["vid"], "handle": t["handle"], "arm": None,
            "from": t["from"], "to": t["to"],
            "reconfirmation_states": states,
            "all_passes_agree_with_new_state": agreed,
            "verdict": ("CONFIRMED — the new state survives five immediate re-requests"
                        if agreed else
                        "NOT CONFIRMED — K4 fires; recorded as an instrument artefact, "
                        "not counted in the window"),
            "passes": passes,
        })

    out = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "diff": diff_path, "vantage": van, "passes_per_transition": PASSES,
           "K4": ("PASSES — every transition confirmed" if all(r["all_passes_agree_with_new_state"]
                                                               for r in results)
                  else "FIRES — at least one transition did not reproduce"),
           "results": results}
    json.dump(out, open(out_path, "w"), indent=1)
    print(json.dumps({"K4": out["K4"],
                      "results": [{k: v for k, v in r.items() if k != "passes"}
                                  for r in results]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
