#!/usr/bin/env python3
"""Run 2026-09-20's post-hoc false-notice scan against every repair variant.

Session 167. The suspicion pattern is IMPORTED UNMODIFIED from
tools/same-text-twice/false_notice_scan.py — the same discipline 09-20 used when it
imported the 09-18 rule rather than retyping it. It flags an extracted holder that
reads like the continuation of a sentence. It is a suspicion filter with no stated
false-positive rate, not a decision rule, and it was written on 09-20 after seeing a
relation's class, so it is post-hoc there and inherited here.

Usage: false_notices.py <variants_dir> <spdx_dir> <c2_dir> <out.json>
"""
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools", "same-text-twice"))
from false_notice_scan import SUSPECT                                   # noqa: E402


def scan(rules, texts):
    hits, at_risk = [], 0
    for k, raw in sorted(texts.items()):
        lines = rules.copyright_lines(raw)
        holders = [rules.holder_of(x) for x in lines]
        ph = [bool(rules.has_placeholder(x)) for x in lines]
        fams = rules.l1_families(raw)
        att = rules.l2_attribution(raw, fams)
        flagged = [i for i, h in enumerate(holders) if h and SUSPECT.search(h)]
        if not flagged:
            continue
        clean = [i for i, h in enumerate(holders) if h and i not in flagged and not ph[i]]
        risk = bool(not clean and att == "named")
        at_risk += risk
        hits.append({"input": k, "attribution": att, "n_notices": len(lines),
                     "n_flagged": len(flagged), "n_clean_named": len(clean),
                     "decision_at_risk": risk,
                     "flagged": [{"notice": lines[i][:160], "holder": holders[i][:120]}
                                 for i in flagged]})
    return hits, at_risk


def main():
    vroot, spdx_dir, c2_dir, out_path = sys.argv[1:5]
    c1 = json.load(open(os.path.join(spdx_dir, "texts.json")))
    c2m = json.load(open(os.path.join(c2_dir, "manifest.json")))
    ok = {f'{e["repo"]}@{e["path"]}' for e in c2m["entries"] if e.get("digest_matches")}
    c2 = {k: v for k, v in json.load(open(os.path.join(c2_dir, "texts.json"))).items()
          if k in ok}
    idx = json.load(open(os.path.join(vroot, "index.json")))
    rows, detail = [], {}
    for row in sorted(idx["variants"], key=lambda r: (r["n_repairs"], r["variant"])):
        v = row["variant"]
        sys.path.insert(0, os.path.join(vroot, v))
        for m in ("rules", "fingerprints"):
            sys.modules.pop(m, None)
        rules = importlib.import_module("rules")
        h1, r1 = scan(rules, c1)
        h2, r2 = scan(rules, c2)
        sys.path.pop(0)
        rows.append({"variant": v, "repairs": row["repairs"],
                     "C1_inputs_with_a_false_notice": len(h1),
                     "C1_false_notices": sum(x["n_flagged"] for x in h1),
                     "C2_inputs_with_a_false_notice": len(h2),
                     "C2_false_notices": sum(x["n_flagged"] for x in h2),
                     "inputs_with_a_false_notice": len(h1) + len(h2),
                     "false_notices": sum(x["n_flagged"] for x in h1 + h2),
                     "decisions_at_risk": r1 + r2})
        if v in ("00000", "10000", "00001", "10001", "11111", "01110"):
            detail[v] = {"C1": h1, "C2": h2}
    out = {"note": "Session 167. 2026-09-20's post-hoc false-notice scan, pattern imported "
                   "unmodified, over the unperturbed baseline of every repair variant.",
           "pattern": SUSPECT.pattern,
           "declared": "post-hoc on 2026-09-20 and inherited here; a suspicion filter, "
                       "never a decision rule",
           "reference_2026_09_20": {"inputs_with_a_false_notice": 14, "false_notices": 15,
                                    "decisions_at_risk": 0},
           "variants": rows, "detail": detail}
    json.dump(out, open(out_path, "w"), indent=1, ensure_ascii=False)
    for r in rows:
        print(r["variant"], r["repairs"], "inputs", r["inputs_with_a_false_notice"],
              "notices", r["false_notices"], "decisions_at_risk", r["decisions_at_risk"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
