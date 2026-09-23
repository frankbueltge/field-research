#!/usr/bin/env python3
"""Estimates, adjudications and robustness checks. Session 168, 2026-09-23.

Reads the screens and samples from outside the repository, writes the artifact's data/.
The adjudications below were made in-session by this practice, reading each sentence.
NO PERSON READ ANY OF IT -- the correction of 2026-09-21 stands.
"""
import hashlib
import html
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from handover import analyse                                        # noqa: E402

WORK = sys.argv[1]
DATA = sys.argv[2]

# ---- adjudications, by position in the flagged list / sample list of each corpus ----
FLAG_VERDICT = {
    "F": ["rule_error"] * 6,
    "A": ["rule_error"] * 2,
    "M": (["real"] * 3 + ["rule_error"] * 2 + ["rule_error"] * 13 + ["rule_error"] * 2
          + ["real"] * 3 + ["rule_error"] * 2),
}
FLAG_NOTE = {
    ("M", 0): "10/434 = 2.3041 %; printed 2.2 %. The companion 14 of 452 (3.1 %) is consistent.",
    ("M", 1): "40/445 = 8.9888 %; printed 9.2 %. A smaller undisclosed denominator would fit.",
    ("M", 2): "34/459 = 7.4074 %; printed 7.7 %. Same sentence as the one above.",
    ("M", 20): "13/965 = 1.3472 %; printed 1.4 %. Every other fraction in this abstract is consistent.",
    ("M", 21): "22/65 = 33.8462 %; printed 33.9 %. Every other fraction in this abstract is consistent.",
    ("M", 22): "3/44 = 6.82 %; printed 9 %. The line above reports 9 % for 4/44.",
}
# rule-recomputable stratum: index of tokens whose pairing is NOT the one a reader makes
PREC_BAD = {"M": [16, 17], "A": [0, 5], "F": [3, 5, 8, 14, 18, 19]}
PREC_BY_ARITHMETIC = {"M": [3, 4, 19], "A": [], "F": []}
# non-recomputable stratum: classification
NONREC = {
    "M": ["other", "k_or_n_absent", "k_or_n_absent", "threshold", "k_or_n_absent", "other",
          "other", "k_or_n_absent", "k_or_n_absent", "difference", "other", "rule_miss",
          "k_or_n_absent", "other", "other", "k_or_n_absent", "k_or_n_absent", "other",
          "threshold", "k_or_n_absent", "threshold", "other", "other", "threshold", "other"],
    "A": ["k_or_n_absent", "k_or_n_absent", "difference", "difference", "k_or_n_absent",
          "other", "k_or_n_absent", "other", "other", "k_or_n_absent", "difference",
          "k_or_n_absent", "k_or_n_absent", "difference", "k_or_n_absent", "k_or_n_absent",
          "difference", "k_or_n_absent", "k_or_n_absent", "k_or_n_absent", "difference",
          "k_or_n_absent", "k_or_n_absent", "other", "k_or_n_absent"],
    "F": ["k_or_n_absent", "k_or_n_absent", "k_or_n_absent", "k_or_n_absent", "threshold",
          "k_or_n_absent", "k_or_n_absent", "k_or_n_absent", "k_or_n_absent", "k_or_n_absent",
          "k_or_n_absent", "k_or_n_absent", "k_or_n_absent", "k_or_n_absent", "k_or_n_absent",
          "k_or_n_absent", "k_or_n_absent", "k_or_n_absent", "k_or_n_absent", "k_or_n_absent",
          "k_or_n_absent", "other", "k_or_n_absent", "k_or_n_absent", "k_or_n_absent"],
}


def wilson(k, n, z=1.959963985):
    if n == 0:
        return [0.0, 1.0]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [max(0.0, c - h), min(1.0, c + h)]


