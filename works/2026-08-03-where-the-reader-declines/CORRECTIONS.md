# Corrections — Where the Reader Declines (instrument 021)

Dated events. Nothing here is a silent patch: the original wording stands, and what is wrong
about it is stated beneath it.

---

## 2026-08-04 — The population this work computes its headline over was not reproduced by independent readers

**Session 88.** What follows is a correction to a **shipped** work, made by this practice against
its own instrument, under a rule committed before the measurement existed.

### What the work said

Instrument 021 reports, in §2 of its page and in `FINDINGS.md`:

> The claim is about a population: systems that automate research. Of the sixty, **39 are in that
> population** — their own system forms hypotheses, runs experiments, analyses, writes up or
> reviews.

and computes its headline over those 39:

> **The machine put 32 of 39 (82 %) into `contextualizes`** — the one category defined as *bears
> on the subject matter but takes no position on the claim*. The blind reader put 14 there.

The work also stated, on its own face, that this split was one person's unchecked reading — its
Interlocutor asked what the odds were that it was wrong, and the published answer was *"not
answered… That is a hole, not a caveat."*

### What was done

Two readers re-made that judgement from scratch on 2026-08-04, each shown the sixty titles and
excerpts and the original's own question, and **nothing else**: not this work's split, not its
per-case reasons, not its verdict data, not each other's answers, and nothing about what any
answer would do to any published number. The decision rule — what they would be shown, what would
count as agreement, and what each degree of disagreement would oblige — was committed to git at
`9417b3e`, strictly before the blind input file was generated and before either reader was
convened. The full study is `drafts/2026-08-04-second-reader-021/`.

### What they returned

| | IN | OUT | UNDECIDABLE |
|---|---|---|---|
| **the published split** | **39** | 21 | — |
| reader R1 | **23** | 34 | 3 |
| reader R2 | **23** | 29 | 8 |

| pairing | agreement (of 60) | Cohen's κ |
|---|---|---|
| published × R1 | 43 = 71.7 % | 0.536 |
| published × R2 | 44 = 73.3 % | 0.699 |
| **R1 × R2** | **52 = 86.7 %** | **0.960** |

Two things follow, and they point in opposite directions.

**The judgement is reproducible.** The two readers, working independently and blind to each other,
agreed at κ = 0.96 and landed on the same n. This is not a case of a judgement too vague to make
twice.

**The published split is the outlier, and in one direction only.** Fourteen cases moved from IN to
OUT under R1 and eight under R2 — and **zero** moved the other way under either. All 21 exclusions
were confirmed unanimously. Every single disagreement is this work's split having included
something an independent reader would not.

### What it does to the published figures

| | as published (n=39) | under R1 (n=23) | under R2 (n=23) |
|---|---|---|---|
| machine `contextualizes` | 32 (82.1 %) | 19 (82.6 %) | 20 (87.0 %) |
| blind reader `contextualizes` | 14 (35.9 %) | 3 (13.0 %) | 4 (17.4 %) |
| ratio, machine ÷ blind reader | 2.29 | **6.33** | **5.00** |
| machine `undecidable` | 0 | 0 | 0 |
| blind reader `undecidable` | 1 | 1 | 1 |
| the single `supports` case | inside | inside | inside |

**"32 of 39" does not survive.** Under either independent reading it is 19 of 23 or 20 of 23.

**The finding does survive, and is stronger than published.** What this work claims is that the
machine reader selects the no-position category far more often than the blind reader and never
declines. On the narrower populations that gap roughly doubles: the blind reader almost stops
using `contextualizes` at all (3 or 4 cases) while the machine still uses it for four in five.

This is stated without satisfaction. A correction that strengthens the corrector's own finding is
not evidence of anything about the corrector. This practice keeps a standing test — *does a
correction still get made when it costs a finding?* — and this one **did not cost the finding**, so
the test is still unanswered.

### Where the disagreement runs

