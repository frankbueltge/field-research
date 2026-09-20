#!/usr/bin/env python3
"""Score both corpora under the pinned rule, once unperturbed and once per relation.

Session 165, 2026-09-20. The rule is IMPORTED from tools/is-it-a-licence/ and never
edited or copied. Its digests are checked here against the pre-registration (K4).
No model is called anywhere in this file.

Usage: run.py <spdx_dir> <c2_dir> <out.json> [--rules-dir DIR] [--label NAME]
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import relations as R                                          # noqa: E402

PINNED = {
    "rules.py": "ccb373b6edb1e4397d7ac145aca6ff94e995934c9315b1ccc23eb266a288a2ed",
    "fingerprints.py": "57db4c561a58683d81fb35be3781168a419785183215a864ed5694981b6669cd",
}


def load_rule(rules_dir):
    digests = {}
    for f in ("rules.py", "fingerprints.py"):
        digests[f] = hashlib.sha256(open(os.path.join(rules_dir, f), "rb").read()).hexdigest()
    sys.path.insert(0, rules_dir)
    for mod in ("rules", "fingerprints"):
        sys.modules.pop(mod, None)
    import rules                                                # noqa
    import fingerprints                                         # noqa
    return rules, fingerprints, digests


def verdict(rules, fp, raw):
    """The whole scored tuple of the pre-registration §5."""
    fams = rules.l1_families(raw)
    att = rules.l2_attribution(raw, fams)
    delivers, reason = rules.file_delivers(raw)
    lines = fp.copyright_lines(raw)
    return {
        "l0": bool(rules.l0_nonempty(raw)),
        "families": list(fams),
        "attribution": att,
        "delivers": bool(delivers),
        "reason": reason,
        "n_notices": len(lines),
        "notices": lines,
        "holders": [fp.holder_of(ln) for ln in lines],
        "placeholders": [bool(fp.has_placeholder(ln)) for ln in lines],
        "apache_appendix_unfilled": bool(rules.apache_appendix_unfilled(raw, fams)),
    }


def key(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=False)


def main():
    spdx_dir, c2_dir, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    rules_dir = os.path.join(ROOT, "tools", "is-it-a-licence")
    label = "shipped"
    if "--rules-dir" in sys.argv:
        rules_dir = sys.argv[sys.argv.index("--rules-dir") + 1]
    if "--label" in sys.argv:
        label = sys.argv[sys.argv.index("--label") + 1]

    rules, fp, digests = load_rule(rules_dir)
    k4 = (label == "shipped" and digests != PINNED)

    c1_texts = json.load(open(os.path.join(spdx_dir, "texts.json")))
    c1_man = json.load(open(os.path.join(spdx_dir, "manifest.json")))
    c2_texts = json.load(open(os.path.join(c2_dir, "texts.json")))
    c2_man = json.load(open(os.path.join(c2_dir, "manifest.json")))
    c2_ok = {f'{e["repo"]}@{e["path"]}' for e in c2_man["entries"] if e.get("digest_matches")}

    corpora = {
        "C1": {k: v for k, v in sorted(c1_texts.items())},
        "C2": {k: v for k, v in sorted(c2_texts.items()) if k in c2_ok},
    }

    result = {
        "note": "Session 165. Verdicts of the pinned 2026-09-18 rule on both corpora, "
                "unperturbed and under each pre-registered metamorphic relation. "
                "No rule and no relation calls a model.",
        "rule_label": label,
        "rules_dir": os.path.relpath(rules_dir, ROOT),
        "rule_digests": digests,
        "K4_digest_mismatch": k4,
        "corpus_digests": {"C1": c1_man["corpus_digest"], "C2": c2_man["corpus_digest"]},
        "counts": {"C1": len(corpora["C1"]), "C2": len(corpora["C2"])},
        "relations": [{"id": i, "desc": d, "scored": i != "M9"} for i, d, _ in R.ALL],
        "baseline": {},
        "violations": [],
        "violation_counts": {},
    }
    if k4:
        result["stopped"] = "K4 fired: the imported rule is not the pinned one."
        json.dump(result, open(out_path, "w"), indent=1, ensure_ascii=False)
        print(json.dumps(result["rule_digests"], indent=1)); return 1

    base = {}
    for cname, texts in corpora.items():
        base[cname] = {}
        for k, raw in texts.items():
            base[cname][k] = verdict(rules, fp, raw)
        result["baseline"][cname] = {k: key(v) for k, v in base[cname].items()}

    for rid, desc, fn in R.ALL:
        n = 0
        for cname, texts in corpora.items():
            for k, raw in texts.items():
                fu = fn(raw)
                v = verdict(rules, fp, fu)
                if key(v) != key(base[cname][k]):
                    n += 1
                    result["violations"].append({
                        "relation": rid, "corpus": cname, "input": k,
                        "source_sha256": hashlib.sha256(raw.encode()).hexdigest(),
                        "followup_sha256": hashlib.sha256(fu.encode()).hexdigest(),
                        "before": base[cname][k], "after": v,
                        "fields_changed": sorted(
                            f for f in v if key(v[f]) != key(base[cname][k][f])),
                    })
        result["violation_counts"][rid] = n

    result["scored_violation_total"] = sum(
        n for r, n in result["violation_counts"].items() if r != "M9")
    json.dump(result, open(out_path, "w"), indent=1, ensure_ascii=False)
    print(json.dumps({
        "rule": label, "counts": result["counts"],
        "violations": result["violation_counts"],
        "scored_total": result["scored_violation_total"]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
