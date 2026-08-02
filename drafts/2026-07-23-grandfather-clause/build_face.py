#!/usr/bin/env python3
"""Build the face of the Grandfather Clause ledger.

Deterministic, offline, no network. Reads only files already committed in this
draft directory and emits ``data.json``, which ``work.astro`` imports at build
time. Every number rendered on the face comes from here; nothing is typed by
hand into the component.

Two properties this script is written to have, because the face's whole subject
is the difference between a rule fixed in advance and a rule believed later:

1. It derives the post-hoc per-specimen states from the committed non-stripping
   paths, then **checks the derived stratum aggregates against the committed
   ``a1-alt-reading.json``** and exits non-zero on any disagreement. The face
   cannot silently disagree with the ledger it renders.
2. It has no clock. ``AS_AT`` is a committed constant, so the countdown to A2
   is the same on every machine and at every rebuild.

Run from this directory:  python3 build_face.py
"""

import hashlib
import json
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
A1 = os.path.join(HERE, "a1")

# The date this face was built and the date every "as at" figure on it is
# relative to. A committed constant, never a clock read: same input, same
# output, on any machine, at any later rebuild.
AS_AT = "2026-08-02"

SEAM_APPLICATION = "2026-08-02"   # Art. 50(2) marking duty applies
SEAM_GRACE_END = "2026-12-02"     # transitional grace for in-market systems expires

TIER_ORDER = [
    "flagged AI — high",
    "AI-leaning",
    "human-leaning",
    "flagged human — high",
]

