#!/usr/bin/env python3
"""rebuild_audit_123 - does a fresh build of the bundle agree with what was shipped?

Session 123, 2026-08-16. The bundle on disk is split-brained: `expectation.json` and
`FIGURES.md` from the session-120 build sit beside `*-CORRECTED-2026-08-16.*` written by
session 122's drift repair, and `MANIFEST.json` still hashes the superseded pair as if it
were the bundle. `memory/downstream-commitments.md` condition 10(c) states that defect as a
condition on other people's reuse. This session rebuilds instead.

Before rebuilding on a longer panel, this script asks the narrower question the session's own
bet is about: rebuilt AT THE SHIPPED CUT-OFF, with the same run files, does the current build
script reproduce what was shipped, and does it reproduce what session 122 published as the
correction?

Two comparisons, both leaf by leaf over the whole JSON tree:

  A. fresh build (cut-off 2026-08-14T23:59:59Z)  vs  the SHIPPED files
     Expected difference: the V1 reference-clock repair, and nothing else.
  B. fresh build (same cut-off)                  vs  the CORRECTED files of session 122
     Expected difference: NONE. Session 122 published these as the corrected values; if the
     build script that session repaired does not reproduce them, one of the two is wrong.

Any leaf that differs in A but is NOT a band-derived leaf, or any leaf that differs at all in
B, is a further defect - which is exactly what this session bet it would find.

Usage:  python3 rebuild_audit_123.py FRESH_DIR [--out rebuild-audit-123.json]
"""
import argparse
import json
import os
import re
import sys

# Leaves whose value legitimately differs between two builds of the same panel because they
# record WHEN the build ran or WHERE its inputs sat, not what was measured. Named explicitly
# so that "expected to differ" is a stated list and not a judgement made while reading a diff.
BUILD_STAMP_KEYS = {"built_utc", "built_by", "generated_utc"}


