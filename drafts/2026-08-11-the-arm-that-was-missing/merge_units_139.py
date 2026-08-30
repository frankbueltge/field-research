#!/usr/bin/env python3
"""merge_units_139 - the two batches' hand-delimited units, joined into one population fragment.

Session 139, 2026-08-30. Nothing is chosen here: the two batch outputs of `slice_139.py` are
concatenated in file order and their manifests summed. The unit keys already carry the file path and
the `hand139` namespace, so a key is unique across batches by construction and the script asserts it
rather than trusting it.

THIS IS A FRAGMENT, NOT A POPULATION. Nineteen files of fifty-three are delimited. Nothing may be
divided by 53 using this file.
"""
import json
import sys


def main(out_units, out_manifest, *pairs):
    units, manifest, sources = [], [], []
    for i in range(0, len(pairs), 2):
        up, mp = pairs[i], pairs[i + 1]
        units += json.load(open(up, encoding="utf-8"))
        m = json.load(open(mp, encoding="utf-8"))
        manifest += m["manifest"]
        sources += [up, mp]
    keys = [u["key"] for u in units]
    assert len(keys) == len(set(keys)), "key collision across batches"
    roles = sorted({r["role"] for r in manifest})
    json.dump(units, open(out_units, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump({
        "source": "hand delimitation, PREREGISTRATION-138B.md section 2, executed under "
                  "PREREGISTRATION-139.md; merged from the two batch outputs",
        "merged_from": sources,
        "namespace": "hand139",
        "files_delimited": len(manifest),
        "files_in_full_population": 53,
        "this_is_a_fragment": "19 of 53 files under this design (10 here in batch 2, 9 in batch 1, "
                              "plus the 3 PILOT-138 files which are NOT merged here). No figure "
                              "may be divided by 53 using this file.",
        "units": len(units),
        "truncated_units": sum(1 for u in units if u["truncated"]),
        "by_role_passes": {r: sum(1 for x in manifest if x["role"] == r) for r in roles},
        "by_role_units": {r: sum(1 for u in units if u["role"] == r) for r in roles},
        "key_map": {u["key"]: {"file": u["file"], "role": u["role"],
                               "ordinal": u["ordinal"]} for u in units},
        "manifest": manifest,
    }, open(out_manifest, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("merged %d files, %d units (%d truncated)" % (
        len(manifest), len(units), sum(1 for u in units if u["truncated"])))
    print("by role, passes:", {r: sum(1 for x in manifest if x["role"] == r) for r in roles})
    print("by role, units: ", {r: sum(1 for u in units if u["role"] == r) for r in roles})


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
