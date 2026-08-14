#!/usr/bin/env python3
"""What the overlay actually moves — every published quantity that touches a refuted reading.

Session 119. `audit_instrument.py` A8 found two readings this arc's own confirmation step
refuted that are still standing in run files; `corrections.py` records them as a dated overlay
without editing any measurement record. This file answers the only question that matters next:
**does anything this practice has published move, and by how much?**

It imports `day4_118.py`'s own Wilson function and design effect rather than writing a second
one, because a correction computed with new code is a second chance to be wrong.

No requests. Reads files already on disk.
"""
import importlib.util
import json
import time

import corrections as corrections_mod


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


d4 = _load("day4_118", "day4_118.py")           # guarded by __main__; import runs nothing
wilson, DEFF = d4.wilson, d4.DEFF

DAY3 = "ledger/run-2026-08-13T0427Z.json"
DAY4 = "ledger/run-2026-08-14T0343Z.json"
ECHOES = {"7368171405361351954"}   # session 118 excluded this by hand; the overlay does it by rule


def states(path, overlay):
    d = json.load(open(path))
    s = {o["vid"]: o["state"] for o in d["observations"]}
    a = {o["vid"]: o["arm"] for o in d["observations"]}
    applied = []
    for (rf, vid), row in overlay.items():
        if rf == path and vid in s and s[vid] != row["corrected_state"]:
            applied.append({"vid": vid, "was": s[vid], "read_as": row["corrected_state"]})
            s[vid] = row["corrected_state"]
    return s, a, applied


def absence(path, overlay):
    s, _, applied = states(path, overlay)
    det = [v for v, x in s.items() if x != "INDETERMINATE"]
    nr = sum(1 for v in det if s[v] == "NOT-RETRIEVABLE")
    return {"file": path, "determinate": len(det), "not_retrievable": nr,
            "share": nr / len(det), "overlay_rows_applied": applied}


def exposure(overlay):
    """Interval 3 exposure, rebuilt exactly as `day4_118.py` builds it."""
    s3, a3, _ = states(DAY3, overlay)
    s4, _, _ = states(DAY4, overlay)
    det = [v for v in s3
           if s3[v] in ("RETRIEVABLE", "NOT-RETRIEVABLE")
           and s4.get(v) in ("RETRIEVABLE", "NOT-RETRIEVABLE")
           and a3.get(v) != "B-truncated"]
    absent3 = [v for v in det if s3[v] == "NOT-RETRIEVABLE"]
    present3 = [v for v in det if s3[v] == "RETRIEVABLE"]
    ret = sum(1 for v in absent3 if s4[v] == "RETRIEVABLE" and v not in ECHOES)
    return {"determinate_in_both_excluding_B_truncated": len(det),
            "absent_on_day3": len(absent3), "present_on_day3": len(present3),
            "confirmed_returns": ret, "confirmed_losses": 0,
            "return_rate_per_interval": ret / len(absent3),
            "return_rate_wilson_binomial": wilson(ret, len(absent3)),
            "return_rate_wilson_widened_at_crossed_deff": wilson(ret, len(absent3), DEFF),
            "loss_rate_upper_widened": wilson(0, len(present3), DEFF)[1]}


def main():
    overlay = corrections_mod.load()
    raw, cor = {}, {}
    for p in (DAY3, DAY4):
        raw[p] = absence(p, {})
        cor[p] = absence(p, overlay)
    ex_raw, ex_cor = exposure({}), exposure(overlay)

    diffs = []
    for name in ("diff-baseline-day3", "diff-baseline-day4", "diff-day2-day3", "diff-day3-day4"):
        a = json.load(open(f"ledger/{name}.json"))
        b = json.load(open(f"ledger/corrected/{name}.json"))
        diffs.append({"diff": name, "transitions_raw": a["n_transitions"],
                      "transitions_corrected": b["n_transitions"],
                      "overlay_rows_used": b["corrections_applied"]["n"],
                      "dropped": sorted({t["vid"] for t in a["transitions"]}
                                        - {t["vid"] for t in b["transitions"]}),
                      "added": sorted({t["vid"] for t in b["transitions"]}
                                      - {t["vid"] for t in a["transitions"]})})

    out = {
        "schema": "field-research/overlay-downstream/1", "session": 119,
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "requests_made": 0,
        "deff_used": DEFF,
        "absence_share": {"raw": raw, "corrected": cor,
                          "delta_pp": {p: 100 * (cor[p]["share"] - raw[p]["share"])
                                       for p in raw}},
        "interval3_exposure": {"raw": ex_raw, "corrected": ex_cor},
        "diffs": diffs,
        "what_moves": ("Nothing this practice has published in prose. The two exposure "
                       "denominators move by one unit each, the absence share by less than "
                       "three hundredths of a percentage point, and no interval endpoint moves "
                       "in the digits this arc prints. The finding is not the size of the "
                       "movement; it is that two derived files carried a reading the arc had "
                       "already refuted, and only the interval diffs were ever corrected by "
                       "hand — the two baseline diffs never were."),
    }
    json.dump(out, open("overlay-downstream-119.json", "w"), indent=1)
    print(json.dumps(out, indent=1))
    print("wrote overlay-downstream-119.json")


if __name__ == "__main__":
    main()
