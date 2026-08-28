#!/usr/bin/env python3
"""blinding_check_137 - how much of the role survives the blinding, measured rather than assumed.

Session 137, 2026-08-28. The classification pre-registered in `PREREGISTRATION-137B.md` hands
classifiers unit text with every explicit role word replaced. Session 134's classification did the
same and its report asserted the blinding worked. **Asserted is not measured**, and a classifier who
can tell which role wrote a unit is not blind, whatever the substitution table did.

WHAT IT COUNTS
--------------
1. **Explicit leaks** - the role words the blinder is supposed to remove, still present.
2. **Stylistic tells** - tokens that are not role words but occur in one role's units and not in
   another's. A tell that is perfectly separating is as good as a label.

For each token the script prints the count per role and, where a token appears in exactly one role's
units, marks it SEPARATING. This is a lower bound on what a reader could infer: it tests the tokens
named here and nothing else, and prose style is not a token.
"""
import json
import re
import sys

TELLS = {
    "role word: interlocutor/verifier/severed reader":
        re.compile(r"[Ii]nterlocutor|[Vv]erifier|[Ss]evered reader"),
    "'Charge N'": re.compile(r"\bCharge \d"),
    "'Finding N'": re.compile(r"\bFinding \d"),
    "'BLOCKING'": re.compile(r"\bBLOCKING\b"),
    "'I recomputed' / 'recomputed'": re.compile(r"\brecomputed\b", re.I),
    "'I ran' / 'I fetched'": re.compile(r"\bI (?:ran|fetched|re-ran)\b"),
    "'my/I' first person": re.compile(r"\b(?:I|my)\b"),
    "verdict vocabulary": re.compile(r"SURVIVES|REFUTED|PASS WITH FINDINGS"),
}


def main(units_path, manifest_path, out_path):
    units = json.load(open(units_path, encoding="utf-8"))
    km = json.load(open(manifest_path, encoding="utf-8"))["key_map"]
    roles = sorted({v["role"] for v in km.values()})
    totals = {r: sum(1 for v in km.values() if v["role"] == r) for r in roles}

    rows = []
    for name, pat in TELLS.items():
        per = {r: 0 for r in roles}
        for u in units:
            r = km[u["key"]]["role"]
            if pat.search(u["text"]):
                per[r] += 1
        hit_roles = [r for r in roles if per[r]]
        rows.append({
            "tell": name, "per_role": per,
            "separating": len(hit_roles) == 1 and per[hit_roles[0]] > 0,
            "roles_hit": hit_roles,
        })

    out = {"units": len(units), "units_by_role": totals, "tells": rows}
    json.dump(out, open(out_path, "w", encoding="utf-8"), indent=1)
    print("units %d  %s" % (len(units), totals))
    for r in rows:
        print("%-34s %s%s" % (r["tell"], r["per_role"],
                              "  SEPARATING" if r["separating"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
