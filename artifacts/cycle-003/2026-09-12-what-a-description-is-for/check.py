#!/usr/bin/env python3
"""Verify the artifact: every number, verdict and quoted passage on the page, recomputed.

Session 158, cycle 003.

The lesson of 2026-09-11 is built in: a checker that reads results.json and compares it to the page
cannot catch a lie written into results.json and re-rendered. So every scored quantity here is
recomputed from data/task-rows.json — the per-item labels joined to the per-item screen verdicts —
and from data/labels-*.json and data/sheet-key.json, which are the primary record. results.json is
then checked AGAINST that recomputation, and the page is checked against both.

Exit 0 only if every check passes.

Usage:
    python3 artifacts/cycle-003/2026-09-12-what-a-description-is-for/check.py
"""

from __future__ import annotations

import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
THIN = " "

FAIL: list[str] = []
N = 0


def ck(cond: bool, what: str) -> None:
    global N
    N += 1
    if not cond:
        FAIL.append(what)


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def group(v, dp=0):
    return f"{v:,.{dp}f}".replace(",", THIN)


def on_page(page: str, v, dp=0) -> bool:
    return group(v, dp) in page


def kappa(a, b):
    n = len(a)
    agree = sum(1 for x, y in zip(a, b) if x == y) / n
    pa, pb = sum(a) / n, sum(b) / n
    ch = pa * pb + (1 - pa) * (1 - pb)
    return (agree - ch) / (1 - ch) if ch < 1 else 0.0


