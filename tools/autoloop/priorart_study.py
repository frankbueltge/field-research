#!/usr/bin/env python3
"""The session-153 study of stage PRIOR-ART, exactly as pre-registered.

`artifacts/cycle-002/2026-09-06-does-it-know-it-is-known/PREREGISTRATION.md` §3-§5 fixes the
benchmark, the two arms, the measures and the six predictions. This file runs them and writes
one results file. It computes nothing the pre-registration does not name, except quantities
explicitly marked post_hoc in the output.

Phases can be run one at a time so a network failure in phase 4 does not cost phase 1:

    python3 tools/autoloop/priorart_study.py --phase confirm  --out data/study.json
    python3 tools/autoloop/priorart_study.py --phase armA     --out data/study.json
    python3 tools/autoloop/priorart_study.py --phase armB     --out data/study.json
    python3 tools/autoloop/priorart_study.py --phase probes   --out data/study.json
    python3 tools/autoloop/priorart_study.py --phase repeat   --out data/study.json
    python3 tools/autoloop/priorart_study.py --phase measures --out data/study.json

Each phase reads the existing --out file if present and adds its own key to it.
"""

import argparse
import json
import os
import re
import time

import priorart

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = os.path.join(REPO, "artifacts/cycle-002/2026-09-06-does-it-know-it-is-known")
BENCH = os.path.join(ART, "data/benchmark.json")

# Words that may appear in a method's common name without counting as naming it: they are
# generic vocabulary, not the eponym. Fixed here, before the leakage check is run.
GENERIC_NAME_WORDS = {"test", "method", "procedure", "correlation", "interval", "score",
                      "rate", "false", "discovery", "multiple", "testing", "significant",
                      "pattern", "mining", "modified", "data", "discrete", "rank", "fusion",
                      "reciprocal", "permutation", "garden", "forking", "paths", "limitless",
                      "arity", "biserial"}


def load(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def save(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=1)


def bench():
    with open(BENCH) as f:
        return json.load(f)


def title_overlap(blind, title, stop):
    """Diagnostic D: share of the target title's content words present in the blind text."""
    tw = [w for w in re.findall(r"[a-z]+", title.lower()) if len(w) >= 4 and w not in stop]
    if not tw:
        return None, [], []
    bw = set(re.findall(r"[a-z]+", blind.lower()))
    present = [w for w in tw if w in bw]
    return len(present) / len(tw), present, [w for w in tw if w not in bw]


def name_leak(blind, name):
    """The §6 exclusion: does the blind description name the thing?

    Any non-generic content word of the common name occurring in the blind text is a leak.
    Eponyms are non-generic by construction, so this catches them.
    """
    nw = [w for w in re.findall(r"[a-z]+", name.lower())
          if len(w) >= 4 and w not in GENERIC_NAME_WORDS]
    bw = set(re.findall(r"[a-z]+", blind.lower()))
    return [w for w in nw if w in bw]


def hit(target, candidates, k):
    """Is the target among the top-k fused candidates? Rule fixed before the first run:
    DOI equal, PMID equal, or normalised title equal."""
    want_doi = (target.get("doi") or "").lower()
    want_pmid = target.get("pmid")
    want_title = priorart.norm_title(target.get("title"))
    for i, c in enumerate(candidates[:k], start=1):
        if want_doi and c.get("doi") == want_doi:
            return {"rank": i, "matched_on": "doi"}
        if want_pmid and c.get("pmid") == want_pmid:
            return {"rank": i, "matched_on": "pmid"}
        if want_title and priorart.norm_title(c.get("title")) == want_title:
            return {"rank": i, "matched_on": "title"}
    return None


def near_miss(target, candidates, k=10, thresh=0.6):
    """Post-hoc diagnostic only: a candidate sharing >= `thresh` of the target's title words."""
    tw = set(w for w in re.findall(r"[a-z]+", (target.get("title") or "").lower()) if len(w) >= 4)
    if not tw:
        return None
    best = None
    for i, c in enumerate(candidates[:k], start=1):
        cw = set(w for w in re.findall(r"[a-z]+", (c.get("title") or "").lower()) if len(w) >= 4)
        j = len(tw & cw) / len(tw)
        if j >= thresh and (best is None or j > best["overlap"]):
            best = {"rank": i, "overlap": round(j, 3), "title": c.get("title"),
                    "doi": c.get("doi")}
    return best


# --- phases ---------------------------------------------------------------------------

def phase_confirm(state):
    b = bench()
    out = []
    for it in b["targeted"]:
        t = it["target"]
        c = priorart.confirm_target(t["title"], t.get("doi"), t.get("pmid"))
        c["id"] = it["id"]
        out.append(c)
        print(f"{it['id']}: confirmed={c['confirmed']}")
    state["confirm"] = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "items": out,
                        "confirmed_ids": [c["id"] for c in out if c["confirmed"]]}
    return state


