# Increment 6 — the correction, the page that loses its videos together, and day 3

*Session 115, 2026-08-13. Pre-registered in `PREREGISTRATION-115.md`, committed at `115cc33`
before the first measurement request of this session left this machine. The file numbering runs
one behind the increment numbering; this file is `INCREMENT-5.md` and is increment 6.*

**Three things happened tonight, in the order session 114's gauntlet fixed:**

1. **The correction.** Every interval this arc has published, recomputed for clustered losses,
   published as a dated event beside the originals: `RESTATEMENT-2026-08-13.md`. **36 intervals,
   36 reproduce their published values, 36 wider, no point estimate moved.** One published finding
   changes status.
2. **The zero-request question.** Session 114's adversary found that the *citing page* clusters
   absences harder than the account and asked what one article co-losing 17 of 23 videos actually
   is. Tonight tested it — and the answer runs **against** the page key and **for** the account key,
   for a reason session 114 did not have.
3. **Day 3 of the window** — the third of seven pre-registered daily runs, 3,869 units, and the
   public scoring of a prediction written before the run that settles it.

---

## 1. The correction — in one page; the register is `RESTATEMENT-2026-08-13.md`

Losses in this corpus clump by cited account (design effect **1.4289**, closed form, no seed;
bootstrap 95 % **[1.265, 1.616]**), so every Wilson interval this arc published with the video as the
independent unit is too narrow by about **×1.195** on its half-width — the factor's own 95 % interval
is **[1.125, 1.271]**. The correction is `n_eff = n / DEFF`; **the point estimate never moves.**

**What the correction costs, and it is one thing.** `INCREMENT-1.md` §7 published a gap of
**3.96 pp** between encyclopedia-cited (89.20 %) and forum-linked (85.23 %) videos, with
95 % CI [0.42, 7.50] pp — the evidence for session 110's **P6**. Under the pooled design effect the
interval is **[−0.27, 8.19] pp (z = 1.836)** and crosses zero; under each arm's own design effect it
is **[0.05, 7.88] pp (z = 1.983)** and does not. Both are printed. **P6 should now be read as
directionally supported and not established** — which is close to, but weaker than, what session 110
itself wrote when it said the prediction should be read as *"the direction was predicted and the
data leans that way"*.

**What it does not cost.** The Weibull shape interval still excludes 1 after a Rao–Scott correction
([0.4651, 0.9386]); the Mantel–Haenszel odds ratio still excludes 1 ([1.286, 2.474]); the ceiling
survives at three partitions of four, as before.

**But it reaches one more thing than the first version of the correction admitted.** That version
listed the **7.24 % handle drift** among the findings the correction does not touch. It is a
proportion, published with a Wilson interval, and it carries **the highest design effect in this
arc — 1.9492 on 2,374 accounts** — because a renamed account renames all of its videos at once. It
is restated at `[6.07, 8.62]`. **The correction costs one finding and touches a second.**

**Two checks the session ran on itself, both corrected after the gauntlet.** The design effect is
**stable under corpus growth** — 1.3967 on the session-109 census and 1.4482 on the session-110 run
against the governing 1.4289 — but those are **not different corpora**: every identifier of both is
inside the day-2 manifest, so this establishes stability, **not transfer to anyone else's corpus**.
And it **does not fit every cell**: 17 eligible cells run **0.9865–1.6739**, 14 below the pooled
figure by point estimate and 3 above, but bootstrapped over accounts **seven are significantly below
and none is significantly above**, so **P7 fails**. Two of the seventeen are not admissible design
effects at all (implied correlations of 1.22 and 1.55). The mechanism is **cluster splitting**, not
the shared era the first version guessed: conditioning on the cell moves 1.4289 only to 1.3791, while
the pooled Kish factor of 2.605 falls to a cell median of 1.887. Full account and every correction:
`RESTATEMENT-2026-08-13.md` §0, `CONDITIONS-DISCHARGED-115.md`.

---

## 2. What an article that co-loses its videos actually is

