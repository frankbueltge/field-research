#!/usr/bin/env python3
"""slice_139 - cut the hand-delimited files into units, mechanically, with no further judgement.

Session 139, 2026-08-30. `PREREGISTRATION-138B.md` §2 requires each counter to return "the verbatim
first line of every item in the primary enumeration ... enough to slice the file mechanically
afterwards without any further judgement". This script is the cash value of that sentence: given the
delimiter lines the two counters AGREED on, it locates each one in the file and cuts.

THIS IS NOT A CARVE AND THE BAN OF `PREREGISTRATION-138B.md` §1 DOES NOT REACH IT. It chooses
nothing. It contains no pattern, no family, no threshold and no heuristic; it is given the boundaries
by hand and only finds the offsets. If a delimiter cannot be located exactly, the file is reported
UNSLICEABLE and no unit is emitted for it - a failure to locate is published, never repaired by
loosening the match.

THE BLINDING AND TRUNCATION ARE CARRIED OVER UNCHANGED, which `PREREGISTRATION-138B.md` §4 requires
so that all three studies stay comparable: `blind()` and `truncate()` are imported from
`extract_units_137_v2.py` and not reimplemented, so no silent drift can enter through a retyped
regex. Importing two text-normalising helpers is not using the banned extractor to carve; nothing
from `pick_family`/`split_on` is imported or called.

The unit key is namespaced "hand139", not "v2", so no unit of this population can ever be confused
with a v2 unit in a later join.
"""
import hashlib
import json
import sys

from extract_units_137_v2 import blind, truncate


def locate(lines, delim, start):
    """Exact match first, then whitespace-stripped. Returns index or None. No fuzzy matching."""
    for i in range(start, len(lines)):
        if lines[i] == delim:
            return i, "exact"
    for i in range(start, len(lines)):
        if lines[i].strip() == delim.strip():
            return i, "stripped"
    return None, None


def main(agreed_path, out_units, out_manifest):
    agreed = json.load(open(agreed_path, encoding="utf-8"))
    m = json.load(open("units-manifest-137-v2.json", encoding="utf-8"))
    path_of = {r["file"].split("/")[-1]: r["file"] for r in m["manifest"]}
    role_of = {r["file"].split("/")[-1]: r["role"] for r in m["manifest"]}

    units, manifest = [], []
    for name in sorted(agreed):
        delims = agreed[name]
        path = path_of[name]
        lines = open(path, encoding="utf-8").read().split("\n")
        idx, how, cursor, failed = [], [], 0, None
        for d in delims:
            i, kind = locate(lines, d, cursor)
            if i is None:
                failed = d
                break
            idx.append(i)
            how.append(kind)
            cursor = i + 1
        rec = {"file": path, "role": role_of[name], "delimiters": len(delims)}
        if failed is not None:
            rec.update(status="UNSLICEABLE", units=0, unlocated=failed)
            manifest.append(rec)
            continue
        bounds = idx + [len(lines)]
        texts = ["\n".join(lines[bounds[k]:bounds[k + 1]]).strip()
                 for k in range(len(idx))]
        rec.update(status="SLICED", units=len(texts),
                   match_kinds=sorted(set(how)),
                   first_line=idx[0], empty_slices=sum(1 for t in texts if not t))
        manifest.append(rec)
        for ordinal, text in enumerate(texts, 1):
            key = hashlib.sha256(
                (path + "|hand139|" + str(ordinal)).encode("utf-8")).hexdigest()[:12]
            body, cut = truncate(blind(text))
            units.append({"key": key, "file": path, "role": role_of[name],
                          "ordinal": ordinal, "truncated": cut,
                          "chars": len(text), "text": body})

    json.dump(units, open(out_units, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)
    roles = sorted({r["role"] for r in manifest})
    json.dump({
        "source": "hand delimitation, PREREGISTRATION-138B.md section 2, executed under "
                  "PREREGISTRATION-139.md",
        "namespace": "hand139", "truncate_at": 6000,
        "files": len(manifest),
        "sliced": sum(1 for r in manifest if r["status"] == "SLICED"),
        "unsliceable": sum(1 for r in manifest if r["status"] == "UNSLICEABLE"),
        "units": len(units),
        "truncated_units": sum(1 for u in units if u["truncated"]),
        "by_role_passes": {r: sum(1 for x in manifest
                                  if x["role"] == r and x["status"] == "SLICED")
                           for r in roles},
        "by_role_units": {r: sum(1 for u in units if u["role"] == r) for r in roles},
        "key_map": {u["key"]: {"file": u["file"], "role": u["role"],
                               "ordinal": u["ordinal"]} for u in units},
        "manifest": manifest,
    }, open(out_manifest, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    print("sliced %d of %d files, %d units, %d truncated" % (
        sum(1 for r in manifest if r["status"] == "SLICED"), len(manifest),
        len(units), sum(1 for u in units if u["truncated"])))
    for r in manifest:
        if r["status"] == "UNSLICEABLE":
            print("UNSLICEABLE %s - could not locate %r" % (r["file"], r["unlocated"]))
        elif r["match_kinds"] != ["exact"]:
            print("NOTE %s matched with %s" % (r["file"], r["match_kinds"]))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
