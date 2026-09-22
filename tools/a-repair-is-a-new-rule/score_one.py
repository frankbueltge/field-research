#!/usr/bin/env python3
"""Score ONE rule variant through all four test regimes of the pre-registration.

Session 167, 2026-09-22. Usage:
    score_one.py <variant_dir> <spdx_dir> <c2_dir> <d1_source.json> <out.json> [--detail]

The four regimes, §4 of the pre-registration:
  1  fixtures  -- the 100 hand-made cases of 2026-09-18, against this variant
  2  mutation  -- the 27 deliberate mutations of 2026-09-18, against this variant
  3  metamorphic -- the 8 scored relations of 2026-09-20 over all 896 inputs
  4  the real corpus -- the 105 D1 repositories and their 156 files

Only DECISION fields count as a violation (§4). The fields that quote the input are
computed, committed and reported separately as description changes — that correction is
by design and is the repair of this practice's seventh bad test.

Nothing here calls a model or the network. It reads fetched text from disk.
"""
import hashlib
import importlib
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools", "same-text-twice"))
import relations as R                                                   # noqa: E402

DECISION = ["l0", "families", "attribution", "delivers", "reason",
            "apache_appendix_unfilled"]
QUOTING = ["n_notices", "notices", "holders", "placeholders"]


def load_variant(vdir):
    sys.path.insert(0, vdir)
    for mod in ("rules", "fingerprints", "fixtures", "mutants"):
        sys.modules.pop(mod, None)
    rules = importlib.import_module("rules")
    fp = importlib.import_module("fingerprints")
    assert os.path.dirname(os.path.abspath(rules.__file__)) == os.path.abspath(vdir), \
        (rules.__file__, vdir)
    return rules, fp


def verdict(rules, fp, raw):
    fams = rules.l1_families(raw)
    att = rules.l2_attribution(raw, fams)
    delivers, reason = rules.file_delivers(raw)
    lines = rules.copyright_lines(raw)
    return {
        "l0": bool(rules.l0_nonempty(raw)),
        "families": list(fams),
        "attribution": att,
        "delivers": bool(delivers),
        "reason": reason,
        "apache_appendix_unfilled": bool(rules.apache_appendix_unfilled(raw, fams)),
        "n_notices": len(lines),
        "notices": lines,
        "holders": [rules.holder_of(ln) for ln in lines],
        "placeholders": [bool(rules.has_placeholder(ln)) for ln in lines],
    }


def key(v, fields):
    return json.dumps([v[f] for f in fields], sort_keys=True, ensure_ascii=False)


def run_fixtures(vdir):
    sys.path.insert(0, vdir)
    for mod in ("rules", "fingerprints", "fixtures"):
        sys.modules.pop(mod, None)
    fx = importlib.import_module("fixtures")
    res = fx.run()
    failed = [r["id"] for r in res if not r["pass"]]
    return {"n_cases": len(res), "n_fail": len(failed), "failed_ids": sorted(failed)}


def run_mutants(vdir):
    for mod in ("rules", "fingerprints", "fixtures", "mutants"):
        sys.modules.pop(mod, None)
    sys.path.insert(0, vdir)
    mt = importlib.import_module("mutants")
    rows, base_fail = [], None
    # mutants.main() prints and writes; re-implement its body so nothing is written
    import fixtures as fx
    base = fx.run()
    base_fail = [r["id"] for r in base if not r["pass"]]
    for name, fn in mt.MUTANTS:
        mt.restore()
        fn()
        try:
            res = fx.run()
            caught = [r["id"] for r in res if not r["pass"]]
        finally:
            mt.restore()
        survived = not [c for c in caught if c not in base_fail]
        rows.append({"mutant": name, "survived": survived,
                     "expected_to_survive": name in mt.EXPECTED_SURVIVORS})
    unexpected = sorted(r["mutant"] for r in rows
                        if r["survived"] and not r["expected_to_survive"])
    caught_but_expected = sorted(r["mutant"] for r in rows
                                 if not r["survived"] and r["expected_to_survive"])
    return {"n_mutants": len(rows), "baseline_failures": sorted(base_fail),
            "n_survived": sum(1 for r in rows if r["survived"]),
            "unexpected_survivors": unexpected,
            "expected_survivors_that_were_caught": caught_but_expected}


