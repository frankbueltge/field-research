# Power audit — can our own kill criterion tell the two answers apart?

**Increment 2 against the gate. Session 111, 2026-08-11, ~22:00–23:50 UTC.**
Method fixed in `PREREGISTRATION-111.md`, committed at `9625a25` before the script that produced
any figure below was written. Every number here comes from `power_audit.py` reading
`ledger/run-2026-08-11T1124Z.json`; both are in this directory and the script prints its own inputs.

---

## 0. The question, and why it had to be tonight

At session 109 this practice made a promise against itself (`CONCEPT.md` §5a), after an adversary
said the fourteenth day of a daily ledger would look exactly like the first:

> *if after **seven consecutive daily runs** the ledger has recorded **zero** state transitions across
> the whole corpus, the daily-series argument is **dead** … and the arc parks.*

Session 110 then ran the instrument twice in one day and found zero transitions across 2,147 jointly
determinate identifiers, and published that the result argued against the arc.

**The question this session asks is the one that should have come before the promise:** given how
rarely these videos actually disappear, and how many of them we are watching, *would seven days
produce a transition even if videos were disappearing at a perfectly ordinary rate?* If the answer is
no, then zero transitions is the predicted outcome in **both** worlds, §5a cannot distinguish between
them, and keeping the promise would end this arc on arithmetic rather than on evidence.

That is exactly the failure this practice bound itself against at session 108 — *write kill criteria
that can distinguish, not criteria that can only kill.* Session 109 applied that check to five new
criteria and did not apply it to §5a.

**Tonight or not at all.** Day 2 is 2026-08-12. Days cannot be added to a window retroactively.
Identifiers can be added before it opens.

## 1. Population, and what was thrown away

| | n |
|---|---|
| Observations in the run file | 2,904 |
| Excluded — arm B-truncated (the harvest artefact, not videos) | 249 |
| Excluded — `INDETERMINATE` | 33 |
| Excluded — not a 19-digit identifier (the dating rule does not hold; session 110) | 4 |
| **Analysed** | **2,618** |
| of which currently retrievable | **2,320** (88.62 %) |

Mean age at the reference instant (2026-08-11T12:00:00Z, the midpoint of run 2): **2.880 years**.

## 2. What the corpus already says about disappearance

Cross-sectional survival by creation year, pooled over both arms. Wilson 95 % intervals.

| cohort | n | retrievable | fraction | 95 % CI | mean age | fitted |
|---|---|---|---|---|---|---|
| 2018 | 2 | 2 | 1.0000 | [0.342, 1.000] | 8.15 y | 0.770 |
| 2019 | 29 | 21 | 0.7241 | [0.543, 0.853] | 7.01 y | 0.790 |
| 2020 | 130 | 106 | 0.8154 | [0.740, 0.873] | 6.02 y | 0.809 |
| 2021 | 249 | 212 | 0.8514 | [0.802, 0.890] | 5.08 y | 0.828 |
| 2022 | 412 | 353 | 0.8568 | [0.820, 0.887] | 4.10 y | 0.850 |
| 2023 | 574 | 487 | 0.8484 | [0.817, 0.875] | 3.11 y | 0.875 |
| 2024 | 548 | 500 | 0.9124 | [0.886, 0.933] | 2.11 y | 0.903 |
| 2025 | 510 | 480 | 0.9412 | [0.917, 0.959] | 1.15 y | 0.935 |
| 2026 | 164 | 159 | 0.9695 | [0.931, 0.987] | 0.34 y | 0.972 |

**2023 is the non-monotone year session 109 already flagged**, and it is the one cohort the fit misses
badly (observed 0.848 against fitted 0.875). It is reported here rather than smoothed.

**Weibull maximum likelihood on the individual outcomes**, `S(t) = exp(-(λt)^k)`:

- **shape k = 0.6959**, 95 % profile-likelihood CI **[0.5017, 0.8983]** — **the interval excludes 1.**
- scale λ = 0.01787 / year; implied median life 33.0 years.
- The naive constant-hazard figure, for comparison and labelled naive: **λ̂ = 0.0420 / year**.

`k < 1` means the implied hazard **falls with age**: 0.0423/yr at age 1 against 0.0259/yr at age 5, a
ratio of 0.61. **This is not evidence that any individual video gets safer as it ages** — a mixture of
durable and fragile videos produces exactly this shape even when every single one has a constant
hazard (`PREREGISTRATION-111.md` §4, frailty). Either way it is the number the design has to survive.

## 3. The answer

Over the pre-registered window — **seven daily runs bind six one-day intervals** — on the **2,320**
identifiers currently retrievable:

| | expected transitions | P(zero) |
|---|---|---|
| **Fitted hazard (k = 0.696)** | **1.309** | **0.270** |
| Naive constant hazard | 1.599 | 0.202 |

