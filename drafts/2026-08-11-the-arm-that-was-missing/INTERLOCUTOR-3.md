# Interlocutor pass 3 — the power audit

**Target:** `POWER-AUDIT.md` (increment 2, session 111), `PREREGISTRATION-111.md` (commit `9625a25`),
`power_audit.py`, `power-audit.json`, `ledger/run-2026-08-11T1124Z.json`.

**A note on method before anything else, because it matters to the verdict:** this object was not
static while I worked on it. Between my first read of `POWER-AUDIT.md` (180 lines, ending at §9) and
my last read of it, the repository moved through six more commits — `fa24bb0`, `21fb239`, `a4d5455`,
`f16c540`, `74e35e8`, `38c47af` — each adding a self-found correction or extension. I made none of
these commits; I have no write access to this repository and did not use one. This report audits the
state at **`HEAD = 48603ff`** (`git log -1`, confirmed below), specifically `POWER-AUDIT.md` as it
stood at commit `38c47af`, which was the last commit to touch that file before I finished. Two of the
concrete faults I found independently — described in §(a).3 and §(a).8 below — were *also* found and
fixed, in the direction against the audit's own conclusion, by the process that produced the document,
in commits that postdate the base audit (`0be6151`) but predate my finishing this report. I flag this
plainly rather than claim credit for catches I did not get to first, and I flag it because a moving
target changes what "REFUTED" can mean: some of what I found is no longer in the document.

Every command below is reproducible from `/home/user/field-research/drafts/2026-08-11-the-arm-that-was-missing/`
unless stated otherwise. My own re-implementation lives at
`/tmp/claude-0/-home-user-field-research/5bb58988-490a-586c-98a6-fb4d57bc6c88/scratchpad/reimpl.py`
and is reproduced in full at the end of this report (§ appendix) so a third party does not have to
trust a path outside this directory.

```
$ git log -1
48603ff5f1422974430d3f7044a5a6d3bf7d3f6b
$ python3 -c "import numpy" ; python3 -c "import scipy"
ModuleNotFoundError: No module named 'numpy'
ModuleNotFoundError: No module named 'scipy'
```

---

## §(a) — Does the core claim survive?

**The claim under test, verbatim from my brief:** *"the arc pre-committed that zero state transitions
across seven consecutive daily runs kills its daily-series argument. Under the disappearance hazard
implied by the corpus the arc already holds, the expected number of transitions over that window is
1.31 and the probability of observing zero is 0.27 — so the criterion fires by chance roughly one time
in four even if the implied rate is real, and if it fires it delivers a likelihood ratio of only about
3.7:1, which the arc promised to treat as decisive."*

### 1. Independent re-implementation — the headline arithmetic reproduces exactly

I wrote my own loader, my own Weibull MLE (ternary search in log-λ at each grid point in k — not the
golden-section search `power_audit.py` uses, a different search algorithm entirely), my own
profile-likelihood CI, my own hazard and expected-transition formulas, from the raw ledger file. I did
not import or execute `power_audit.py`.

```
$ python3 reimpl.py
n analysed: 2618 excluded: {'btrunc': 249, 'indet': 33, 'notdigit': 4, 'nonpos': 0}
retrievable: 2320 / 2618 = 0.8861726508785333
mean age (yr): 2.8796361378641837
naive lambda/yr: 0.041964844176153024
Weibull MLE (independent fit): k = 0.695856502117081  lambda = 0.01787172521419502  loglik = -899.2759988840289
profile-likelihood 95% CI on k: (0.5012977718809741, 0.8989921227497276)
E[transitions] fitted (D=6): 1.309048530036077  P(zero) Poisson approx: 0.27007690423613195
E[transitions] naive (D=6): 1.5993172647010272  P(zero): 0.20203440693969896
Likelihood ratio = 3.703 : 1
```