def main():
    vdir, spdx_dir, c2_dir, d1_src, out_path = sys.argv[1:6]
    detail = "--detail" in sys.argv
    vid = os.path.basename(os.path.abspath(vdir))

    digests = {f: hashlib.sha256(open(os.path.join(vdir, f), "rb").read()).hexdigest()
               for f in ("rules.py", "fingerprints.py")}

    c1_texts = json.load(open(os.path.join(spdx_dir, "texts.json")))
    c1_man = json.load(open(os.path.join(spdx_dir, "manifest.json")))
    c2_texts = json.load(open(os.path.join(c2_dir, "texts.json")))
    c2_man = json.load(open(os.path.join(c2_dir, "manifest.json")))
    c2_ok = {f'{e["repo"]}@{e["path"]}' for e in c2_man["entries"] if e.get("digest_matches")}
    corpora = {"C1": dict(sorted(c1_texts.items())),
               "C2": {k: v for k, v in sorted(c2_texts.items()) if k in c2_ok}}

    rules, fp = load_variant(vdir)

    # ---------------------------------------------------------- regime 3: metamorphic
    base = {c: {k: verdict(rules, fp, t) for k, t in texts.items()}
            for c, texts in corpora.items()}
    dec_counts, desc_counts, violations = {}, {}, []
    for rid, desc, fn in R.ALL:
        nd = nq = 0
        for c, texts in corpora.items():
            for k, raw in texts.items():
                v = verdict(rules, fp, fn(raw))
                b = base[c][k]
                d = key(v, DECISION) != key(b, DECISION)
                q = key(v, QUOTING) != key(b, QUOTING)
                nd += d
                nq += (q and not d)
                if d:
                    rec = {"relation": rid, "corpus": c, "input": k,
                           "change": "; ".join(
                               f"{f} {json.dumps(b[f], ensure_ascii=False)} -> "
                               f"{json.dumps(v[f], ensure_ascii=False)}"
                               for f in DECISION if key(b, [f]) != key(v, [f]))}
                    if detail:
                        rec["before"] = {f: b[f] for f in DECISION + QUOTING}
                        rec["after"] = {f: v[f] for f in DECISION + QUOTING}
                    violations.append(rec)
        dec_counts[rid] = nd
        desc_counts[rid] = nq
    scored = [r for r, _, _ in R.SCORED]
    dec_total = sum(dec_counts[r] for r in scored)

    # ------------------------------------------------------- regime 4: the real corpus
    D1src = json.load(open(d1_src))
    d1 = [r for r in D1src["repos"] if r["R3_licence_0916"]]
    SCORED_FAMS = fp.SCORED_FAMILIES
    repo_rows, missing = [], []
    for r in d1:
        files = []
        for f in r["files"]:
            k = r["repo"] + "@" + f["path"]
            if k not in corpora["C2"]:
                missing.append(k)
                continue
            raw = corpora["C2"][k]
            fams = rules.l1_families(raw)
            files.append({
                "path": f["path"],
                "families": fams,
                "attribution": rules.l2_attribution(raw, fams),
                "scored_family": [x for x in fams if x in SCORED_FAMS],
                "delivers": rules.file_delivers(raw)[0],
                "reason": rules.file_delivers(raw)[1],
                "n_notices": len(rules.copyright_lines(raw)),
            })
        repo_rows.append({
            "repo": r["repo"], "cohort": r["cohort"],
            "voices": rules.l3_voices([x["families"] for x in files]),
            "delivers_any": any(x["delivers"] for x in files),
            "any_identified": bool(rules.l3_voices([x["families"] for x in files])),
            "files": files,
        })

    def best_att(r):
        vs = [f["attribution"] for f in r["files"] if f["attribution"] is not None]
        for v in ("named", "placeholder", "no_holder", "no_copyright_line"):
            if v in vs:
                return v
        return None

    scored_repos = [r for r in repo_rows if any(f["scored_family"] for f in r["files"])]
    att = Counter(best_att(r) for r in scored_repos)
    headline_k = sum(1 for r in repo_rows if r["delivers_any"])
    out = {
        "variant": vid,
        "digests": digests,
        "corpus_digests": {"C1": c1_man["corpus_digest"], "C2": c2_man["corpus_digest"]},
        "counts": {"C1": len(corpora["C1"]), "C2": len(corpora["C2"])},
        "fixtures": run_fixtures(vdir),
        "mutation": run_mutants(vdir),
        "metamorphic": {
            "decision_changing": dec_counts,
            "description_only": desc_counts,
            "scored_decision_total": dec_total,
            "control_M4_decision": dec_counts["M4"],
        },
        "real_corpus": {
            "n_D1": len(repo_rows),
            "missing_texts": sorted(missing),
            "headline": {"k": headline_k, "n": len(repo_rows),
                         "pct": round(100.0 * headline_k / len(repo_rows), 1)},
            "identified": {"k": sum(1 for r in repo_rows if r["any_identified"]),
                           "n": len(repo_rows)},
            "L2": {"n": len(scored_repos), "counts": dict(sorted(att.items(),
                                                                 key=lambda x: str(x[0])))},
            "multivoice": sum(1 for r in repo_rows if len(r["voices"]) >= 2),
            "delivering_repos": sorted(r["repo"] for r in repo_rows if r["delivers_any"]),
            "no_holder_repos": sorted(r["repo"] for r in scored_repos
                                      if best_att(r) == "no_holder"),
        },
        "unperturbed_keys": {c: {k: key(v, DECISION) for k, v in base[c].items()}
                             for c in ("C1", "C2")},
        "violations": violations if detail else violations[:0],
        "n_violations_recorded": len(violations),
    }
    if detail:
        out["unperturbed_full"] = {c: {k: {f: v[f] for f in DECISION + QUOTING}
                                       for k, v in base[c].items()} for c in ("C1", "C2")}
    json.dump(out, open(out_path, "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"variant": vid, "fixtures_fail": out["fixtures"]["n_fail"],
                      "mut_unexpected": out["mutation"]["unexpected_survivors"],
                      "dec_total": dec_total, "M4": dec_counts["M4"],
                      "headline": out["real_corpus"]["headline"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
