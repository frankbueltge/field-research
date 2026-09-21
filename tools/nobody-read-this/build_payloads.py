#!/usr/bin/env python3
"""Build the two blind adjudication payloads of session 166 (2026-09-21).

Arm A: the 11 cases session 164 adjudicated by hand, plus 4 mechanically chosen
sentinels, presented without any sign of which verdict is this practice's.
Arm B: up to 6 violation instances from each of the 10 classes session 165
adjudicated by hand, plus 4 sentinels, presented as source/follow-up pairs.

No model is called in this file. The reference labels are read, never written.

Usage: build_payloads.py <spdx_dir> <c2_dir> <run.json> <out_dir>
"""
import hashlib
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SEED = 20260921

DEC = ["l0", "families", "attribution", "delivers", "reason", "apache_appendix_unfilled"]
ECHO = ["notices", "holders", "n_notices", "placeholders"]

ATTR_VOCAB = """  "named"             - the document carries a copyright notice naming a holder
  "placeholder"       - it carries a copyright notice whose holder is an unfilled template
                        placeholder such as <year> <copyright holders> or [fullname]
  "no_holder"         - it carries a copyright notice but no holder can be read from it
  "no_copyright_line" - the document carries no copyright notice at all
  null                - not applicable: this is not one of the families whose canonical text
                        carries a copyright line inside the grant"""

# The two rungs, quoted from the specification the implementations were given, with the
# file paths of this repository removed. The redaction is recorded in data/items.json.
SPEC = """RUNG 1 - identified. The document's normalised text contains, as an exact substring, a
distinctive operative phrase of a known licence family. Normalisation: lowercase, all runs
of whitespace (including newlines) collapsed to one space, curly quotes folded to straight.
Each phrase is a sentence chosen to appear in no other family. A document matching more
than one family is recorded as multi-family, not silently resolved. Recall is deliberately
sacrificed for precision: a document that is not identified is recorded as not identified,
which is NOT a finding that it is not a licence.

RUNG 2 - attributed. For the families whose canonical text carries a copyright line inside
the operative grant - MIT-family, ISC, BSD-2/3/4-Clause and Zlib - the document carries a
line matching `copyright` + a year or year range + a holder, where the holder is not an
unfilled template placeholder. For every other family the answer is null, "not applicable",
never a negative answer. The Apache-2.0 and GPL-family appendices that read
`Copyright [yyyy] [name of copyright owner]` are explicitly OUTSIDE the scored set:
shipping them unedited is the normal, correct way to apply those licences."""


def excerpt(text, anchor_at=None, anchor_word="copyright"):
    """The excerpt rule of PREREGISTRATION.md section 6. Deterministic."""
    if len(text) <= 4000:
        return text, False
    if anchor_at is None:
        i = text.lower().find(anchor_word)
        anchor_at = i if i >= 0 else None
    head = text[:1200]
    if anchor_at is None:
        tail = text[-2800:]
        omitted = len(text) - 1200 - len(tail)
    else:
        lo = max(1200, anchor_at - 1400)
        hi = min(len(text), lo + 2800)
        lo = max(1200, hi - 2800)
        tail = text[lo:hi]
        omitted = lo - 1200
    if omitted <= 0:
        return text[:4000], True
    return head + f"\n[... {omitted} characters omitted ...]\n" + tail, True


def first_diff(a, b):
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            return i
    return n if len(a) != len(b) else None


def sig(v):
    ch = [f for f in DEC if json.dumps(v["before"][f], sort_keys=True)
          != json.dumps(v["after"][f], sort_keys=True)]
    return (v["relation"],
            " | ".join(f"{f}: {v['before'][f]!r} -> {v['after'][f]!r}" for f in ch))


