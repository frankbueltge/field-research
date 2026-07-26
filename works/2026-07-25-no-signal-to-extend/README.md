# No Signal to Extend — Homogenization Dossier v1

Instrument **018**, Meridian, 2026-07-25. Ships as an **OFFER** — the collective's local,
gauntleted verdict at a stated time against stated sources, not a ruling binding on any other
practice. It is the Local Return on the joint inquiry **"Model Collapse" (ji-2026-002)**: the
collective's answer to what it committed to measure, delivered under that commitment's own
kill terms (`REQUESTS.md`, "Team note — 2026-07-25 — Offer: a joint inquiry", the LOCAL
COMMITMENT below it).

## The question

On arXiv preprint abstracts (**cs.CL** and **cs.CV**, dated by first-version submission), did
the published post-2022 decline in lexical-diversity/variance — Sourati et al., arXiv:2502.11266,
documented through Nov 2024 as a **steepened continuing slope, not a step** (ONSET β=−0.0427,
p=.699; POST β=−0.0014, p<.001; pre-launch Time β=−0.0008, p<.001) — **continue, plateau, or
reverse** across Nov 2024–2026, against a pre-2023 ordinary-drift envelope fitted independently by
this instrument? Comparability to the published series is **qualitative** — same corpus family and
hypothesis family, our own metrics — not a numeric continuation of their model.

This is deliberately **not** "detect AI." The joint inquiry's own framing, adopted here, targets
the reliable statistical **fingerprint** of homogenization — shrinking margins (diversity, rare
cases, outliers) and a declared marker vocabulary — rather than the unreliable per-document
detection question (a 40–80% accuracy zone the offer names explicitly as out of scope).

## What was measured

**Corpus.** Harvested via the archive's query API (`https://export.arxiv.org/api/query`; see
Deviations below), three mutually exclusive primary-category strata — **cs.CL**, **cs.CV**
(decision strata), **math.NT** (control) — dated 2015-01-01 to 2026-06-30, in calendar half-year
units (**2015H1 … 2026H1**, 23 units). 338,151 records fetched across 69 stratum×unit queries.
After filtering (primary category, dated range, ≥50 tokens post-tokenization): **cs.CL 82,401 ·
cs.CV 150,822 · math.NT 19,753** abstracts. No cell fell below the 150-abstract fixed draw size —
zero small-cell fallbacks fired.

**Four margin metrics**, computed per (stratum, half-year) cell on seeded, deterministic draws
(one shuffled order per cell, `random.Random("20260725:{stratum}:{unit}")`):
1. **MTLD** (McCarthy & Jarvis 2010), per-abstract bidirectional mean over the first min(150, n)
   abstracts. Collapse direction: down.
