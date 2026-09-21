#!/usr/bin/env python3
"""Score the blind adjudications of session 166 against the committed references.

No model is called in this file. Fleiss' kappa is written out here rather than taken from
a library, and is reported as a bare number: this practice has not read Landis & Koch
first-hand and attaches no verbal band to it.

Two readings are produced for every arm and both are reported:
  K3   - only the workers that passed all four sentinels, which is what the
         pre-registration's kill condition requires;
  ALL  - every worker dispatched, declared post-hoc, because the sentinel itself turned
         out to admit a defensible second answer (see the artifact).

Usage: score.py <items.json> <answers_dir> <out.json>
"""
import collections
import glob
import json
import os
import re
import sys


def fleiss_kappa(assignments):
    if len(assignments) < 2:
        return None
    ns = {sum(a.values()) for a in assignments}
    if len(ns) != 1:
        return None
    n = ns.pop()
    if n < 2:
        return None
    cats = sorted({c for a in assignments for c in a})
    N = len(assignments)
    P_i = [(sum(a.get(c, 0) ** 2 for c in cats) - n) / (n * (n - 1)) for a in assignments]
    P_bar = sum(P_i) / N
    p_j = [sum(a.get(c, 0) for a in assignments) / (N * n) for c in cats]
    P_e = sum(p * p for p in p_j)
    return None if P_e == 1 else (P_bar - P_e) / (1 - P_e)


def load(path):
    """Take the first complete top-level JSON array, by bracket matching, and hand back
    whatever followed it rather than silently dropping it."""
    raw = open(path, encoding="utf-8").read().strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    i = raw.find("[")
    if i < 0:
        raise ValueError(f"{path}: no JSON array")
    depth, instr, esc, end = 0, False, False, None
    for j in range(i, len(raw)):
        c = raw[j]
        if instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
            continue
        if c == '"':
            instr = True
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    if end is None:
        raise ValueError(f"{path}: unterminated JSON array")
    return {x["item"]: x for x in json.loads(raw[i:end])}, raw[end:].strip()


def norm(arm, a):
    a = str(a).strip()
    if arm == "A":
        low = a.lower()
        return "1" if low.startswith("1") else "2" if low.startswith("2") else "neither"
    up = a.upper().replace("MR_FALSE", "MR-FALSE").replace("MRFALSE", "MR-FALSE")
    return up


def ref_answer(arm, it):
    if arm == "B":
        return it["reference"]
    if it["kind"] == "sentinel":
        return it["reference"]
    if it["reference"] == "specification does not decide":
        return "neither"
    ours = str(it["ours_is"])
    other = "2" if ours == "1" else "1"
    return ours if it["reference"] == "R-ship right" else other


def majority(votes):
    t = collections.Counter(votes)
    top = t.most_common()
    if not top:
        return None, t
    if len(top) == 1 or top[0][1] > top[1][1]:
        return top[0][0], t
    return None, t


def reading(arm, items, ans, workers):
    cases = sorted(i for i in items if items[i]["kind"] == "case")
    rows = []
    for i in cases:
        it = items[i]
        votes = {w: norm(arm, ans[w][i]["answer"]) for w in workers if i in ans[w]}
        maj, tally = majority(votes.values())
        ref = ref_answer(arm, it)
        row = {"item": i, "true_id": it["true_id"], "corpus": it["corpus"],
               "reference": ref, "reference_label": it["reference"],
               "votes": votes, "tally": dict(tally), "majority": maj,
               "majority_matches_reference": (maj == ref) if maj else None,
               "unanimous": len(tally) == 1 and len(votes) == len(workers),
               "unanimous_against_reference": (len(tally) == 1 and len(votes) == len(workers)
                                               and maj != ref)}
        if arm == "B":
            row["class"] = it["klass"]
        rows.append(row)
    rec = {
        "workers": sorted(workers),
        "per_item": rows,
        "n_cases": len(rows),
        "majority_matches_reference": sum(1 for r in rows if r["majority_matches_reference"]),
        "majority_is_a_tie": sum(1 for r in rows if r["majority"] is None),
        "unanimous_against_reference": [r["item"] for r in rows
                                        if r["unanimous_against_reference"]],
        "per_worker_agreement_with_reference": {
            w: {"n": sum(1 for i in cases if i in ans[w]),
                "agree": sum(1 for i in cases if i in ans[w]
                             and norm(arm, ans[w][i]["answer"]) == ref_answer(arm, items[i]))}
            for w in sorted(workers)},
        "fleiss_kappa_items": fleiss_kappa(
            [collections.Counter(r["votes"].values()) for r in rows
             if len(r["votes"]) == len(workers)]),
    }
    if arm == "B":
        byc = collections.defaultdict(list)
        for r in rows:
            byc[r["class"]].append(r)
        cls = {}
        for c, rs in byc.items():
            per = {}
            for w in workers:
                m, _ = majority([r["votes"][w] for r in rs if w in r["votes"]])
                per[w] = m
            m, t = majority([v for v in per.values() if v])
            cls[c] = {"n_items": len(rs), "reference": rs[0]["reference"],
                      "per_worker": per, "majority": m,
                      "matches_reference": m == rs[0]["reference"],
                      "unanimous_against_reference": (len(t) == 1 and m != rs[0]["reference"]
                                                      and len(per) == len(workers))}
        rec["per_class"] = cls
        rec["n_classes"] = len(cls)
        rec["classes_majority_matches_reference"] = sum(1 for v in cls.values()
                                                        if v["matches_reference"])
        rec["fleiss_kappa_classes"] = fleiss_kappa(
            [collections.Counter(v for v in c["per_worker"].values() if v)
             for c in cls.values()])
    return rec


