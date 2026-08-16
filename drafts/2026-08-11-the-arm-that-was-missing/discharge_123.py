#!/usr/bin/env python3
"""discharge_123 - recompute the gauntlet's own figures with our code before accepting them.

Session 123, 2026-08-16. This practice's standing form: a reviewer's number is recomputed here
first, and where our recomputation disagrees with the report, BOTH are published.

What is checked:

  C1  The Interlocutor's charge that `FIGURES.md` and `reference-baseline.json` ship
      "21 encyclopedia language editions" while the true count is 37. The report re-derived 37
      independently of the two-session-old erratum. We re-derive it a third way here: from the
      corpus files on disk, counting the editions that actually contribute a W-article unit to
      the panel this bundle was built from.

  C1b The related charge that `FIGURES.md`'s 0.14 pp across-day spread is the figure the first
      gauntlet's erratum E17 found 2.35x inflated, and that no qualification of it survives
      anywhere in `deliverable-v0.3/`.

  C2c The charge that `receiver-eleven.md` cites `LIMITS.md` section 8 for a statistical-power
      caveat that existed under v0.1's numbering and does not exist anywhere in v0.3's rewritten
      LIMITS. Checked by resolving every `LIMITS.md §N` cross-reference in the bundle against the
      actual headings of the LIMITS shipped beside it.

  A   Whether `FIGURES.md` would in fact have failed the prose audit had it been passed to it -
      the counterfactual the charge rests on.

Usage: python3 discharge_123.py
"""
import glob
import json
import os
import re

import figures as F

BUNDLE = "deliverable-v0.3"
out = {"schema": "field-research/gauntlet-discharge/1", "session": 123, "checks": {}}


# ---- C1: how many encyclopedia language editions actually contribute a W-article unit? -------
manifest = json.load(open("manifest-day2-onward.json"))
article_arms = {"A", "A-new"}
article_vids = {str(u["vid"]) for u in manifest["units"] if u.get("arm") in article_arms}

vid_editions = {}
for path in sorted(glob.glob("corpus-*.json")):
    host = os.path.basename(path)[len("corpus-"):-len(".json")]
    try:
        data = json.load(open(path))
    except Exception as e:
        out.setdefault("unreadable_corpus_files", []).append({"file": path, "error": type(e).__name__})
        continue
    # The corpus files nest differently across harvest generations; every 19-digit run of digits
    # anywhere in the file is taken as a candidate identifier and intersected with the panel.
    blob = json.dumps(data)
    for vid in set(re.findall(r"(?<!\d)(\d{19})(?!\d)", blob)):
        if vid in article_vids:
            vid_editions.setdefault(vid, set()).add(host)

editions = sorted({h for hs in vid_editions.values() for h in hs})
wiki_editions = sorted(h for h in editions if h.endswith("wikipedia.org"))
out["checks"]["C1_language_editions"] = {
    "charge": "FIGURES.md and reference-baseline.json say 21 encyclopedia language editions",
    "reviewer_value": 37,
    "our_value_distinct_editions_contributing_a_W_article_unit": len(wiki_editions),
    "our_value_all_hosts": len(editions),
    "article_units_in_panel": len(article_vids),
    "article_units_matched_to_an_edition": len(vid_editions),
    "article_units_unmatched": len(article_vids) - len(vid_editions),
    "editions": wiki_editions,
    "corpus_files_on_disk": len(glob.glob("corpus-*.json")),
    "method": ("every 19-digit identifier appearing anywhere in a corpus file is taken as a "
               "candidate and intersected with the panel's A/A-new units; an edition counts if at "
               "least one panel article unit appears in its file. Unmatched units are reported "
               "rather than assumed to belong anywhere."),
}

# ---- C1b: does the string "21" still ship, and is the 0.14 pp figure qualified anywhere? -----
fig = open(os.path.join(BUNDLE, "FIGURES.md")).read()
ref = json.load(open(os.path.join(BUNDLE, "reference-baseline.json")))
bundle_text = ""
for root, _, names in os.walk(BUNDLE):
    for n in names:
        if n.endswith((".md", ".json")):
            bundle_text += open(os.path.join(root, n), errors="replace").read()

