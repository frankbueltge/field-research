# The second reader on instrument 021's population split — decision rule

**Committed before either reader saw a single case.** Session 88, 2026-08-04.

This file exists because a rule written after the numbers exist is not a rule. Everything below —
what the readers are shown, what counts as agreement, and what each degree of disagreement obliges
this practice to do — is fixed here, in git, before the measurement. The precedent is
`drafts/2026-08-03-the-correction-that-arrives-too-late/RULE.md` (session 86), which did the same
thing for the joint inquiry.

---

## 1. The debt this discharges

Instrument 021, *Where the Reader Declines*
(`works/2026-08-03-where-the-reader-declines/`), shipped at session 83. Its headline is computed
over a **population of 39 of 60 sources**, and that population was selected by hand, by one
builder, in one sitting. The work's own Interlocutor asked (`INTERLOCUTOR.md`, I4) what the
probability is that this judgement is wrong given that the same builder is on record making three
errors of the same kind — substituting a pattern for a reading — in the same sitting. The work's
published answer:

> **Practice's response:** not answered. There is no second reader for the split, and the
> Skeptic's S4 records that the exclusions carry no per-case reason. The honest statement is that
> the split has the same provenance as three known errors and has not been independently checked.
> That is a hole, not a caveat.

The hole has been open since 2026-08-03 and was deferred at sessions 84, 85, 86 and 87.

## 2. The object, pinned

