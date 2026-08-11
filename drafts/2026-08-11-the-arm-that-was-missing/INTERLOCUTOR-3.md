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

---

## Appendix — the independent script, reproduced in full

Run with `python3 reimpl.py` from
`/home/user/field-research/drafts/2026-08-11-the-arm-that-was-missing/`. No numpy, no scipy (verified
absent on this machine). Does not import `power_audit.py`.

```python
#!/usr/bin/env python3
"""
INDEPENDENT re-implementation, written from scratch, NOT importing or calling power_audit.py.
Purpose: check every headline number in POWER-AUDIT.md against a from-scratch pipeline.
Pure standard library only (verified: no numpy, no scipy on this machine).

Run from: /home/user/field-research/drafts/2026-08-11-the-arm-that-was-missing/
"""
import json, math, time, calendar, random

RUN = "ledger/run-2026-08-11T1124Z.json"

# ---- 1. Load raw, independently ------------------------------------------------
d = json.load(open(RUN))
obs = d["observations"]
assert len(obs) == 2904, f"unexpected observation count: {len(obs)}"

T_REF = calendar.timegm((2026, 8, 11, 12, 0, 0, 0, 0, 0))
YEAR_S = 365.25 * 86400.0

def build(exclude_btrunc=True, exclude_indet=True, require19=True):
    rows = []
    excl = {"btrunc": 0, "indet": 0, "notdigit": 0, "nonpos": 0}
    for o in obs:
        if exclude_btrunc and o["arm"] == "B-truncated":
            excl["btrunc"] += 1
            continue
        if exclude_indet and o["state"] == "INDETERMINATE":
            excl["indet"] += 1
            continue
        vid = str(o["vid"])
        if require19 and len(vid) != 19:
            excl["notdigit"] += 1
            continue
        if not vid.isdigit():
            excl["notdigit"] += 1
            continue
        created = int(vid) >> 32
        age_s = T_REF - created
        if age_s <= 0:
            excl["nonpos"] += 1
            continue
        rows.append({
            "vid": vid, "arm": o["arm"],
            "alive": 1 if o["state"] == "RETRIEVABLE" else 0,
            "created": created, "age_y": age_s / YEAR_S,
        })
    return rows, excl

rows, excl = build()
print("=== BASELINE (matches PREREGISTRATION-111 exclusion rules) ===")
print("n analysed:", len(rows), "excluded:", excl)
live = sum(r["alive"] for r in rows)
print("retrievable:", live, "/", len(rows), "=", live/len(rows))
mean_age = sum(r["age_y"] for r in rows) / len(rows)
print("mean age (yr):", mean_age)

# ---- 2. Naive constant-hazard estimate -----------------------------------------
s_bar = live/len(rows)
lam_naive = -math.log(s_bar) / mean_age
print("naive lambda/yr:", lam_naive)

# ---- 3. Weibull MLE, written independently (Nelder-Mead-ish coordinate search) --
def negloglik(lam, k, rows):
    if lam <= 0 or k <= 0:
        return 1e18
    ll = 0.0
    for r in rows:
        x = (lam * r["age_y"]) ** k
        if x > 700: x = 700.0
        if r["alive"]:
            ll -= x
        else:
            if x < 1e-12:
                return 1e18
            ll += math.log1p(-math.exp(-x)) if x < 30 else 0.0
    return -ll

def fit_lambda_ternary(rows, k, lo=1e-6, hi=10.0, iters=200):
    # ternary search in log-lambda space (independent implementation of the same idea,
    # written without reference to power_audit.py's golden-section code)
    a, b = math.log(lo), math.log(hi)
    for _ in range(iters):
        m1 = a + (b - a) / 3
        m2 = b - (b - a) / 3
        f1 = negloglik(math.exp(m1), k, rows)
        f2 = negloglik(math.exp(m2), k, rows)
        if f1 < f2:
            b = m2
        else:
            a = m1
        if b - a < 1e-10:
            break
    lam = math.exp((a + b) / 2)
    return lam, negloglik(lam, k, rows)

def full_fit(rows, k_lo=0.05, k_hi=6.0, steps=2000):
    best = None
    curve = []
    for i in range(steps + 1):
        k = math.exp(math.log(k_lo) + (math.log(k_hi) - math.log(k_lo)) * i / steps)
        lam, nll = fit_lambda_ternary(rows, k)
        curve.append((k, lam, -nll))
        if best is None or -nll > best[2]:
            best = (k, lam, -nll)
    return best, curve

best, curve = full_fit(rows)
k_hat, lam_hat, ll_hat = best
print("Weibull MLE (independent fit): k =", k_hat, " lambda =", lam_hat, " loglik =", ll_hat)

def profile_ci(curve, best, crit=3.841458821):
    thr = best[2] - crit / 2
    ks = [k for (k, _, ll) in curve if ll >= thr]
    return (min(ks), max(ks)) if ks else (None, None)

klo, khi = profile_ci(curve, best)
print("profile-likelihood 95% CI on k:", (klo, khi))

# ---- 4. Power: expected transitions and P(zero), independent formula -----------
def hazard_per_day(lam, k, t_y):
    return k * (lam ** k) * (t_y ** (k - 1)) / 365.25

def expected_transitions(rows, lam, k, days=6):
    return sum(days * hazard_per_day(lam, k, r["age_y"]) for r in rows if r["alive"])

e_fit = expected_transitions(rows, lam_hat, k_hat, days=6)
p_zero_fit = math.exp(-e_fit)
print("E[transitions] fitted (D=6):", e_fit, " P(zero) Poisson approx:", p_zero_fit)

e_naive = live * 6 * lam_naive / 365.25
print("E[transitions] naive (D=6):", e_naive, " P(zero):", math.exp(-e_naive))

lr = p_zero_fit / 1.0  # LR of zero-transitions under implied-rate world vs world of literal zero risk
print("Likelihood ratio (P(zero|world A=fitted) : P(zero|world B=never disappears)) = %.3f : 1" % (1/p_zero_fit))

# ---- 5. EXACT (non-Poisson-approximated) P(zero), independent check ------------
def exact_p_zero(rows, lam, k, days=6):
    """Product over currently-retrievable identifiers of the exact conditional
    survival probability over the window, using the Weibull cumulative hazard,
    NOT the small-p Poisson shortcut."""
    delta_y = days / 365.25
    logp = 0.0
    for r in rows:
        if not r["alive"]:
            continue
        t0 = r["age_y"]
        t1 = t0 + delta_y
        H0 = (lam * t0) ** k
        H1 = (lam * t1) ** k
        # conditional survival prob = exp(-(H1-H0))
        logp += -(H1 - H0)
    return math.exp(logp)

p_zero_exact = exact_p_zero(rows, lam_hat, k_hat, days=6)
print("EXACT P(zero), D=6 (no Poisson approx):", p_zero_exact, " vs Poisson-approx:", p_zero_fit,
      " diff:", p_zero_exact - p_zero_fit)

# ---- 6. D=7 sensitivity: the calendar-date check --------------------------------
e_fit_7 = expected_transitions(rows, lam_hat, k_hat, days=7)
p_zero_7 = math.exp(-e_fit_7)
print("\n--- If the window is 7 intervals (CONCEPT.md's literal 'through 2026-08-18') ---")
print("E[transitions] fitted (D=7):", e_fit_7, " P(zero):", p_zero_7,
      " LR:", 1/p_zero_7)

# ---- 7. Sensitivity to exclusion rules ------------------------------------------
print("\n=== EXCLUSION SENSITIVITY ===")
def summarize(rows, label):
    live = sum(r["alive"] for r in rows)
    mean_age = sum(r["age_y"] for r in rows) / len(rows)
    s_bar = live / len(rows)
    lam_naive = -math.log(s_bar) / mean_age
    best, curve = full_fit(rows, steps=600)
    k_hat, lam_hat, ll = best
    e = expected_transitions(rows, lam_hat, k_hat, days=6)
    print(f"{label}: n={len(rows)} live={live} frac={s_bar:.4f} k={k_hat:.4f} lam={lam_hat:.5f} "
          f"E={e:.4f} P0={math.exp(-e):.4f}")

# (a) baseline
summarize(rows, "baseline (as preregistered)")

# (b) include B-truncated as alive/dead like everything else (do NOT drop it)
rows_bt, _ = build(exclude_btrunc=False)
summarize(rows_bt, "include B-truncated")

# (c) treat INDETERMINATE as NOT-RETRIEVABLE (worst case) instead of excluding
def build_indet_as_dead():
    rows = []
    for o in obs:
        if o["arm"] == "B-truncated":
            continue
        vid = str(o["vid"])
        if len(vid) != 19:
            continue
        created = int(vid) >> 32
        age_s = T_REF - created
        if age_s <= 0:
            continue
        alive = 1 if o["state"] == "RETRIEVABLE" else 0  # INDETERMINATE -> 0
        rows.append({"vid": vid, "arm": o["arm"], "alive": alive,
                     "created": created, "age_y": age_s / YEAR_S})
    return rows
rows_indet_dead = build_indet_as_dead()
summarize(rows_indet_dead, "INDETERMINATE counted as dead")

# (d) treat INDETERMINATE as RETRIEVABLE (best case)
def build_indet_as_alive():
    rows = []
    for o in obs:
        if o["arm"] == "B-truncated":
            continue
        vid = str(o["vid"])
        if len(vid) != 19:
            continue
        created = int(vid) >> 32
        age_s = T_REF - created
        if age_s <= 0:
            continue
        alive = 1 if o["state"] in ("RETRIEVABLE", "INDETERMINATE") else 0
        rows.append({"vid": vid, "arm": o["arm"], "alive": alive,
                     "created": created, "age_y": age_s / YEAR_S})
    return rows
rows_indet_alive = build_indet_as_alive()
summarize(rows_indet_alive, "INDETERMINATE counted as alive")

# (e) relax digit-length filter to >=17 digits (include the 4 excluded 18-digit rows
#     using the SAME >>32 rule, to see whether they behave as outliers)
def build_relaxed():
    rows = []
    for o in obs:
        if o["arm"] == "B-truncated":
            continue
        if o["state"] == "INDETERMINATE":
            continue
        vid = str(o["vid"])
        if len(vid) < 17 or not vid.isdigit():
            continue
        created = int(vid) >> 32
        age_s = T_REF - created
        if age_s <= 0:
            continue
        rows.append({"vid": vid, "arm": o["arm"],
                     "alive": 1 if o["state"] == "RETRIEVABLE" else 0,
                     "created": created, "age_y": age_s / YEAR_S})
    return rows
rows_relaxed = build_relaxed()
summarize(rows_relaxed, "17+ digit ids (includes the 4 excluded 18-digit rows)")

# show what those 4 rows decode to under the >>32 rule, and whether the years are sane
print("\nthe 4 excluded 18-digit rows, decoded anyway:")
for o in obs:
    vid = str(o["vid"])
    if o["arm"] != "B-truncated" and o["state"] != "INDETERMINATE" and len(vid) == 18:
        created = int(vid) >> 32
        try:
            y = time.gmtime(created).tm_year
        except Exception:
            y = "ERR"
        print(f"  vid={vid} state={o['state']} decoded_year={y} created_epoch={created}")

# ---- 8. Non-parametric cohort read-off: independent, no Weibull at all ---------
print("\n=== NON-PARAMETRIC COHORT MODEL (no distributional assumption) ===")
def year_of(r):
    return time.gmtime(r["created"]).tm_year

cohorts = {}
for r in rows:
    y = year_of(r)
    c = cohorts.setdefault(y, [0, 0])
    c[0] += 1
    c[1] += r["alive"]

years = sorted(cohorts)
print("cohort fractions:", {y: round(cohorts[y][1]/cohorts[y][0], 4) for y in years})

# Estimate a "local" annual hazard between adjacent cohorts by comparing survival
# fractions at consecutive mean ages, converting to a hazard via -ln(S2/S1)/dt.
# This treats the cross-sectional fractions as a rough survival curve without
# fitting any parametric form - a genuine alternative model.
mean_age_by_year = {}
for r in rows:
    mean_age_by_year.setdefault(year_of(r), []).append(r["age_y"])
mean_age_by_year = {y: sum(v)/len(v) for y, v in mean_age_by_year.items()}

# order oldest (largest age) to youngest (smallest age): survival should increase
# as age decreases (S(older) <= S(younger)) in this cross-sectional reading
ordered = sorted(years, key=lambda y: -mean_age_by_year[y])
print("ordered oldest->youngest:", ordered)
local_hazards = []
for i in range(len(ordered) - 1):
    y_old, y_new = ordered[i], ordered[i+1]
    s_old = cohorts[y_old][1] / cohorts[y_old][0]
    s_new = cohorts[y_new][1] / cohorts[y_new][0]
    dt = mean_age_by_year[y_new] - mean_age_by_year[y_old]  # negative age gap -> positive dt going younger->older is reversed
    dt = mean_age_by_year[y_old] - mean_age_by_year[y_new]
    if dt <= 0 or s_old <= 0 or s_new <= 0:
        continue
    # local hazard rate estimate: -(ln(s_old) - ln(s_new)) / dt   [per year], read off
    # directly from the cross-sectional curve, no Weibull
    h_local = -(math.log(s_old) - math.log(s_new)) / dt
    local_hazards.append((y_old, y_new, dt, h_local))
    print(f"  between {y_old} (age {mean_age_by_year[y_old]:.2f}) and {y_new} "
          f"(age {mean_age_by_year[y_new]:.2f}): local hazard = {h_local:.5f}/yr")

# apply the *youngest-interval* local hazard (closest to where the live corpus
# actually sits) as a constant-hazard estimate for the power calc, as a fully
# nonparametric alternative to the Weibull fit
if local_hazards:
    h_last = local_hazards[-1][3]
    e_nonparam = live * 6 * h_last / 365.25
    print(f"\nnonparametric constant-hazard-from-youngest-gap: h={h_last:.5f}/yr  "
          f"E(D=6)={e_nonparam:.4f}  P(zero)={math.exp(-e_nonparam):.4f}")
    # average over all local hazards too
    h_avg = sum(h for (_,_,_,h) in local_hazards) / len(local_hazards)
    e_nonparam2 = live * 6 * h_avg / 365.25
    print(f"nonparametric constant-hazard-from-average-of-gaps: h={h_avg:.5f}/yr  "
          f"E(D=6)={e_nonparam2:.4f}  P(zero)={math.exp(-e_nonparam2):.4f}")

# ---- 9. Discrete-time cloglog / logistic model on cohort data, own IRLS --------
print("\n=== DISCRETE-TIME CLOGLOG (Weibull-equivalent discrete model), own fit ===")
# For grouped/binary data with covariate = ln(age), a cloglog link
#   cloglog(1-S) = ln(-ln(S)) = k*ln(lambda) + k*ln(age)
# is the exact discrete-time equivalent of a Weibull proportional-hazards model.
# Fit ln(-ln(fraction_alive)) ~ a + b*ln(age) by ordinary least squares on the
# COHORT MEANS (not individual rows) - a genuinely different estimation method
# (group-level OLS instead of individual-level MLE) as a robustness check.
xs, ys, ns = [], [], []
for y in years:
    n, a = cohorts[y]
    if n < 20:
        continue
    frac = a / n
    if frac <= 0 or frac >= 1:
        continue
    age = mean_age_by_year[y]
    xs.append(math.log(age))
    ys.append(math.log(-math.log(frac)))
    ns.append(n)

# weighted least squares (weight = n) fit of ys = A + B*xs
W = sum(ns)
xbar = sum(n*x for n,x in zip(ns,xs))/W
ybar = sum(n*y for n,y in zip(ns,ys))/W
Sxx = sum(n*(x-xbar)**2 for n,x in zip(ns,xs))
Sxy = sum(n*(x-xbar)*(y-ybar) for n,x,y in zip(ns,xs,ys))
B = Sxy/Sxx
A = ybar - B*xbar
k_cloglog = B
lam_cloglog = math.exp(A / k_cloglog) if k_cloglog != 0 else None
print(f"cloglog-OLS-on-cohorts: k={k_cloglog:.4f}  lambda={lam_cloglog:.5f}/yr  (cf. MLE k={k_hat:.4f} lambda={lam_hat:.5f})")
e_cloglog = expected_transitions(rows, lam_cloglog, k_cloglog, days=6)
print(f"E(D=6) under cloglog-OLS fit: {e_cloglog:.4f}  P(zero)={math.exp(-e_cloglog):.4f}")

# ---- 10. Log-logistic alternative model, own MLE --------------------------------
print("\n=== LOG-LOGISTIC ALTERNATIVE MODEL, own MLE ===")
# S(t) = 1 / (1 + (t/alpha)^beta)
def negloglik_loglogistic(alpha, beta, rows):
    if alpha <= 0 or beta <= 0:
        return 1e18
    ll = 0.0
    for r in rows:
        t = r["age_y"]
        x = (t/alpha)**beta
        S = 1.0/(1.0+x)
        if r["alive"]:
            if S <= 0: return 1e18
            ll += math.log(S)
        else:
            F = 1.0 - S
            if F <= 1e-300: return 1e18
            ll += math.log(F)
    return -ll

def fit_loglogistic(rows, beta_lo=0.1, beta_hi=6.0, steps=800):
    best = None
    for i in range(steps+1):
        beta = math.exp(math.log(beta_lo) + (math.log(beta_hi)-math.log(beta_lo))*i/steps)
        # for fixed beta, find alpha by ternary search
        a, b = math.log(0.01), math.log(1000.0)
        for _ in range(150):
            m1 = a + (b-a)/3
            m2 = b - (b-a)/3
            f1 = negloglik_loglogistic(math.exp(m1), beta, rows)
            f2 = negloglik_loglogistic(math.exp(m2), beta, rows)
            if f1 < f2: b = m2
            else: a = m1
            if b-a < 1e-9: break
        alpha = math.exp((a+b)/2)
        nll = negloglik_loglogistic(alpha, beta, rows)
        if best is None or nll < best[2]:
            best = (alpha, beta, nll)
    return best

alpha_hat, beta_hat, nll_ll = fit_loglogistic(rows)
print(f"log-logistic MLE: alpha(median life)={alpha_hat:.3f}yr  beta={beta_hat:.4f}  loglik={-nll_ll:.3f}")
print(f"(compare Weibull loglik={ll_hat:.3f} -- higher loglik = better fit, same # of params)")

def hazard_loglogistic_per_day(alpha, beta, t):
    # h(t) = (beta/alpha)*(t/alpha)^(beta-1) / (1+(t/alpha)^beta), per year -> per day
    x = (t/alpha)**(beta-1)
    denom = 1 + (t/alpha)**beta
    h_year = (beta/alpha) * x / denom
    return h_year/365.25

def expected_transitions_loglogistic(rows, alpha, beta, days=6):
    return sum(days*hazard_loglogistic_per_day(alpha, beta, r["age_y"]) for r in rows if r["alive"])

e_ll = expected_transitions_loglogistic(rows, alpha_hat, beta_hat, days=6)
print(f"E(D=6) under log-logistic fit: {e_ll:.4f}  P(zero)={math.exp(-e_ll):.4f}")

print("\n=== SUMMARY TABLE ===")
print(f"{'model':35s} {'E(D=6)':>10s} {'P(zero)':>10s}")
print(f"{'Weibull MLE (as published)':35s} {e_fit:10.4f} {p_zero_fit:10.4f}")
print(f"{'Weibull MLE, D=7':35s} {e_fit_7:10.4f} {p_zero_7:10.4f}")
print(f"{'naive constant hazard':35s} {e_naive:10.4f} {math.exp(-e_naive):10.4f}")
print(f"{'nonparametric (youngest gap)':35s} {e_nonparam:10.4f} {math.exp(-e_nonparam):10.4f}")
print(f"{'nonparametric (avg of gaps)':35s} {e_nonparam2:10.4f} {math.exp(-e_nonparam2):10.4f}")
print(f"{'cloglog-OLS on cohorts':35s} {e_cloglog:10.4f} {math.exp(-e_cloglog):10.4f}")
print(f"{'log-logistic MLE':35s} {e_ll:10.4f} {math.exp(-e_ll):10.4f}")
```