Every headline number matches `power-audit.json` to at least four significant figures: k = 0.6959,
λ = 0.01787, CI [0.5013, 0.8990] against their [0.5017, 0.8983] (the ~0.001 difference is grid
resolution — I used 2000 steps on the k-grid, they used 1200, and both are approximations of a
continuous profile), E = 1.309, P(zero) = 0.270, LR = 3.70 : 1. **The core arithmetic is not
fabricated and is not a bug. I could not break it by rewriting it from scratch.**

**The Poisson approximation itself, checked exactly.** `P(zero) = exp(-E)` is a small-probability
approximation to the true product of per-identifier survival probabilities over the window. I computed
the exact product directly from the Weibull cumulative hazard (`exact_p_zero` in the appendix, no
Poisson shortcut):

```
EXACT P(zero), D=6 (no Poisson approx): 0.271143712681605  vs Poisson-approx: 0.27007690423613195
```

The exact figure is 0.0011 *higher* than the reported approximation — i.e. the approximation the audit
uses is very slightly conservative in the direction of understating its own point (P(zero) is actually
marginally higher, the criterion marginally weaker, than what was published). This is a clean, unbiased
detail: if there were a thumb on the scale here it would run the other way.

### 2. The exclusions — I recomputed under four different rules; none moves the conclusion by more than a rounding error

| exclusion rule | n | live | k | λ | E (D=6) | P(zero) |
|---|---|---|---|---|---|---|
| as pre-registered (baseline) | 2,618 | 2,320 | 0.6959 | 0.01787 | 1.309 | 0.2701 |
| include B-truncated rows | 2,618 | 2,320 | 0.6959 | 0.01787 | 1.309 | 0.2701 |
| INDETERMINATE counted as dead (conservative) | 2,651 | 2,320 | 0.6581 | 0.01756 | 1.396 | 0.2476 |
| INDETERMINATE counted as alive (generous) | 2,651 | 2,353 | 0.6903 | 0.01710 | 1.301 | 0.2723 |
| relax digit filter to 17+ (admits the 4 excluded rows) | 2,622 | 2,321 | 0.7127 | 0.01920 | 1.332 | 0.2641 |

Two findings worth stating plainly:

- **"Include B-truncated rows" changes nothing at all**, and the reason is not that the exclusion is
  vacuous in principle but that it is *redundant in this corpus*: every B-truncated vid has a length in
  {5,…,18}, never 19, so the 19-digit filter already screens all 249 of them out before the arm filter
  gets a chance to matter. The pre-registration argues for excluding B-truncated as a substantive
  decision (§2: "the harvest artefact… not videos"); in this run of the numbers it is belt-and-suspenders,
  not load-bearing. Worth knowing, not a flaw.
- **The most adversarial reasonable choice (INDETERMINATE-as-dead) moves P(zero) from 0.270 to 0.248**
  — LR from 3.70:1 to 4.04:1. Still nowhere near what "decisive" would require under any normal
  reading of that word.
- **I independently decoded the 4 excluded 18-digit rows anyway**, using the same `>>32` rule, to check
  whether the exclusion is doing real work or laundering an inconvenient case:
  ```
  vid=194951213564514304 state=RETRIEVABLE   decoded_year=1971 created_epoch=45390616
  vid=677767122007582643 state=NOT-RETRIEVABLE decoded_year=1975 created_epoch=157804955
  vid=726459750741134635 state=NOT-RETRIEVABLE decoded_year=1975 created_epoch=169142091
  vid=740580884959830349 state=NOT-RETRIEVABLE decoded_year=1975 created_epoch=172429924
  ```
  All four decode to years before the platform existed. That is exactly the failure mode
  `PREREGISTRATION-111.md` §2 describes for the 19-digit rule (and `194951213564514304` is the literal
  example it names). **This exclusion is not a convenience filter; independently re-deriving it from
  the raw ids confirms it is doing exactly the job claimed for it.**

### 3. The dating rule — holds under an external check, but the window arithmetic it feeds is a genuine problem the document has already half-fixed

`int(vid) >> 32` as unix seconds, restricted to 19-digit ids, produces a clean 2018–2026 cohort spread
with no visible artefacts (my own cohort-fraction table below matches the published one to four
decimal places). I could not break the decoding rule itself.

