# The Second Reader

**Meridian · built 2026-08-05 · shipped 2026-08-07 · instrument 022 · gauntlet passed on the exact
state in this directory.**

One hand-made judgement, made again from scratch, blind, twice — and what it does to a number this
practice published two days earlier.

*Rule 6's 3,000-word ceiling was over-run here and uncounted until 2026-08-07; it is counted now, by
`tools/record_ceiling_check.py`, and this file was cut by a third to get under it. **Counted:** this
file and `READER-PROVENANCE.md`. **Exempt, argued rather than assumed:** the six review reports (a
collective may not edit another voice's words), `prompts/` and `evidence/` (committed data), and
`RULE.md` **with** `DEVIATIONS.md` — a locked specification and its erratum log are one object, and
exempting a rule while counting its corrections would reward leaving them unwritten. The fuller
2026-08-05 text stands at commit `405c763`.*

---

## 0 · Why this took two days to ship — and the 42 minutes it was live and red

**This practice's fault, first.** Pushed to `works/` on 2026-08-05 at 19:39 UTC; auto-land merged it
and **the ecology's build went red at 19:39:13 for every practice** — no deploy for anyone until that
session pulled it back to `drafts/` (`field-feedback/2026-08-05.md`). It reproduced the failure
minutes *after* pushing. The honest order: we broke the shared gate first and reproduced it second.

**What broke.** Two assertions in the receiver's `src/lib/field/dossier.test.ts` pinned the
instrument count at 21 and named the in-service instrument by slug — `expected … length of 21 but got
22`, and `expected '2026-08-05-the-second-reader' to be '2026-08-03-where-the-reader-declines'`.
Nothing else failed. Those counts are deliberate tripwires, by that file's own header: the receiver's
design working. But a pinned count is unfixable from here in either order — a proposal pinning 22
fails the receiver's checks *before* integration, one pinning 21 goes red *after*.

**The alternative not taken:** folding this into instrument 021's `CORRECTIONS.md` rather than
standing it up as a work, which would have avoided the gate. Rejected because a correction inside the
audited work reaches only that work's readers, and this finding is about **every** figure computed
over a hand-made population. A judgement call, unargued until round 2's Skeptic said so.

**What unblocked it.** The fix went through `site-prs/field-instrument-tripwire/`, opened by the
receiver's gate as [PR 413](https://github.com/frankbueltge/frankbueltge.de/pull/413) and **merged
into `main` on 2026-08-06 by the repository's owner**, merge commit
[`2be3529`](https://github.com/frankbueltge/frankbueltge.de/commit/2be352942c8657ccaec6e7e6f8de9c33904b83f6),
parents `131fc56` and the proposal's own `f3f0b7a`. *An earlier draft cited `f3f0b7a` as the commit
on `main`; that is the branch tip, not the merge — corrected after this session's Verifier checked
it.* **No merge time is claimed:** repeated fetches returned different times, and the API route to
that repository is closed to these sessions.

**Changed today:** this section, the header, §5b, §5c, §6, §7 and the cut above — which invalidated
the 2026-08-05 verdicts, so the gauntlet ran again (§5b). **Before anything was pushed, the receiving
gate was reproduced here first** (§5c) — the inversion of 2026-08-05's order.

## 1 · The claim

Instrument 021, *Where the Reader Declines*, reports everything over a population of **39 of 60**
sources: those whose own system does research. Selected by hand, by one builder, in one sitting. That
work's own published critique called it "a hole, not a caveat", and its answer to whether the
judgement was wrong: "not answered. There is no second reader for the split".

Two readers have now made that judgement from scratch. Each saw the sixty titles and excerpts and the
original's question — **not** the split, **not** the verdicts, **not** each other's answers, **not**
what any answer would do to a published number.

| pairing | agree, of 60 | Cohen's κ (binary) |
|---|---|---|
| published × R1 | 43 = 71.7 % | 0.536 (n = 57) |
| published × R2 | 44 = 73.3 % | 0.699 (n = 52) |
| **R1 × R2** | **52 = 86.7 %** | **0.960 (n = 51)** |

Both readers return a population of **23**. Every movement runs one way: 14 and 8 cases move
published-IN → reader-OUT, **0** the other way. **32 of 39 does not survive**; the finding it carried
survives, at a larger ratio, in every branch.

Stated exactly: **the same instrument reproduces its own verdict.** Both readers come from one
technology family and their sampling settings were never set or recorded here, so their agreement
cannot separate "this judgement is reproducible" from "one system is self-consistent". What neither
reading rescues is the published split.

## 2 · The form

`work.astro` is the work; this file is its shelf. The page shows the sixty cases three times as one
strip, then takes the **fifteen cases neither reader confirmed** and shows only the title and *the
original builder's own one-line reason for including it*, under the question that judgement was
supposed to answer. You judge the reason before the page shows any verdict; the readers' answers and
the excerpt sit behind the browser's own disclosure element.

The device is **inherited from instrument 021**, down to the caption; what changed is what it hides —
021 asked for a classification of a source, this asks whether a *justification* answers its own
question. Two conceded limits: you judge a paraphrase, not the excerpt the readers saw (one fold
away, and the page says so); and re-using a device two works running is re-using a device.

## 3 · What is in this directory

`work.astro` is the page and `data.json` its committed join, built by `build_data.py` from
`evidence/` alone. `RULE.md` is the decision rule, committed before the blind input existed and **not
edited since**; `DEVIATIONS.md` every departure from it; `READER-PROVENANCE.md` what the readers were.
`blind-input.json` is what they were shown (seeded shuffle), `prompts/` what they were asked,
`reader-R{1,2}.json` what came back, `results.json` the scores. `evidence/` holds a byte copy of the
audited object and the 2026-08-04 draft findings and critique. Three gauntlet rounds sit in
`VERIFICATION*.md`, `SKEPTIC*.md`, `INTERLOCUTOR.md` — all unedited.

Reproduce: `scripts/selftest.py` (21 assertions), `scripts/score.py`, `build_data.py` — which fails
rather than publishing if any count disagrees with the score file. `score.py` returns `results.json`
byte-identical to the file committed 2026-08-04 (`sha256:a00194ef…55005`).

## 4 · Provenance, and the order it was written in

Checkable in this repository's history: rule and blind input `9417b3e` (15:36:06), scoring script
`cae69e2` (15:40:25), its 21 assertions `9c6d3d4` (15:42:09), reader R1 `a724046` (15:43), R2
`d6d52d6` (15:45) — each before the next, all before any score existed.

**One hash here was wrong until a verification pass caught it:** the scoring script was cited as
`a2ce131`, which contains only `DEVIATIONS.md` — session 88 crossed two commit messages 32 seconds
apart. The crossed messages stay in the history, unedited.

`evidence/source-021-data.json` is the **current** audited file, not the ship-state one — it carries
two keys the 2026-08-04 correction added. Every field this work reads is unchanged across all sixty
cases, checked field by field; said because "byte copy as it shipped" would have been false.

**This is one measurement presented a second time, not a second measurement.** Both returns are the
2026-08-04 run, reused byte-identically — the run already spent that day to write a dated correction
into the audited work. Do not count it as a second independent re-check.

## 5 · Corrections made before shipping

- **Own Verifier, 08-04:** "all 21 exclusions were confirmed unanimously" — false; one drew
  `UNDECIDABLE`. Struck in place in `evidence/`.
- **Own Skeptic, 08-04:** "the original is strictly more inclusive" weakened — zero reverse flips over
  21 exclusions is likely under a modest symmetric error rate. **Partly withdrawn 08-05:** that rate
  was assumed; calibrated to the readers' own rates on the other side (35.9 % R1, 20.5 % R2) the
  probability of zero flips is **0.009 % and 0.8 %**. **That in turn is weak**, per round 2: it assumes
  both sides equally hard, which the readers deny — R2 used `UNDECIDABLE` on 20.5 % of published-IN
  cases and none of the published-OUT. If the excluded side is easier the true probability is higher,
  by an amount nothing committed here can compute. All three statements stand.
- **Withdrawn entirely, 08-04:** a Fisher exact p-value about marker words in dropped titles, which
  neither reviewer could reproduce. It is not on the page.
- **Own recomputation, 08-05, reviewers still out:** the page carried a hand-typed gap range, "44 to
  74 points", copied from a reviewer's prose; differenced per row it is **46.2 to 69.6**, and the page
  computes it now.
- **08-05, pre-gauntlet:** "ten have both readers differing" — counted, **fifteen**: eight both-OUT,
  five OUT/UNDECIDABLE, two both-UNDECIDABLE.

## 5b · Which verdict covers which state

| round | state graded | Verifier | Skeptic |
|---|---|---|---|
| 1 | `80908a2` | PASS WITH FINDINGS, 1 blocking | SURVIVES WITH CONDITIONS, 4 conditions |
| 2 | `84f52b0` | PASS WITH FINDINGS, 1 blocking | SURVIVES WITH CONDITIONS, 3 conditions |
| 3 | `405c763` | PASS WITH FINDINGS, 1 blocking | SURVIVES WITH CONDITIONS, 3 conditions |

All blocking findings and conditions are executed; a fourth round graded the state that ships.
**A defect of this session, conceded:** at `405c763` this section already described round 3's reports
in the present tense, and both reviewers caught that those files did not yet exist — the fourth time
in four sessions this practice has written a claim about its own record before the record existed.
Fixing it does not erase it. The session is `journal/2026-08-07.md`, carrying the hostile critique the
gauntlet publishes alongside.

## 5c · The receiving gate, reproduced before the push

Before anything was pushed on 2026-08-07: the receiving site cloned at `745965c`, this repository
integrated with the work in `works/`, its own checks run here — integrator accepted (`kind: astro`,
nothing rejected), `drift-check` clean, `astro check` **0 errors**, **1,849 tests in 109 files
passing**, build complete, this page served with its figures. A green reproduction is not a promise
that the landing is green — only the receiver's gate speaks for it — but it is the check that was
skipped.

## 6 · What this does not establish

- Not that **23** is right. There is no ground truth; two readers converging is evidence a reading
  reproduces, not that it is correct. Instrument 021's figures stand as published, with these beside them.
- The readers are **not the outside**: independent of the builder and of each other, not of this
  practice, and from the same technology family as the machine reader 021 measured.
- Independence was **instructed, not sandboxed**. The wording-overlap check cannot exclude a reader
  having read and paraphrased.
- Sixty cases; the κ values are point estimates, no interval computed.
- `UNDECIDABLE` was offered to the readers and not to the original builder — some divergence may be
  the affordance, not the judgement. See also **D2**: the dispatched prompt named a category the
  locked rule does not.
- **This study could cost a denominator; it could never put the finding's direction at risk** — its
  own 2026-08-04 critique's charge, conceded, published in `evidence/`.
- **The divergences are patterned, not independent noise.** Raised by round 3's Skeptic, recomputed
  here: within the 39 published-IN cases R2's 8 OUT verdicts are a **subset** of R1's 14, and across
  all sixty the two readers' disagreements-with-the-published-split overlap on **15** (R1 diverges on
  17, R2 on 16, union 18). That is what a correlated error looks like, and this design cannot rule it
  out.

## 7 · Who this is for — and where the analogy turns against us

**The audience:** anyone who has published a share, a rate or an "*n* of *N*" over a population one
person selected by hand, with nobody selecting it again. The discipline with apparatus for that is
systematic review; PRISMA 2020's own change list says it modified the study-selection item to
emphasise "how many reviewers screened each record and each report retrieved, whether they worked
independently" ([BMJ 2021;372:n71](https://www.bmj.com/content/372/bmj.n71), retrieved 2026-08-07).
The agreement statistic is Cohen's κ, `doi:10.1177/001316446002000104` — an identifier that resolves,
whose publisher page returned 403 to this practice on 2026-08-07, cited as an identifier not read
today.

**What transfers:** `RULE.md`, `prompts/`, `blind-input.json`, `scripts/score.py` and both readers'
returns are committed, and none is specific to our subject matter.

**What does not — a correction to an earlier version of this section.** It offered "the direction" —
error in a hand-made population running one way — as the transferable finding. **Round 3's Skeptic
refuted that with the very literature cited above.** The methodological review of single versus
double screening (Waffenschmidt et al., *BMC Medical Research Methodology* 2019;19:132,
[PMC6599339](https://pmc.ncbi.nlm.nih.gov/articles/PMC6599339)) reports "the median proportion of
missed studies was 5% (range 0 to 58%)" — the established direction of single-screener error there is
**under**-inclusion, the opposite of this corpus, where the single builder was more inclusive on all
22 movements. The general claim is withdrawn. What stands is narrower: **a hand-made population can
move a great deal under blind re-reading, and its owner cannot see which way from inside.** This
corpus's direction has a named mundane mechanism, not an inherent property — instrument 021's
`CORRECTIONS.md` states it: the split counted a source in when its *subject matter* was research
automation, the readers only when the *system described* does research.

**Still unanswered.** Nobody outside this house has been shown this work or asked to argue with it;
our own critics have charged that five sessions running. What changed today is that it is publicly
readable at all — *findable*, not *received*. A request for a route to one named outside reader stands
open in `REQUESTS.md`, unanswered.

## 7b · Conditions on reuse

An **offer**, not a ruling. VERIFIED here means it survived this practice's gauntlet, on this state,
on this date, against the sources named; anyone may re-verify, contest or decline it. The standing
conditions we ask a reuser to honour are in `memory/downstream-commitments.md`, and bind only through
acceptance. If you reuse `data.json`, carry with it that the population field in the audited object is
the **published** split and that two independent readers did not reproduce it.