`works/2026-08-03-where-the-reader-declines/data.json` as committed at **`1949ea6`** (this
session's opening marker; the file is unchanged from its ship state at session 83). Sixty cases,
each with `position` (1–60), `title`, `excerpt`, `excerpt_sha256`, and — not shown to the readers —
`in_population`, `population_reason`, `exclusion_reason`, `gold`, `machine`.

The blind input file `blind-input.json` is generated from it mechanically by
`scripts/make_blind_input.py`, which carries **only** `case_id`, `title` and `excerpt`, in an order
shuffled by `random.Random(88).shuffle` (seed = the session number, recorded here so the shuffle
reproduces). No original judgement, no verdict, no count, no reference to instrument 021 or to what
any answer would do to any published figure appears in the file or in either reader's prompt.

## 3. The question the readers answer — verbatim, as the original builder wrote it

From `works/2026-08-03-where-the-reader-declines/build_data.py`, the docstring that defines the one
hand-made judgement in the work:

> does this source's own system do research — form hypotheses, run experiments, analyse, write up,
> review — or does it do something else (reasoning, code, robotics, arithmetic, computer
> operation, fact-checking, negotiation, style)?

and the reason the judgement exists, from the same file:

> A paper about self-verification in code generation is evidence about code generation. Counting
> it as evidence about research automation inflates the denominator with sources the claim never
> addressed.

The claim whose population it is, quoted to the readers as context and to nothing else:

> *Systems that automate the research cycle end to end verify their own outputs independently of
> the component that produced them.*

## 4. Two readers, not one

The debt names "a second reader". This rule convenes **two**, independently, from the same blind
input, with no contact between them and no access to each other's answers.

**Why two, declared in advance:** one reader can only tell us whether the original split is
idiosyncratic. Two tell us whether *the judgement itself* is stable. If R1 and R2 agree with each
other no better than either agrees with the original, then the population judgement is unstable in
general — a finding about the instrument, not a verdict against its builder. That distinction
cannot be drawn after the fact from a single reader, so it is bought here, before the fact.

**What both readers are, stated plainly and not dressed up:** convened roles of this practice on an
efficient model tier — not human readers, and not a sibling practice as instrument 021's blind
verdict-reader was. They are independent of the builder of the split and of each other. They are
not independent of this practice. That limit is a limit of this measurement and travels with every
number it produces.

**Independence is instructed, not sandboxed.** Both readers work from the excerpts in their prompt
and are instructed not to open this repository. Instruction is not enforcement, so §7 pre-registers
a check that would show a violation.

## 5. What each reader returns, per case

- `case_id` — echoed back.
- `verdict` — exactly one of `IN`, `OUT`, `UNDECIDABLE`.
- `deciding_quote` — a phrase copied verbatim from the title or excerpt that carries the decision.
- `reason` — one sentence, in the reader's own words.

`UNDECIDABLE` is offered deliberately. The original split is binary; forcing a binary answer would
manufacture agreement where a reader has none. Instrument 021's own sharpest finding is about a
reader that was given an undecidable affordance and never used it, so withholding one here would be
this practice measuring others by a standard it declines to apply to its own instrument.

## 6. The metrics, fixed now

Computed by `scripts/score.py`, over all 60 cases, for each of the three pairings **R1×original,
R2×original, R1×R2**:

1. **Raw agreement** on the binary IN/OUT, with `UNDECIDABLE` counted as **disagreement** with any
   binary verdict, and reported separately as its own count so the effect is visible rather than
   buried.
2. **Cohen's κ** on the binary IN/OUT over the cases where both members of the pair gave a binary
   verdict.
3. **Direction** — for each reader against the original: how many cases moved IN→OUT and how many
   OUT→IN, so a reader that is simply more inclusive is not confused with one that disagrees case
   by case.
4. **n under each split**, and the recomputed in-population tables.

## 7. The check that would show a reader peeked

Pre-registered because a reader that had read `build_data.py` would produce agreement that means
nothing. For each case, compare the reader's `reason` against the original's
`population_reason` / `exclusion_reason` on **content words that appear in neither the title nor
the excerpt** — the words a reader could only have got from the original text. Jaccard overlap on
that residue.

**Thresholds, fixed now:** any single case at ≥ 0.60, or a mean across the 60 above 0.35, and that
reader's run is **treated as compromised, discarded unused, and reported as discarded**. A
compromised run is not re-run into a clean one by re-prompting until it passes; if a run is
discarded, this session says so and the debt stays open.

## 8. The bands, and what each obliges

Recomputed under each reader's split, and stated in advance. "The headline" means the two sentences
instrument 021 leads with: that the machine reader put **32 of 39 (82 %)** in-population sources
into `contextualizes`, against the blind reader's 14; and that the machine used `undecidable`
**zero** times where the blind reader used it once in-population.

**Which published figures move with the split, established before the readers ran** — because a
pre-registration that misstates what is at stake is worthless:

| figure | as published | moves with the split? |
|---|---|---|
| in-population n | 39 | **yes** |
| machine in-population `contextualizes` | 32 (82 % of 39) | **yes** |
| blind reader in-population distribution | 1 / 6 / 17 / 14 / 1 | **yes** |
| machine in-population distribution | 1 / 2 / 4 / 32 / 0 | **yes** |
| overall agreement | 31 of 57 decidable = 54.4 % | **no** — computed over all sixty |
| majority-class floor | 42.1 % | **no** — same |

So a moved split cannot rescue or destroy the agreement figure. It can only move the population
finding, which is the one under audit.

- **Band A — confirmed.** Both readers return the original's binary verdict on all 60. Obligation:
  a dated note in the work recording independent confirmation, both readers' per-case reasons
  published, the hole recorded closed. No figure changes.

- **Band B — disagreement that does not move the headline.** Under *both* readers' splits, the
  machine's `contextualizes` share within the population still exceeds the blind reader's by a
  factor of at least **1.5**, *and* the machine's in-population `undecidable` count is still **0**
  while the blind reader's is at least **1**. Obligation: publish every disputed case with all
  three verdicts and reasons; publish the recomputed tables under each split beside the shipped
  ones at equal prominence; a dated note in the work stating the range the figures span. No
  withdrawal.

- **Band C — the headline moves.** Either Band B condition fails under either reader's split, **or**
  n moves by more than 5 cases under either split, **or** the single `supports` case leaves the
  population under either split. Obligation: a **dated correction** on the shipped work, in the form
  this practice's rule 6 requires — the original stated and struck, not silently replaced — with
  every affected figure restated, and the finding restated at whatever strength survives the widest
  of the splits.

## 9. No adjudication, and no ground truth

There is no external ground truth for this judgement. Neither reader is treated as correct and
neither is the original.

**The conductor of this session does not adjudicate disputed cases.** Disputed cases are published
as disputed, with all three verdicts and all three reasons side by side. This is fixed here because
the alternative — a conductor deciding, case by case, after seeing what each decision does to a
published number — is precisely the failure the pre-registration exists to prevent.

The shipped figures stay as computed under the original split, because those are the figures that
were published. What the readers produce is published beside them, not in place of them.

## 10. What this cannot settle

- It cannot establish that the original split is *right*, only whether independent readers reach it.
- Both readers share this practice's provenance and a technology family with the machine reader
  instrument 021 measured. They are not the outside.
- Sixty cases is sixty cases; the κ's confidence interval will be wide and will be reported wide.
- If both readers are wrong in the same direction, this measurement cannot see it.

---

*Locked at session 88, 2026-08-04, before `scripts/make_blind_input.py` was run and before either
reader was convened. Any change to this file after that point is a deviation and is logged as one,
in `DEVIATIONS.md`, with its reason.*
