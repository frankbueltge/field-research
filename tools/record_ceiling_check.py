#!/usr/bin/env python3
"""record_ceiling_check.py — count a work's process record against rule 6's ceiling.

WHY THIS EXISTS (2026-08-06, session 96)
----------------------------------------
Production Amendment rule 6: "A work's process record beyond committed code and data
stays under 3,000 words."

Session 95's hostile critic counted one line's record at 10,161 words and found that no
document in it acknowledged the ceiling existed. Session 96 compressed the record and
then, in the very section arguing about word counts, printed a figure that was stale
before the commit was made: the paragraph stating "RECORD.md 2,090 words" was itself
293 words long, so the file was 2,383 words at the moment the claim was written, and
2,705 by the end of the session. A third figure, 2,126, had been written into
`memory/open-questions.md` for the same file at a commit where it measured 2,090.

Session 96's own Interlocutor: "a single script ... that computes and asserts the
record's own word count at build time, so a document about precision stops publishing
three different figures for the same file in one afternoon."

This is that script. The lesson it encodes is not about arithmetic. A hand-carried
number describing a document that is still being written is a claim that cannot be true
at the moment it is made — the same failure this collective keeps finding in the
surfaces it measures, reproduced in its own record three sessions running.

WHAT COUNTS
-----------
Prose. Markdown files in the draft or work directory, EXCEPT files the caller names as
exempt. Code (`.py`, `.sh`, `.js`, `.html`) and data (`.json`, `.log`, `.csv`) are
outside the ceiling by the rule's own wording ("beyond committed code and data").

Exemptions are NOT decided here. This script takes them as an argument, prints them by
name, and prints BOTH totals — with and without. A count that quietly applied an
exemption would be the thing it exists to prevent.

USAGE
-----
    python3 tools/record_ceiling_check.py drafts/<slug>/
    python3 tools/record_ceiling_check.py drafts/<slug>/ --exempt PREREGISTRATION.md
    python3 tools/record_ceiling_check.py drafts/<slug>/ --quiet    # exit status only

Exit 0 = the non-exempt total is under the ceiling. Exit 1 = it is over.
The exit status deliberately ignores the exempt total, which is why that total is
always printed: the script reports the number the collective must argue about, and
refuses to be the thing that decides it.

THE LIMIT OF THIS INSTRUMENT, STATED PLAINLY
--------------------------------------------
`wc -w`-style whitespace counting counts markdown syntax, table pipes and URLs as
words. It therefore OVERCOUNTS prose, which is the safe direction for a ceiling but
means this script and a markup-stripped count will disagree by a few percent. Both are
printed. Neither is authoritative; the rule does not say which it means, and this
script does not decide that either.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CEILING = 3000

PROSE_SUFFIXES = {".md", ".txt", ".rst"}

# Markup removed for the second count: fenced code, inline code, link targets,
# headers, emphasis markers, table pipes, list bullets, blockquote markers.
_FENCE = re.compile(r"```.*?```", re.S)
_INLINE_CODE = re.compile(r"`[^`]*`")
_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_BARE_URL = re.compile(r"https?://\S+")
_MARKS = re.compile(r"[#>*_|~\-]+")


def count_raw(text: str) -> int:
    return len(text.split())


def count_stripped(text: str) -> int:
    t = _FENCE.sub(" ", text)
    t = _INLINE_CODE.sub(" ", t)
    t = _LINK.sub(r"\1", t)
    t = _BARE_URL.sub(" ", t)
    t = _MARKS.sub(" ", t)
    return len(t.split())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("directory", help="draft or work directory to count")
    ap.add_argument(
        "--exempt",
        action="append",
        default=[],
        metavar="FILENAME",
        help="a prose file the caller claims is exempt; repeatable. "
        "The claim is printed, never evaluated.",
    )
    ap.add_argument("--quiet", action="store_true", help="exit status only")
    args = ap.parse_args()

    root = Path(args.directory)
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    exempt = set(args.exempt)
    counted: list[tuple[str, int, int]] = []
    exempted: list[tuple[str, int, int]] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in PROSE_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        row = (str(path.relative_to(root)), count_raw(text), count_stripped(text))
        (exempted if row[0] in exempt else counted).append(row)

    missing = exempt - {r[0] for r in exempted}

    total_raw = sum(r[1] for r in counted)
    total_stripped = sum(r[2] for r in counted)
    exempt_raw = sum(r[1] for r in exempted)
    exempt_stripped = sum(r[2] for r in exempted)

    over = total_raw >= CEILING

    if not args.quiet:
        print(f"{root}  —  process record against rule 6's {CEILING}-word ceiling")
        print(f"{'':2}{'file':<34}{'raw':>8}{'stripped':>10}")
        for name, raw, stripped in counted:
            print(f"{'':2}{name:<34}{raw:>8}{stripped:>10}")
        print(f"{'':2}{'COUNTED TOTAL':<34}{total_raw:>8}{total_stripped:>10}")
        if exempted:
            print()
            print("  claimed exempt by the caller — printed, not evaluated:")
            for name, raw, stripped in exempted:
                print(f"{'':2}{name:<34}{raw:>8}{stripped:>10}")
            print(f"{'':2}{'WITH EXEMPT FILES':<34}"
                  f"{total_raw + exempt_raw:>8}{total_stripped + exempt_stripped:>10}")
        if missing:
            print()
            for name in sorted(missing):
                print(f"  WARNING: --exempt {name} matched no file in {root}")
        print()
        if over:
            print(f"  OVER    the counted record is {total_raw - CEILING} words over the ceiling")
        else:
            print(f"  UNDER   {CEILING - total_raw} words of headroom on the counted record")
        if exempted:
            print("          the exempt total above is the number the collective must argue")
            print("          about; this script does not decide it.")

    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main())
