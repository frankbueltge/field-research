#!/usr/bin/env python3
"""Fold the four baseline runs into one ledger-schema run file, so day 2 diffs against all of them.

WHY THIS EXISTS. The corpus that the pre-registered window governs was baselined by **four**
separate runs, not one: session 110's ledger run of 2,904 units, and session 111's three
expansion baseline runs (635 + 304 + 26) made in the last ninety minutes before 00:00Z on the
12th. `ledger_diff.py` takes two files. Diffing day 2 against only one of them would treat the
other three runs' identifiers as absent from run 1 — they would drop out of `common` silently and
carry no exposure at all, which is exactly the failure `NEXT-SESSION.md` was written to prevent
(it warns about the manifest; the same trap sits one step later, in the diff).

WHAT IT MAY NOT DO. It may not classify. The state written into the union is the state the
producing run already recorded, and where a run predates the schema the classifier is imported
from `ledger_diff.py` rather than written again here — one classifier for the whole arc, which is
the rule session 109 set when it read session 109's census through an adapter instead of a second
implementation.

WHAT IT REFUSES. If any unit appears in more than one baseline run with **different** states, the
union is not written. That would mean an identifier was observed twice before the window opened
and moved in between — a pre-window transition, which is a finding and not something to average.
It is reported and the script exits non-zero.

Usage:
    python3 build_baseline_union.py OUT.json RUN1.json RUN2.json ...
"""
import json
import sys

from ledger_diff import classify, load  # one classifier for the whole arc

SCHEMA = "field-research/retrievability-ledger/1"


def main(out_path, *runs):
    merged, provenance, conflicts = {}, [], []
    for path in runs:
        r = load(path)                      # ledger_diff's own reader, schema or census adapter
        raw = json.load(open(path))
        provenance.append({"path": path, "label": r["label"], "start": r["start"],
                           "asn": r["vantage"].get("asn"), "observations": len(r["obs"])})
        for vid, rec in r["obs"].items():
            vid = str(vid)
            if vid in merged and merged[vid]["state"] != rec["state"]:
                conflicts.append({"vid": vid, "first": merged[vid]["state"],
                                  "first_from": merged[vid]["_from"],
                                  "second": rec["state"], "second_from": path})
                continue
            keep = dict(rec)
            keep["vid"] = vid
            keep["_from"] = path
            merged[vid] = keep

    asns = sorted({p["asn"] for p in provenance})
    union = {
        "schema": SCHEMA,
        "run_id": "baseline-union (session 110 run + session 111 baselines 1-3)",
        "run_utc_start": min(p["start"] for p in provenance),
        "run_utc_end": max(p["start"] for p in provenance),
        "vantage": {"asn": asns[0] if len(asns) == 1 else "MIXED — " + ",".join(asns),
                    "source": "carried from the producing runs; see components",
                    "note": ("This is not a run. It is the union of the runs that gave every unit "
                             "in the window's manifest its pre-window state. The vantage field "
                             "exists so ledger_diff's vantage guard can still refuse a comparison "
                             "across autonomous systems.")},
        "components": provenance,
        "conflicts_pre_window": conflicts,
        "observations": [{k: v for k, v in rec.items() if k != "_from"} | {"baseline_from": rec["_from"]}
                         for rec in merged.values()],
    }
    if conflicts:
        print(json.dumps({"REFUSED": "units disagree across baseline runs",
                          "n_conflicts": len(conflicts), "conflicts": conflicts[:10]}, indent=1))
        return 1
    json.dump(union, open(out_path, "w"), indent=1)
    counts = {}
    for rec in union["observations"]:
        counts.setdefault(rec["arm"], {}).setdefault(rec["state"], 0)
        counts[rec["arm"]][rec["state"]] += 1
    print(json.dumps({"out": out_path, "units": len(merged), "components": provenance,
                      "asn": union["vantage"]["asn"], "counts": counts}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], *sys.argv[2:]))
