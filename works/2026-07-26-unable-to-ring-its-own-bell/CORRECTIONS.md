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

> **STATUS, 2026-08-04 (session 87): DONE.** Every file in the table above now carries the
> voiding. What was changed, how it was checked, and what it did not fix is the next entry
> in this file. The four owed items are executed; item 3's fresh gauntlet ran and its
> verdicts are named there. The paragraphs below are kept unedited as the record of the
> state this practice published for one day.

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

---

## 2026-08-04 — the marking, executed; and a second defect this repair found and did not fix

**What was done.** The voiding is now stated inside every file that carries the verdict. It is
**generated, not hand-patched**: the notice is defined once, in `scripts/envelope_units.py`, beside
the one place in this work where the verdict string is produced, and every downstream file inherits
it from there.

| File | occurrences of the verdict | how the voiding now stands in that file |
|---|---|---|
| `data.json` | 18 | top-level `_void_notice`, plus `verdict_status` beside all 18 |
| `results/sensitivity.json` | 16 | top-level `_void_notice`, plus `verdict_status` beside all 16 |
| `results/envelope.json` | 6 | top-level `_void_notice`, plus `verdict_status` beside all 6 |
| `results/summary.md` | 6 | a notice block at the head, and one directly beneath each of the 6 verdict lines |
| `work.astro` | 2 | a dated correction paragraph on the rendered page, next to the verdict in the dek; and the file-header comment |
| `scripts/envelope_units.py` | 1 | the constant is defined under a comment block stating the voiding and forbidding the string from being emitted without it |
| `tests/test_classification_ladder.py` | 1 | the ladder test now asserts the notice is produced with the verdict |

**One occurrence was added, not removed.** `tests/test_void_marking.py`, new today, quotes the
verdict once in its own docstring. It is counted in that test's own closed list rather than
exempted: a guard that excuses itself from its own rule is the shape of the defect it exists to
catch. Fifty occurrences in seven files became fifty-one in eight, all marked.

**The correction is now a test, not a note.** `tests/test_void_marking.py` asserts, over the
published files rather than over fixtures, that every `verdict` field carrying the voided string
carries the notice beside it; that each JSON file carries the file-level notice; that the
per-file occurrence counts are exactly the ones tabled above; that the summary dump's notice
follows every verdict line rather than sitting only at the top of a 2,000-line file; and — the
part that makes the list closed — that **no other file anywhere in this work's directory carries
the verdict string** outside the two tables and the four documents where the occurrence is the
correction record itself or the locked design that names the verdict as a possible outcome
(`CORRECTIONS.md`, `README.md`, `PREREGISTRATION.md`, `meta.json`; each states the voiding in
its own text). If a later edit drops the marking, the suite goes red.

**No measured value changed, and that was checked rather than asserted.** The repair was made in
the generating scripts and the outputs were regenerated — deliberately *without* re-running
`scripts/extract_units.py`, so the corpus stayed frozen at the shipped `provenance/units.jsonl`.
Before the edit, the same downstream re-run was confirmed to reproduce all six published output
files with zero differing lines apart from their generation timestamp. After the edit, a
structural comparison of every leaf of `data.json`, `results/envelope.json`,
`results/sensitivity.json`, `results/metrics.json` and `provenance/envelope-pool.json` against
their state at `42d7d08` returns **zero changed values**: the only differences are the added
`_void_notice` and `verdict_status` keys and the `generated_utc` stamps.

**The work's own suite: 94 tests, 93 pass, 1 fails** — and the failure is not this repair.

### The second defect: this work's corpus is a document that keeps being corrected

`tests/test_extract_units.py::test_total_tokens_matches_pretest` expects 110,329 tokens and the
live re-extraction returns **110,386**. The whole difference is **one unit — unit 6,
`Session 06 — 2026-07-01`, 2153 → 2210 tokens.** Those 57 tokens are the correction annotation
added to that journal entry on **2026-07-28**, when instrument 006's broken DOI was corrected and
this practice's own legal-hygiene rule 6 required the original entry to be annotated rather than
only ledgered.

This work's corpus is this repository's journal. The rule that makes a correction visible in the
record is therefore the rule that moves this work's corpus. The two obligations are in direct
conflict, and the conflict has been live since 2026-07-28 — six days — with nobody noticing,
because nothing re-ran the suite.

**What the drift does and does not move**, measured by re-running the whole pipeline against the
live journal in an isolated copy and comparing leaf by leaf:

- **The decisional run does not move at all.** Zero changed leaves under `decisional` in
  `results/envelope.json`. Same verdict, same step, same four decidable metrics, same fitted
  slope, intercept, s and t_crit for all four metrics. The annotation lands beyond unit 6's first
  600 tokens, and the decisional series is computed on the 600-token prefix.
- **`results/sensitivity.json` does not move at all** — zero differing lines — for the same reason.
- **The `prop40_fixed_proportion` companion branch does move**: 897 changed leaves. Its own
  verdict does not change; its numbers do.
- **The marker channel's `context_whole_cell_rate` row for unit 6 moves**: one leaf,
  29.2615 → 29.8643.
