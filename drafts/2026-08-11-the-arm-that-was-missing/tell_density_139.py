#!/usr/bin/env python3
"""tell_density_139 - testing this session's own conjecture instead of leaving it as one.

Session 139, 2026-08-30. `DELIMITATION-139.md` offered a mechanism for why the hand-delimited units
carry more role-revealing tokens than the machine's, and marked it CONJECTURE:

    hand delimitation selects a report's real findings list, and a findings list is where a role's
    vocabulary lives, whereas v2 sometimes carved chapters or remedies.

If that is right, the gap should sit in the files where v2 and the hand DISAGREE - the files where
v2 carved something other than the findings - and should be small or absent where they agree.

THE TEST. Restrict BOTH populations to the same nineteen delimited files. Compute the RULE-U carrier
share (every tell with zero hits among that population's reader units) for the hand units and for
v2's units, split by whether v2's count agreed with the hand count. `VERIFIER-124.md` contributes no
v2 units at all (v2 called it UNEXTRACTABLE) and is reported separately rather than folded in.

WHAT IT CANNOT DO. Nineteen files, and the disagreeing group is six. This is a check on a conjecture,
not a measurement of a population, and a difference in the predicted direction on six files is not
the conjecture established. The result is reported as counts beside shares, and the shares are
printed only because the two groups are different sizes.
"""
import json

from blinding_check_137 import TELLS

hand_units = json.load(open("units-139.json", encoding="utf-8"))
hand_km = json.load(open("units-manifest-139.json", encoding="utf-8"))["key_map"]
v2_units = json.load(open("units-137-v2.json", encoding="utf-8"))
v2_km = json.load(open("units-manifest-137-v2.json", encoding="utf-8"))["key_map"]

cmp_rows = json.load(open("extractor-vs-hand-139.json", encoding="utf-8"))["rows"]
group = {r["file"]: r["verdict"] for r in cmp_rows}


def reader_free(units, km):
    return [p for n, p in TELLS.items()
            if not any(p.search(u["text"]) for u in units if km[u["key"]]["role"] == "reader")]


def share(units, km, pats, want):
    sel = [u for u in units if group.get(km[u["key"]]["file"].split("/")[-1]) in want]
    hit = [u for u in sel if any(p.search(u["text"]) for p in pats)]
    return len(hit), len(sel)


hp, vp = reader_free(hand_units, hand_km), reader_free(v2_units, v2_km)
out, rows = {}, []
for label, want in (("v2 AGREES with the hand count", {"AGREE"}),
                    ("v2 DISAGREES", {"DISAGREE"}),
                    ("v2 called it UNEXTRACTABLE", {"V2-UNEXTRACTABLE"})):
    hh, hn = share(hand_units, hand_km, hp, want)
    vh, vn = share(v2_units, v2_km, vp, want)
    rows.append({"group": label,
                 "hand": {"carriers": hh, "units": hn,
                          "share": round(hh / hn, 4) if hn else None},
                 "v2": {"carriers": vh, "units": vn,
                        "share": round(vh / vn, 4) if vn else None}})
out["rows"] = rows
out["conjecture"] = ("hand delimitation selects a report's real findings list, where a role's "
                     "vocabulary lives; v2 sometimes carved chapters or remedies")
json.dump(out, open("tell-density-139.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

print("%-32s %-22s %s" % ("group", "hand-delimited", "v2"))
for r in rows:
    def f(d):
        return "n/a" if d["share"] is None else "%3d/%-4d (%.1f %%)" % (
            d["carriers"], d["units"], 100 * d["share"])
    print("%-32s %-22s %s" % (r["group"], f(r["hand"]), f(r["v2"])))
