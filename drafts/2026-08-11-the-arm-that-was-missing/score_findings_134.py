#!/usr/bin/env python3
"""Score `PREREGISTRATION-134.md`'s predictions against two blind classifiers' labels.

Session 134, 2026-08-24. Written WHILE THE CLASSIFIERS WERE STILL RUNNING and before either
label file existed, so the scoring rule could not be shaped by the labels it scores. The
pre-registration's P1-P4 and K1-K5 are transcribed here as code and nowhere improvised.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LABELS = ("A", "B", "C", "D", "E")


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return json.load(fh)


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def main():
    pop = load("findings-134.json")
    la = load("labels-134-A.json")["labels"]
    lb = load("labels-134-B.json")["labels"]
    recs = {r["id"]: r for r in pop["records"]}

    ids = sorted(recs)
    missing = {"A": [i for i in ids if i not in la], "B": [i for i in ids if i not in lb]}

    # ---- K1: raw agreement -------------------------------------------------
    both = [i for i in ids if i in la and i in lb]
    agree = [i for i in both if la[i]["label"] == lb[i]["label"]]
    raw_agreement = len(agree) / len(both) if both else 0.0
    k1_failed = raw_agreement < 0.60

    # ---- K3: E rate --------------------------------------------------------
    e_a = [i for i in both if la[i]["label"] == "E"]
    e_b = [i for i in both if lb[i]["label"] == "E"]
    e_either = sorted(set(e_a) | set(e_b))
    k3_failed = (len(e_either) / len(both)) > (1 / 3) if both else True

    # ---- the A set both classifiers agree on -------------------------------
    a_both = [i for i in both if la[i]["label"] == "A" and lb[i]["label"] == "A"]
    a_either = sorted({i for i in both if la[i]["label"] == "A" or lb[i]["label"] == "A"})

    # ---- K2: attribution ---------------------------------------------------
    attributed = [i for i in ids if recs[i]["role"] not in ("UNATTRIBUTED",)]
    k2_failed = len(attributed) < 20

    def roles_of(idlist):
        out = {}
        for i in idlist:
            out.setdefault(recs[i]["role"], []).append(i)
        return {k: sorted(v) for k, v in sorted(out.items())}

    a_both_roles = roles_of(a_both)
    a_either_roles = roles_of(a_either)

    # ---- P1: exclusivity claim --------------------------------------------
    non_panel_a = [i for i in a_both if recs[i]["role"] not in ("READER_PANEL", "UNATTRIBUTED")]
    p1_refuted = len(non_panel_a) > 0

    # ---- P3: interlocutor AND verifier ------------------------------------
    p3_int = [i for i in a_both if recs[i]["role"] == "INTERLOCUTOR"]
    p3_ver = [i for i in a_both if recs[i]["role"] == "VERIFIER"]
    p3_held = bool(p3_int) and bool(p3_ver)

    # ---- P2 and P4 need proportions, which K1/K3 may forbid ---------------
    proportions_allowed = not (k1_failed or k3_failed)
    p2 = p4 = None
    per_role = {}
    if proportions_allowed:
        classifiable = [i for i in both if la[i]["label"] != "E" and lb[i]["label"] != "E"]
        a_share = len([i for i in classifiable if i in a_both]) / len(classifiable) if classifiable else None
        p2 = {"a_share_agreed": a_share, "held": (a_share is not None and a_share < 0.25),
              "denominator": len(classifiable),
              "note": "numerator counts findings BOTH classifiers labelled A"}
        for role in sorted({recs[i]["role"] for i in classifiable}):
            n = [i for i in classifiable if recs[i]["role"] == role]
            k = [i for i in n if i in a_both]
            per_role[role] = {"n": len(n), "a": len(k),
                              "rate": (len(k) / len(n)) if n else None}
        rated = {r: v for r, v in per_role.items() if v["n"] >= 1}
        top = max(rated, key=lambda r: rated[r]["rate"]) if rated else None
        p4 = {"top_role_by_rate": top,
              "held": top == "READER_PANEL",
              "per_role": per_role,
              "fence": "K4: no significance test is run and none may be quoted; "
                       "the panel denominator is single digits."}

    result = {
        "generated_by": "score_findings_134.py",
        "preregistration": "PREREGISTRATION-134.md",
        "population": {"file": "findings-134.json", "n": pop["n_findings"],
                       "sha256_of_payload": sha(pop), "by_role": pop["by_role"]},
        "classifiers": {"A": {"n_labelled": len(la), "missing": missing["A"]},
                        "B": {"n_labelled": len(lb), "missing": missing["B"]}},
        "kill_conditions": {
            "K1_raw_agreement": {"value": raw_agreement, "threshold": 0.60,
                                 "failed": k1_failed, "n_compared": len(both)},
            "K2_attributed": {"value": len(attributed), "threshold": 20, "failed": k2_failed},
            "K3_e_rate": {"n_e_either": len(e_either), "of": len(both),
                          "threshold": "1/3", "failed": k3_failed, "ids": e_either},
            "K4": "no significance test computed anywhere in this script",
            "K5": "the disposition column was never read into the classifier input",
        },
        "proportions_reported": proportions_allowed,
        "A_set": {
            "agreed_by_both": {"n": len(a_both), "ids": a_both, "by_role": a_both_roles},
            "either_classifier": {"n": len(a_either), "ids": a_either, "by_role": a_either_roles},
        },
        "P1_exclusivity": {
            "claim": "POST-MORTEM.md S8: the severed-reader panel is the only instrument here "
                     "that has ever found that class of defect",
            "refuted": p1_refuted,
            "counterexamples_agreed_by_both": [
                {"id": i, "role": recs[i]["role"], "file": recs[i]["file"],
                 "line": recs[i]["line"], "row": recs[i]["row"],
                 "finding": recs[i]["finding"]} for i in non_panel_a],
        },
        "P3_both_roles": {"held": p3_held, "interlocutor": p3_int, "verifier": p3_ver},
        "P2_minority": p2,
        "P4_rate_residue": p4,
        "label_matrix": {
            a: {b: len([i for i in both if la[i]["label"] == a and lb[i]["label"] == b])
                for b in LABELS} for a in LABELS},
    }
    out = os.path.join(HERE, "score-134.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, ensure_ascii=False)

    print(f"population {pop['n_findings']}  compared {len(both)}")
    print(f"K1 raw agreement {raw_agreement:.4f}  failed={k1_failed}")
    print(f"K3 E either {len(e_either)}/{len(both)}  failed={k3_failed}")
    print(f"A agreed by both: {len(a_both)}   by either: {len(a_either)}")
    print(f"A by role (agreed): { {k: len(v) for k, v in a_both_roles.items()} }")
    print(f"P1 refuted: {p1_refuted}   ({len(non_panel_a)} non-panel A findings)")
    print(f"P3 held: {p3_held}   interlocutor={len(p3_int)} verifier={len(p3_ver)}")
    if p2:
        print(f"P2 A share {p2['a_share_agreed']:.4f} of {p2['denominator']} -> held={p2['held']}")
    if p4:
        print(f"P4 top role {p4['top_role_by_rate']} -> held={p4['held']}")
        for r, v in p4["per_role"].items():
            print(f"    {r:<16} {v['a']}/{v['n']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
