#!/usr/bin/env python3
"""Emit `data.json` — every number the work's face shows — from the two results files.

No number on the published face is typed by hand. This script reads `results/audit.json` and
`results/history.json`, copies the values the face needs, and cross-checks the ones that appear
in both: if the single-state audit and the longitudinal pass ever disagree about the audited
state, this script fails instead of shipping a face that contradicts its own evidence.

Usage:
  python3 scripts/build_face.py            # write data.json
  python3 scripts/build_face.py --check    # recompute and fail if it differs
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIT = os.path.join(HERE, "results", "audit.json")
HISTORY = os.path.join(HERE, "results", "history.json")
OUT = os.path.join(HERE, "data.json")


def by_id(assertions):
    return {a["id"]: a for a in assertions}


def build():
    audit = json.load(open(AUDIT, encoding="utf-8"))
    hist = json.load(open(HISTORY, encoding="utf-8"))
    manifest = json.load(open(os.path.join(HERE, "sources", "history", "MANIFEST.json"),
                              encoding="utf-8"))
    A, H = by_id(audit["assertions"]), by_id(hist["assertions"])

    audited_short = "a7879398"
    audited = next(s for s in hist["states"] if s["commit_short"] == audited_short)

    # --- cross-checks: the two passes must agree about the state they share -------
    problems = []
    if audited["labels"]["field"] != A["A3"]["value"]:
        problems.append("A3 (%s) != longitudinal field label count (%s)"
                        % (A["A3"]["value"], audited["labels"]["field"]))
    if audited["forward_arm"]["pairs"] != audited["forward_arm"]["resolved_loose"]:
        problems.append("the audited state's forward arm no longer resolves completely")
    if A["A4"]["value"] != 0:
        problems.append("A4 residue is no longer 0")
    a12 = A["A12"]["value"]
    if audited["solo_by_citer"] != {k: {h: v.get(h, 0) for h in ("gebrauch", "praxis", "urteil")}
                                    for k, v in a12.items()}:
        problems.append("A12 and the longitudinal solo table disagree: %s vs %s"
                        % (a12, audited["solo_by_citer"]))
    sec = H["H2"]["value"]
    if manifest["audited_state_lifetime_human"] != "%dh%02dm" % (sec // 3600, (sec % 3600) // 60):
        problems.append("the manifest's human duration disagrees with H2's seconds — the exact "
                        "defect the gauntlet's Skeptic found in the first built state")
    if problems:
        raise SystemExit("REFUSING to build the face:\n  " + "\n  ".join(problems))

    return {
        "generated_from": {
            "audit": os.path.relpath(AUDIT, HERE),
            "history": os.path.relpath(HISTORY, HERE),
            "note": "Every number on the face comes from these two files. This build fails if "
                    "they contradict each other about the state they share.",
        },
        "repository_pin": hist["repository_pin"],
        "late_repository_pin": "f21f275",
        "audited_state": audited_short,
        "states": [
            {
                "short": s["commit_short"],
                "at": s["committed_at"],
                "subject": s["subject"],
                "entries": s["entries"],
                "labels": s["labels"],
                "shared": s["shared_entries"],
                "solo": s["solo_by_citer"],
                "urteil_key": s["urteil_key_present"],
                "urteil_pop": s["urteil_populated"],
                "pairs": s["forward_arm"]["pairs"],
                "pairs_into_own_freeze": s["forward_arm"]["pairs_into_own_freeze"],
                "files": s["forward_arm"]["distinct_files"],
                "loose": s["forward_arm"]["resolved_loose"],
                "strict": s["forward_arm"]["resolved_strict"],
                "missing_at_pin": len(s["forward_arm"]["unresolved_file_not_at_repo_pin"]),
                "wrong_identifier": len(s["forward_arm"]["unresolved_identifier_not_in_file"]),
            }
            for s in hist["states"]
        ],
        "loop": H["H7"]["value"] | {"entries_on_that_evidence": H["H8"]["value"]},
        "discrimination": H["H9"]["value"],
        "invariant_holds": H["H6"]["value"],
        "audited_state_lifetime_seconds": H["H2"]["value"],
        "audited_state_lifetime_human": manifest["audited_state_lifetime_human"],
        "audit_engagement_window_human": manifest["audit_engagement_window_human"],
        "audit_fetched": manifest["audit_fetched"],
        "sieve": audit["sieve"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    text = json.dumps(build(), ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    if args.check:
        if not os.path.exists(OUT) or open(OUT, encoding="utf-8").read() != text:
            print("FAIL: data.json differs from a fresh build")
            return 1
        print("OK: data.json is byte-identical to a fresh build")
        return 0
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("wrote %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
