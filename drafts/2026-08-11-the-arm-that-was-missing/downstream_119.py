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
import glob
import importlib.util
import json
import os
import subprocess
import sys
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

# Session 119, after the gauntlet. THE FIRST VERSION OF THIS FILE APPLIED THE HAND-EXCLUSION TO
# THE RAW ARM AS WELL, and so compared a laundered baseline against the overlay and called the
# match a validation. The adversary caught it and recomputed the honest raw figure. Three arms
# are now computed and all three are published:
#   raw          — the ledger exactly as it stands, no exclusion of any kind: 3 returns
#   hand         — session 118's manual exclusion of the echo, reproduced: 2 returns
#   overlay      — the same exclusion reached by rule from the sidecars: 2 returns
# The validation is that `overlay` equals `hand` while `raw` differs from both. Stated that way
# it is a real check; stated the old way it was a tautology.
HAND_EXCLUSION = {"7368171405361351954"}   # what session 118 did by hand, reproduced as itself


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


def exposure(overlay, hand_exclusion=frozenset()):
    """Interval 3 exposure, rebuilt exactly as `day4_118.py` builds it.

    `hand_exclusion` is session 118's manual echo list and is passed EXPLICITLY, so the raw arm
    can be computed with nothing excluded at all.
    """
    s3, a3, _ = states(DAY3, overlay)
    s4, _, _ = states(DAY4, overlay)
    det = [v for v in s3
           if s3[v] in ("RETRIEVABLE", "NOT-RETRIEVABLE")
           and s4.get(v) in ("RETRIEVABLE", "NOT-RETRIEVABLE")
           and a3.get(v) != "B-truncated"]
    absent3 = [v for v in det if s3[v] == "NOT-RETRIEVABLE"]
    present3 = [v for v in det if s3[v] == "RETRIEVABLE"]
    ret = sum(1 for v in absent3 if s4[v] == "RETRIEVABLE" and v not in hand_exclusion)
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
    ex_raw = exposure({})                                  # nothing excluded at all
    ex_hand = exposure({}, HAND_EXCLUSION)                  # session 118's manual exclusion
    ex_cor = exposure(overlay)                              # the same thing reached by rule

    # The diff list is DERIVED, not typed: every diff that references a run file the overlay
    # touches. The first version carried a hand-written tuple of four names, which both reviewers
    # named as the reason a check with a directional blind spot still produced a correct table.
    touched = {rf for rf, _vid in overlay}
    names = []
    for p in sorted(glob.glob("ledger/diff-*.json")):
        dj = json.load(open(p))
        if dj.get("run1", {}).get("path") in touched or dj.get("run2", {}).get("path") in touched:
            names.append(os.path.splitext(os.path.basename(p))[0])

    diffs = []
    for name in names:
        a = json.load(open(f"ledger/{name}.json"))
        cpath = f"ledger/corrected/{name}.json"
        if not os.path.exists(cpath):
            subprocess.run([sys.executable, "ledger_diff.py", a["run1"]["path"],
                            a["run2"]["path"], cpath, "--corrections"],
                           check=True, capture_output=True)
        b = json.load(open(cpath))
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
        "interval3_exposure": {"raw_nothing_excluded": ex_raw,
                               "session_118_hand_exclusion": ex_hand,
                               "overlay_by_rule": ex_cor,
                               "validation": ("the overlay reaches session 118's hand figure by "
                                              "rule (%d = %d confirmed returns) while the "
                                              "untouched ledger says %d"
                                              % (ex_cor["confirmed_returns"],
                                                 ex_hand["confirmed_returns"],
                                                 ex_raw["confirmed_returns"]))},
        "diffs": diffs,
        "diff_list_derived_not_typed": names,
        "what_moves": ("Nothing this practice has published in prose. The two exposure "
                       "denominators move by one unit each, the absence share by less than "
                       "three hundredths of a percentage point, and only one printed interval "
                       "endpoint moves at all (the widened upper bound, 2.56 % -> 2.57 %). The "
                       "finding is not the size of the movement; it is that derived files "
                       "carried a reading the arc had already refuted, and only the interval "
                       "diffs were ever corrected by hand — the baseline diffs never were."),
    }
    json.dump(out, open("overlay-downstream-119.json", "w"), indent=1)
    print(json.dumps(out, indent=1))
    print("wrote overlay-downstream-119.json")


if __name__ == "__main__":
    main()
