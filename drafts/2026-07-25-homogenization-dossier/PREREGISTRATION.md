# Pre-registration — Homogenization Dossier v1 (ji-2026-002 · Meridian)

**Status: LOCKED (session 63, 2026-07-25) — this file's lock is the commit whose message
says "pre-registration LOCKED", made BEFORE any measurement fetch.** The Skeptic's pre-read
(PASS WITH CONDITIONS; all seven blocking conditions applied — `SKEPTIC-PREREAD.md`) and the
Builder's unit-tested scripts (110 tests passing) precede the lock. Method, metrics, null model and
decision rule are fixed by this document BEFORE any measurement fetch. Per the Local
Commitment (REQUESTS.md, session 61): append-whatever-it-shows; no threshold adjustment; no
re-run; the inquiry closes on the answer it gets. Any later edit to this file invalidates the
run it precedes.

## 1. Question

On arXiv preprint abstracts (strata **cs.CL** and **cs.CV**, dated by first-version
submission), did the published post-2022 decline in lexical-diversity/variance — Sourati et
al., arXiv:2502.11266, documented through Nov 2024 as a **steepened continuing slope, not a
step** (ONSET p=.699; POST β=−0.0014, p<.001; see `VERIFICATION-sourati.md`) — **continue,
plateau, or reverse** across the extension window, against a pre-2023 ordinary-drift envelope
fitted independently by this instrument? Comparability to the published series is
qualitative (same corpus family and hypothesis family, our own metrics), not a numeric
continuation of their model.

## 2. Corpus (declared before harvest)

- **Route:** the archive's own bulk-metadata interface (OAI-PMH), `ListRecords`,
  `metadataPrefix=arXiv`, sets `cs` and `math`, `from=2015-01-01` (datestamp superset;
  see `provenance/feasibility-pretest.md`), at the courtesy rate ≈1 request/3 s.
  Metadata is CC0. No full texts; abstracts only; no author-level analysis.
- **Stratum membership:** the record's **primary category** (first entry of `<categories>`)
  is exactly `cs.CL`, `cs.CV`, or `math.NT`. Mutually exclusive by construction. (The
  feasibility counts in provenance are any-listing counts and therefore upper bounds.)
- **Dating:** `<created>` (first-version submission date) in **2015-01-01 … 2026-06-30**.
- **Unit:** calendar half-years (H1 = Jan 1–Jun 30, H2 = Jul 1–Dec 31): 23 units,
  2015H1 … 2026H1.
- **Text:** the abstract field as served by the metadata route (current-version text).
  **Named validity caveat:** pre-2023 bins can contain post-2022 revised abstracts; the
  bulk route serves one current abstract per record (conductor's observation from the
  pre-test probes; no bulk route serving first-version abstracts was found — searched, not
  proven absent). Direction of bias: any post-launch contamination of the envelope period
  makes the envelope itself more model-like, biasing AGAINST detecting post-launch collapse
  — conservative for CONTINUE, anti-conservative for REVERSE claims of small magnitude.
  **Bounding, pre-registered:** the harvest's datestamp gives a free upper bound — the share
  of pre-2023-created records per stratum whose datestamp is ≥ 2023-01-01 (metadata touched
  post-launch, for any reason) ships with the Dossier as the contamination ceiling.
- **Author metadata:** the raw bulk XML incidentally carries public bibliographic author
  fields; the filtered corpus files keep only {id, created, datestamp, unit, abstract}
  (datestamp serves the contamination ceiling above), no author fields are ever parsed
  into the analysis, and raw XML stays out of git per repo convention (public/aggregate
  text only, no author-level analysis — the commitment's bound, honored by construction).
- **Exclusions:** abstracts with fewer than 50 tokens after tokenization (withdrawal
  notices, stubs). Exclusion counts reported per cell.
- **Tokenizer (fixed):** Unicode NFKC → lowercase → remove URLs (`https?://\S+`),
  inline TeX math (`$…$`), TeX commands (`\\[a-zA-Z]+`) → tokens =
  `[a-z]+(?:[-'][a-z]+)*` (unit tests: see §3).
- **Storage:** raw XML and the filtered per-stratum JSONL corpora stay out of git (size);
  the repo carries the harvest scripts, all harvest parameters, per-cell counts, sha256
  manifests of raw chunks and filtered corpora, and every derived metric value. The
  archive's records are live (updates change datestamps and abstract text), so bit-exact
  re-harvest at a later date is not guaranteed; the manifest freezes what THIS run measured.

## 3. Margin metrics (4), computed per (stratum, half-year) cell

All draws are seeded and deterministic, realized as **one seeded order per cell**: the cell's
arXiv IDs are sorted lexicographically, then shuffled in place by
`random.Random("20260725:{stratum}:{unit}").shuffle(ids)`; every draw below is a prefix of
that single shuffled order (no separate `.sample()` calls — the two stdlib methods consume
the RNG stream differently, and this document fixes the shuffle-then-prefix realization).

1. **MTLD** (McCarthy & Jarvis 2010; TTR threshold 0.72, bidirectional mean; a factor
   completes when the running TTR reaches or drops below the threshold, i.e. `<= 0.72`,
   matching the reference implementation), per abstract,
   averaged over the first **min(150, n)** abstracts of the cell's seeded order — a fixed
   draw size, so the mean's sampling precision is constant across cells (cells below 150
   use the whole cell and are flagged). Collapse direction: **down**.
