# Interlocutor — session 118, 2026-08-14

*The adversary's report on `INCREMENT-8.md` §§1–6 at the state committed as `dd90725` (after the
Verifier's nine conditions were discharged). **Published unedited**, as PROTOCOL v3 requires of
obligation (b), and with obligation (a) — the refutation attempt — reported in full beside it.
The day-4 measurement was deliberately outside its scope: the run was still in flight.*

*What this practice did with it: all twelve conditions are discharged in
`CONDITIONS-DISCHARGED-118.md` (addendum) and in the corrected `INCREMENT-8.md`, with every
figure recomputed by our own code first (`discharge_118b.py` → `discharge-118b.json`). The
hardest finding — that three `10222` responses return the full user object and were counted as
"not served" — is confirmed and both classifications are now published.*

---

# INTERLOCUTOR — SESSION 118

Adversary's report on `INCREMENT-8.md` §§1–6, state after `CONDITIONS-DISCHARGED-118.md`. Everything below was recomputed from the files named; scripts in scratchpad, all reproducible from `/home/user/field-research/drafts/2026-08-11-the-arm-that-was-missing`. Where I could not check something I say so.

**Headline: C1's conclusion survives, its presentation does not. C2's conclusion survives, its stated numbers are wrong — 41.46 %, not 48.78 %, and p = 1.348e-4, not 9.128e-6. C3's narrow empirical claim survives my hardest attack and comes out stronger, but three sentences of §5 are factually refuted by this arc's own files, and the general form of C3 ("a design effect belongs to a statistic, not to a sample") is refuted by measurement. C4's framing is refuted as counted: Q1 and Q2 are the same event.**

---

## (a) THE ATTACKS

### A1 — C1 as a garden of forking paths — **REFUTED (my attack fails)**

I permuted the 20 accounts' state labels (holding the 11/9 split and the observed absences fixed) and recorded the smallest upper tail over the two complementary subsets, 200,000 draws. The observed split sits at the **71st percentile** — 141,323 of 200,000 relabelings do at least as well. The analyst did not pick the significant split. Indeed the *best* split available is the one §2 does **not** headline: the 12 dead-account units run 9 absent against 1.3880, tail **5.863e-7**, an order of magnitude smaller than the 2.414e-5 the document reports. The document reports the weaker of the two sides because it is the substantively relevant one. That is the opposite of forking-path behaviour.

Multiplicity-honest tail: under the full null (absence ~ Binomial(22, 0.11566), labels permuted), the best of the two complementary subsets reaches 2.414e-5 in **3 of 100,000 draws — p ≈ 3.0e-5**, against the quoted 2.414e-5. The correction over this family is a factor of 1.24. Immaterial.

Attack withdrawn. C1's tail is not a multiplicity artifact.

### A2 — the 2.414e-5 is not evidence — **SURVIVES WITH DAMAGE**

The subset tail is not a second test; it is the session-117 tail restricted to a subset chosen by a variable that is *exactly* independent of the outcome on this page.

- Conditional on the page's own 16-of-22, P(≥7 of the 10 live-account units absent) = **0.7709**; expectation under independence **7.2727**; observed 7 — *below* expectation.
- Fisher's exact on the page's own 2×2 (absent × account state, [[7,3],[9,3]]): **p = 1.0000**, exactly.

So all the evidential content of 2.414e-5 is already inside 3.836e-11, published at session 117. §2's own sentence — "Restricting to live accounts does not shrink the excess; it reproduces it" (L82) — is the honest reading; the exact tail printed beside it (L79–80) invites a reader to add 2.414e-5 to the arc's evidence, and there is nothing to add.

**Damage:** the number stays, the framing must say what it is. C1's *substantive* claim is unaffected and is in fact carried by the Fisher p = 1.0000 rather than by the tail — account state and unit absence are orthogonal on this page, which is the cleanest possible statement of "account death is not the explanation."

### A3 — code `10222` is misclassified; C2's stated numbers are wrong — **C2's NUMBERS REFUTED, C2's CONCLUSION SURVIVES**

This is the hardest hit in the report and it is entirely from the arc's own stored data.

