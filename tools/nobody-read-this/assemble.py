#!/usr/bin/env python3
"""Assemble session 166's data.json from the scored adjudications.

Adds the frozen-reference digests (K5), the pre-registered predictions with their verdicts
computed from the data rather than asserted, and the headline figures the page and the
summary must state. No model is called here.

Usage: assemble.py <scored.json> <items.json> <out.json>
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

FROZEN = [
    "artifacts/2026-09-19-the-second-hand/data/adjudication.json",
    "artifacts/2026-09-19-the-second-hand/data/verdicts.json",
    "artifacts/2026-09-20-the-same-text-twice/data/adjudication.json",
    "artifacts/2026-09-20-the-same-text-twice/data/violations.json",
    "artifacts/2026-09-20-the-same-text-twice/data/verdicts.json",
    "tools/is-it-a-licence/rules.py",
    "tools/is-it-a-licence/fingerprints.py",
]


def sha(p):
    return hashlib.sha256(open(os.path.join(ROOT, p), "rb").read()).hexdigest()


def main():
    scored = json.load(open(sys.argv[1]))
    items = json.load(open(sys.argv[2]))
    A, B = scored["arms"]["A"], scored["arms"]["B"]

    def rd(arm, tag):
        return arm[tag]

    out = dict(scored)
    out["k5_reference_digests"] = {p: sha(p) for p in FROZEN}

    a3, aall = rd(A, "K3"), rd(A, "ALL")
    b3, ball = rd(B, "K3"), rd(B, "ALL")

    preds = []

    def P(n, text, verdict, detail):
        preds.append({"n": n, "prediction": text, "verdict": verdict, "detail": detail})

    P(1, "Arm A: the majority of the four workers matches the committed verdict on at least "
         "8 of 11 cases.",
      "CONFIRMED" if aall["majority_matches_reference"] >= 8 else "REFUTED",
      f"{aall['majority_matches_reference']} of {aall['n_cases']} under the all-workers "
      f"reading; {a3['majority_matches_reference'] if a3 else None} of "
      f"{a3['n_cases'] if a3 else None} under K3.")

    acq = [r for r in aall["per_item"] if r["reference_label"] == "R-ship right"]
    P(2, "Arm A: on the 4 cases where this practice acquitted its own rule against four "
         "unanimous independent implementations, the majority sides with the shipped rule "
         "on at least 3 of 4.",
      "CONFIRMED" if sum(1 for r in acq if r["majority_matches_reference"]) >= 3 else "REFUTED",
      f"{sum(1 for r in acq if r['majority_matches_reference'])} of {len(acq)}.")

    P(3, "Arm B: the majority category matches the committed class label on at least 7 of "
         "10 classes.",
      "CONFIRMED" if ball["classes_majority_matches_reference"] >= 7 else "REFUTED",
      f"{ball['classes_majority_matches_reference']} of {ball['n_classes']} under the "
      f"all-workers reading; "
      f"{b3['classes_majority_matches_reference'] if b3 else None} of "
      f"{b3['n_classes'] if b3 else None} under K3.")

    c10 = ball["per_class"].get("10", {})
    all_mrfalse = (c10.get("per_worker") and
                   all(v == "MR-FALSE" for v in c10["per_worker"].values()))
    P(4, "Arm B: all four workers label class 10 - the 967 violations that were this "
         "practice's own bad test - as MR-FALSE.",
      "CONFIRMED" if all_mrfalse else "REFUTED",
      f"per-worker majorities on class 10: {c10.get('per_worker')}")

    convictions = aall["unanimous_against_reference"] + ball["unanimous_against_reference"]
    P(5, "At least one committed verdict or class label is contradicted by all four workers.",
      "CONFIRMED" if convictions else "REFUTED",
      f"unanimous-against-us items: {convictions or 'none'}")

    ka, kb = aall["fleiss_kappa_items"], ball["fleiss_kappa_items"]
    P(6, "Fleiss' kappa among the workers is at least 0.60 in both arms, computed on the "
         "non-sentinel items.",
      "CONFIRMED" if (ka is not None and kb is not None and ka >= 0.6 and kb >= 0.6)
      else "REFUTED",
      f"arm A kappa = {ka}, arm B kappa = {kb} (all-workers reading)")

    out["predictions"] = preds
    out["predictions_confirmed"] = sum(1 for p in preds if p["verdict"] == "CONFIRMED")
    out["predictions_refuted"] = sum(1 for p in preds if p["verdict"] == "REFUTED")

    out["cost"] = {
        "this_session": {
            "workers_dispatched": len(A["workers_dispatched"]) + len(B["workers_dispatched"]),
            "items_put_in_front_of_a_worker": A["n_items"] + B["n_items"],
            "judgements_collected": sum(len(v) for v in
                                        [A["coverage"], B["coverage"]] for v in v.values())
            if False else (sum(A["coverage"].values()) + sum(B["coverage"].values())),
            "arguments_this_practice_read_itself": None,
        },
        "2026-09-19": {"workers_dispatched": 4, "internal_disagreements": 127,
                       "unanimous_convictions": 11,
                       "arguments_this_practice_read_itself": 127},
        "2026-09-20": {"workers_dispatched": 0, "decision_changing_violations": 167,
                       "classes": 10, "arguments_this_practice_read_itself": 10},
    }

    out["headline"] = {
        "arm_A_majority_matches_of_11": aall["majority_matches_reference"],
        "arm_B_classes_matched_of_10": ball["classes_majority_matches_reference"],
        "convictions_of_our_reading": len(convictions),
        "workers_dispatched": len(A["workers_dispatched"]) + len(B["workers_dispatched"]),
        "judgements_collected": sum(A["coverage"].values()) + sum(B["coverage"].values()),
        "person_occurrences_in_the_two_artifacts": 14,
    }
    json.dump(out, open(sys.argv[3], "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"headline": out["headline"],
                      "predictions": [(p["n"], p["verdict"]) for p in preds]}, indent=1))


if __name__ == "__main__":
    main()
