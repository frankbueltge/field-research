#!/usr/bin/env python3
"""Run the rule on this session's own summary. Session 168, 2026-09-23.

Post-hoc and outside the registered measurement: corpus F was pinned before this document
existed. Reported beside the registered result, never instead of it.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from handover import analyse                                        # noqa: E402

ART = sys.argv[1]
text = open(os.path.join(ART, "SUMMARY.md"), encoding="utf-8").read()
toks = analyse(text)
rec = [t for t in toks if t["verdict"] != "not_recomputable"]
out = {
    "note": "Post-hoc, outside the registered measurement: corpus F was pinned before this "
            "document existed. The rule run on this session's own five-minute summary.",
    "tokens": len(toks), "recomputable": len(rec),
    "rate": round(100.0 * len(rec) / len(toks), 2),
    "verdicts": {v: sum(1 for t in rec if t["verdict"] == v)
                 for v in ("consistent", "complement", "inconsistent")},
    "flagged": [{"printed": t["text"], "pair": t["pair"], "verdict": t["verdict"],
                 "why": "this summary quotes a number that was wrong, or a pairing the rule "
                        "gets wrong, in one of the corpora"}
                for t in rec if t["verdict"] != "consistent"],
}
json.dump(out, open(os.path.join(ART, "data", "self.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print(json.dumps({k: out[k] for k in ("tokens", "recomputable", "rate", "verdicts")}))