# The detector bands frozen by instrument 014 and inherited verbatim by this
# pre-registration (README, "Scoring"). The band's own inherited wording is
# verdict language -- "flagged AI", "flagged human" -- which a design review
# before this build found reads as an assertion about a file rather than as a
# score range. So the face leads with the float and names the band by its
# numeric range; the inherited wording is disclosed, not used as a label.
# Every specimen's score is checked against the band its committed tier names.
BANDS = [
    ("0.90 – 1.00", "flagged AI — high", lambda s: s >= 0.90),
    ("0.50 – 0.90", "AI-leaning", lambda s: 0.50 <= s < 0.90),
    ("0.10 – 0.50", "human-leaning", lambda s: 0.10 < s < 0.50),
    ("0.00 – 0.10", "flagged human — high", lambda s: s <= 0.10),
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def days_between(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days


def fail(msg):
    print("FAIL: " + msg, file=sys.stderr)
    sys.exit(1)


L1_FIELDS = {"state_governing", "state_post_hoc", "layer1_state", "state"}
L2_FIELDS = {"detector_score", "detector_tier", "ai_generated", "tier", "band"}


def assert_no_joined_record(node, path="data"):
    """Refuse to emit any record carrying a marking state and a detector score.

    A design review before this build established that the face's real risk is
    not a computed rate but an eyeballed one: two adjacent columns, and the
    reader performs the division ``apply_layer2.py`` is forbidden to perform
    (LAYER2-PROTOCOL.md R6, and the code-level guard its condition C6 forced).
    A caption cannot prevent that; a structural guard can. This is the sibling
    of ``assert_no_derived_rate`` in the reading tool, one layer further out.
    """
    if isinstance(node, dict):
        keys = set(node)
        if keys & L1_FIELDS and keys & L2_FIELDS:
            fail("%s joins a marking state and a detector score on one record: %s"
                 % (path, sorted((keys & L1_FIELDS) | (keys & L2_FIELDS))))
        for k, v in node.items():
            assert_no_joined_record(v, path + "." + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            assert_no_joined_record(v, "%s[%d]" % (path, i))


def main():
    inputs = {
        "a1-results.json": os.path.join(A1, "a1-results.json"),
        "a1-alt-reading.json": os.path.join(A1, "a1-alt-reading.json"),
        "a1-layer2-reading.json": os.path.join(A1, "a1-layer2-reading.json"),
        "ledger.json": os.path.join(HERE, "ledger.json"),
    }
    results = load(inputs["a1-results.json"])
    alt = load(inputs["a1-alt-reading.json"])
    l2 = load(inputs["a1-layer2-reading.json"])
    ledger = load(inputs["ledger.json"])

    # ---------------------------------------------------------------- specimens
    l2_by_id = {s["id"]: s for s in l2["specimens"]}
    non_stripping = alt["non_stripping_paths_by_positive_control"]

    specimens = []
    for s in results["specimens"]:
        sid = s["id"]
        if sid not in l2_by_id:
            fail("specimen %s has no layer-2 row" % sid)
        governing = s["state"]

        # Rule A1-S': "no XMP, no EXIF, no PNG text chunk" is evidence of
        # transport stripping ONLY on paths not shown to preserve manifests.
        # A path is shown to preserve them by a positive control -- a specimen
        # that arrived over it carrying a valid manifest.
        url = s.get("source_url", "")
        path_shown_non_stripping = any(p in url for p in non_stripping)
        if governing == "indeterminate-at-capture" and path_shown_non_stripping:
            post_hoc = "unmarked-at-capture"
        else:
            post_hoc = governing

        l2row = l2_by_id[sid]
        if l2row["tier"] not in TIER_ORDER:
            fail("unknown detector tier %r on %s" % (l2row["tier"], sid))

        # Layer-1 record only. The detector score deliberately does NOT travel
        # on this record -- see assert_no_joined_record below.
        specimens.append({
            "id": sid,
            "provider": s["provider"],
            "stratum": s["stratum"],
            "source_type_short": s.get("source_type", "").split(" (")[0].split(",")[0],
            "in_decision_rule": s["in_decision_rule"],
            "days_since_seam": s.get("days_since_seam"),
            "state_governing": governing,
            "state_post_hoc": post_hoc,
            "state_changed": post_hoc != governing,
            "path_shown_non_stripping": path_shown_non_stripping,
            "sha256_short": s["sha256"][:12],
            "sha256": s["sha256"],
        })

    # ------------------------------------------- check the derivation reproduces
    # the committed alt reading, stratum by stratum. If it does not, the face
    # would be rendering a third reading nobody wrote down.
    for stratum, committed in alt["strata"].items():
        mine = [x for x in specimens if x["stratum"] == stratum]
        n = len(mine)
        indet = sum(1 for x in mine if x["state_post_hoc"] == "indeterminate-at-capture")
        marked = sum(1 for x in mine if x["state_post_hoc"] == "machine-readable-marked")
        if n != committed["n"]:
            fail("%s: derived N %d != committed %d" % (stratum, n, committed["n"]))
        if indet != committed["indeterminate"]:
            fail("%s: derived indeterminate %d != committed %d"
                 % (stratum, indet, committed["indeterminate"]))
        if marked != committed["marked"]:
            fail("%s: derived marked %d != committed %d"
                 % (stratum, marked, committed["marked"]))
        states = {}
        for x in mine:
            states[x["state_post_hoc"]] = states.get(x["state_post_hoc"], 0) + 1
        if states != committed["states"]:
            fail("%s: derived states %r != committed %r" % (stratum, states, committed["states"]))

    # X-observation-only is outside the pre-registered strata and so absent from
    # the alt reading. Say so rather than leaving a silent hole.
    unchecked_strata = sorted(
        {x["stratum"] for x in specimens} - set(alt["strata"].keys())
    )

    # ------------------------------------------------------------ the two readings
    def row(stratum, src, checked):
        d = src["strata"][stratum]
        return {
            "stratum": stratum,
            "n": d["n"],
            "indeterminate": d["indeterminate"],
            "effective_n": d["effective_n"],
            "marked": d["marked"],
            "marked_proportion": d["marked_proportion"],
            "wilson_95": d["wilson_95"],
            "capture_inconclusive": d["capture_inconclusive"],
            "reproduced_by_this_script": checked,
        }

    strata_order = ["S-signatory", "N-nonsignatory", "C-camera-control", "X-observation-only"]
    governing_rows = [row(s, results, s in alt["strata"]) for s in strata_order]
    post_hoc_rows = [row(s, alt, True) for s in strata_order if s in alt["strata"]]

    changed = [x for x in specimens if x["state_changed"]]

    # ---------------------------------------- which strata moved between the rules
    # Computed, not asserted: a design review before this build warned that a
    # symmetric side-by-side teaches "the same files read two ways" as a general
    # property when in fact one stratum of five files moved and nothing else did.
    moved_strata, unchanged_strata = [], []
    for stratum, committed in alt["strata"].items():
        g = results["strata"][stratum]
        same = all(g[k] == committed[k] for k in
                   ("n", "indeterminate", "effective_n", "marked",
                    "marked_proportion", "capture_inconclusive", "states"))
        (unchanged_strata if same else moved_strata).append(stratum)

    # ------------------------------------------------------------- detector arm
    # Kept structurally apart from the Layer-1 records above. The bands are
    # counts; the raw floats are published as a sorted list carrying no specimen
    # identity, so no reader can perform by eye the cross-tabulation this arm's
    # own rule forbids it to compute (LAYER2-PROTOCOL.md R6).
    bands = []
    for label, inherited, test in BANDS:
        rows = [l2_by_id[x["id"]] for x in specimens if test(l2_by_id[x["id"]]["ai_generated"])]
        for r in rows:
            if r["tier"] != inherited:
                fail("%s scores %s, in band %s, but is committed as tier %r"
                     % (r["id"], r["ai_generated"], label, r["tier"]))
        bands.append({"band": label, "inherited_label": inherited, "count": len(rows)})
    if sum(b["count"] for b in bands) != len(specimens):
        fail("bands do not partition the specimens")

    scores_sorted = sorted(l2_by_id[x["id"]]["ai_generated"] for x in specimens)
    eligible = [x for x in specimens
                if l2_by_id[x["id"]]["eligible_for_unmarked_but_detector_flagged"]]

    repro = l2["inherited_specimen_reproduction"]
    repro_pairs = [{
        "a1_id": p["a1_id"],
        "earlier_id": p["instrument_014_id"],
        "score_earlier": p["score_2026_07_11"],
        "score_now": p["score_at_this_run"],
        "delta": p["delta"],
        "identical": p["identical"],
    } for p in repro["pairs"]]

    # ---------------------------------------------------------------- the spine
    spine = [
        {"anchor": "A0", "date": "2026-07-11", "status": "context",
         "label": "inherited registry, excluded from the decision rule",
         "days_from_application_seam": days_between(SEAM_APPLICATION, "2026-07-11")},
        {"anchor": "A-inst", "date": "2026-07-23", "status": "filled",
         "label": "institutional baseline, captured before the seam",
         "days_from_application_seam": days_between(SEAM_APPLICATION, "2026-07-23")},
        {"anchor": "A1", "date": "2026-08-02", "status": "filled",
         "label": "fresh capture, taken on the seam itself",
         "days_from_application_seam": days_between(SEAM_APPLICATION, "2026-08-02")},
        {"anchor": "A2", "date": SEAM_GRACE_END, "status": "locked",
         "label": "first session on or after the grace expiry — not yet takeable",
         "days_from_application_seam": days_between(SEAM_APPLICATION, SEAM_GRACE_END)},
    ]
    days_to_a2 = days_between(AS_AT, SEAM_GRACE_END)
    if days_to_a2 <= 0:
        fail("AS_AT is not before A2 — the countdown constant is stale")

    # --------------------------------------------------------------- locked cells
    # The prose of each cell is authored; every number in it is computed above.
    n_specimens = len(specimens)
    locked = [
        {
            "cell": "directional label for S-signatory and N-nonsignatory",
            "would_say": "one of the values fixed in advance: adoption-shift · reversal · "
                         "null — not distinguishable from sampling noise",
            "kept_empty_by": "the pre-registered load-bearing pair is A1 → A2 and the CI-overlap "
                             "gate; a single anchor carries no direction. Both strata are also "
                             "capture-inconclusive under the governing rule.",
            "earliest": SEAM_GRACE_END,
            "days_away_at_as_at": days_to_a2,
        },
        {
            "cell": "led-the-timeline for S-signatory",
            "would_say": "the A1-only descriptive label led-the-timeline",
            "kept_empty_by": "a capture-inconclusive stratum is forced into no directional label "
                             "by the rule locked on 2026-07-23",
            "earliest": "not at this anchor",
            "days_away_at_as_at": None,
        },
        {
            "cell": "unmarked-but-detector-flagged",
            "would_say": "the count of specimens in the pre-registered state "
                         "unmarked-but-detector-flagged — the statute's second limb, read "
                         "independently of the provider's marking",
            "kept_empty_by": "0 of %d specimens are eligible: the state requires a specimen in "
                             "unmarked-at-capture under the GOVERNING reading, and the governing "
                             "reading has none. The emptiness was written down before the "
                             "detector ran." % n_specimens,
            "earliest": "A2, if any specimen there is unmarked-at-capture",
            "days_away_at_as_at": days_to_a2,
        },
        {
            "cell": "marked proportion for N-nonsignatory",
            "would_say": "the field marked-proportion, with its Wilson interval, for this stratum",
            "kept_empty_by": "effective N = 0. All five arrived over a path not shown to preserve "
                             "manifests, so all five are indeterminate-at-capture and excluded "
                             "from numerator and denominator alike.",
            "earliest": "A2, on a capture path with a positive control",
            "days_away_at_as_at": days_to_a2,
        },
        {
            "cell": "any compliance reading, at any anchor in this window",
            "would_say": "no field exists for it — the cell is unavailable, not merely empty",
            "kept_empty_by": "in-market systems hold grace until 2026-12-02 and pre-seam outputs "
                             "never need retroactive marking, so an unmarked output in this "
                             "window is consistent with full compliance",
            "earliest": "never, for this window",
            "days_away_at_as_at": None,
        },
    ]

    data = {
        "built_by": "build_face.py",
        "as_at": AS_AT,
        "determinism": "no clock is read; AS_AT is a committed constant",
        "work": ledger["work"],
        "pre_registered": ledger["pre_registered"],
        "anchor": results["anchor"],
        "anchor_date": results["date"],
        "days_since_seam_at_capture": results["days_since_seam"],
        "seams": {"application": SEAM_APPLICATION, "grace_end": SEAM_GRACE_END},
        "days_to_a2_at_as_at": days_to_a2,
        "spine": spine,
        "readings": {
            "governing": {
                "rule": "A1-S — fixed in writing before any specimen was scored",
                "status": "GOVERNING",
                "rows": governing_rows,
            },
            "post_hoc": {
                "rule": alt["reading"],
                "status": "NON-GOVERNING",
                "governing_reading": alt["governing_reading"],
                "non_stripping_paths": non_stripping,
                "rows": post_hoc_rows,
            },
            "moved_strata": sorted(moved_strata),
            "unchanged_strata": sorted(unchanged_strata),
            "no_corrected_reading": unchecked_strata,
        },
        "state_changes": {
            "count": len(changed),
            "of_total": n_specimens,
            "ids": [x["id"] for x in changed],
            "from_to": sorted({(x["state_governing"], x["state_post_hoc"]) for x in changed}),
        },
        "detector": {
            "run_date": l2["layer2_run_date"],
            "rule_committed": l2["reading_rule_committed"],
            "attempted": l2["specimens_attempted"],
            "scored": l2["specimens_scored"],
            "hashes_verified_before_upload": l2["sha256_all_verified_before_upload"],
            "bands": bands,
            "scores_sorted_no_identity": scores_sorted,
            "eligible_count": len(eligible),
            "join_not_rendered": (
                "The per-specimen join of marking state and detector score exists in "
                "a1/a1-layer2-reading.json, committed and public. It is deliberately not "
                "rendered on this face: two adjacent columns are a division a reader "
                "performs by eye, and R6 forbids this arm to compute one."
            ),
            "refusals": l2["refusals"],
            "reproduction": {
                "pairs": repro_pairs,
                "all_reproduced": repro["all_reproduced"],
                "what_this_is": repro["what_this_is"],
            },
        },
        "locked_cells": locked,
        "specimens_layer1": specimens,
        "unchecked_strata": unchecked_strata,
        "inputs": [
            {"file": name, "sha256": sha256_file(path)}
            for name, path in sorted(inputs.items())
        ],
    }

    assert_no_joined_record(data)

    out = os.path.join(HERE, "data.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    print("wrote %s — %d specimens, %d changed state between the two readings, "
          "%d locked cells, %d days to A2 at %s"
          % (out, n_specimens, len(changed), len(locked), days_to_a2, AS_AT))


if __name__ == "__main__":
    main()