2. **Hapax share under fixed-size sampling:** concatenate the cell's abstracts in the seeded
   order; truncate to the first **T = 15,000 tokens**; hapax share = types occurring exactly
   once ÷ total types. Collapse direction: **down**.
3. **Zipf-tail slope on the same fixed 15,000-token pool:** OLS slope of log10(frequency) on
   log10(rank) over ranks 101…1,000 (if the pool has fewer than 1,000 types, use
   101…max-rank and flag; below 300 types the cell is marked non-computable). A thinning
   rare-word tail drops faster: collapse direction: **more negative**.
4. **Between-abstract similarity on fixed draws:** the first **N_s = min(150, n)** abstracts
   of the cell's seeded order (the same prefix as metric 1, deliberately);
   within-draw TF-IDF (tf = raw count, idf = ln(N_draw/df) with N_draw the actual draw
   size), L2-normalized, mean pairwise cosine. Collapse direction: **up**.
   Disclosed metric property: within-draw idf zeroes any token present in every drawn
   abstract, so the metric measures similarity in the non-universal vocabulary — a draw of
   identical abstracts scores 0, not 1; convergence registers as rising overlap among
   discriminating tokens, which is the margin property under test.

Cells smaller than a draw size use the whole cell and are flagged in the output table; how
often each fallback fires ships in the output table (the feasibility counts are any-listing
upper bounds, so trigger frequency is unverified until harvest).
For classification, every metric is **reoriented so that collapse = negative** (similarity
enters with sign flipped).

**Non-computable units:** a unit where a metric cannot be computed (e.g. the Zipf pool below
300 types) is excluded from that window's Δ mean and cannot itself satisfy the
two-consecutive rule; if exclusions leave a window with fewer than 2 computable units for a
metric, that metric is **non-decidable** for that stratum-window, excluded from the ≥2-of-4
count, and flagged explicitly. (Non-computability is not missing-at-random — severe collapse
itself could cause it; any such flag is reported prominently, never silently dropped.)

**Unit-testing:** the tokenizer, all four metrics, the envelope arithmetic and the
classification logic are unit-tested in `tests/` before any measurement fetch; the lock
commit contains the passing tests.

## 4. Null model — the ordinary-drift envelope

Per metric × stratum: OLS linear regression on the **16 envelope units 2015H1–2022H2**
(x = 0…15). For any later unit x*, the two-sided 95% prediction interval is
ŷ(x*) ± t₀.₉₇₅,₁₄ · s · √(1 + 1/16 + (x*−x̄)²/Sxx), with t₀.₉₇₅,₁₄ = 2.1448.
Standardized deviation z(x*) = (y(x*) − ŷ(x*)) / SE_pred(x*), reoriented collapse-negative.

- **Out-of-band (per unit):** z < −2.1448 (collapse side only, per the commitment). Stated
  precisely: a one-sided α = 0.025 test derived from the two-sided 95% PI's lower bound —
  more conservative than a one-sided 95% test, deliberately.
- **Anomaly (per metric, per window):** out-of-band in **two consecutive units** of that
  window.
- **Known heteroscedasticity, disclosed:** the OLS envelope treats all 16 points as
  equal-precision; fixed-size draws hold *sampling* precision constant by design (that is
  their purpose), but residual variance may still drift with the corpus's ~12–14× growth
  inside the fitting window (topic/author-mix churn). Direction: extra early-window noise
  widens the PI, biasing toward NO-SIGNAL — conservative for any positive finding.
- Envelope caveat, pre-registered: the envelope's final unit 2022H2 contains the one-month
  post-launch sliver (Nov 30–Dec 31 2022) — kept, per the commitment's own "pre-2023"
  boundary; direction: contaminates the envelope toward collapse, i.e. conservative.
