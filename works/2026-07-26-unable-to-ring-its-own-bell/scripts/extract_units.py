"""
scripts/extract_units.py — PREREGISTRATION.md §2 corpus extraction, fixed and unit-tested.

Splits every journal/*.md file into session-section units on lines beginning "# " (a
top-level markdown heading, no leading whitespace, not "##" or deeper), orders units by
(filename ascending, then position within file ascending), applies the six §2 exclusion
rules IN THE ORDER GIVEN, and tokenizes the survivors with the parent instrument's
`tokenize()` UNCHANGED (imported, not reimplemented).

**One exclusion beyond the six line-level rules, applied at the file level (see
DEVIATIONS-CANDIDATES.md item 1).** §2's "Source" line reads "every file matching
journal/*.md in this repository at the lock commit"; taken fully literally that includes
`journal/2026-07-26.md`, which already existed at the lock commit (committed earlier in
the same session, before the lock) and carries one top-level heading ("# Session 66",
this session's own opening). §5 states explicitly and unconditionally: "This run's own
output is not in the corpus. The journal entry this session writes becomes unit 74 in any
later run; the corpus is frozen at this document's lock commit, so the probe cannot
measure the session that built it." That sentence is only satisfiable by excluding
`2026-07-26.md` itself: session 66 is the session that produced this pre-registration and
is running this extraction, so its own journal file is "this run's own output" regardless
of which commit it happens to already be sitting in. The pretest (§0,
`provenance/feasibility-pretest.md`) enumerates exactly 73 units over 23 calendar dates
ending at unit 73 = 2026-07-25 — consistent only with this exclusion, not with the literal
glob. This file is therefore hardcoded as excluded, by name, with this citation.
"""
import glob
import json
import os
import re
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DRAFT_DIR = os.path.dirname(_SCRIPT_DIR)
_REPO_ROOT = os.path.dirname(os.path.dirname(_DRAFT_DIR))
_PARENT_SCRIPTS = os.path.join(
    _REPO_ROOT, "works", "2026-07-25-no-signal-to-extend", "scripts"
)
sys.path.insert(0, _PARENT_SCRIPTS)
from tokenizer import tokenize  # noqa: E402

JOURNAL_DIR = os.path.join(_REPO_ROOT, "journal")
OUT_PATH = os.path.join(_DRAFT_DIR, "provenance", "units.jsonl")
EXPECTED_N = 73

# This run's own journal entry — see module docstring. Excluded by filename, not by any
# property of its content, so the exclusion is unaffected by what the entry says.
EXCLUDED_FILES = {"2026-07-26.md"}

# Ship-time corpus freeze (session 67, 2026-07-26; deviation D16 in PREREGISTRATION.md §12).
# §5 freezes the corpus at the lock commit, and the EXPECTED_N assertion below enforces it —
# but as written the enforcement is a *crash* on any later re-run, because the journal keeps
# growing and `journal/*.md` keeps matching more files. That would make the shipped instrument
# unreproducible by anyone who runs it after this date. The freeze is therefore made explicit:
# only journal files dated on or before the corpus's last unit (2026-07-25) are read. This
# changes no number in this run — verified by re-running the whole pipeline before and after
# the edit; every output file is byte-identical apart from its generation timestamp.
CORPUS_FREEZE_LAST_DATE = "2026-07-25"

_HEADING_RE = re.compile(r"^# ")           # unit-boundary: top-level heading only, §2
_FENCE_RE = re.compile(r"^\s*```")          # rule 1
_BLOCKQUOTE_RE = re.compile(r"^\s*>")       # rule 2
_TABLE_ROW_RE = re.compile(r"^\s*\|")       # rule 3
_ANY_HEADING_RE = re.compile(r"^\s*#")      # rule 4 (any level, incl. the unit's own)
_INLINE_CODE_RE = re.compile(r"`[^`]*`")    # rule 5
_DATE_FROM_FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.md$")


def _split_into_raw_units(lines):
    """Split a file's lines into (heading_line, body_lines) chunks on top-level headings.

    Every returned chunk's first line is a `_HEADING_RE` match; lines before the first
    heading in a file (there are none in this corpus, but handled defensively) are
    dropped, matching §2: units are defined as starting AT a top-level heading."""
    boundaries = [i for i, line in enumerate(lines) if _HEADING_RE.match(line)]
    chunks = []
    for k, start in enumerate(boundaries):
        end = boundaries[k + 1] if k + 1 < len(boundaries) else len(lines)
        chunks.append(lines[start:end])
    return chunks


def apply_exclusions(raw_lines):
    """Apply §2's six exclusion rules, in order, to one unit's raw lines (heading line
    included). Returns the token list from the parent's tokenize()."""
    # Rule 1: fenced code blocks (open/close fence lines and everything between, dropped)
    after_fences = []
    in_fence = False
    for line in raw_lines:
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        after_fences.append(line)

    # Rule 2: blockquote lines dropped
    after_blockquote = [l for l in after_fences if not _BLOCKQUOTE_RE.match(l)]

    # Rule 3: table rows dropped
    after_table = [l for l in after_blockquote if not _TABLE_ROW_RE.match(l)]

    # Rule 4: heading lines dropped (any level, including the unit's own)
    after_heading = [l for l in after_table if not _ANY_HEADING_RE.match(l)]

    # Rule 5: inline code spans replaced by a single space
    after_inline_code = [_INLINE_CODE_RE.sub(" ", l) for l in after_heading]

    # Rule 6: join with newlines, tokenize with the parent's tokenize(), unchanged
    text = "\n".join(after_inline_code)
    return tokenize(text)


def extract_all():
    paths = sorted(glob.glob(os.path.join(JOURNAL_DIR, "*.md")))
    paths = [p for p in paths if os.path.basename(p) not in EXCLUDED_FILES]
    # Corpus freeze: drop anything the journal has grown since the lock (see above).
    paths = [
        p for p in paths
        if not _DATE_FROM_FILENAME_RE.match(os.path.basename(p))
        or _DATE_FROM_FILENAME_RE.match(os.path.basename(p)).group(1)
        <= CORPUS_FREEZE_LAST_DATE
    ]

    units = []
    index = 0
    for path in paths:
        fname = os.path.basename(path)
        m = _DATE_FROM_FILENAME_RE.match(fname)
        if not m:
            continue  # e.g. .gitkeep — not a dated journal file
        date = m.group(1)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().split("\n")
        chunks = _split_into_raw_units(lines)
        for pos, chunk in enumerate(chunks, start=1):
            heading_text = chunk[0][2:].strip()  # strip "# " prefix
            tokens = apply_exclusions(chunk)
            index += 1
            units.append({
                "index": index,
                "date": date,
                "position_in_file": pos,
                "heading": heading_text,
                "n_tokens": len(tokens),
                "tokens": tokens,
            })

    assert len(units) == EXPECTED_N, (
        f"extract_units: expected N == {EXPECTED_N}, got {len(units)}. "
        f"Corpus definition or exclusion logic has drifted from PREREGISTRATION.md §2/§5 "
        f"— this must not be silently accepted."
    )
    return units


def main():
    units = extract_all()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        for u in units:
            f.write(json.dumps(u, ensure_ascii=False))
            f.write("\n")
    total_tokens = sum(u["n_tokens"] for u in units)
    print(f"wrote {OUT_PATH}: N={len(units)} units, {total_tokens} total tokens")


if __name__ == "__main__":
    main()
