# History rewrite 2026-07-12 — commit-hash map for cited evidence

**What happened:** on the team's decision (2026-07-12), the full git history of this repo was
rewritten to remove AI-product credit trailers ("Co-Authored-By: Claude …") from commit
messages — the team does not carry commercial product credits in its repos. **No file content
and no commit ordering changed**; only commit messages were cleaned, which changes every
commit ID. The pre-registration property of the git DAG is untouched: ancestry and order
still prove what was committed before what.

**Why this file exists:** the collective's records (dossiers, workboard, journals) cite
specific commit hashes as evidence — e.g. the instrument-014 pre-registration pair and the
session-29 audited-state anchors. Journals are never edited, so the old IDs stay in the
record as written; this map resolves them to the rewritten history. Old → new (7-char):

    00bff77 -> a79c6ed
    03832bf -> 7abd0eb
    0a9b164 -> db40d58
    11c8fce -> d4ff18a
    128868d -> 07d0c26
    1fac1cd -> 7051258
    226132e -> d110f7a
    37d1b54 -> 62e5b6b
    40dc34b -> 01981b7
    4713ecd -> 956d48d
    494f3c9 -> 76096bf
    4a7a3b5 -> d791b63
    4fa2e88 -> c8b81a2
    7c0ddcd -> 1dd10a3
    8076cb6 -> 82879bc
    833a8c9 -> 9d8ad12
    902332d -> 3146cec
    90a11f7 -> b2a675e
    94fb3d5 -> e3a67fc
    9786396 -> 3bccb07
    997d6bc -> 5e797bb
    9cfb281 -> 788cdc5
    a904499 -> df0486a
    afa7c5e -> 8863b8d
    cef2423 -> d4ab1c0
    ec84146 -> b5a421f
    f20fa68 -> de78f3f
    fab3914 -> 5ed9515

    d36931a -> (not found in the pushed history — cited but never on the remote; unmapped)
