#!/usr/bin/env python3
"""Agreement, oracle and predictions. Session 164, 2026-09-19.

Usage: analyse.py <run.json> <spdx-dir> <out.json>

Nothing here decides a verdict about a licence. It compares verdicts other code
produced, and it counts.
"""
import itertools
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from inputs import FILL_TOKENS                                   # noqa: E402

# A line that opens with a copyright marker. Written for the ORACLE only: it is a
# third hand, not a measuring rung, and it is published so a reader can see what
# the oracle assumed. It decides nothing about any licence — only which entries
# have a fill token sitting on a copyright line.
_OPENS = re.compile(r"^\s*(copyright\b|\(c\)|©|copr\.)", re.I)


def copyright_line_fill(text: str):
    """Fill tokens of §6 that sit on a line opening with a copyright marker."""
    hit = []
    for ln in text.splitlines():
        if not _OPENS.match(ln):
            continue
        for tok in FILL_TOKENS:
            if tok in ln:
                hit.append((ln.strip(), tok))
    return hit


def fam_key(v):
    return None if v is None else tuple(sorted(v["families"]))


def att_key(v):
    return "<missing>" if v is None else v["attribution"]


# Strict oracle of PREREGISTRATION §7: identifier membership in a family.
def is_member(lid: str, fam: str) -> bool:
    return lid == fam or lid in (fam + "-only", fam + "-or-later", fam + "+")