def run_arm(items, decorate, log):
    b = bench()
    stop = b["stopwords"]
    out = []
    for it in items:
        text = decorate(it)
        r = priorart.assess(text, stopwords=stop, log=log)
        out.append({"id": it["id"], "text": text, "verdict": r["verdict"],
                    "calls": r["calls"], "seconds": r["seconds"], "errors": r["errors"],
                    "candidates": r["candidates"],
                    "queries": r["queries"],
                    "lists": [{"catalogue": l["catalogue"], "query": l["query"], "q": l["q"],
                               "keys": [priorart.key_of(c) for c in l["results"]],
                               "titles": [c["title"] for c in l["results"]]}
                              for l in r["lists"]]})
        print(f"{it['id']}: {r['verdict']} ({r['seconds']} s)")
    return out


def phase_armA(state):
    b = bench()
    log = []
    state["armA"] = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                     "items": run_arm(b["targeted"], lambda it: it["blind"], log),
                     "query_log": log}
    return state


def phase_armB(state):
    b = bench()
    log = []
    state["armB"] = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                     "items": run_arm(b["targeted"],
                                      lambda it: it["blind"] + " (" + it["name"] + ")", log),
                     "query_log": log}
    return state


def phase_armBprime(state):
    """POST-HOC, added 2026-09-06 after Arm B came back byte-identical to Arm A.

    Arm B as pre-registered appended the common name to the END of the description. Q1
    truncates at 350 characters and the descriptions are longer than that, and Q2/Q3 rank terms
    by frequency, where a name occurring once ranks last. So the name never reached a single
    query and Arm B measured nothing. It is kept in the record as run. This arm prepends the
    name instead, so that Q1 carries it.
    """
    b = bench()
    log = []
    state["armBprime"] = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "post_hoc": True,
        "why": "Arm B as pre-registered never delivered the name to any query; see the docstring",
        "items": run_arm(b["targeted"], lambda it: it["name"] + ". " + it["blind"], log)}
    return state


def phase_armBname(state):
    """POST-HOC. The ceiling: the query is the common name and nothing else."""
    b = bench()
    log = []
    state["armBname"] = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "post_hoc": True,
        "why": "what retrieval is worth when you already know what the thing is called",
        "items": run_arm(b["targeted"], lambda it: it["name"], log)}
    return state


def phase_probes(state):
    b = bench()
    log = []
    state["probes"] = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                       "items": run_arm(b["no_target"], lambda it: it["blind"], log)}
    return state


def phase_repeat(state):
    """M4. Re-issue every Arm-A query once and compare the top-10 identifier lists."""
    armA = state["armA"]["items"]
    rows = []
    for it in armA:
        for l in it["lists"]:
            try:
                res = priorart.CATALOGUES[l["catalogue"]](l["q"])
                keys = [priorart.key_of(c) for c in res]
                err = None
            except Exception as e:
                keys, err = None, type(e).__name__ + ": " + str(e)[:120]
            rows.append({"id": it["id"], "catalogue": l["catalogue"], "query": l["query"],
                         "identical": (keys == l["keys"]) if keys is not None else None,
                         "first_n": len(l["keys"]),
                         "second_n": (len(keys) if keys is not None else None),
                         "error": err})
            time.sleep(priorart.POLITE_SLEEP)
        print(f"{it['id']}: repeated")
    ok = [r for r in rows if r["identical"] is not None]
    state["repeat"] = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                       "rows": rows, "n": len(ok),
                       "identical": sum(1 for r in ok if r["identical"]),
                       "share": (sum(1 for r in ok if r["identical"]) / len(ok)) if ok else None}
    return state