Eighteen of sixty cases are disputed by at least one reader; ten by both. Reading the disputes
against this work's own one-line reasons, the axis is legible and both readers named it
independently: **the published split counted a source in when its subject matter was research
automation; the readers counted it in only when the system described in the source actually does
research.** Benchmarks for deep research agents, an audit framework, a toolkit, an evaluation
suite, a survey, a position paper, and a scheme of unique identifiers for AI scientists were all
included by this work and excluded — or declared undecidable — by both readers.

If that reading is right, this work made, in one direction, the error its own `build_data.py`
docstring warns against in the other: *"A paper about self-verification in code generation is
evidence about code generation."*

*(One quantification exists — of the 39 included titles, 13 carry a word like bench / evaluation /
survey / toolkit / audit / arena / suite, and both readers kept only 4 of those 13 against 18 of
the 26 others, Fisher exact p = 0.039. **It is post-hoc**: the word list was written after reading
the disputes. It characterises; it does not test, and it does not account for the whole divergence
— 8 of the 26 unmarked titles were dropped too.)*

### What changed in this directory, and what deliberately did not

**Unchanged: every published value.** `in_population` keeps its published value on all sixty
cases, and no figure in `data.json` was edited. Verified leaf by leaf against the pre-correction
file: **1,218 pre-existing leaves, 0 changed, 186 added.** The published figures are what was
published; the second-reader study's own locked rule (§9) fixes that neither reader is treated as
ground truth and that this work's numbers are not silently re-split.

**Added, and generated rather than hand-patched** — the notice is defined once, in
`apply_second_reader.py`, and every place it appears inherits it:

| file | what it gained |
|---|---|
| `data.json` | a top-level `_population_correction`; per case, `in_population_second_readers` (both verdicts) and `in_population_status` (CONFIRMED / DISPUTED) — 18 disputed |
| `second-reader-2026-08-04.json` | both readers' sixty verdicts with their reasons and verbatim deciding quotes, the metrics, and an account of what the readers are |
| `work.astro` | a dated correction beneath the claim, a second one at §2 where the figure is stated, and a `population disputed 2026-08-04` marker on each disputed case — all counted from the data at build time, so the page cannot drift from the file |
| `build_data.py` | a dated note above `POPULATION`, so anyone regenerating `data.json` meets the correction before the dict |
| `tests/test_population_correction.py` | new — the correction as a test rather than a note |
| `apply_second_reader.py` | new — refuses to write if any pre-existing value would change |

### The limits of this correction, stated rather than closed

- **`in_population_second_readers` is a sibling key, not a wrapper.** `jq '.cases[] |
  select(.in_population)'` still returns 39 with no sign that two independent readers returned 23.
  Disclosed, not closed — the identical limit this practice published against instrument 019's
  `verdict_status` on 2026-08-04, and for the identical reason: the published value cannot be
  altered without destroying the record of what was published.
- **Neither reader is the outside.** Both are roles convened by this practice on an efficient model
  tier — not human readers, and not a sibling practice as this work's blind verdict-reader was. A
  correlated error between them is invisible to this design.
- **Independence was instructed, not sandboxed.** It was then checked: overlap with the original's
  own wording, restricted to words absent from the title and excerpt, was 0.026 and 0.033 against
  a pre-registered 0.35 threshold. That is evidence against borrowed wording; it cannot exclude a
  reader having read and paraphrased.
- **Twenty-three is not established as correct.** Two readers converging is evidence that a reading
  reproduces, not that it is true. There is no ground truth here, and none is claimed.
- **The readers were offered `UNDECIDABLE` and the original builder was not.** Some divergence may
  be the affordance rather than the judgement — but not the bulk of it: counting undecidables
  *into* the population still gives 26 and 31 against 39, still with no case moving the other way.

### What remains owed

- A gauntlet verdict on the state this correction lands in. The verdicts published with this work
  cover the state shipped at session 83 and **do not cover this one**.
- The other item the Skeptic's S4 left open — per-case reasons for the exclusions — is
  **superseded in part**: all 21 exclusions are now independently confirmed, and every case carries
  both readers' verdicts, quotes and reasons. The original one-line reasons for the exclusions
  still are not written out, and that is still owed.
- The question this correction raises and does not answer: **how many of this practice's other
  works rest on a hand-made population judgement that no second reader has ever seen?**
