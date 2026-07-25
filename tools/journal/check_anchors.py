#!/usr/bin/env python3
"""Pre-landing check: will the lab's publish gate accept this repo's journal + chronicle?

WHY THIS EXISTS
---------------
The lab site renders one card per *session* out of the synced journal files and deep-links
each card from the chronicle. Its build gate asserts that the two sides agree exactly
(`src/lib/field/chronicle.test.ts`, "every served anchor resolves against the real synced
journals": `expect(served.length).toBe(used.size)`). A single stray top-level `# ` line
anywhere in a journal file therefore publishes a phantom session card that no chronicle entry
can cover — and reds the gate for the whole site, from our side.

That happened on 2026-07-25 (session 64's minutes): a quoted role verdict carried its own `# `
heading into session 63's minutes. Its red looked exactly like the collective's known benign
open-marker transient — same assertion, same off-by-one — so the signature alone could not tell
a real defect from a timing artifact. The two are told apart by the SHAPE of the uncovered
anchor, which this script reports: a positional `YYYY-MM-DD-N` anchor is always a real defect;
the newest `cs-N` is the transient that self-heals at that session's landing.

This script makes reproducing the gate cheap — one command, before landing. It is a *check*,
not a fix, and nothing enforces it: no hook, no workflow. It never edits the journal.

WHAT IT REPRODUCES (and from where)
-----------------------------------
Ports of the two site functions, read from the site's public source on 2026-07-25:
  - `splitSessions`  — https://raw.githubusercontent.com/frankbueltge/frankbueltge.de/main/src/lib/engines/journal.ts
    Breaks on ANY top-level H1, fence-aware; leading text before the first H1 stays a
    heading-less chunk.
  - `sessionAnchor` / `uniqueSessionAnchor` — same file. `collective session N` → `cs-N`;
    `Session N` → `pre-<day>-N` on files dated <= 2026-07-01, else `cs-N`; otherwise the
    positional fallback `<day>-<index>`. Collisions get a day suffix, first claimant keeps the
    clean anchor.
  - `mergeChronicle` — https://raw.githubusercontent.com/frankbueltge/frankbueltge.de/main/src/lib/field/chronicle.ts
    Curated spine is never overwritten; an upstream (= our `chronicle.json`) entry is appended
    only when no entry already covers the same (collective_session, date).

Caveat, stated plainly: this is a *port*, so it can drift from the site if the site changes.
It is an early-warning instrument, not an authority — the site's own test remains the gate.

USAGE
-----
    python3 tools/journal/check_anchors.py            # from the repo root
    python3 tools/journal/check_anchors.py --json     # machine-readable

Exit codes: 0 = the gate would pass · 1 = a real defect (act before landing) · 2 = the known
benign in-flight transient only (a `cs-N` anchor whose chronicle entry the landing commit will
add) · 3 = usage/IO error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JOURNAL_DIR = os.path.join(REPO_ROOT, "journal")
CHRONICLE = os.path.join(REPO_ROOT, "chronicle.json")
SPINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "curated-spine.json")

PRE_CONSTITUTION_CUTOFF = "2026-07-01"


# --- ports of the site's rendering logic ------------------------------------------------

def split_sessions(body: str) -> list[str]:
    """Return one heading string per rendered session card ('' = heading-less chunk)."""
    chunks: list[list[str]] = []
    current: list[str] = []
    in_fence = False
    for line in body.split("\n"):
        if re.match(r"^(```|~~~)", line):
            in_fence = not in_fence
        elif not in_fence and re.match(r"^# ", line) and any(l.strip() for l in current):
            chunks.append(current)
            current = []
        current.append(line)
    if current:
        chunks.append(current)

    headings: list[str] = []
    for chunk_lines in chunks:
        chunk = "\n".join(chunk_lines)
        if not chunk.strip():
            continue
        m = re.match(r"^\s*# ([^\n]+)", chunk)
        headings.append(m.group(1).strip() if m else "")
    return headings or [""]


def session_anchor(heading: str, day: str, index_in_file: int) -> str:
    m = re.search(r"collective session (\d+)", heading, re.I)
    if m:
        return f"cs-{int(m.group(1))}"
    m = re.match(r"^Session (\d+)", heading, re.I)
    if m:
        n = int(m.group(1))
        return f"pre-{day}-{n}" if day <= PRE_CONSTITUTION_CUTOFF else f"cs-{n}"
    return f"{day}-{index_in_file}"


def unique_session_anchor(used: set[str], heading: str, day: str, index_in_file: int) -> str:
    base = session_anchor(heading, day, index_in_file)
    anchor = base
    if anchor in used:
        anchor = f"{base}-{day}"
    n = 2
    while anchor in used:
        anchor = f"{base}-{day}-{n}"
        n += 1
    used.add(anchor)
    return anchor


# --- the two sides the gate compares ---------------------------------------------------

@dataclass(frozen=True)
class Rendered:
    anchor: str
    day: str
    heading: str


def rendered_sessions(journal_dir: str = JOURNAL_DIR) -> list[Rendered]:
    """Every session card the site would render, in the site's chronological order."""
    out: list[Rendered] = []
    used: set[str] = set()
    for name in sorted(f for f in os.listdir(journal_dir) if f.endswith(".md")):
        day = name[:-3]
        with open(os.path.join(journal_dir, name), encoding="utf-8") as fh:
            body = fh.read()
        for i, heading in enumerate(split_sessions(body)):
            out.append(Rendered(unique_session_anchor(used, heading, day, i), day, heading))
    return out


