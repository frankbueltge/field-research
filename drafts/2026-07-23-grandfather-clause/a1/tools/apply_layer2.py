#!/usr/bin/env python3
"""A1 — apply the pre-registered Layer-2 reading rule to whatever the detector returned.

Committed collective session 81, 2026-08-02, **before any score existed** — together with
`../LAYER2-PROTOCOL.md`, which is the rule this file executes. That order is the only reason
its output counts as a pre-registered reading rather than an interpretation shaped to fit a
number, and it is checkable in the git log.

Deterministic and offline. It makes no network call and needs no credential. It is NOT run
inside the credentialled job: interpretation is an act of the collective, in session, and a
scheduled job is not a session (protocol R11). A later session runs this, reads it, and
answers for it.

INPUTS   ../a1-results.json   (Layer 1, as session 80 committed it — never modified here)
         ../layer2.json       (raw detector scores, written by run_layer2.py)
OUTPUT   ../a1-layer2-reading.json

WHAT IT WILL NOT DO, by design and not by omission:

  * It computes NO detector-accuracy figure of any kind — no true-positive rate, no
    false-negative rate, no agreement statistic against stratum. The S/N specimens' generated
    character is the provider's claim about its own gallery page, not verified provenance
    (protocol R6). Extending this file to compute one would break the pre-registration.
  * It assigns NO directional label and adjusts NO Layer-1 proportion or Wilson interval. The
    load-bearing comparison stays A1 -> A2 on Layer 1 (protocol R5).
  * It does not write to `a1-results.json`. That file's `layer2: "deferred"` is the true record
    of what session 80 could reach on the seam (protocol R10).

THE ONE STATE THAT MATTERS, AND ITS PRE-REGISTERED NULL (protocol R3):
`unmarked-but-detector-flagged` requires Layer-1 state `unmarked-at-capture` AND a score >= 0.90.
`indeterminate-at-capture` rows are NOT eligible — the pre-registration excludes them from
numerator and denominator precisely because a missing manifest there may be the host's doing.
A1 has zero `unmarked-at-capture` rows, so this state is empty at A1 whatever the scores are.
That was written down before the scores existed; this script recomputes the eligible count from
the data rather than asserting it, so the claim is checked and not merely repeated.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
A1 = HERE.parent

# Boundaries inherited verbatim from instrument 014 and unchanged (protocol R2): >=0.90
# "flagged AI — high", 0.50-0.90 "AI-leaning", 0.10-0.50 "human-leaning", <=0.10 "flagged
# human — high". Display only; the raw floats are the record.
FLAG_THRESHOLD = 0.90
ELIGIBLE_FOR_FLAG_STATE = "unmarked-at-capture"


def tier(score: float) -> str:
    if score >= 0.90:
        return "flagged AI — high"
    if score >= 0.50:
        return "AI-leaning"
    if score > 0.10:
        return "human-leaning"
    return "flagged human — high"


def main() -> int:
    l2_path = A1 / "layer2.json"
    if not l2_path.is_file():
        sys.exit("layer2.json does not exist yet — the queued detector job has not run. "
                 "Nothing to read; this is not an error in the rule.")

    results = json.loads((A1 / "a1-results.json").read_text(encoding="utf-8"))
    layer2 = json.loads(l2_path.read_text(encoding="utf-8"))
    scores = layer2.get("results", {})

    l1_ids = {s["id"] for s in results["specimens"]}
    l2_ids = set(scores)
    if l1_ids != l2_ids:
        sys.exit("specimen sets differ between a1-results.json and layer2.json — "
                 f"only in Layer 1: {sorted(l1_ids - l2_ids)}; "
                 f"only in Layer 2: {sorted(l2_ids - l1_ids)}. Refusing to read across them.")

    rows, unscored = [], []
    for s in results["specimens"]:
        raw = scores[s["id"]]
        score = raw.get("ai_generated")
        row = {
            "id": s["id"],
            "stratum": s["stratum"],
            "in_decision_rule": s["in_decision_rule"],
            "provider": s.get("provider"),
            "layer1_state": s["state"],
            "ai_generated": score,
            "tier": tier(score) if isinstance(score, (int, float)) else None,
            "eligible_for_unmarked_but_detector_flagged":
                s["state"] == ELIGIBLE_FOR_FLAG_STATE,
        }
        if not isinstance(score, (int, float)):
            row["detector_error"] = raw.get("error", "no score returned")
            unscored.append(s["id"])
        rows.append(row)

    # --- the pre-registered state, recomputed rather than asserted (R3) ------------------
    eligible = [r for r in rows if r["eligible_for_unmarked_but_detector_flagged"]]
    flagged = [r["id"] for r in eligible
               if isinstance(r["ai_generated"], (int, float))
               and r["ai_generated"] >= FLAG_THRESHOLD]

    # --- descriptive tabulation only: tier counts per stratum (R4.2, R5) ----------------
    strata: dict = {}
    for r in rows:
        st = strata.setdefault(r["stratum"], {"n": 0, "scored": 0, "tiers": {},
                                              "layer1_states": {}})
        st["n"] += 1
        st["layer1_states"][r["layer1_state"]] = st["layer1_states"].get(r["layer1_state"], 0) + 1
        if r["tier"]:
            st["scored"] += 1
            st["tiers"][r["tier"]] = st["tiers"].get(r["tier"], 0) + 1

    out = {
        "anchor": "A1",
        "reading": "Layer 2 — the detector limb of Article 50(2), read under the rule committed "
                   "at LAYER2-PROTOCOL.md before any score existed",
        "reading_rule_committed": "2026-08-02 (collective session 81)",
        "capture_date": results["date"],
        "days_since_seam_at_capture": results["days_since_seam"],
        "layer2_run_date": layer2.get("layer2_run_date"),
        "days_from_seam_to_layer2_scoring": layer2.get("days_from_seam_to_layer2_scoring"),
        "sha256_all_verified_before_upload": layer2.get("sha256_all_verified_before_upload"),
        "specimens_scored": layer2.get("specimens_scored"),
        "specimens_attempted": layer2.get("specimens_attempted"),
        "unscored_specimens": unscored,
        "unmarked_but_detector_flagged": {
            "eligible_rows": len(eligible),
            "eligible_ids": [r["id"] for r in eligible],
            "flagged_ids": flagged,
            "count": len(flagged),
            "note": ("Requires Layer-1 state 'unmarked-at-capture' AND ai_generated >= 0.90. "
                     "indeterminate-at-capture rows are NOT eligible (protocol R3). If "
                     "eligible_rows is 0 this state is empty as a property of the capture, "
                     "not as a finding about the detector or about marking."),
        },
        "strata_descriptive": strata,
        "refusals": [
            "No detector-accuracy figure is computed (R6): the S/N specimens' generated "
            "character is the provider's claim about its own gallery page, not verified "
            "provenance.",
            "No directional label is assigned and no Layer-1 proportion or Wilson interval is "
            "adjusted (R5): the load-bearing comparison remains A1 -> A2 on Layer 1.",
            "No compliance inference (README, 'What this is NOT'): in-market systems held grace "
            "until 2026-12-02 and pre-seam outputs never needed retroactive marking.",
            "The detector carries no calibration authority (R2, instrument 014's standing "
            "caveat); tiers are display, the raw floats are the record.",
        ],
        "specimens": rows,
    }
    (A1 / "a1-layer2-reading.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")

    print(f"scored {out['specimens_scored']}/{out['specimens_attempted']}; "
          f"layer 2 run {out['days_from_seam_to_layer2_scoring']} day(s) after the seam")
    for name, st in sorted(strata.items()):
        tiers = ", ".join(f"{k}={v}" for k, v in sorted(st["tiers"].items())) or "none scored"
        print(f"{name}: n={st['n']} scored={st['scored']} [{tiers}]")
    print(f"unmarked-but-detector-flagged: {len(flagged)} of {len(eligible)} eligible row(s)")
    if unscored:
        print(f"UNSCORED (errors recorded in layer2.json): {', '.join(unscored)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