- Sensitivity: the same table under a quadratic envelope (same OLS prediction-interval
  principle, s·√(1 + x₀ᵀ(XᵀX)⁻¹x₀), of which the linear formula above is the special case;
  t₀.₉₇₅,₁₃ = 2.1604 for the 3-parameter fit), reported beside. **Soft downgrade
  rule (decisional):** if the linear and quadratic envelopes disagree on a stratum's headline
  state, the stratum ships BOTH headlines, marked unresolved — the linear envelope alone
  cannot carry a verdict its own curvature check contradicts. Scope, fixed: the
  disagreement test compares the §7 headline state only; the control inputs (marker
  validity, control-clear) are computed once, from the linear envelope — the quadratic pass
  is a curvature check on the margin classification, not an independent second instrument.
- **Missing envelope-era cells:** a non-computable metric value in any of the 16 envelope
  units halts the run for that metric × stratum (loud failure, no silent df degradation);
  such a halt is a deviation event for §10, not an adaptive branch. (Feasibility counts make
  this unlikely; pre-registered so it cannot be improvised later.)

## 5. Windows

- **Envelope:** 2015H1–2022H2 (16 units).
- **Reference window** (the published finding's era, replication context, NOT decision
  units): 2023H1–2024H2 (4 units). Δ_ref = mean z over these 4 units, per metric.
- **Extension window (decision units):** **2025H1, 2025H2, 2026H1** (3 units).
  Δ_ext = mean z over these 3 units. 2024H2 partially overlaps the published series'
  Nov-2024 endpoint; it stays in the reference window, and no decision reads from it.
  Decidability: with 3 extension units, the two-consecutive rule is satisfiable in three
  ways (25H1+25H2, 25H2+26H1, all three) — CONTINUE, PLATEAU and REVERSE are all reachable
  at first run. The one return move (≥2027-01) appends 2026H2 under this same document.

## 6. Per-metric classification (fixed vocabulary)

Let A_ref = anomaly rule met in the reference window; A_ext = anomaly rule met in the
extension window; δ = Δ_ext − Δ_ref (negative = deepening).

- **NO-ANOMALY:** neither A_ref nor A_ext → "consistent with ordinary drift."
- **CONTINUE:** A_ext AND δ ≤ −0.5.
- **NEW-ONSET:** A_ext AND NOT A_ref AND δ ≤ −0.5 (labelled separately; counts with
  CONTINUE for the directional finding).
- **PLATEAU:** A_ext AND |δ| < 0.5 (anomaly persists at its documented depth).
- **REVERSE:** (A_ref OR A_ext) AND δ ≥ +0.5 — an anomaly must have been established in one
  of the two windows before "recovery" can be claimed; a swing between two never-anomalous
  windows is NO-ANOMALY, not REVERSE. Sub-label FULL if all three extension units are inside
  the prediction interval, PARTIAL otherwise.
- **RESIDUAL:** every remaining configuration — chiefly the A_ref-only cases with δ < +0.5
  (the anomaly did not recur in the extension, yet no 0.5-unit recovery is measurable
  either) — reported by its full z-table without a headline label.

The labels are evaluated in this fixed order — **NO-ANOMALY → NEW-ONSET → CONTINUE →
PLATEAU → REVERSE → RESIDUAL** — and the first matching label is the metric's label
(NEW-ONSET precedes CONTINUE because its condition is the stricter subset; the ordering
makes the set exhaustive and mutually exclusive by construction).

**The δ threshold (±0.5), stated rationale:** half the envelope's residual standard unit —
below it, the difference between a 4-unit and a 3-unit window mean is smaller than typical
single-unit noise, so calling it movement would be reading noise; applied symmetrically to
deepening (CONTINUE) and recovery (REVERSE), so it favors neither direction.

## 7. Stratum verdict and decision rule

Per decision stratum (cs.CL, cs.CV, separately), evaluated as an ordered procedure over the
four per-metric labels (metrics flagged non-decidable per §3 leave the ≥2-of-4 and ≤1 counts
computed over the decidable metrics, with the reduced denominator disclosed):

1. **Directional finding "margins shrinking beyond ordinary drift":** ≥2 of 4 metrics with
   A_ext in the collapse direction — AND the control condition below. If it fires, the
   stratum headline is the plurality among the A_ext metrics' labels, pooling
   CONTINUE + NEW-ONSET against PLATEAU; an A_ext metric carrying any other label — an
   arithmetic edge case — is excluded from the bucket count; tie → **MIXED (shrinking)**.
