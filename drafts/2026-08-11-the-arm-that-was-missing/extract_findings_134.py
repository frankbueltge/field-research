#!/usr/bin/env python3
"""Extract the arc's finding-disposition rows into a blinded classification population.

Session 134, 2026-08-24. Written AFTER `PREREGISTRATION-134.md` was committed (6fac67e) and
before any finding was classified.

WHAT IT DOES, exactly as the pre-registration §3 says:
  * walks every `CONDITIONS-*.md` in this directory;
  * finds every markdown table whose header row contains a column named `finding` (case-insensitive)
    -- tables of *conditions discharged* are NOT finding tables and are skipped by that test;
  * emits one record per numbered row, with the finding text, the role the table attributes it to,
    and the file and line it came from;
  * BLINDS the finding text by masking a fixed, published list of role tokens, and records the
    substitution count per record so the blinding is auditable rather than trusted.

WHAT IT DELIBERATELY DOES NOT DO: it does not read the disposition column into the blinded text
(pre-registration K5), and it does not read `POST-MORTEM.md` or the pre-registration. The classifier
sees `blinded` and nothing else.

SELF-REFERENCE, stated because this practice has been caught by it twice (downstream conditions 31,
36): this script writes `findings-134.json` into the directory it enumerates. It does not enumerate
`*.json`, only `CONDITIONS-*.md`, so its output is outside its own search space by construction --
and that is a claim a reader can check in the glob on the line marked SEARCH-SPACE below.
"""
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# The masking list, published rather than described. Applied case-insensitively, longest first.
ROLE_TOKENS = [
    "severed readers", "severed reader", "reader panel", "readers' panel",
    "the panel", "a panel", "panel of three", "panel",
    "Interlocutor", "Verifier", "Skeptic",
    "adversary's", "adversary", "adversaries",
    "this practice, unprompted", "this practice",
]
MASK = "[ROLE]"


def normalise_role(raw):
    """Map a table's source/from cell onto the pre-registration's role vocabulary."""
    if raw is None:
        return "UNATTRIBUTED"
    t = raw.lower()
    t = re.sub(r"[*`]", "", t)
    if not t.strip() or t.strip() in {"-", "--", "—"}:
        return "UNATTRIBUTED"
    if "panel" in t or "reader" in t:
        return "READER_PANEL"
    if "interlocutor" in t:
        return "INTERLOCUTOR"
    if "verifier" in t:
        return "VERIFIER"
    if "skeptic" in t:
        return "SKEPTIC"
    if "this practice" in t or "this session" in t or "conductor" in t or "ourselves" in t:
        return "PRACTICE_SELF"
    return "OTHER"


def blind(text):
    """Mask role tokens. Returns (blinded_text, substitutions)."""
    out, n = text, 0
    for tok in sorted(ROLE_TOKENS, key=len, reverse=True):
        pat = re.compile(re.escape(tok), re.IGNORECASE)
        out, k = pat.subn(MASK, out)
        n += k
    # collapse runs of adjacent masks produced by overlapping tokens
    out = re.sub(r"(\[ROLE\]\W{0,3}){2,}", MASK + " ", out)
    return out, n


def split_row(line):
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def is_sep(line):
    return bool(re.match(r"^\|[\s:|-]+\|?\s*$", line.strip()))


def extract_file(path):
    records = []
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("|") and not is_sep(line):
            header = [c.lower() for c in split_row(line)]
            if any(h in ("finding", "findings") for h in header) and i + 1 < len(lines) \
                    and is_sep(lines[i + 1]):
                fi = next(j for j, h in enumerate(header) if h in ("finding", "findings"))
                si = next((j for j, h in enumerate(header)
                           if h in ("source", "from", "who", "found by")), None)
                j = i + 2
                while j < len(lines) and lines[j].lstrip().startswith("|"):
                    cells = split_row(lines[j])
                    if len(cells) > fi and re.match(r"^\**\d+\**$", cells[0]):
                        raw_role = cells[si] if (si is not None and len(cells) > si) else None
                        text = cells[fi]
                        blinded, subs = blind(text)
                        records.append({
                            "file": os.path.basename(path),
                            "line": j + 1,
                            "row": cells[0].strip("*"),
                            "role_raw": raw_role,
                            "role": normalise_role(raw_role),
                            "finding": text,
                            "blinded": blinded,
                            "mask_substitutions": subs,
                            "blinded_chars": len(blinded),
                        })
                    j += 1
                i = j
                continue
        i += 1
    return records


def main():
    # SEARCH-SPACE: only CONDITIONS-*.md in this directory. The output file is *.json.
    paths = sorted(glob.glob(os.path.join(HERE, "CONDITIONS-*.md")))
    records = []
    for p in paths:
        records.extend(extract_file(p))
    for k, r in enumerate(records, 1):
        r["id"] = f"F{k:03d}"
    by_role = {}
    for r in records:
        by_role[r["role"]] = by_role.get(r["role"], 0) + 1
    payload = {
        "generated_by": "extract_findings_134.py",
        "preregistration": "PREREGISTRATION-134.md",
        "files_scanned": [os.path.basename(p) for p in paths],
        "files_with_finding_tables": sorted({r["file"] for r in records}),
        "n_findings": len(records),
        "by_role": dict(sorted(by_role.items())),
        "mask_tokens": ROLE_TOKENS,
        "records": records,
    }
    out = os.path.join(HERE, "findings-134.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True,
                                       ensure_ascii=False).encode()).hexdigest()
    print(f"{len(records)} findings from {len(payload['files_with_finding_tables'])} files")
    for role, n in payload["by_role"].items():
        print(f"  {role:<16} {n}")
    print(f"payload sha256 {digest}")
    unmasked = [r["id"] for r in records if r["mask_substitutions"] == 0]
    print(f"records with no mask substitution: {len(unmasked)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