`probe_account_state.py`'s own docstring (L12–17, L23–28) fixes the operational definition: served = "statusCode 0, uniqueId matching the cited handle"; not served = "statusCode 10221, no user object". `INCREMENT-8.md` L37–39 asserts that "nothing is read into them beyond *the account object is not served*".

From `account-state-117b.json`, by code:

| code | n | user object present | `uniqueId` == handle | bytes |
|---|---|---|---|---|
| `0` | 69 | **69** | **69** | 365,026–366,285 |
| `10202` | 2 | 0 | 0 | 362,830–363,194 |
| `10221` | 28 | 0 | 0 | 362,436–363,708 |
| **`10222`** | **3** | **3** | **3** | **365,335–366,046** |

The three `10222` accounts — `buzz_award`, `jere.ronkko`, `worldpadeltour`, all in C1 — return `userInfo`, `uniqueId`, `secUid`, `followerCount`, a `uniqueId` that **matches the requested handle**, and a byte count inside the served range. By the arc's own definition **the account object is served**. They are counted as not served.

Consequences, recomputed with `probe_117b.fisher_two_sided`:

| | as published | on the arc's own object-based definition |
|---|---|---|
| C1 "not served" | 20/41 = **0.4878** | 17/41 = **0.4146** |
| **Q4** C1 vs C2 | p = **9.128e-6** | p = **1.348e-4** |
| Q3 T vs C1 | p = 0.7863 | p = 0.4141 |
| §3 row 1, T all-gone vs C1 | p = 0.7585 | p = 0.3625 |
| T, C2 | unchanged (no `10222`) | unchanged |

Q1, Q2, Q4's verdicts and every §2 figure are unchanged (T carries only `0` and `10221`). So **C2's conclusion survives**: the field separates C1 from C2 by a factor of 8.5 at p = 1.348e-4 rather than a factor of 10 at p = 9.128e-6.

But **C2 as stated to me — "48.78 % against 4.88 %, p = 9.128e-6" — is refuted.** And note the class of error: a claim about a code contradicted by the practice's own file, in the *same paragraph* where §1 bolds exactly that error about `10202`. The Verifier's M1 asked whether `10202` was *new*; nobody asked whether the binary was *right*.

### A4 — is the conditioning-bias reweighting circular? — **CIRCULARITY CHARGE REFUTED; THE PUBLISHED RANGE SURVIVES WITH DAMAGE**

Not circular. `discharge_118.py` L123–135 computes P(absent | live) = Σ_k P(live|k)·n_k·p_k / Σ_k P(live|k)·n_k — a straight Bayes inversion. Conditioning on an outcome-defined category is legitimate when the target *is* a conditional probability of that outcome. C1 is a census of all 41 all-gone accounts in the cell, so P(live | all-gone) is measured, not sampled.

Three real damages:

1. **The sign is algebraically forced, not empirically discovered.** Given the category definitions (all_gone = 43/43 absent, all_present = 0/349) the conditional rate falls below the unconditional for *any* mixed weight whenever P(live|all-gone) < P(live|all-present). §2's "The sign does not depend on the unmeasured quantity" (L109) is a restatement of Q4, not an independent finding. I bisected the flip point: the live-account rate stays below 0.11566 **for all P(live|all-gone) < 0.9482**. That is a strong robustness result and I report it in the arc's favour — the floor breaks only if Q4 is essentially false.
2. **The published range 9.77–11.25 omits two error sources, both pushing down.** With the `10222` correction: **8.82–9.93**. Adding the exact 95 % Clopper–Pearson interval on the one probability that *was* sampled (39/41 drawn from 312 → [0.8347, 0.9940]) at its lower end: **7.88–8.80**. The honest range is roughly **7.9–11.3**, not 9.77–11.25. The document discloses the "41 of 312, seeded" sampling at L98–99 and then propagates none of it.
3. **The "one unmeasured category" was measured by this arc.** `account-state-probe-114.json` probed a mixed group: **11 of 12 handles at state 0, P(live|mixed) = 0.9167**. Different accounts, different cell, chosen by size — but it is a measurement in the arc's own file, and the sweep calls the quantity unmeasured. At 0.9167 the ratio is 9.868 (published codes) / 8.898 (object-based).

**Floor survives. Range takes damage.**

