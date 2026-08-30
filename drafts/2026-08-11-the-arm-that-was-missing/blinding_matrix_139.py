#!/usr/bin/env python3
"""blinding_matrix_139 - the same two populations under the same two rules, all four cells.

Session 139, 2026-08-30. Written after `INTERLOCUTOR-139.md`'s blocking finding and BEFORE that
finding was adopted, to recompute it here rather than take it on the adversary's word.

WHAT WENT WRONG, AND IT IS THIS SESSION'S DEFECT. `DELIMITATION-139.md` set **48.9 %** (hand139
units) beside **28.4 %** (v2 units) and said the tells table was imported unchanged "so that no tell
could drift between the two measurements". The TABLE did not drift. The **SELECTION RULE** over that
table did:

  RULE-4  session 137's rule, `PREREGISTRATION-137B.md` section 4b: the four tokens it names -
          `Charge N`, `Finding N`, `BLOCKING`, verdict vocabulary.
  RULE-U  session 139's rule, `blinding_share_139.py`: EVERY tell in the table with zero hits among
          this population's reader units.

RULE-U is wider than RULE-4, so 48.9 % against 28.4 % compares a wider rule against a narrower one
and overstates the movement. This script computes both rules over both populations so the comparison
can be read down a column instead.

It settles nothing about which rule is right, and it does not choose one.
"""
import json

from blinding_check_137 import TELLS

RULE4 = ["'Charge N'", "'Finding N'", "'BLOCKING'", "verdict vocabulary"]


def load(units_path, manifest_path):
    units = json.load(open(units_path, encoding="utf-8"))
    km = json.load(open(manifest_path, encoding="utf-8"))["key_map"]
    return units, km


def carriers(units, km, names):
    hit = set()
    for n in names:
        pat = TELLS[n]
        hit |= {u["key"] for u in units if pat.search(u["text"])}
    return hit


def reader_free_names(units, km):
    out = []
    for n, pat in TELLS.items():
        if not any(pat.search(u["text"]) for u in units if km[u["key"]]["role"] == "reader"):
            out.append(n)
    return out


pops = {
    "v2_483": ("units-137-v2.json", "units-manifest-137-v2.json"),
    "hand139_178": ("units-139.json", "units-manifest-139.json"),
}

res = {"rule_4_tokens": RULE4, "cells": {}, "reader_free_by_population": {}}
for pop, (up, mp) in pops.items():
    units, km = load(up, mp)
    # units-137-v2.json carries only key+text; join role via the manifest key_map.
    rf = reader_free_names(units, km)
    res["reader_free_by_population"][pop] = rf
    for rule, names in (("RULE-4", RULE4), ("RULE-U", rf)):
        c = carriers(units, km, names)
        res["cells"]["%s / %s" % (pop, rule)] = {
            "carriers": len(c), "units": len(units),
            "share": round(len(c) / len(units), 4)}

json.dump(res, open("blinding-matrix-139.json", "w", encoding="utf-8"), indent=1,
          ensure_ascii=False)
print("%-22s %-8s %s" % ("population", "rule", "carriers / units  (share)"))
for k, v in res["cells"].items():
    p, r = k.split(" / ")
    print("%-22s %-8s %4d / %-4d  (%.1f %%)" % (p, r, v["carriers"], v["units"],
                                                100 * v["share"]))
print()
for p, names in res["reader_free_by_population"].items():
    print("%s reader-free tells (%d): %s" % (p, len(names), names))
