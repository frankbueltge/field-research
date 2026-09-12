#!/usr/bin/env python3
"""Anchor the screen verdicts of the sampled items to a text a checker can re-run the rules on.

Session 158, cycle 003. Written **after** an adversary broke check.py on 2026-09-12 by editing
`hollow_broad` in data/task-rows.json, recomputing the derived figures to match, and passing
1,434 checks. The break was real: the per-item screen verdicts had no anchor anywhere in the
repository, so the checker could only test them for internal consistency with themselves.

What this writes, per sampled record: the **raw value**, its sha256, and each frozen rule's outcome
computed here by importing the frozen rules. `check.py` then re-runs R1, R2, R3 and R5 itself from
the raw value and refuses any disagreement, so a verdict cannot be edited without also editing a
text that the masked sheet — committed before any label existed — must still reproduce.

**What this cannot anchor, stated plainly: R4.** The duplicate rule is a relation between a value and
the whole catalogue, and the catalogue is not in this repository (protocol §7). R4 is therefore
checkable only by re-fetching the feed at the recorded digest. `check.py` says so rather than
implying it verified it.

**Status: post-hoc.** This file ran after the labels existed. It is not a primary record. Its
authority is that the raw values it carries must mask down, byte for byte, to values committed in the
sheets before any label existed — which is what makes editing them detectable.

No model is called anywhere in this file. Standard library only.

Usage:
    python3 tools/identify/anchor.py --cache /path/to/cache
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from identify import mask, tokens, r5_title_echo, ARMS  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hollow"))
import hollow  # noqa: E402

OUT = "artifacts/cycle-003/2026-09-12-what-a-description-is-for/data"


def load_recs(cache: str, arm: str) -> dict:
    out = {}
    with open(os.path.join(cache, f"{arm}-recs.jsonl"), encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                r = json.loads(line)
                out[r["id"]] = r
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    args = ap.parse_args()

    keys = json.load(open(os.path.join(OUT, "sheet-key.json"), encoding="utf-8"))
    recs = {"atlas": load_recs(args.cache, "atlas"), "uk": load_recs(args.cache, "uk")}
    arm_of = {"atlas-masked": "atlas", "atlas-unmasked": "atlas", "uk-masked": "uk"}

    out = {
        "_status": "POST-HOC, DECLARED. Written after the labels existed, in response to a checker "
                   "break found by an adversary on 2026-09-12. Not a primary record.",
        "_what_it_anchors": "R1, R2, R3 and R5 are recomputable by check.py from `value` below using "
                            "the frozen rules. The aggregates must follow from the rule outcomes by "
                            "their own boolean definitions.",
        "_what_it_cannot_anchor": "R4 (duplicate) is a relation between a value and the whole "
                                  "catalogue, which is not in this repository (protocol §7). It is "
                                  "checkable only by re-fetching the feed at the digest recorded in "
                                  "results.json.manifest and re-running tools/identify/identify.py.",
        "_why_it_is_not_circular": "Every `value` here must mask down byte-for-byte to the value "
                                   "carried in the matching sheet, and the sheets were committed "
                                   "before any label existed. check.py enforces that round trip.",
        "arms": {},
    }
    for sheet, arm in arm_of.items():
        rows = []
        for k in keys[sheet]:
            r = recs[arm][k["id"]]
            raw = hollow.norm(r["text"])
            c = hollow.classify(r["text"], set())  # R4 supplied separately; see note above
            rows.append({
                "item": k["item"], "id": k["id"], "title": r["title"], "value": raw,
                "value_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                "masked": r["masked"], "masked_token_count": len(tokens(r["masked"])),
                "title_has_no_maskable_token": not tokens(r["title"]),
                "r1_chrome": c["r1_chrome"], "r2_truncated_tail": c["r2_truncated_tail"],
                "r3_truncated_head": c["r3_truncated_head"],
                "r4_duplicate": r["r4_duplicate"],
                "r5_title_echo": r5_title_echo(r["text"], r["title"]),
                "hollow_strict": r["hollow_strict"], "hollow_broad": r["hollow_broad"],
                "identifies_uniquely": r["identifies_uniquely"],
                "narrowing_set_size": r["narrowing_set_size"],
            })
            # the mask must be reproducible from the raw value and the title
            assert mask(r["text"], r["title"]) == r["masked"], f"mask mismatch on {k['id']}"
        out["arms"][sheet] = rows

    json.dump(out, open(os.path.join(OUT, "screen-anchor.json"), "w"), indent=2, ensure_ascii=False)
    n = sum(len(v) for v in out["arms"].values())
    noop = sum(1 for v in out["arms"].values() for r in v if r["title_has_no_maskable_token"])
    print(f"anchored {n} sampled items across {len(out['arms'])} sheets; "
          f"{noop} have a title with no maskable token")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
