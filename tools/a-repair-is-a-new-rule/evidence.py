#!/usr/bin/env python3
"""The load-bearing quotations, per named case, under the named variants.

Session 167. Only notice lines and extracted holders are quoted, and only for the cases
an adjudication rests on. No licence body is committed.

Usage: evidence.py <variants_dir> <spdx_dir> <c2_dir> <out.json>
"""
import importlib
import json
import os
import sys

CASES = [
    # (corpus, input, why it is here)
    ("C1", "BSD-Inferno-Nettverk",
     "defect 6: the holder sits on a later physical line than the word. Ten blind "
     "workers convicted the shipped rule on this input on 2026-09-21."),
    ("C2", "Tencent/Tencent-XR-3DGen@LICENSE",
     "2026-09-20 class 8: an aggregation of notices whose surviving one extracts no "
     "holder after reflow."),
    ("C2", "microsoft/WindowsAgentArena@LICENSE",
     "a real yearless notice: Copyright (c) <holder>. R7 loses it."),
    ("C2", "elixir-research-group/Verifierstesttimescaling.github.io@LICENSE",
     "the second real yearless notice R7 loses."),
    ("C2", "AI-in-Health/BioMedArena@LICENSE",
     "a bare-year notice with no holder. 2026-09-21 checked it holderless; R6 under "
     "R7's scope attaches the next block's prose to it."),
    ("C2", "raja21068/AutoResearch@LICENSE", "the second bare-year notice."),
    ("C2", "Jinxhy/Awesome-MoAI-Security@LICENSE",
     "no copyright notice at all at baseline; R7 finds one in the liability sentence."),
    ("C1", "MIT", "the canonical MIT text, for the liability sentence itself."),
]
VARIANTS = ["00000", "10000", "01000", "00010", "00100", "00001", "01110", "10001", "11111"]
REPAIRS = ["R1", "R4", "R5", "R6", "R7"]


def main():
    vroot, spdx_dir, c2_dir, out_path = sys.argv[1:5]
    c1 = json.load(open(os.path.join(spdx_dir, "texts.json")))
    c2m = json.load(open(os.path.join(c2_dir, "manifest.json")))
    ok = {f'{e["repo"]}@{e["path"]}' for e in c2m["entries"] if e.get("digest_matches")}
    c2 = {k: v for k, v in json.load(open(os.path.join(c2_dir, "texts.json"))).items()
          if k in ok}
    texts = {"C1": c1, "C2": c2}

    out = {"note": "Session 167. Per case, the verdict and the quoted notice lines under each "
                   "named variant. Short quotations only, load-bearing, no licence body.",
           "variant_key": REPAIRS, "cases": []}
    loaded = {}
    for v in VARIANTS:
        sys.path.insert(0, os.path.join(vroot, v))
        for m in ("rules", "fingerprints"):
            sys.modules.pop(m, None)
        loaded[v] = importlib.import_module("rules")
        sys.path.pop(0)

    for corpus, key, why in CASES:
        raw = texts[corpus].get(key)
        rec = {"corpus": corpus, "input": key, "why": why,
               "present": raw is not None, "under": {}}
        if raw is None:
            out["cases"].append(rec)
            continue
        for v in VARIANTS:
            sys.path.insert(0, os.path.join(vroot, v))
            for m in ("rules", "fingerprints"):
                sys.modules.pop(m, None)
            rules = importlib.import_module("rules")
            fams = rules.l1_families(raw)
            lines = rules.copyright_lines(raw)
            rec["under"][v] = {
                "repairs": [r for r, f in zip(REPAIRS, v) if f == "1"],
                "families": fams,
                "attribution": rules.l2_attribution(raw, fams),
                "delivers": rules.file_delivers(raw)[0],
                "reason": rules.file_delivers(raw)[1],
                "n_notices": len(lines),
                "notices": [{"line": ln[:170], "holder": rules.holder_of(ln)[:120]}
                            for ln in lines[:4]],
            }
            sys.path.pop(0)
        out["cases"].append(rec)
    json.dump(out, open(out_path, "w"), indent=1, ensure_ascii=False)
    for c in out["cases"]:
        if not c["present"]:
            print("MISSING", c["input"]); continue
        print("=" * 70); print(c["corpus"], c["input"])
        for v in VARIANTS:
            u = c["under"][v]
            print(f"  {v} {str(u['repairs']):26s} att={str(u['attribution']):18s} "
                  f"del={u['delivers']} n={u['n_notices']}")
            for n in u["notices"][:2]:
                print(f"       {n['line'][:96]!r}  -> {n['holder'][:52]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
