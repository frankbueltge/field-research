# Power audit — can our own kill criterion tell the two answers apart?

**Increment 2 against the gate. Session 111, 2026-08-11, ~22:00–23:50 UTC.**
Method fixed in `PREREGISTRATION-111.md`, committed at `9625a25` before the script that produced
any figure below was written. Every number here comes from `power_audit.py` reading
`ledger/run-2026-08-11T1124Z.json`; both are in this directory and the script prints its own inputs.

---

## 0. The question, and why it had to be tonight

At session 109 this practice made a promise against itself (`CONCEPT.md` §5a), after an adversary
said the fourteenth day of a daily ledger would look exactly like the first:

> *if after **seven consecutive daily runs** (through 2026-08-18) the ledger has recorded **zero**
> state transitions across the whole corpus, the daily-series argument is **dead** … and the arc parks.*

*The parenthetical date was missing from this quotation in the base commit `0be6151`, unmarked. It is
restored here on the adversary's condition 1 — and it is the exact clause whose absence let the
interval miscount of §8a stand: quoting a pre-commitment with its own deadline silently trimmed is
how an arc loses track of what it promised.*

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

*Governing figures are the **seven-interval** ones (§8a: seven runs through 2026-08-18, the date
§5a's own text names). The six-interval column is kept because it is what the base commit computed
and because deleting a superseded number is not how this practice corrects one.*

| | intervals | expected transitions | P(zero) |
|---|---|---|---|
| **Fitted hazard (k = 0.696) — GOVERNING** | **7** | **1.527** | **0.217** |
| Fitted hazard, six-interval reading (base commit) | 6 | 1.309 | 0.270 |
| Naive constant hazard, seven intervals | 7 | 1.866 | 0.155 |
| Naive constant hazard, six intervals | 6 | 1.599 | 0.202 |

**§5a fires by chance better than one time in five, even if the disappearance rate implied by our own
corpus is exactly right.**

And the sharper form. If §5a fires, what is the evidence actually worth? Zero transitions has
probability **0.217** in the world where our implied rate is real and probability **1.000** in the
world where nothing ever disappears. That is a likelihood ratio of about **4.6 : 1** (3.7 : 1 on the
six-interval reading).

> **We promised to treat a result worth under 5 : 1 as decisive.** That is the finding of this audit,
> and it is about our own instrument, not about the platform.

**One thing that sentence is doing must be named, on the adversary's condition 3.** §5a does not use
probabilistic language. It says *"dead"*, unconditionally. **The likelihood ratio is this audit's own
interpretive gloss** — our choice of instrument for asking what a null result would be worth — laid
over a promise that was written without any such instrument in mind. A reader is entitled to reject
the gloss and keep the promise; what they cannot do, having read §3, is keep the promise *and* believe
that its firing would settle anything. Whether a likelihood ratio is even the right scoring instrument
here is an open question this practice has recorded rather than answered
(`memory/open-questions.md`, session 111).

For scale: the pair of runs session 110 already made — 7.3 hours apart — had an expected transition
count of **0.066**. Observing zero there carried a likelihood ratio of about **1.07 : 1**. Session 110
wrote of that result, verbatim: *"The first evidence this arc has produced on that question **supports
the critic, not us.**"* (`INCREMENT-1.md`). On this arithmetic it was **very close to no evidence at
all in either direction.** We did not know that when we published it. It stands as published; this is
the correction to what it was worth, dated today.

*(An earlier draft of this paragraph put a paraphrase inside quotation marks and attributed it to
session 110. It was caught here and replaced with the verbatim sentence before landing. This arc's
signature error is quoting a source for something it does not quite say, and it very nearly happened
in the document auditing that habit.)*

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

## 4a. Not all identifiers are worth the same, and it is the young ones that pay

`k < 1` has a design consequence the arc had not drawn. Because the implied hazard falls with age,
an identifier's contribution to the expected transition count depends on how old it is. Per
identifier per day, under the fitted curve (`power-audit-age-enrichment.json`):

| age band | live n | mean daily hazard | relative to the corpus mean |
|---|---|---|---|
| 0–1 y | 323 | 1.478 × 10⁻⁴ | **1.57×** |
| 1–2 y | 503 | 1.034 × 10⁻⁴ | 1.10× |
| 2–3 y | 512 | 8.793 × 10⁻⁵ | 0.94× |
| 3–5 y | 733 | 7.700 × 10⁻⁵ | 0.82× |
| 5 y + | 249 | 6.809 × 10⁻⁵ | 0.72× |

One identifier added at age three months is worth **1.88×** an average current one; at seven years,
**0.68×**. **A request spent on a recent video buys about 2.8 times the expected transition of a
request spent on a seven-year-old one.** The intuition that a link-rot study should chase old
material is exactly backwards for a *forward* series: old material has already done its dying.

Two limits on that recommendation, both real. It is derived from the fitted curve, which is the thing
under question. And it is **not** an argument that the corpus should be *replaced* by young
identifiers — the old cohorts are what make the age structure estimable at all, and a corpus tuned
only for transition-yield stops being able to check its own hazard model.

## 5. The confounds, and which way each of them cuts

Every one of these was named in `PREREGISTRATION-111.md` §4 before the numbers existed.

- **Cross-sectional is not longitudinal.** These are nine cohorts measured once, not one cohort
  followed. Reading them as a survival curve assumes a 2019 video faced the same hazard schedule as a
  2024 one. The 2023 anomaly and the three-of-ten editions running the other way (session 109) are
  evidence against that assumption. **This is the largest weakness of the estimate and it does not
  have a stated direction.**
- **Frailty. ~~Makes E an overestimate.~~ WITHDRAWN — see §8c.** This section originally argued that
  survivors are enriched for durable videos, so the forward hazard is lower than the fitted one, so E
  is an overestimate — and said explicitly that the direction flattered our own conclusion. **A
  specialist review fitted two literal frailty models to the same data and the sign does not hold**:
  a gamma-frailty model gives E = 1.304 (below), a two-point mixture gives E = 1.321 (above), and
  the two fit **equally well** (AIC 1802.65 against 1802.55). The reasoning was plausible and it was
  not checked. **The claim is withdrawn; frailty's direction here is undetermined.** The magnitude is
  small enough that the headline is untouched, which is not a defence of having asserted it.
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
| **P3** | expected transitions below 3 | **HOLDS** — **1.527** on the governing seven-interval reading (1.309 on six) |
| **P4** | P(zero) above 0.20 | **HOLDS, and narrowly** — **0.217** on the governing reading (0.270 on six). At eight intervals it would fail. The prediction survives on the reading this practice adopted *against* itself, which is worth stating rather than banking |
| **P5** | fitted E below naive E | **HOLDS** — 1.527 against 1.866 on seven intervals (1.309 against 1.599 on six); the naive figure flatters the design by 22 % either way |
| **P6** | arm A shows a *shallower* age gradient than arm B | **FAILS** — A's cumulative-failure gradient F(5)/F(1) = **3.10**, B's = **1.96**. A is the steeper. Registered as expected to fail (session 110's point estimates already ran this way) and it did. What the arms actually differ in is **shape**, not depth: B loses more when young (F(1) = 0.095 against A's 0.053) and then flattens hard (k = 0.451 against A's 0.742). With 66 deaths in arm B and a CI on k of [0.160, 0.891], **this comparison is too weak to carry an interpretation** and none is offered. |
| **P7** | ≥ 500 new determinate identifiers baselined before 00:00Z | scored in `EXPANSION-111.md` |

**Six scored, five hold, one fails.**

## 8. Kill criteria

| | fires? | value |
|---|---|---|
| **K1** | no | 2,320 retrievable, datable identifiers (threshold 1,500) |
| **K2** | no | 7 yearly cohorts with n ≥ 100 (threshold 6): 2020–2026 |
| **K3** | no | CI on k is [0.502, 0.898] — it excludes 1 and is not wider than [0.5, 2.0]; the shape **is** determined and the figures may be published as points |
| **K4** | no | E = **1.53** (seven intervals; 1.31 on six), threshold 10. **K4 was not a live test, and the adversary is right that it was not** (condition 4): the same pre-registration predicted λ ∈ [0.01, 0.10]/yr in P2, and **no λ in that band can produce E > 10 on this corpus** — the top of the band gives roughly 4. K4 was written to pass, which is exactly the defect session 108 taught this practice to look for, committed in the same document that applies that lesson to §5a. **Recorded as a defective criterion, not as a passed one.** |
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

**STANDING INSTRUCTION, adopted on the adversary's condition 5 and binding on later sessions:** this
bound stays **unquantified** until longitudinal data exists. A cross-sectional snapshot cannot supply
a return rate, and no later session may round this into a number without new repeated observation.

**Two known biases run in opposite directions and are not netted out:** omitted returns make `E` an
underestimate (here); frailty was claimed in §5 to make it an overestimate, **and that claimed
direction did not survive review** (§8c). Neither is measured. The headline
survives both only because the gap it has to cross is large — a criterion promised as decisive
delivering odds under 5 : 1 — and not because the arithmetic is tight. That is stated rather than
left for a reader to work out.

## 8c. The specialist's findings — including the one that breaks a claim of ours

*A domain specialist in survival analysis and study design was convened because this session applied
methods it does not independently hold, and the resulting numbers govern whether an arc continues.
The specialist holds no vote on any verdict. Full report and scripts:
`SPECIALIST-survival-111.md`, `specialist-survival-scripts/`.*

**It reproduced the pipeline from the raw ledger file rather than from our output**, and found no
coding or arithmetic error anywhere in `power_audit.py`: k = 0.6959, λ = 0.01787, E = 1.309,
P(zero) = 0.270 and the 5,310-identifier / 14-day target all reproduce.

**Three findings, and the first one is against us.**

**1. Our K3 "the shape *is* determined" does not survive a defensible respecification.** Refitting on
**recent cohorts only (2023–2026)** — the cohorts *least* exposed to the pruning and
citation-selection confounds §5 itself names — gives **k = 0.859, CI [0.553, 1.193], which
includes 1.**

> Under this audit's own K3 — *"the 95 % CI on k includes 1 → shape undetermined, every power figure
> published as a range, never a point"* — **that specification would have fired K3.**

**We reproduced this ourselves before letting the record lean on it** (`specialist-reproduced-111.txt`,
our own fitter, our own hand): k = **0.8597**, CI **[0.5543, 1.1924]** — matching the specialist to
three decimals. And the reproduction went one step further than the report did:

| fit | n | k | 95 % CI | CI includes 1? |
|---|---|---|---|---|
| pooled 2018–2026 | 2,618 | 0.6959 | [0.5017, 0.8983] | **no** |
| recent 2023–2026 | 1,796 | 0.8597 | [0.5543, 1.1924] | **yes** |
| old 2018–2022 | 822 | 0.8033 | [0.1661, 1.7559] | **yes** |

**Neither half of the corpus determines the shape. Only the pooled fit does.** A parameter that is
significant in the whole and in neither part is a parameter carried by the *contrast between* the
parts — which is precisely the cross-sectional cohort comparison whose identifying assumption §5 says
is this estimate's largest weakness. **The claim that the shape is determined is narrowed to:
determined on the pooled fit, and on nothing else.** The power conclusion is robust to it (E moves
1.31 → 1.22, both far inside underpowered territory); **K3's verdict is not**, and that matters
because K3 was one of this session's own guards.

**2. The frailty direction we asserted in §5 is withdrawn** — see §5. Two literal frailty models fit
equally well and disagree on the sign.

**3. The young-enrichment lever is real and now quantified.** §4a argued from the fitted curve that
recent identifiers pay more. The specialist put a number on it: closing the gap to P(zero) ≤ 0.05
needs about **1,748 new identifiers at ~90 days old against ~2,990 at the corpus's current age mix**
— roughly **40 % fewer requests for the same power.**

**Net direction of every correction the specialist could quantify:** P(zero) moves **up**, from 0.270
toward **0.277–0.280** — the design is if anything slightly weaker than we reported, never stronger.

**What we do not do with this.** Finding 1 is an argument that this audit's own guard was run too
narrowly, not an argument that the audit's conclusion is wrong; and it is emphatically not a reason to
re-open §5a's amendment in our own favour. It is recorded as a defect in our robustness practice:
**a kill criterion applied against a single specification is a criterion tested against itself.** That
is the same lesson as §5a, one level up, found by someone else, in the same session.

## 9. What this document does not claim

It is **not** evidence about whether videos disappear. It is evidence about whether this instrument
could see it if they did. Nothing here is a packet, no `status` is claimed, nothing is addressed to
anyone, and no party named in this record has been or will be contacted by this practice. No gauntlet
verdict is claimed; any verdict obtained is good only for the exact state it was run on.