**What I could, and did, break independently before reading past §8 of the document: the interval
count.** `CONCEPT.md` §5a, the actual pre-commitment, reads (verified verbatim):

> "if after **seven consecutive daily runs** (through 2026-08-18) the ledger has recorded **zero**
> state transitions across the whole corpus, the daily-series argument is **dead**, and this arc's
> value rests on the one-time findings it has already produced — which the record will say in those
> words, and the arc parks."

`PREREGISTRATION-111.md` §1 and `power_audit.py`'s `D_INTERVALS = 6` treat day 1 as 2026-08-11 (per
`INCREMENT-1.md`'s ruling that the two same-day runs count as one day) and count seven runs as
2026-08-11 … 2026-08-17 — six intervals. But `CONCEPT.md` §5a's own parenthetical names **2026-08-18**
as the closing date, which is the date you get if the seven runs are 2026-08-12 … 2026-08-18 (i.e. if
2026-08-11 is a baseline that precedes the seven counted runs, not the first of them) — **seven**
intervals. Nothing in `PREREGISTRATION-111.md`, `INCREMENT-1.md`, or the base text of `POWER-AUDIT.md`
(§§0–8, as originally committed at `0be6151`) reconciles this, and the direction of the error is not
neutral: **fewer intervals means a smaller E, a larger P(zero), and a weaker likelihood ratio — exactly
the direction that flatters this session's own thesis that the criterion is underpowered.** I computed
both readings independently before finding that the document had already done the same thing:

```
--- If the window is 7 intervals (CONCEPT.md's literal 'through 2026-08-18') ---
E[transitions] fitted (D=7): 1.5272232850420893  P(zero): 0.21713776067633217  LR: 4.605371248580806
```

This matches `power-audit-addendum-window.json`'s figure (1.5272231770970033) to seven significant
figures. **The document has, in fact, already caught this** — §8a, added after the base text was
committed, runs both readings, states the direction of the bias against itself, and adopts the
seven-interval reading as "governing" specifically because it is "the reading least favourable to this
session's own conclusion." That is the correct response to the problem. But two things remain true and
are conditions, not resolved:

1. **The §0 blockquote of CONCEPT.md §5a, as it stands right now, still silently drops the
   parenthetical date.** Compare the actual text above to what is printed in `POWER-AUDIT.md` line 15–16:
   > "if after **seven consecutive daily runs** the ledger has recorded **zero** state transitions
   > across the whole corpus, the daily-series argument is **dead** … and the arc parks."

   The `…` is placed *after* "dead," eliding "and this arc's value rests on the one-time findings it
   has already produced — which the record will say in those words" — a marked omission. But
   "(through 2026-08-18)" — the one clause whose absence let the six-interval miscount stand for
   twelve minutes of git history uncontested — is dropped with **no ellipsis mark at all**, mid-clause,
   as if the sentence simply reads "seven consecutive daily runs the ledger…" This is a quotation-
   accuracy fault, and it is not cosmetic: an inaccurate quotation of the single sentence the whole
   session is auditing hid, from a reader trusting the quote, the exact fact that turned out to be
   load-bearing. §8a fixes the *number*; it does not fix the *quotation* that obscured the number's
   origin. **This is condition 1, below.**
2. §§1–8 of the document (the tables in §1, §3, §4, §7, §8, the K1–K4 kill-criteria verdicts) are all
   still expressed in six-interval terms, with only a pointer at the bottom (§8a) to the seven-interval
   "governing" figures. A reader who stops at §7's prediction table or §8's kill-criteria table — which
   is most of the document — reads P3, P4, K3, K4 scored against **1.309 / 0.270**, not the numbers the
   document itself says now govern. **This is condition 2.**

### 4. Model dependence — I fit three more models from scratch; the power conclusion does not depend on the Weibull choice

- **A completely different estimation method on the same individual data — Weibull maximum likelihood
  as published.** (already covered above)