def served_anchors(chronicle_path: str = CHRONICLE, spine_path: str = SPINE) -> list[str]:
    """Every anchor the site would serve: curated spine + our chronicle, merge rule applied."""
    with open(spine_path, encoding="utf-8") as fh:
        spine = json.load(fh)["entries"]
    anchors: list[str] = [e["anchor"] for e in spine]
    with open(chronicle_path, encoding="utf-8") as fh:
        chronicle = json.load(fh)

    # The site keys coverage on (collective_session, date) because our numbering has drifted
    # before — and it seeds that key set from the curated spine as well as from upstream, so a
    # chronicle entry re-claiming a spine session/date pair is skipped rather than duplicated.
    covered: set[tuple[int | None, str]] = {
        (e["collective_session"], e["date"]) for e in spine
    }
    taken = set(anchors)
    upstream = sorted(chronicle, key=lambda e: (e["date"], e["collective_session"]))
    for entry in upstream:
        key = (entry["collective_session"], entry["date"])
        if key in covered:
            continue
        covered.add(key)
        anchor = f"cs-{entry['collective_session']}"
        if anchor in taken:
            anchor = f"{anchor}-{entry['date']}"
            n = 2
            while anchor in taken:
                anchor = f"cs-{entry['collective_session']}-{entry['date']}-{n}"
                n += 1
        taken.add(anchor)
        anchors.append(anchor)
    return anchors


# --- the report -------------------------------------------------------------------------

def check(journal_dir: str = JOURNAL_DIR,
          chronicle_path: str = CHRONICLE,
          spine_path: str = SPINE) -> dict:
    rendered = rendered_sessions(journal_dir)
    served = served_anchors(chronicle_path, spine_path)
    rendered_set = {r.anchor for r in rendered}
    served_set = set(served)

    stray = [
        {"anchor": r.anchor, "day": r.day, "heading": r.heading}
        for r in rendered
        if r.anchor not in served_set and re.match(r"^\d{4}-\d{2}-\d{2}-\d+$", r.anchor)
    ]
    missing_entry = [
        {"anchor": r.anchor, "day": r.day, "heading": r.heading}
        for r in rendered
        if r.anchor not in served_set and not re.match(r"^\d{4}-\d{2}-\d{2}-\d+$", r.anchor)
    ]
    unrendered = [a for a in served if a not in rendered_set]

    if stray or unrendered or len(served) != len(rendered):
        status = "TRANSIENT" if (missing_entry and not stray and not unrendered) else "DEFECT"
    else:
        status = "PASS"
    # A shortfall made only of `cs-N` anchors is the recognised in-flight transient: the
    # session's own landing commit adds chronicle entry N. Anything else is ours to fix now.
    if status == "PASS" and missing_entry:
        status = "TRANSIENT"

    return {
        "status": status,
        "rendered": len(rendered),
        "served": len(served),
        "stray_headings": stray,
        "sessions_without_chronicle_entry": missing_entry,
        "served_anchors_not_rendered": unrendered,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--journal-dir", default=JOURNAL_DIR)
    ap.add_argument("--chronicle", default=CHRONICLE)
    ap.add_argument("--spine", default=SPINE)
    args = ap.parse_args(argv)

    try:
        report = check(args.journal_dir, args.chronicle, args.spine)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"check_anchors: cannot run — {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"rendered session cards: {report['rendered']}")
        print(f"served chronicle anchors: {report['served']}")
        for s in report["stray_headings"]:
            print(
                f"DEFECT  stray top-level '# ' heading in journal/{s['day']}.md renders a phantom\n"
                f"        session card (anchor {s['anchor']}) that no chronicle entry can cover:\n"
                f"        \"{s['heading'] or '(text above the first heading)'}\"\n"
                f"        Fix: demote it (#### …) or fence it — do not add a chronicle entry for it."
            )
        for s in report["sessions_without_chronicle_entry"]:
            print(
                f"SHORTFALL  session card {s['anchor']} (journal/{s['day']}.md) has no chronicle.json\n"
                f"           entry. Benign only while that session is in flight — its landing commit\n"
                f"           must append the entry. Otherwise: append it now."
            )
        for a in report["served_anchors_not_rendered"]:
            print(
                f"DEFECT  chronicle serves anchor {a} but no journal session renders it —\n"
                f"        a dead deep-link (wrong session number/date, or a re-pinned spine)."
            )
        print(f"status: {report['status']}")

    return {"PASS": 0, "DEFECT": 1, "TRANSIENT": 2}[report["status"]]


if __name__ == "__main__":
    sys.exit(main())
