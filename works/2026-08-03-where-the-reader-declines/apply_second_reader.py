#!/usr/bin/env python3
"""apply_second_reader.py — carry the 2026-08-04 population correction into the data layer.

WHY THIS EXISTS
---------------
This work's headline is computed over a population of 39 sources that one builder selected
by hand. On 2026-08-04 two independent readers re-made that judgement blind and both
returned **23**, agreeing with each other (Cohen's kappa 0.96 on the binary call) far more
than either agreed with this file. Neither reader moved a single case *into* the population
that this file excludes: the divergence is entirely this file being more inclusive.

The prose correction lives in `CORRECTIONS.md` and on the page. That is not enough, and this
practice knows it is not enough: on 2026-08-04 it repaired a shipped work of its own whose
prose carried a withdrawal its **data** did not, and the whole lesson of that repair was that
the data is the form in which a claim reaches anyone who reuses it. A reuser filtering
`data.json` on `in_population` must not get an unreproduced split with nothing attached.

WHAT IT DOES, AND WHAT IT REFUSES TO DO
---------------------------------------
It **adds keys and changes no value**. `in_population` keeps its published value everywhere —
the published figures are what was published, and `RULE.md` §9 of the second-reader study
fixes that neither reader is treated as ground truth, so nothing here silently re-splits the
population. What each case gains is a sibling record of what the independent readers said.

The notice text is defined **once**, below, so every place it appears inherits it rather than
being patched one by one.

The check that makes this trustworthy is at the end: the script re-reads the file it wrote and
asserts, leaf by leaf against the input, that every pre-existing value is byte-identical and
that the only differences are added keys. If that assertion fails, the file is not written.

THE LIMIT, STATED HERE BECAUSE IT IS REAL
-----------------------------------------
`in_population_second_readers` is a **sibling key, not a wrapper**. A reuser who runs
`jq '.cases[] | select(.in_population)'` gets the 39 with no indication that two independent
readers returned 23. That gap is disclosed, not closed — the same limit this practice
published against instrument 019's `verdict_status` on 2026-08-04, and it is the same shape
of limit for the same reason: the published value cannot be altered without destroying the
record of what was actually published.

Idempotent. Offline. stdlib only.

    python3 apply_second_reader.py           # apply
    python3 apply_second_reader.py --check   # exit 1 if the marking is missing or wrong
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data.json"
SECOND = HERE / "second-reader-2026-08-04.json"

# Defined once. Everything downstream inherits it.
NOTICE = (
    "POPULATION NOT REPRODUCED BY INDEPENDENT READERS (2026-08-04). The `in_population` "
    "field in this file is the split published at session 83: 39 of 60. Two readers who had "
    "never seen it, working blind from the same excerpts and the same question, each "
    "returned 23, agreeing with each other at Cohen's kappa 0.96 and with this split at 0.54 "
    "and 0.70. Neither reader added a case this split excludes; every disagreement is this "
    "split including something they would not. The published values are unchanged on purpose "
    "— see CORRECTIONS.md, entry 2026-08-04, for what the figures become under each reader's "
    "split. Any reuse of `in_population` must carry this."
)

STATUS_CONFIRMED = "CONFIRMED by both independent readers (2026-08-04)"
STATUS_DISPUTED = "DISPUTED — see in_population_second_readers (2026-08-04)"


def load_second() -> dict[str, dict[str, str]]:
    s = json.loads(SECOND.read_text(encoding="utf-8"))
    return {c["case_id"]: {"R1": c["R1"], "R2": c["R2"]} for c in s["cases"]}


def mark(doc: dict, second: dict[str, dict[str, str]]) -> dict:
    out = json.loads(json.dumps(doc))  # deep copy; the input is never mutated
    out["_population_correction"] = {
        "date": "2026-08-04",
        "notice": NOTICE,
        "published_n": 39,
        "independent_readers_n": {"R1": 23, "R2": 23},
        "record": "CORRECTIONS.md (entry 2026-08-04); second-reader-2026-08-04.json",
    }
    for case in out["cases"]:
        verdicts = second[case["case_id"]]
        published = "IN" if case["in_population"] else "OUT"
        agreed = verdicts["R1"] == published and verdicts["R2"] == published
        case["in_population_second_readers"] = dict(verdicts)
        case["in_population_status"] = STATUS_CONFIRMED if agreed else STATUS_DISPUTED
    return out


def added_keys_only(before, after, path: str = "") -> list[str]:
    """Every place a pre-existing value changed. Empty list = only keys were added."""
    bad: list[str] = []
    if isinstance(before, dict) and isinstance(after, dict):
        for k, v in before.items():
            if k not in after:
                bad.append(f"{path}/{k}: REMOVED")
            else:
                bad += added_keys_only(v, after[k], f"{path}/{k}")
    elif isinstance(before, list) and isinstance(after, list):
        if len(before) != len(after):
            bad.append(f"{path}: length {len(before)} -> {len(after)}")
        else:
            for i, (b, a) in enumerate(zip(before, after)):
                bad += added_keys_only(b, a, f"{path}/{i}")
    elif before != after:
        bad.append(f"{path}: {before!r} -> {after!r}")
    return bad


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    doc = json.loads(DATA.read_text(encoding="utf-8"))
    second = load_second()
    missing = {c["case_id"] for c in doc["cases"]} - set(second)
    if missing:
        raise SystemExit(f"no second-reader verdict for {len(missing)} case(s): {sorted(missing)[:3]}")

    marked = mark(doc, second)

    if args.check:
        problems: list[str] = []
        if doc.get("_population_correction", {}).get("notice") != NOTICE:
            problems.append("top-level _population_correction missing or stale")
        for case in doc["cases"]:
            if "in_population_second_readers" not in case:
                problems.append(f"{case['case_id']}: no second-reader record")
            elif case.get("in_population_status") not in (STATUS_CONFIRMED, STATUS_DISPUTED):
                problems.append(f"{case['case_id']}: status {case.get('in_population_status')!r}")
        for p in problems:
            print("  ", p)
        print("MARKED" if not problems else f"UNMARKED ({len(problems)} problems)")
        raise SystemExit(0 if not problems else 1)

    # The guarantee: only added keys, no changed values, checked before anything is written.
    baseline = {k: v for k, v in doc.items() if k != "_population_correction"}
    for c in baseline.get("cases", []):
        c.pop("in_population_second_readers", None)
        c.pop("in_population_status", None)
    changed = added_keys_only(baseline, marked)
    if changed:
        raise SystemExit("REFUSING TO WRITE — values changed:\n  " + "\n  ".join(changed[:20]))

    DATA.write_text(json.dumps(marked, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n_disputed = sum(1 for c in marked["cases"] if c["in_population_status"] == STATUS_DISPUTED)
    print(f"marked {len(marked['cases'])} cases; {n_disputed} disputed; no value changed")


if __name__ == "__main__":
    main()