def main():
    screens = {c: json.load(open(os.path.join(WORK, f"screen-{c}.json"), encoding="utf-8"))
               for c in "MAF"}
    samples = json.load(open(os.path.join(WORK, "samples.json"), encoding="utf-8"))
    corpora = {c: json.load(open(os.path.join(WORK, f"corpus-{c}.json"), encoding="utf-8"))
               for c in "MAF"}

    # ---------- manifests ----------
    manifest = {}
    for c in "MAF":
        rows = []
        for d in corpora[c]["docs"]:
            rows.append({"id": d["id"],
                         "sha256": hashlib.sha256(d["text"].encode("utf-8")).hexdigest(),
                         "chars": len(d["text"])})
        joint = hashlib.sha256("".join(r["sha256"] for r in rows).encode()).hexdigest()
        manifest[c] = {"source": corpora[c]["source"], "documents": len(rows),
                       "corpus_digest": joint, "docs": rows}
        for key in ("term", "query", "year", "esearch_count", "records_seen",
                    "fetched_at_utc", "built_at_utc", "summaries", "bulletins"):
            if key in corpora[c]:
                manifest[c][key] = corpora[c][key]

    # ---------- adjudication of every flagged token ----------
    adjud = {}
    for c in "FAM":
        flagged = [t for t in screens[c]["tokens"] if t["verdict"] in ("inconsistent", "complement")]
        assert len(flagged) == len(FLAG_VERDICT[c]), (c, len(flagged))
        rows = []
        for i, t in enumerate(flagged):
            s = t["sentence"]
            rows.append({"corpus": c, "doc": t["doc"], "printed": t["text"], "pair": t["pair"],
                         "recomputed": round(100.0 * t["pair"][0] / t["pair"][1], 4),
                         "verdict": FLAG_VERDICT[c][i],
                         "note": FLAG_NOTE.get((c, i)),
                         "quote": (s[:220] + "…") if len(s) > 220 else s})
        adjud[c] = rows

    # ---------- the stratified estimate ----------
    est = {}
    for c in "MAF":
        s = samples[c]
        n_rec, n_non = s["N_rec"], s["N_non"]
        total = n_rec + n_non
        srec = len(s["recomputable"])
        good = srec - len(PREC_BAD[c])
        snon = len(s["non_recomputable"])
        miss = sum(1 for x in NONREC[c] if x == "rule_miss")
        p_rec, p_non = good / srec, miss / snon
        point = (n_rec * p_rec + n_non * p_non) / total
        lo_rec, hi_rec = wilson(good, srec)
        lo_non, hi_non = wilson(miss, snon)
        est[c] = {
            "corpus": c, "tokens": total, "documents": manifest[c]["documents"],
            "documents_with_a_percentage": screens[c]["counts"]["documents_with_a_percentage"],
            "screen": {"recomputable": n_rec, "not_recomputable": n_non,
                       "rate": round(100.0 * n_rec / total, 2),
                       "consistent": screens[c]["counts"]["consistent"],
                       "inconsistent": screens[c]["counts"]["inconsistent"],
                       "complement": screens[c]["counts"]["complement"]},
            "sample": {"recomputable_read": srec, "pairing_a_reader_would_make": good,
                       "precision": round(p_rec, 4),
                       "precision_95": [round(lo_rec, 4), round(hi_rec, 4)],
                       "non_recomputable_read": snon, "rule_misses": miss,
                       "miss_rate": round(p_non, 4),
                       "miss_rate_95": [round(lo_non, 4), round(hi_non, 4)],
                       "pairing_confirmed_only_by_arithmetic": len(PREC_BY_ARITHMETIC[c]),
                       "composition": {k: NONREC[c].count(k) for k in sorted(set(NONREC[c]))}},
            "hand_over_rate": {
                "point": round(100.0 * point, 2),
                "low": round(100.0 * (n_rec * lo_rec + n_non * lo_non) / total, 2),
                "high": round(100.0 * (n_rec * hi_rec + n_non * hi_non) / total, 2)},
            "real_arithmetic_errors": sum(1 for r in adjud[c] if r["verdict"] == "real"),
            "flagged": len(adjud[c]),
            "flag_precision": round(sum(1 for r in adjud[c] if r["verdict"] == "real")
                                    / len(adjud[c]), 4) if adjud[c] else None,
        }
        docs_with_error = sorted({r["doc"] for r in adjud[c] if r["verdict"] == "real"})
        est[c]["documents_with_a_real_error"] = len(docs_with_error)
        est[c]["docs_with_a_real_error"] = docs_with_error

    # ---------- robustness 1: HTML numeric entities decoded ----------
    rob = {}
    for c in "MA":
        base = screens[c]["counts"]
        ent_docs = sum(1 for d in corpora[c]["docs"] if "&#" in d["text"])
        toks, rec = 0, 0
        for d in corpora[c]["docs"]:
            got = analyse(html.unescape(d["text"]), doc_id=d["id"])
            toks += len(got)
            rec += sum(1 for t in got if t["verdict"] != "not_recomputable")
        rob[c] = {"documents_carrying_html_entities": ent_docs,
                  "tokens_as_fetched": base["tokens"], "tokens_decoded": toks,
                  "recomputable_as_fetched": base["recomputable"], "recomputable_decoded": rec,
                  "screen_rate_as_fetched": round(100.0 * base["recomputable"] / base["tokens"], 2),
                  "screen_rate_decoded": round(100.0 * rec / toks, 2) if toks else None}

    # ---------- robustness 2: is the asterisk-stripping line inert? ----------
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "handover.py"),
               encoding="utf-8").read()
    anchor = "line = re.sub(r'\\*+', '', line)"
    assert src.count(anchor) == 1
    ns = {}
    exec(compile(src.replace(anchor, "pass", 1), "no-asterisk.py", "exec"), ns)
    alt = ns["analyse"]
    same, differ = 0, 0
    for c in "MAF":
        for d in corpora[c]["docs"]:
            a = [(t["value"], t["verdict"], tuple(t["pair"] or ())) for t in analyse(d["text"])]
            b = [(t["value"], t["verdict"], tuple(t["pair"] or ())) for t in alt(d["text"])]
            if a == b:
                same += 1
            else:
                differ += 1
    rob["asterisk_stripping"] = {
        "claim": "R-1's asterisk stripping is inert on all three corpora",
        "documents_identical": same, "documents_differing": differ}

    os.makedirs(DATA, exist_ok=True)
    json.dump(manifest, open(os.path.join(DATA, "corpora.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    json.dump(adjud, open(os.path.join(DATA, "adjudication.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    json.dump(est, open(os.path.join(DATA, "estimates.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    json.dump(rob, open(os.path.join(DATA, "robustness.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    for c in "MAF":
        e = est[c]
        print(f"{c}: {e['tokens']} tokens, screen {e['screen']['rate']} %, "
              f"hand-read {e['hand_over_rate']['point']} % "
              f"[{e['hand_over_rate']['low']}, {e['hand_over_rate']['high']}], "
              f"precision {e['sample']['precision']}, misses {e['sample']['rule_misses']}, "
              f"flags {e['flagged']} -> real {e['real_arithmetic_errors']}")
    print(json.dumps(rob, indent=1))


if __name__ == "__main__":
    main()