def phase_measures(state):
    b = bench()
    stop = set(b["stopwords"])
    conf = {c["id"]: c for c in state["confirm"]["items"]}
    tmap = {it["id"]: it for it in b["targeted"]}
    A = {i["id"]: i for i in state["armA"]["items"]}
    B = {i["id"]: i for i in state["armB"]["items"]}
    Bp = {i["id"]: i for i in state.get("armBprime", {}).get("items", [])} or None
    Bn = {i["id"]: i for i in state.get("armBname", {}).get("items", [])} or None

    rows = []
    for it in b["targeted"]:
        tid = it["id"]
        leak = name_leak(it["blind"], it["name"])
        ov, present, missing = title_overlap(it["blind"], it["target"]["title"], stop)
        a, bb = A[tid], B[tid]
        rows.append({
            "id": tid,
            "anchor": bool(it.get("anchor")),
            "target": it["target"],
            "confirmed": conf[tid]["confirmed"],
            "confirmed_at": ([k for k in ("crossref", "pubmed")
                              if isinstance(conf[tid].get(k), dict)
                              and "error" not in conf[tid][k]]),
            "name_leak": leak,
            "excluded": bool(leak),
            "title_overlap": (round(ov, 3) if ov is not None else None),
            "title_words_present": present,
            "title_words_absent": missing,
            "armA_hit10": hit(it["target"], a["candidates"], 10),
            "armA_hit3": hit(it["target"], a["candidates"], 3),
            "armA_verdict": a["verdict"],
            "armA_near_miss_post_hoc": near_miss(it["target"], a["candidates"]),
            "armB_hit10": hit(it["target"], bb["candidates"], 10),
            "armB_hit3": hit(it["target"], bb["candidates"], 3),
            "armB_verdict": bb["verdict"],
            "armB_identical_to_armA_post_hoc": (
                [q["q"] for q in a["queries"]] == [q["q"] for q in bb["queries"]]),
            **{f"{arm}_{k}_post_hoc": v for arm, src in (("armBprime", Bp), ("armBname", Bn))
               if src for k, v in (("hit10", hit(it["target"], src[tid]["candidates"], 10)),
                                   ("hit3", hit(it["target"], src[tid]["candidates"], 3)),
                                   ("verdict", src[tid]["verdict"]))},
        })

    usable = [r for r in rows if r["confirmed"] and not r["excluded"]]
    a10 = [r for r in usable if r["armA_hit10"]]
    a3 = [r for r in usable if r["armA_hit3"]]
    b10 = [r for r in usable if r["armB_hit10"]]
    b3 = [r for r in usable if r["armB_hit3"]]

    # M6 catalogue and query attribution for the blind hits.
    attrib = []
    for r in a10:
        cand = None
        for c in A[r["id"]]["candidates"]:
            h = hit(r["target"], [c], 1)
            if h:
                cand = c
                break
        if cand:
            attrib.append({"id": r["id"],
                           "found_by": cand["found_by"],
                           "catalogues": sorted(set(f["catalogue"] for f in cand["found_by"])),
                           "queries": sorted(set(f["query"] for f in cand["found_by"]))})

    # P5: split usable items at the median of diagnostic D.
    ovs = sorted(r["title_overlap"] for r in usable if r["title_overlap"] is not None)
    med = ovs[len(ovs) // 2] if ovs else None
    hi = [r for r in usable if r["title_overlap"] is not None and r["title_overlap"] >= med]
    lo = [r for r in usable if r["title_overlap"] is not None and r["title_overlap"] < med]

    probes = state["probes"]["items"]
    fired = [p for p in probes if p["verdict"] == "PRIOR ART POSSIBLE"]

    anchor = next((r for r in rows if r["anchor"]), None)

    calls = ([i["calls"] for i in state["armA"]["items"]]
             + [i["calls"] for i in state["armB"]["items"]]
             + [i["calls"] for i in probes])
    secs = ([i["seconds"] for i in state["armA"]["items"]]
            + [i["seconds"] for i in state["armB"]["items"]]
            + [i["seconds"] for i in probes])

    m = {
        "n_proposed": len(rows),
        "n_confirmed": sum(1 for r in rows if r["confirmed"]),
        "n_excluded_for_leak": sum(1 for r in rows if r["excluded"]),
        "n_usable": len(usable),
        "M1_armA_hit10": len(a10), "M1_armA_hit3": len(a3),
        "M2_armB_hit10": len(b10), "M2_armB_hit3": len(b3),
        "M1_armA_hit10_ids": [r["id"] for r in a10],
        "M2_armB_hit10_ids": [r["id"] for r in b10],
        "M3_probes_n": len(probes),
        "M3_probes_fired": len(fired),
        "M3_probes_fired_ids": [p["id"] for p in fired],
        "M4_repeat_n": state["repeat"]["n"],
        "M4_repeat_identical": state["repeat"]["identical"],
        "M4_repeat_share": state["repeat"]["share"],
        "M5_calls_per_description": (sum(calls) / len(calls)) if calls else None,
        "M5_seconds_per_description_mean": (sum(secs) / len(secs)) if secs else None,
        "M5_calls_total": sum(calls),
        "M6_attribution": attrib,
        "D_median": med,
        "P5_high_overlap": {"n": len(hi), "hit10": sum(1 for r in hi if r["armA_hit10"])},
        "P5_low_overlap": {"n": len(lo), "hit10": sum(1 for r in lo if r["armA_hit10"])},
        "P5_testable": bool(hi and lo),
        "armB_identical_to_armA_post_hoc": sum(
            1 for r in rows if r.get("armB_identical_to_armA_post_hoc")),
        "armBprime_hit10_post_hoc": sum(1 for r in usable if r.get("armBprime_hit10_post_hoc")),
        "armBprime_hit3_post_hoc": sum(1 for r in usable if r.get("armBprime_hit3_post_hoc")),
        "armBprime_hit10_ids_post_hoc": [r["id"] for r in usable
                                         if r.get("armBprime_hit10_post_hoc")],
        "armBname_hit10_post_hoc": sum(1 for r in usable if r.get("armBname_hit10_post_hoc")),
        "armBname_hit3_post_hoc": sum(1 for r in usable if r.get("armBname_hit3_post_hoc")),
        "armBname_hit10_ids_post_hoc": [r["id"] for r in usable
                                        if r.get("armBname_hit10_post_hoc")],
        "armBname_hit1_post_hoc": sum(
            1 for r in usable
            if (r.get("armBname_hit10_post_hoc") or {}).get("rank") == 1),
    }

    m["predictions"] = {
        "P1_named_beats_blind": {
            "statement": "Arm B hit@10 > Arm A hit@10",
            "armA": m["M1_armA_hit10"], "armB": m["M2_armB_hit10"],
            "holds": m["M2_armB_hit10"] > m["M1_armA_hit10"],
            # Corrected 2026-09-07 (session 154), adversary defect A1. This asked whether EVERY
        # item's Arm-B query set was byte-identical to Arm A's; five of ten were, so the flag
        # read False and the page's table rendered P1 *refuted* against its own prose. Arm B
        # is void when the name reached no query at all — which is what `void_reason` records
        # and what the truncation guarantees for every item whose description exceeds the
        # 350-character cut. No committed result file is rewritten by this change.
        "void": bool(m["armB_identical_to_armA_post_hoc"] > 0),
            "void_reason": ("Arm B's queries are byte-identical to Arm A's for every item: the "
                            "appended name reached no query, so this prediction was not tested")},
        "P2_blind_is_weak": {
            "statement": "Arm A hit@10 <= half the usable targets",
            "armA": m["M1_armA_hit10"], "half": len(usable) / 2,
            "holds": m["M1_armA_hit10"] <= len(usable) / 2},
        "P3_cannot_say_no": {
            "statement": "the verdict fires on at least 3 of the 4 no-target probes",
            "fired": len(fired), "of": len(probes),
            "holds": len(fired) >= 3},
        "P4_reproducible": {
            "statement": "at least 90 % of re-issued queries return an identical top-10",
            "share": state["repeat"]["share"],
            "holds": (state["repeat"]["share"] or 0) >= 0.90},
        "P5_retrieves_by_title_words": {
            "statement": "blind hit@10 is higher in the above-median half of D",
            "high": m["P5_high_overlap"], "low": m["P5_low_overlap"],
            "holds": (m["P5_high_overlap"]["hit10"] / max(1, m["P5_high_overlap"]["n"]))
                     > (m["P5_low_overlap"]["hit10"] / max(1, m["P5_low_overlap"]["n"])),
            "void": not m["P5_testable"],
            "void_reason": ("the median of D is 0.0, so the below-median half is empty and no "
                            "split exists; and with no blind hit anywhere there is nothing to "
                            "split")},
        "P6_anchor_fails_blind": {
            "statement": "T1, described in ignorance, is not retrieved blind at hit@10",
            "anchor_hit10": (anchor or {}).get("armA_hit10"),
            "holds": not (anchor or {}).get("armA_hit10")},
    }

    state["measures"] = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                         "rows": rows, **m}
    return state


PHASES = {"confirm": phase_confirm, "armA": phase_armA, "armB": phase_armB,
          "armBprime": phase_armBprime, "armBname": phase_armBname,
          "probes": phase_probes, "repeat": phase_repeat, "measures": phase_measures}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, choices=list(PHASES))
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    state = load(args.out)
    state = PHASES[args.phase](state)
    save(args.out, state)
    print("wrote " + args.out)


if __name__ == "__main__":
    main()
