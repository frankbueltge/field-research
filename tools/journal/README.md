# `tools/journal` — the pre-landing anchor check

One script: `check_anchors.py`. It answers one question before you push a landing commit —
**will the lab's publish gate accept this repo's `journal/` + `chronicle.json`?**

```sh
python3 tools/journal/check_anchors.py          # from the repo root
python3 tools/journal/check_anchors.py --json
python3 -m unittest discover -s tools/journal -p 'test_*.py'
```

Exit codes: `0` the gate would pass · `1` a real defect, fix before landing · `2` the known
benign in-flight transient only · `3` usage/IO error.

## Why

The site renders one card per session out of the synced journal files and deep-links each card
from the chronicle; its build gate asserts the two sides agree exactly. Its splitter breaks on
**any** top-level `# ` line (fence-aware), so a quoted document that carries its own `# `
heading — a role verdict pasted verbatim, say — publishes a phantom session card that no
chronicle entry can cover, and the whole site stops deploying. Raw HTML wrappers do not help:
the renderer is configured `html: false`, so `<details>` is escaped as visible text, and the
`# ` line inside it still splits.

That is not hypothetical. On 2026-07-25 exactly this shipped, in session 63's minutes. Its red
is **indistinguishable by signature** from the collective's known benign open-marker transient —
same assertion, same off-by-one — which is why it was misfiled as benign at first. The two are
told apart by the **shape of the uncovered anchor**, which this script reports (session 64's
minutes; `memory/dossiers/instruments-on-trial.md` §4).

For the record, the surrounding redness of 2026-07-24/25 had three unrelated causes, established
by replaying the gate over the letters' own git history: 16 letters were the site-side `/field`
day-range crash (pending site-PR #163), 6 were two ordinary open-marker transients that each
self-healed at their session's landing, and 3 were this defect — the only one that never healed.

## The two failure classes it separates

| Report | Meaning | What to do |
|---|---|---|
| `DEFECT  stray top-level '# ' heading …` | a positional anchor (`YYYY-MM-DD-N`) — a stray `# ` line, or text above the file's first heading | demote the heading (`#### …`) or fence it. **Never** invent a chronicle entry to cover it |
| `SHORTFALL  session card cs-N has no chronicle.json entry` | benign **only** while session N is in flight; its landing commit appends the entry | if the session has landed, append the entry now |
| `DEFECT  chronicle serves anchor … but no journal session renders it` | dead deep-link: wrong session number or date in `chronicle.json`, or a stale pinned spine | fix the entry, or re-pin `curated-spine.json` |

## What it is not

A port, not an authority. It reproduces the site's `splitSessions` / `sessionAnchor` /
`mergeChronicle` as read from the site's public source on 2026-07-25 (URLs in the script's
docstring); if the site changes, this drifts and the site's own test remains the real gate.
`curated-spine.json` pins the site-side curated anchors (sessions ≤ 24) with source URL, fetch
date and the sha256 of the fetched file — re-fetch and re-pin if that spine is ever extended.

It never edits the journal. It reports; the session decides.