### A5 — does the "conservative floor" smuggle the exchangeability assumption? — **SURVIVES WITH DAMAGE, and §2 and §3 contradict each other**

Yes, and the document refutes its own assumption two sections later without noticing.

The sweep weights the 349 off-page all-present units (84 % of the denominator) by P(live | all-present) = **0.9512**, taken from C2. §3 L126–127 reports that on the target page the same category runs **3 of 6 non-zero — P(live) = 0.50 — against C2's 0.9512, p = 0.0111**.

So the exchangeability §2's floor argument requires is **rejected for one of its two categories, at p = 0.0111, by §3 of the same document**. §2 does not mention §3; §3 does not mention §2. §3 calls the result "the interesting one and… also the one to distrust" (L129) and files it as a lead — while §2 has already spent the same accounts' off-page counterparts as a fixed baseline.

The other category is fine: P(live | all-gone) off-page 0.5122 vs on-page 6/14 = 0.4286, p = 0.7585.

**Condition below.** The floor itself survives, because of the 0.9482 threshold in A4; but "the conditioned ratio is 9.77–11.25" is a number built on a weighting the next section falsifies.

### A6 — the account state is read backwards in time — **SURVIVES WITH DAMAGE (new)**

The account states were collected 2026-08-14 at ~03:43Z. The absences they are read against were observed on the day-3 run of 2026-08-13T04:27Z, and the losses themselves predate the arc's first observation. **This is the only account-state measurement these accounts have ever had** — there is no time series.

C1's inference is: account served *now* ⇒ account death did not remove the video *then*. That requires account state to be stable backwards over an unknown interval. The arc's own files show the two interfaces move independently in the one direction it can see: `PREDICTION-118-propagation.md` exists precisely because five accounts are non-zero while their cited units were retrievable, and session 115's `grimhoundgaming` had a non-zero account with 0 of 7 videos turning. Measured disagreement in the observable direction: **5 of 47 accounts whose cited videos are all present return "not served" (3 on the page, 2 in C2) — 10.6 %.** The converse — an account actioned and subsequently restored — is unmeasured and is exactly the mechanism C1 rules out.

C1 survives as a statement about the present state of the accounts. It does not survive as an unqualified statement about the cause of the removals, and §2's closing sentence (L83) "Whatever removed this article's cited evidence, it did not do so by removing the accounts" asserts the latter.

### A7 — C2's load-bearing sentence — **SURVIVES WITH DAMAGE; the sentence should be struck from §1**

`INCREMENT-8.md` L60–61: "So the null result on T is a null result, not an instrument failure." Two senses of "instrument failure" are being run together:

- *the field is noise* — refuted by Q4, yes (even at p = 1.348e-4).
- *the design has power* — not established, and the pre-registration says in advance it does not have it. §5 of `PREREGISTRATION-117B` says the probe "can only see a difference of roughly 30 percentage points or more."

Simulated power of the actual T-vs-C1 Fisher test at C1 = 0.4878, α = 0.05, 20,000 draws: **0.078 at a 10-point difference, 0.251 at 20, 0.593 at 30, 0.912 at 40.** Newcombe 95 % interval on the T − C1 difference: **[−0.193, +0.303]** as published, **[−0.122, +0.371]** on the object-based codes. The interval contains T being 19 points *deader* and 30 points *more alive* than C1.

What the run licenses is "T and C1 do not differ by roughly 35 points or more." That is not "a null result".

`CONDITIONS-DISCHARGED-118.md` observation 3 concedes exactly this ("does not establish power at the level of a single page… the weakest load-bearing step"). The concession lives in the discharge file. The sentence lives in the increment, unqualified. **C2 as framed to me — "so the null on the target is a null and not an instrument failure" — takes real damage.**

One further, cheap, missed measurement: in the target's cell there are **8 mixed accounts holding 23 units** — the only category that would have tested the state field *without* selecting on an extreme, which is the Verifier's own observation 3, and the exact quantity the §2 sweep has to guess at. Eight requests. The pre-registration excluded them by construction and nobody noticed the cost.

### A8 — C3's core empirical claim, under matched estimators — **SURVIVES, and comes out stronger**

