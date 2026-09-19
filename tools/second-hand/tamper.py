#!/usr/bin/env python3
"""Deliberate corruptions of this session's own evidence. Session 164.

A checker nobody has attacked is a checker nobody has read. Each corruption below
changes one committed value, runs check.py against the corrupted copy, and records
whether the check noticed. A corruption that slips through is a hole in the checker
and is published as one.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = os.path.join(ROOT, "artifacts", "2026-09-19-the-second-hand")


def jset(path, fn):
    d = json.load(open(path))
    fn(d)
    json.dump(d, open(path, "w"), indent=1)


def tset(path, old, new):
    s = open(path).read()
    assert old in s, f"tamper target absent: {old[:40]}"
    open(path, "w").write(s.replace(old, new, 1))


CORRUPTIONS = [
 ("corpus: change one entry's sha256",
  lambda a: jset(f"{a}/data/corpus.json", lambda d: d["entries"][0].__setitem__("sha256", "0"*64))),
 ("corpus: drop one entry",
  lambda a: jset(f"{a}/data/corpus.json", lambda d: d["entries"].pop())),
 ("corpus: restate the digest",
  lambda a: jset(f"{a}/data/corpus.json", lambda d: d.__setitem__("corpus_digest", "f"*64))),
 ("corpus: claim 741 texts",
  lambda a: jset(f"{a}/data/corpus.json", lambda d: d.__setitem__("texts_ok", 741))),
 ("verdicts: delete one row",
  lambda a: jset(f"{a}/data/verdicts.json", lambda d: d["rows"].pop())),
 ("verdicts: invent a family outside the vocabulary",
  lambda a: jset(f"{a}/data/verdicts.json",
                 lambda d: d["rows"][0]["R-ship"].__setitem__("families", ["EUPL-1.2"]))),
 ("verdicts: invent an attribution value",
  lambda a: jset(f"{a}/data/verdicts.json",
                 lambda d: d["rows"][3]["I-A"].__setitem__("attribution", "probably"))),
 ("verdicts: flip one independent's verdict on canonical MIT",
  lambda a: jset(f"{a}/data/verdicts.json",
                 lambda d: [r for r in d["rows"] if r["id"] == "MIT" and r["arm"] == "C"][0]
                 ["I-A"].__setitem__("attribution", "named"))),
 ("verdicts: make R-def agree with R-ship on MIT",
  lambda a: jset(f"{a}/data/verdicts.json",
                 lambda d: [r for r in d["rows"] if r["id"] == "MIT" and r["arm"] == "C"][0]
                 ["R-def"].__setitem__("attribution", "placeholder"))),
 ("verdicts: claim an implementation failed nothing when it failed",
  lambda a: jset(f"{a}/data/verdicts.json",
                 lambda d: d["delivery"]["I-B"].__setitem__("n_failures", 7))),
 ("analysis: inflate the all-five agreement",
  lambda a: jset(f"{a}/data/analysis.json",
                 lambda d: d["unanimous"]["C"].__setitem__("all_agree_families", 700))),
 ("analysis: restate one pair's agreement",
  lambda a: jset(f"{a}/data/analysis.json",
                 lambda d: d["pairwise"]["I-A vs R-ship"]["C"].__setitem__("families_agree", 739))),
 ("analysis: shrink the internal disagreement to flatter the method",
  lambda a: jset(f"{a}/data/analysis.json",
                 lambda d: d["independents_internal"]["C"]
                 .__setitem__("independents_disagree_internally", 3))),
 ("analysis: inflate the count that convicts us",
  lambda a: jset(f"{a}/data/analysis.json",
                 lambda d: d["independents_internal"]["C"]
                 .__setitem__("independents_unanimous_against_R_ship", 40))),
 ("analysis: break the transition arithmetic",
  lambda a: jset(f"{a}/data/analysis.json",
                 lambda d: d["l2_transition"]["R-ship"].__setitem__("placeholder_then_named", 11))),
 ("analysis: give R-def a passing transition score",
  lambda a: jset(f"{a}/data/analysis.json",
                 lambda d: d["l2_transition"]["R-def"].__setitem__("pct_correct", 90.0))),
 ("adjudication: drop a case that convicts us",
  lambda a: jset(f"{a}/data/adjudication.json", lambda d: d["cases"].pop(0))),
 ("adjudication: turn a conviction into an acquittal",
  lambda a: jset(f"{a}/data/adjudication.json",
                 lambda d: d["cases"][0].__setitem__("verdict", "R-ship right"))),
 ("adjudication: misstate what the independents said",
  lambda a: jset(f"{a}/data/adjudication.json",
                 lambda d: d["cases"][0]["independents"].__setitem__("attribution", "placeholder"))),
 ("adjudication: name a fourth suspect file in the 09-18 data",
  lambda a: jset(f"{a}/data/adjudication.json",
                 lambda d: d["defect_4"]["effect_on_published_numbers"]["findings"]
                 .append({"repo": "invented/repo", "file": "LICENSE",
                          "sha256_matches_0918": True, "verdict": "invented"}))),
 ("predictions: turn a refutation into a confirmation",
  lambda a: jset(f"{a}/data/predictions.json",
                 lambda d: d["predictions"]["P3"].__setitem__("verdict", "CONFIRMED"))),
 ("predictions: claim a kill condition never existed",
  lambda a: jset(f"{a}/data/predictions.json",
                 lambda d: d["kill_conditions"].pop("K4"))),
 ("predictions: say a kill condition fired",
  lambda a: jset(f"{a}/data/predictions.json",
                 lambda d: d["kill_conditions"]["K1"].__setitem__("fired", True))),
 ("predictions: change an expectation after the fact",
  lambda a: jset(f"{a}/data/predictions.json",
                 lambda d: d["predictions"]["P3"].__setitem__("expected", "confirmed"))),
 ("implementations: change a committed module's recorded digest",
  lambda a: jset(f"{a}/data/implementations.json",
                 lambda d: d["implementations"][0].__setitem__("sha256", "1"*64))),
 ("K3: claim the scan passed when it did not",
  lambda a: jset(f"{a}/data/k3-run1-defective.json", lambda d: d.__setitem__("all_pass", True))),
 ("K3: hide the second failing run",
  lambda a: os.remove(f"{a}/data/k3-run2-defective.json")),
 ("sources: mark the unread paper as read",
  lambda a: jset(f"{a}/data/sources.json",
                 lambda d: [s for s in d["sources"] if s["key"] == "knight-leveson-1986"][0]
                 .__setitem__("read", True))),
 ("sources: put a quotation into the unread paper",
  lambda a: jset(f"{a}/data/sources.json",
                 lambda d: [s for s in d["sources"] if s["key"] == "knight-leveson-1986"][0]
                 .__setitem__("quotations", [{"page_marker": "p.96", "text": "x"*60}]))),
 ("sources: alter the number inside a quoted passage",
  lambda a: jset(f"{a}/data/sources.json",
                 lambda d: [s for s in d["sources"] if s["key"] == "wolter-2019"][0]["quotations"][1]
                 .__setitem__("text", "agreed on their result in 149000 of those cases. 99.00% of all license hits"))),
 ("page: restate the headline agreement",
  lambda a: tset(f"{a}/index.html", "82.7&nbsp;%", "97.4&nbsp;%")),
 ("page: drop the sentence that says the headline does not move",
  lambda a: tset(f"{a}/index.html", "does not move", "moves a lot")),
 ("page: remove a prediction from the table",
  lambda a: tset(f"{a}/index.html", '<td class="pid">P3</td>', '<td class="pid">PX</td>')),
 ("page: delete the independence limitation",
  lambda a: tset(f"{a}/index.html", "weak, and it is part of the finding",
                 "strong, and beyond question")),
 ("pre-registration: delete a prediction",
  lambda a: tset(f"{a}/PREREGISTRATION.md", "- **P4.**", "- **PX.**")),
 ("pre-registration: delete the fill table's holder token",
  lambda a: tset(f"{a}/PREREGISTRATION.md", "[name of copyright owner]", "[redacted]")),
]


def main():
    results = []
    for name, corrupt in CORRUPTIONS:
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "repo")
            os.makedirs(root)
            shutil.copytree(ART, os.path.join(root, "artifacts", "2026-09-19-the-second-hand"))
            shutil.copytree(os.path.join(ROOT, "artifacts",
                                         "2026-09-18-a-licence-file-is-not-a-licence"),
                            os.path.join(root, "artifacts",
                                         "2026-09-18-a-licence-file-is-not-a-licence"))
            shutil.copytree(os.path.join(ROOT, "tools"), os.path.join(root, "tools"))
            art = os.path.join(root, "artifacts", "2026-09-19-the-second-hand")
            try:
                corrupt(art)
            except Exception as exc:
                results.append({"corruption": name, "caught": None,
                                "error": f"could not apply: {type(exc).__name__}: {exc}"})
                continue
            p = subprocess.run([sys.executable, os.path.join(art, "check.py"),
                                os.path.join(tmp, "out.json")],
                               capture_output=True, text=True)
            results.append({"corruption": name, "caught": p.returncode != 0,
                            "first_failure": next((l.strip() for l in p.stdout.splitlines()
                                                   if l.strip().startswith("FAIL")), None)
                            or (p.stderr.strip().splitlines()[-1] if p.returncode else None)})
    missed = [r for r in results if r["caught"] is not True]
    out = {"note": "Deliberate corruptions of this session's own evidence, each run against a "
                   "copy of check.py. A corruption that is not caught is a hole in the checker "
                   "and is published as one.",
           "n_corruptions": len(results), "n_caught": len(results) - len(missed),
           "n_missed": len(missed), "corruptions": results}
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ART, "data", "tamper-check.json")
    open(dest, "w").write(json.dumps(out, indent=1) + "\n")
    print(f"{len(results)} corruptions, {len(results)-len(missed)} caught, {len(missed)} missed")
    for m in missed:
        print("  MISSED:", m["corruption"], m.get("error", ""))


if __name__ == "__main__":
    main()