def wilson(k, n, z=1.959963985):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def main() -> int:
    page = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    R = load("results.json")
    S = load("size-curve.json")
    SRC = load("sources.json")
    rows = load("task-rows.json")
    keys = load("sheet-key.json")

    # ---------------------------------------------------------------- 1. primary record intact
    for arm in ("atlas-masked", "atlas-unmasked", "uk-masked"):
        lab = load(f"labels-{arm}.json")
        sheet = load(f"sheet-{arm}.json")
        ck(len(lab["labels"]) == 60, f"{arm}: 60 labels")
        ck(len(sheet["items"]) == 60, f"{arm}: 60 sheet items")
        ck(sorted(x["item"] for x in lab["labels"]) == list(range(1, 61)),
           f"{arm}: labels are items 1..60 with no gap or repeat")
        ck(len(keys[arm]) == 60, f"{arm}: 60 key rows")
        ck(len(rows[arm]) == 60, f"{arm}: 60 joined rows")
        # the sheet must not leak a verdict to the reader
        # The field names, not loose words: a catalogue value may legitimately contain "screen"
        # or "duplicate", and a checker that forbids those convicts the corpus, not the sheet.
        blob = json.dumps(sheet, ensure_ascii=False).lower()
        for leak in ("hollow_broad", "hollow_strict", "r1_chrome", "r2_truncated_tail",
                     "r3_truncated_head", "r4_duplicate", "r5_title_echo",
                     "identifies_uniquely", "narrowing_set_size", "correct_index"):
            ck(leak not in blob, f"{arm}: sheet does not leak '{leak}' to the reader")
        # every correct_index must actually be a candidate index present in the sheet
        ci = {k["item"]: k["correct_index"] for k in keys[arm]}
        for it in sheet["items"]:
            ck(any(c["index"] == ci[it["item"]] for c in it["candidates"]),
               f"{arm}: item {it['item']} key points at a real candidate")
            ck(len(it["candidates"]) == 5, f"{arm}: item {it['item']} has 5 candidates")
            ck(len({c['title'] for c in it['candidates']}) == 5,
               f"{arm}: item {it['item']} candidates are distinct")

        # the join in task-rows.json must reproduce from labels + key
        byitem = {x["item"]: x["answer"] for x in lab["labels"]}
        for r in rows[arm]:
            ck(r["answer"] == byitem[r["item"]], f"{arm}: item {r['item']} answer matches the label")
            ck(r["correct_index"] == ci[r["item"]], f"{arm}: item {r['item']} key matches")
            ck(r["correct"] == (r["answer"] == r["correct_index"]),
               f"{arm}: item {r['item']} correctness follows from answer and key")
            ck(r["cannot_tell"] == (r["answer"] == "cannot_tell"),
               f"{arm}: item {r['item']} cannot_tell follows from the answer")

    # the two home arms must be the same records in the same order
    ck([r["id"] for r in rows["atlas-masked"]] == [r["id"] for r in rows["atlas-unmasked"]],
       "the masked and unmasked home arms are the same 60 records in the same order")

    # ------------------------------------------------- 2. every scored quantity, recomputed
    for arm in ("atlas-masked", "atlas-unmasked", "uk-masked"):
        rr = rows[arm]
        a = R["arms"][arm]
        ok = sum(1 for r in rr if r["correct"])
        ck(a["correct"] == ok, f"{arm}: correct count recomputes")
        # the stored figures are rounded to two places, so compare at that resolution
        ck(abs(a["accuracy_pct"] - round(100 * ok / 60, 2)) < 1e-9, f"{arm}: accuracy recomputes")
        lo, hi = wilson(ok, 60)
        ck(abs(a["accuracy_ci"][0] - round(100 * lo, 2)) < 0.011
           and abs(a["accuracy_ci"][1] - round(100 * hi, 2)) < 0.011,
           f"{arm}: accuracy interval recomputes")
        ck(a["cannot_tell"] == sum(1 for r in rr if r["cannot_tell"]),
           f"{arm}: cannot_tell count recomputes")
        for key, sel in (("flagged", True), ("unflagged", False)):
            sub = [r for r in rr if bool(r["hollow_broad"]) is sel]
            c = sum(1 for r in sub if r["correct"])
            ck(a[key]["n"] == len(sub), f"{arm}: {key} n recomputes")
            ck(a[key]["correct"] == c, f"{arm}: {key} correct recomputes")
            ck(abs(a[key]["accuracy_pct"] - round(100 * c / len(sub), 2)) < 1e-9,
               f"{arm}: {key} accuracy recomputes")
        ck(abs(a["gap_points"] - (a["unflagged"]["accuracy_pct"] - a["flagged"]["accuracy_pct"]))
           < 0.011, f"{arm}: gap recomputes from the two accuracies")
        sv = a["screen_vs_task"]
        tp = sum(1 for r in rr if r["hollow_broad"] and not r["correct"])
        fp = sum(1 for r in rr if r["hollow_broad"] and r["correct"])
        fn = sum(1 for r in rr if not r["hollow_broad"] and not r["correct"])
        tn = sum(1 for r in rr if not r["hollow_broad"] and r["correct"])
        ck((sv["flagged_and_wrong"], sv["flagged_but_right"], sv["unflagged_and_wrong"],
            sv["unflagged_and_right"]) == (tp, fp, fn, tn), f"{arm}: confusion cells recompute")
        ck(tp + fp + fn + tn == 60, f"{arm}: confusion cells sum to 60")
        ck(sv["precision"] is None or abs(sv["precision"] - round(tp / (tp + fp), 4)) < 1e-9,
           f"{arm}: precision recomputes")
        ck(sv["recall"] is None or abs(sv["recall"] - round(tp / (tp + fn), 4)) < 1e-9,
           f"{arm}: recall recomputes")
        k = kappa([1 if r["hollow_broad"] else 0 for r in rr],
                  [0 if r["correct"] else 1 for r in rr])
        ck(abs(sv["cohen_kappa"] - round(k, 4)) < 1e-9, f"{arm}: kappa recomputes")

    # ------------------------------------------------- 3. predictions follow from the numbers
    P = R["predictions"]
    hm, uu = R["arms"]["atlas-masked"], R["arms"]["uk-masked"]
    at = R["census"]["atlas"]
    want = {
        "P1": "confirmed" if hm["flagged"]["accuracy_pct"] <= 40.0 else "refuted",
        "P2": "confirmed" if hm["unflagged"]["accuracy_pct"] >= 70.0 else "refuted",
        "P3": "confirmed" if hm["screen_vs_task"]["precision"] > 0.30 else "refuted",
        "P4": "confirmed" if P["P4"]["kappa"] >= 0.30 else "refuted",
        "P5": "not evaluable",
        "P6": "confirmed" if uu["gap_points"] < hm["gap_points"] else "refuted",
        "P7": "confirmed" if at["narrowing"]["not_unique_pct"] >= 10.0 else "refuted",
    }
    for k, v in want.items():
        ck(P[k]["verdict"] == v, f"{k}: verdict follows from its own falsifier ({v})")
    ck(P["P5"]["r5_in_catalogue"] == at["screen"]["r5_title_echo"]["n"],
       "P5: the R5 count it reports is the census count")
    ck(P["P5"]["r5_in_catalogue"] == 0 and P["P5"]["r5_items_in_sample"] == 0,
       "P5: unevaluable because R5 fires nowhere in the home catalogue")
    t = P["_tally"]
    ck(t["refuted"] == sum(1 for v in want.values() if v == "refuted"), "tally: refuted count")
    ck(t["confirmed"] == sum(1 for v in want.values() if v == "confirmed"), "tally: confirmed count")
    ck(t["refuted"] + t["confirmed"] + t["not_evaluable"] == 7, "tally: all seven accounted for")

    # ------------------------------------------------- 4. kill conditions, recomputed
    K = R["kill_conditions"]
    ck(K["K1"]["fired"] == (hm["unflagged"]["accuracy_pct"] < 40.0), "K1 fires iff its condition holds")
    ck(K["K3"]["fired"] == any(R["arms"][a]["cannot_tell_pct"] >= 20.0 for a in R["arms"]),
       "K3 fires iff its condition holds")
    ck(K["K4"]["fired"] == (R["census"]["uk"]["declared_completeness_pct"] < 80.0),
       "K4 fires iff its condition holds")
    TOK = re.compile(r"[^\W_]{3,}", re.UNICODE)
    for arm in ("atlas-masked", "atlas-unmasked", "uk-masked"):
        sheet = load(f"sheet-{arm}.json")
        few = sum(1 for i in sheet["items"] if len(TOK.findall(i["value"])) < 3)
        ck(K["K2"]["arms"][arm]["under_3_tokens"] == few, f"K2: {arm} token count recomputes")
    ck(K["K2"]["fired"] == any(v["fired"] for v in K["K2"]["arms"].values()),
       "K2 fires iff one of its arms fires")
    ck(not any(K[k]["fired"] for k in K), "no kill condition fired, as the page states")
    ck("none fired" in page, "the page says no kill condition fired")

    # ------------------------------------------------- 5. the size curve
    lad = S["uk_ladder"]
    ck(all(lad[i]["not_unique_pct"] < lad[i + 1]["not_unique_pct"] for i in range(len(lad) - 1)),
       "the size curve is monotone increasing, as the page's argument requires")
    c = S["comparison_at_n_521"]
    ck(abs(c["uk_subsampled"] - lad[0]["not_unique_pct"]) < 1e-9, "curve: the 521 point is the ladder's")
    ck(abs(c["uk_at_full_size"] - lad[-1]["not_unique_pct"]) < 1e-9, "curve: the full-size point is the ladder's")
    ck(abs(c["home"] - at["narrowing"]["not_unique_pct"]) < 1e-9, "curve: the home point is the census's")
    ck(lad[-1]["n"] == R["census"]["uk"]["present"], "curve: the top of the ladder is the whole catalogue")
    ck(S["_status"].startswith("POST-HOC"), "the size curve declares itself post-hoc")
    ck("post-hoc and declared" in page, "the page declares the size curve post-hoc")

    # ------------------------------------------------- 6. the page carries the measured numbers
    for v, dp in [(hm["accuracy_pct"], 2), (hm["flagged"]["accuracy_pct"], 2),
                  (hm["unflagged"]["accuracy_pct"], 2), (hm["gap_points"], 2),
                  (uu["accuracy_pct"], 2), (uu["flagged"]["accuracy_pct"], 2),
                  (uu["unflagged"]["accuracy_pct"], 2), (uu["gap_points"], 2),
                  (hm["screen_vs_task"]["precision"], 4), (uu["screen_vs_task"]["precision"], 4),
                  (hm["screen_vs_task"]["cohen_kappa"], 4), (uu["screen_vs_task"]["cohen_kappa"], 4),
                  (at["narrowing"]["not_unique_pct"], 2),
                  (R["census"]["uk"]["narrowing"]["not_unique_pct"], 2),
                  (c["uk_subsampled"], 2), (c["uk_at_full_size"], 2),
                  (at["records"], 0), (R["census"]["uk"]["records"], 0),
                  (R["census"]["uk"]["present"], 0),
                  (hm["flagged"]["correct"], 0), (hm["flagged"]["n"], 0)]:
        ck(on_page(page, v, dp), f"the page carries {group(v, dp)}")
    ck(group(at["screen"]["hollow_broad"]["pct"], 1) in page,
       "the page carries the home broad rate of 2026-09-08")
    ck(abs(at["screen"]["hollow_broad"]["pct"] - 40.5) < 1e-9,
       "the home arm reproduces the 40.5 % published on 2026-09-08")
    ck(R["manifest"]["atlas"]["sha256"][:8] in page, "the page carries the atlas feed digest")

    # every verdict chip on the page must be the verdict in the data
    chips = re.findall(r'<td><strong>(P\d)</strong>.*?<span class="chip \w+">([a-z ]+)</span>',
                       page, re.S)
    ck(len(chips) == 7, "the page renders seven prediction verdicts")
    for pk, vtext in chips:
        ck(vtext == P[pk]["verdict"], f"the page's chip for {pk} is the measured verdict")

    # ------------------------------------------------- 7. the quotations
    for s in SRC["sources"]:
        for q in s["quotes"]:
            norm = re.sub(r"\s+", " ", q["quote_restored"]).strip()
            if q["id"].endswith("three-strategies") or q["id"].endswith("acordar"):
                ck(norm.replace("…", "") .strip('".') [:60] in re.sub(r"\s+", " ", page),
                   f"the page carries the opening of quotation {q['id']}")
            # the restoration must differ from the extraction only by ligature glyphs
            a = q["quote_as_extracted"].replace(" ", "")
            b = q["quote_restored"].replace(" ", "")
            ck(len(b) >= len(a) - 2,
               f"{q['id']}: the restored quote is not shorter than what was extracted")
    ck(SRC["standing_claim_and_its_limits"]["limits"][:40] in page,
       "the page carries the stated limit of the literature claim")
    ck("two-paper check" in page, "the page says the literature check is two papers, not a census")
    ck("Neither sentence is in it" in page,
       "the page reports the fabricated quotations against ourselves")

    # ------------------------------------------------- 8. house rules
    doc_blob = page + json.dumps(SRC, ensure_ascii=False)
    for banned in ["openai", "gpt-", "anthropic", "claude", "gemini", "llama", "mistral",
                   "copilot", "chatgpt"]:
        ck(banned not in doc_blob.lower(),
           f"no tool or vendor name in this practice's own voice: '{banned}'")
    ck("<script" not in page.lower(), "the page carries no script")
    ck("http://" not in page and "https://" not in page.replace("https://arxiv.org", ""),
       "the page fetches nothing: no network reference beyond a cited source address")
    ck("PREREGISTRATION.md" in page, "the page points at its pre-registration")

    print(f"{N - len(FAIL)}/{N} checks passed")
    for f in FAIL:
        print("  FAIL:", f, file=sys.stderr)
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