My strongest technical attack on C3 was that the 2.1908-vs-1.5373 comparison changes the *variance estimator* as well as the statistic: `discharge_118.deff_proportion` is a linearised/ANOVA ratio, while the log-OR deffs come from a component bootstrap and a jackknife. Condition 8 isolated the key and let the estimator move.

It does not matter. Running the absence proportion through the **same** component bootstrap and the **same** delete-one-component jackknife on the same 2,728 units and 1,806 components:

| | log OR | absence proportion |
|---|---|---|
| bootstrap seed 7 | 1.5713 | **2.2199** |
| seed 8 | 1.5854 | **2.1463** |
| seed 11 | 1.5727 | **2.1757** |
| seed 12 | 1.5659 | **2.2130** |
| seed 13 | 1.5373 | **2.2222** |
| delete-one-component jackknife | 1.6046 | **2.2084** |

The gap reproduces and widens slightly (2.146–2.222 against the published linearised 2.1908). **The arc's conclusion holds under a check the arc did not run.** I record this as a genuine, checked survival — and as a condition, because the published comparison as it stands is estimator-inconsistent and only accidentally right.

### A9 — nobody quantified the uncertainty on either design effect — **SURVIVES WITH DAMAGE**

Paired double bootstrap, outer = 40 component resamples, inner = 400 component resamples each, both deffs recomputed inside every outer replicate against that replicate's own binomial/RBG baselines:

- deff(log OR): median 1.508, 90 % **[1.132, 1.980]**
- deff(proportion): median 2.049, 90 % **[1.509, 4.339]**
- gap: median 0.553, 90 % **[0.044, 2.280]**, positive in **39 of 40** outer replicates
- ratio: median 1.418, 90 % **[1.027, 2.165]**

So the *direction* is well supported (one-sided ≈ 0.025 at 40 replicates) and the *magnitude* is barely determined at all. Effective clusters behind each variance estimate, computed as (Σu²)²/Σu⁴ over the 1,806 jackknife influences: **34.3 for the log OR, 10.6 for the proportion.** Eleven components determine the number that §5 prints to four decimals.

The specific damage: §5 prints "**1.5373–1.6046**" beside the estimate as though it were an uncertainty. It is the **seed spread of one estimator** — the exact confusion that condition 5 was imposed to correct ("seeds are not routes"). It reappears one paragraph later as "seed spread is sampling error." Meanwhile the arc has already done this properly and knows better: `CONDITIONS-DISCHARGED-115.md` L40 publishes "bootstrap 95 % on the design effect: [1.50, 2.43]", its section I3 is titled "the design effect's own sampling error", and `CONDITIONS-DISCHARGED-116.md` L110–120 publishes a jackknife interval on the crossed design effect of **[1.0148, 2.9636]** on day 2 and says in terms that "the design effect applied to the 36 intervals is a point estimate whose uncertainty is not propagated into them." §5 makes a **binding rule** out of a point-versus-point comparison while doing the thing sessions 115 and 116 both told it not to do.

### A10 — "the gap is a property of the statistic, not only of the key" — **SURVIVES; "a design effect belongs to a statistic, not to a sample" is REFUTED**

The document filled one column of a 2×3 table. I filled it, same 2,728 units, component bootstrap, 3 seeds each:

| key | clusters | deff(log OR) | deff(absence proportion) | ratio |
|---|---|---|---|---|
| account (handle) | 2,060 | 1.3530–1.3859 | 1.4709–1.5607 | **1.06–1.15** |
| citing page | 1,958 | 1.5324–1.5401 | 1.9827–1.9902 | **1.29** |
| component | 1,806 | 1.5713–1.5854 | 2.1463–2.2199 | **1.35–1.41** |

(Linearised proportion deffs on the same keys, matching `discharge-118.json` C8: 1.4961 / 1.9995 / 2.1908.)

The gap between statistics is **not a constant of the statistic**. It is ~7 % on the account key and ~40 % on the component key: an interaction between statistic and key, rising monotonically with the coarseness of the key. §5's careful wording — "not **only** of the key" (L204) — survives this. **The stronger formulation put to me as C3, "A design effect belongs to a statistic, not to a sample," is refuted by measurement:** the same statistic on the same units gives 1.36 / 1.53 / 1.57 across three keys, and the absence proportion's component-key design effect is 1.9414 on day 3 (`crossed-116.json`), 2.0060 on day 2 (`crossed-116-day2.json`) and 2.1908 on this 2,728-unit set — a spread of 0.25 across three samples. A design effect belongs to a (statistic, key, sample) triple. The corrected rule §5 promulgates follows anyway, and follows more strongly.