- **A grouped weighted-least-squares cloglog fit on the nine cohort means** — a different estimator
  class entirely (linear regression on a transformed cohort table, not individual-level likelihood
  maximisation), and the exact discrete-time equivalent of the Weibull model:
  ```
  cloglog-OLS-on-cohorts: k=0.7066  lambda=0.01842/yr  (cf. MLE k=0.6959 lambda=0.01787)
  E(D=6) under cloglog-OLS fit: 1.3082  P(zero)=0.2703
  ```
  Essentially identical to the MLE figure.
- **A log-logistic survival model**, `S(t) = 1/(1+(t/α)^β)`, a different distributional family with its
  own from-scratch MLE:
  ```
  log-logistic MLE: alpha=43.324yr  beta=0.7360  loglik=-899.253  (Weibull loglik=-899.276)
  E(D=6) under log-logistic fit: 1.3076  P(zero)=0.2705
  ```
  The two models are statistically indistinguishable on this data (Δloglik = 0.02 for the same number
  of free parameters) and give the same power answer to three decimal places.
- **A fully non-parametric cohort read-off**, computing a local hazard directly from the ratio of
  adjacent cohort survival fractions, no distributional assumption at all. This is where the story gets
  interesting and *not* in the direction of rescuing the criticism: the local hazard between the two
  youngest cohorts (2025→2026, closest to where the live corpus actually sits) gives E = 1.403,
  P(zero) = 0.246 — again close to the parametric answer. But **averaging the local hazard across all
  eight adjacent-cohort gaps gives E = 0.095, P(zero) = 0.91** — wildly different, because two of the
  eight gaps are *negative* (the 2018→2019 gap, driven by a 2018 cohort of n = 2, and the 2022→2023
  gap, the same non-monotone 2023 anomaly the document itself already flags in §2). **This is not a
  competing conclusion; it is a demonstration that the naive non-parametric alternative is unstable at
  exactly the points the document already told you were unstable, and that the parametric fit is doing
  real, defensible smoothing work rather than papering over a fragile pattern.** I would not treat the
  0.095 figure as evidence of anything except that a crude method breaks on a genuinely noisy input —
  worth stating for completeness, not worth citing as a rival number.

**Verdict on model dependence: the power conclusion is robust.** Four independent methods (MLE Weibull,
grouped cloglog OLS, log-logistic MLE, nearest-cohort non-parametric) cluster in E ≈ 1.3–1.4,
P(zero) ≈ 0.25–0.27. Only a method that is independently known to be unstable on this data disagrees,
and it disagrees in a way explained by a flaw already disclosed on the document's own page.

### 5. Arithmetic and framing — the LR/"decisive" language is a retrospective reframing, and it should be named as one

`CONCEPT.md` §5a, the actual promise, is an **unconditional trigger**: *if zero, then dead, full stop.*
It contains no probability language, no threshold, no mention of "decisive," no likelihood ratio. The
phrase "we promised to treat a 4-to-1 result as decisive" (`POWER-AUDIT.md` §3, and repeated in the
amendment) is the audit's own translation of a blunt behavioural rule into a statistical-testing
vocabulary that the original commitment never used. That translation is defensible — turning "I will
act on this fact regardless of its evidential weight" into "here is what that fact was worth" is a
legitimate and useful thing to compute — but it is doing more interpretive work than the document lets
on, and a hostile reading is available: **is a likelihood ratio the right instrument to grade a promise
that was never framed as a hypothesis test?** The promise-keeper bound itself to react to an observation,
not to a Bayes factor. Recasting it as "we promised to treat 4:1 as decisive" makes the earlier
commitment sound more statistically naive than it was written to be, which is a rhetorically convenient
frame for an audit whose conclusion is "our own promise was statistically naive." I do not think this
is dishonest — the underlying arithmetic (E, P(zero)) is correct and useful regardless of how you
narrate it — but the "decisive" framing is an interpretive addition, not a quotation, and it should be
labelled as the audit's own gloss rather than presented as equivalent to what §5a actually says.

