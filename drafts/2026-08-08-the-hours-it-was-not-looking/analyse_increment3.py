#!/usr/bin/env python3
"""analyse_increment3.py — everything the six sweeps say, in one place.

Written after the sweeps, not before: the pre-registered predictions are scored by
`score_increment3.py`; this collects the cross-series and cross-copy comparisons the
sweeps made possible and that no single series can answer.

Usage: analyse_increment3.py <scratch-dir> <out.json>
"""

from __future__ import annotations

import glob
import json
import os
import sys
from datetime import datetime, timedelta, timezone

FMT = "%Y%m%d%H%M%S"
STEP = timedelta(minutes=15)
W0, W1 = "20221110220000", "20221111183000"
SERIES = [("en", "gkg"), ("en", "export"), ("en", "mentions"),
          ("tr", "gkg"), ("tr", "export"), ("tr", "mentions")]


def load(path):
    header = footer = None
    rows = []
    for line in open(path, encoding="utf-8"):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("k") == "header":
            header = r
        elif r.get("k") == "footer":
            footer = r
        else:
            rows.append(r)
    return header, rows, footer


def runs(cycles):
    ts = sorted(datetime.strptime(c, FMT).replace(tzinfo=timezone.utc) for c in cycles)
    out, cur = [], []
    for t in ts:
        if cur and t - cur[-1] == STEP:
            cur.append(t)
        else:
            if cur:
                out.append(cur)
            cur = [t]
    if cur:
        out.append(cur)
    return out


def main():
    scratch, out = sys.argv[1], sys.argv[2]
    absent, meta, mism = {}, {}, {}
    for s, t in SERIES:
        p = os.path.join(scratch, f"sweep-{s}-{t}.jsonl")
        if not os.path.exists(p):
            meta[f"{s}-{t}"] = {"state": "NOT RUN"}
            continue
        h, rows, f = load(p)
        absent[(s, t)] = {r["c"] for r in rows if r["k"] == "absent"}
        mism[(s, t)] = [r for r in rows if r["k"] == "size-mismatch"]
        meta[f"{s}-{t}"] = {"state": "COMPLETE" if f else "PARTIAL",
                            "listed": (f or h).get("total"), "probed": (f or {}).get("done"),
                            "absent": (f or {}).get("absent"),
                            "size_mismatch": (f or {}).get("mismatch"),
                            "unresolved": (f or {}).get("unresolved"),
                            "other_status": (f or {}).get("other"),
                            "throttled": (f or {}).get("throttled"),
                            "seconds": (f or {}).get("elapsed_s"),
                            "rate_per_s": (f or {}).get("rate_per_s")}

    res = {"series": meta}
    total_probes = sum(m.get("probed") or 0 for m in meta.values())
    res["total_requests_to_the_file_host"] = total_probes
    res["total_unresolved"] = sum(m.get("unresolved") or 0 for m in meta.values())
    res["total_absent_files"] = sum(m.get("absent") or 0 for m in meta.values())

    union = set().union(*absent.values()) if absent else set()
    res["cycles_touched_by_any_absence"] = len(union)
    res["cycles_absent_in_every_series"] = len(set.intersection(*absent.values())) if absent else 0

    # which types fail together
    profile = {}
    for c in sorted(union):
        key = "+".join(f"{s}/{t}" for s, t in SERIES if c in absent.get((s, t), set()))
        profile.setdefault(key, []).append(c)
    res["failure_profiles"] = {k: {"cycles": len(v), "example": v[0], "first": v[0], "last": v[-1]}
                               for k, v in sorted(profile.items(), key=lambda kv: -len(kv[1]))}

    # runs per series and over the union
    res["runs"] = {}
    for (s, t), a in absent.items():
        rr = runs(a)
        res["runs"][f"{s}-{t}"] = {
            "runs": len(rr), "runs_ge_4": sum(1 for r in rr if len(r) >= 4),
            "top": [{"length": len(r), "first": r[0].strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "last": r[-1].strftime("%Y-%m-%dT%H:%M:%SZ")}
                    for r in sorted(rr, key=len, reverse=True)[:6]]}

    res["size_mismatches"] = {f"{s}-{t}": [{"cycle": m["c"], "declared": m["d"],
                                            "served": m["cl"]} for m in v]
                              for (s, t), v in mism.items() if v}

    # the free second copy, scored against the union of all six series
    api = []
    for f in sorted(glob.glob(os.path.join(scratch, "api-*.json"))):
        d = json.load(open(f))
        if "missing" not in d:
            api.append({"file": os.path.basename(f), "result": "UNRESOLVED"})
            continue
        miss = d["missing"]
        real = [c for c in miss if c in union]
        api.append({"file": os.path.basename(f), "start": d["start"], "end": d["end"],
                    "query": d.get("query"), "resolution": d.get("date_resolution"),
                    "quarter_hours": d["expected"], "returned": d["returned"],
                    "omitted": d["missing_count"],
                    "omitted_with_at_least_one_absent_file": len(real),
                    "omitted_with_every_file_served": d["missing_count"] - len(real)})
    res["free_second_copy"] = api
    fifteen = [a for a in api if a.get("resolution") == "15m"]
    res["free_second_copy_totals_at_15m"] = {
        "probes": len(fifteen),
        "quarter_hours_examined": sum(a["quarter_hours"] for a in fifteen),
        "omitted_by_the_api": sum(a["omitted"] for a in fifteen),
        "of_those_with_every_file_served": sum(a["omitted_with_every_file_served"]
                                               for a in fifteen),
        "of_those_with_a_genuinely_absent_file": sum(
            a["omitted_with_at_least_one_absent_file"] for a in fifteen)}

    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "free_second_copy"}, indent=1)[:4000])


if __name__ == "__main__":
    main()