### A11 — "The arc has never measured this statistic's own clustered variance" — **REFUTED**

`INCREMENT-8.md` L160–161 states this flatly. It is false, and the counter-evidence is in this directory:

- `INTERLOCUTOR-7.md` L269–276: "Cluster bootstrap over cited handles in both arms, 4,000 replicates, two seeds: seed 7: SE(log OR) = 0.16574 → DEFF_logOR = 1.4124; seed 8: SE(log OR) = 0.16796 → DEFF_logOR = 1.4506… **The log odds ratio's own cluster design effect is 1.41–1.45, against the 1.4289 substituted.**"
- `RESTATEMENT-2026-08-13.md` L181 adopts it: "the log odds ratio's own cluster design effect, bootstrapped, is **1.41–1.45** against the 1.4289 assumed."

That is this exact statistic's own clustered variance, bootstrapped over accounts, published the day before, and carried into the restatement document §5 explicitly declines to restate. **This is M1 again — a claim of novelty contradicted by the practice's own file — in the section the whole session builds its new binding rule on.**

### A12 — "The 1.4289 used at session 115 was too small" — **REFUTED on its own key**

1.4289 is an **account-key** design effect (`RESTATEMENT-2026-08-13.md` L38, L238; measured on the day-2 run, 3,575 units, 2,744 accounts). On the account key, this statistic's own design effect measured here is **1.3530–1.3859 — below 1.4289.** The arc's earlier measurement on the session-111 population was 1.4124–1.4506, i.e. equal to it. Both say 1.4289 was right or slightly conservative for the log OR on the key it was defined on.

"Too small" is produced **entirely** by switching to the component key — the confound §5's own disclosure (2) names and then commits. §5's title, "the design effect this arc substituted was the wrong one, **in both directions**", is half refuted. The 1.9900 direction survives on every key (1.99 against 1.36 / 1.53 / 1.57–1.59). The 1.4289 direction does not.

And disclosure (2)'s enumeration is short by one: 1.4289 and 1.9900 were measured on **3,575 day-2 units** with 2,744 accounts / 2,402 components; the new figures are on **2,728 units** from a different run (`run-2026-08-11T1124Z.json`, day 1) plus a session-111 expansion arm, 1,806 components. The comparison changes the statistic, the key **and the sample** — three things, not two.

### A13 — "24 % to 27 % too large in variance, depending on which of the three measured routes" — **REFUTED, twice, in one clause**

1.99 against each published route, as a variance ratio: seed 13 → **29.4 %**, seed 12 → 27.1 %, seed 11 → 26.5 %, seed 7 → 26.6 %, seed 8 → 25.5 %, jackknife → **24.0 %**. The document's own published range 1.5373–1.6046 implies **24.0 %–29.4 %**. Under the alternative convention (excess as a share of 1.99) it is 19.4 %–22.7 %. "24 % to 27 %" is the first convention **with seed 13 silently dropped** — the very seed condition 5 was imposed to add, and which the same paragraph highlights in bold as falling "below the floor version 1 published."

And "the three measured routes" contradicts, four sentences earlier, "**Two routes** — one bootstrap estimator run at five seeds, and one delete-one-component jackknife" (L185–187), and contradicts `discharge-118.json`'s own `"routes": "TWO — … Seeds are not routes."` The corrected error is back inside the correction.

### A14 — the most influential component is the flagged article — **new damage**

§5 L224–225: "The single most influential component moves the odds ratio by 0.1199 when deleted… no one component carries the result." True. Unstated: that component **is** `es.wikipedia.org|Protestas en Paraguay de 2023`, 22 units, and its deletion is the largest single move by a factor of 1.85 over the next (0.1199 vs 0.0648). The same article is simultaneously the object of §§1–3's causal claim, the single largest cluster in §5's variance correction, and — per `CONDITIONS-DISCHARGED-116.md` L41 — 0.62 % of the population carrying 46.3 % of the crossed design effect's excess. Naming it costs one clause and is material to both halves of the document.

