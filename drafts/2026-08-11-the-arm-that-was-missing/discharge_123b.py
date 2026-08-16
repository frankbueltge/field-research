#!/usr/bin/env python3
"""discharge_123b - recompute the Verifier's five blocking findings with our own code.

Session 123, 2026-08-16. Standing form: a reviewer's figure is recomputed here before it is
accepted, and where our recomputation disagrees with the report, BOTH are published.

All five findings share one shape: a sentence in `deliverable-v0.3/LIMITS.md` or `FIGURES.md` or
`MANIFEST.json` that the FIRST gauntlet (2026-08-15) already found false and published a true
value for, reproduced into version 0.3 unchanged. So this script does two things:

  1. checks each of the five against the primary data, independently of the reviewer's route;
  2. asks the general question the five raise together - **how many of the first gauntlet's
     published errata are still live in version 0.3?** - by taking that gauntlet's own errata
     table as the checklist it always was and nobody re-ran.

Usage: python3 discharge_123b.py
"""
import json
import os
import re
from collections import Counter

BUNDLE = "deliverable-v0.3"
out = {"schema": "field-research/gauntlet-discharge/2", "session": 123, "part": "b",
       "findings": {}}

limits = open(os.path.join(BUNDLE, "LIMITS.md")).read()
figs = open(os.path.join(BUNDLE, "FIGURES.md")).read()
man = json.load(open(os.path.join(BUNDLE, "MANIFEST.json")))

# ---- F1: did all twenty synthetic control identifiers return the same code? ------------------
f1 = {"claim_in_bundle": bool(re.search(r"twenty synthetic identifiers[^.]*same code", limits)),
      "source": "reverify-results.json"}
try:
    rv = json.load(open("reverify-results.json"))
    arm_c = rv["arm_c"] if isinstance(rv.get("arm_c"), list) else rv.get("arm_c", {}).get("results", [])
    pairs = Counter()
    for r in (arm_c if isinstance(arm_c, list) else []):
        pairs[(r.get("http"), r.get("http_2") if "http_2" in r else r.get("http"))] += 1
    f1["arm_c_n"] = len(arm_c) if isinstance(arm_c, list) else None
    f1["http_codes"] = Counter(str(r.get("http")) for r in arm_c) if isinstance(arm_c, list) else None
    f1["n_with_no_code"] = sum(1 for r in arm_c if r.get("http") is None) if isinstance(arm_c, list) else None
except Exception as e:
    f1["error"] = f"{type(e).__name__}: {e}"
f1["reviewer_value"] = "19 of 20 returned the code; the 20th had no code at all (transport failure)"
out["findings"]["F1_twenty_synthetic"] = f1

# ---- F2: is a vantage logged in every source run before its first request? -------------------
f2 = {"claim_in_bundle": bool(re.search(r"logged into every run file before the first", limits)),
      "source_runs": []}
for sr in man.get("source_runs", []):
    p = sr.get("file")
    row = {"label": sr.get("label"), "file": p, "run_id": sr.get("run_id")}
    if p and os.path.exists(p):
        d = json.load(open(p))
        v = d.get("vantage", {})
        row["vantage_source"] = v.get("source")
        row["vantage_fetched_utc"] = v.get("fetched_utc")
        row["is_a_union_of_components"] = "components" in d
        row["n_components"] = len(d.get("components", [])) if "components" in d else None
    else:
        row["unreadable"] = True
    f2["source_runs"].append(row)
f2["n_runs_whose_vantage_is_carried_not_logged"] = sum(
    1 for r in f2["source_runs"] if r.get("vantage_source") and "carried" in str(r["vantage_source"]))
out["findings"]["F2_vantage_logged_in_every_run"] = f2

# ---- F3: does any code compare a decoded creation time against endpoint metadata? ------------
f3 = {"claim_in_bundle": bool(re.search(r"checked against the endpoint's own returned metadata", limits))}
hits = []
for fn in ["probe.py", "ledger.py", "presence_check.py", "census.py",
           os.path.join(BUNDLE, "tools", "presence_check.py")]:
    if not os.path.exists(fn):
        continue
    src = open(fn, errors="replace").read()
    hits.append({"file": fn,
                 "mentions_create_time_field": bool(re.search(r"create_time|createTime|upload_date", src)),
                 "stores_endpoint_creation_time": bool(re.search(r"\[.create_time.\]\s*=", src))})
f3["files_searched"] = hits
f3["any_file_stores_an_endpoint_creation_time"] = any(h["stores_endpoint_creation_time"] for h in hits)
out["findings"]["F3_metadata_check"] = f3

