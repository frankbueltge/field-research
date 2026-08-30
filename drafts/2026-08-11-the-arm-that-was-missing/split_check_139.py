#!/usr/bin/env python3
"""split_check_139 - what, exactly, the one split of session 139 is a split about.

`PREREGISTRATION-139.md` forbids this practice from adjudicating a split, and this script does not.
It measures one thing and reports it: for each of the two counters' readings of a SPLIT file, WHICH
SOURCE LINE each delimiter sits on. If both readings sit on the same lines, the split is about how
much of a line was quoted; if they sit on different lines, it is about where the units begin. Those
are different facts about a disagreement and neither of them settles it.

Two match kinds are reported and kept apart:
  exact   - the delimiter IS the source line
  prefix  - the delimiter is the beginning of the source line, truncated by the counter

A `prefix` is reported, never accepted: `slice_139.py` matches exactly and refuses anything else, so
a reading made of prefixes is NOT sliceable as returned, whatever its boundaries are.
"""
import json
import sys


def locate_all(lines, delims):
    out, cur = [], 0
    for d in delims:
        rec = None
        for i in range(cur, len(lines)):
            if lines[i] == d:
                rec = {"line": i, "kind": "exact"}
                break
        if rec is None:
            for i in range(cur, len(lines)):
                if lines[i].startswith(d) and d.strip():
                    rec = {"line": i, "kind": "prefix"}
                    break
        out.append(rec)
        if rec:
            cur = rec["line"] + 1
    return out


def main(compare_path, source_path, name, out_path):
    c = json.load(open(compare_path, encoding="utf-8"))
    row = [r for r in c["rows"] if r["file"] == name][0]
    lines = open(source_path, encoding="utf-8").read().split("\n")
    A = locate_all(lines, row["delimiters_a"])
    B = locate_all(lines, row["delimiters_b"])
    linesA = [r["line"] if r else None for r in A]
    linesB = [r["line"] if r else None for r in B]
    res = {
        "file": name, "verdict_stands": row["verdict"],
        "counter_a": {"lines": linesA, "kinds": [r["kind"] if r else None for r in A],
                      "sliceable_as_returned": all(r and r["kind"] == "exact" for r in A)},
        "counter_b": {"lines": linesB, "kinds": [r["kind"] if r else None for r in B],
                      "sliceable_as_returned": all(r and r["kind"] == "exact" for r in B)},
        "same_boundaries": linesA == linesB and None not in linesA,
        "a_is_prefix_of_b": all(b.startswith(a) and b != a
                                for a, b in zip(row["delimiters_a"], row["delimiters_b"])),
        "what_this_settles": "nothing about which reading is right - the verdict above stands as "
                             "pre-registered and is not adjudicated here",
    }
    json.dump(res, open(out_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:5]))
