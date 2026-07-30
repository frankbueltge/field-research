#!/usr/bin/env python3
"""chronicle_check.py — refuse to land a chronicle entry the receiving site cannot read.

WHY THIS EXISTS (2026-07-30, session 73)
----------------------------------------
`chronicle.json` is not ours alone. The ecology's site copies it verbatim into its own
tree and validates it; if the parse fails, the whole build fails, nothing deploys, and
no practice's work publishes — not only ours. On 2026-07-30 sessions 71 and 72 each
wrote an entry with no `summary` at all and a `works` value carrying prose instead of a
slug. Both were invalid. The gate stayed red and this practice could not see why,
because a different error of ours was failing an earlier step and hiding it.

So: an entry is not "written" until it parses. This script is the check that says so,
and it runs offline, on our side, before landing.

THE SCHEMA IS NOT OURS AND IS PINNED, NOT INVENTED
--------------------------------------------------
The constraints below are transcribed from the receiving repository's published source:

    repo   : github.com/frankbueltge/frankbueltge.de   (public)
    file   : src/lib/field/chronicle.ts  ->  `upstreamEntrySchema`
    commit : f9033b3adf222b62e8a14858939111e54f5b82d6   (read 2026-07-30)
    sha256 : d5f7ca997344e382df4f3c0737d2c07f209bb9534ba2695a6b7aa317b2f5f561

    collective_session : integer > 0
    date               : /^\\d{4}-\\d{2}-\\d{2}$/
    move               : string, length >= 1
    summary            : string, length >= 20
    works              : array of strings, each /^[a-z0-9-]+$/   (default [])
    verdict            : string length >= 1, or null              (default null)

Keys beyond these are permitted and ignored by the receiver (`note`, `correction`);
this practice uses them and they are not validated here beyond being JSON.

THE LIMIT OF THIS INSTRUMENT, STATED PLAINLY
--------------------------------------------
It is a REPLICA of a schema owned by someone else, pinned to one commit. If the
receiver changes that schema, this check will keep passing and be wrong — it cannot
detect its own staleness, which is the exact failure mode the work this practice was
reviewing the same day is about. Re-read the pinned file when the gate reports a
`ChronicleError`-shaped failure that this script does not reproduce.

It also does NOT check the receiver's second gate — that every session rendered from
`journal/` is covered by exactly one chronicle entry with a resolvable anchor — in the
receiver's own terms, because that arm needs the site's hand-curated spine for sessions
1..24, which does not live in this repository. What it checks instead is the part that
is decidable here: from the earliest session this file covers onward, journal sessions
and chronicle entries stand one-to-one.

USAGE
-----
    python3 tools/chronicle_check.py            # check, print findings
    python3 tools/chronicle_check.py --quiet    # exit status only

Exit 0 = would parse. Exit 1 = would turn the ecology's build red.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
FENCE_RE = re.compile(r"^(```|~~~)")
# Anchor derivation, transcribed from the same repository's src/lib/engines/journal.ts
# (`sessionAnchor`): a heading names its session either as "Session N ..." or as
# "... collective session N ...".
HEAD_NUM_RES = (re.compile(r"^Session (\d+)", re.I), re.compile(r"collective session (\d+)", re.I))


def entry_errors(i: int, e: dict) -> list[str]:
    """Every way this entry would fail the receiver's parse. Not the first — all of them."""
    out: list[str] = []
    if not isinstance(e, dict):
        return [f"entry {i}: not an object"]

    cs = e.get("collective_session")
    if not (isinstance(cs, int) and not isinstance(cs, bool) and cs > 0):
        out.append(f"collective_session must be a positive integer, got {cs!r}")

    date = e.get("date")
    if not (isinstance(date, str) and DATE_RE.match(date)):
        out.append(f"date must match YYYY-MM-DD, got {date!r}")

    move = e.get("move")
    if not (isinstance(move, str) and len(move) >= 1):
        out.append("move must be a non-empty string")

    summary = e.get("summary")
    if not isinstance(summary, str):
        out.append(f"summary is REQUIRED and must be a string, got {type(summary).__name__}")
    elif len(summary) < 20:
        out.append(f"summary must be at least 20 characters, got {len(summary)}")

    works = e.get("works", [])
    if not isinstance(works, list):
        out.append(f"works must be an array, got {type(works).__name__}")
    else:
        for w in works:
            if not (isinstance(w, str) and SLUG_RE.match(w)):
                out.append(f"works entry must be a bare slug [a-z0-9-]+, got {w!r}")

    verdict = e.get("verdict", None)
    if verdict is not None and not (isinstance(verdict, str) and len(verdict) >= 1):
        out.append("verdict must be a non-empty string or null")

    return [f"entry {i} (session {cs}, {date}): {m}" for m in out]


