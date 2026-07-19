#!/usr/bin/env python3
"""SECONDARY probe (exploratory, prompted by the null primary result — NOT the pre-registered
primary). Question: the primary spike used the single nearest-to-Oct-2024 capture per URL and
found p(content_present)=0.00. Does ANY in-window capture per URL preserve cited content?
This tests the more permissive "recoverable from the archive at all in-window" quantity the
Skeptic flagged, so a DESCOPE-vs-KILL decision rests on best-case, not nearest-only.

Same containment as classify.py: structural envelope only; keyed by sample index; records no
handle/URL and no content substance."""
import json, os, time
here = os.path.dirname(os.path.abspath(__file__))
import importlib.util
spec = importlib.util.spec_from_file_location("clf", os.path.join(here, "classify.py"))
# import fetch/classify without running classify.py's main loop:
src = open(os.path.join(here, "classify.py")).read()
ns = {}
# execute only up to the "results = []" main loop
head = src.split("results = []")[0]
ns["__file__"] = os.path.join(here, "classify.py")
exec(compile(head, "classify.py", "exec"), ns)
fetch, classify = ns["fetch"], ns["classify"]

sample = json.load(open(os.path.join(here, "sample.json")))["sample"]
cdx = json.load(open(os.path.join(here, "..", "2026-07-16-half-life-archival-probe",
                                    "cdx_results.json")))
by_url = {r["url"]: r for r in cdx}
LO, HI = "20231001000000", "20250101000000"

recs = []
for i, s in enumerate(sample):
    caps = sorted({c[0] for c in by_url[s["url"]]["captures"]
                   if c[1] == "200" and LO <= c[0] < HI})
    best = "none"; got = False; labels = []
    for ts in caps:
        body = fetch(ts, s["url"])
        lab = classify(body)["label"] if body else "fetch_failed"
        labels.append(lab)
        if lab == "content_present":
            best = "content_present"; got = True; break
        time.sleep(0.8)
    if not got:
        # rank remaining by informativeness
        for pref in ["content_thin", "login_shell", "unavailable", "other", "fetch_failed"]:
            if pref in labels:
                best = pref; break
    recs.append({"i": i, "n_caps": len(caps), "best": best, "labels": labels})
    print(f'[{i:2d}] caps={len(caps)} best={best:16s} {labels}')

from collections import Counter
any_content = sum(1 for r in recs if r["best"] == "content_present")
tally = Counter(r["best"] for r in recs)
out = {"n": len(recs), "any_content_present": any_content,
       "best_label_tally": dict(tally), "results": recs}
json.dump(out, open(os.path.join(here, "secondary_results.json"), "w"), indent=1)
print("\nANY in-window capture content_present:", any_content, "of", len(recs))
print("best-label tally:", dict(tally))
