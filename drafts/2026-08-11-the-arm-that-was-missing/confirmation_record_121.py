#!/usr/bin/env python3
"""confirmation_record_121 — what this arc actually knows about single readings.

Session 121, 2026-08-15. Built to answer the condition that stopped the ship
(`CONDITIONS-120.md`, I3): the bundle offered the reproducibility of an aggregate rate on a
fixed panel as the warrant for trusting a *single reading* of somebody else's list, and this
arc's own confirmation step refutes that warrant. The number was quoted three times today from
three different places and never computed in one.

So it is computed here, from the raw sidecars only, and nothing about it is typed by hand.

WHAT IT READS
    ledger/transition-confirm-*.json   the K4 sidecars: five immediate re-requests per
                                       transition, at the instrument's own 1.0 s spacing
    ledger/corrections.json            the session-119 overlay: which run-file readings the
                                       confirmation step has already refuted

THE ONE JUDGEMENT IT MAKES, AND IT IS MECHANICAL. A confirmed `NOT-RETRIEVABLE`->`RETRIEVABLE`
reading is an **artefact echo** — not a genuine transition — when the absence it reverses is
itself a reading the overlay corrects. That is the defect session 119 built the overlay for:
the confirmation step refuted a reading, the run file kept it, and the next day's diff read the
uncorrected file and reported our own refuted reading coming back as a fresh event. An echo is
counted separately rather than dropped, because both counts are true of different questions:
raw readings answer "how often does a re-request agree with a first pass", genuine transitions
answer "how often is a change real".

Usage:  python3 confirmation_record_121.py [-o confirmation-record-121.json]
Offline. Reads committed files only, makes no request.
"""
import argparse
import glob
import hashlib
import json
import sys

SIDECARS = "ledger/transition-confirm-*.json"
CORRECTIONS = "ledger/corrections.json"


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build(sidecar_glob=SIDECARS, corrections_path=CORRECTIONS):
    corr = json.load(open(corrections_path))
    # An identifier+run_file pair the overlay corrects. The absence it corrects is the one a
    # later "return" would be echoing.
    corrected_vids = {c["vid"] for c in corr["corrections"]
                      if c["state_in_run_file"] == "NOT-RETRIEVABLE"
                      and c["corrected_state"] == "RETRIEVABLE"}

    readings = []
    for path in sorted(glob.glob(sidecar_glob)):
        d = json.load(open(path))
        for r in d.get("results", []):
            direction = f'{r["from"]}->{r["to"]}'
            confirmed = bool(r["all_passes_agree_with_new_state"])
            echo = (direction == "NOT-RETRIEVABLE->RETRIEVABLE"
                    and r["vid"] in corrected_vids)
            readings.append({
                "sidecar": path,
                "sidecar_sha256": sha256(path),
                "generated_utc": d.get("generated_utc"),
                "vid": r["vid"],
                "handle": r["handle"],
                "direction": direction,
                "passes": r["reconfirmation_states"],
                "n_passes": len(r["reconfirmation_states"]),
                "confirmed": confirmed,
                "artefact_echo": echo,
                "echo_note": ("this return reverses an absence the session-119 overlay corrects: "
                              "the absence itself failed five re-requests, so the return is the "
                              "arc's own refuted reading coming back, not a platform event"
                              if echo else None),
            })

    def tally(rows):
        out = {}
        for d in ("NOT-RETRIEVABLE->RETRIEVABLE", "RETRIEVABLE->NOT-RETRIEVABLE"):
            sel = [r for r in rows if r["direction"] == d]
            out[d] = {"n": len(sel),
                      "confirmed": sum(1 for r in sel if r["confirmed"]),
                      "refuted": sum(1 for r in sel if not r["confirmed"])}
        return out

    genuine = [r for r in readings if not r["artefact_echo"]]
    return {
        "schema": "field-research/confirmation-record/1",
        "built_by": "confirmation_record_121.py, session 121",
        "sources": {"sidecars": sorted(glob.glob(sidecar_glob)),
                    "corrections": corrections_path,
                    "corrections_sha256": sha256(corrections_path)},
        "passes_per_reading": 5,
        "what_a_pass_is": ("one further request to the same endpoint for the same identifier, "
                           "at the instrument's own 1.0 s spacing, immediately after the reading "
                           "being tested. A reading is CONFIRMED only if all five agree with it."),
        "all_readings": tally(readings),
        "genuine_transitions_only": tally(genuine),
        "n_artefact_echoes": sum(1 for r in readings if r["artefact_echo"]),
        "readings": readings,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("-o", "--out", default="confirmation-record-121.json")
    a = ap.parse_args(argv)
    rec = build()
    json.dump(rec, open(a.out, "w"), indent=1)
    print(f"{len(rec['readings'])} confirmation readings across "
          f"{len(rec['sources']['sidecars'])} sidecars; "
          f"{rec['n_artefact_echoes']} artefact echo(es)")
    for label in ("all_readings", "genuine_transitions_only"):
        print(f"  {label}:")
        for d, t in rec[label].items():
            print(f"    {d:<34} n={t['n']}  confirmed={t['confirmed']}  refuted={t['refuted']}")
    print("written", a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