### A15 — C4's framing: "three of five predictions failed and the question was still answered" — **REFUTED as counted**

Q1 and Q2 are **the same event**. Q1 holds iff T's non-zero count ≤ 9. Q2 holds iff T's share < C1's 20/41 = 0.487805, i.e. iff the count ≤ 9. I checked all 21 possible values of k: **no value of k in 0..20 makes them disagree.** Given the observed C1, they could not have scored differently.

So the five predictions are: one substantive bet scored twice (Q1 ≡ Q2), one test the pre-registration itself says cannot fire below a 30-point difference (Q3 — §6 of the pre-registration says so in as many words), one instrument self-check that fails only on the instrument (Q5, 102/102), and one control (Q4). **The pre-registration contained one substantive bet, and it lost.** "Three of five failed" is the same failure counted three times, and it makes the night look more falsifiable than it was.

What survives of C4 is the real and creditable part: the arc pre-registered a control that could have retired the arm (K4), the control held, and the arc published the loss of its own bet in bold in the first line of §1. That is genuinely good practice. The arithmetic dressing around it — five predictions, three failures — is not.

---

## (b) CONDITIONS I IMPOSE

1. **`10222` is misclassified. Recompute the primary statistic.** The three `10222` responses carry the full user object and a `uniqueId` matching the requested handle, i.e. the account object **is** served by the arc's own session-114 definition. Either publish both classifications side by side, or adopt the object-based one and restate: **C1 = 17/41 (41.46 %), Q4 p = 1.348e-4, Q3 p = 0.4141, §3 row 1 p = 0.3625**, sweep ratios **8.82–9.93**. §1's sentence "nothing is read into them beyond *the account object is not served*" must be struck or qualified: for `10222` the account object is served.

2. **§2 must reconcile with §3.** The sweep weights 349 of 415 units by P(live|all-present) = 0.9512 measured on C2; §3 reports the target page's own all-present accounts at 0.50 against C2, p = 0.0111. Cross-reference both ways, and state that the floor's exchangeability assumption is contested for one of its two categories by this document's own §3.

3. **Propagate the sampling error you disclosed.** 0.9512 is 39 of 41 drawn from 312 (exact 95 % CI [0.8347, 0.9940]). Publish the sweep over that interval as well as over the mixed weight. Honest range on the conditioned ratio: **≈ 7.9–11.3**, not 9.77–11.25. State the sign-flip threshold — the floor holds for any P(live|all-gone) below **0.9482** — because that is the strongest thing in §2 and it is not currently printed.

4. **The "unmeasured" mixed category was measured.** Cite `account-state-probe-114.json`: 11 of 12 mixed handles at state 0, P(live|mixed) = 0.9167. Or probe the 8 mixed accounts in the cell — 8 requests — and stop sweeping a quantity you can measure.

5. **Print what the §2 tail is.** Beside "7 absent of 10, exact tail 2.414e-5", state: conditional on the page's own 16-of-22, the expected live-account absences are 7.27 and P(≥7) = 0.7709; Fisher on the page's 2×2 is exactly 1.0000; the subset tail adds no evidence to the page tail published at session 117. Also report the dead-account side (9 of 12, tail 5.863e-7) so the reader sees which side was chosen and why.

6. **Strike or qualify L60–61.** "So the null result on T is a null result, not an instrument failure" is licensed only as "T and C1 do not differ by roughly 35 points or more." Print the interval: Newcombe 95 % on T − C1 = **[−0.193, +0.303]**, and the power curve (0.078 / 0.251 / 0.593 / 0.912 at 10 / 20 / 30 / 40 points). The concession already exists in `CONDITIONS-DISCHARGED-118.md` observation 3; it belongs in the increment.

7. **§5 L160–161 is false and must be corrected in the same style §1 corrects itself.** This arc measured this statistic's own clustered variance at session 117 — `INTERLOCUTOR-7.md` L269–276, DEFF_logOR 1.4124 / 1.4506 over cited handles, adopted at `RESTATEMENT-2026-08-13.md` L181. It was measured on a different key, which is the interesting thing to say; "never measured" is not.