def flatten(o, prefix=""):
    """Every leaf of a JSON tree as path -> value. Lists index by position."""
    if isinstance(o, dict):
        for k, v in o.items():
            yield from flatten(v, f"{prefix}.{k}" if prefix else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from flatten(v, f"{prefix}[{i}]")
    else:
        yield prefix, o


def leafdiff(a_path, b_path):
    """Leaf-by-leaf comparison of two JSON files. Returns (n_leaves, differences, only_a, only_b)."""
    A = dict(flatten(json.load(open(a_path))))
    B = dict(flatten(json.load(open(b_path))))
    diffs = []
    for k in sorted(set(A) & set(B)):
        if A[k] != B[k]:
            diffs.append({"path": k, "fresh": A[k], "other": B[k]})
    only_a = sorted(set(A) - set(B))
    only_b = sorted(set(B) - set(A))
    return len(A), len(B), diffs, only_a, only_b


# An age-band label as this bundle writes them: `0-1y` ... `4-5y`, and the open top band `5y+`.
# Matched as a path SEGMENT, never as a substring of a longer word.
BAND_LABEL = re.compile(r"^(\d+-\d+y|\d+y\+)$")

# Leaf names that exist only because a figure is computed ACROSS age bands. `gradient-test.json`
# is the age-gradient test in its entirety, so every leaf of it is band-derived by construction;
# these names are listed anyway so the rule is readable without knowing that.
GRADIENT_KEYS = {"young", "old", "ratio_old_over_young", "fisher_two_sided_p",
                 "young_band", "old_band"}


def classify(path, filename=""):
    """Why is this leaf allowed to differ between a fresh build and the shipped one?

    Only two answers are accepted without a finding:
      build_stamp  - it records the build, not the measurement
      band_derived - it is a per-age-band cell, or a figure computed across bands, which is
                     exactly what the V1 reference-clock repair moves (session 122,
                     DRIFT-122.md): a unit's band is now read at the declared reference time
                     instead of at the first day of the panel.
    Everything else is UNEXPECTED and is a defect this session found.

    CORRECTED IN THE SESSION THAT WROTE IT, before the figure was published: the first version
    of this function tested `"band" in path`, which is a substring test that misses every path
    naming a band by its LABEL (`across_day_stability.0-1y.mean`) or by its role in the gradient
    (`results[0].ratio_old_over_young`). It reported 97 UNEXPECTED leaves that were all
    band-derived. The count is not corrected by hand here; the rule is corrected and re-run.
    """
    segs = [s for p in path.split(".") for s in [p.split("[")[0]] if s]
    last = segs[-1] if segs else ""
    if last in BUILD_STAMP_KEYS:
        return "build_stamp"
    if os.path.basename(filename).startswith("gradient-test"):
        return "band_derived"
    if last in GRADIENT_KEYS:
        return "band_derived"
    if any(BAND_LABEL.match(s) for s in segs):
        return "band_derived"
    if "band" in segs or "by_band" in segs or "bands" in segs:
        return "band_derived"
    return "UNEXPECTED"


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("fresh", help="directory of the fresh build at the shipped cut-off")
    ap.add_argument("--shipped", default="deliverable")
    ap.add_argument("--out", default="rebuild-audit-123.json")
    a = ap.parse_args(argv)

    pairs = [
        ("A_vs_shipped", "expectation.json", "expectation.json"),
        ("A_vs_shipped", "reference-baseline.json", "reference-baseline.json"),
        ("A_vs_shipped", "gradient-test.json", "gradient-test.json"),
        ("B_vs_corrected", "expectation.json", "expectation-CORRECTED-2026-08-16.json"),
        ("B_vs_corrected", "reference-baseline.json", "reference-baseline-CORRECTED-2026-08-16.json"),
        ("B_vs_corrected", "gradient-test.json", "gradient-test-CORRECTED-2026-08-16.json"),
    ]

    result = {"schema": "field-research/rebuild-audit/1",
              "session": 123,
              "fresh_build_dir": a.fresh,
              "shipped_dir": a.shipped,
              "comparisons": []}

    for group, fresh_name, other_name in pairs:
        fp = os.path.join(a.fresh, fresh_name)
        op = os.path.join(a.shipped, other_name)
        if not (os.path.exists(fp) and os.path.exists(op)):
            result["comparisons"].append({"group": group, "fresh": fp, "other": op,
                                          "status": "MISSING"})
            continue
        n_a, n_b, diffs, only_a, only_b = leafdiff(fp, op)
        by_class = {}
        for d in diffs:
            d["class"] = classify(d["path"], other_name)
            by_class[d["class"]] = by_class.get(d["class"], 0) + 1
        result["comparisons"].append({
            "group": group,
            "fresh": fp,
            "other": op,
            "leaves_fresh": n_a,
            "leaves_other": n_b,
            "n_differing": len(diffs),
            "by_class": by_class,
            "only_in_fresh": only_a[:40],
            "n_only_in_fresh": len(only_a),
            "only_in_other": only_b[:40],
            "n_only_in_other": len(only_b),
            "unexpected": [d for d in diffs if d["class"] == "UNEXPECTED"][:60],
            "n_unexpected": sum(1 for d in diffs if d["class"] == "UNEXPECTED"),
        })

    result["verdict"] = {
        "B_reproduces_session_122_correction": all(
            c.get("n_differing", 1) - c.get("by_class", {}).get("build_stamp", 0) == 0
            for c in result["comparisons"] if c["group"] == "B_vs_corrected"),
        "n_unexpected_total": sum(c.get("n_unexpected", 0) for c in result["comparisons"]),
    }
    json.dump(result, open(a.out, "w"), indent=1)
    print(json.dumps(result["verdict"], indent=1))
    for c in result["comparisons"]:
        print(f'{c["group"]:16s} {os.path.basename(c["other"]):45s} '
              f'diff={c.get("n_differing")} unexpected={c.get("n_unexpected")} '
              f'onlyfresh={c.get("n_only_in_fresh")} onlyother={c.get("n_only_in_other")}')
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