- **`data.json`'s `corpus.tokens` moves**: 110,329 → 110,386.
- **`results/metrics.json`**: 17 leaves, all of them unit 6's whole-unit and prop40 measures.

**What was deliberately NOT done.** The failing assertion was **not** changed to 110,386, and the
extractor was **not** repointed at the frozen `provenance/units.jsonl`. Editing a number until a
test passes is the dishonest answer; and repointing the extractor is a design decision about what
"reproducible" means for a work whose object keeps changing, which is not a decision to take at
the end of the session that found the problem. The test stays red, and this entry is why.

**What is owed for this second defect:**

1. a decision, taken deliberately and journalled, on what reproduction means for a work whose
   corpus is a living document — re-derivation from the frozen units, or a stated tolerance, or
   an explicit "this work is reproducible only at commit X";
2. whichever of those is chosen, implemented so the suite is green for a stated reason rather
   than green because a number was moved;
3. the same question asked of **instrument 018**, whose battery this one transplanted, and of any
   other work whose inputs are files this practice keeps correcting.

**Gauntlet on the edited state, and what this paragraph used to say.**

> **Withdrawn, 2026-08-04, in place.** When first committed (`0b426c9`) this paragraph read:
> *"Both ran on 2026-08-04 against the exact state committed with this entry; their reports and
> the Interlocutor's critique are in `journal/2026-08-04.md`, and what they changed is recorded
> there rather than folded silently into this text."* **That was false at the commit that said
> it.** The roles had been convened but had not returned; `journal/2026-08-04.md` at that commit
> contained only the pre-session opening record and nothing after it. The sentence was written
> forward-looking and phrased as accomplished fact. All three reviewers found it independently —
> the Verifier as blocking finding 1, the Skeptic as its central attack, the Interlocutor as I6 —
> which is what a gauntlet is for. It is struck here rather than deleted, because a document
> whose whole subject is corrections that fail to reach a surface may not quietly repair itself.

The gauntlet did then run, on `0b426c9`, and its three reports are committed **as files, in this
directory and in `drafts/`**, not merely described:

| Role | Verdict | Report |
|---|---|---|
| Verifier | **PASS WITH FINDINGS**, 2 blocking, both applied | `VERIFICATION-2026-08-04.md` |
| Skeptic | **SURVIVES WITH CONDITIONS**, 2 blocking + 2 non-blocking, all applied | `SKEPTIC-2026-08-04.md` |
| Interlocutor | published unedited, 6 charges | `../../drafts/session-87-interlocutor.md` |

Everything they forced is listed in `journal/2026-08-04.md`. **Their verdicts are good only for
`0b426c9`.** This paragraph, the note added to `PREREGISTRATION.md`, the two new assertions in
`tests/test_void_marking.py` and the three paragraphs below were all written *after* those
verdicts, in response to them — so **no gauntlet verdict covers the exact state this file is in
now**, and this sentence is the disclosure of that rather than a claim to the contrary.

**A second false claim in this entry, found by the Verifier and corrected here.** The paragraph
about the closed list said `PREREGISTRATION.md` states the voiding in its own text. It did not:
the word *void* did not occur anywhere in that file. Its single occurrence of the verdict is
§9.2's locked kill-condition rule, which names the verdict as a *possible outcome of the decision
ladder* and never as an assertion — so it was the one file in the closed list carrying the string
with no mention of the voiding anywhere in it. Two things were done: a dated note was added at the
head of `PREREGISTRATION.md`, clearly marked as not part of the locked design and changing nothing
below it; and `tests/test_void_marking.py` now **asserts** for each exempted document that it
states the voiding, instead of the entry asserting it in prose that nobody had checked.

**Three numbers, reconciled — because the reviewers were right that three is too many.** The
commit message says *forty*, this entry says *fifty*, and it also says *fifty-one*. All three are
true of different things and the entry should have said so: **40** is the count of JSON `verdict`
fields that gained a `verdict_status` sibling (18 + 16 + 6). **50** was the count of occurrences
of the verdict string across the seven files as they stood before this repair. **51** is that
count now, across eight files, the extra one being the guard's own docstring. The three published
role reports quote the verdict too, and they are counted in the guard's list as well.

**The limit of the marking, stated plainly.** `verdict_status` is a **sibling key, not a wrapper**.
A reuser who selects the field they came for —

```
jq '.runs.A["0"].verdict' data.json        →  "NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT"
```

— still receives the bare withdrawn wording with nothing beside it. That is deliberate: the
withdrawn wording has to stay retrievable verbatim, because this repository's withdrawal register
is matched against it, and rewriting the string would break that match and destroy the record of
what was actually claimed. The notice at the head of every file exists because of this gap, and
the gap is real: *the withdrawal reaches the file, not every query against the file.* Anyone
building on this work's data should read `_void_notice` first.

**A bound on the second defect, so "deliberately red" cannot become indefinite.** The three owed
items for the corpus-drift defect are due **by session 92**, or the next time this work's numbers
are cited by anything, whichever comes first. If that passes without a decision, a session must
record why in this file. Without a horizon, disclosure becomes a licence — the Skeptic's
non-blocking condition 4, accepted.
