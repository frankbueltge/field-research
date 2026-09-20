#!/usr/bin/env python3
"""Assemble session 165's data.json from the four runs.

The pre-registered oracle is the whole verdict tuple (§5). This session found that
oracle too wide -- `notices` and `holders` QUOTE the input, so they cannot be
invariant under a relation that edits the lines they quote. Both readings are
reported: the registered one and a decision-field reading declared post-hoc.

No model is called here.
"""
import collections
import json
import os
import sys

DEC = ["l0", "families", "attribution", "delivers", "reason", "apache_appendix_unfilled"]
ECHO = ["notices", "holders", "n_notices", "placeholders"]


def j(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=False)


def dec_changed(v):
    return [f for f in DEC if j(v["before"][f]) != j(v["after"][f])]


def sig(v):
    return (v["relation"],
            " | ".join(f"{f}: {v['before'][f]!r} -> {v['after'][f]!r}" for f in dec_changed(v)))


def summarise(run):
    out = {"rule_label": run["rule_label"], "rule_digests": run["rule_digests"],
           "registered_oracle": {}, "decision_oracle": {}, "classes": {}}
    cls = collections.defaultdict(list)
    for v in run["violations"]:
        if dec_changed(v):
            cls[sig(v)].append(v)
    for rid, _, _ in [(r["id"], 0, 0) for r in run["relations"]]:
        out["registered_oracle"][rid] = run["violation_counts"][rid]
        out["decision_oracle"][rid] = sum(len(x) for (r, _), x in cls.items() if r == rid)
    out["registered_scored_total"] = sum(n for r, n in out["registered_oracle"].items() if r != "M9")
    out["decision_scored_total"] = sum(n for r, n in out["decision_oracle"].items() if r != "M9")
    out["scored_classes"] = sum(1 for (r, _) in cls if r != "M9")
    out["unscored_classes_M9"] = sum(1 for (r, _) in cls if r == "M9")
    out["classes"] = [
        {"relation": r, "change": s, "n": len(x),
         "C1": sum(1 for v in x if v["corpus"] == "C1"),
         "C2": sum(1 for v in x if v["corpus"] == "C2"),
         "examples": [v["input"] for v in x[:5]]}
        for (r, s), x in sorted(cls.items())]
    out["echo_only_violations"] = sum(
        1 for v in run["violations"] if not dec_changed(v) and v["relation"] != "M9")
    return out


def headline(old, base, byrepo, D1):
    delivers = sum(1 for rp in D1 if any(json.loads(base[k])["delivers"] for k in byrepo[rp]))
    noholder = []
    for rp in D1:
        atts = [a for a in (json.loads(base[k])["attribution"] for k in byrepo[rp])
                if a is not None]
        if atts and "named" not in atts:
            noholder.append(rp)
    return {"k": delivers, "n": len(D1), "pct": round(100 * delivers / len(D1), 1),
            "names_no_holder": len(noholder), "names_no_holder_repos": sorted(noholder)}


