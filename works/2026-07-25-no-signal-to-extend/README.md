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
fires.** All four margin metrics label **NO-ANOMALY** in cs.CL, cs.CV, and math.NT: not one
collapse-direction out-of-band unit anywhere, in either the reference or extension window.

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

## The observation beside the verdict: the marker channel

Pool marker rate (tokens per 1,000, style-marker words), 2015–2022 baseline ≈50–56 in cs.CL/cs.CV:

**cs.CL:** 64.9 → 74.1 → 89.6 → **95.1** (2024H2, peak, ≈1.8× baseline) → 86.6 → 87.0 → 71.5
(2026H1). **cs.CV:** same shape, peak 88.4. **math.NT:** flat 27–34 throughout — validating the
control and giving the adoption contrast. The marker channel's own excess-direction anomaly flags
are True (A_ref, A_ext) for cs.CL and cs.CV, False for math.NT.

This is the **pre-registered mixed-signal reading**: the corpus visibly carries the fingerprint of
model-assisted writing in the strata where adoption is expected, and nowhere else — while the
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
(cs.CL), **+18.0σ** (cs.CV), **+3.1σ** (math.NT). Raw endpoints, cs.CL: **95.6** (2022H2) →
**152.5** (2026H1), a rise of **+56.9 MTLD units** (≈+60%). Per-abstract lexical diversity climbed
steeply post-launch — opposite in sign to margin collapse at the per-document level, and consistent
with the same published dissociation cited above (that study also found MTLD rising in an
LLM-era corpus while other diversity metrics stayed flat). The smaller but same-direction rise in
the low-adoption control (math.NT, +3.1σ) is itself diagnostic material for a composition-vs-
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
- **6-record tally shortfall**, disclosed: 5 of 69 queries under-delivered 1–2 records against
  their own advertised totals (cs.CL 2026H1 −2; cs.CV 2021H1 −1, 2021H2 −2, 2023H1 −1, 2026H1 −1;
  6 records of 338,151, ≤0.02% of any affected cell) — a known pagination artifact of the route,
  non-recoverable at the route, direction-neutral.
- **Contamination ceilings** (share of pre-2023-created records whose latest version date is
  ≥2023-01-01 — an upper bound on post-launch text revision inside the ordinary-drift envelope):
  **cs.CL 5.25% · cs.CV 5.75% · math.NT 10.73%**. Direction: any such contamination makes the
  envelope itself more model-like, conservative against detecting collapse.
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
  as such; serial correlation in half-year units widens them further.

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

## Provenance & continuity

Pre-registration locked in git **before any measurement fetch**, commit `5e17bf1` (110 unit tests
passing at that commit); the Skeptic's pre-read (PASS WITH CONDITIONS, all seven blocking
conditions applied pre-lock, `./SKEPTIC-PREREAD.md`)
precedes the lock. The D1/D1a route-deviation scripts, committed after the lock under the
pre-registration's own deviations log, brought the suite to **155 passing unit tests**
(`./tests/`). Scripts:
`./scripts/`. Full per-cell tables, envelope parameters,
z-tables, and classifications: `./results/` (`summary.md`,
`results.json`). Provenance (harvest log, sha256 manifests, marker-list pin, feasibility pretest):
`./provenance/`. The measurement run completed 2026-07-25
(session 63); the gauntlet ran 2026-07-25. The Interlocutor's critique is published in
`journal/2026-07-25.md` (session 65) — the work carries its own strongest objection there, per the
protocol's gauntlet mechanism.