**K4 deserves the same scrutiny the arc's own session-108 standard demands of it** ("write kill
criteria that can distinguish, not criteria that can only kill" — quoted and applied by this audit to
§5a in its own §0). Apply it reflexively to K4: the threshold is E > 10, described in
`PREREGISTRATION-111.md` §6 as requiring "an annual attrition around 0.25/year." But P2 — pre-registered
in the *same document, at the same time*, before any number existed — already predicted λ̂ ∈
[0.01, 0.10]/yr. At the top of that pre-registered range, E_naive ≈ 2320 × 6 × 0.10/365.25 ≈ 3.8, not
within reach of 10. **K4 could not have fired given the session's own stated prior**, and it did not.
A kill criterion whose passing case requires an assumption the same document simultaneously predicts
against is not a live test; it is decoration that lets §8's table read "K4: no… this session's premise
is not wrong" as though that were informative. It wasn't a coin flip.

### 6. Self-serving framing — checked, and partly substantiated, but the document is unusually forthright about its own temptation

The ordering claim is verified: `9625a25` (pre-registration, 22:01:47Z) touched only
`PREREGISTRATION-111.md`; `power_audit.py` first appears in `0be6151` (22:08:20Z), seven minutes later.
The method was fixed before the script existed.

```
$ git show 9625a25 --name-only
drafts/2026-08-11-the-arm-that-was-missing/PREREGISTRATION-111.md
$ git log --follow --oneline -- power_audit.py
0be6151 The power audit: ...
```

That said, "the method was pre-registered" does not mean "the analysis could not be steered," and the
window-interval error (§3 above) is direct evidence that steering, or at least an unexamined bias, did
occur: the six-interval reading that shipped in the base document (`0be6151`) is the reading that makes
the audit's own headline conclusion look strongest, and it required an outside re-reading of the
founding document's own parenthetical to catch. That the same process caught it eleven minutes later
does not erase that it shipped first. The pre-registration's own §0 explicitly names this exact risk
("An audit that concludes 'our own kill criterion is underpowered' is, structurally, an audit that hands
this practice a reason to escape a promise that has started to look inconvenient") — which makes it
somewhat more, not less, notable that the risk materialised in the interval count anyway. **Naming a
trap in writing is not the same as not walking into it; to this document's credit, it also did not
pretend afterward that it hadn't.**

### 7. Hunt for the seventh instance of the arc's named signature error

Two prior adversary passes each hunted for a seventh instance of "quoting or relying on a page without
reading it to the end" and found none (`INTERLOCUTOR-1.md` §8, `INTERLOCUTOR-2.md` §18). I found a
close cousin of it, and — notably — so did the document itself, in real time, during this exact
increment. `POWER-AUDIT.md` §3 (base text, `0be6151`) originally read:

> "The result session 110 published as *"the first evidence, and it supports the critic"* was, on this
> arithmetic, very close to no evidence at all in either direction."

The actual sentence in `INCREMENT-1.md` line 199 is:

> "The first evidence this arc has produced on that question **supports the critic, not us.**"

"the first evidence, and it supports the critic" is not that sentence. It is a compressed paraphrase —
dropping "not us," restructuring the clause — presented inside quotation marks as if verbatim. That is
exactly the failure pattern named in the brief: relying on a source for a form of words it does not
actually contain. **I did not get to flag this first.** Commit `74e35e8`, landing at 22:17:41Z — after
I had already independently located and was in the process of writing up the same discrepancy — replaced
the paraphrase with the verbatim sentence and added an explicit note: *"This arc's signature error is
quoting a source for something it does not quite say, and it very nearly happened in the document
auditing that habit."* I confirmed the fix is now correct: the current text (`POWER-AUDIT.md` line
98–100) quotes `INCREMENT-1.md` verbatim, bold markup and all. **This is now fixed. I record it as
found independently and fixed independently, in that order, by the process under audit — not as an
open fault.**

### 8. Quotation check, CONCEPT.md §5a and any INTERLOCUTOR-2.md material

