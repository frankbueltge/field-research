#!/usr/bin/env python3
"""Diff two ledger runs and report state transitions.

Enforces two rules the arc committed to before it had any results to protect:

1. **Vantage guard.** If the two runs were made from different autonomous systems, the runs are
   **flagged and not compared** (`vantage-2026-08-11.md`, condition 2 of the adversary's
   verdict). A single egress point cannot distinguish a video that was removed from one that
   became unavailable *from this location*; comparing across two egress points would silently
   convert a routing difference into a finding.

2. **Determinate states only.** A transition is a change between RETRIEVABLE and
   NOT-RETRIEVABLE. Anything touching INDETERMINATE — a transport error, a timeout, any other
   status — is reported separately and never counted as a transition.

Run 1 (session 109's census) predates this schema, so it is read through an adapter that
applies the *same* classification function rather than a second one written for it.
"""
import json
import sys


def classify(rec):
    if rec.get("http") == 200 and not rec.get("parse_error"):
        return "RETRIEVABLE"
    if rec.get("http") == 400:
        return "NOT-RETRIEVABLE"
    return "INDETERMINATE"


def load(path):
    d = json.load(open(path))
    if d.get("schema", "").startswith("field-research/retrievability-ledger/"):
        obs = {r["vid"]: r for r in d["observations"]}
        van = d["vantage"]
        label = d["run_id"]
        start = d["run_utc_start"]
    else:                                  # session 109's census — the same classifier applied
        obs = {r["vid"]: dict(r, state=classify(r)) for r in d["results"]}
        van = {"asn": "AS396982", "ip": "160.79.106.131",
               "source": "vantage-2026-08-11.md (recorded for the session, not per run)"}
        label = "census (session 109)"
        start = d["run_utc_start"]
    return {"path": path, "label": label, "start": start, "vantage": van, "obs": obs}


def main(p1, p2, out_path):
    r1, r2 = load(p1), load(p2)

    same_vantage = r1["vantage"].get("asn") == r2["vantage"].get("asn")
    guard = {"run1_asn": r1["vantage"].get("asn"), "run2_asn": r2["vantage"].get("asn"),
             "same_autonomous_system": same_vantage,
             "verdict": "COMPARABLE" if same_vantage else
                        "FLAGGED — vantage moved between runs; the runs are not compared"}

    common = sorted(set(r1["obs"]) & set(r2["obs"]))
    both_determinate, transitions, indeterminate_edges = [], [], []
    for vid in common:
        s1, s2 = r1["obs"][vid]["state"], r2["obs"][vid]["state"]
        if "INDETERMINATE" in (s1, s2):
            indeterminate_edges.append({"vid": vid, "from": s1, "to": s2})
            continue
        both_determinate.append(vid)
        if s1 != s2:
            transitions.append({"vid": vid, "from": s1, "to": s2,
                                "handle": r2["obs"][vid].get("handle"),
                                "run1_http": r1["obs"][vid].get("http"),
                                "run2_http": r2["obs"][vid].get("http")})

    report = {
        "run1": {"path": p1, "label": r1["label"], "start": r1["start"],
                 "asn": r1["vantage"].get("asn"), "n": len(r1["obs"])},
        "run2": {"path": p2, "label": r2["label"], "start": r2["start"],
                 "asn": r2["vantage"].get("asn"), "n": len(r2["obs"])},
        "vantage_guard": guard,
        "observed_in_both": len(common),
        "determinate_in_both": len(both_determinate),
        "touching_indeterminate": len(indeterminate_edges),
        "transitions": transitions if same_vantage else [],
        "n_transitions": len(transitions) if same_vantage else None,
        "disagreement_rate_pct": (round(100 * len(transitions) / len(both_determinate), 3)
                                  if same_vantage and both_determinate else None),
        "indeterminate_edges": indeterminate_edges,
        "note": ("A transition is a dated change in public retrievability from this vantage. "
                 "It is not a deletion: session 109's three-arm control established the "
                 "platform's HTTP 400 is semantically empty — removal, geo-restriction from "
                 "this one vantage, a privacy change and an identifier that never existed are "
                 "indistinguishable through this endpoint."),
    }
    json.dump(report, open(out_path, "w"), indent=1)
    print(json.dumps({k: v for k, v in report.items()
                      if k not in ("transitions", "indeterminate_edges", "note")}, indent=1))
    if transitions and same_vantage:
        print("\nTRANSITIONS (each must survive an immediate re-request — K5):")
        for t in transitions:
            print(" ", t["vid"], t["from"], "->", t["to"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
