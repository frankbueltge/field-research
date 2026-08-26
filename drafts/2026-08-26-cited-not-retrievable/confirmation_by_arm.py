#!/usr/bin/env python3
"""confirmation_by_arm - the confirmation record split by the arm the identifier belongs to.

Session 136, 2026-08-26. Written because the Verifier found that this session published a
confirmation count over ALL arms as the last row of a table whose every other row is scoped to the
encyclopedia arms (`VERIFIER-136.md`, finding 7). The figure quoted its source faithfully; the
table it sat in did not have that population.

THE PRACTICE'S OWN RULE APPLIES TO ITS OWN REVIEWER. `POST-MORTEM.md` §3 records refusing to adopt
an adversary's handed-over numbers on trust as one of three things that worked, and the refusal paid
once. The Verifier reported 5 of 15 and 9 of 9 for the encyclopedia arms. This script computes them
here rather than typing them, so the correction is this practice's own computation and the reviewer's
figure is a check on it and not its source.

WHAT IT READS
    ../2026-08-11-the-arm-that-was-missing/confirmation-record-121.json   the 28 readings
    ../2026-08-11-the-arm-that-was-missing/ledger/run-2026-08-25T0341Z.json  vid -> arm

A reading's arm is the arm of its identifier in the manifest the run file records. An identifier
that appears in no run file is reported separately rather than dropped.

Usage:  python3 confirmation_by_arm.py [-o out.json]
Offline. Reads committed files only, makes no request.
"""
import argparse
import collections
import hashlib
import json
import os

ARC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "2026-08-11-the-arm-that-was-missing")
WIKI_ARMS = ("A", "A-new", "A2")


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build():
    rec_path = os.path.join(ARC, "confirmation-record-121.json")
    run_path = os.path.join(ARC, "ledger", "run-2026-08-25T0341Z.json")
    rec = json.load(open(rec_path))
    arms = {o["vid"]: o["arm"] for o in json.load(open(run_path))["observations"]}

    buckets = collections.defaultdict(lambda: collections.Counter())
    unknown = []
    for r in rec["readings"]:
        arm = arms.get(r["vid"])
        if arm is None:
            unknown.append(r["vid"])
            continue
        scope = "encyclopedia" if arm in WIKI_ARMS else "other_arms"
        key = (scope, r["direction"], bool(r.get("artefact_echo")))
        buckets[key]["n"] += 1
        buckets[key]["confirmed" if r.get("confirmed") else "refuted"] += 1

    out = {
        "schema": "field-research/confirmation-by-arm/1",
        "built_by": "confirmation_by_arm.py, session 136, 2026-08-26",
        "offline": True,
        "sources": {"confirmation_record": os.path.basename(rec_path),
                    "confirmation_record_sha256": sha256(rec_path),
                    "run_file_for_arms": os.path.basename(run_path),
                    "run_file_sha256": sha256(run_path)},
        "encyclopedia_arms": list(WIKI_ARMS),
        "n_readings_total": len(rec["readings"]),
        "identifiers_not_in_the_run_file": unknown,
        "what_this_is_not": "These are RAW readings unless the row says echoes are excluded. A "
                            "confirmation count travels with the word raw or genuine or it does not "
                            "travel (memory/downstream-commitments.md condition 8). And in either "
                            "form six events is not a rate, and neither are fifteen.",
        "counts": {},
    }
    for scope in ("encyclopedia", "other_arms"):
        block = {}
        for direction in ("NOT-RETRIEVABLE->RETRIEVABLE", "RETRIEVABLE->NOT-RETRIEVABLE"):
            raw = collections.Counter()
            genuine = collections.Counter()
            for echo in (False, True):
                c = buckets.get((scope, direction, echo))
                if not c:
                    continue
                raw.update(c)
                if not echo:
                    genuine.update(c)
            block[direction] = {
                "raw": {"n": raw["n"], "confirmed": raw["confirmed"], "refuted": raw["refuted"]},
                "genuine": {"n": genuine["n"], "confirmed": genuine["confirmed"],
                            "refuted": genuine["refuted"]},
                "artefact_echoes_excluded_from_genuine": raw["n"] - genuine["n"],
            }
        out["counts"][scope] = block
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    out = build()
    if a.out:
        open(a.out, "w").write(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
        print("wrote " + a.out)
    for scope, block in out["counts"].items():
        print("== " + scope)
        for direction, d in block.items():
            print("   %-30s raw %d/%d confirmed, %d refuted | genuine %d/%d confirmed, %d refuted"
                  % (direction, d["raw"]["confirmed"], d["raw"]["n"], d["raw"]["refuted"],
                     d["genuine"]["confirmed"], d["genuine"]["n"], d["genuine"]["refuted"]))
    if out["identifiers_not_in_the_run_file"]:
        print("identifiers not in the run file: "
              + ", ".join(out["identifiers_not_in_the_run_file"]))


if __name__ == "__main__":
    main()