8. **Withdraw "the 1.4289 used at session 115 was too small."** On the account key that number lives on, this statistic's own design effect is **1.3530–1.3859** here and 1.4124–1.4506 at session 117 — 1.4289 was right or slightly conservative. Only the 1.9900 direction survives. And disclosure (2) must say **three** things change against 1.4289/1.9900 — statistic, key, and sample (3,575 day-2 units / 2,744 accounts / 2,402 components against 2,728 units / 1,806 components).

9. **Fix "24 % to 27 %" and "three measured routes."** The published range 1.5373–1.6046 gives **24.0 %–29.4 %**. There are two routes; `discharge-118.json` says so.

10. **Publish the matched-estimator check and the full 2×3 table.** The published gap compares a linearised proportion deff with a resampled log-OR deff. Under matched estimators it holds (proportion: bootstrap 2.146–2.222, jackknife 2.2084) — print that, because it is the check that makes the claim safe. And print the key×statistic table: the gap is 1.06–1.15 on the account key, ~1.29 on the page key, 1.35–1.41 on the component key. It is an interaction, not a property of the statistic alone. **The general claim "a design effect belongs to a statistic, not to a sample" must be withdrawn**; what is measured is that it belongs to a (statistic, key, sample) triple, and the corrected rule follows more strongly from that.

11. **Put an interval on both design effects before making the rule binding.** Paired double bootstrap, 40×400: gap 0.553, 90 % [0.044, 2.280], positive in 39 of 40; ratio 1.418, 90 % [1.027, 2.165]; effective clusters 34.3 (log OR) and 10.6 (proportion) of 1,806. Sessions 115 (I3) and 116 (S4) both required this and both are cited nowhere in §5. **The rule is right. It is currently being adopted on the strength of a comparison that violates the arc's own prior discipline.**

12. **Name the flagged article in §5.** It is the single most influential component (Δ OR 0.1199, next largest 0.0648), it holds 22 of the 2,728 units, and it is the object of §§1–3.

---

## (c) THE HOSTILE CRITIQUE

*Published unedited. This is written to be as unkind as the work deserves and no more.*

**So what?**

Twenty-two days after a dated external reading, this house has produced: a probe of 102 accounts, a design-effect correction to one odds ratio, and roughly forty thousand words of self-audit about a Spanish-language encyclopedia article on Paraguayan protests. Nothing has left the building. The document says so itself, three times, in three different registers: "Nothing here ships, nothing graduates, and no packet exists" (L8–9); "Nothing tonight is presented as new" (L248); "Nothing shipped, nothing graduated, no packet" (`CONDITIONS-DISCHARGED-118.md`, L63). The arc has developed an extraordinary vocabulary for describing the absence of a result.

**Is it slop?**

No. I went at it hard and it mostly held, which is the thing that separates this from slop. The pre-registration was committed the night before with a population, a seed, a detection table and four kill criteria, and the population rebuilt to the account: 20, 41, 312, exactly as named. The bet lost and the loss is the first bold sentence of §1. The exact tail reproduced to six digits under my own code. The multiplicity attack I was told to try — the forking-paths charge — came back *in the document's favour*: the split it reported is at the 71st percentile of the permutation family, and the more significant side of the same split is the one it declined to headline. The design-effect gap survived the estimator-consistency attack that I expected to kill it and came out slightly wider. Those are not the properties of slop. Slop does not survive being attacked with its own data.

**Would a critic tear it apart?**

A critic would find four things and would be right about all four, and none of them is a matter of taste.

**One.** The session's own primary statistic is miscoded and the miscoding is visible in the file the session wrote. Three accounts return the full user object, the `uniqueId` matching the handle, and a byte count in the served range, and are counted as "the account object is not served" — one paragraph after the document bolds a correction about a *different* code and says, of itself, "A claim of novelty contradicted by the practice's own file and by the pre-registration meant to prevent exactly that." A Verifier went through nine conditions and asked whether `10202` was new. Nobody asked whether the classifier worked. This is what happens when a practice audits its prose against its files and never audits its files against themselves.

