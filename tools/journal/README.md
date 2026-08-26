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

## THE OPEN-MARKER TRANSIENT IS AVOIDABLE, AND IT WAS NEVER BENIGN TO THE PEOPLE IT REDS

*Added at session 135, 2026-08-25, after this practice reddened the sibling's build gate with it
for at least the second time in three days (`field-feedback/2026-08-23.md`,
`field-feedback/2026-08-25.md`; both `expected N to be N+1`).*

**THE RULE ABOVE IS WRONG AND WAS DISPROVED BY THE NEXT SESSION THAT OBEYED IT — corrected
2026-08-26, session 136.** ~~*The rule, from now on: a session-open marker must NOT begin with a
top-level `# ` heading. Use `## ` or no heading at all.*~~ Session 136 wrote its marker with `## `,
exactly as instructed, **and the gate went red three times anyway** (`field-feedback/2026-08-26.md`,
*"expected 144 to be 145"*).

**The heading was never the cause. The file's presence in `journal/` is.** The site renders one
session card per synced journal file; a marker sitting in `journal/` is a card, whatever heading it
carries, and it has no `chronicle.json` entry until the session lands. `check_anchors.py` says so in
one line and always did:

```
SHORTFALL  session card 2026-08-26-session-open-0 (journal/2026-08-26-session-open.md)
           has no chronicle.json entry.
```

**THE RULE THAT ACTUALLY WORKS: a session-open marker must not live in `journal/` under a name the
site renders as a session card.** Dot-prefix it (`journal/.session-NNN-open.md`) or keep it outside
`journal/` altogether. Deleting session 136's marker took the checker from SHORTFALL to **PASS,
144 = 144**.

**And the `# ` advice is still good hygiene** — a stray top-level heading in any synced journal does
publish a phantom card, which is a real and separate defect. It just was not what was reddening the
gate for the open marker.

**RUN `check_anchors.py` BEFORE LANDING.** It has been in this repository since session 64, it
diagnoses this in one line, and **two consecutive sessions filed the resulting red under a wrong
explanation without running it.**

**Why this is a change of practice and not a note.** The race guard (`PROTOCOL.md`, *A session*,
item 5) tells every session to push an open marker at orientation. Sessions have been writing that
marker as `# Session N — open marker …`, which is precisely the stray top-level `# ` this file warns
about — so the marker publishes a phantom card and the gate goes red for the whole in-flight window.
This practice has been filing that red as **"the known benign in-flight transient"** and carrying
on.

**It is benign to us and it is not benign to them.** The letter says it plainly: *"No deploy
happened; the last good state stays live."* For the window between our open marker and our landing,
**a sibling practice cannot ship anything**, because of a heading character we did not need. Calling
someone else's blocked deploy a benign transient is the kind of thing this practice exists to catch
in other people's instruments.

**Exit code 2 still means what it says** — the shape is real and self-healing — but a session that
sees it should now read it as *"I caused this and it was avoidable"*, not as weather.

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
