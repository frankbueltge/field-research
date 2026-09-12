#!/usr/bin/env python3
"""Score the identification task against the frozen screen and against the model-free instrument.

Session 158, cycle 003. Predictions, falsifiers and kill conditions are fixed by
artifacts/cycle-003/2026-09-12-what-a-description-is-for/PREREGISTRATION.md §3-§4 and are read
from this file's constants, which restate them verbatim.

This file joins labels that already exist. It never produces a label, and it is written so that
running it before the labels exist fails loudly rather than inventing anything.

No model is called anywhere in this file. Standard library only.

Usage:
    python3 tools/identify/score.py --cache /path/to/cache --labels /path/to/labels-dir
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hollow"))
import hollow  # noqa: E402

OUT = "artifacts/cycle-003/2026-09-12-what-a-description-is-for/data"
CHANCE = 0.20

ARM_SHEETS = ["atlas-masked", "atlas-unmasked", "uk-masked"]


def binom_sf(k: int, n: int, p: float) -> float:
    """P(X >= k) for X ~ Binomial(n, p). Exact, standard library."""
    return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def pct(k, n):
    return round(100.0 * k / n, 2) if n else None


def ci(k, n):
    lo, hi = hollow.wilson(k, n)
    return [round(100 * lo, 2), round(100 * hi, 2)]


def load_recs(cache: str, arm: str) -> dict:
    path = os.path.join(cache, f"{arm}-recs.jsonl")
    out = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                r = json.loads(line)
                out[r["id"]] = r
    return out


def join(sheet_label: str, labels_dir: str, keys: dict, recs: dict) -> list[dict]:
    lab_path = os.path.join(labels_dir, f"labels-{sheet_label}.json")
    if not os.path.exists(lab_path):
        raise SystemExit(f"NO LABELS FOR {sheet_label}: {lab_path} does not exist")
    doc = json.load(open(lab_path, encoding="utf-8"))
    by_item = {}
    for rec in doc["labels"]:
        if rec["item"] in by_item:
            raise SystemExit(f"DUPLICATE ITEM {rec['item']} in {sheet_label}")
        by_item[rec["item"]] = rec["answer"]
    key = keys[sheet_label]
    if len(by_item) != len(key):
        raise SystemExit(f"LABEL COUNT MISMATCH {sheet_label}: {len(by_item)} vs {len(key)}")
    rows = []
    for k in key:
        if k["item"] not in by_item:
            raise SystemExit(f"MISSING ITEM {k['item']} in {sheet_label}")
        ans = by_item[k["item"]]
        cannot = (ans == "cannot_tell")
        if not cannot and not (isinstance(ans, int) and 1 <= ans <= 5):
            raise SystemExit(f"BAD ANSWER {ans!r} for item {k['item']} in {sheet_label}")
        r = recs[k["id"]]
        rows.append({
            "item": k["item"], "id": k["id"], "answer": ans,
            "correct_index": k["correct_index"],
            "cannot_tell": cannot,
            "correct": (not cannot) and ans == k["correct_index"],
            "hollow_broad": r["hollow_broad"], "hollow_strict": r["hollow_strict"],
            "r5_title_echo": r["r5_title_echo"],
            "identifies_uniquely": r["identifies_uniquely"],
            "narrowing_set_size": r["narrowing_set_size"],
            "masked_token_count": r["masked_token_count"],
        })
    return rows


def arm_stats(rows: list[dict]) -> dict:
    n = len(rows)
    ok = sum(1 for r in rows if r["correct"])
    ct = sum(1 for r in rows if r["cannot_tell"])
    fl = [r for r in rows if r["hollow_broad"]]
    un = [r for r in rows if not r["hollow_broad"]]
    fk = sum(1 for r in fl if r["correct"])
    uk_ = sum(1 for r in un if r["correct"])

    # the screen scored against the task: "uninformative" == the reader picked wrong
    tp = sum(1 for r in rows if r["hollow_broad"] and not r["correct"])
    fp = sum(1 for r in rows if r["hollow_broad"] and r["correct"])
    fn = sum(1 for r in rows if not r["hollow_broad"] and not r["correct"])
    tn = sum(1 for r in rows if not r["hollow_broad"] and r["correct"])
    kappa = hollow.cohen_kappa([1 if r["hollow_broad"] else 0 for r in rows],
                               [0 if r["correct"] else 1 for r in rows])
    return {
        "n": n,
        "accuracy_pct": pct(ok, n), "accuracy_ci": ci(ok, n), "correct": ok,
        "cannot_tell": ct, "cannot_tell_pct": pct(ct, n),
        "flagged": {"n": len(fl), "correct": fk, "accuracy_pct": pct(fk, len(fl)),
                    "accuracy_ci": ci(fk, len(fl)) if fl else None,
                    "p_vs_chance": round(binom_sf(fk, len(fl), CHANCE), 6) if fl else None},
        "unflagged": {"n": len(un), "correct": uk_, "accuracy_pct": pct(uk_, len(un)),
                      "accuracy_ci": ci(uk_, len(un)) if un else None,
                      "p_vs_chance": round(binom_sf(uk_, len(un), CHANCE), 6) if un else None},
        "gap_points": (round(pct(uk_, len(un)) - pct(fk, len(fl)), 2)
                       if fl and un else None),
        "screen_vs_task": {
            "flagged_and_wrong": tp, "flagged_but_right": fp,
            "unflagged_and_wrong": fn, "unflagged_and_right": tn,
            "agreement_pct": pct(tp + tn, n),
            "cohen_kappa": round(kappa, 4),
            "precision": round(tp / (tp + fp), 4) if (tp + fp) else None,
            "recall": round(tp / (tp + fn), 4) if (tp + fn) else None,
        },
    }


def narrowing_vs_task(rows: list[dict]) -> dict:
    a = [0 if r["identifies_uniquely"] else 1 for r in rows]
    b = [0 if r["correct"] else 1 for r in rows]
    tp = sum(1 for x, y in zip(a, b) if x == 1 and y == 1)
    fp = sum(1 for x, y in zip(a, b) if x == 1 and y == 0)
    fn = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    tn = sum(1 for x, y in zip(a, b) if x == 0 and y == 0)
    return {"not_unique_and_wrong": tp, "not_unique_but_right": fp,
            "unique_and_wrong": fn, "unique_and_right": tn,
            "n_not_unique": tp + fp,
            "agreement_pct": pct(tp + tn, len(rows)),
            "cohen_kappa": round(hollow.cohen_kappa(a, b), 4),
            "precision": round(tp / (tp + fp), 4) if (tp + fp) else None,
            "recall": round(tp / (tp + fn), 4) if (tp + fn) else None}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True)
    ap.add_argument("--labels", required=True)
    args = ap.parse_args()

    census = json.load(open(os.path.join(OUT, "census.json"), encoding="utf-8"))
    keys = json.load(open(os.path.join(OUT, "sheet-key.json"), encoding="utf-8"))
    recs = {"atlas": load_recs(args.cache, "atlas"), "uk": load_recs(args.cache, "uk")}

    rows = {
        "atlas-masked": join("atlas-masked", args.labels, keys, recs["atlas"]),
        "atlas-unmasked": join("atlas-unmasked", args.labels, keys, recs["atlas"]),
        "uk-masked": join("uk-masked", args.labels, keys, recs["uk"]),
    }
    stats = {k: arm_stats(v) for k, v in rows.items()}

    # the two home arms must be the same 60 records in the same order (PREREGISTRATION §2.3)
    if [r["id"] for r in rows["atlas-masked"]] != [r["id"] for r in rows["atlas-unmasked"]]:
        raise SystemExit("HOME ARMS DIVERGED: masked and unmasked rows are not the same records")

    hm, hu, uu = stats["atlas-masked"], stats["atlas-unmasked"], stats["uk-masked"]

    # --- kill conditions (PREREGISTRATION §4) ---
    sheet_m = {k: json.load(open(os.path.join(OUT, f"sheet-{k}.json"), encoding="utf-8"))
               for k in ARM_SHEETS}
    import re
    TOK = re.compile(r"[^\W_]{3,}")
    k2 = {}
    for k, sh in sheet_m.items():
        few = sum(1 for i in sh["items"] if len(TOK.findall(i["value"])) < 3)
        k2[k] = {"under_3_tokens": few, "pct": pct(few, len(sh["items"])), "fired": pct(few, len(sh["items"])) >= 25.0}
    kills = {
        "K1": {"condition": "home masked, UNFLAGGED accuracy < 40 %",
               "value_pct": hm["unflagged"]["accuracy_pct"],
               "fired": hm["unflagged"]["accuracy_pct"] < 40.0},
        "K2": {"condition": ">= 25 % of sampled masked values retain fewer than 3 tokens",
               "arms": k2, "fired": any(v["fired"] for v in k2.values())},
        "K3": {"condition": "a reader answers cannot_tell on >= 20 % of an arm's items",
               "arms": {k: {"pct": v["cannot_tell_pct"], "fired": v["cannot_tell_pct"] >= 20.0}
                        for k, v in stats.items()},
               "fired": any(v["cannot_tell_pct"] >= 20.0 for v in stats.values())},
        "K4": {"condition": "data.gov.uk notes non-empty on < 80 % of records",
               "value_pct": census["census"]["uk"]["declared_completeness_pct"],
               "fired": census["census"]["uk"]["declared_completeness_pct"] < 80.0},
    }

    # --- predictions (PREREGISTRATION §3) ---
    p = {}
    p["P1"] = {"statement": "home, masked: reader accuracy on FLAGGED items <= 40 % (<= 2x chance)",
               "value_pct": hm["flagged"]["accuracy_pct"], "n": hm["flagged"]["n"],
               "verdict": "confirmed" if hm["flagged"]["accuracy_pct"] <= 40.0 else "refuted"}
    p["P2"] = {"statement": "home, masked: reader accuracy on UNFLAGGED items >= 70 %",
               "value_pct": hm["unflagged"]["accuracy_pct"], "n": hm["unflagged"]["n"],
               "verdict": "confirmed" if hm["unflagged"]["accuracy_pct"] >= 70.0 else "refuted"}
    prec = hm["screen_vs_task"]["precision"]
    p["P3"] = {"statement": "home, masked: screen precision against the task > 0.30 "
                            "(0.129 against the emptiness question, 2026-09-11)",
               "precision": prec, "prior_2026_09_11": 0.129,
               "verdict": "confirmed" if (prec is not None and prec > 0.30) else "refuted"}
    nvt = narrowing_vs_task(rows["atlas-masked"])
    p["P4"] = {"statement": "home: kappa between 'not identifies_uniquely' and 'reader wrong' >= 0.30",
               "kappa": nvt["cohen_kappa"], "detail": nvt,
               "verdict": "confirmed" if nvt["cohen_kappa"] >= 0.30 else "refuted"}

    r5_home = [r for r in rows["atlas-masked"] if r["r5_title_echo"]]
    if len(r5_home) < 5:
        p["P5"] = {"statement": "home: accuracy on R5-flagged items falls by >= 30 points "
                                "unmasked -> masked, non-R5 falls by < 15 points",
                   "r5_items_in_sample": len(r5_home),
                   "r5_in_catalogue": census["census"]["atlas"]["screen"]["r5_title_echo"]["n"],
                   "verdict": "not evaluable",
                   "note": "PREREGISTRATION §3 declared in advance: fewer than 5 R5-flagged items "
                           "in the home sample makes P5 not evaluable. R5 fires on 0 of 521 atlas "
                           "values, so no sample could have evaluated it."}
    else:
        def acc(rs):
            return pct(sum(1 for r in rs if r["correct"]), len(rs))
        ids5 = {r["id"] for r in r5_home}
        m5 = [r for r in rows["atlas-masked"] if r["id"] in ids5]
        u5 = [r for r in rows["atlas-unmasked"] if r["id"] in ids5]
        mo = [r for r in rows["atlas-masked"] if r["id"] not in ids5]
        uo = [r for r in rows["atlas-unmasked"] if r["id"] not in ids5]
        d5, do = acc(u5) - acc(m5), acc(uo) - acc(mo)
        p["P5"] = {"statement": "home: R5 drop >= 30 points, non-R5 drop < 15 points",
                   "r5_drop_points": round(d5, 2), "non_r5_drop_points": round(do, 2),
                   "verdict": "confirmed" if (d5 >= 30.0 and do < 15.0) else "refuted"}

    p["P6"] = {"statement": "the flagged/unflagged accuracy gap is SMALLER on data.gov.uk than at home",
               "gap_home_points": hm["gap_points"], "gap_uk_points": uu["gap_points"],
               "verdict": ("confirmed" if (uu["gap_points"] is not None and hm["gap_points"] is not None
                                           and uu["gap_points"] < hm["gap_points"]) else "refuted")}
    nu = census["census"]["atlas"]["narrowing"]
    p["P7"] = {"statement": "census, home: >= 10 % of the atlas's descriptions fail to identify "
                            "their record uniquely",
               "value_pct": nu["not_unique_pct"], "ci": nu["not_unique_ci"],
               "verdict": "confirmed" if nu["not_unique_pct"] >= 10.0 else "refuted"}

    scored = [v for v in p.values() if v["verdict"] in ("confirmed", "refuted")]
    p["_tally"] = {"total": len(p) - 0, "scored": len(scored),
                   "confirmed": sum(1 for v in scored if v["verdict"] == "confirmed"),
                   "refuted": sum(1 for v in scored if v["verdict"] == "refuted"),
                   "not_evaluable": sum(1 for v in p.values() if v.get("verdict") == "not evaluable")}

    # --- declared exploratory, scored on nothing ---
    def acc_of(rs):
        return pct(sum(1 for r in rs if r["correct"]), len(rs))
    ex = {
        "_note": "Declared exploratory. No prediction is scored on anything in this block.",
        "masking_cost_home": {
            "unmasked_accuracy_pct": hu["accuracy_pct"], "masked_accuracy_pct": hm["accuracy_pct"],
            "drop_points": round(hu["accuracy_pct"] - hm["accuracy_pct"], 2),
            "caveat": "BETWEEN readers, not within: the two home arms were read by two independent "
                      "readers (PREREGISTRATION §2.3, §5.4). The drop confounds masking with "
                      "reader variation and nothing here may attribute it to masking alone.",
            "unmasked_flagged_accuracy_pct": hu["flagged"]["accuracy_pct"],
            "unmasked_unflagged_accuracy_pct": hu["unflagged"]["accuracy_pct"],
        },
        "strict_vs_task_home": {
            "flagged_and_wrong": sum(1 for r in rows["atlas-masked"]
                                     if r["hollow_strict"] and not r["correct"]),
            "flagged": sum(1 for r in rows["atlas-masked"] if r["hollow_strict"]),
        },
        "narrowing_vs_task_uk": narrowing_vs_task(rows["uk-masked"]),
        "accuracy_by_narrowing_home": {
            "unique": acc_of([r for r in rows["atlas-masked"] if r["identifies_uniquely"]]),
            "not_unique": acc_of([r for r in rows["atlas-masked"] if not r["identifies_uniquely"]]),
        },
        "accuracy_by_narrowing_uk": {
            "unique": acc_of([r for r in rows["uk-masked"] if r["identifies_uniquely"]]),
            "not_unique": acc_of([r for r in rows["uk-masked"] if not r["identifies_uniquely"]]),
        },
        "narrowing_is_size_dependent": {
            "note": "The narrowing set is an intersection of posting lists in the catalogue itself, "
                    "so a larger catalogue makes unique identification harder for the SAME text. "
                    "Home (N=521) and data.gov.uk (N=67,205) are therefore NOT comparable on "
                    "not_unique_pct. Found by us this session; filed as a defect.",
            "n_home": census["census"]["atlas"]["present"],
            "n_uk": census["census"]["uk"]["present"],
        },
    }

    out = {
        "generated_by": "tools/identify/score.py", "date": "2026-09-12", "session": 158, "cycle": 3,
        "question": "Missing Data Art",
        "preregistration": "artifacts/cycle-003/2026-09-12-what-a-description-is-for/PREREGISTRATION.md",
        "chance_accuracy_pct": CHANCE * 100,
        "arms": stats, "predictions": p, "kill_conditions": kills,
        "narrowing_vs_task_home": nvt, "exploratory": ex,
        "census": census["census"], "manifest": census["manifest"], "params": census["params"],
    }
    json.dump(out, open(os.path.join(OUT, "results.json"), "w"), indent=2, ensure_ascii=False)
    json.dump({k: v for k, v in rows.items()},
              open(os.path.join(OUT, "task-rows.json"), "w"), indent=2, ensure_ascii=False)

    for k, v in stats.items():
        print(f"{k}: acc {v['accuracy_pct']} % (flagged {v['flagged']['accuracy_pct']} % / "
              f"unflagged {v['unflagged']['accuracy_pct']} %), cannot_tell {v['cannot_tell']}, "
              f"precision {v['screen_vs_task']['precision']}, kappa {v['screen_vs_task']['cohen_kappa']}")
    for k, v in p.items():
        if k != "_tally":
            print(f"  {k}: {v['verdict']}")
    print("  kills:", {k: v["fired"] for k, v in kills.items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