def main():
    sc, out_path, root = sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "."
    runs = {v: json.load(open(os.path.join(sc, f"run-{v}.json")))
            for v in ("shipped", "B", "C", "D")}
    old = json.load(open(os.path.join(
        root, "artifacts/2026-09-18-a-licence-file-is-not-a-licence/data/data.json")))
    c1man = json.load(open(os.path.join(sc, "spdx", "manifest.json")))
    c2man = json.load(open(os.path.join(sc, "c2", "manifest.json")))
    old_c1 = json.load(open(os.path.join(
        root, "artifacts/2026-09-19-the-second-hand/data/corpus.json")))

    byrepo = collections.defaultdict(list)
    for r in old["repos"]:
        for f in r.get("files", []):
            byrepo[r["repo"]].append(r["repo"] + "@" + f["path"])
    D1 = [r["repo"] for r in old["repos"] if r["n_licence_shaped"] > 0]

    # K1: does the shipped rule reproduce every committed 2026-09-18 verdict?
    base = {k: json.loads(v) for k, v in runs["shipped"]["baseline"]["C2"].items()}
    k1 = []
    for r in old["repos"]:
        for f in r.get("files", []):
            k = r["repo"] + "@" + f["path"]
            b = base.get(k)
            if b is None:
                k1.append([k, "absent"]); continue
            named = sum(1 for i, h in enumerate(b["holders"])
                        if h and not b["placeholders"][i])
            ph = sorted(l for i, l in enumerate(b["notices"]) if b["placeholders"][i])
            for fld, a, c in (("families", f["families"], b["families"]),
                              ("attribution", f["attribution"], b["attribution"]),
                              ("delivers", f["delivers"], b["delivers"]),
                              ("reason", f["reason"], b["reason"]),
                              ("n_copyright_lines", f["n_copyright_lines"], b["n_notices"]),
                              ("n_named", f["n_named_copyright_lines"], named),
                              ("placeholder_lines", sorted(f["placeholder_lines"]), ph),
                              ("apache", f["apache_appendix_unfilled"],
                               b["apache_appendix_unfilled"])):
                if j(a) != j(c):
                    k1.append([k, fld, a, c])

    data = {
        "note": "Session 165, 2026-09-20. Metamorphic perturbation of this practice's own "
                "2026-09-18 measuring rule, on the two corpora its published numbers and "
                "its 2026-09-19 experiment rest on. No rule, relation, adjudication or "
                "check in this session calls a model.",
        "preregistration": "PREREGISTRATION.md, committed before any corpus was fetched",
        "corpora": {
            "C1": {"what": "the 740 canonical SPDX licence texts, as published",
                   "n": runs["shipped"]["counts"]["C1"],
                   "license_list_version": c1man["license_list_version"],
                   "corpus_digest": c1man["corpus_digest"],
                   "digest_of_2026_09_19": old_c1["corpus_digest"],
                   "identical_to_2026_09_19": c1man["corpus_digest"] == old_c1["corpus_digest"],
                   "days_since": 1},
            "C2": {"what": "the 156 licence-shaped files of 2026-09-18, at their pinned commits",
                   "n": runs["shipped"]["counts"]["C2"],
                   "n_pinned": c2man["n_pinned"], "n_fetched": c2man["n_fetched"],
                   "n_digest_matches": c2man["n_digest_matches"],
                   "excluded": c2man["excluded"], "corpus_digest": c2man["corpus_digest"],
                   "days_since": 2},
        },
        "kill_conditions": {
            "K1_fidelity_of_SUT": {"fired": bool(k1), "fields_compared": 8,
                                   "files_compared": len(base), "mismatches": k1},
            "K2_fidelity_of_C1": {"fired": not (c1man["corpus_digest"] == old_c1["corpus_digest"]),
                                  "share_matching": 1.0},
            "K3_null": {"fired": runs["shipped"]["violation_counts"]["M1"] == 0},
            "K4_identity": {"fired": runs["shipped"]["K4_digest_mismatch"]},
        },
        "relations": runs["shipped"]["relations"],
        "runs": {v: summarise(r) for v, r in runs.items()},
        "headline_rederived": {v: headline(old, runs[v]["baseline"]["C2"], byrepo, D1)
                               for v in ("shipped", "C", "D")},
        "headline_published_0918": {"k": old["headline"]["k"], "n": old["headline"]["n"],
                                    "pct": old["headline"]["pct"], "names_no_holder": 6},
        "baseline_movement_under_repair": {},
    }
    for v in ("B", "C", "D"):
        mv = {}
        for c in ("C1", "C2"):
            tup = [k for k in runs["shipped"]["baseline"][c]
                   if runs["shipped"]["baseline"][c][k] != runs[v]["baseline"][c][k]]
            dec = [k for k in tup
                   if any(j(json.loads(runs["shipped"]["baseline"][c][k])[f])
                          != j(json.loads(runs[v]["baseline"][c][k])[f]) for f in DEC)]
            mv[c] = {"tuples_moved": len(tup), "decisions_moved": len(dec),
                     "decisions": sorted(dec)}
        data["baseline_movement_under_repair"][v] = mv

    json.dump(data, open(out_path, "w"), indent=1, ensure_ascii=False)
    r = data["runs"]
    print(json.dumps({
        "K": {k: v["fired"] for k, v in data["kill_conditions"].items()},
        "registered_total": {v: r[v]["registered_scored_total"] for v in r},
        "decision_total": {v: r[v]["decision_scored_total"] for v in r},
        "classes": {v: r[v]["scored_classes"] for v in r},
        "echo_only": {v: r[v]["echo_only_violations"] for v in r},
        "headline": data["headline_rederived"]}, indent=1))


if __name__ == "__main__":
    main()