**§5a fires by chance roughly one time in four, even if the disappearance rate implied by our own
corpus is exactly right.**

And the sharper form. If §5a fires, what is the evidence actually worth? Zero transitions has
probability **0.270** in the world where our implied rate is real and probability **1.000** in the
world where nothing ever disappears. That is a likelihood ratio of about **3.7 : 1**.

> **We promised to treat a 4-to-1 result as decisive.** That is the finding of this audit, and it is
> about our own instrument, not about the platform.

For scale: the pair of runs session 110 already made — 7.3 hours apart — had an expected transition
count of **0.066**. Observing zero there carried a likelihood ratio of about **1.07 : 1**. The result
session 110 published as *"the first evidence, and it supports the critic"* was, on this arithmetic,
**very close to no evidence at all in either direction.** We did not know that when we published it.
It stands as published; this is the correction to what it was worth, dated today.

## 4. What it would take

| assumed shape | λ / yr | E | P(zero) | live corpus for P(zero) ≤ 0.05 | or days at the present corpus |
|---|---|---|---|---|---|
| k = 0.50 | 0.00567 | 1.066 | 0.344 | 6,519 | 17 |
| k = 0.75 | 0.02202 | 1.369 | 0.254 | 5,076 | 13 |
| k = 1.00 (constant) | 0.04256 | 1.622 | 0.198 | 4,285 | 11 |
| **k = 0.696 (fitted)** | **0.01787** | **1.309** | **0.270** | **5,310** | **14** |

Two levers, and they are not equally available. **Days are closed** — the window is pre-registered
and lengthening it moves a promise in the direction that delays its own firing, which §0 of this
session's pre-registration forbids without a dated amendment. **Identifiers are open until 00:00Z.**
Roughly **2.3×** the present live corpus is what turns §5a from a 4-to-1 result into a 20-to-1 one.

## 5. The confounds, and which way each of them cuts

Every one of these was named in `PREREGISTRATION-111.md` §4 before the numbers existed.

- **Cross-sectional is not longitudinal.** These are nine cohorts measured once, not one cohort
  followed. Reading them as a survival curve assumes a 2019 video faced the same hazard schedule as a
  2024 one. The 2023 anomaly and the three-of-ten editions running the other way (session 109) are
  evidence against that assumption. **This is the largest weakness of the estimate and it does not
  have a stated direction.**
- **Frailty makes E an overestimate.** If the corpus is a mixture of durable and fragile videos, the
  survivors are enriched for durable ones, and the *forward* hazard of the 2,320 that are alive today
  is **lower** than the cross-sectional average this fit recovers. That pushes E below 1.31 and
  P(zero) above 0.27 — **the direction that makes this audit's conclusion stronger, which is exactly
  why it is stated here rather than left out.**
- **Arm A is pruned.** Editors and bots remove dead links from articles, deleting dead videos from
  the corpus preferentially in older articles, making arm A's old cohorts look better than the truth.
  That biases λ **downward** and E with it. §6 below is the beginning of a control for this.
- **Left truncation.** A video deleted before anyone cited it never enters the corpus.
- The instrument measures **public retrievability through one credential-free route**, from one
  logged network vantage (AS396982, US). Never deletion, moderation, geo-restriction or intent.

## 6. The repair, and it is a control as well as a volume

Rather than adding identifiers wherever they were cheapest, the expansion attempted tonight is
**arm A2: the same wikis, outside article space** — talk pages, user pages, project pages, drafts,
templates, categories. Same operator, same editors, same subject matter, and **no link-maintenance
regime**: nobody fixes a dead link in a 2019 talk-page comment. It is at once the volume the power
calculation asks for and the control the pruning confound has been missing. If arm A2's old cohorts
survive **worse** than arm A's, the pruning bias is measured rather than argued.

Results of the expansion, and the amendment to §5a it does or does not license, are in
`EXPANSION-111.md` beside this file. **No power figure in this document is restated on the strength
of the expansion** — this document is the audit of the corpus as session 110 left it.

## 7. Predictions, scored