# ---- F4: are the B-truncated control identifiers all not-videos? -----------------------------
f4 = {"claim_in_limits": bool(re.search(r"display-truncated identifiers that are \*\*not\*\*\s*\n?videos", limits)),
      "claim_in_figures": bool(re.search(r"display-truncated strings and not\s*\n?videos", figs))}
try:
    lc = json.load(open("legacy-id-control.json"))
    f4["legacy_id_control"] = {k: lc[k] for k in list(lc)[:8] if not isinstance(lc[k], (list, dict))}
    blob = json.dumps(lc)
    f4["mentions_12345"] = '"12345"' in blob or "'12345'" in blob
    f4["resolves_field_present"] = bool(re.search(r"RETRIEVABLE", blob))
except Exception as e:
    f4["error"] = f"{type(e).__name__}: {e}"
f4["reviewer_value"] = "248 of 249 do not resolve; `12345` is a real video predating the current scheme"
out["findings"]["F4_not_videos"] = f4

# ---- F5: is there an unfilled TEMPLATE placeholder in the shipped manifest? ------------------
f5 = {"entries_with_template_placeholder": [
    {"label": sr.get("label"), "file": sr.get("file"), "run_id": sr.get("run_id")}
    for sr in man.get("source_runs", []) if "TEMPLATE" in str(sr.get("run_id", ""))]}
f5["n"] = len(f5["entries_with_template_placeholder"])
out["findings"]["F5_template_placeholder"] = f5

# ---- the general question: how many of the FIRST gauntlet's errata are still live? -----------
# `deliverable/GAUNTLET-2026-08-15.md` is the errata table published with version 0.1. It was
# never used as a checklist against the rebuild. Here it is, used as one - mechanically, by
# looking for each erratum's own false phrase in the version 0.3 bundle.
g = open("deliverable/GAUNTLET-2026-08-15.md", errors="replace").read()
errata_ids = re.findall(r"^\|\s*(E\d+)\s*\|", g, re.M)
bundle_text = {}
for root, _, names in os.walk(BUNDLE):
    for n in sorted(names):
        if n.endswith((".md", ".json")):
            p = os.path.join(root, n)
            bundle_text[os.path.relpath(p, BUNDLE)] = open(p, errors="replace").read()

# The phrases the five findings turn on, taken from the errata table's own quoted wording.
PHRASES = {
    "E1": r"twenty synthetic identifiers",
    "E2": r"logged into every run file|logged in every run file",
    "E3": r"checked against the endpoint's own returned metadata",
    "E7": r"not\s*\*?\*?\s*videos|and not\s+videos",
    "E11": r"TEMPLATE",
    "E17": r"0\.14 percentage points|0\.14 pp",
}
live = {}
for eid, rx in PHRASES.items():
    where = [f for f, t in bundle_text.items() if re.search(rx, t)]
    live[eid] = {"phrase": rx, "still_present_in": where, "n_files": len(where)}
out["first_gauntlet_errata_recheck"] = {
    "errata_ids_in_the_published_table": errata_ids,
    "n_errata_in_table": len(errata_ids),
    "phrases_checked": len(PHRASES),
    "results": live,
    "n_still_live_of_those_checked": sum(1 for v in live.values() if v["n_files"]),
    "note": ("only the phrases the two reviewers turned on were machine-checked here. The "
             "remaining errata of that table have NOT been re-checked against version 0.3 by this "
             "script, and their status is therefore UNKNOWN rather than clear - which is itself "
             "the finding: the table was never re-run as a checklist."),
}

json.dump(out, open("discharge-123b.json", "w"), indent=1)
print(json.dumps({
    "F1_claim_present": f1["claim_in_bundle"], "F1_no_code_count": f1.get("n_with_no_code"),
    "F2_claim_present": f2["claim_in_bundle"],
    "F2_runs_with_carried_vantage": f2["n_runs_whose_vantage_is_carried_not_logged"],
    "F3_claim_present": f3["claim_in_bundle"],
    "F3_any_code_stores_endpoint_creation_time": f3["any_file_stores_an_endpoint_creation_time"],
    "F4_claim_in_limits": f4["claim_in_limits"], "F4_claim_in_figures": f4["claim_in_figures"],
    "F5_template_entries": f5["n"],
    "errata_phrases_still_live": {k: v["n_files"] for k, v in live.items()},
    "n_errata_in_first_gauntlet_table": len(errata_ids),
}, indent=1))
