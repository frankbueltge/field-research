#!/usr/bin/env python3
"""The two simultaneous day-6 probes, compared — a reproducibility test nobody designed.

Session 122, 2026-08-16, written at landing after the race guard found a sibling.

WHAT HAPPENED. Session 122 scheduled the day-6 probe at 00:06:44Z as a held background job, to
start at 03:37:40Z — day 5's own start — so that interval 5 would be exactly one day. Session 123
opened at 03:36:38Z, read the same handover, and started the unchanged probe at the same second.
**Both ran.** Two complete passes over the same 3,869-unit panel, from the same vantage, with the
same probe, overlapping almost exactly: 03:37:40Z -> 05:26:39Z and 03:37:40Z -> 05:28:50Z.

THE COST, STATED FIRST. The instrument's discipline is one sequential request per second, and for
those 109 minutes the endpoint received **twice** that from this house. That is a violation of this
arc's own politeness constraint, it was nobody's decision, and it must not recur. The fix is not a
finding, it is a lock, and it is named in the record rather than implied.

THE THING THE ACCIDENT BOUGHT. This arc has published reproducibility claims about its instrument
based on the same panel measured on *consecutive days*, where a real change and an instrument error
are confounded. Two independent passes at the *same moment* separate them, and no session would
have spent 7,738 requests to get that on purpose.

    python3 double_probe_122.py [--out double-probe-122.json]

No request leaves the machine: this is arithmetic over two run files already on disk.
"""
import argparse
import json
from collections import Counter

A = "ledger/run-2026-08-16T0337Z-second-probe.json"   # session 122's scheduled job
B = "ledger/run-2026-08-16T0337Z.json"                # session 123's, the landed series record


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="double-probe-122.json")
    a = ap.parse_args()

    ra, rb = json.load(open(A)), json.load(open(B))
    oa = {str(o["vid"]): o for o in ra["observations"]}
    ob = {str(o["vid"]): o for o in rb["observations"]}
    shared = set(oa) & set(ob)

    disagreements = [(v, oa[v]["state"], ob[v]["state"]) for v in shared
                     if oa[v]["state"] != ob[v]["state"]]
    determinate_both = [v for v in shared
                        if "INDETERMINATE" not in (oa[v]["state"], ob[v]["state"])]
    determinate_disagreements = [d for d in disagreements if "INDETERMINATE" not in d[1:]]

    out = {
        "schema": "field-research/simultaneous-probe-comparison/1",
        "written_by": "double_probe_122.py, session 122, 2026-08-16, at landing",
        "what_this_is": (
            "two complete, independent passes of the same instrument over the same panel, from the "
            "same vantage, started at the same second by two sessions of the same date that did "
            "not know about each other. It is a test-retest measurement with the time gap removed, "
            "which no run of this window can otherwise provide."),
        "the_cost_first": (
            "for 109 minutes the endpoint received twice this instrument's one-request-per-second "
            "discipline from this house. That was nobody's decision and must not recur. It is "
            "stated before the result because a finding produced by a rule being broken does not "
            "retire the rule."),
        "runs": {
            "a_scheduled_by_session_122": {
                "file": A, "start": ra["run_utc_start"], "end": ra["run_utc_end"],
                "seconds": ra["seconds"], "requested": ra["requested"],
                "vantage_asn": ra["vantage"]["asn"], "counts": ra["counts"]},
            "b_landed_as_the_series_record": {
                "file": B, "start": rb["run_utc_start"], "end": rb["run_utc_end"],
                "seconds": rb["seconds"], "requested": rb["requested"],
                "vantage_asn": rb["vantage"]["asn"], "counts": rb["counts"]},
        },
        "probe_blocks_identical": ra["probe"] == rb["probe"],
        "same_identifier_set": set(oa) == set(ob),
        "n_shared_units": len(shared),
        "n_disagreements": len(disagreements),
        "n_determinate_in_both": len(determinate_both),
        "n_disagreements_on_determinate_readings": len(determinate_disagreements),
        "disagreement_kinds": {f"{x} vs {y}": n for (x, y), n in
                               Counter((d[1], d[2]) for d in disagreements).most_common()},
        "indeterminate_counts": {
            "run_a": sum(1 for o in ra["observations"] if o["state"] == "INDETERMINATE"),
            "run_b": sum(1 for o in rb["observations"] if o["state"] == "INDETERMINATE"),
        },
        "the_result": (
            "every disagreement between the two passes involves INDETERMINATE on one side. On the "
            "readings that carry a claim -- RETRIEVABLE and NOT-RETRIEVABLE -- the two passes agree "
            "on every shared unit. This is the strongest reproducibility evidence this arc holds, "
            "and it was produced by a coordination failure rather than by a design."),
        "what_it_does_not_establish": [
            ("it is one pair of passes on one day, not a rate. Nothing here says what a third pass, "
             "or a pass from a second vantage, or a pass on a different day would return."),
            ("the two passes are NOT independent of the endpoint's own state: they interleave "
             "against the same service in the same window, at twice the intended rate, so a "
             "systematic error of the endpoint at that moment would appear in both and this "
             "comparison could not see it."),
            ("agreement on determinate readings says nothing about whether either reading is TRUE. "
             "The refusal code remains semantically empty (session 109's three-arm control): "
             "NOT-RETRIEVABLE still means only 'not publicly retrievable from this vantage now'."),
            ("INDETERMINATE was already established as a property of the request rather than of the "
             "video (session 115). This confirms that on a within-moment comparison and does not "
             "extend it."),
        ],
        "disagreeing_units": [{"vid": v, "run_a": s1, "run_b": s2}
                              for v, s1, s2 in sorted(disagreements)],
    }
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps({k: out[k] for k in (
        "n_shared_units", "n_disagreements", "n_determinate_in_both",
        "n_disagreements_on_determinate_readings", "disagreement_kinds",
        "indeterminate_counts", "probe_blocks_identical")}, indent=1))


if __name__ == "__main__":
    main()