**Full stdout from the run cited throughout this report:**

```
=== BASELINE (matches PREREGISTRATION-111 exclusion rules) ===
n analysed: 2618 excluded: {'btrunc': 249, 'indet': 33, 'notdigit': 4, 'nonpos': 0}
retrievable: 2320 / 2618 = 0.8861726508785333
mean age (yr): 2.8796361378641837
naive lambda/yr: 0.041964844176153024
Weibull MLE (independent fit): k = 0.695856502117081  lambda = 0.01787172521419502  loglik = -899.2759988840289
profile-likelihood 95% CI on k: (0.5012977718809741, 0.8989921227497276)
E[transitions] fitted (D=6): 1.309048530036077  P(zero) Poisson approx: 0.27007690423613195
E[transitions] naive (D=6): 1.5993172647010272  P(zero): 0.20203440693969896
Likelihood ratio (P(zero|world A=fitted) : P(zero|world B=never disappears)) = 3.703 : 1
EXACT P(zero), D=6 (no Poisson approx): 0.271143712681605  vs Poisson-approx: 0.27007690423613195  diff: 0.001066808445473022

--- If the window is 7 intervals (CONCEPT.md's literal 'through 2026-08-18') ---
E[transitions] fitted (D=7): 1.5272232850420893  P(zero): 0.21713776067633217  LR: 4.605371248580806

=== EXCLUSION SENSITIVITY ===
baseline (as preregistered): n=2618 live=2320 frac=0.8862 k=0.6959 lam=0.01787 E=1.3090 P0=0.2701
include B-truncated: n=2618 live=2320 frac=0.8862 k=0.6959 lam=0.01787 E=1.3090 P0=0.2701
INDETERMINATE counted as dead: n=2651 live=2320 frac=0.8751 k=0.6581 lam=0.01756 E=1.3959 P0=0.2476
INDETERMINATE counted as alive: n=2651 live=2353 frac=0.8876 k=0.6903 lam=0.01710 E=1.3007 P0=0.2723
17+ digit ids (includes the 4 excluded 18-digit rows): n=2622 live=2321 frac=0.8852 k=0.7127 lam=0.01920 E=1.3315 P0=0.2641

the 4 excluded 18-digit rows, decoded anyway:
  vid=194951213564514304 state=RETRIEVABLE decoded_year=1971 created_epoch=45390616
  vid=677767122007582643 state=NOT-RETRIEVABLE decoded_year=1975 created_epoch=157804955
  vid=726459750741134635 state=NOT-RETRIEVABLE decoded_year=1975 created_epoch=169142091
  vid=740580884959830349 state=NOT-RETRIEVABLE decoded_year=1975 created_epoch=172429924

=== NON-PARAMETRIC COHORT MODEL (no distributional assumption) ===
cohort fractions: {2018: 1.0, 2019: 0.7241, 2020: 0.8154, 2021: 0.8514, 2022: 0.8568, 2023: 0.8484, 2024: 0.9124, 2025: 0.9412, 2026: 0.9695}
ordered oldest->youngest: [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
  between 2018 (age 8.15) and 2019 (age 7.01): local hazard = -0.28313/yr
  between 2019 (age 7.01) and 2020 (age 6.02): local hazard = 0.11905/yr
  between 2020 (age 6.02) and 2021 (age 5.08): local hazard = 0.04628/yr
  between 2021 (age 5.08) and 2022 (age 4.10): local hazard = 0.00643/yr
  between 2022 (age 4.10) and 2023 (age 3.11): local hazard = -0.00993/yr
  between 2023 (age 3.11) and 2024 (age 2.11): local hazard = 0.07214/yr
  between 2024 (age 2.11) and 2025 (age 1.15): local hazard = 0.03235/yr
  between 2025 (age 1.15) and 2026 (age 0.34): local hazard = 0.03680/yr

nonparametric constant-hazard-from-youngest-gap: h=0.03680/yr  E(D=6)=1.4026  P(zero)=0.2460
nonparametric constant-hazard-from-average-of-gaps: h=0.00250/yr  E(D=6)=0.0952  P(zero)=0.9092

=== DISCRETE-TIME CLOGLOG (Weibull-equivalent discrete model), own fit ===
cloglog-OLS-on-cohorts: k=0.7066  lambda=0.01842/yr  (cf. MLE k=0.6959 lambda=0.01787)
E(D=6) under cloglog-OLS fit: 1.3082  P(zero)=0.2703

=== LOG-LOGISTIC ALTERNATIVE MODEL, own MLE ===
log-logistic MLE: alpha(median life)=43.324yr  beta=0.7360  loglik=-899.253
(compare Weibull loglik=-899.276 -- higher loglik = better fit, same # of params)
E(D=6) under log-logistic fit: 1.3076  P(zero)=0.2705

=== SUMMARY TABLE ===
model                                   E(D=6)    P(zero)
Weibull MLE (as published)              1.3090     0.2701
Weibull MLE, D=7                        1.5272     0.2171
naive constant hazard                   1.5993     0.2020
nonparametric (youngest gap)            1.4026     0.2460
nonparametric (avg of gaps)             0.0952     0.9092
cloglog-OLS on cohorts                  1.3082     0.2703
log-logistic MLE                        1.3076     0.2705
```

Additionally, the independent verification of `POWER-AUDIT.md` §4a's age-band hazard table (added in
commit `38c47af`, the last commit touching `POWER-AUDIT.md` before this report was finished), computed
from the same rows using the fitted k, λ from the run above and no other code path:

```
$ python3 -c "... (age-band grouping, shown inline) ..."
0 1 n= 323 mean_hazard= 0.00014784730656517043
1 2 n= 503 mean_hazard= 0.0001033926171710801
2 3 n= 512 mean_hazard= 8.792973320907603e-05
3 5 n= 733 mean_hazard= 7.69968687587734e-05
5 99 n= 249 mean_hazard= 6.809174668455889e-05
corpus mean hazard 9.40408360281409e-05 live 2320
```

Matches `power-audit-age-enrichment.json` exactly. The document's derived ratios (1.88× at three
months, 0.68× at seven years, 2.76×≈"2.8×" between them) were independently recomputed from the
continuous hazard function at those exact ages and also match:

```
t=0.25: 1.8770864038914046
t=7:    0.6813034033302724
ratio:  2.7551402131796747
```


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