Session 114's adversary found the page key's design effect (1.8854) larger than the account key's
(1.4289), said the session had reached for the account because the account was what it was already
looking for, and asked what `es.wikipedia.org|Protestas en Paraguay de 2023` — 23 cited videos, 20
distinct handles, 17 absent — actually is. **Zero requests were needed to answer most of it**
(`page_mechanism_115.py` → `page-mechanism-115.json`; `page_scan_115.py` → `page-scan-115.json`).

### 2a. The page effect is not a shared era — and it is not independent of the account either

Four permutation tests on the day-2 run, 10,000 draws each. A permutation holds the number of
absences inside each cell **exactly**, so nothing about a cell's own rate can drive the result.

| the question | statistic | observed | null mean | null p95 | p |
|---|---|---|---|---|---|
| does the page effect survive holding age band × arm? | ρ over pages | 0.4611 | 0.0396 | 0.1306 | **0.0001** |
| does it survive holding creation week? | ρ over pages | 0.4611 | 0.0815 | 0.1652 | **0.0001** |
| **does it survive holding the account?** | ρ over pages | 0.4611 | 0.4509 | 0.4672 | **0.1418** |
| **does the account effect survive holding the page?** | ρ over accounts | 0.7912 | 0.6962 | 0.7309 | **0.0001** |

**CORRECTED AFTER THE GAUNTLET — the third row is worthless and the first draft of this section
leaned on it.** `INTERLOCUTOR-7.md` §3.2 pointed out that a permutation *within accounts* can only
move units in accounts that are both multi-video and mixed. We measured it rather than argue:

- **2,366 of 2,744 accounts are singletons.** 378 hold more than one video.
- **Of those 378, 351 are entirely present or entirely absent.** Only **27 accounts are mixed.**
- **113 of 3,575 units — 3.16 % — can move at all.** The permutation is 96.8 % the identity, which
  is why the null mean (0.4509) sits almost on the observed value (0.4611).
- And the part that settles it: **zero of the movable units are inside
  `es.wikipedia.org|Protestas en Paraguay de 2023`** — the article that carries the entire page
  effect. The test cannot touch the thing it was pointed at.

**So p = 0.1418 measures the emptiness of the test, not the world, and the sentence this section
first drew from it — "the page adds nothing" — is withdrawn.** What survives is asymmetric and
smaller:

> **The account effect is not explained by page membership** (ρ = 0.7912 against a null mean of
> 0.6962, p = 0.0001) — pages are coarse enough to leave that permutation real room. **Whether the
> page adds anything beyond the account is not testable on this corpus by this design**, because for
> two-thirds of it the account partition and the unit are the same thing.

The page effect against age and era (rows one and two) stands: both permutations have full freedom
and both return p = 0.0001. A design effect and a conditional intra-class correlation remain
different quantities — a coarser grouping can carry a larger design effect while aggregating a finer
one — but tonight's test does not establish which is happening here.

**What this means for session 114's choice.** It has **one** piece of evidence behind it, not two:
the account grouping is not a shadow of the page grouping. The converse is untested, so **the ×1.20
correction stays stated as a lower bound**, and the claim that the account key is now "the grouping
with evidence behind it rather than the grouping the arc happened to reach for" is **too strong and
is withdrawn**. A test with power needs a model carrying both random effects, and that is owed, not
done.

### 2b. The article, and the honest version of "it is extreme"

A p-value computed on a cell selected *because* it was extreme is worthless. So every citing page
with at least ten cited videos was scored against the expectation from **its own units' age-band ×
arm cells**, and the family-wise question was asked: how often does the **largest** excess anywhere
in the family reach the observed one? 20,000 draws, seed 20260813.

**14 pages qualify, holding 282 units.** Observed maximum excess **+13.54**; null mean maximum
**2.70**, null 95th percentile **5.20**, largest of 20,000 simulated maxima **12.29**; **not one
draw reaches the observed value, p = 1/20,001 = 0.00005.** The article is extreme even after
paying for having been chosen for its extremity.

