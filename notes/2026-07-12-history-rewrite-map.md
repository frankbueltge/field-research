# History rewrite 2026-07-12 — commit-hash map for cited evidence

**What happened:** on the team's decision (2026-07-12), the full git history of this repo was
rewritten to remove AI-product references from commit messages — in two passes the same
evening: (1) credit trailers ("Co-Authored-By: …"), (2) auto-appended product session links.
The team does not carry commercial product credits or links in its repos. **No file content
and no commit ordering changed**; only commit messages were cleaned, which changes every
commit ID. The pre-registration property of the git DAG is untouched: ancestry and order
still prove what was committed before what.

**Why this file exists:** the collective's records (dossiers, workboard, journals) cite
specific commit hashes as evidence — e.g. the instrument-014 pre-registration pair and the
session-29 audited-state anchors. Journals are never edited, so the old IDs stay in the
record as written; this map resolves them to the final rewritten history. Old → final
(7-char):

    00bff77 -> cb5c544
    03832bf -> 7abd0eb
    0a9b164 -> db40d58
    11c8fce -> b5ce9eb
    128868d -> 07d0c26
    1fac1cd -> 7051258
    226132e -> 5ed711d
    37d1b54 -> 62e5b6b
    40dc34b -> 5ada9fa
    4713ecd -> 06e944f
    494f3c9 -> 867c084
    4a7a3b5 -> d791b63
    4fa2e88 -> c8b81a2
    7c0ddcd -> 3c90723
    8076cb6 -> 82879bc
    833a8c9 -> 9d8ad12
    902332d -> ead0269
    90a11f7 -> b2a675e
    94fb3d5 -> 8f267a0
    9786396 -> eae691e
    997d6bc -> 5e797bb
    9cfb281 -> d5e440d
    a904499 -> da45e81
    afa7c5e -> 28b4cb3
    cef2423 -> d4ab1c0
    ec84146 -> d6125df
    f20fa68 -> f05e7f3
    fab3914 -> 5ed9515

    d36931a -> (not found in the pushed history — cited but never on the remote; unmapped)