def journal_sessions(root: Path) -> list[tuple[int | None, str, str]]:
    """(session number or None, day, heading) for every H1 in journal/, fence-aware."""
    found = []
    for path in sorted(root.glob("journal/*.md")):
        day = path.stem
        in_fence = False
        for line in path.read_text(encoding="utf-8").splitlines():
            if FENCE_RE.match(line):
                in_fence = not in_fence
            elif not in_fence and line.startswith("# "):
                heading = line[2:].strip()
                num = None
                for rx in HEAD_NUM_RES:
                    m = rx.search(heading)
                    if m:
                        num = int(m.group(1))
                        break
                found.append((num, day, heading))
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--quiet", action="store_true", help="exit status only")
    args = ap.parse_args()

    errors: list[str] = []
    notes: list[str] = []

    try:
        entries = json.loads((ROOT / "chronicle.json").read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 — any failure here is a hard stop
        print(f"chronicle.json could not be read as JSON: {exc}")
        return 1

    if not isinstance(entries, list):
        print("chronicle.json must be a JSON array")
        return 1

    for i, e in enumerate(entries):
        errors.extend(entry_errors(i, e))

    # (collective_session, date) is the receiver's identity for a session — the engine's
    # own numbering has drifted before (two days both claiming session 24), so the pair
    # must be unique or the receiver silently drops the later one as already covered.
    seen: dict[tuple, int] = {}
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            continue
        key = (e.get("collective_session"), e.get("date"))
        if key in seen:
            errors.append(f"entry {i}: duplicate (collective_session, date) {key} — also at entry {seen[key]}")
        seen[key] = i

    for i, e in enumerate(entries):
        if isinstance(e, dict) and isinstance(e.get("date"), str):
            if not (ROOT / "journal" / f"{e['date']}.md").exists():
                errors.append(f"entry {i}: no journal/{e['date']}.md for this entry")

    # Parity, in the part decidable here (see the module docstring).
    covered = {(e["collective_session"], e["date"]) for e in entries
               if isinstance(e, dict) and isinstance(e.get("collective_session"), int) and isinstance(e.get("date"), str)}
    if covered:
        first = min(cs for cs, _ in covered)
        for num, day, heading in journal_sessions(ROOT):
            if num is None:
                notes.append(f"journal/{day}.md: heading names no session number ({heading!r}) — positional anchor on the site")
            elif num >= first and (num, day) not in covered:
                errors.append(f"journal/{day}.md session {num} has no chronicle entry ({heading!r})")
        headings = {(n, d) for n, d, _ in journal_sessions(ROOT) if n is not None}
        for cs, day in sorted(covered):
            if cs >= first and (cs, day) not in headings:
                errors.append(f"chronicle entry (session {cs}, {day}) has no matching journal heading")

    if not args.quiet:
        print(f"chronicle.json: {len(entries)} entries checked against the receiver's pinned schema")
        for n in notes:
            print(f"  note    {n}")
        for e in errors:
            print(f"  FAIL    {e}")
        if not errors:
            print("  PASS    every entry would parse; journal and chronicle stand one-to-one")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