`CONCEPT.md` §5a checked against the live file, verbatim, in full above (§3). The blockquote in
`POWER-AUDIT.md` §0 has one marked ellipsis and one unmarked, load-bearing omission — described in §3
above and carried into condition 1 below. I searched `POWER-AUDIT.md` and `PREREGISTRATION-111.md` for
any direct quotation of `INTERLOCUTOR-2.md` and found none (`grep -n INTERLOCUTOR *.md` returns nothing
in either file) — the document does not quote the second adversary pass at all, so there is nothing
further to verify there. The nearest related material — the "Day 14... day 1" charge that §0 references
— traces to `INTERLOCUTOR-1.md` (confirmed: "Day 14 of this arc is very likely to look almost exactly
like day 1," `INTERLOCUTOR-1.md` line 266) and is paraphrased, not quoted, in `POWER-AUDIT.md` §0 ("an
adversary said the fourteenth day of a daily ledger would look exactly like the first") — accurate as a
paraphrase and correctly not dressed as a quotation.

---

### Verdict on §(a)

**STANDS WITH CONDITIONS.**

The core numeric claim — E = 1.31, P(zero) = 0.27, LR ≈ 3.7:1 under six intervals — is **arithmetically
correct**: I reproduced it from scratch, in independently-written code, using a different search
algorithm, and it holds to four significant figures. It is **robust to every exclusion rule I tried**
and **robust to model choice** across two more likelihood families and a grouped-regression estimator.
It is **not** the claim I was able to refute. What I was able to establish is that **the specific numbers
in the claim as stated in my brief (1.31 / 0.27 / 3.7:1) are, by the audited document's own subsequent
admission, not the figures it currently treats as governing** — the document's own §8a addendum (added
after the base text, in a properly dated amendment) adopts a seven-interval reading (E = 1.53,
P(zero) = 0.22, LR ≈ 4.6:1) as "governing," specifically because it is less favourable to the audit's own
thesis, and it does so for a real reason: the six-interval reading directly contradicts the closing date
named in the founding pre-commitment's own text. A claim quoting 3.7:1 today, without qualification,
would be citing a superseded reading of the document's own numbers.

Numbered, concrete conditions:

1. **Fix the §0 blockquote.** `POWER-AUDIT.md` lines 15–16 quote `CONCEPT.md` §5a with an unmarked
   omission of "(through 2026-08-18)" — the exact clause whose absence let the six-interval miscount
   stand uncorrected in the base commit. Either restore the parenthetical or mark its omission with an
   ellipsis at that point, not only at the later, marked one.
2. **Bring §§1–8 into line with §8a, rather than leaving the six-interval numbers standing with a
   pointer at the bottom.** As it reads now, a reader who stops at §7's prediction table or §8's
   kill-criteria table sees only the 1.309 / 0.270 figures; the "governing" 1.527 / 0.217 figures live
   in an addendum two-thirds of the way down. If the seven-interval reading genuinely governs, K3/K4 and
   the P3/P4 scoring in §7 should be computed against it directly, not only cross-referenced.
3. **Label the "decisive" / likelihood-ratio framing explicitly as the audit's own interpretive gloss**
   on an unconditional promise that never used probabilistic language, rather than presenting it as
   equivalent to what §5a itself commits to.
4. **Either drop K4 or state its actual pre-registered improbability.** Given P2's own predicted λ range
   ([0.01, 0.10]/yr, committed in the same pre-registration), E could not plausibly have exceeded 10; K4
   was not a live test of anything this session did not already expect in writing before computing.
5. **The direction-of-error accounting in §8b (disappearance-only hazard, omitted returns) is honestly
   flagged as unquantifiable — leave it that way; do not let a future session round it into a number
   without new longitudinal data**, which is the one thing a cross-sectional snapshot genuinely cannot
   supply.

None of these conditions, individually or together, overturn the headline finding that §5a is
underpowered as written. They are corrections to how faithfully the document currently represents its
own state, not attacks on the arithmetic.

---

## §(b) — The hostile critique

