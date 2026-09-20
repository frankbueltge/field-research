#!/usr/bin/env python3
"""Post-hoc: does the UNPERTURBED data already contain false copyright notices?

Session 165. Declared post-hoc, and the provenance matters: relation M6 produced a
class in which a reflowed liability sentence was read as a copyright notice. That
class prompted this scan of the unperturbed baseline. It is not a rung, it was not
pre-registered, and the pattern below was written after seeing that class. Every hit
is hand-read and recorded in data/adjudication.json.

The pattern flags an EXTRACTED HOLDER that reads like the continuation of a sentence.
It is a suspicion filter with a stated false-positive rate, not a decision rule.
"""
import json
import re
import sys

SUSPECT = re.compile(
    r"(?i)\b(be liable|shall be|liable for|notice and|holders? be|is hereby|must be"
    r"|may not|in all copies|disclaim|warrant|damages|include|retain|reproduce)\b")


def main():
    run = json.load(open(sys.argv[1]))
    out = {"note": __doc__.strip().split("\n\n")[0],
           "declared": "post-hoc; pattern written after seeing relation M6's class",
           "pattern": SUSPECT.pattern, "hits": [], "decisions_at_risk": 0}
    for corpus in ("C1", "C2"):
        for k, raw in run["baseline"][corpus].items():
            v = json.loads(raw)
            flagged = [i for i, h in enumerate(v["holders"]) if h and SUSPECT.search(h)]
            if not flagged:
                continue
            clean = [i for i, h in enumerate(v["holders"])
                     if h and i not in flagged and not v["placeholders"][i]]
            at_risk = bool(not clean and v["attribution"] == "named")
            out["decisions_at_risk"] += at_risk
            out["hits"].append({
                "corpus": corpus, "input": k, "attribution": v["attribution"],
                "n_notices": v["n_notices"], "n_flagged": len(flagged),
                "n_clean_named": len(clean), "decision_at_risk": at_risk,
                "flagged": [{"notice": v["notices"][i], "holder": v["holders"][i]}
                            for i in flagged]})
    out["n_inputs_with_a_false_notice"] = len(out["hits"])
    out["n_false_notices"] = sum(h["n_flagged"] for h in out["hits"])
    json.dump(out, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k != "hits"}, indent=1))


if __name__ == "__main__":
    main()