def main():
    spdx_dir, c2_dir, run_path, out_dir = sys.argv[1:5]
    os.makedirs(out_dir, exist_ok=True)
    c1 = json.load(open(os.path.join(spdx_dir, "texts.json")))
    c2 = json.load(open(os.path.join(c2_dir, "texts.json")))
    run = json.load(open(run_path))
    text_of = {"C1": c1, "C2": c2}

    adjA = json.load(open(os.path.join(
        ROOT, "artifacts/2026-09-19-the-second-hand/data/adjudication.json")))
    verA = json.load(open(os.path.join(
        ROOT, "artifacts/2026-09-19-the-second-hand/data/verdicts.json")))
    adjB = json.load(open(os.path.join(
        ROOT, "artifacts/2026-09-20-the-same-text-twice/data/adjudication.json")))

    rng = random.Random(SEED)
    items = {"A": [], "B": []}

    # ---------------------------------------------------------------- Arm A
    for c in adjA["cases"]:
        flip = rng.random() < 0.5
        v1, v2 = ((c["independents"], c["R_ship"]) if flip else (c["R_ship"], c["independents"]))
        items["A"].append({
            "true_id": c["id"], "corpus": "C1", "kind": "case",
            "reference": c["verdict"],
            "ours_is": (2 if flip else 1),
            "v1": v1, "v2": v2,
        })

    # Arm A sentinels: first four C1 ids, identifier order, where the shipped rule and all
    # four independents agree attribution == "named" (arm C rows of session 164).
    rows = {r["id"]: r for r in verA["rows"] if r.get("arm") == "C"}
    agreed = [i for i in sorted(rows)
              if all(rows[i].get(k, {}).get("attribution") == "named"
                     for k in ("R-ship", "I-A", "I-B", "I-C", "I-D"))]
    for sid in agreed[:4]:
        r = rows[sid]
        good = {"families": r["R-ship"]["families"], "attribution": "named"}
        bad = {"families": r["R-ship"]["families"], "attribution": "no_copyright_line"}
        flip = rng.random() < 0.5
        items["A"].append({
            "true_id": sid, "corpus": "C1", "kind": "sentinel",
            "reference": ("2" if flip else "1"),
            "ours_is": None,
            "v1": (bad if flip else good), "v2": (good if flip else bad),
        })

    # ---------------------------------------------------------------- Arm B
    viol = run["violations"]
    dec_rows, echo_rows = [], []
    for v in viol:
        if v["relation"] == "M9":
            continue
        (dec_rows if sig(v)[1] else echo_rows).append(v)
    classes = {}
    for v in dec_rows:
        classes.setdefault(sig(v), []).append(v)

    def pick(rows_, n):
        rows_ = sorted(rows_, key=lambda r: (r["corpus"], r["input"]))
        return rows_ if len(rows_) <= n else rng.sample(rows_, n)

    def attr_pair(entry):
        """The attribution transition named in a committed class entry, e.g.
        'attribution no_copyright_line -> named; ...' -> ('no_copyright_line', 'named')."""
        m = re.search(r"attribution ([A-Za-z_]+) -> ([A-Za-z_]+)", entry["change"])
        return (m.group(1), m.group(2))

    by_key = {}
    for k, r in classes.items():
        v = r[0]
        by_key.setdefault((k[0], str(v["before"]["attribution"]),
                           str(v["after"]["attribution"])), []).extend(r)

    def cls_rows(entry):
        """Match a committed class entry to tonight's rows by relation and attribution
        transition. That pair is unique across the nine signatures; 9 and 9b share it and
        are split by the input the hand named."""
        rows_ = by_key.get((entry["relation"],) + attr_pair(entry))
        if rows_ is None:
            return None
        named = entry.get("inputs")
        if named:
            return [x for x in rows_ if x["input"] in named]
        sibling = [e for e in adjB["classes"]
                   if e is not entry and e["relation"] == entry["relation"]
                   and attr_pair(e) == attr_pair(entry) and e.get("inputs")]
        if sibling:
            excl = {i for e in sibling for i in e["inputs"]}
            return [x for x in rows_ if x["input"] not in excl]
        return rows_

    for entry in adjB["classes"]:
        label = str(entry["n"])
        if entry["n"] == 10:
            rows_ = pick(echo_rows, 6)
        else:
            rows_ = cls_rows(entry)
            if rows_ is None:
                raise SystemExit(f"class {label}: no signature matched")
            rows_ = pick(rows_, 6)
        for v in rows_:
            items["B"].append({
                "true_id": v["input"], "corpus": v["corpus"], "kind": "case",
                "klass": label, "reference": entry["verdict"], "relation": v["relation"],
                "before": {f: v["before"][f] for f in DEC},
                "after": {f: v["after"][f] for f in DEC},
                "source_sha256": v["source_sha256"], "followup_sha256": v["followup_sha256"],
            })

    # Arm B sentinels: first four C1 ids, identifier order, in no scored violation at all,
    # shown under the declared control relation with identical before/after tuples.
    touched = {v["input"] for v in viol if v["relation"] != "M9"}
    clean = [i for i in sorted(c1) if i not in touched][:4]
    for sid in clean:
        base = json.loads(run["baseline"]["C1"][sid])
        items["B"].append({
            "true_id": sid, "corpus": "C1", "kind": "sentinel",
            "klass": "sentinel", "reference": "MR-FALSE", "relation": "M4",
            "before": {f: base[f] for f in DEC}, "after": {f: base[f] for f in DEC},
            "source_sha256": None, "followup_sha256": None,
        })

    # ---------------------------------------------------------------- render
    rng.shuffle(items["A"])
    rng.shuffle(items["B"])
    for arm in ("A", "B"):
        for n, it in enumerate(items[arm], 1):
            it["item_id"] = f"{arm}{n:02d}"

    sys.path.insert(0, os.path.join(ROOT, "tools", "same-text-twice"))
    import relations as R
    relfn = {rid: fn for rid, _, fn in R.ALL}
    reldesc = {rid: d for rid, d, _ in R.ALL}

    outA = [HEAD_A]
    for it in items["A"]:
        txt = text_of[it["corpus"]][it["true_id"]]
        ex, cut = excerpt(txt)
        it["excerpt_sha256"] = hashlib.sha256(ex.encode()).hexdigest()
        it["excerpt_chars"] = len(ex)
        it["excerpted"] = cut
        outA.append(
            f"\n=== ITEM {it['item_id']} "
            f"{'(excerpt of a longer document)' if cut else '(complete document)'} ===\n"
            f"--- DOCUMENT BEGINS ---\n{ex}\n--- DOCUMENT ENDS ---\n"
            f"Verdict 1: family/families = {json.dumps(it['v1']['families'])}; "
            f"holder question = {json.dumps(it['v1']['attribution'])}\n"
            f"Verdict 2: family/families = {json.dumps(it['v2']['families'])}; "
            f"holder question = {json.dumps(it['v2']['attribution'])}\n")
    outA.append(TAIL_A.format(ids=", ".join(i["item_id"] for i in items["A"])))

    outB = [HEAD_B]
    for it in items["B"]:
        src = text_of[it["corpus"]][it["true_id"]]
        fu = relfn[it["relation"]](src)
        d = first_diff(src, fu)
        exs, cs = excerpt(src, anchor_at=d)
        exf, cf = excerpt(fu, anchor_at=d)
        it["excerpt_sha256"] = [hashlib.sha256(exs.encode()).hexdigest(),
                                hashlib.sha256(exf.encode()).hexdigest()]
        it["excerpt_chars"] = [len(exs), len(exf)]
        it["excerpted"] = bool(cs or cf)
        outB.append(
            f"\n=== ITEM {it['item_id']} "
            f"{'(excerpts of a longer document)' if (cs or cf) else '(complete documents)'} ===\n"
            f"Transformation applied: {reldesc[it['relation']]}\n"
            f"--- DOCUMENT A (before) BEGINS ---\n{exs}\n--- DOCUMENT A ENDS ---\n"
            f"--- DOCUMENT B (after) BEGINS ---\n{exf}\n--- DOCUMENT B ENDS ---\n"
            f"Reading of A: {json.dumps(it['before'], ensure_ascii=False)}\n"
            f"Reading of B: {json.dumps(it['after'], ensure_ascii=False)}\n")
    outB.append(TAIL_B.format(ids=", ".join(i["item_id"] for i in items["B"])))

    pa, pb = "".join(outA), "".join(outB)
    open(os.path.join(out_dir, "payload-A.txt"), "w").write(pa)
    open(os.path.join(out_dir, "payload-B.txt"), "w").write(pb)
    man = {
        "note": "Session 166, 2026-09-21. The item manifest of the two blind adjudication "
                "payloads. Holds the true corpus identifier and the reference label of every "
                "item; neither ever reached a worker. No licence text is committed.",
        "seed": SEED,
        "spec_redaction": "The two rungs are quoted from the specification of session 164 with "
                          "this repository's file paths removed, so that a worker cannot find "
                          "the instrument. Nothing else was altered inside the quoted rungs.",
        "payloads": {
            "A": {"chars": len(pa), "sha256": hashlib.sha256(pa.encode()).hexdigest(),
                  "n_items": len(items["A"]),
                  "n_sentinels": sum(1 for i in items["A"] if i["kind"] == "sentinel")},
            "B": {"chars": len(pb), "sha256": hashlib.sha256(pb.encode()).hexdigest(),
                  "n_items": len(items["B"]),
                  "n_sentinels": sum(1 for i in items["B"] if i["kind"] == "sentinel")}},
        "items": items,
    }
    json.dump(man, open(os.path.join(out_dir, "items.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in man["payloads"].items()}, indent=1))


HEAD_A = """You are adjudicating between two readings of a set of software licence documents.
For each item below you are given a document (or a marked excerpt of one) and two verdicts
produced by two different readers. Decide which verdict is right for what the document
actually says, under the specification quoted below.

THE SPECIFICATION - this is the whole of what the two readers were asked to apply:

""" + SPEC + """

The permitted answers to the holder question are exactly:
""" + ATTR_VOCAB + """

For each item answer with exactly one of:
  1        - Verdict 1 is right
  2        - Verdict 2 is right
  neither  - the specification does not decide this case: it can be read either way, or its
             own premise fails here

Judge each item on its own. The two verdicts may differ on the family question, on the
holder question, or on both; choose the verdict that is right overall, and if they are
right on different halves, answer `neither` and say so in your reason.

"""

TAIL_A = """
=== HOW TO ANSWER ===

Answer from the text above alone. Use no tools. Read no file. Search nothing.

Return a JSON array, one object per item, in this exact shape and covering every item:

  {{"item": "A01", "answer": "1" | "2" | "neither",
    "reason": "one line",
    "deciding_line": "the line of the document you decided on, quoted exactly"}}

Cover all {ids}.

After the JSON array, add one final line listing every file you read and every search you
ran while answering. If you read none and ran none, write exactly: TOOLS: none
"""

HEAD_B = """You are adjudicating the results of a test. A rule reads a licence document and
returns a verdict. The test rewrites the document in a way that is supposed not to change
what it says, runs the same rule again, and reports every case where the verdict moved.

Your job, for each item: say WHY the verdict moved.

THE SPECIFICATION the rule is supposed to implement:

""" + SPEC + """

The fields of a verdict:
  l0                        - the document is non-empty
  families                  - the licence families identified under rung 1
  attribution               - the answer to the holder question under rung 2, one of:
""" + ATTR_VOCAB + """
  delivers                  - the document both identifies a licence and names a licensor
  reason                    - the rule's own word for why `delivers` came out as it did
  apache_appendix_unfilled  - the Apache-2.0 appendix is present and unfilled

For each item choose exactly one of these four categories. The definitions are fixed and
you must use them as written:

  DEFECT     - the rule's verdict on document A (the original) is wrong for what a reader
               sees. The rewriting exposed an error the rule was already making.
  LATENT     - the verdict on A is right; the verdict on B is wrong. The rule would misread
               a legitimate variant of this document that does not happen to occur here.
  MR-FALSE   - the rewriting did not preserve meaning in this case, or the test itself was
               wrong to expect these two verdicts to be identical. No error of the rule is
               implied.
  UNDECIDED  - the specification does not decide this case.

"""

TAIL_B = """
=== HOW TO ANSWER ===

Answer from the text above alone. Use no tools. Read no file. Search nothing.

Return a JSON array, one object per item, in this exact shape and covering every item:

  {{"item": "B01", "answer": "DEFECT" | "LATENT" | "MR-FALSE" | "UNDECIDED",
    "reason": "one line",
    "deciding_line": "the line of document A you decided on, quoted exactly"}}

Cover all {ids}.

After the JSON array, add one final line listing every file you read and every search you
ran while answering. If you read none and ran none, write exactly: TOOLS: none
"""


if __name__ == "__main__":
    main()
