#!/usr/bin/env python3
"""Validate the mechanical detector against the committed hand-audit labels, and run the
post-hoc checks the pre-registration did not name (each marked post_hoc in the output).

No model is called here. Standard library only.
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hollow import cohen_kappa, wilson, classify, duplicate_keys, norm  # noqa: E402

OUT = "artifacts/cycle-003/2026-09-08-complete-and-empty/data"


def confusion(mech: list[int], hand: list[int]) -> dict:
    tp = sum(1 for m, h in zip(mech, hand) if m == 1 and h == 0)  # flagged, unusable
    fp = sum(1 for m, h in zip(mech, hand) if m == 1 and h == 1)  # flagged, usable
    fn = sum(1 for m, h in zip(mech, hand) if m == 0 and h == 0)  # missed
    tn = sum(1 for m, h in zip(mech, hand) if m == 0 and h == 1)
    n = len(mech)
    agree = (tp + tn) / n
    # kappa on the "unusable" coding: mechanical flag vs hand label 0
    k = cohen_kappa(mech, [1 - h for h in hand])
    return {
        "flagged_and_unusable": tp, "flagged_but_usable": fp,
        "unflagged_and_unusable": fn, "unflagged_and_usable": tn,
        "agreement_pct": round(100 * agree, 2),
        "cohen_kappa": round(k, 4),
        "recall_on_unusable": round(tp / (tp + fn), 4) if (tp + fn) else None,
        "precision": round(tp / (tp + fp), 4) if (tp + fp) else None,
    }


def main() -> int:
    results = json.load(open(os.path.join(OUT, "results.json")))
    entries = {r["title"]: r for r in json.load(open(os.path.join(OUT, "entries.json")))}
    audit = json.load(open(os.path.join(OUT, "audit-labels.json")))
    sample = json.load(open(os.path.join(OUT, "audit-sample.json")))

    sample_titles = [s["title"] for s in sample]
    labels = {}
    for rec in audit["labels"]:
        # exact match required. A 40-character prefix match was used until 2026-09-08 and let a
        # label whose recorded title diverged after character 40 pass as a match; the adversary
        # found one. A divergence must fail here, not be absorbed.
        matches = [t for t in sample_titles if t == rec["title"]]
        if len(matches) != 1:
            print(f"AUDIT LABEL DOES NOT MATCH EXACTLY ONE SAMPLED ENTRY: {rec['title']!r} -> {matches}",
                  file=sys.stderr)
            return 2
        labels[matches[0]] = rec["label"]
    if len(labels) != len(sample_titles):
        print("AUDIT SIZE MISMATCH", file=sys.stderr)
        return 2

    hand = [labels[t] for t in sample_titles]
    out = {"n": len(hand),
           "hand_unusable": sum(1 for h in hand if h == 0),
           "hand_unusable_pct": round(100 * sum(1 for h in hand if h == 0) / len(hand), 2)}
    lo, hi = wilson(out["hand_unusable"], out["n"])
    out["hand_unusable_ci95"] = [round(100 * lo, 2), round(100 * hi, 2)]

    for agg in ("hollow_broad", "hollow_strict", "r1_chrome", "r2_truncated_tail",
                "r3_truncated_head", "r4_duplicate"):
        mech = [1 if entries[t][agg] else 0 for t in sample_titles]
        out[agg] = confusion(mech, hand)
        out[agg]["flag_rate_pct"] = round(100 * sum(mech) / len(mech), 2)

    # --- post-hoc 1: is provenance the whole story? ------------------------
    rows = list(entries.values())
    rh = [r for r in rows if r["provenance"] == "Rhizome ArtBase"]
    nr = [r for r in rows if r["provenance"] != "Rhizome ArtBase"]
    posthoc = {
        "post_hoc": True,
        "note": "Not in the pre-registered test set. Reported because 12 of 12 tests survived BH, "
                "which is a warning that the covariates are not independent.",
        "rhizome": {"n": len(rh),
                    "hollow_broad": sum(1 for r in rh if r["hollow_broad"]),
                    "hollow_strict": sum(1 for r in rh if r["hollow_strict"]),
                    "verify_status_levels": sorted({r["verify_status"] for r in rh}),
                    "medium_class_levels": sorted({r["medium_class"] for r in rh})},
        "not_rhizome": {"n": len(nr),
                        "hollow_broad": sum(1 for r in nr if r["hollow_broad"]),
                        "hollow_strict": sum(1 for r in nr if r["hollow_strict"])},
    }

    # --- post-hoc 2: the datasets register's fields are not free text -------
    cache = os.environ.get("HOLLOW_CACHE", ".hollow-cache")
    ds_path = os.path.join(cache, "datasets.json")
    ds_posthoc = {"post_hoc": True,
                  "note": "P5 named three fields as free text without checking their cardinality. "
                          "Two of the three are controlled vocabularies, on which the duplicate "
                          "rule R4 flags everything by construction."}
    if os.path.exists(ds_path):
        ds = json.load(open(ds_path))["entries"]
        for f in ("relevanz", "pruef_vermerk", "aufnahmegrund"):
            vals = [str(e.get(f) or "") for e in ds]
            ne = [v for v in vals if norm(v)]
            dd = duplicate_keys(ne)
            flags = [classify(v, dd) for v in ne]
            ds_posthoc[f] = {
                "n_nonempty": len(ne),
                "distinct_values": len(set(norm(v).casefold() for v in ne)),
                "is_free_text_by_cardinality": len(set(norm(v).casefold() for v in ne)) > 0.5 * len(ne),
                "hollow_strict_with_r4": sum(1 for x in flags if x["hollow_strict"]),
                "hollow_strict_without_r4": sum(1 for x in flags if x["r1_chrome"]),
            }
    else:
        ds_posthoc["unavailable"] = f"no cached datasets feed at {ds_path}"

    # --- post-hoc 3: effective completeness of the content field ------------
    n = len(rows)
    eff = {
        "post_hoc": True,
        "field": "decisive_move",
        "declared_completeness_pct": 100.0,
        "effective_completeness_broad_pct": round(100 * (1 - sum(1 for r in rows if r["hollow_broad"]) / n), 2),
        "effective_completeness_strict_pct": round(100 * (1 - sum(1 for r in rows if r["hollow_strict"]) / n), 2),
        "effective_completeness_hand_pct": round(100 - out["hand_unusable_pct"], 2),
        "hand_ci95_pct": [round(100 - out["hand_unusable_ci95"][1], 2),
                          round(100 - out["hand_unusable_ci95"][0], 2)],
    }
    # register-wide corrected completeness, all cells
    atlas_cells = results["declared_missing"]["atlas"]["cells"]
    atlas_missing = results["declared_missing"]["atlas"]["declared_missing"]
    eff["register_completeness_declared_pct"] = results["declared_missing"]["atlas"]["completeness_pct"]
    for tag, k in (("broad", sum(1 for r in rows if r["hollow_broad"])),
                   ("strict", sum(1 for r in rows if r["hollow_strict"]))):
        eff[f"register_completeness_corrected_{tag}_pct"] = round(
            100 * (atlas_cells - atlas_missing - k) / atlas_cells, 2)
    eff["papers_declared_pct"] = results["declared_missing"]["papers"]["completeness_pct"]
    eff["datasets_declared_pct"] = results["declared_missing"]["datasets"]["completeness_pct"]

    payload = {"validation": out, "post_hoc_provenance": posthoc,
               "post_hoc_datasets_fields": ds_posthoc, "post_hoc_effective_completeness": eff}
    with open(os.path.join(OUT, "validation.json"), "w") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