out["checks"]["C1b_shipped_strings"] = {
    "figures_md_contains_21_language_editions": bool(
        re.search(r"\b21\b[^|\n]{0,40}language editions", fig)),
    "reference_baseline_population_what_it_is": ref["population"].get("what_it_is"),
    "reference_baseline_says_21": "21" in str(ref["population"].get("what_it_is", "")),
    "figures_md_contains_0_14_pp_spread": "0.14 percentage points" in fig or "0.14 pp" in fig,
    "bundle_contains_balanced_panel_qualification": "0.0577" in bundle_text
                                                    or "balanced panel" in bundle_text,
    "note": ("the qualification the first gauntlet's erratum E17 published is the balanced-panel "
             "spread of 0.0577 pp on 3,465 units determinate on every day; if the bundle carries "
             "neither that number nor the phrase, the corrected reading is absent from it"),
}

# ---- C2c: every `LIMITS.md §N` cross-reference resolved against the LIMITS shipped beside it --
limits = open(os.path.join(BUNDLE, "LIMITS.md")).read()
headings = {int(m.group(1)): m.group(2).strip()
            for m in re.finditer(r"^##\s*(\d+)\.\s*(.+)$", limits, re.M)}
refs = []
for root, _, names in os.walk(BUNDLE):
    for n in sorted(names):
        if not n.endswith(".md"):
            continue
        p = os.path.join(root, n)
        for m in re.finditer(r"`?LIMITS\.md`?\s*§+\s*(\d+)", open(p, errors="replace").read()):
            sec = int(m.group(1))
            refs.append({"file": os.path.relpath(p, BUNDLE), "section": sec,
                         "resolves": sec in headings,
                         "heading_it_lands_on": headings.get(sec)})
out["checks"]["C2c_cross_references"] = {
    "charge": ("receiver-eleven.md cites LIMITS.md section 8 for a statistical-power caveat; "
               "v0.3's LIMITS was rewritten from twelve sections to nine and section 8 is now a "
               "different topic"),
    "limits_sections_in_v03": headings,
    "n_sections_v03": len(headings),
    "references_found": refs,
    "n_unresolvable": sum(1 for r in refs if not r["resolves"]),
    "power_caveat_present_anywhere_in_v03_limits": bool(
        re.search(r"hypothes|statistical power|underpowered", limits, re.I)),
}

# ---- A: would FIGURES.md have failed the prose audit? ---------------------------------------
au = F.audit_prose([os.path.join(BUNDLE, "FIGURES.md")],
                   os.path.join(BUNDLE, "FIGURE-PROVENANCE.json"))
out["checks"]["A_figures_md_against_the_audit"] = {
    "charge": "FIGURES.md is generated prose and was never passed to audit_prose()",
    "n_unmatched_if_it_had_been": au["n_unmatched_total"],
    "first_20_unmatched": au["files"][0]["unmatched"][:20],
    "note": ("a large count here does NOT mean FIGURES.md is wrong - it is generated by a "
             "different script from a different source and its numbers were never registered in "
             "this provenance table. It means the audit, as built, could not have covered it "
             "without the figures being routed through `figures.py` first. The charge is about "
             "scope, and this is the size of the scope that was left out."),
}

json.dump(out, open("discharge-123.json", "w"), indent=1)
print(json.dumps({
    "C1_our_edition_count": out["checks"]["C1_language_editions"][
        "our_value_distinct_editions_contributing_a_W_article_unit"],
    "C1_reviewer_value": 37,
    "C1b_21_still_shipped": out["checks"]["C1b_shipped_strings"][
        "figures_md_contains_21_language_editions"],
    "C1b_0.14pp_qualified_anywhere": out["checks"]["C1b_shipped_strings"][
        "bundle_contains_balanced_panel_qualification"],
    "C2c_unresolvable_refs": out["checks"]["C2c_cross_references"]["n_unresolvable"],
    "C2c_power_caveat_present": out["checks"]["C2c_cross_references"][
        "power_caveat_present_anywhere_in_v03_limits"],
    "A_figures_md_unmatched": out["checks"]["A_figures_md_against_the_audit"][
        "n_unmatched_if_it_had_been"],
}, indent=1))