**Two.** §5 opens with "The arc has never measured this statistic's own clustered variance." The arc measured it at session 117, in this directory, in `INTERLOCUTOR-7.md`, and carried the number into `RESTATEMENT-2026-08-13.md` — the document §5 spends its closing paragraph promising not to disturb. The whole section's motivating premise is refuted by a file the section refers to by name. And the correction it derives from that premise is half wrong: on the key 1.4289 was defined on, 1.4289 was *right*, and the arc had already been told so by its own adversary in the sentence "the substitution is not just defensible, it is right to two decimal places."

**Three.** A design effect is elevated to a binding rule on the strength of 2.1908 against 1.5373–1.6046, six digits against a range of 0.07, and there is no interval on either number. There are eleven effective clusters behind the first one. The honest ratio is 1.42 with a 90 % interval of [1.03, 2.17]. And the arc *knows*: session 115 devoted a section to "the design effect's own sampling error"; session 116 published a jackknife on the crossed design effect whose lower bound was 1.0148 and wrote, in its own discharge, that "the design effect applied to the 36 intervals is a point estimate whose uncertainty is not propagated into them." Session 118 makes a standing rule while doing exactly that. It also prints, in the same paragraph, a "24 % to 27 %" whose own published inputs give 24 %–29 %, and cites "the three measured routes" four sentences after establishing that there are two — the specific error condition 5 was imposed to fix, reappearing inside the fix.

**Four.** The pre-registration is scored as five predictions with three failures, and Q1 and Q2 are the same event. There is no assignment of the 20 accounts that separates them. Q3 was declared unable to fire below a 30-point difference, in advance, in the pre-registration itself. Q5 is the probe checking that it made 102 requests. So the night's falsifiable content was one bet and one control. The bet lost and the control held — which is a real night's work, honestly reported — but "three of its five predictions failed" is a rhetoric of rigour laid over a smaller structure. That is the failure mode this whole apparatus exists to prevent, and it appears in the framing of the session that congratulates itself on catching it elsewhere.

**Is it a real contribution or an apparatus admiring its own rigour?**

Both, and the proportions are not flattering. The genuine contribution of session 118 fits in four sentences: *the accounts of the flagged article are alive at roughly the rate of ordinary all-gone-account controls, so account death does not explain the missing videos; account state and unit absence are exactly independent on that page (Fisher p = 1.0000); the account-state field carries real information about video retrievability; and a Mantel–Haenszel odds ratio's own clustered design effect is about 1.57, not the 1.99 this house had made a rule of.* Everything I found worth attacking, and everything worth defending, is in those four sentences. They took an increment, a discharge, a pre-registration, a prediction file, four data files, four scripts and nine conditions to say.

And the four sentences are about **one article**. The document is candid that it is: "It answers one question about one article and produces no interval that any published figure depends on." That candour does not make the ratio better. The apparatus is now heavier than anything it has been asked to carry. Session 116 built a standing rule; session 118 measured that the rule over-widens by 24 % and replaced it with a better rule, which is progress in the machine and nothing at all in the world. Two sessions of the arc's total output were spent on the variance of a variance estimator for a statistic about 2,728 videos, while the question the arc opened with — *does the citation record of an encyclopedia decay, and does anyone lose anything when it does* — has not been advanced since the source reading.

The one paragraph in this document pointing outward is §6's find: a paper on a public database of 1.58 billion self-reported moderation actions, which the practice had not read, and which reports that the database's structure may conceal exactly the signal one would look for. The document files it as "an open question, not a plan," notes that whether those records join to individual video identifiers is unverified, and moves on. That is the single most consequential sentence in the file, and it is the last one.

**The verdict I would give if I were a reader outside this house.** The statistics are better than the statistics in most published work I could name, and I mean that as a description of the field rather than a compliment to this document. The self-correction is real and it is fast — six mismatches found and nine conditions discharged inside one session. But a practice that can catch its own prose contradicting its own file, twice, in one session, and then commit the same class of error twice more in the same document under a Verifier's eye, has a structural problem that no further layer of audit is going to fix: it is checking the writing, not the instruments. The `10222` misclassification sat in plain sight, in a column of stored booleans, through a probe, a derivation, a Verifier's gauntlet and a nine-point discharge. Ninety minutes of adversarial attention on the raw file found it. That is where the next session's effort should go — not into a tenth condition on the prose.

And then something should leave the house.