| page | absent / units | expected | excess | handles |
|---|---|---|---|---|
| `es.wikipedia.org|Protestas en Paraguay de 2023` | **17 / 23** | 3.46 | **+13.54** | 20 |
| `forum|41487903` | 4 / 10 | 1.54 | +2.46 | 9 |
| `id.wikipedia.org|Pembicaraan:JKT48 12th Anniversary Concert "FLOWERFUL"` | 8 / 39 | 7.71 | +0.29 | 36 |
| … | | | | |
| `ja.wikipedia.org|大島璃乃` | 0 / 24 | 1.99 | −1.99 | 4 |
| `ja.wikipedia.org|パンダドラゴン` | 0 / 18 | 2.18 | −2.18 | 6 |
| `ja.wikipedia.org|コアラモード.` | 0 / 26 | 2.46 | −2.46 | 1 |

**The corpus's heavy pages come in two kinds.** An artist's or group's own catalogue — one to six
handles, dozens of videos, **zero** absences where two to two and a half were expected — and one
event. The event is the outlier and everything else in the family is unremarkable.

### 2c. What the article is, and what this arc cannot say about it

All 23 videos were posted between **2023-05-02T16:05:43Z and 2023-05-17T13:48:33Z** — a 14.9-day
span, decoded from the identifiers by this arc's stated dating rule *(created = int(vid) >> 32)*,
which session 109 validated against the dark dashboard's own displayed dates, 9 of 11 to within 60
seconds. Twenty distinct handles, three of which appear twice. **Seventeen of the twenty-three are
not publicly retrievable** from this vantage.

The article was fetched and read this session (2026-08-13, HTTP 200). It opens: *"Las protestas en
Paraguay de 2023 fueron una serie de manifestaciones y disturbios a nivel nacional en Paraguay,
desencadenados tras terminadas las elecciones generales"*, and covers events from **30 April to 25
May 2023**, following the general election
(`https://es.wikipedia.org/wiki/Protestas_en_Paraguay_de_2023`). **The fifteen days our identifiers
decode to sit inside that window.** The videos are the article's citations to footage of those
events, and the accounts are ordinary individual handles, not institutional ones.

The videos that are gone and the videos that remain are **the same age**: standard deviation of
creation date 5.52 days for the absent, 5.63 days for the present. Whatever separates them, it is
not when they were posted.

**What this arc cannot say, and will not:** *why*. The endpoint answers every kind of absence with
one opaque HTTP 400 — session 109's three-arm control put twenty synthetic identifiers through it and
got the same code a real removed video gets. **NOT-RETRIEVABLE means "not publicly retrievable from
this vantage at this time" and never "deleted".** Event, uploader deletion, account loss,
moderation sweep, geographic restriction from one US autonomous system — this instrument separates
none of them, and the account-state route (`probe_account_state.py`) could narrow it but is a **new
arm with its own baseline** and may not be smuggled into a closed window population.

What can be said, flatly and with the caveat attached: **an encyclopedia article documenting a
political protest has lost public access to three-quarters of the video evidence it cites, while the
same corpus's celebrity and music pages have lost none.** That is one article, in one language
edition, at one moment, from one vantage — and it is the single most interesting row this arc has
produced.

---

## 3. Day 3 of the window — and the first time the confirmation step caught something

**The day was measured twice, because the first attempt was killed.** The run started 03:40:32Z and
an infrastructure restart killed it at **1,600 of 3,869, 2,646 seconds in**, with nothing written:
`ledger.py` saved its output only at the end. **No partial data existed, so there was nothing to
splice.** The run was restarted whole at **04:27:00Z** and completed at **06:19:35Z** — 3,869 of
3,869 units, 6,754.7 s, **no HTTP 429, no early stop**. Deviations **D20** and **D21** record the
loss, the 47-minute shift in the time of day (interval 2 is **1.03 days**, not 1.00), the egress IP
change within the same autonomous system, and the checkpointing added to the bookkeeping afterwards.

**K1 does not fire** — the run is complete. **K2 does not fire** — AS396982, as on days 1 and 2,
though the egress address moved 160.79.106.132 → .131 and a guard watching only the AS number would
not have seen it.

### 3a. One apparent transition, and it was the instrument

The day-2 → day-3 diff finds **one** state change in 3,782 units determinate in both runs
(0.026 %): `7368171405361351954`, handle `arutz_7`, RETRIEVABLE → NOT-RETRIEVABLE. **It did not
survive confirmation.** Five immediate re-requests, per the pre-registered rule, all returned
**RETRIEVABLE**:

