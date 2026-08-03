#!/usr/bin/env python3
"""Selftest for measure.py — synthetic fixtures only, no repository data.

Every assertion pins one clause of RULE.md, including the two deviations (D2, D3).
Run from the repository root:

    python3 drafts/2026-08-03-the-correction-that-arrives-too-late/selftest.py
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import measure as M  # noqa: E402

FAILS = []
N = 0


def check(name, got, want):
    global N
    N += 1
    if got != want:
        FAILS.append(f"{name}: got {got!r}, want {want!r}")


# --------------------------------------------------------------- §3.3 sessions
check("session single", M.sessions_in("2026-07-03, session 07"), [7])
check("session range", M.sessions_in("2026-07-02, sessions 02–03"), [2, 3])
check("session two named", M.sessions_in("session 46 (ledgered session 47)"), [46, 47])
check("session none", M.sessions_in("2026-07-03"), [])
check("session hyphen", M.sessions_in("the session-33 journal entry"), [33])

# --------------------------------------- §3.2 + deviation D2: heading attribution
heads = M.journal_sessions([
    "# Session 07 — 2026-07-01",
    "text",
    "# Journal — 2026-07-16 (collective session 39)",
    "text",
    "# Collective session 41 (2026-07-16, third invocation of the date)",
    "text",
    "## Session 99 — a level-two heading must not attribute",
    "text",
])
check("D2 plain heading", heads[1], 7)
check("D2 journal heading", heads[3], 39)
check("D2 collective heading", heads[5], 41)
check("D2 level-two ignored", heads[7], 41)

# ------------------------------------------ §3.5 + deviation D3: count claims
check("count digits", M.count_claim("`discarded.md` — 18 rows from the ledgers"), 18)
check("count words", M.count_claim("Six discard entries ledgered (session 07)"), 6)
check("count none", M.count_claim("ledgered in `memory/discarded.md`"), None)
check("D3 session id is not a quantity",
      M.count_claim("the session-33 journal entry stands as minutes, the"), None)
check("D3 quantity after a session id still counts",
      M.count_claim("session 41: two rows added to `discarded.md`"), 2)

# ------------------------------------------------------- §4.2 key-string filters
check("key too short", M.key_strings('the row said “too short here”'), [])
check("key too few words", M.key_strings('“averylongsinglewordstringwithoutanyspacesatall”'), [])
check("key drops a path",
      M.key_strings('“see drafts/2026-07-30-follow-the-line/results/audit.json for this”'), [])
check("key drops a url",
      M.key_strings('“fetched from https://example.org/some/long/path/here/now”'), [])
check("key drops a marker phrase",
      M.key_strings('“this sentence was withdrawn by the round-two skeptic”'), [])
check("key kept", M.key_strings('the claim “the rate rises to 54.5 per cent everywhere” was cut'),
      ["the rate rises to 54.5 per cent everywhere"])
check("key from backticks", M.key_strings('`the floor holds at one point one everywhere`'),
      ["the floor holds at one point one everywhere"])

# ------------------------------------------------- §4.5–4.6 occurrence + marking
with tempfile.TemporaryDirectory() as td:
    key = "the rate rises to 54.5 per cent everywhere"
    marked = os.path.join(td, "marked.md")
    unmarked = os.path.join(td, "unmarked.md")
    with open(marked, "w", encoding="utf-8") as fh:
        fh.write("intro\n**Erratum — the sentence below was withdrawn.**\n" + key + "\n")
    with open(unmarked, "w", encoding="utf-8") as fh:
        fh.write("intro\n" + key + "\ntrailing prose that says nothing about it\n")
    far = os.path.join(td, "far.md")
    with open(far, "w", encoding="utf-8") as fh:
        fh.write("withdrawn\n" + "\n" * 15 + key + "\n")

    overlap = os.path.join(td, "overlap.md")
    with open(overlap, "w", encoding="utf-8") as fh:
        fh.write("intro\n" + key + "\n")

    real_root = M.ROOT
    M.ROOT = td
    try:
        occ = M.scan([key], ["marked.md", "unmarked.md", "far.md"])
        # D4: two overlapping keys at one location must count as ONE occurrence
        dedup = M.scan([key, key[:35]], ["overlap.md"])
    finally:
        M.ROOT = real_root
    by_file = {o["file"]: o for o in occ}
    check("occurrences found", sorted(by_file), ["far.md", "marked.md", "unmarked.md"])
    check("marked neighbourhood", by_file["marked.md"]["marked_in_place"], True)
    check("unmarked neighbourhood", by_file["unmarked.md"]["marked_in_place"], False)
    check("marker outside the 10-line window does not count",
          by_file["far.md"]["marked_in_place"], False)
    check("D4 overlapping keys count once", len(dedup), 1)
    check("D4 both keys listed on the one occurrence", len(dedup[0]["keys"]), 2)

# ------------------------------------------------- surface classes (pre-read 7)
check("class journal", M.surface_class("journal/2026-07-01.md"), "journal")
check("class shipped", M.surface_class("works/x/data.json"), "shipped")
check("class shipped delivery", M.surface_class("deliveries/x/LETTER.md"), "shipped")
check("class memory", M.surface_class("memory/claims.md"), "curated-memory")
check("class drafts", M.surface_class("drafts/x/y.md"), "drafts")
check("class archive", M.surface_class("archive/x.md"), "archive")
check("class other", M.surface_class("WORKBOARD.md"), "other")

# --------------------------------------- D3: retrospective commentary is excluded
check("D8 tokens drop stopwords and short words",
      M.tokens("the session ledgered a paywalled mischaracterisation"),
      {"paywalled", "mischaracterisation"})

# ------------------------------------------------------ §4.3 the rights exclusion
entry = {"text": "a name was redacted from the served page under legal hygiene"}
check("rights rule fires",
      any(x in entry["text"].lower() for x in M.RIGHTS_EXCLUSIONS), True)
check("rights rule does not fire on ordinary text",
      any(x in "an ordinary withdrawn claim".lower() for x in M.RIGHTS_EXCLUSIONS), False)

# ------------------------------------------------------------- register parsing
reg = "\n".join([
    "| What | Why | Date |",
    "|---|---|---|",
    "| a claim | because | 2026-07-03, session 07 |",
    "",
    "## 2026-07-30 (session 71)",
    "",
    "- **A bullet entry** — withdrawn the same session it was written.",
    "  continuation line of the same bullet.",
    "",
])
entries = M.parse_register(reg)
check("register entry count", len(entries), 2)
check("register row session", entries[0]["sessions"], [7])
check("register bullet session", entries[1]["sessions"], [71])
check("register header row skipped",
      all("What | Why" not in e["text"] for e in entries), True)

print(f"{N - len(FAILS)} passed, {len(FAILS)} failed, {N} assertions")
for f in FAILS:
    print("  FAIL", f)
sys.exit(1 if FAILS else 0)
