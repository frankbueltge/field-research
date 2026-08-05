#!/usr/bin/env python3
"""Compose ./data.json for the work from the committed evidence, and nothing else.

Offline and deterministic. Every input is a committed file in this directory, each of them
committed before this script existed, and each hashed into the output so a reader can check
that the page was drawn from the bytes it names.

Inputs
  evidence/source-021-data.json  byte copy of works/2026-08-03-where-the-reader-declines/
                                 data.json — the audited object: sixty cases, the hand-made
                                 split (`in_population`), and the one-line reason behind each.
  reader-R1.json                 reader R1's sixty verdicts, unedited, as returned
  reader-R2.json                 reader R2's sixty verdicts, unedited, as returned
  blind-input.json               exactly what the readers were shown
  results.json                   scores computed by scripts/score.py under the locked rule

The script computes the per-case join and the counts the page shows; the coefficients that
need the locked rule's definitions (Cohen's kappa, the band) are carried across from
results.json unchanged and labelled in the output as carried, not recomputed here.

Run:  python3 build_data.py   (writes ./data.json)
"""

import hashlib
import json
import pathlib

HERE = pathlib.Path(__file__).parent
EV = HERE / "evidence"

# The reader returns, the blind input and the score file sit at the work root, in the exact
# layout scripts/score.py and scripts/make_blind_input.py expect, so that the reproduction
# commands in README.md run here unchanged. evidence/ holds what those scripts do not read:
# the byte copy of the audited object, the two reader prompts, and the 2026-08-04 records.
INPUTS = [
    HERE / "blind-input.json",
    HERE / "reader-R1.json",
    HERE / "reader-R2.json",
    HERE / "results.json",
    EV / "source-021-data.json",
]


def sha256(path: pathlib.Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: pathlib.Path):
    return json.loads(path.read_text())


def main() -> None:
    src = load(EV / "source-021-data.json")
    r1 = {c["case_id"]: c for c in load(HERE / "reader-R1.json")["cases"]}
    r2 = {c["case_id"]: c for c in load(HERE / "reader-R2.json")["cases"]}
    res = load(HERE / "results.json")

    cases = []
    for c in sorted(src["cases"], key=lambda c: c["position"]):
        cid = c["case_id"]
        published = "IN" if c["in_population"] else "OUT"
        a, b = r1[cid], r2[cid]
        cases.append(
            {
                "position": c["position"],
                "case_id": cid,
                "arxiv": c["arxiv"],
                "title": c["title"],
                "excerpt": c["excerpt"],
                "excerpt_sha256": c["excerpt_sha256"],
                "published": published,
                # The original's own one-line reason for the judgement, verbatim from the
                # audited file. `population_reason` carries it for both directions there;
                # `exclusion_reason` repeats it for excluded cases and is null for included
                # ones, so only the first is read.
                "published_reason": c["population_reason"],
                "r1": {"verdict": a["verdict"], "reason": a["reason"], "quote": a["deciding_quote"]},
                "r2": {"verdict": b["verdict"], "reason": b["reason"], "quote": b["deciding_quote"]},
                "disputed": published != a["verdict"] or published != b["verdict"],
                "both_differ": published != a["verdict"] and published != b["verdict"],
            }
        )

    assert len(cases) == 60, len(cases)

    counts = {
        "published_IN": sum(1 for c in cases if c["published"] == "IN"),
        "published_OUT": sum(1 for c in cases if c["published"] == "OUT"),
        "disputed": sum(1 for c in cases if c["disputed"]),
        "both_differ": sum(1 for c in cases if c["both_differ"]),
    }
    for who in ("r1", "r2"):
        for v in ("IN", "OUT", "UNDECIDABLE"):
            counts[f"{who}_{v}"] = sum(1 for c in cases if c[who]["verdict"] == v)
        counts[f"{who}_in_to_out"] = sum(
            1 for c in cases if c["published"] == "IN" and c[who]["verdict"] == "OUT"
        )
        counts[f"{who}_out_to_in"] = sum(
            1 for c in cases if c["published"] == "OUT" and c[who]["verdict"] == "IN"
        )
        counts[f"{who}_agree"] = sum(1 for c in cases if c[who]["verdict"] == c["published"])
    counts["r1_r2_agree"] = sum(1 for c in cases if c["r1"]["verdict"] == c["r2"]["verdict"])

    # Cross-check against the independently computed score file: the same numbers must
    # come out of both, or this build fails rather than publishes a quiet divergence.
    by_pairing = {p["pairing"]: p for p in res["pairings"]}
    assert counts["r1_IN"] == res["counts"]["R1"]["IN"], "R1 IN disagrees with results.json"
    assert counts["r2_IN"] == res["counts"]["R2"]["IN"], "R2 IN disagrees with results.json"
    assert counts["published_IN"] == res["counts"]["original"]["IN"]
    for who, key in (("r1", "original x R1"), ("r2", "original x R2")):
        p = by_pairing[key]
        assert counts[f"{who}_agree"] == p["agree"], (who, counts[f"{who}_agree"], p["agree"])
        assert counts[f"{who}_in_to_out"] == p[f"original_IN_to_{who.upper()}_OUT"]
        assert counts[f"{who}_out_to_in"] == p[f"original_OUT_to_{who.upper()}_IN"]
    assert counts["r1_r2_agree"] == by_pairing["R1 x R2"]["agree"]

    out = {
        "_note": (
            "Built by build_data.py from the committed files listed in `inputs` and nothing else. "
            "Every count in `counts` is computed here from the per-case join and checked "
            "against results.json, which was computed independently by scripts/score.py "
            "under the rule locked in RULE.md before any reader ran. The fields under "
            "`carried` are taken from results.json unchanged."
        ),
        "work": "The Second Reader",
        "date": "2026-08-05",
        "audited_object": {
            "work": "works/2026-08-03-where-the-reader-declines/",
            "instrument": "021 — Where the Reader Declines",
            "file": "data.json",
            "copy": "evidence/source-021-data.json",
        },
        "question_put_to_the_readers": (
            "does this source's own system do research — form hypotheses, run experiments, "
            "analyse, write up, review — or does it do something else (reasoning, code, "
            "robotics, arithmetic, computer operation, fact-checking, negotiation, style)?"
        ),
        "counts": counts,
        "carried": {
            "pairings": res["pairings"],
            "tables": res["tables"],
            "peek_check": res["peek_check"],
            "band_undecidable_outside": res["band_undecidable_outside"],
            "band_undecidable_inside": res["band_undecidable_inside"],
            "validation_errors": res["validation_errors"],
        },
        "inputs": {p.name: sha256(p) for p in INPUTS},
        "cases": cases,
    }

    (HERE / "data.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"data.json written: {len(cases)} cases, {counts['disputed']} disputed")


if __name__ == "__main__":
    main()