def main():
    run = json.load(open(sys.argv[1]))
    texts = json.load(open(os.path.join(sys.argv[2], "texts.json")))
    out_path = sys.argv[3]

    delivered = [k for k, v in run["delivery"].items() if v["delivered"]]
    indep = [k for k in delivered if k.startswith("I-")]
    rows = run["rows"]
    byarm = {"C": [r for r in rows if r["arm"] == "C"],
             "F": [r for r in rows if r["arm"] == "F"]}

    # ---------------------------------------------------------------- agreement
    compare = [k for k in delivered if k != "R-def"]      # R-def is a control, not a peer
    pairs = {}
    for a, b in itertools.combinations(sorted(compare), 2):
        rec = {}
        for arm in ("C", "F"):
            rs = byarm[arm]
            fam_same = sum(1 for r in rs if fam_key(r[a]) == fam_key(r[b]))
            att_same = sum(1 for r in rs if att_key(r[a]) == att_key(r[b]))
            both = sum(1 for r in rs if fam_key(r[a]) == fam_key(r[b])
                       and att_key(r[a]) == att_key(r[b]))
            rec[arm] = {"n": len(rs), "families_agree": fam_same,
                        "attribution_agree": att_same, "both_agree": both,
                        "families_agree_pct": round(100 * fam_same / len(rs), 2),
                        "both_agree_pct": round(100 * both / len(rs), 2)}
        pairs[f"{a} vs {b}"] = rec

    unanimous = {}
    for arm in ("C", "F"):
        rs = byarm[arm]
        u_f = sum(1 for r in rs if len({fam_key(r[k]) for k in compare}) == 1)
        u_b = sum(1 for r in rs if len({(fam_key(r[k]), att_key(r[k])) for k in compare}) == 1)
        unanimous[arm] = {"n": len(rs), "all_agree_families": u_f, "all_agree_both": u_b,
                          "all_agree_families_pct": round(100 * u_f / len(rs), 2)}

    # ------------------------------------------------- independents among themselves
    indep_internal = {}
    for arm in ("C", "F"):
        rs = byarm[arm]
        dis = sum(1 for r in rs if len({fam_key(r[k]) for k in indep}) > 1
                  or len({att_key(r[k]) for k in indep}) > 1)
        # all independents agree with each other AND differ from R-ship
        block = sum(1 for r in rs
                    if len({(fam_key(r[k]), att_key(r[k])) for k in indep}) == 1
                    and (fam_key(r[indep[0]]), att_key(r[indep[0]]))
                    != (fam_key(r["R-ship"]), att_key(r["R-ship"])))
        indep_internal[arm] = {"n": len(rs), "independents_disagree_internally": dis,
                               "independents_unanimous_against_R_ship": block}

    # ------------------------------------------------------- majority against R-ship
    majority = []
    for r in rows:
        theirs = [(fam_key(r[k]), att_key(r[k])) for k in indep]
        mine = (fam_key(r["R-ship"]), att_key(r["R-ship"]))
        counts = {}
        for t in theirs:
            counts[t] = counts.get(t, 0) + 1
        top, n = max(counts.items(), key=lambda kv: kv[1])
        if n > len(indep) / 2 and top != mine:
            majority.append({"id": r["id"], "arm": r["arm"], "n_agreeing": n,
                             "independents": {"families": list(top[0] or ()),
                                              "attribution": top[1]},
                             "R_ship": {"families": list(mine[0] or ()),
                                        "attribution": mine[1]}})

    # ---------------------------------------------------------------- strict oracle
    oracle = {}
    for k in compare:
        pos = nonmember = 0
        offenders = {}
        for r in byarm["C"]:
            v = r[k]
            if not v:
                continue
            for f in v["families"]:
                pos += 1
                if not is_member(r["id"], f):
                    nonmember += 1
                    offenders.setdefault(f, []).append(r["id"])
        oracle[k] = {"positive_identifications": pos,
                     "on_member_ids": pos - nonmember,
                     "not_member_unadjudicated": nonmember,
                     "member_pct": round(100 * (pos - nonmember) / pos, 2) if pos else None,
                     "by_family": {f: sorted(v) for f, v in sorted(offenders.items())}}

    # --------------------------------------------- L2 paired transition (ground truth)
    fills = {lid: copyright_line_fill(texts[lid]) for lid in texts}
    fill_ids = sorted(lid for lid, h in fills.items() if h)
    cmap = {r["id"]: r for r in byarm["C"]}
    fmap = {r["id"]: r for r in byarm["F"]}
    transition = {}
    for k in compare + (["R-def"] if "R-def" in delivered else []):
        scored = ok = missed = other = 0
        misses = []
        for lid in fill_ids:
            c, f = cmap[lid][k], fmap[lid][k]
            if c is None or f is None:
                continue
            if c["attribution"] is None and f["attribution"] is None:
                continue                                   # family not scored by this rule
            scored += 1
            if c["attribution"] == "placeholder" and f["attribution"] == "named":
                ok += 1
            elif c["attribution"] == f["attribution"]:
                missed += 1
                misses.append({"id": lid, "verdict_both_arms": c["attribution"],
                               "line": fills[lid][0][0][:160], "token": fills[lid][0][1]})
            else:
                other += 1
                misses.append({"id": lid, "C": c["attribution"], "F": f["attribution"],
                               "line": fills[lid][0][0][:160], "token": fills[lid][0][1]})
        transition[k] = {"scored": scored, "placeholder_then_named": ok,
                         "same_verdict_both_arms": missed, "other": other,
                         "pct_correct": round(100 * ok / scored, 2) if scored else None,
                         "failures": misses[:40]}

    # ------------------------------------------------------------------ the MIT probe
    mit = {k: {"C": cmap["MIT"][k], "F": fmap["MIT"][k]} for k in delivered}

    result = {
        "note": "Session 164. Agreement between implementations of one specification.",
        "license_list_version": run["license_list_version"],
        "corpus_digest": run["corpus_digest"],
        "delivered": delivered, "independents": indep,
        "compare_set": sorted(compare),
        "pairwise": pairs, "unanimous": unanimous,
        "independents_internal": indep_internal,
        "majority_against_R_ship": majority,
        "n_majority_against_R_ship": len(majority),
        "strict_oracle": oracle,
        "l2_transition": transition,
        "n_fill_ids": len(fill_ids),
        "mit_probe": mit,
    }
    json.dump(result, open(out_path, "w"), indent=1)
    print(json.dumps({k: v for k, v in result.items()
                      if k in ("delivered", "unanimous", "independents_internal",
                               "n_majority_against_R_ship", "n_fill_ids")}, indent=1))


if __name__ == "__main__":
    main()
