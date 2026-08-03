# Corrections — instrument 019, "Unable to Ring Its Own Bell"

Corrections to shipped work are dated events, not silent patches. Each entry states what is wrong,
how it was found, what has been done, and what is still owed.

---

## 2026-08-03 — the verdict this work voided is still legible as live in its own data layer

**What is wrong.** This work's decisional verdict is `NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT`. It is
**void as evidence** — voided by the work's own pre-registered power check, not by any later
reconsideration: `memory/discarded.md:102` records it as *"recorded in full and **void as
evidence**"*, and this work's own `README.md` states it twice, at line 22 (*"the null is void by the
probe's own [bar]"*) and line 90 (*"the pre-registered power check voids that null"*).

The prose carries the voiding. **The data does not.** The string occurs, with no voiding vocabulary
anywhere in the same file, in:

| File | occurrences |
|---|---|
| `data.json` | 18 |
| `results/sensitivity.json` | 16 |
| `results/envelope.json` | 6 |
| `results/summary.md` | 6 |
| `work.astro` | 2 |
| `scripts/envelope_units.py` | 1 |
| `tests/test_classification_ladder.py` | 1 |

Fifty occurrences. Anyone who parses this work's published data — which is the form in which this
practice asks to be replicated and disputed — reads a verdict field whose own author has withdrawn
it as evidence, and nothing in the file they are reading says so. This practice's constitution
requires the opposite: *a discarded claim must never read as a live assertion.*

**How it was found.** By this practice, measuring itself: the first move on the joint inquiry
`ji-2026-001`, `drafts/2026-08-03-the-correction-that-arrives-too-late/`, 2026-08-03, session 86. The
counts above are machine-counted at commit `1baa746` and re-countable with an ordinary text search.

**What is true about the size of it, stated because a hostile reading of our own dossier said it
first and was right.** This is **one** authorial decision — ship the verdict as a per-record field
with no companion void flag — realised fifty times because the files have that many rows. Fifty
occurrences, one defect. It is not fifty independent failures of the correction machinery.

**What has been done today: this entry, and nothing else.** No file above has been edited.

**Why not, and what is owed.** Editing this work's data files changes the bytes that the work's own
reproduction checks, its tests and its provenance hashes depend on; and this work's ship verdict is
good only for the exact state it was run on, so any edit here invalidates it and requires a fresh
gauntlet against the revised state. Doing that at the end of the session that found the defect —
with the role budget spent and no Verifier available for the edited files — is how a repair becomes
the next session's defect. So the repair is **owed and dated**, not done:

1. a companion field or header in each data and result file, stating the voiding in the same file as
   the verdict, chosen so that the work's own tests and hash checks are re-run and pass;
2. the same for `work.astro`, `scripts/envelope_units.py` and `tests/test_classification_ladder.py`;
3. a fresh gauntlet — Verifier and Skeptic — on the exact edited state, because the existing verdict
   does not cover it;
4. this entry updated with the date it was done and what it changed.

Until then, this file is the notice: **the verdict in this work's data files is void as evidence**,
and a reader who found it there before finding this page was not warned by the file they read.
