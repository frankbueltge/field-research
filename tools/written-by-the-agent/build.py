#!/usr/bin/env python3
"""Write the artifact's data/ from the work directory. Session 171, 2026-09-26.

The readings below were made in-session by this practice, reading each sentence and, for
table cells, the table header. NO PERSON READ ANY OF IT.
"""
import json
import os
import sys
from collections import Counter

WORK, DATA = sys.argv[1], sys.argv[2]

# ---- every flag, adjudicated ----
FLAGS = {
    "2510.16194#0": ("rule_error",
                     "The rule paired 33% with '3 in 4' taken from 'top-3 in 4 of 6'. The sentence "
                     "prints 2 of 6 (33%), which is consistent. Not an error in the paper."),
}
# ---- the 60 sampled not_recomputable tokens, classed (09-23 classes) ----
OTHER = {"2509.12179#1": "a standard deviation", "2509.12179#21": "a standard deviation",
         "2509.12179#24": "a standard deviation", "2509.12179#25": "a standard deviation",
         "2509.12179#30": "a correlation printed as a percentage",
         "2510.18003#89": "a theoretical random-guess baseline", "2510.18003#91": "a theoretical random-guess baseline",
         "2510.18003#94": "a theoretical random-guess baseline", "2510.18003#97": "a theoretical random-guess baseline",
         "2510.18003#117": "an F1 score", "2603.15712#0": "an accuracy quoted from cited work"}
DIFF = {"2509.12179#11": "a relative reduction", "2509.12179#27": "a relative improvement",
        "2509.12179#39": "a relative improvement", "2509.12179#43": "a relative improvement"}
NOTE = {"2510.16194#2": "coverage; the table prints the numerator (Num Correct) but no denominator",
        "2510.18003#98": "a true-positive rate; the evaluation set is described as 50 real and 50 "
                         "generated papers, yet 81.6 % of 50 is not an integer (40/49 fits); "
                         "the denominator actually used is not printed",
        "2603.15712#20": "printed beside '18 of the best 25', which is 72 %, not 75 %; the 75 % is a "
                         "different quantity whose counts are not printed",
        "2603.15712#27": "n = 250 is printed, k is not; 57 or 58 of 250 would both print 23 %"}


def main():
    match = json.load(open(os.path.join(WORK, "match.json")))
    p1 = {p["openreview"]: p.get("arxiv") for p in json.load(open(os.path.join(WORK, "match-pass1.json")))["papers"]}
    units = json.load(open(os.path.join(WORK, "units.json")))
    byline = json.load(open(os.path.join(WORK, "byline.json")))
    docs = {d["arxiv"]: d for d in units["docs"]}
    os.makedirs(DATA, exist_ok=True)

    corpus = []
    for p in match["papers"]:
        a = p.get("arxiv")
        corpus.append({
            "openreview": p["openreview"], "title": p["title"], "tier": p["tier"],
            "first_listed_author": p["authors"].split(",")[0].strip(),
            "arxiv": a, "found_on": ("pass1" if p1.get(p["openreview"]) else ("recheck" if a else None)),
            "recheck_query": p.get("recheck_query"),
            "recheck_nearest_refused": (p.get("recheck_candidates") or [None])[0] if not a else None,
            "html_status": p.get("html_status"),
            "text_sha256": docs[a]["text_sha256"] if a in docs else None,
            "words": docs[a]["words"] if a in docs else None,
            "percentage_tokens": docs[a]["tokens"] if a in docs else None})
    json.dump({"list_url": match["list_url"], "list_sha256": match["list_sha256"],
               "fetched_at_utc": match["fetched_at_utc"], "rechecked_at_utc": match.get("rechecked_at_utc"),
               "papers": corpus}, open(os.path.join(DATA, "corpus.json"), "w"), indent=1, ensure_ascii=False)

    sample = set(units["sample"])
    out_units, reading = [], []
    for u in units["units"]:
        rec = {"uid": u["uid"], "printed": u["text"], "verdict": u["verdict"], "pair": u["pair"]}
        if u["verdict"] != "not_recomputable" or u["uid"] in sample:
            s, j = u["sentence"], u["span"][0]
            rec["context"] = s[max(0, j - 110):j + 70]            # a short quotation, not the text
        out_units.append(rec)
        if u["verdict"] in ("inconsistent", "complement"):
            v, n = FLAGS[u["uid"]]
            reading.append({"uid": u["uid"], "kind": "flag", "judgement": v, "note": n})
        if u["uid"] in sample:
            c = ("other" if u["uid"] in OTHER else "difference" if u["uid"] in DIFF else "k_or_n_absent")
            reading.append({"uid": u["uid"], "kind": "sample", "class": c,
                            "note": OTHER.get(u["uid"]) or DIFF.get(u["uid"]) or NOTE.get(u["uid"]) or
                            "a share of counted things (papers, candidates, cases, wins); its counts are not in the sentence"})
    json.dump({"rule": "tools/a-number-you-cannot-check/handover.py, imported unchanged",
               "seed": 20260926, "sample": units["sample"], "units": out_units},
              open(os.path.join(DATA, "units.json"), "w"), indent=1, ensure_ascii=False)
    json.dump({"reader": "this practice, in session; no person read any of it", "readings": reading},
              open(os.path.join(DATA, "reading.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(byline, open(os.path.join(DATA, "byline.json"), "w"), indent=1, ensure_ascii=False)
    print(Counter(r.get("class") or r.get("judgement") for r in reading))


if __name__ == "__main__":
    main()
