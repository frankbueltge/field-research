#!/usr/bin/env python3
"""Commit the evidence a reader needs and nothing a licence forbids.

Session 165. Two files:
  verdicts.json    the decision fields of every input under every rule variant,
                   unperturbed - 896 inputs x 4 rules
  violations.json  every decision-changing violation, with both digests and the
                   decision fields before and after, plus the notice lines where a
                   notice is what changed (short quotations, load-bearing)

No licence body is committed. Only notice lines are quoted, and only where the
adjudication rests on them.
"""
import json
import sys

DEC = ["l0", "families", "attribution", "delivers", "reason", "apache_appendix_unfilled"]


def main():
    sc, outdir = sys.argv[1], sys.argv[2]
    runs = {v: json.load(open(f"{sc}/run-{v}.json")) for v in ("shipped", "B", "C", "D")}
    v = {"note": "Session 165. Decision fields of every input, unperturbed, under each "
                 "rule variant. Re-derivable from the named feeds and the committed digests.",
         "rules": {k: r["rule_digests"] for k, r in runs.items()},
         "inputs": {}}
    for c in ("C1", "C2"):
        for k in runs["shipped"]["baseline"][c]:
            rec = {"corpus": c}
            for lab, r in runs.items():
                d = json.loads(r["baseline"][c][k])
                rec[lab] = {f: d[f] for f in DEC}
                rec[lab]["n_notices"] = d["n_notices"]
            v["inputs"][k] = rec
    json.dump(v, open(f"{outdir}/verdicts.json", "w"), indent=1, ensure_ascii=False)

    out = {"note": "Session 165. Every decision-changing violation of the shipped rule, and "
                   "of each repair variant. A violation is one (relation, input) pair whose "
                   "decision fields differ between the source text and the follow-up text.",
           "by_rule": {}}
    for lab, r in runs.items():
        rows = []
        for x in r["violations"]:
            ch = [f for f in DEC
                  if json.dumps(x["before"][f], sort_keys=True)
                  != json.dumps(x["after"][f], sort_keys=True)]
            if not ch:
                continue
            rows.append({
                "relation": x["relation"], "corpus": x["corpus"], "input": x["input"],
                "source_sha256": x["source_sha256"], "followup_sha256": x["followup_sha256"],
                "changed": ch,
                "before": {f: x["before"][f] for f in ch},
                "after": {f: x["after"][f] for f in ch},
                "notices_before": x["before"]["notices"][:4],
                "notices_after": x["after"]["notices"][:4],
            })
        out["by_rule"][lab] = {"n": len(rows), "rows": rows}
    json.dump(out, open(f"{outdir}/violations.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: d["n"] for k, d in out["by_rule"].items()}, indent=1))


if __name__ == "__main__":
    main()