| | prediction | outcome |
|---|---|---|
| **P1** | fitted `k` below 1 | **HOLDS** — 0.696, CI [0.502, 0.898], excludes 1 |
| **P2** | naive λ̂ between 0.01 and 0.10 /yr | **HOLDS** — 0.0420 |
| **P3** | expected transitions below 3 | **HOLDS** — 1.309 |
| **P4** | P(zero) above 0.20 | **HOLDS** — 0.270 |
| **P5** | fitted E below naive E | **HOLDS** — 1.309 against 1.599; the naive figure flatters the design by 22 % |
| **P6** | arm A shows a *shallower* age gradient than arm B | **FAILS** — A's cumulative-failure gradient F(5)/F(1) = **3.10**, B's = **1.96**. A is the steeper. Registered as expected to fail (session 110's point estimates already ran this way) and it did. What the arms actually differ in is **shape**, not depth: B loses more when young (F(1) = 0.095 against A's 0.053) and then flattens hard (k = 0.451 against A's 0.742). With 66 deaths in arm B and a CI on k of [0.160, 0.891], **this comparison is too weak to carry an interpretation** and none is offered. |
| **P7** | ≥ 500 new determinate identifiers baselined before 00:00Z | scored in `EXPANSION-111.md` |

**Six scored, five hold, one fails.**

## 8. Kill criteria

| | fires? | value |
|---|---|---|
| **K1** | no | 2,320 retrievable, datable identifiers (threshold 1,500) |
| **K2** | no | 7 yearly cohorts with n ≥ 100 (threshold 6): 2020–2026 |
| **K3** | no | CI on k is [0.502, 0.898] — it excludes 1 and is not wider than [0.5, 2.0]; the shape **is** determined and the figures may be published as points |
| **K4** | no | E = 1.31, threshold 10. **This session's premise is not wrong** — had E exceeded 10 the audit would have said so in those words |
| **K5** | scored in `EXPANSION-111.md` | |

## 8a. Addendum, found after §§1–8 were written and committed

*Added at ~22:14Z, after the main text was committed at `0be6151`. The git history carries the
ordering; this is not presented as something the audit knew from the start. (A first version of this
sentence carried a commit hash that was not the audit's; it was corrected before landing, and the
correction is noted rather than made quietly — the rule that governs a wrong figure governs a wrong
hash.)*

Applying this arc's second standing check — *read to the end of the page you are about to quote* — to
`CONCEPT.md` §5a itself turned up a discrepancy **inside the pre-commitment**. Its text says *"seven
consecutive daily runs **(through 2026-08-18)**"*. Session 110's minutes say *"Day 2 is 2026-08-12"*,
which makes day 1 the 11th and seven runs end on **2026-08-17**. The two readings differ by one run,
and therefore by one observable interval.

Both are computed rather than one chosen:

| reading | intervals | E | P(zero) | likelihood ratio | live corpus for P(zero) ≤ 0.05 |
|---|---|---|---|---|---|
| seven runs 08-11 … 08-17 (session 110's day numbering) | 6 | 1.309 | 0.270 | **3.70 : 1** | 5,310 (2.29×) |
| seven runs 08-12 … 08-18 after the 08-11 baseline (§5a's own parenthetical) | 7 | 1.527 | 0.217 | **4.61 : 1** | 4,551 (1.96×) |

**The discrepancy does not rescue the criterion.** On either reading §5a fires by chance better than
one time in five and delivers evidence at odds under 5 : 1.

**The rule this practice adopts for it, stated now rather than on 2026-08-18:** the **longer** window
governs — seven runs through 2026-08-18, seven intervals — because it is the text of the
pre-commitment itself *and* because it is the reading **least favourable to this session's own
conclusion**. Where §§1–8 above quote the six-interval figures they are left standing as computed;
the governing numbers for the arc are the seven-interval row. Figures in
`power-audit-addendum-window.json`.

## 8b. Second addendum — a scope error in this audit's own arithmetic, found by us at ~22:20Z

**§5a counts *state transitions*, in either direction. This audit modelled only one direction.**

Every figure in §§1–8 is built from a survival hazard: the rate at which a retrievable video stops
being retrievable. But an identifier that reads NOT-RETRIEVABLE today and RETRIEVABLE next Tuesday is
also a state transition under §5a's own wording, and there are **298** such identifiers in the
corpus. This audit's `E` therefore counts **disappearances only** and omits returns.

**Direction of the error: against this session's conclusion.** `E = 1.53` is a **lower** bound on
expected transitions and `P(zero) = 0.217` is an **upper** bound on the false-kill rate. The true
criterion is somewhat better powered than §§1–8 say.

**It cannot be quantified from anything this practice holds.** A cross-sectional snapshot contains no
information about a return rate; only repeated observation does. What we have is that the two runs of
2026-08-11, 7.3 hours apart, produced **zero** transitions in **either** direction across 2,147
jointly determinate identifiers — which bounds the combined per-observation rate loosely and
estimates neither component. **Recorded as an unquantified bound, not folded into a number.**

**Two known biases now run in opposite directions and are not netted out:** frailty makes `E` an
overestimate (§5), omitted returns make it an underestimate (here). Neither is measured. The headline
survives both only because the gap it has to cross is large — a criterion promised as decisive
delivering odds under 5 : 1 — and not because the arithmetic is tight. That is stated rather than
left for a reader to work out.

## 9. What this document does not claim

It is **not** evidence about whether videos disappear. It is evidence about whether this instrument
could see it if they did. Nothing here is a packet, no `status` is claimed, nothing is addressed to
anyone, and no party named in this record has been or will be contacted by this practice. No gauntlet
verdict is claimed; any verdict obtained is good only for the exact state it was run on.
