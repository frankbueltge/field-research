#!/usr/bin/env python3
"""Compute every verdict from the harvest, and write the committed evidence.

Session 163, 2026-09-18. Needs no network. Usage:
    python3 build.py <harvest.json> <session162-repos.json> <out data.json>

What is committed and what is not: full licence texts are third-party material and are
NOT written out. What is written is the path, size, sha256, the rung verdicts, the
literal copyright line where it holds a template placeholder (which names nobody), the
fact that a holder exists where one does (never the holder's name), and the first 200
normalised characters of every file this instrument could not identify — the evidence
promised in the pre-registration so a reader can judge the hand reading.
"""
import json
import math
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rules
from fingerprints import normalise, SCORED_FAMILIES


def wilson(k, n, z=1.959963984540054):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    s = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return [round((c - s) / d, 4), round((c + s) / d, 4)]


def pct(k, n):
    return None if n == 0 else round(100.0 * k / n, 1)


def main(harvest_path, prior_path, out_path):
    H = json.load(open(harvest_path))
    P = json.load(open(prior_path))
    prior = {r["repo"]: r for r in P["repos"]}

    repos = []
    for h in H["repos"]:
        pr = prior.get(h["repo"], {})
        r3_0916 = bool((pr.get("rungs") or {}).get("R3_licence"))
        prior_blob_sha = {k: v.get("sha256") for k, v in (pr.get("blobs_read") or {}).items()}

        files = []
        for b in h["blobs"]:
            raw = b["text"]
            fams = rules.l1_families(raw)
            att = rules.l2_attribution(raw, fams)
            delivers, reason = rules.file_delivers(raw)
            cl = rules.copyright_lines(raw)
            placeholder_lines = [l for l in cl if rules.has_placeholder(l)][:2]
            named = [l for l in cl if not rules.has_placeholder(l) and rules.holder_of(l)]
            rec = {
                "path": b["path"], "bytes": b["bytes"], "sha256": b["sha256"],
                "nonempty": rules.l0_nonempty(raw),
                "families": fams,
                "attribution": att,
                "scored_family": [f for f in fams if f in SCORED_FAMILIES],
                "delivers": delivers, "reason": reason,
                "n_copyright_lines": len(cl),
                "n_named_copyright_lines": len(named),
                "placeholder_lines": placeholder_lines,
                "apache_appendix_unfilled": rules.apache_appendix_unfilled(raw, fams),
                "sha256_on_0916": prior_blob_sha.get(b["path"]),
                "changed_since_0916": (prior_blob_sha.get(b["path"]) is not None
                                       and prior_blob_sha[b["path"]] != b["sha256"]),
            }
            if not fams:
                rec["first_200_normalised"] = normalise(raw)[:200]
            files.append(rec)

        voices = rules.l3_voices([f["families"] for f in files])
        repos.append({
            "repo": h["repo"], "cohort": h["cohort"],
            "door_ok": h["door_ok"], "door_refs": h["door_refs"],
            "clone_ok": h["clone_ok"], "head_sha": h["head_sha"],
            "n_files": h["n_files"], "tree_digest": h["tree_digest"],
            "tree_digest_0916": pr.get("tree_digest"),
            "tree_changed_since_0916": (pr.get("tree_digest") is not None
                                        and h["tree_digest"] is not None
                                        and pr["tree_digest"] != h["tree_digest"]),
            "R3_licence_0916": r3_0916,
            "error": h["error"],
            "n_licence_shaped": len(h["licence_paths"]),
            "blob_errors": h["blob_errors"],
            "files": files,
            "voices": voices,
            "delivers_any": any(f["delivers"] for f in files),
            "any_placeholder": any(f["attribution"] == "placeholder" for f in files),
            "any_identified": bool(voices),
            "apache_appendix_unfilled": any(f["apache_appendix_unfilled"] for f in files),
        })

    by = {r["repo"]: r for r in repos}
    D1 = [r for r in repos if r["R3_licence_0916"]]
    n1 = len(D1)

    # ---- L0 over files, within D1
    d1_files = [f for r in D1 for f in r["files"]]
    n_files = len(d1_files)
    n_nonempty = sum(1 for f in d1_files if f["nonempty"])

    # ---- L1, L2, headline, all at repository level over D1
    n_identified = sum(1 for r in D1 if r["any_identified"])
    n_delivers = sum(1 for r in D1 if r["delivers_any"])

    # L2 denominator: D1 repositories with at least one file in a SCORED family
    scored_repos = [r for r in D1 if any(f["scored_family"] for f in r["files"])]
    def best_att(r):
        vs = [f["attribution"] for f in r["files"] if f["attribution"] is not None]
        for v in ("named", "placeholder", "no_holder", "no_copyright_line"):
            if v in vs:
                return v
        return None
    att_counts = Counter(best_att(r) for r in scored_repos)
    n_scored = len(scored_repos)
    n_named = att_counts.get("named", 0)
    n_placeholder = att_counts.get("placeholder", 0)

    # ---- L3
    n_multivoice = sum(1 for r in D1 if len(r["voices"]) >= 2)

    # ---- P6: D1 repositories our own R3 rung rests on nothing this instrument identifies
    r3_unsupported = sorted(r["repo"] for r in D1 if not r["any_identified"])

    # ---- cohort split, descriptive only: no test was pre-registered and the design
    #      has no power for one (session 162 measured its own MDE at 14-23 points).
    def split(pred):
        out = {}
        for c in ("A", "B"):
            sub = [r for r in D1 if r["cohort"] == c]
            k = sum(1 for r in sub if pred(r))
            out[c] = {"k": k, "n": len(sub), "pct": pct(k, len(sub))}
        return out

    predictions = [
        {"id": "P1", "claim": "at least 95 % of the licence-shaped files in D1 are non-empty",
         "threshold": 95.0, "observed": pct(n_nonempty, n_files),
         "k": n_nonempty, "n": n_files, "direction": "at_least"},
        {"id": "P2", "claim": "at least 85 % of D1 repositories have a licence-shaped file "
                              "this instrument identifies",
         "threshold": 85.0, "observed": pct(n_identified, n1),
         "k": n_identified, "n": n1, "direction": "at_least"},
        {"id": "P3", "claim": "among D1 repositories with a scored family, at least 90 % name "
                              "a holder that is not a placeholder",
         "threshold": 90.0, "observed": pct(n_named, n_scored),
         "k": n_named, "n": n_scored, "direction": "at_least"},
        {"id": "P4", "claim": "at most 5 % of D1 repositories with a scored family carry an "
                              "unfilled placeholder where the holder should be",
         "threshold": 5.0, "observed": pct(n_placeholder, n_scored),
         "k": n_placeholder, "n": n_scored, "direction": "at_most"},
        {"id": "P5", "claim": "at most 15 % of D1 repositories carry two or more distinct "
                              "identified licence families",
         "threshold": 15.0, "observed": pct(n_multivoice, n1),
         "k": n_multivoice, "n": n1, "direction": "at_most"},
        {"id": "P6", "claim": "at most 3 D1 repositories rest their R3_licence only on files "
                              "this instrument does not identify as a licence",
         "threshold": 3, "observed": len(r3_unsupported),
         "k": len(r3_unsupported), "n": n1, "direction": "at_most_count"},
    ]
    for p in predictions:
        o, t = p["observed"], p["threshold"]
        if o is None:
            p["verdict"] = "undecidable"
        elif p["direction"] == "at_least":
            p["verdict"] = "confirmed" if o >= t else "REFUTED"
        else:
            p["verdict"] = "confirmed" if o <= t else "REFUTED"

    # ---- kill conditions, evaluated here on the harvest
    listed = sum(r["n_licence_shaped"] for r in repos if r["clone_ok"] and r["head_sha"])
    failed_blobs = sum(len(r["blob_errors"]) for r in repos)
    k2_rate = pct(failed_blobs, listed)

    fam_counter = Counter(f for r in repos for f in r["voices"])

    # ------------------------------------------------------------------ post hoc
    # Everything in this block was computed AFTER the six predictions were resolved.
    # It is labelled as post hoc wherever it appears and none of it decides a prediction.
    PERMISSIVE = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "BSD-4-Clause", "ISC",
                  "Zlib", "BSL-1.0", "Unlicense", "CC0-1.0", "WTFPL", "EPL-2.0"}
    RECIPROCAL = {"GPL-2.0", "GPL-3.0", "LGPL-2.1", "LGPL-3.0", "AGPL-3.0", "MPL-2.0",
                  "CC-BY-NC-4.0", "CC-BY-NC-SA-4.0", "Llama-Community", "OpenRAIL"}

    def root_families(r):
        return sorted({x for f in r["files"] if "/" not in f["path"] for x in f["families"]})

    root_ok = [r for r in D1 if root_families(r)]
    no_root_file = [r["repo"] for r in D1 if not any("/" not in f["path"] for f in r["files"])]
    A_all = [r for r in repos if r["cohort"] == "A" and r["head_sha"]]
    A_root = [r for r in A_all if root_families(r)]
    mixed = sorted(r["repo"] for r in D1
                   if (set(r["voices"]) & PERMISSIVE) and (set(r["voices"]) & RECIPROCAL))

    post_hoc = {
        "note": "Computed after the six predictions were resolved. Post hoc, and marked so "
                "wherever it appears.",
        "identified_licence_at_the_root": {
            "claim": "D1 repositories whose ROOT holds a licence file this instrument identifies",
            "k": len(root_ok), "n": n1, "pct": pct(len(root_ok), n1),
            "wilson95": wilson(len(root_ok), n1),
            "repos_with_no_licence_shaped_file_at_the_root": no_root_file,
            "repos_with_a_root_file_we_cannot_identify":
                sorted(r["repo"] for r in D1 if not root_families(r)
                       and any("/" not in f["path"] for f in r["files"])),
        },
        "cohort_A_restated": {
            "n": len(A_all),
            "licence_file_anywhere_0916": {"k": sum(1 for r in A_all if r["R3_licence_0916"]),
                                           "pct": pct(sum(1 for r in A_all if r["R3_licence_0916"]),
                                                      len(A_all))},
            "identified_licence_at_the_root": {"k": len(A_root),
                                               "pct": pct(len(A_root), len(A_all))},
            "benchmark_note": "Hora, Montandon & Costa (arXiv:2605.16701) report LICENSE at "
                              "73.1 %. Their study design II.B says they 'relied on the GitHub "
                              "REST APIs for Git trees to collect all files, directories, and "
                              "extensions', and their directory table counts 'workflows' at "
                              "77.3 %, which only exists inside .github. Their count is "
                              "TREE-WIDE, like session 162's rung. So the 78.6 % comparison "
                              "session 162 made is matched on that point and is NOT corrected "
                              "here. The root figure is a different and stricter question.",
        },
        "permissive_declared_over_reciprocal_present": {
            "claim": "D1 repositories carrying both a permissive and a reciprocal or "
                     "use-restricted family among their licence-shaped files",
            "k": len(mixed), "n": n1, "pct": pct(len(mixed), n1), "repos": mixed,
            "limit": "File level only: no source header is read, so this is a strict lower "
                     "bound on what Wolter et al. measure with a scanner.",
        },
        "root_speaks_for_less_than_the_tree": {
            "claim": "multi-family repositories whose ROOT names fewer families than the tree "
                     "holds — the file-level shadow of what Wolter et al. measure with a scanner",
            "examples": [],
        },
        "run1_defective_L2": {
            "note": "The first build of this session scored L2 with a rule that counted MIT's "
                    "own boilerplate sentence as a copyright notice. It is kept at "
                    "data/data-run1-defective-L2.json. It reported 67 of 67 named, 0 without a "
                    "holder, and a headline of 99.0 %. The repaired rule reports the numbers "
                    "in this file. Nothing was deleted.",
            "run1_headline_pct": 99.0, "run1_named": 67, "run1_no_holder": 0,
        },
    }
    mv = [r for r in D1 if len(r["voices"]) >= 2]
    short_root = [r for r in mv if set(root_families(r)) < set(r["voices"])]
    perm_over_rec = [r for r in mv
                     if set(root_families(r)) and set(root_families(r)) <= PERMISSIVE
                     and (set(r["voices"]) - set(root_families(r))) & RECIPROCAL]
    blk = post_hoc["root_speaks_for_less_than_the_tree"]
    blk["k"] = len(short_root)
    blk["n"] = len(mv)
    blk["examples"] = [{"repo": r["repo"], "root": root_families(r), "tree": r["voices"]}
                       for r in short_root]
    blk["permissive_root_over_reciprocal_below"] = {
        "k": len(perm_over_rec), "n_D1": n1,
        "repos": [{"repo": r["repo"], "root": root_families(r),
                   "below": sorted(set(r["voices"]) - set(root_families(r)))}
                  for r in perm_over_rec]}

    out = {
        "note": "Session 163, 2026-09-18. Of the licence files this practice counted on "
                "2026-09-16, how many are a grant a reader can act on. Every verdict is "
                "computed from the harvest by rules in tools/is-it-a-licence/ and no rule "
                "calls a model.",
        "built_utc": H["finished_utc"],
        "population_digest": H["population_digest"],
        "harvest": {"started_utc": H["started_utc"], "finished_utc": H["finished_utc"],
                    "seconds": H["seconds"]},
        "counts": {
            "n_population": len(repos),
            "doors_answering": sum(1 for r in repos if r["door_ok"]),
            "clones_with_head": sum(1 for r in repos if r["head_sha"]),
            "empty_repositories": sorted(r["repo"] for r in repos if r["door_refs"] == 0),
            "n_D1": n1,
            "D1_cohort_A": sum(1 for r in D1 if r["cohort"] == "A"),
            "D1_cohort_B": sum(1 for r in D1 if r["cohort"] == "B"),
            "n_licence_shaped_files_in_D1": n_files,
            "n_licence_shaped_files_all": sum(r["n_licence_shaped"] for r in repos),
        },
        "headline": {
            "claim": "share of D1 repositories delivering L0 and L1 and (L2 where applicable)",
            "k": n_delivers, "n": n1, "pct": pct(n_delivers, n1),
            "wilson95": wilson(n_delivers, n1),
            "by_cohort": split(lambda r: r["delivers_any"]),
            "against_0916": "session 162 reported 78.6 % of cohort A carrying a licence FILE; "
                            "this is the share of those files that are a grant this instrument "
                            "can identify, over the whole of D1.",
        },
        "rungs": {
            "L0_nonempty_files": {"k": n_nonempty, "n": n_files, "pct": pct(n_nonempty, n_files)},
            "L1_identified_repos": {"k": n_identified, "n": n1, "pct": pct(n_identified, n1),
                                    "wilson95": wilson(n_identified, n1),
                                    "by_cohort": split(lambda r: r["any_identified"])},
            "L2_attribution_over_scored_repos": {
                "n": n_scored, "counts": dict(att_counts),
                "named_pct": pct(n_named, n_scored),
                "placeholder_pct": pct(n_placeholder, n_scored),
                "wilson95_named": wilson(n_named, n_scored)},
            "L3_multivoice_repos": {"k": n_multivoice, "n": n1, "pct": pct(n_multivoice, n1),
                                    "by_cohort": split(lambda r: len(r["voices"]) >= 2)},
        },
        "apache_appendix_unfilled_not_scored": {
            "note": "Reported, never scored. Shipping the Apache-2.0 appendix unedited is the "
                    "normal way to apply the licence (amendment 1 to the pre-registration).",
            "k": sum(1 for r in D1 if r["apache_appendix_unfilled"]),
            "n": sum(1 for r in D1 if "Apache-2.0" in r["voices"]),
        },
        "our_own_rung": {
            "claim": "D1 repositories whose R3_licence rests only on files this instrument "
                     "does not identify as a licence",
            "repos": r3_unsupported,
            "k": len(r3_unsupported), "n": n1, "pct": pct(len(r3_unsupported), n1),
        },
        "families_seen": dict(fam_counter.most_common()),
        "kill_conditions": {
            "K1": "see data/control-check.json — fired on the first run, repaired before any "
                  "repository blob was scored, passed on the second",
            "K2_blob_fetch_failures": {
                "listed_paths": listed, "failed": failed_blobs, "pct": k2_rate,
                "threshold_pct": 10.0,
                "fired": bool(k2_rate is not None and k2_rate > 10.0)},
            "K3": "see data/control-check.json — did not fire",
        },
        "retrievability": {
            "note": "By-product, filed to the standing series, not this session's question.",
            "doors_0831": 144, "doors_0916": 144,
            "doors_0918": sum(1 for r in repos if r["door_ok"]),
            "trees_changed_since_0916": sorted(
                r["repo"] for r in repos if r["tree_changed_since_0916"]),
            "licence_blobs_changed_since_0916": sorted(
                f"{r['repo']}:{f['path']}" for r in repos for f in r["files"]
                if f["changed_since_0916"]),
        },
        "predictions": predictions,
        "post_hoc": post_hoc,
        "repos": repos,
    }
    json.dump(out, open(out_path, "w"), indent=1)
    c = out["counts"]
    print(f"D1 = {n1} repositories ({c['D1_cohort_A']} A / {c['D1_cohort_B']} B), "
          f"{n_files} licence-shaped files")
    print(f"HEADLINE: {n_delivers}/{n1} = {pct(n_delivers, n1)} % deliver")
    print(f"L1 identified: {n_identified}/{n1} = {pct(n_identified, n1)} %")
    print(f"L2 over {n_scored} scored repos: {dict(att_counts)}")
    print(f"L3 two or more families: {n_multivoice}/{n1}")
    print(f"our own rung unsupported: {len(r3_unsupported)} -> {r3_unsupported}")
    print(f"K2: {failed_blobs}/{listed} blob failures")
    for p in predictions:
        print(f"  {p['id']} {p['verdict']:9s} observed {p['observed']} vs {p['threshold']}")
    ph = out["post_hoc"]
    print("post hoc: identified licence AT THE ROOT "
          f"{ph['identified_licence_at_the_root']['k']}/{n1} = "
          f"{ph['identified_licence_at_the_root']['pct']} %")
    print("post hoc: cohort A root", ph["cohort_A_restated"]["identified_licence_at_the_root"])
    print("post hoc: permissive over reciprocal", ph["permissive_declared_over_reciprocal_present"]["k"])
    blk = ph["root_speaks_for_less_than_the_tree"]
    print("post hoc: root names fewer families than the tree:", blk["k"], "of", blk["n"],
          "multi-family repositories")
    print("post hoc: permissive root over a reciprocal family below:",
          blk["permissive_root_over_reciprocal_below"]["k"], "of", n1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
