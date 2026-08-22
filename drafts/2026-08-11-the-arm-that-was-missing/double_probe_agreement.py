#!/usr/bin/env python3
"""double_probe_agreement - what the accidental same-second replicates say about this instrument.

Session 131, 2026-08-22.

Twice in this series two complete probes of the same 3,869-unit panel have run at the same start
second from two different network vantages inside one autonomous system:

  2026-08-16  two sessions of one date, one holding and one opening a minute before the hour
              (`DOUBLE-PROBE-122.md`)
  2026-08-22  two sessions of one date in two separate checkouts, which `run_window_day.py`'s own
              docstring names as the case its lock cannot see: "Two probes launched from two
              separate checkouts of this repository cannot see each other's reservation and this
              would not stop them."

Both were recorded as accidents. Neither was ever read as what it also is: a REPLICATE - the same
question asked twice, at once, by two independent runs. This script reads them that way. It adds no
measurement; it re-reads two pairs of committed run files.

WHAT IT COMPUTES, and the distinction is the whole point:
  - agreement on DETERMINATE verdicts: identifiers both probes called RETRIEVABLE or
    NOT-RETRIEVABLE, and whether the two calls match;
  - the INDETERMINATE boundary: identifiers one probe could not classify and the other could.
The first is the instrument's reproducibility. The second is where it is soft, and reporting only
the first would overstate the instrument.

Offline. Reads committed files only, makes no request.
"""
import json
import sys

PAIRS = [
    ("2026-08-16", "ledger/run-2026-08-16T0337Z.json",
     "ledger/run-2026-08-16T0337Z-second-probe.json"),
    ("2026-08-22", "ledger/run-2026-08-22T0341Z.json",
     "ledger/run-2026-08-22T0341Z-second-probe.json"),
]


def states(path):
    d = json.load(open(path))
    return ({str(o["vid"]): o["state"] for o in d["observations"]}, d)


def main():
    out = {
        "schema": "field-research/double-probe-agreement/1",
        "computed_by": "double_probe_agreement.py, session 131",
        "what_this_is": (
            "the two same-second, two-vantage replicates this series has produced by accident, "
            "read as replicates. No new measurement; two pairs of committed run files re-read."
        ),
        "pairs": [],
    }
    tot_det, tot_agree = 0, 0
    for date, p1, p2 in PAIRS:
        s1, d1 = states(p1)
        s2, d2 = states(p2)
        both = [v for v in s1 if v in s2]
        det_both = [v for v in both
                    if s1[v] != "INDETERMINATE" and s2[v] != "INDETERMINATE"]
        agree = [v for v in det_both if s1[v] == s2[v]]
        disagree = [{"vid": v, "run1": s1[v], "run2": s2[v]}
                    for v in det_both if s1[v] != s2[v]]
        only1 = [v for v in both if s1[v] == "INDETERMINATE" and s2[v] != "INDETERMINATE"]
        only2 = [v for v in both if s2[v] == "INDETERMINATE" and s1[v] != "INDETERMINATE"]
        both_ind = [v for v in both
                    if s1[v] == "INDETERMINATE" and s2[v] == "INDETERMINATE"]
        tot_det += len(det_both)
        tot_agree += len(agree)
        out["pairs"].append({
            "date": date,
            "run1": {"file": p1, "ip": d1["vantage"]["ip"], "asn": d1["vantage"]["asn"],
                     "start": d1["run_utc_start"], "end": d1["run_utc_end"],
                     "seconds": d1["seconds"]},
            "run2": {"file": p2, "ip": d2["vantage"]["ip"], "asn": d2["vantage"]["asn"],
                     "start": d2["run_utc_start"], "end": d2["run_utc_end"],
                     "seconds": d2["seconds"]},
            "same_start_second": d1["run_utc_start"] == d2["run_utc_start"],
            "different_vantage_ip": d1["vantage"]["ip"] != d2["vantage"]["ip"],
            "same_autonomous_system": d1["vantage"]["asn"] == d2["vantage"]["asn"],
            "observed_in_both": len(both),
            "determinate_in_both": len(det_both),
            "agree": len(agree),
            "disagree": len(disagree),
            "disagreements": disagree,
            "indeterminate_in_run1_only": len(only1),
            "indeterminate_in_run2_only": len(only2),
            "indeterminate_in_both": len(both_ind),
        })
    out["totals"] = {
        "paired_determinate_readings": tot_det,
        "agreements": tot_agree,
        "disagreements": tot_det - tot_agree,
        "agreement_rate_pct": round(100.0 * tot_agree / tot_det, 4) if tot_det else None,
    }
    out["what_this_does_not_establish"] = (
        "Both vantages sit in the SAME autonomous system, so this measures reproducibility across "
        "two hosts of one network and says nothing about a vantage elsewhere. It is also two days "
        "out of eleven, both chosen by accident rather than design. And it says nothing about "
        "whether a determinate verdict is CORRECT - only that the instrument returns the same one "
        "twice."
    )
    with open(sys.argv[1] if len(sys.argv) > 1 else "double-probe-agreement-131.json",
              "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps({"pairs": [{k: p[k] for k in
                                 ["date", "observed_in_both", "determinate_in_both", "agree",
                                  "disagree", "indeterminate_in_run1_only",
                                  "indeterminate_in_run2_only", "indeterminate_in_both"]}
                                for p in out["pairs"]],
                      "totals": out["totals"]}, indent=1))


if __name__ == "__main__":
    main()
