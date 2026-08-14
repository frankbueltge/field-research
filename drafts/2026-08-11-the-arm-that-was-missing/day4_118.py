#!/usr/bin/env python3
"""Day 4 of the pre-registered window: the interval, its exposures, and the artefact echo.

Session 118, 2026-08-14. No new request: this reads the four run files already on disk and the
three confirmation files beside them.

The one thing this session found that nobody had looked for: `confirm_transition.py` refutes an
apparent transition but DOES NOT CORRECT THE LEDGER, so a refuted reading survives in the run
file and manufactures a spurious transition in the NEXT interval. Quantified here.

Usage: python3 day4_118.py
"""
import json
import math

RUNS = [("baseline", "ledger/baseline-union.json"),
        ("day2", "ledger/run-2026-08-12T0341Z.json"),
        ("day3", "ledger/run-2026-08-13T0427Z.json"),
        ("day4", "ledger/run-2026-08-14T0343Z.json")]
CONFIRMS = {"interval1": "ledger/transition-confirm-2026-08-12.json",
            "interval2": "ledger/transition-confirm-2026-08-13.json",
            "interval3": "ledger/transition-confirm-2026-08-14.json"}
DEFF = 1.9900          # session 116's crossed design effect, for a simple proportion


def states(path):
    d = json.load(open(path))
    obs = d["observations"] if "observations" in d else d["units"]
    return ({str(o["vid"]): o["state"] for o in obs},
            {str(o["vid"]): o.get("arm") for o in obs}, d)


def wilson(x, n, deff=1.0, z=1.959963985):
    if n == 0:
        return [None, None]
    ne = n / deff
    p = x / n
    den = 1 + z * z / ne
    c = (p + z * z / (2 * ne)) / den
    h = z * math.sqrt(p * (1 - p) / ne + z * z / (4 * ne * ne)) / den
    return [max(0.0, c - h), min(1.0, c + h)]


