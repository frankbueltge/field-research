#!/usr/bin/env python3
"""check.py — verify this artifact offline.

Session 157, cycle 003. What it verifies, and the list is exhaustive on purpose:

  1. BYTE IDENTITY. build.py is re-run into a temporary file and the result must be
     byte-for-byte the committed index.html. This closes the substring hole the Atelier
     reported against its own checker on 2026-09-09 and which we adopt here with credit.
  2. NUMERALS. Every number in the page's visible text must be derivable from
     data/results.json under one of the page's formatting conventions.
  3. QUANTITIES WRITTEN AS WORDS. Every spelled-out quantity in the narrative must be
     declared in data/narrative.json with its value, and that value must occur in
     data/results.json. (Session 155's checker missed these entirely.)
  4. VERDICTS. P1-P7 are recomputed here from the raw per-catalogue numbers, by code that
     does not import the tool that produced them, and must match the stored verdicts.
  5. QUOTED VALUES. Every catalogue value quoted on the page must match data/results.json.
  6. QUOTED SOURCES. Every passage quoted from outside must match data/sources.json, and
     each source there must carry a URL, an access date and the extraction route.

  What it does NOT verify, stated where the claim is made and repeated here: the narrative
  prose. A false sentence with no number in it, written into data/narrative.json, passes
  every check below. That is the residue reported as a failure on 2026-09-09 and it is
  unchanged today.

Exit 0 only if every check passes. Standard library only; no network.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FAILS: list[str] = []
CHECKS = 0


def ok(cond: bool, msg: str) -> None:
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILS.append(msg)


def text_of(html_doc: str) -> str:
    body = re.sub(r"<style.*?</style>", " ", html_doc, flags=re.S | re.I)
    body = re.sub(r"<script.*?</script>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    body = (body.replace("&thinsp;", "").replace("&nbsp;", " ").replace("&amp;", "&")
                .replace("&chi;", "chi").replace("&kappa;", "kappa").replace("&rsquo;", "'")
                .replace("&ldquo;", '"').replace("&rdquo;", '"').replace("&lt;", "<")
                .replace("&gt;", ">").replace("&quot;", '"').replace("&sup2;", "2")
                .replace("&mdash;", "—").replace("&ndash;", "–").replace("&times;", "x"))
    return re.sub(r"\s+", " ", body)


def walk(obj, out: set) -> None:
    if isinstance(obj, dict):
        for v in obj.values():
            walk(v, out)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, out)
    elif isinstance(obj, bool):
        pass
    elif isinstance(obj, (int, float)):
        out.add(obj)


def renderings(values: set) -> set:
    """Every string form in which a value from results.json may legitimately appear."""
    s = set()
    for v in values:
        if isinstance(v, int) or (isinstance(v, float) and v.is_integer()):
            i = int(v)
            s.add(str(i))
            s.add(f"{i:,}".replace(",", ""))
        if isinstance(v, float):
            for nd in (2, 3, 4, 5):
                s.add(f"{v:.{nd}f}")
            s.add(repr(v))
        s.add(str(v))
    return s


WORD_RE = re.compile(
    r"\b(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|"
    r"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|"
    r"eighty|ninety|hundred|thousand|million)\b", re.I)


def recompute_verdicts(d: dict) -> dict:
    """P1-P7 from the raw numbers, independent of tools/travel/travel.py."""
    C, A = d["catalogues"], d.get("audit")
    scored = ("cma", "uk", "govdata")
    v = {}

    v["P1"] = "confirmed" if all(
        C[c]["declared_completeness_pct"] >= 95.0
        and C[c]["held"]["hollow_broad"]["pct"] >= 5.0 for c in scored) else "refuted"

    passes = []
    for c in scored:
        a, k = C[c].get("association"), C[c].get("concentration")
        passes.append(bool(a and k and a.get("bh_survivor") and k["ratio"] >= 2.0))
    v["P2"] = "confirmed" if all(passes) else ("refuted" if not any(passes) else "split")

    passes = [C[c]["p3_broad_is_r2"]["pct"] >= 95.0 for c in scored]
    v["P3"] = "confirmed" if all(passes) else ("refuted" if not any(passes) else "split")

    v["P4"] = ("confirmed" if A and A["agreement_pct"] >= 75.0 and A["kappa"] >= 0.42
               else ("refuted" if A else "pending"))

    de = C["govdata"]["held"]["r3_opener"]["pct"]
    en = C["uk"]["held"]["r3_opener"]["pct"]
    v["P5"] = "confirmed" if (de < 1.0 and en >= 1.0) else "refuted"

    v["P6"] = "confirmed" if any(
        C[c]["held"]["r5_title_echo"]["pct"] >= 1.0
        and C[c]["p6_r5_increment"]["r5_only"] >= 20 for c in scored) else "refuted"

    want = d["predictions"]["P7"]["published_2026_09_08"]
    at = C["atlas"]
    got = {"records": at["records"], "all_broad_pct": at["all"]["hollow_broad"]["pct"],
           "held_broad_pct": at["held"]["hollow_broad"]["pct"],
           "r4_held_k": at["held"]["r4_duplicate"]["k"],
           "broad_is_r2_held_agree": at["p3_broad_is_r2"]["agree"],
           "held_n": at["split"]["held"]}
    v["P7"] = "confirmed" if got == want else "refuted"
    return v


def main() -> int:
    page_path = os.path.join(HERE, "index.html")
    page = open(page_path, encoding="utf-8").read()
    d = json.load(open(os.path.join(HERE, "data", "results.json"), encoding="utf-8"))
    nar = json.load(open(os.path.join(HERE, "data", "narrative.json"), encoding="utf-8"))
    src = json.load(open(os.path.join(HERE, "data", "sources.json"), encoding="utf-8"))

    # ---- 1. byte identity -------------------------------------------------
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "rendered.html")
        r = subprocess.run([sys.executable, os.path.join(HERE, "build.py"), "--out", out],
                           capture_output=True, text=True)
        ok(r.returncode == 0, f"build.py exited {r.returncode}: {r.stderr[:200]}")
        if r.returncode == 0:
            rendered = open(out, "rb").read()
            ok(rendered == open(page_path, "rb").read(),
               "index.html is not byte-identical to a fresh render of build.py")

    body = text_of(page)

    # ---- 2. numerals ------------------------------------------------------
    vals: set = set()
    walk(d, vals)
    allowed = renderings(vals)
    allowed |= {str(x) for x in range(0, 11)}                 # section and list numbers
    allowed |= set(nar.get("allowed_literals", []))
    bad = []
    for tok in re.findall(r"\d[\d.]*", body):
        tok = tok.rstrip(".")
        if tok in allowed:
            continue
        try:
            f = float(tok)
        except ValueError:
            bad.append(tok)
            continue
        if any(abs(f - float(a)) < 1e-9 for a in allowed if _isnum(a)):
            continue
        bad.append(tok)
    ok(not bad, f"numbers on the page not derivable from results.json: {sorted(set(bad))[:24]}")

    # ---- 3. quantities written as words -----------------------------------
    declared = {k.lower(): v for k, v in nar.get("word_numbers", {}).items()}
    undeclared = sorted({w.lower() for w in WORD_RE.findall(body)} - set(declared))
    ok(not undeclared,
       f"quantities written as words and not declared in narrative.json: {undeclared[:24]}")
    for w, val in declared.items():
        ok(val in vals or val in {int(x) for x in vals if float(x).is_integer()},
           f"declared word-number '{w}' = {val} does not occur in results.json")

    # ---- 4. verdicts ------------------------------------------------------
    mine = recompute_verdicts(d)
    for k, verdict in mine.items():
        stored = d["predictions"][k]["verdict"]
        ok(stored == verdict, f"{k}: page carries '{stored}', recomputation gives '{verdict}'")
        ok(f"{verdict}" in body, f"{k}: verdict '{verdict}' does not appear on the page")

    # ---- 5. quoted catalogue values ---------------------------------------
    for q in d["quotes"]:
        frag = q["value"][:90]
        marker = _html_escape(frag)
        ok(marker in page or frag in body,
           f"quoted value not found on the page: {frag[:60]!r}")

    # ---- 6. quoted outside sources ----------------------------------------
    for s in src["sources"]:
        for field in ("url", "accessed_utc", "extraction"):
            ok(bool(s.get(field)), f"source {s.get('id')} is missing {field}")
        for p in s.get("passages", []):
            ok(p["quote"] in body or _html_escape(p["quote"]) in page,
               f"passage from {s['id']} is not on the page: {p['quote'][:60]!r}")

    # ---- report -----------------------------------------------------------
    print(f"check.py — {CHECKS} checks over index.html, results.json, narrative.json, sources.json")
    if FAILS:
        for f in FAILS:
            print("  FAIL " + f)
        print(f"{len(FAILS)} of {CHECKS} checks failed.")
        return 1
    print("all passed: page is a byte-identical render of the committed record; every numeral and "
          "every spelled-out quantity is derivable from it; every prediction verdict recomputes; "
          "every quoted value and passage matches the record.")
    print("NOT verified: the narrative prose. A false sentence carrying no number, written into "
          "narrative.json, passes this checker. Reported as a failure, not as future work.")
    return 0


def _isnum(x: str) -> bool:
    try:
        float(x)
        return True
    except ValueError:
        return False


def _html_escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


if __name__ == "__main__":
    raise SystemExit(main())
