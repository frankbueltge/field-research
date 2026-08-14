#!/usr/bin/env python3
"""A dated correction to session 115's scoring file — recomputed, not asserted.

Session 119, after the gauntlet. The adversary found that `score-115.json` scores prediction P1
with `transitions_total: 1` and a `detail` block naming `7368171405361351954` (`arutz_7`) —
**the very reading the same session's own confirmation step refuted with five re-requests**, and
which `ledger/corrections.json` now records as an instrument artefact. A scored prediction
resting on a refuted reading is exactly what this practice's rule 6 forbids: *a discarded claim
must never read as live.*

This file recomputes P1 under the overlay and writes the correction beside the original.
**`score-115.json` is not edited** — a dated correction is a new event, never a silent patch.

No requests. Reads files already on disk.
"""
import json
import time

import corrections as corrections_mod

SRC = "score-115.json"
OUT = "score-115-correction-119.json"


def main():
    old = json.load(open(SRC))
    p1 = old["P1"]
    overlay = corrections_mod.load()
    refuted = {vid for (_rf, vid) in overlay}

    kept = [t for t in p1["detail"] if t["vid"] not in refuted]
    dropped = [t for t in p1["detail"] if t["vid"] in refuted]
    n = len(kept)

    # P1 as session 115 wrote it: "0, 1 or 2 confirmed transitions, grimhoundgaming excluded"
    holds_before = p1["verdict"] == "HOLDS"
    holds_after = n in (0, 1, 2)

    out = {
        "schema": "field-research/dated-correction/1", "session": 119,
        "corrects": SRC, "corrects_field": "P1",
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "requests_made": 0,
        "found_by": ("the adversary of session 119, reading the arc's own derived files rather "
                     "than its prose"),
        "what_was_wrong": ("P1 was scored with transitions_total = %d, and its detail block names "
                           "%s — a reading this arc's confirmation step refuted with five "
                           "immediate re-requests and now records as an instrument artefact "
                           "(ledger/corrections.json). The file has read as live since "
                           "2026-08-13." % (p1["transitions_total"],
                                            ", ".join(t["vid"] for t in dropped))),
        "as_published": {"transitions_total": p1["transitions_total"],
                         "verdict": p1["verdict"], "detail": p1["detail"]},
        "corrected": {"transitions_total": n, "detail": kept,
                      "dropped_as_refuted": dropped, "verdict": "HOLDS" if holds_after else
                      "DOES NOT HOLD"},
        "does_the_verdict_move": {
            "before": holds_before, "after": holds_after,
            "answer": ("No. P1 predicted 0, 1 or 2 confirmed transitions, and %d is inside that "
                       "band exactly as 1 was. The verdict does not move; what was wrong is the "
                       "evidence under it — the arc reported a confirmed transition it had "
                       "itself refuted, and the interval it counted was empty." % n)},
        "not_edited": ("score-115.json is left exactly as session 115 wrote it. This correction "
                       "is a new dated event beside it, per the practice's rule that a "
                       "correction is never a silent patch."),
    }
    json.dump(out, open(OUT, "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("corrects", "corrected", "does_the_verdict_move")},
                     indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