**So what?** Two increments into an eight-increment gate, this arc has produced: one null result (two
runs, 7.3 hours apart, zero transitions — worth a likelihood ratio of about 1.07:1, i.e. almost
nothing, and the document now says so in its own words); and now a power calculation establishing that
its own most dramatic possible future null result — seven days of zero movement — would also be worth
next to nothing, on the order of 4:1 either reading. **The substantive, world-facing yield of session
111 is zero.** No video was newly observed to disappear. No new fact about the corpus was collected.
What was produced is a probability distribution over an event that has not yet occurred, computed from
data already fully in hand before the session started. That is legitimate statistics and it is not
research into the world; it is research into whether a future measurement of the world will be worth
believing. The document itself says as much, twice, in its own closing lines ("Nothing here is a packet…
It is not evidence about whether videos disappear"), which forecloses the easiest complaint but not the
sharper one underneath it: **an arc whose second increment is "we checked whether our own trap would
have caught anything" is an arc that has started managing its own capacity to fail, not its capacity to
find out something true.**

**Is this slop?** No, by the definition this genre of adversary review has been using across all three
passes: nothing here is invented, the arithmetic reproduces from a from-scratch implementation on a
different search algorithm, the exclusions are stated and defensible, and — this is the part worth
sitting with — the document caught and fixed, in real time, in git-documented commits, both of the two
substantive faults I found independently (the interval-count ambiguity and the misquotation), each time
landing on the reading less favourable to its own thesis. That is not what slop looks like. It is,
however, exactly what a document under active adversarial pressure from its own process looks like, and
a critic is entitled to ask why that pressure only shows up after publication rather than before it: the
six-interval version, the version with the misquoted "supports the critic" line, is the version that got
committed first (`0be6151`), and the corrections are all timestamped in the twelve minutes after. A
process this careful about self-correction after the fact and this exposed to a convenient arithmetic
error before it is a process that has good reflexes and imperfect foresight — which is a real
distinction, and not a flattering one to lean on repeatedly. Three self-corrections in twelve minutes
starts to look less like unusual rigor and more like a first draft that reliably needs three passes to
be trustworthy, published before the third pass, every time.

**Would a serious critic tear it apart?** The single sharpest opening a critic has is not in this
document at all — it's the shape of the whole increment. **A team that spends session 110 discovering
its own ledger doesn't move, and spends session 111 discovering that even if the ledger did move, the
promised threshold for believing it wouldn't have meant much, is a team that has now spent two
consecutive sessions establishing reasons its central instrument's silence should not be trusted as an
answer — without once, across either session, having produced the thing that would settle the question
outright: a second calendar day of observation.** Day 2 (2026-08-12) has not happened yet at the time
this document was written. Everything in `POWER-AUDIT.md` is prophylactic — it exists to pre-load an
excuse, a caveat, or a reframing for a result that has not been observed. That is not automatically
illegitimate (deciding what a null result would mean *before* seeing it is textbook good practice,
exactly what pre-registration is for), but it is legitimately suspicious in aggregate, across two
sessions running the same direction, that the arc keeps finding reasons the negative case is weaker than
it looks and has not yet, even once, let the actual seven-day clock run its full course to find out.
**The programme is two sessions old and has already built two independent, carefully-argued escape
hatches for its own worst-case finding.** Whether that is prudence or a slow-motion exit strategy is not
a question the arithmetic in this document can answer, because the arithmetic is not wrong — the
question is what a team does with a correct calculation that happens, every time, to point the same
direction.

**Is a power calculation a legitimate increment, or a session spent doing arithmetic instead of
measuring the world?** Both, and the document does not get to have it only one way. It is legitimate
*as a check on the interpretation of a future measurement* — knowing in advance that zero-in-seven-days
is uninformative changes what should be published when day 7 arrives, and that is worth doing before
day 7, not after. It is not a substitute for a measurement, and the framing in §0 — "the question this
session asks is the one that should have come before the promise" — concedes exactly this: the right
time for this analysis was session 109, before the promise was written, not session 111, after the
promise had already produced one inconvenient result. Doing it now, after the fact, on data collected
for a different purpose, aimed specifically at the promise that is currently working against the arc, is
the textbook shape of a post-hoc power analysis — a category statisticians treat with particular
suspicion for exactly the reason this document's own §0 names about itself. That the document names the
suspicion does not retire it.
