#!/usr/bin/env python3
"""The standing check that has failed three times, made into a script.

Session 116, 2026-08-13. Pre-registered in PREREGISTRATION-116.md.

WHY THIS EXISTS
---------------
Three consecutive sessions published a number contradicted by this draft's own machine-written
files:

  session 113  a ceiling its own by-year table refuted
  session 114  "five of ten fail" printed above a table showing four
  session 115  a per-cell maximum of 1.7052 above a table topping out at 1.6739 — inside the
               section about this exact failure mode

The mechanism was named at session 115: the arc's pre-registered subtract-first check compares
CODE OUTPUT against PUBLISHED INTERVALS, and has never compared PROSE against JSON. That is
where all three failures lived. Session 115's handover asked whether a discipline that has failed
three times should be a script. This is the script.

WHAT IT DOES
------------
Reads a prose file, pulls every number out of it, and asks of each one: does this value occur
anywhere in the machine-written JSON of this draft? It reports the ones that do not.

WHAT IT CANNOT DO, STATED PLAINLY
---------------------------------
It does not know which field a number was supposed to come from, so it cannot catch a number
that is right for the wrong reason, nor one copied correctly from the wrong row. A number can
also be legitimately absent from every JSON — a count of paragraphs, a date, a figure quoted
from an outside source. So its output is a WORKLIST, not a verdict, and every unmatched number
must be dispositioned by hand in the session record. What it does catch, mechanically and every
time, is the class that has bitten three times: a figure in prose that exists nowhere in the
data this draft computed.

Usage:
    python3 prose_vs_json.py INCREMENT-6.md [more.md ...]
    python3 prose_vs_json.py --json                 # machine-readable
"""
import glob
import json
import os
import re
import sys

NUM = re.compile("(?<![\\w.])([-\u2212\u2013]?\\d+(?:\\.\\d+)?)(?![\\w])")
SKIP_CONTEXT = re.compile(r"session |§|day |http|\.md|\.py|\.json|20\d\d-\d\d-\d\d")


def json_values(paths):
    """Every numeric value in every machine-written JSON of this draft, with its origin."""
    vals = {}

    def walk(o, where):
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, f"{where}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{where}[{i}]")
        elif isinstance(o, bool):
            pass
        elif isinstance(o, (int, float)):
            vals.setdefault(float(o), []).append(where)

    for p in paths:
        try:
            walk(json.load(open(p)), os.path.basename(p))
        except Exception as e:                      # a broken file is a finding, not a crash
            vals.setdefault(None, []).append(f"{p}: UNREADABLE {e}")
    return vals


def matches(tok, vals):
    """Does the prose token equal some JSON value, at the token's own precision?"""
    tok = tok.replace("\u2212", "-").replace("\u2013", "-")
    dec = len(tok.split(".")[1]) if "." in tok else 0
    x = float(tok)
    hits = []
    for v, where in vals.items():
        if v is None:
            continue
        for cand in (v, v * 100.0, v / 100.0):      # percent/fraction, the arc's two scales
            if round(cand, dec) == x:
                hits.extend(where[:3])
                break
        if len(hits) >= 3:
            break
    return hits


def audit(prose_path, vals):
    text = open(prose_path).read()
    seen, rows = set(), []
    for line_no, line in enumerate(text.splitlines(), 1):
        for m in NUM.finditer(line):
            tok = m.group(1)
            # load-bearing = has a decimal point, or is a long integer. Section numbers, years,
            # small counts and dates are not audited: they are checked by reading, and saying
            # otherwise would be a false claim of coverage.
            if "." not in tok and len(tok.lstrip("-")) < 4:
                continue
            ctx = line[max(0, m.start() - 40):m.end() + 40]
            if SKIP_CONTEXT.search(ctx) and "." not in tok:
                continue
            key = (tok, line_no)
            if key in seen:
                continue
            seen.add(key)
            hits = matches(tok, vals)
            rows.append({"value": tok, "line": line_no, "matched": bool(hits),
                         "found_in": hits[:3], "context": ctx.strip()})
    return rows


WORDNUM = r"(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d+)"
EXTREMAL = re.compile(
    r"\b(range|ranges|ceiling|floor|maximum|minimum|max|min|highest|lowest|largest|smallest|"
    r"topping out|tops out|at most|at least|up to|no more than|no fewer|worst|best|bound|"
    r"bounded|upper|lower|all of|none of|every|not one)\b", re.I)
NOFM = re.compile(rf"\b({WORDNUM})\s+of\s+(?:the\s+)?({WORDNUM})\b", re.I)


def disposition_pass(prose_path):
    """The second pass, and the one that matters.

    Running pass 1 on the archived version of RESTATEMENT-2026-08-13.md that carried session
    115's failure proves pass 1 would NOT have caught it: 1.7052 is a real per-cell design
    effect that does occur in this draft's JSON — it simply belongs to a partition that was
    never in the set the sentence claimed to summarise. A value-existence check is structurally
    blind to that. So this pass does not check values at all. It lists the sentences whose FORM
    is the form all three failures took — a summary over a set, or a count out of a total — and
    demands each be dispositioned by hand against the table it claims to summarise.
    """
    rows = []
    for line_no, line in enumerate(open(prose_path).read().splitlines(), 1):
        why = []
        e = EXTREMAL.search(line)
        if e:
            why.append(f"extremal claim: '{e.group(1)}'")
        n = NOFM.search(line)
        if n:
            why.append(f"count-out-of-total: '{n.group(0)}'")
        if why:
            nums = [m.group(1) for m in NUM.finditer(line)]
            rows.append({"line": line_no, "why": why, "numbers": nums,
                         "text": line.strip()[:160]})
    return rows


def main(argv):
    as_json = "--json" in argv
    files = [a for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 2
    vals = json_values(sorted(glob.glob("*.json")))
    report = {"json_files_read": len(glob.glob("*.json")),
              "distinct_json_values": len([k for k in vals if k is not None]), "files": {}}
    bad = 0
    for f in files:
        rows = audit(f, vals)
        un = [r for r in rows if not r["matched"]]
        disp = disposition_pass(f)
        bad += len(un)
        report["files"][f] = {"numbers_audited": len(rows), "unmatched": len(un),
                              "unmatched_rows": un,
                              "claims_requiring_disposition": len(disp),
                              "disposition_rows": disp}
        if not as_json:
            print(f"\n{f}: pass 1 — {len(rows)} numbers audited, {len(un)} not found in any "
                  f"JSON of this draft")
            for r in un:
                print(f"  line {r['line']:4d}  {r['value']:>14s}   {r['context'][:96]}")
            print(f"{f}: pass 2 — {len(disp)} claims whose FORM is the form all three published "
                  f"failures took; disposition each against its own table")
            for r in disp:
                print(f"  line {r['line']:4d}  [{'; '.join(r['why'])}]  {r['text'][:88]}")
    if as_json:
        print(json.dumps(report, indent=1))
    else:
        print(f"\n{report['distinct_json_values']} distinct numeric values across "
              f"{report['json_files_read']} JSON files. Unmatched is a WORKLIST, not a verdict — "
              f"disposition each one in the record.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