2. Else **kill condition (the offer's own):** if ≤1 metric shows any collapse-direction
   anomaly across reference and extension windows, the stratum reads **NO SIGNAL BEYOND
   ORDINARY DRIFT**; if both decision strata read so, the Dossier ships that negative
   result with full weight and the inquiry closes.
3. Else the stratum headline is the **plurality label over all four metrics' labels**
   (CONTINUE + NEW-ONSET pool; REVERSE sub-labels pool; NO-ANOMALY and RESIDUAL count in
   the denominator but cannot become the headline — a stratum reaching this step has ≥2
   anomalous metrics by construction); tie or no plurality among anomaly labels →
   **MIXED**, reported metric-by-metric. This step is what a majority-REVERSE stratum
   ships as: **REVERSE — the documented anomaly did not persist against the envelope.**

Every stratum configuration lands in exactly one of steps 1–3; there is no undefined bucket.

**Control stratum (math.NT):**

- **Validity precondition:** math.NT's *marker channel* (§8) must NOT itself meet the
  anomaly rule in the **excess direction** (z > +2.1448; see §8) over the single combined
  window 2023H1–2026H1 against its own envelope. The wider 7-unit window is a deliberate
  asymmetry versus the margin metrics' split ref/ext windows: the control's validity should
  fail on assistance-adoption evidence from ANY post-launch period, not only the extension.
  If it fails, math.NT is **downgraded to comparison stratum** (informative, no veto) —
  declared here, before measurement.
- **If valid:** a directional finding additionally requires math.NT NOT to show ≥2-of-4
  collapse-direction A_ext itself. If the control collapses too, the verdict is downgraded
  to **"shared shift — attribution open"** (a corpus-wide/secular force is not
  distinguishable from model influence by this instrument).

**Familywise false-positive arithmetic (disclosed beside any positive finding):** under the
null with independent units, P(one metric shows A_ext) ≈ 2·(0.025)² − (0.025)³ ≈ 0.00123;
≥2 of 4 independent metrics ≈ 6·(0.00123)² ≈ 9×10⁻⁶ per stratum; under total inter-metric
correlation it degrades toward 1.2×10⁻³ per stratum, ≈2.5×10⁻³ across the two decision
strata. Serial correlation in half-year units widens these further; the numbers are
approximations, stated as such, direction of each approximation noted in the shipped work.

## 8. Marker channel (attribution context — explicitly NOT a margin metric)

- **Marker set:** the 407 words annotated `type=="style"` in the published excess-vocabulary
  list (Kobak et al. 2025, Science Advances 11(27) eadt3813;
  `provenance/excess_words.csv`, sha256
  `f5786f3cc83f9578043aaecf2774c6200cb68b5e774afc3afe40af4eb0cf8285`, fetched 2026-07-25
  from the authors' public repository, path `results/excess_words.csv`). Style words only:
  content-type words track topics, not writing style.
- **Statistic per cell (decisional):** marker tokens per 1,000 tokens over the **same fixed
  15,000-token seeded pool as §3 metrics 2–3** — fixed-size, so the statistic's sampling
  precision is constant across cells (the whole-cell rate is heteroscedastic across a ~41×
  cell-size range and is therefore reported as context only, never fed to an envelope).
  **Re-baselined by construction:** the envelope (same §4 method) is fitted on THIS corpus's
  own 2015–2022 half-year rates per stratum — the published list's PubMed baseline rates are
  never imported.
- **Direction (fixed here, since §4's formula is typed to the collapse tail):** the marker
  channel is NOT reoriented; excess is the **upper** tail, and out-of-band for this channel
  means **z > +2.1448** — anomalously HIGH marker rate. An implementer copying §4's
  z < −2.1448 literally would test for anomalously low marker usage and void the §7 gate.
- **Decidability:** the §3 non-computable/non-decidable machinery is scoped to the four
  margin metrics; for this channel, if the §7 validity window cannot be evaluated on ≥2
  computable units, the gate is indeterminate and math.NT is **downgraded** (fail-safe: the
  control loses its veto rather than wrongly holding it).
- **Roles:** (a) the math.NT validity precondition (§7); (b) context beside any margin
  finding — including the pre-registered mixed-signal reading: marker excess with margins
  in-band replicates the published news-corpus dissociation (Fitterer et al., ACL 2025 SRW)
  and ships as exactly that, not as collapse.

## 9. What ships

Dossier v1: the per-cell metric tables, envelope parameters, z-tables, classifications,
verdicts, kill-or-finding — whatever it shows — plus provenance (harvest parameters, counts,
manifests), the marker-channel context, the §2 caveats, and the full gauntlet's published
critique. Downstream conditions per `memory/downstream-commitments.md`.

## 10. Deviations log

None at lock. Any deviation discovered mid-run is recorded here with date and rationale and
re-runs the gauntlet's judgement on whether the run survives.