def main():
    S, A, D = {}, {}, {}
    for lab, path in RUNS:
        S[lab], A[lab], D[lab] = states(path)

    conf = {}
    for k, path in CONFIRMS.items():
        d = json.load(open(path))
        conf[k] = {r["vid"]: r for r in d.get("results", [])}
        conf[k + "_K4"] = d.get("K4")

    out = {"schema": "field-research/window-day4/1", "session": 118, "date": "2026-08-14",
           "runs": {lab: {"start": D[lab].get("run_utc_start"),
                          "n": len(S[lab]),
                          "asn": (D[lab].get("vantage") or {}).get("asn")} for lab, _ in RUNS}}

    # ---- interval 3 in full, unit by unit, with each unit's whole history
    hist = {}
    for vid, r in conf["interval3"].items():
        hist[vid] = {"handle": r["handle"], "from": r["from"], "to": r["to"],
                     "verdict": r["verdict"],
                     "history": {lab: S[lab].get(vid) for lab, _ in RUNS}}
    out["interval3_transitions"] = hist
    out["interval3_K4"] = conf["interval3_K4"]

    # ---- the artefact echo: a refuted reading left in the ledger reappears next interval
    echo = []
    for vid, r in conf["interval3"].items():
        for earlier in ("interval1", "interval2"):
            e = conf.get(earlier, {}).get(vid)
            if e and "NOT CONFIRMED" in e["verdict"]:
                echo.append({"vid": vid, "handle": r["handle"],
                             "refuted_in": earlier, "refuted_reading": e["to"],
                             "counted_again_in": "interval3", "as": f"{r['from']} -> {r['to']}",
                             "history": {lab: S[lab].get(vid) for lab, _ in RUNS}})
    out["artefact_echo"] = {
        "cases": echo,
        "mechanism": ("confirm_transition.py refutes a reading but does not correct the run "
                      "file; the refuted state stays in the ledger and the next interval's diff "
                      "reports the reversal as a fresh transition"),
    }

    # ---- the honest count over three intervals
    genuine = {"returns": [], "losses": [], "refuted": [], "echoes": [e["vid"] for e in echo]}
    for k in ("interval1", "interval2", "interval3"):
        for vid, r in conf[k].items():
            if "NOT CONFIRMED" in r["verdict"]:
                genuine["refuted"].append({"interval": k, "vid": vid, "claimed": r["to"]})
            elif vid in genuine["echoes"] and k == "interval3":
                pass                                   # counted in the echo block, not here
            elif r["to"] == "RETRIEVABLE":
                genuine["returns"].append({"interval": k, "vid": vid, "handle": r["handle"]})
            else:
                genuine["losses"].append({"interval": k, "vid": vid, "handle": r["handle"]})
    out["three_intervals"] = {
        "confirmed_returns": len(genuine["returns"]),
        "confirmed_losses": len(genuine["losses"]),
        "apparent_transitions_refuted_by_re_request": len(genuine["refuted"]),
        "echoes_excluded_from_the_count": len(genuine["echoes"]),
        "detail": genuine,
    }

    # ---- exposure: who was at risk of returning, and of being lost, in interval 3
    det = [v for v in S["day3"]
           if S["day3"][v] in ("RETRIEVABLE", "NOT-RETRIEVABLE")
           and S["day4"].get(v) in ("RETRIEVABLE", "NOT-RETRIEVABLE")
           and A["day3"].get(v) != "B-truncated"]
    absent3 = [v for v in det if S["day3"][v] == "NOT-RETRIEVABLE"]
    present3 = [v for v in det if S["day3"][v] == "RETRIEVABLE"]
    ret = sum(1 for v in absent3 if S["day4"][v] == "RETRIEVABLE"
              and v not in genuine["echoes"])
    los = sum(1 for v in present3 if S["day4"][v] == "NOT-RETRIEVABLE"
              and any(vid == v and "NOT CONFIRMED" not in r["verdict"]
                      for vid, r in conf["interval3"].items()))
    out["interval3_exposure"] = {
        "determinate_in_both_excluding_B_truncated": len(det),
        "absent_on_day3": len(absent3), "confirmed_returns": ret,
        "present_on_day3": len(present3), "confirmed_losses": los,
        "return_rate_per_interval": ret / len(absent3),
        "return_rate_wilson_binomial": wilson(ret, len(absent3)),
        "return_rate_wilson_widened_at_crossed_deff": wilson(ret, len(absent3), DEFF),
        "loss_rate_per_interval": los / len(present3),
        "loss_rate_wilson_widened_at_crossed_deff": wilson(los, len(present3), DEFF),
        "deff_used": DEFF,
        "caveat": ("three events over three intervals; the design effect applied here is the "
                   "absence proportion's, which is the statistic it was measured on, and this "
                   "is a rate on a different population. Thin, and stated as thin."),
    }

    # ---- P118-1
    five = {"7234121532635761926": "bruno_martiinez",
            "7230168662945189126": "monicaaquino191",
            "7228741383975095558": "payo_junior_oficial",
            "7193104172198202625": "sbsaustralia",
            "7251623512144743686": "lazpiyanist"}
    turned = {v: S["day4"].get(v) for v in five}
    n_turned = sum(1 for s in turned.values() if s == "NOT-RETRIEVABLE")
    out["P118_1"] = {
        "population": five, "day4_states": turned, "n_turned": n_turned,
        "holds": n_turned < 3,
        "rule_of_three_upper_95_on_propagation": 1 - 0.05 ** (1 / len(five)),
        "note": ("written and committed at 03:46Z with the run unfinished and no observation "
                 "from it opened"),
    }

    # ---- indeterminacy, the standing observation
    ind = {lab: sum(1 for s in S[lab].values() if s == "INDETERMINATE") for lab, _ in RUNS}
    rep = len({v for v in S["day3"] if S["day3"][v] == "INDETERMINATE"} &
              {v for v in S["day4"] if S["day4"][v] == "INDETERMINATE"})
    out["indeterminate"] = {"per_run": ind, "repeated_day3_to_day4": rep,
                            "note": "indeterminacy is a property of the request, not the video"}

    json.dump(out, open("day4-118.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "interval3_transitions"}, indent=1))
    print("wrote day4-118.json")


if __name__ == "__main__":
    main()
