# Where the Reader Declines — findings

**Status:** draft, gauntlet run 2026-08-03. Not shipped.

## The question

One claim, fixed before anything was read:

> *Systems that automate the research cycle end to end verify their own outputs
> independently of the component that produced them.*

Sixty published arXiv abstracts, drawn mechanically. Four category definitions,
locked and hash-pinned before the labelling. A sibling practice (Ulysses)
labelled all sixty **blind** — no access to what was being measured — and gave a
one-sentence reason and a named deciding rule per case. Then a machine reader
(`gemini-3.5-flash-lite`) classified the same sixty under the same definitions.

The question this work asks is not about AI scientists. It is:

> **Where does an automatic reader land when the criteria demand a commitment?**

## The measurement

Reproduced independently for this work by re-joining the committed files
(`build_data.py`), not copied from the runtime's own report:

- agreement **31 of 57 decidable cases = 54.4 %**
- majority-class floor **42.1 %** — what a classifier scores by always naming
  the commonest label
- a second run of the same machine over byte-identical frozen inputs scored
  **52.6 %**, so **differences under ~2 points are noise**. That second figure
  comes from a runtime commit (`cc6df74`) that is **not on the default branch**;
  the variance claim inherits that weakness (`VERIFICATION.md`, F2).

## The finding

The claim is about a population: systems that automate research. Of the sixty,
**39 are in that population** — their own system forms hypotheses, runs
experiments, analyses, writes up or reviews. The other 21 are about reasoning,
code generation, robotics, arithmetic, computer operation, fact-checking,
negotiation and style. They are marked, not dropped.

Within those 39:

| | blind reader | machine |
|---|---|---|
| supports | 1 | 1 |
| contradicts | 6 | 2 |
| qualifies | 17 | 4 |
| contextualizes | 14 | **32** |
| undecidable | 1 | 0 |

**The machine put 32 of 39 (82 %) into `contextualizes`** — the one category
defined as *bears on the subject matter but takes no position on the claim*.
The blind reader put 14 there.

Across the full sixty the same shape holds: 43 of 60. The blind reader's
contradictions land in that column seven times; its qualifications fifteen times.
Both are movements **away** from committing.

**And the undecidable move was never used.** The criteria carry
`R-undecidable-is-a-finding`; the output schema carries an `undecidable` flag;
the prompt's **last sentence** is *"If the criteria cannot decide this case at
all, answer `undecidable` and say in the rationale which word or distinction the
excerpt fails on."* The affordance existed at every level. The blind reader used
it three times. The machine used it zero times.

## What this does and does not license

**Measured:** under identical definitions, identical excerpts and an explicit
undecidable affordance, the machine reader selects the no-position category more
than twice as often as the blind reader, and never declines.

**Not established:** that this is *evasion* — a disposition. `contextualizes` is
a broad definition ("a definition, a background measurement, a count, a
description of the field, or a statement about something adjacent"), and a
reader applying a broad category literally will use it often. That is a
competing explanation this data does not exclude. It survives the Skeptic and
the language of this work was weakened accordingly (`SKEPTIC.md`, S1).

## The second result, and why it is second

Of the 38 decidable in-population sources, **one supports the claim**
(*Towards Verifiable and Self-Correcting AI Physicists for Quantum Many-Body
Simulations* — verifiers separate from the generating agents, asserted of the
framework as such) and **six contradict it**.

That is a thin base and it is reported as one: `supports` has n=1, far below the
20–30 per category that would make a per-category figure readable. It is stated
because it is what the blind labels say, not because it can carry weight.

## Limits

- **Abstracts, not papers.** What a source says about itself in ~200 words. An
  adjacent measurement on a *different* corpus put an abstract at roughly 28 %
  of that corpus's numeric-token claims; that is an order of magnitude, not a
  property of these sixty, and must not be read as one. A system may verify
  independently and never mention it in an abstract.
- **One labelling practice, one machine, one run.** No second labeller, so
  "blind human-analogue" means one reader's careful reading, not a consensus.
- **The population split is a human judgement.** Written case by case with its
  reason in `build_data.py` so any line can be contested alone.
- **Contamination cannot be excluded.** The excerpts are published abstracts
  that may have been in the machine's training data.

## The builder's own failure, on the record

The population split was first attempted with a keyword test over titles
(`scien|research|discovery|…`). It reported 31 in-population and — worse — put
the single `supports` **outside** the population, because *"Towards Verifiable
and Self-Correcting AI Physicists"* contains none of those words. The finding
derived from it was stated to the responsible human as *"zero of thirty support
the claim"*. That was false, and it was false about the one case carrying the
most weight.

It was caught by reading the sixty titles.

This is the third instance of the same substitution during this work's
construction: a `grep` over mentioned identifiers counted three of one archive
run's verifications into another's; a regex over rationales was proposed for a
question that needed ten texts read; and this. **The work's subject is a reader
that reaches for a pattern where a reading is required. Its builder did the same
thing three times while building it.** That belongs on the face of the work, not
in a footnote.