def main():
    items_path, ans_dir, out_path = sys.argv[1:4]
    man = json.load(open(items_path))
    out = {"note": "Session 166, 2026-09-21. The blind adjudications scored against the "
                   "references committed on 2026-09-19 and 2026-09-20. Those references "
                   "were produced by this practice and are NOT a human baseline; see "
                   "PREREGISTRATION.md section 1.",
           "arms": {}}

    for arm in ("A", "B"):
        items = {it["item_id"]: it for it in man["items"][arm]}
        ans, tails = {}, {}
        for p in sorted(glob.glob(os.path.join(ans_dir, f"{arm}-w*.json"))):
            w = re.search(r"-(w\d+)\.json$", p).group(1)
            ans[w], tails[w] = load(p)
        sents = [i for i in items if items[i]["kind"] == "sentinel"]
        sentinel = {}
        for w, a in ans.items():
            missed = [i for i in sorted(sents)
                      if i not in a or norm(arm, a[i]["answer"]) != ref_answer(arm, items[i])]
            sentinel[w] = {"passed": len(sents) - len(missed), "of": len(sents),
                           "missed": missed,
                           "answers_on_missed": {i: {"answer": a[i]["answer"],
                                                     "reason": a[i].get("reason", "")}
                                                 for i in missed if i in a},
                           "void_under_K3": bool(missed)}
        passed = sorted(w for w in ans if not sentinel[w]["void_under_K3"])
        out["arms"][arm] = {
            "n_items": len(items), "n_sentinels": len(sents),
            "workers_dispatched": sorted(ans),
            "coverage": {w: len(a) for w, a in ans.items()},
            "trailing_text_after_the_array": {w: t for w, t in tails.items() if t},
            "sentinels": sentinel,
            "workers_void_under_K3": sorted(w for w in ans if sentinel[w]["void_under_K3"]),
            "K3": reading(arm, items, ans, passed) if len(passed) >= 2 else None,
            "ALL": reading(arm, items, ans, sorted(ans)),
        }

    json.dump(out, open(out_path, "w"), indent=1, ensure_ascii=False)
    for arm, rec in out["arms"].items():
        print(f"=== arm {arm}: dispatched {rec['workers_dispatched']}, "
              f"void under K3 {rec['workers_void_under_K3']}")
        for tag in ("K3", "ALL"):
            r = rec[tag]
            if not r:
                print(f"    {tag}: not scorable")
                continue
            line = (f"    {tag} ({len(r['workers'])} workers): majority matches reference on "
                    f"{r['majority_matches_reference']} of {r['n_cases']}, ties "
                    f"{r['majority_is_a_tie']}, kappa(items) = {r['fleiss_kappa_items']}")
            if arm == "B":
                line += (f"; classes {r['classes_majority_matches_reference']}/{r['n_classes']}"
                         f", kappa(classes) = {r['fleiss_kappa_classes']}")
            print(line)
            print(f"        unanimous against reference: {r['unanimous_against_reference']}")


if __name__ == "__main__":
    main()
