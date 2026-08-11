#!/usr/bin/env python3
"""The index must see everywhere this practice writes.

Written 2026-08-12 (architect), after the same failure was found in three houses on one night:
a constitution is edited, the practice starts keeping records somewhere new, and the memory
tool's source list is not extended. Nothing fails loudly — `recall` keeps working perfectly on
a corpus that no longer holds the work, so the only way to know where anything stood is to read
it end to end.

Four gaps existed here when this was written — two found by reading, two found by this test
on its first run:

  · `notes/**` — 21 files of feasibility notes and spikes, unindexed since 2026-07-02
  · `deliveries/**` — 10 delivered packets with their verifier reports
  · `field-feedback/**` — 22 build-feedback letters to the practice
  · `memory/*.md` — the curated memory itself. PROTOCOL.md sends a session to "curated
    `memory/`" as the FIRST step of orientation, and only `memory/dossiers/**` was indexed, so
    claims.md, open-questions.md, discarded.md and downstream-commitments.md — the four files
    the constitution names first — were exactly the ones recall could not return.

So the check is not "does the tool work". It is: **does the index still point at the places this
repository actually keeps its records.**
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cli import SOURCE_GLOBS, _collect_source_files

REPO_ROOT = Path(__file__).resolve().parents[2]

# Directories holding this practice's records. A new one is added here in the same commit that
# starts writing to it — that is the whole discipline this file enforces.
RECORD_DIRS = ["journal", "works", "drafts", "notes", "deliveries", "field-feedback"]

# Files the constitution's orientation step names, which must be reachable by name.
CURATED_MEMORY = [
    "memory/claims.md",
    "memory/open-questions.md",
    "memory/discarded.md",
    "memory/downstream-commitments.md",
]


def _covered(rel_dir: str) -> bool:
    return any(glob.startswith(f"{rel_dir}/") for glob in SOURCE_GLOBS)


def test_every_record_directory_is_indexed() -> None:
    missing = [d for d in RECORD_DIRS if (REPO_ROOT / d).is_dir() and not _covered(d)]
    assert not missing, (
        f"these directories hold records but no SOURCE_GLOBS entry reaches them: {missing}. "
        "A session cannot recall what is not indexed, so it reads the whole record instead. "
        "Add the glob in the commit that starts writing there."
    )


def test_the_curated_memory_is_reachable() -> None:
    """The files the constitution sends a session to first must be in the index."""
    indexed = {p.resolve() for p in _collect_source_files(REPO_ROOT)}
    unreachable = [
        rel for rel in CURATED_MEMORY
        if (REPO_ROOT / rel).is_file() and (REPO_ROOT / rel).resolve() not in indexed
    ]
    assert not unreachable, (
        f"the curated memory is not reachable by recall: {unreachable}. PROTOCOL.md names "
        "'curated memory/' as the first step of orientation; if recall cannot return these, the "
        "instruction sends the session to files it then has to open by hand."
    )


def test_no_record_directory_is_silently_unindexed() -> None:
    """A new top-level directory holding markdown is either a record directory or declared."""
    not_records = {
        "archive": "superseded texts; recall should return the live text",
        "docs": "specification and design, not the practice's own record",
        "governance": "delegation documents, read directly and rarely",
        "memory": "indexed, both curated files and dossiers",
        "tools": "code",
        "pulse": "derived activity data, not prose",
        "atlas": "reference collection, not this practice's own record",
    }
    unaccounted = []
    for entry in sorted(REPO_ROOT.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        if entry.name in RECORD_DIRS or entry.name in not_records:
            continue
        if not any(entry.rglob("*.md")):
            continue
        unaccounted.append(entry.name)
    assert not unaccounted, (
        f"top-level directories holding markdown are neither indexed nor declared non-records: "
        f"{unaccounted}. Add each to RECORD_DIRS (and SOURCE_GLOBS) or to the declaration above."
    )
