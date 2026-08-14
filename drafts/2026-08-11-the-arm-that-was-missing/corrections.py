#!/usr/bin/env python3
"""The correction overlay — how a refuted reading stops coming back as data.

Session 119, DEVIATION D23. **BOOKKEEPING ONLY: no request of any probe changes, and no
archived measurement record is edited.** The probe, the endpoint, the user agent, the 1.0 s
delay, the 25 s timeout, the classification and the order are untouched, which is the only
reason days 1–7 stay comparable.

THE DEFECT, found by hand at session 118 and made into a standing check by `audit_instrument.py`
A8: `confirm_transition.py` writes its verdict to a sidecar and never touches the ledger. A
reading it refutes therefore stays in the run file — and the next interval, diffed against that
file, reports the reversal of **our own refuted reading** as a fresh transition. It happened:
`arutz_7`'s day-3 absence failed all five re-requests at session 115, and session 118's diff
read the uncorrected file and reported a return.

THE RULE THIS ARC HAS ALREADY WRITTEN, WHICH THE FIX MUST NOT BREAK (D22, session 117):

    a measurement record is not corrected by rewriting it.

So the correction does not go into the run file. It travels beside it, dated, with its
authority named — the sidecar that refuted the reading — and with the five re-request states
that are the evidence. Every consumer that applies the overlay says so in its own output, so a
corrected number can never be mistaken for a raw one. Nothing is silent.

WHAT IS AND IS NOT A CORRECTION. Only a transition the confirmation step refuted, i.e. K4 fired
on it: five immediate re-requests all disagreed with the new state. The corrected value is the
state those five re-requests support, and it is never chosen by us. A reading nobody re-requested
is not corrected — an unchecked state stays exactly as measured.

Usage:
    python3 corrections.py build      # rebuild ledger/corrections.json from the sidecars
    python3 corrections.py show
"""
import glob
import json
import sys
import time

OUT = "ledger/corrections.json"
CONFIRM_GLOB = "ledger/transition-confirm-*.json"
SCHEMA = "field-research/ledger-corrections/1"

POLICY = (
    "An overlay, never an edit. Each row says: this run file carries this state for this "
    "identifier, the confirmation step of this arc refuted it with five immediate re-requests "
    "that all said otherwise, and the state those re-requests support is the one a consumer "
    "should read. The run file is unchanged and stays the record of what the instrument "
    "actually returned. Any consumer applying this overlay must report that it did, and which "
    "rows it used — see ledger_diff.py --corrections."
)


def build():
    rows = []
    for p in sorted(glob.glob(CONFIRM_GLOB)):
        d = json.load(open(p))
        diff_path = d.get("diff")
        try:
            run_file = json.load(open(diff_path))["run2"]["path"]
        except Exception:
            run_file = None
        for r in d.get("results", []):
            if r.get("all_passes_agree_with_new_state"):
                continue
            states = r["reconfirmation_states"]
            supported = max(set(states), key=states.count)
            if len(set(states)) != 1:
                # not a clean refutation: five re-requests that disagree among themselves are
                # a finding about the endpoint, not an authority to correct anything
                rows.append({"vid": r["vid"], "handle": r.get("handle"),
                             "run_file": run_file, "corrected_state": None,
                             "status": "NOT CORRECTED — the five re-requests disagree among "
                                       "themselves; recorded, not resolved",
                             "evidence_five_re_requests": states, "authority": p})
                continue
            rows.append({
                "vid": r["vid"], "handle": r.get("handle"),
                "run_file": run_file,
                "state_in_run_file": r["to"],
                "corrected_state": supported,
                "status": "CORRECTED",
                "reason": ("K4 fired: the transition reported by the diff did not survive five "
                           "immediate re-requests, so the run file's state is an instrument "
                           "artefact and the arc has already ruled it out of the window"),
                "evidence_five_re_requests": states,
                "authority": p,
                "authority_generated_utc": d.get("generated_utc"),
                "diff_that_reported_it": diff_path,
            })
    payload = {"schema": SCHEMA, "recorded_by_session": 119,
               "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "deviation": "D23 — bookkeeping only; no probe and no archived run file changes",
               "policy": POLICY,
               "n_corrections": sum(1 for r in rows if r.get("corrected_state")),
               "corrections": rows}
    json.dump(payload, open(OUT, "w"), indent=1)
    print(json.dumps({"n_corrections": payload["n_corrections"],
                      "rows": [{k: r[k] for k in ("vid", "handle", "run_file",
                                                  "corrected_state", "status") if k in r}
                               for r in rows]}, indent=1))
    print("wrote", OUT)


def load(path=OUT):
    """(run_file, vid) -> row, for the rows that actually carry a correction.

    Session 119, after the gauntlet: the first version was a dict comprehension, so two sidecars
    correcting the same (run file, identifier) would have silently kept the last one. Unexercised
    today — the two rows are distinct — and it is exactly the class of silent-last-wins bug this
    arc fixed in `cluster_keys.page_index()` at session 117. A collision now raises.
    """
    try:
        d = json.load(open(path))
    except FileNotFoundError:
        return {}
    out = {}
    for r in d["corrections"]:
        if not r.get("corrected_state"):
            continue
        k = (r["run_file"], r["vid"])
        if k in out and out[k]["corrected_state"] != r["corrected_state"]:
            raise ValueError(f"two sidecars disagree about {k}: "
                             f'{out[k]["corrected_state"]} vs {r["corrected_state"]} — '
                             f"resolve it in the record, not by taking the last one")
        out[k] = r
    return out


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "build":
        build()
    elif cmd == "show":
        print(json.dumps(json.load(open(OUT)), indent=1))
    else:
        print(__doc__)
        sys.exit(2)
