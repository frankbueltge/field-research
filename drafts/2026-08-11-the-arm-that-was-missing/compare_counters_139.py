#!/usr/bin/env python3
"""compare_counters_139 - the agreement comparison of PREREGISTRATION-139.md, section "Verdicts".

Session 139, 2026-08-30. Reads the four counters' reports as they were returned, verbatim, and
applies the four verdict categories fixed before the draw:

    DELIMITED       both counts equal AND every delimiter line the same
    SPLIT-COUNT     counts differ
    SPLIT-BOUNDARY  counts equal, delimiters differ
    UNDELIMITABLE   both find no primary enumeration

IT ADJUDICATES NOTHING. Where the two counters differ, both readings are recorded and neither is
preferred - `PREREGISTRATION-138B.md` section 2, and it is the clause that stops a session choosing
its own rate.

PARSING, AND WHY IT IS CHECKED RATHER THAN TRUSTED. Each counter's report is free-form markdown. The
parser takes, per FILE-n section, the first fenced code block - which is where every counter put its
delimiter list - and treats its non-empty lines as the delimiters. The count is read from the
counter's own COUNT line, NOT from the number of lines parsed, so that a parser slip shows up as a
mismatch between the two and is reported, never silently absorbed.
"""
import json
import re
import sys

FILEHDR = re.compile(r"^\s*#{0,4}\s*\**FILE-(\d{1,2})\**\s*$", re.M)
COUNT = re.compile(r"COUNT[:\s\*]*?(\d+)", re.I)
NOPRIM = re.compile(r"NO PRIMARY ENUMERATION", re.I)


def parse(path):
    raw = open(path, encoding="utf-8").read()
    hits = [(m.group(1), m.start(), m.end()) for m in FILEHDR.finditer(raw)]
    out = {}
    for k, (num, _s, e) in enumerate(hits):
        end = hits[k + 1][1] if k + 1 < len(hits) else len(raw)
        body = raw[e:end]
        cm = COUNT.search(body)
        count = int(cm.group(1)) if cm else None
        if NOPRIM.search(body):
            count = 0
        fence = re.search(r"```[a-zA-Z]*\n(.*?)```", body, re.S)
        delims = [l for l in fence.group(1).split("\n") if l.strip()] if fence else []
        out["FILE-%s" % num] = {"count": count, "delimiters": delims,
                                "parsed_lines": len(delims)}
    return out


def main(draw_path, batch, rep_a, rep_b, out_path):
    d = json.load(open(draw_path, encoding="utf-8"))
    names = d[batch]
    A, B = parse(rep_a), parse(rep_b)
    rows = []
    for i, name in enumerate(names, 1):
        lab = "FILE-%d" % i
        a, b = A.get(lab), B.get(lab)
        if a is None or b is None:
            rows.append({"file": name, "label": lab, "verdict": "UNPARSED",
                         "note": "a counter's section for this label was not found"})
            continue
        same_delims = a["delimiters"] == b["delimiters"]
        if a["count"] == 0 and b["count"] == 0:
            v = "UNDELIMITABLE"
        elif a["count"] != b["count"]:
            v = "SPLIT-COUNT"
        elif same_delims:
            v = "DELIMITED"
        else:
            v = "SPLIT-BOUNDARY"
        rows.append({
            "file": name, "label": lab, "verdict": v,
            "count_a": a["count"], "count_b": b["count"],
            "parsed_a": a["parsed_lines"], "parsed_b": b["parsed_lines"],
            "count_matches_parse_a": a["count"] == a["parsed_lines"],
            "count_matches_parse_b": b["count"] == b["parsed_lines"],
            "delimiters_identical": same_delims,
            "delimiters": a["delimiters"] if v == "DELIMITED" else None,
            "delimiters_a": None if v == "DELIMITED" else a["delimiters"],
            "delimiters_b": None if v == "DELIMITED" else b["delimiters"],
        })
    json.dump({"batch": batch, "reports": [rep_a, rep_b], "rows": rows},
              open(out_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for r in rows:
        flag = ""
        if r["verdict"] != "UNPARSED" and not (r["count_matches_parse_a"]
                                               and r["count_matches_parse_b"]):
            flag = "  <-- COUNT/PARSE MISMATCH a=%s/%s b=%s/%s" % (
                r["count_a"], r["parsed_a"], r["count_b"], r["parsed_b"])
        print("%-24s %-15s A=%-4s B=%-4s%s" % (
            r["file"], r["verdict"], r.get("count_a"), r.get("count_b"), flag))
    print("\n%s: %s" % (batch, {v: sum(1 for r in rows if r["verdict"] == v)
                               for v in sorted({r["verdict"] for r in rows})}))


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:6]))
