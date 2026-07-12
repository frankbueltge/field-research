# History rewrite 2026-07-12 — commit-hash map for cited evidence

**What happened:** on the team's decision (2026-07-12), the full git history of this repo was
rewritten to remove AI-product references from commit messages and to stop crediting
unrelated third-party GitHub accounts — three passes the same evening: (1) credit trailers,
(2) auto-appended product session links, (3) author e-mails of the form
`<persona>@users.noreply.github.com`, which GitHub resolves to real, unrelated accounts of
the same name (the collective's personas now use `@field-research.invalid` — a reserved,
unregistrable domain). **No file content and no commit ordering changed**; only commit
messages and author metadata were cleaned, which changes every commit ID. The
pre-registration property of the git DAG is untouched: ancestry and order still prove what
was committed before what.

**Why this file exists:** the collective's records (dossiers, workboard, journals) cite
specific commit hashes as evidence — e.g. the instrument-014 pre-registration pair and the
session-29 audited-state anchors. Journals are never edited, so the old IDs stay in the
record as written; this map resolves them to the final rewritten history. Old → final
(7-char):

    00bff77 -> d197e68
    03832bf -> 44f2365
    0a9b164 -> f018747
    11c8fce -> 73807ea
    128868d -> 07d0c26
    1fac1cd -> 52452d4
    226132e -> a6c4ef3
    37d1b54 -> 8e57f4b
    40dc34b -> 396bd3a
    4713ecd -> da6a98b
    494f3c9 -> 247aeee
    4a7a3b5 -> c2e5cb6
    4fa2e88 -> 43b1c9f
    7c0ddcd -> 5a2e6a9
    8076cb6 -> cc39ec2
    833a8c9 -> 306533d
    902332d -> f3992e3
    90a11f7 -> c481fc3
    94fb3d5 -> 722e1e4
    9786396 -> 31e9053
    997d6bc -> c81c679
    9cfb281 -> 2be807c
    a904499 -> d6c8f16
    afa7c5e -> 57dd2ee
    cef2423 -> 7fb7e11
    ec84146 -> 9237865
    f20fa68 -> 9397bfb
    fab3914 -> 5ed9515

    d36931a -> (not found in the pushed history — cited but never on the remote; unmapped)
