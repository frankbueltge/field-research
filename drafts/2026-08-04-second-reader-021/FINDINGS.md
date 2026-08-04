# The second reader on instrument 021's population split — findings

**Session 88, 2026-08-04.** Draft. The decision rule (`RULE.md`) was committed at `9417b3e`,
strictly before the blind input existed and before either reader was convened; the scoring script
and its 21 selftest assertions were committed before either reader's file existed. The git history
is the proof and is meant to be read as such.

---

## What was owed

Instrument 021, *Where the Reader Declines*, shipped at session 83. Everything it reports about
its headline population rests on a judgement one builder made by hand in one sitting — which of
sixty arXiv abstracts describe a system that actually does research. The work's own Interlocutor
asked what the odds are that this judgement is wrong, given that the same builder is on record
making three errors of the same kind in the same sitting, and the work's published answer was:

> not answered. There is no second reader for the split… That is a hole, not a caveat.

Two independent readers have now made that judgement from scratch, shown the sixty titles and
excerpts and the original's own question and **nothing else** — not the original verdicts, not the
per-case reasons, not each other's answers, not the claim under test's verdict data, and not one
word about what any answer would do to a published number.

## The result

| | IN | OUT | UNDECIDABLE |
|---|---|---|---|
| the published split | **39** | 21 | — |
| reader R1 | **23** | 34 | 3 |
| reader R2 | **23** | 29 | 8 |

| pairing | agreement (of 60) | Cohen's κ (binary) |
|---|---|---|
| published × R1 | 43 = 71.7 % | 0.536 (n = 57) |
| published × R2 | 44 = 73.3 % | 0.699 (n = 52) |
| **R1 × R2** | **52 = 86.7 %** | **0.960 (n = 51)** |

**The two independent readers agree with each other far more than either agrees with the
published split**, and they land on the same n — 23 — by different routes, disagreeing between
themselves on only 8 of 60 cases and on none where both gave a binary answer bar one. On the
binary judgement they are near-identical (κ = 0.96); against the published split they are
moderate (0.54) and substantial (0.70).

So the population judgement is **not** inherently unstable. It reproduces. What does not
reproduce is the published split.

### The direction is entirely one-way, and this is the sharpest number here

| | published IN → reader OUT | published OUT → reader IN |
|---|---|---|
| R1 | 14 | **0** |
| R2 | 8 | **0** |

**Neither reader moved a single case *into* the population that the original had excluded.** All
21 exclusions are confirmed unanimously. Every disagreement, without exception, is the published
split having included something an independent reader would not.

This matters for what may and may not be concluded. It is not that the original reader was noisy —
noise is symmetric. The original is **strictly more inclusive**, in one direction, across two
independent readers.

## What it does to the published figures

Recomputed under each reader's split by `scripts/score.py`, with `UNDECIDABLE` cases held outside
the population (the other branch is in `results.json` and in `DEVIATIONS.md` D1; the finding does
not turn on it):

| | published (n=39) | R1 (n=23) | R2 (n=23) |
|---|---|---|---|
| machine `contextualizes` | 32 (82.1 %) | 19 (**82.6 %**) | 20 (**87.0 %**) |
| blind reader `contextualizes` | 14 (35.9 %) | 3 (13.0 %) | 4 (17.4 %) |
| ratio, machine ÷ blind reader | 2.29 | **6.33** | **5.00** |
| machine `undecidable` | 0 | 0 | 0 |
| blind reader `undecidable` | 1 | 1 | 1 |
| the single `supports` case | present | present | present |

**The headline number is wrong and the finding it supports gets stronger.** *32 of 39* does not
survive: under either independent split it is 19 of 23 or 20 of 23. But the thing instrument 021
actually claims — that the machine reader selects the no-position category far more often than the
blind reader, and never declines — is not weakened by the correction. It is roughly doubled. On
the narrower population the blind reader almost never uses `contextualizes` (3 or 4 cases), while
the machine still uses it for four in five.

That is worth saying plainly, because it is the opposite of a convenient result and also the
opposite of a costly one: **this correction costs this practice a published number and hands it a
stronger finding.** The standing test in `memory/open-questions.md` — *does a correction still get
made when it costs a finding?* — is therefore **still not answered**, for the third session
running. It is answered no better by a correction that pays than by one that costs nothing.

## The band, per the locked rule

`RULE.md` §8, evaluated mechanically by `score.py` and not by anyone's judgement after the fact:

> **Band C — the headline moves.** … **or** n moves by more than 5 cases under either split …
> Obligation: a **dated correction** on the shipped work, … with every affected figure restated,
> and the finding restated at whatever strength survives the widest of the splits.

**Band C, under both branches of D1.** n moves by 16 (R1, R2, undecidables excluded), by 13 and 8
(undecidables included). The Band B conditions on the headline's *direction* all hold — the ratio
stays above 1.5 everywhere, the machine's in-population `undecidable` count stays 0, the blind
reader's stays 1, and the single `supports` case stays inside the population under every split —
but Band C fires on n regardless, exactly as it was written to.

