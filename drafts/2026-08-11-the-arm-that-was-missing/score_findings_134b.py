#!/usr/bin/env python3
"""Score `PREREGISTRATION-134.md` on the REPAIRED population, and measure the adversary's own attack.

Session 134, 2026-08-24, written after `VERIFIER-134.md` and `INTERLOCUTOR-134.md` returned and
after both of the Verifier's blocking findings and the Interlocutor's charge 2 were acted on.
It supersedes `score_findings_134.py`, which stands unedited as the state the two roles read.

WHAT CHANGED, and every one of these is somebody else's finding, not this practice's second thought:
  * the population is `findings-134c.json` -- 124 findings from ELEVEN files, not 102 from ten
    (`VERIFIER-134.md` blocking 2: the first extractor required digit-only row ids and dropped
    `CONDITIONS-122.md`'s twenty-two findings in silence);
  * role attribution no longer resolves a two-role cell by first-match-wins; six such cells are
    JOINT and are counted as neither role (`INTERLOCUTOR-134.md` charge 2);
  * findings are keyed `file#row`, not by position, so a population repair cannot silently move a
    label from one finding to another;
  * the labels are two rounds by four classifiers -- the original 102 by two, the 22 recovered
    findings by two others -- and the rounds are reported SEPARATELY as well as pooled, because
    two rounds by different readers is not one reliability figure;
  * a SENSITIVITY PASS runs the adversary's own two lists (`interlocutor-134-lists.json`, taken
    from `INTERLOCUTOR-134.md` charge 4) against the per-role rates, to measure how far the rate
    comparison moves under a hostile but defensible re-reading. This session withdrew that
    comparison on the strength of what this pass returns.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LABELS = ("A", "B", "C", "D", "E")


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as fh:
        return json.load(fh)


def rates(keys_a, universe, recs):
    """A-count and rate per role over `universe`, where `keys_a` are the class-A keys."""
    out = {}
    for k in universe:
        role = recs[k]["role"]
        d = out.setdefault(role, {"n": 0, "a": 0})
        d["n"] += 1
        if k in keys_a:
            d["a"] += 1
    for d in out.values():
        d["rate"] = d["a"] / d["n"] if d["n"] else None
    return dict(sorted(out.items()))


def main():
    pop = load("findings-134c.json")
    recs = {r["key"]: r for r in pop["records"]}
    idmap = load("round2-idmap.json")           # round-2 F-id -> key
    lists = load("interlocutor-134-lists.json")

    # ---- assemble the two label rounds, both keyed -------------------------
    r1a = load("labels-134-A.keyed.json")["labels"]
    r1b = load("labels-134-B.keyed.json")["labels"]
    r2c = {idmap[i]: v for i, v in load("labels-134-C-round2.json")["labels"].items() if i in idmap}
    r2d = {idmap[i]: v for i, v in load("labels-134-D-round2.json")["labels"].items() if i in idmap}

    rounds = {
        "round1": {"classifiers": ["A", "B"], "x": r1a, "y": r1b},
        "round2": {"classifiers": ["C", "D"], "x": r2c, "y": r2d},
    }
    per_round = {}
    for name, r in rounds.items():
        both = sorted(set(r["x"]) & set(r["y"]))
        agree = [k for k in both if r["x"][k]["label"] == r["y"][k]["label"]]
        per_round[name] = {
            "classifiers": r["classifiers"],
            "n": len(both),
            "raw_agreement": len(agree) / len(both) if both else None,
            "a_agreed": sorted(k for k in both
                               if r["x"][k]["label"] == "A" and r["y"][k]["label"] == "A"),
            "e_either": sorted(k for k in both
                               if "E" in (r["x"][k]["label"], r["y"][k]["label"])),
        }

    universe = sorted(set(r1a) & set(r1b) | (set(r2c) & set(r2d)))
    a_agreed = sorted(set(per_round["round1"]["a_agreed"]) | set(per_round["round2"]["a_agreed"]))
    e_either = sorted(set(per_round["round1"]["e_either"]) | set(per_round["round2"]["e_either"]))
    pooled_agree = sum(len(v["a_agreed"]) for v in per_round.values())  # unused; kept explicit
    del pooled_agree

    n_agree = sum(int(v["raw_agreement"] * v["n"] + 0.5) for v in per_round.values())
    pooled_agreement = n_agree / len(universe) if universe else None

    # ---- K1/K2/K3 ----------------------------------------------------------
    k1 = {name: {"value": v["raw_agreement"], "failed": v["raw_agreement"] < 0.60}
          for name, v in per_round.items()}
    k1["pooled"] = {"value": pooled_agreement, "failed": pooled_agreement < 0.60}
    attributed = [k for k in universe if recs[k]["role"] not in ("UNATTRIBUTED", "OTHER")
                  and not recs[k]["role"].startswith("JOINT")]
    k2_failed = len(attributed) < 20
    k3_failed = (len(e_either) / len(universe)) > (1 / 3) if universe else True

    # ---- P1: the exclusivity claim ----------------------------------------
    non_panel = [k for k in a_agreed if recs[k]["role"] != "READER_PANEL"
                 and not recs[k]["role"].startswith("JOINT")]
    p1_refuted = len(non_panel) > 0
    # the subset the adversary itself certified as surviving hostile reading
    solid = [k for k in lists["solid"] if k in a_agreed]
    solid_non_panel = [k for k in solid if recs[k]["role"] != "READER_PANEL"
                       and not recs[k]["role"].startswith("JOINT")]

    # ---- P2 ----------------------------------------------------------------
    classifiable = [k for k in universe if k not in e_either]
    a_share = len([k for k in classifiable if k in a_agreed]) / len(classifiable) if classifiable else None

    # ---- P4 and the sensitivity pass this session withdrew it on -----------
    base = rates(set(a_agreed), classifiable, recs)
    pruned_keys = set(a_agreed) - set(lists["contested"])
    pruned = rates(pruned_keys, classifiable, recs)
    half = set(a_agreed) - set(lists["contested"][:len(lists["contested"]) // 2])
    half_pruned = rates(half, classifiable, recs)

    def rank(table):
        cand = {r: v for r, v in table.items()
                if v["n"] >= 5 and not r.startswith("JOINT") and r not in ("OTHER", "UNATTRIBUTED")}
        return sorted(cand, key=lambda r: -cand[r]["rate"]) if cand else []

    result = {
        "generated_by": "score_findings_134b.py",
        "supersedes": "score_findings_134.py and score-134.json",
        "preregistration": "PREREGISTRATION-134.md",
        "acted_on": ["VERIFIER-134.md blocking 1 and 2", "INTERLOCUTOR-134.md charges 1, 2, 3, 4, 8"],
        "population": {"file": "findings-134c.json", "n": pop["n_findings"],
                       "files": pop["files_with_finding_tables"], "by_role": pop["by_role"],
                       "sha256_of_payload": hashlib.sha256(
                           json.dumps(pop, sort_keys=True, ensure_ascii=False).encode()).hexdigest()},
        "rounds": per_round,
        "kill_conditions": {"K1": k1, "K2": {"attributed": len(attributed), "failed": k2_failed},
                            "K3": {"e_either": len(e_either), "of": len(universe),
                                   "failed": k3_failed, "keys": e_either},
                            "K4": "no significance test is computed anywhere in this script",
                            "K5": "the disposition column was never shown to any classifier"},
        "P1_exclusivity": {
            "refuted": p1_refuted,
            "n_non_panel_A": len(non_panel),
            "non_panel_A": [{"key": k, "role": recs[k]["role"],
                             "finding": recs[k]["finding"][:200]} for k in non_panel],
            "certified_by_the_adversary": {
                "n": len(solid_non_panel), "keys": solid_non_panel,
                "note": "the subset INTERLOCUTOR-134.md charge 4 names as surviving a hostile "
                        "reading with no real argument against A"},
        },
        "P2_minority": {"a_share": a_share, "held": a_share is not None and a_share < 0.25,
                        "denominator": len(classifiable)},
        "P4_rate_comparison": {
            "STATUS": "WITHDRAWN BY THIS SESSION -- see INCREMENT-22.md. The table below is "
                      "published as the evidence for the withdrawal, not as a result.",
            "base": base, "base_ranking": rank(base),
            "all_contested_pruned": pruned, "pruned_ranking": rank(pruned),
            "half_contested_pruned": half_pruned, "half_ranking": rank(half_pruned),
            "contested_list_source": "INTERLOCUTOR-134.md charge 4",
        },
    }
    with open(os.path.join(HERE, "score-134b.json"), "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, ensure_ascii=False)

    print(f"population {pop['n_findings']} from {len(pop['files_with_finding_tables'])} files")
    for name, v in per_round.items():
        print(f"  {name}: n={v['n']} agreement={v['raw_agreement']:.4f} A={len(v['a_agreed'])}")
    print(f"pooled agreement {pooled_agreement:.4f}   E either {len(e_either)}/{len(universe)}")
    print(f"P1 refuted: {p1_refuted}  non-panel A: {len(non_panel)}  "
          f"adversary-certified non-panel A: {len(solid_non_panel)}")
    print(f"P2 A share {a_share:.4f} of {len(classifiable)} -> held={a_share < 0.25}")
    print("P4 rate comparison (WITHDRAWN; printed as evidence for the withdrawal):")
    for label, table in (("base", base), ("half pruned", half_pruned), ("all pruned", pruned)):
        row = "  ".join(f"{r}={table[r]['a']}/{table[r]['n']}"
                        for r in ("INTERLOCUTOR", "VERIFIER", "READER_PANEL") if r in table)
        print(f"    {label:<12} {row}   ranking={rank(table)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
