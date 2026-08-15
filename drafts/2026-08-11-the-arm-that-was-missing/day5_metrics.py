#!/usr/bin/env python3
"""day5_metrics - the interval-4 figures, computed into a file so the prose can be checked.

Session 120. This arc's standing rule is that a document may not quote a number that exists
nowhere but in the sentence quoting it. The interval length and the interval-4 rates were
computed in an ad-hoc shell during the session; this puts them on disk with the code that
makes them, so `prose_vs_json.py` can find them and anyone can recompute them.
"""
import calendar, json, math, time

D4, D5 = "ledger/run-2026-08-14T0343Z.json", "ledger/run-2026-08-15T0337Z.json"
CORR = "ledger/corrections.json"
t = lambda s: calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))


def wilson(k, n, z=1.959963985):
    if n == 0:
        return (None, None)
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


d4, d5 = json.load(open(D4)), json.load(open(D5))
corr = {(c["run_file"], str(c["vid"])): c for c in json.load(open(CORR))["corrections"]}


def states(run, path):
    out = {}
    for o in run["observations"]:
        s = o["state"]
        c = corr.get((path, str(o["vid"])))
        if c and s == c["state_in_run_file"]:
            s = c["corrected_state"]
        out[str(o["vid"])] = (o["arm"], s)
    return out


s4, s5 = states(d4, D4), states(d5, D5)
DET = ("RETRIEVABLE", "NOT-RETRIEVABLE")
ret = [v for v, (a, s) in s4.items()
       if a != "B-truncated" and s == "RETRIEVABLE" and s5.get(v, (0, 0))[1] in DET]
abs_ = [v for v, (a, s) in s4.items()
        if a != "B-truncated" and s == "NOT-RETRIEVABLE" and s5.get(v, (0, 0))[1] in DET]
losses = [v for v in ret if s5[v][1] == "NOT-RETRIEVABLE"]
returns = [v for v in abs_ if s5[v][1] == "RETRIEVABLE"]
lo, hi = wilson(len(losses), len(ret))

out = {
    "schema": "field-research/interval-metrics/1",
    "interval": 4,
    "arm": "overlay-corrected; the raw diff is the primary record and is published beside it",
    "run_from": d4["run_utc_start"], "run_to": d5["run_utc_start"],
    "interval_days": round((t(d5["run_utc_start"]) - t(d4["run_utc_start"])) / 86400, 4),
    "run_seconds": d5["seconds"], "requested": d5["requested"], "planned": d5["planned"],
    "stopped": d5["stopped"],
    "retrievable_at_day4_determinate_at_day5": len(ret),
    "confirmed_losses": len(losses), "loss_ids": losses,
    "loss_rate": len(losses) / len(ret) if ret else None,
    "loss_rate_wilson": [lo, hi],
    "absent_at_day4_determinate_at_day5": len(abs_),
    "returns": len(returns), "return_ids": returns,
    "note": ("a loss here is a reading that survived five immediate re-requests. NOT-RETRIEVABLE "
             "does not mean deleted - the endpoint's refusal is semantically empty."),
}
json.dump(out, open("day5-metrics.json", "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "note"}, indent=1))