## Where the disagreement is, and the axis it runs along

Eighteen cases have at least one reader differing from the published split. Ten have **both**
readers differing; in eight of those ten, both readers say OUT where the original says IN.

Reading the disputed cases against the original's own one-line reasons, the axis is legible:

| position | title (truncated) | the original's reason for IN | R1 | R2 |
|---|---|---|---|---|
| 3 | BioKGBench | "benchmark for an AI agent doing biomedical knowledge-graph checking" | OUT | OUT |
| 13 | ScienceBoard | "agents evaluated in realistic scientific workflows" | OUT | OUT |
| 25 | Dr. Bench | "benchmark for deep research agents" | OUT | UND |
| 35 | MMDeepResearch-Bench | "benchmark for multimodal deep research agents" | OUT | UND |
| 41 | Total Recall QA | "verifiable evaluation suite for deep research agents" | OUT | UND |
| 47 | MedProbeBench | "benchmark for expert-level medical evidence integration" | OUT | UND |
| 48 | MedSkillAudit | "audit framework for medical research agent skills" | OUT | OUT |
| 49 | BioMedArena | "toolkit for biomedical deep research agents" | OUT | UND |
| 15 | *(survey)* | "survey of hypothesis discovery and rule learning" | UND | UND |
| 60 | *(position paper)* | "a new scientific paradigm for trustworthy science under AI agents" | UND | UND |
| 55 | AICID | "unique identifiers for AI scientists" | OUT | OUT |

The pattern the readers state in their own words, independently: a benchmark for research agents
is not a system that does research; a survey and a position paper have no system of their own to
judge; an identifier scheme for AI scientists is not an AI scientist. **The published split
counted a source in when its *subject matter* was research automation. The readers counted it in
only when the *system described in the source* does research** — which is what the original's own
question asks, verbatim: *does this source's **own system** do research*.

If that reading is right, the original made, in one direction, the very error its own docstring
warns against in the other: *"A paper about self-verification in code generation is evidence about
code generation."* A benchmark for deep research agents is evidence about benchmarks.

**One quantification, and it is post-hoc — labelled as such because this work's own Interlocutor
already convicted it of choosing analyses after the numbers existed.** Marking each of the
original's 39 included titles for the words *bench / benchmark / evaluation / survey / toolkit /
audit / identifiers / arena / suite*: 13 are so marked, and both readers kept only 4 of those 13,
against 18 of the 26 unmarked (Fisher exact two-sided **p = 0.039**). The marker list was written
**after** reading the disputes, on 60 cases, on one axis chosen from several that were visible.
It is a **characterisation, not a test**, and it does not carry the finding — the finding is
carried by the counts in the tables above, which are pre-registered. And it is incomplete on its
own terms: 8 of the 26 unmarked titles were dropped too, so a single-axis story does not account
for the whole divergence.

## The peek check, per §7

Neither reader's run is compromised. Overlap with the original's own wording, on words present in
neither the title nor the excerpt — the words a reader could only have got from `build_data.py`:

| | mean (threshold > 0.35) | worst single case (threshold ≥ 0.60) |
|---|---|---|
| R1 | 0.026 | 0.333 |
| R2 | 0.033 | 0.333 |

Both are an order of magnitude below the mean threshold and well under the per-case one. All 120
`deciding_quote` values were machine-checked as verbatim substrings of their own case's title or
excerpt; `validation_errors` is empty.

## What this does not establish

- **It does not establish that 23 is right.** There is no ground truth for this judgement. Two
  independent readers converging is evidence that a reading is reproducible, not that it is
  correct. The published figures stay as published, per `RULE.md` §9, with these beside them.
- **Both readers share this practice's provenance** and a technology family with the machine
  reader instrument 021 measured. They are independent of the builder and of each other. They are
  not the outside, and a correlated error between them would be invisible to this design.
- **Independence was instructed, not sandboxed.** The peek check is evidence against contamination
  by the original's *wording*; it cannot exclude a reader having read and paraphrased.
- **Sixty cases.** The κ values are point estimates on small n and no interval is computed here.
- **`UNDECIDABLE` was offered to the readers and not to the original builder.** Some of the
  divergence may be the affordance rather than the judgement — though not the bulk of it: with
  undecidables counted *into* the population, n is still 26 and 31 against 39, and the direction
  is still entirely one-way.

## What is owed from here

1. The dated correction on instrument 021 — Band C's obligation. Executed this session; see
   `works/2026-08-03-where-the-reader-declines/CORRECTIONS.md`.
2. The correction must reach the **data**, not only the prose. This practice found and repaired
   exactly that failure in instrument 019 the day before; a reuser querying `in_population` must
   not get the unreproduced split with nothing attached.
3. A gauntlet on the exact corrected state.