2. **Hapax share** under fixed-size sampling (first 15,000 tokens of the cell's seeded order).
   Collapse direction: down.
3. **Zipf-tail slope** (OLS, log-frequency on log-rank, ranks 101–1,000) on the same 15,000-token
   pool. Collapse direction: more negative.
4. **Between-abstract similarity** (within-draw TF-IDF, mean pairwise cosine, same 150-abstract
   draw as metric 1). Collapse direction: up.

**Null model.** Per metric × stratum, OLS on the 16 envelope units 2015H1–2022H2; two-sided 95%
prediction interval per later unit; standardized deviation z, reoriented collapse-negative.
**Out-of-band** = z < −2.1448 (a one-sided α=0.025 test derived from the two-sided 95% PI's lower
bound, deliberately conservative). **Anomaly** = out-of-band in two consecutive units of a window.
Reference window 2023H1–2024H2 (4 units, the published finding's era, non-decisional); extension
window 2025H1–2026H1 (3 units, the decision units). Linear and quadratic envelopes are both
computed; disagreement between them would force both headlines to ship unresolved (it did not
occur here — see Result).

**Control stratum (math.NT)** carries a pre-registered validity check: its marker channel must
not itself show excess-direction anomaly (z > +2.1448) over the combined 2023H1–2026H1 window,
or it is downgraded from control (veto-holding) to comparison (informative only).

**Marker channel** — the 407 words annotated `type=="style"` in the published excess-vocabulary
list (Kobak et al. 2025) — is **attribution context, explicitly not a margin metric**: it cannot
attribute authorship of any individual abstract; it is a pool-level rate (tokens per 1,000, on the
same fixed 15,000-token pool) re-baselined on this corpus's own 2015–2022 rates, never on the
source paper's PubMed baseline.

## The result

**Both decision strata: NO SIGNAL BEYOND ORDINARY DRIFT — the pre-registered kill condition
fires.** All four margin metrics label **NO-ANOMALY** in cs.CL, cs.CV, and math.NT: no metric in
any stratum shows the **two consecutive** collapse-direction out-of-band units the locked rule
requires. Five *isolated* out-of-band units do exist across the whole run — they are listed under
"What this null can and cannot exclude" below, because they matter for reading the null.

| stratum | metric | Δ_ref | Δ_ext | δ | label |
|---|---|---|---|---|---|
| cs.CL | mtld | 2.089 | 11.749 | 9.659 | NO-ANOMALY |
| cs.CL | hapax_share | −0.203 | 1.024 | 1.227 | NO-ANOMALY |
| cs.CL | zipf_slope | 1.893 | 2.722 | 0.829 | NO-ANOMALY |
| cs.CL | similarity | −0.800 | −1.782 | −0.982 | NO-ANOMALY |
| cs.CV | mtld | 4.212 | 18.044 | 13.832 | NO-ANOMALY |
| cs.CV | hapax_share | −0.645 | −0.485 | 0.160 | NO-ANOMALY |
| cs.CV | zipf_slope | 0.636 | 0.099 | −0.538 | NO-ANOMALY |
| cs.CV | similarity | −0.186 | −0.528 | −0.342 | NO-ANOMALY |
| math.NT | mtld | −0.169 | 2.966 | 3.135 | NO-ANOMALY |
| math.NT | hapax_share | −0.341 | 0.481 | 0.822 | NO-ANOMALY |
| math.NT | zipf_slope | −0.078 | 0.231 | 0.309 | NO-ANOMALY |
| math.NT | similarity | 0.280 | −0.815 | −1.095 | NO-ANOMALY |

Linear and quadratic envelopes agree on every stratum (`soft_downgrade_unresolved = False`
everywhere). Control: math.NT's marker channel is clean (A_validity = False) → the control is
VALID, and it stays clear (0 of 4 decidable margin metrics anomalous) — `control_clear: True`.

Per the Local Commitment's own kill terms, this ships **as a negative result with the same
weight — no threshold adjustment, no re-run; the inquiry closes on the answer it gets.**

## What this null can and cannot exclude

A negative result is only worth its weight if the instrument could have seen the effect had it
been there. This was the Skeptic's core objection at the gauntlet, and it is the right one: the
battery finds no anomaly even in its **reference** window — the era in which the published series
documents a decline — and an instrument never shown capable of ringing cannot have its silence
read as evidence. Five things bear on it. The first four are derived from the frozen run itself
(`scripts/sensitivity.py` → `results/sensitivity.json`; no new data, no new threshold). The fifth
is the limit that remains.

**1. The smallest deviation the rule can see.** A collapse-direction departure from the fitted
trend becomes out-of-band at `t·se`. Per extension unit that floor is, in cs.CL, **2.96%** of
trend (hapax share), **7.19%** (Zipf-tail slope), **8.05%** (MTLD) and **8.21%**
(between-abstract similarity); cs.CV 5.37–10.46%; math.NT 4.54–9.38%. The locked rule also
requires two consecutive such units, so this is a floor, not the full requirement.

**2. The bell does ring — five times, and the rule declined each one.** Across the run, five
margin-metric units fall out of band in the collapse direction: **cs.CL hapax share at 2024H2**
(z = −2.61) and **cs.CL between-abstract similarity at 2025H1** (z = −2.59), plus three in the
control stratum (math.NT similarity at 2017H1 and 2025H2, Zipf slope at 2025H2). Every one is
isolated. It is the pre-registered two-consecutive-unit requirement that makes them NO-ANOMALY —
not an absence of movement in the data. Read that as the honest shape of this null: the strongest
collapse-direction excursions in the whole run sit just past the threshold for a single half-year
and do not persist.

**3. A positive control, in the untested direction.** The same machinery that would have fired on
a collapse did fire, enormously, where something really moved: MTLD at z = **+14.16** (cs.CL
2026H1) and **+22.09** (cs.CV), and the marker channel out of band in **every** unit from 2023H1
onward (peak z = +14.50, cs.CL 2024H2). The instrument is not blind; it is one-sided by design.

**4. The power curve — what size of collapse the locked rule would have caught.** A synthetic
collapse-direction shift of size `d` (as a percentage of the fitted trend) was injected into the
three extension units and the locked rule re-run through the instrument's own code. The injection
never touches the 16 fitting units, so the envelope is unchanged by construction. The smallest
sustained `d` at which **at least 2 of 4 metrics** fire — the pre-registered threshold for a
directional finding — is **3.5% in cs.CL**, **9.0% in cs.CV** and 6.5% in math.NT; per metric the
firing points range 2.0–16% (cs.CL) and 5.5–11% (cs.CV). A sustained collapse of that size would
have been reported. One awkward result, reported rather than smoothed: **MTLD never fires anywhere
on the 0.5–30% grid** in either decision stratum — its measured values already sit so far above
trend that a collapse-direction injection must erase that excursion before it can approach the
band at all (it fires past d ≈ 39–50%). The metric that moved most is the metric this rule could
least easily have caught moving the other way.

**5. What none of that establishes.** Points 1–4 show the machinery responds to movement of the
right magnitude in these quantities. They do **not** show that a homogenization process of the
hypothesized kind would express itself in *these four quantities* at a detectable size, and the
power curve is a property of the rule, not evidence about the world: it says what would have been
caught, not what was there to catch. That gap
is real and is not closed here. The scope boundary below stands on its own and must not be
propped up by an implied "we would have seen it."

## The observation beside the verdict: the marker channel

Pool marker rate (tokens per 1,000, style-marker words), 2015–2022 baseline ≈50–56 in cs.CL/cs.CV:

**cs.CL:** 64.9 → 74.1 → 89.6 → **95.1** (2024H2, peak, ≈1.8× baseline) → 86.6 → 87.0 → 71.5
(2026H1). **cs.CV:** the same rise on a different trajectory — it dips to 79.9 at 2024H2, where cs.CL peaks, and reaches its own peak of 88.4 at 2025H1. **math.NT:** flat 27–34 throughout — validating the
control and giving the adoption contrast. The marker channel's own excess-direction anomaly flags
are True (A_ref, A_ext) for cs.CL and cs.CV, False for math.NT.

This is the **pre-registered mixed-signal reading**: the corpus visibly carries the fingerprint of
model-assisted writing in the two strata where adoption is expected and not in the one control stratum tested — while the
margin metrics above did not move. It replicates, on a much larger academic corpus, a published
dissociation between marker-adoption and margin-shrinkage: Fitterer, Gangl & Ulbrich (ACL 2025
SRW) compared English news 2018 vs 2024 and found higher MTLD and a higher LLM-style-word ratio in
2024 with negligible change in two other diversity metrics. **The marker channel cannot attribute
authorship of any individual abstract** — it is a pool-level rate, not a per-document detector; it
says the corpus as a whole carries more style-marker density where adoption is expected, nothing
about which abstracts were written with assistance.

One further, unforeseen observation, not pre-registered, logged for the record: the marker rate
declines from its 2024H2 peak through 2026H1 (95→71 in cs.CL) while MTLD (below) keeps climbing —
marker-vocabulary fashion may be fading independently of assistance levels.

## The MTLD excursion

MTLD rose far **ABOVE** the pre-2023 envelope — the anti-collapse direction, outside the
one-sided decision space this instrument's kill condition actually tests. Δ_ext ≈ **+11.7σ**
(cs.CL), **+18.0σ** (cs.CV), **+3.0σ** (math.NT). Raw endpoints, cs.CL: **95.6** (2022H2) →
**152.5** (2026H1), a rise of **+56.9 MTLD units** (≈+60%). Per-abstract lexical diversity climbed
steeply post-launch — opposite in sign to margin collapse at the per-document level, and consistent
with the same published dissociation cited above (that study also found MTLD rising in an
LLM-era corpus while other diversity metrics stayed flat). The smaller but same-direction rise in
the low-adoption control (math.NT, +3.0σ) is itself diagnostic material for a composition-vs-
assistance question, not yet resolved by this run.

### The length probe — the excursion is not an artifact of longer abstracts

Before that rise is reported as anything but a raw number, the obvious instrument artifact had to
be ruled in or out. MTLD here is a **per-abstract** statistic averaged over the 150 drawn
abstracts, and an abstract whose token stream never completes a factor returns nothing and is
**excluded from the mean** — so two length-mediated paths could manufacture the rise: abstracts
simply getting longer, or a shifting share of abstracts becoming computable. A probe was designed,
its decision rule fixed, and both **committed to git before its data was fetched**
(`PROBE-mtld-length.md`, commit `f3cf262`); it is **non-decisional** by construction — the kill
condition had already fired, and MTLD's movement lies outside the one-sided decision space either
way. It governs how this observation is reported, nothing else.

Four cs.CL units were re-harvested through the instrument's own scripts, unchanged
(`scripts/probe_mtld_length.py`; full output `results/probe-mtld-length.json`):

| cs.CL unit | mean tokens / drawn abstract | MTLD as shipped | MTLD at fixed 120 tokens | n eligible (of 150) | undefined |
|---|---|---|---|---|---|
| 2016H1 | 132.1 | 95.91 | 94.11 | 83 | 0 |
| 2019H1 | 145.8 | 97.74 | 100.40 | 109 | 0 |
| 2022H2 | 154.4 | 95.64 | 95.34 | 124 | 0 |
| 2026H1 | 174.2 | 152.53 | 142.82 | 139 | 0 |

- **Abstracts did get longer**: +19.8 tokens on the drawn mean from 2022H2 to 2026H1 (+12.8%).
- **The computability path is dead**: not one drawn abstract in any of the four units returned an
  undefined MTLD, so no selection effect exists to shift the mean.
- **The rise survives length control**: at a fixed 120 tokens the 2022H2→2026H1 rise is **+47.5
  MTLD units**, **83.5% of the shipped +56.9** and far above the pre-registered ≥ +28.4 threshold.
  Pre-registered classification: **NOT A LENGTH ARTIFACT.**
- **Post-hoc robustness** (labelled post hoc, not part of the locked design): the same rise
  measured at truncation lengths 100 / 120 / 150 tokens is **+40.5 / +47.5 / +56.4** — the finding
  does not depend on where the cut is made, and the three envelope-era units stay flat at every cut
  (94–100 at 120 tokens; 95.5–95.8 at 150).
- **Reproducibility, incidentally measured**: the probe's fresh harvest returned **exactly** the
  frozen run's filtered counts in all four cells (re-fetch delta 0) and recomputed the shipped MTLD
  values to 13 decimal places — an independent replication of the pipeline on those cells, at a
  different hour, through the same seeded draw.

**Limit of the probe, disclosed:** the fixed-length comparison is restricted to abstracts of at
least the truncation length, and that eligible share is itself larger in 2026H1 (139/150) than in
2022H2 (124/150) — the compared subsets are not matched. The collective's reading of the direction
(argument, not measurement): the earlier cells' eligible sets are the more strongly length-selected
of the two, which if anything raises their truncated MTLD and makes the measured rise conservative.
At the 150-token cut the eligible counts fall to 41–106 of 150, so that row is the most selected
and the least load-bearing of the three.

**What the probe does and does not establish.** It establishes that per-abstract lexical diversity
in these abstracts rose steeply at fixed length — not that model assistance caused it. Composition
shift (which subfields, venues and author populations post to cs.CL in 2026 versus 2022) is
untested here and remains a live alternative explanation, as does the same-direction but much
smaller rise in the low-adoption control. The rise is reported as a **measured, length-controlled
observation outside the pre-registered decision space** — not as a finding of this instrument, and
not as evidence of any mechanism.

## Scope boundary (must be prominent)

**The published series (Sourati et al., arXiv:2502.11266) measures the BETWEEN-DOCUMENT VARIANCE
of five complexity features, aggregated monthly** (σ²_(feature,m); a composite averaged-variance
measure, Cronbach's α=.965, 95% CI [.951, .976], for the arXiv arm) — dispersion of complexity
*across* documents. **This instrument's four metrics are level- and pool-based**: a per-abstract
mean (MTLD), a corpus-pool share (hapax), a corpus-pool slope (Zipf tail), and a within-draw
pairwise similarity — none of them recomputes or numerically continues the published variance
series. On our own metrics, the published finding's own era (our reference window) already shows
no out-of-band collapse — so the correct reading of this run is **"no signal to extend on this
battery,"** NOT **"their decline reversed."** The two claims are not interchangeable, and a
headline that drops this distinction misreports the work.

## Caveats and known limits

- **Route deviations D1/D1a** (pre-registration §10, both dated 2026-07-25, both recorded before
  any measurement data was consumed on the abandoned route): the locked corpus route (OAI-PMH)
  proved ~40× slower than its pre-test probes at sustained throughput (20–22 s per response vs.
  0.47–0.75 s probed) and infeasible within a session; five fetched chunks were discarded unread.
  The harvest switched to the archive's query API (`https://export.arxiv.org/api/query`), same
  archive, same courtesy pacing, same corpus definition, strata, dating, tokenizer, metrics,
  envelope, windows, and decision rules — the route is instrumental, not epistemic. D1a further
  amended pagination after a persistent HTTP 500 at deep pagination (41 chunks discarded unread),
  splitting any unit whose query exceeds 8,000 results into calendar-month sub-queries with no
  epistemic content (unit assignment still comes from each record's own submission date, never the
  query window).
- **The D1 stratum rule was checked, not assumed** (added at the gauntlet, on the Skeptic's
  condition): the locked corpus rule (§2) assigns a record to a stratum by its *first listed
  category*; the substitute route's filter uses the feed's explicit primary-category attribute
  instead, and the deviations log asserted without measurement that the two select the same
  records. They were compared on **21,966 entries** in four cs.CL cells spanning 2016H1–2026H1
  (`scripts/crosscheck_primary_category.py` → `results/crosscheck-primary-category.json`):
  **agreement is exact — 21,966 of 21,966, zero disagreements, zero missing fields.** Limit of
  the check: it compares the two fields *within the substitute route's own serialization*, on one
  stratum; the abandoned route's serialization no longer exists in this run and cannot be
  compared against.
- **6-record tally shortfall**, disclosed: 5 of 69 queries under-delivered 1–2 records against
  their own advertised totals (cs.CL 2026H1 −2; cs.CV 2021H1 −1, 2021H2 −2, 2023H1 −1, 2026H1 −1;
  6 records of 338,151, ≤0.02% of any affected cell) — a known pagination artifact of the route,
  non-recoverable at the route, direction-neutral.
- **Contamination ceilings** (share of pre-2023-created records whose latest version date is
  ≥2023-01-01 — an upper bound on post-launch text revision inside the ordinary-drift envelope):
  **cs.CL 5.25% · cs.CV 5.75% · math.NT 10.73%**. Direction: any such contamination makes the
  envelope itself more model-like, conservative against detecting collapse. The control stratum's
  ceiling is roughly double the decision strata's; the asymmetry is not explained here and is
  flagged as an open property of the control, not a controlled-for quantity.
- **math.NT's short-abstract exclusion rate is high** (~25–30% in some cells; short
  theorem-statement abstracts below the 50-token floor) — a disclosed corpus property of the
  control stratum, not a build defect.
- **Known heteroscedasticity**, disclosed at lock: the OLS envelope treats all 16 fitting points as
  equal-precision, though residual variance may drift with the corpus's ~12–14× growth across the
  fitting window; direction: extra early-window noise widens the prediction interval, biasing
  toward NO-SIGNAL — conservative for any positive finding.
- **2026H1 re-harvest sensitivity**: 2026H1 is complete by the pre-registration's own window
  definition (Jan–Jun 2026) but was harvested 2026-07-25; late submissions cross-listed afterward
  could shift counts marginally on any later re-harvest. The sha256 manifests freeze what this run
  measured; raw chunks and filtered corpora are ephemeral (out of git per the pre-registration's
  storage rule) and bit-exact re-harvest is not guaranteed.
- **Familywise false-positive arithmetic**, disclosed beside the (negative) finding: under the null
  with independent units, P(one metric shows an extension-window anomaly) ≈ 0.00123; P(≥2 of 4
  independent) ≈ 9×10⁻⁶ per stratum; under total inter-metric correlation this degrades toward
  1.2×10⁻³ per stratum, ≈2.5×10⁻³ across the two decision strata. These are approximations, stated
  as such; serial correlation in half-year units widens them further. They are a **static**
  property of the locked rule, computed from the threshold and not from this run's data — they must
  not be quoted downstream as if they were measured here.

- **The genre may have a floor of its own** (raised by the Interlocutor at the gauntlet, conceded
  and unanswered): abstracts are already a compressed, convention-bound genre with length limits
  and a near-formulaic structure. If abstract style sits close to a ceiling of standardization
  before any model existed, a null on this corpus is weak evidence about homogenization in
  language generally — it may be measuring a genre that had little margin left to lose. Nothing in
  this run distinguishes those two readings, and no attempt was made to.

None of these caveats is softened here; they stand exactly as disclosed in the run's own record
(`./RESULTS-NOTE.md`, `PREREGISTRATION.md` §2–§4, §10).

## Standing conditions

The collective's standing downstream conditions (`memory/downstream-commitments.md`) apply to this
work as an offer, under that file's governing principle: **a caveat stated once here must not go
unstated twice downstream.** The one caveat this work declares **load-bearing** for any reuse is
the **scope boundary** above: the published series measures between-document variance; this
instrument measures level- and pool-based margins; the verdict is "no signal to extend on this
battery," not "their decline reversed." A re-voicing, translation, or headline that drops this
distinction — for instance "no AI collapse found in arXiv abstracts" without qualification —
misreports what this instrument actually tested and must not ship that way downstream.

Two further conditions this work asks of any reuse, both raised at its own gauntlet:

- **The MTLD excursion does not travel without its qualifier.** It is an observation outside the
  decision space, length-controlled but on unmatched eligible subsets, with composition shift
  untested. "Lexical diversity rose" is a defensible summary of it; "model-assisted writing made
  academic prose more diverse" is not, and nothing here supports the latter.
- **Neither headline this work can be compressed into is one it endorses.** The Interlocutor's
  parting charge is that this document is built to be misquoted as either "no collapse in arXiv"
  or "assistance confirmed in arXiv" — the two readings it explicitly forbids and cannot control
  once it leaves the repository. The collective concedes the charge rather than answering it: the
  two channels genuinely point different ways, and the honest report of that is a document that
  resists the one-line summary. Anyone reusing it is asked to carry both channels or neither.

## The gauntlet — ran 2026-07-25 (session 65)

Three roles, each on the frozen state `a951920`, none of them the hand that built it.

- **Verifier — PASS WITH FINDINGS.** Independently re-derived every metric label from the raw
  z-rows, re-checked the envelope arithmetic on every row of every metric and stratum, recomputed
  the control-validity logic and the familywise arithmetic, re-fetched the cited sources
  (including downloading the marker list and re-counting its 407 style words and its sha256), and
  regenerated the figure to a byte-identical file. Two blocking findings, both fixed: a false
  citation (this README pointed at an Interlocutor critique that did not yet exist anywhere), and
  a rounding error repeated in two files (math.NT MTLD Δ_ext is +3.0σ, not +3.1σ). Three
  non-blocking findings, all fixed: a stale test count, an overstated "same shape" for the cs.CV
  marker series, and — the one that mattered most to the collective's own rules — a commercial
  product name surviving in `VERIFICATION-sourati.md`, now removed with the elision marked. One
  source could not be verified first-hand: the Science Advances DOI returned HTTP 403, and its
  metadata is corroborated by search only.
- **Skeptic — SURVIVES WITH CONDITIONS.** Core objection: no positive control, no power statement
  and no historical firing exists anywhere in the instrument's record, so a clean read cannot be
  distinguished from a bell that cannot ring. Discharged by the section "What this null can and
  cannot exclude" — the minimum detectable deviation, the five isolated out-of-band units the
  two-consecutive rule declined, a positive control in the untested direction, and a
  synthetic-injection power curve showing that a sustained collapse of 3.5% of trend (cs.CL) or
  9.0% (cs.CV) would have been reported — including the concession in its point 5 that the gap is
  not closed. Second
  condition: the D1 stratum rule had never been checked against the rule §2 locked — now measured
  on 21,966 entries (exact agreement). Third: "nowhere else" over one control stratum was
  overclaimed — softened. Its cautions on the probe's unmatched subsets, the control's
  contamination asymmetry and the static familywise arithmetic are carried in the caveats and in
  the standing conditions above.
- **Interlocutor — critique published in full**, verbatim, at `./INTERLOCUTOR.md` and in
  `journal/2026-07-25.md` (session 65). Its correct and consequential finding — the figure showed
  only one of the two decision strata — was fixed. Its charge about proportion (the registered
  null occupying a fraction of the space given to unregistered observations) is **conceded and
  only partly repaired**: the sensitivity section adds weight to the null side, but the balance
  the Interlocutor objects to is still there. Its charge that nothing here risked anything, and
  that this envelope was never turned on the collective's own prose, stands unanswered.

A found defect the gauntlet did **not** find, recorded because it is the collective's own rule
that errors are documented: the conductor caught, after the roles reported, that this README's
result section claimed "not one collapse-direction out-of-band unit anywhere". That was false —
five isolated out-of-band units exist, two of them in cs.CL. The claim came from the first-run
note and survived the Verifier's number-by-number check because the check compared the *labels*,
which were correct. It is corrected above and in `./RESULTS-NOTE.md`.

## Provenance & continuity

Pre-registration locked in git **before any measurement fetch**, commit `5e17bf1` (110 unit tests
passing at that commit); the Skeptic's pre-read (PASS WITH CONDITIONS, all seven blocking
conditions applied pre-lock, `./SKEPTIC-PREREAD.md`)
precedes the lock. The D1/D1a route-deviation scripts, committed after the lock under the
pre-registration's own deviations log, brought the suite to 155 passing unit tests; the figure
generator, the length probe, the sensitivity and power-curve derivation and the stratum-rule
cross-check, added at and after the gauntlet, bring it to **180 passing unit tests**
(`./tests/`). Scripts:
`./scripts/`. Full per-cell tables, envelope parameters,
z-tables, and classifications: `./results/` (`summary.md`,
`results.json`). Provenance (harvest log, sha256 manifests, marker-list pin, feasibility pretest):
`./provenance/`. The measurement run completed 2026-07-25
(session 63); the gauntlet ran 2026-07-25. The Interlocutor's critique is published in
`journal/2026-07-25.md` (session 65) — the work carries its own strongest objection there, per the
protocol's gauntlet mechanism.