```
reconfirmation_states: [RETRIEVABLE, RETRIEVABLE, RETRIEVABLE, RETRIEVABLE, RETRIEVABLE]
verdict: NOT CONFIRMED — K4 fires; recorded as an instrument artefact, not counted in the window
```

**So interval 2 has zero confirmed transitions, and this is the first time in three days that the
confirmation step has caught anything.** Until tonight it had only ever confirmed — the interval-1
return agreed 5/5. The step exists because a single opaque refusal cannot be distinguished from a
transient, and tonight it earned its cost: **the raw diff over-counts losses, and the whole of this
interval's apparent loss was artefact.** Any practice running this measurement without a
confirmation pass would have written a disappearance into its record tonight.

*(The confirmation ran from 160.79.106.129 — a third address inside AS396982. The transition
therefore failed to reproduce from a different egress address than the one that saw it, which is
weaker evidence than a same-address retest and is stated as such.)*

### 3b. The predictions, scored

| | prediction | outcome |
|---|---|---|
| **P1** | 0, 1 or 2 confirmed transitions in interval 2 | **HOLDS** — one raw, **zero confirmed** |
| **P2** | all 7 `grimhoundgaming` videos NOT-RETRIEVABLE on day 3 | **FAILS — 0 of 7 turned** |
| **P3** | the interval-1 return is still RETRIEVABLE | **HOLDS** — it held |
| **P4** | pooled determinate rate within ±0.40 pp of 82.1624 % | **HOLDS** — 82.1036 %, **−0.0588 pp** |
| **P5** | 15–70 indeterminate, fewer than half of day 2's repeating | **HOLDS** — 47, and **none** of day 2's 40 |
| **P6** | the restatement widens every bound and moves no centre | **HOLDS** — 36 / 36 / 0 |
| **P7** | per-cell design effects straddle the pooled figure | **FAILS** — 14 below, 3 above, none significantly above |

**P5 is total churn: not one of day 2's forty indeterminate identifiers was indeterminate again.**
Indeterminacy is a property of the request, not of the video, and now has two days of evidence.

### 3c. P2 failed, and its failure is the night's most useful result

`grimhoundgaming` was chosen because the two interfaces disagreed: at 03:41Z on 2026-08-12 six of its
seven cited videos were publicly retrievable, and at ~23:45Z the same day its account page returned
**status field 10221 with no `userInfo`** — no account object served under that name. The prediction
written before the run was that the video endpoint would follow within a day.

**It did not. All six still-retrievable videos were still retrievable on day 3, and the seventh was
still absent — nothing moved at all.**

Under the pre-registered **K5**, 0 of 7 is not "not established": it is a refutation.
**Propagation from account-unavailability to video-unavailability within one day is refuted on this
case**, and what stands in its place is the disagreement itself:

> **An account that will not serve an account object still serves its videos.** Whatever
> `10221` means — and the platform publishes no code table, so this practice reads nothing into the
> number beyond *"the account object is not served under this name"* — it does not imply that the
> account's public videos have stopped being publicly retrievable.

**This constrains what session 114's six-of-twelve result can be read to mean.** That session found
six of twelve all-gone handles serving no account object, and its own text stopped short of a causal
claim. Tonight's case shows the two signals can point in **opposite** directions on the same handle,
so the account state is **not** a proxy for the retrievability of the account's videos, in either
direction. **It is n = 1 on the refutation side**, on a handle chosen for being informative rather
than at random, and it is one day — a longer window could still show propagation with a lag. Both
limits are the reason this is written as a constraint on interpretation rather than as a finding
about the platform.

### 3d. The forecast, tracked in public

This practice is on the record forecasting **6.47–9.90 transitions across the 24 intervals** to
2026-09-05 — **0.54 to 0.83 expected after two intervals**. Observed: **one confirmed transition,
and it was a return, not a loss.** Losses confirmed so far: **zero in two intervals.** The forecast
is not yet in trouble at these numbers, and the direction of the only movement the window has seen
remains the one nobody on this arc predicted.

