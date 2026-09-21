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
      f"per-worker majorities on class 10: {c10.get('per_worker')}. Read on the workers "
      f"that delivered. The payload showed decision fields only, and class 10's decision "
      f"fields are identical before and after, so these items reached a worker as 'nothing "
      f"changed' - the same thing the arm's own sentinels showed. See the artifact.")

    convictions = aall["unanimous_against_reference"] + ball["unanimous_against_reference"]
    P(5, "At least one committed verdict or class label is contradicted by all four workers "
         "(read on the workers that delivered).",
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
            "arguments_this_practice_read_itself": 2,
            "what_this_practice_read_itself": "The one case the blind readers convicted us on, "
                                              "and the licence text behind it. Everything else "
                                              "was read by a dispatched worker.",
        },
        "2026-09-19": {"workers_dispatched": 4, "internal_disagreements": 127,
                       "unanimous_convictions": 11,
                       "arguments_this_practice_read_itself": 127},
        "2026-09-20": {"workers_dispatched": 0, "decision_changing_violations": 167,
                       "classes": 10, "arguments_this_practice_read_itself": 10},
    }

    out["workers"] = {
        "dispatched": 10,
        "delivered": len(A["workers_dispatched"]) + len(B["workers_dispatched"]),
        "arm_A": {"dispatched": 6, "delivered": len(A["workers_dispatched"]),
                  "note": "Four, then two replacements after K3 voided two of the first four."},
        "arm_B": {"dispatched": 4, "delivered": len(B["workers_dispatched"]),
                  "note": "One of the four returned no answer file within the session. "
                          "It is counted as dispatched and not delivered, and every arm-B "
                          "number below is over the three that delivered."},
    }
    out["headline"] = {
        "arm_A_majority_matches_of_11": aall["majority_matches_reference"],
        "arm_B_class_entries_matched_of_11": ball["classes_majority_matches_reference"],
        "arm_B_items_matched_of_45": aall and ball["majority_matches_reference"],
        "convictions_of_our_reading": len(convictions),
        "workers_delivered": len(A["workers_dispatched"]) + len(B["workers_dispatched"]),
        "judgements_collected": sum(A["coverage"].values()) + sum(B["coverage"].values()),
        "person_occurrences_in_the_two_artifacts": 14,
        "bad_tests_set_tonight": 3,
    }
    out["the_K3_selection_effect"] = {
        "what": "Arm B's K3 reading keeps only the two workers that passed the sentinels. "
                "Those are exactly the two that voted with this practice on the one class "
                "where the four split. So the K3 reading returns 44 of 45 items, 11 of 11 "
                "classes and Fleiss' kappa = 1.0.",
        "reading": "That kappa is manufactured by the kill condition, not found by the "
                   "experiment. A perfect agreement produced by discarding the workers who "
                   "disagreed is not evidence of anything, and it is reported here only so "
                   "that nobody can quote it without this sentence.",
        "which_number_this_artifact_stands_behind": "The all-workers reading: 38 of 45 items, "
                                                    "10 of 11 class entries, kappa 0.85.",
    }
    out["findings"] = {
        "defect_6": {
            "what": "A copyright notice whose holder sits on a later physical line than the "
                    "word `copyright` is read as `no_holder`. SPDX BSD-Inferno-Nettverk "
                    "carries its years over four lines and the holder on the fourth.",
            "quoted_line": "Inferno Nettverk A/S, Norway.  All rights reserved.",
            "how_it_was_found": "Item B49. All three arm-B workers that delivered called it "
                                "DEFECT against this practice's committed LATENT. The reading "
                                "was then checked first-hand against the licence text.",
            "what_it_convicts": "Not the rule alone - the 2026-09-20 adjudication. The "
                                "evidence was already in that session's data and this "
                                "practice read it as a latent risk rather than a present "
                                "error.",
            "does_it_move_a_published_number": "No, and this was checked rather than assumed. "
                                               "All five real licence files scored `no_holder` "
                                               "carry a bare year and no holder at all "
                                               "(`Copyright (c) 2025` and the like), so "
                                               "`no_holder` is right for every one of them. "
                                               "The defect is demonstrated on the canonical "
                                               "corpus only.",
            "not_found_by": ["100 fixtures", "27 mutations",
                             "four independent reimplementations (2026-09-19)",
                             "eight metamorphic relations (2026-09-20) - which DID reach the "
                             "input, and whose finding this practice then mislabelled"],
        },
        "bad_tests_set_tonight": [
            {"n": 8, "what": "K4, the leakage check: forbidden strings that the evidence "
                             "itself must contain. Caught before dispatch; Amendment 1."},
            {"n": 9, "what": "The arm-A sentinel: both candidate verdicts asserted the same "
                             "licence family and differed only on the holder question, so a "
                             "worker disputing the shared half could answer `neither` - which "
                             "the instructions expressly allowed. Three of six workers did, "
                             "and K3 voided all three."},
            {"n": 10, "what": "The arm-B payload and its sentinel: the payload showed decision "
                              "fields only, and both the sentinels and class 10 have "
                              "identical decision fields before and after. The control and "
                              "the live item reached every worker as the same item - "
                              "'nothing changed'. The consequence is exact and mechanical: "
                              "the two workers that passed all four sentinels are the two "
                              "that called class 10 MR-FALSE, and the two that missed all "
                              "four are the two that called class 10 UNDECIDED. Sentinel "
                              "performance predicts the class-10 vote perfectly, because "
                              "they are the same judgement. The sentinel had no "
                              "discriminating power at all, and K3 therefore selects the "
                              "workers who already agree with this practice."},
        ],
        "the_undecidable_case": {
            "item": "A10", "true_id": "InnoSetup",
            "our_label": "specification does not decide",
            "votes": "three workers for one verdict, three for the other, none for `neither`",
            "reading": "No worker reached this practice's answer, and the six split exactly "
                       "down the middle on it. A dead heat is not agreement with `undecided`, "
                       "and it is not disagreement either.",
        },
    }
    json.dump(out, open(sys.argv[3], "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"headline": out["headline"],
                      "predictions": [(p["n"], p["verdict"]) for p in preds]}, indent=1))


if __name__ == "__main__":
    main()
