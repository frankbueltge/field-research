# Pre-registration — Homogenization Dossier v1 (ji-2026-002 · Meridian)

**Status: DRAFT — NOT YET LOCKED (session 63, 2026-07-25; Skeptic pre-read in flight).
The lock is the commit whose message says "pre-registration LOCKED".** Method, metrics, null model and
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
  metadata route does not serve version-1 abstracts in bulk. Direction of bias: any
  post-launch contamination of the envelope period makes the envelope itself more
  model-like, biasing AGAINST detecting post-launch collapse — conservative for CONTINUE,
  anti-conservative for REVERSE claims of small magnitude; carried on the work.
- **Exclusions:** abstracts with fewer than 50 tokens after tokenization (withdrawal
  notices, stubs). Exclusion counts reported per cell.
- **Tokenizer (fixed):** Unicode NFKC → lowercase → remove URLs (`https?://\S+`),
  inline TeX math (`$…$`), TeX commands (`\\[a-zA-Z]+`) → tokens =
  `[a-z]+(?:[-'][a-z]+)*`. Unit-tested in `tests/`.
- **Storage:** raw XML and the filtered per-stratum JSONL corpora stay out of git (size);
  the repo carries the harvest scripts, all harvest parameters, per-cell counts, sha256
  manifests of raw chunks and filtered corpora, and every derived metric value. The
  archive's records are live (updates change datestamps and abstract text), so bit-exact
  re-harvest at a later date is not guaranteed; the manifest freezes what THIS run measured.

## 3. Margin metrics (4), computed per (stratum, half-year) cell

All draws are seeded and deterministic: RNG = `random.Random("20260725:{stratum}:{unit}")`
over the cell's arXiv IDs sorted lexicographically.

1. **MTLD** (McCarthy & Jarvis 2010; TTR threshold 0.72, bidirectional mean), per abstract,
   averaged over a seeded draw of up to 1,000 abstracts per cell.
   Collapse direction: **down**.
2. **Hapax share under fixed-size sampling:** concatenate the cell's abstracts in seeded
   order; truncate to the first **T = 15,000 tokens**; hapax share = types occurring exactly
   once ÷ total types. Collapse direction: **down**.
3. **Zipf-tail slope on the same fixed 15,000-token pool:** OLS slope of log10(frequency) on
   log10(rank) over ranks 101…1,000 (if the pool has fewer than 1,000 types, use
   101…max-rank and flag; below 300 types the cell is marked non-computable). A thinning
   rare-word tail drops faster: collapse direction: **more negative**.
4. **Between-abstract similarity on fixed draws:** seeded draw of **N_s = 150** abstracts;
   within-draw TF-IDF (tf = raw count, idf = ln(150/df)), L2-normalized, mean pairwise
   cosine. Collapse direction: **up**.

Cells smaller than a draw size use the whole cell and are flagged in the output table.
For classification, every metric is **reoriented so that collapse = negative** (similarity
enters with sign flipped).

## 4. Null model — the ordinary-drift envelope

Per metric × stratum: OLS linear regression on the **16 envelope units 2015H1–2022H2**
(x = 0…15). For any later unit x*, the two-sided 95% prediction interval is
ŷ(x*) ± t₀.₉₇₅,₁₄ · s · √(1 + 1/16 + (x*−x̄)²/Sxx), with t₀.₉₇₅,₁₄ = 2.1448.
Standardized deviation z(x*) = (y(x*) − ŷ(x*)) / SE_pred(x*), reoriented collapse-negative.

- **Out-of-band (per unit):** z < −2.1448 (collapse side only, per the commitment).
- **Anomaly (per metric, per window):** out-of-band in **two consecutive units** of that
  window.
- Envelope caveat, pre-registered: the envelope's final unit 2022H2 contains the one-month
  post-launch sliver (Nov 30–Dec 31 2022) — kept, per the commitment's own "pre-2023"
  boundary; direction: contaminates the envelope toward collapse, i.e. conservative.
- Sensitivity (reported beside, non-decisional): the same table under a quadratic envelope.

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
- **REVERSE:** δ ≥ +0.5 (recovering toward the envelope; sub-label FULL if all three
  extension units are inside the prediction interval, PARTIAL otherwise).
- Residual cases (e.g. A_ext with +0.5 > δ > −0.5 boundary noise, A_ref only) are reported
  by their z-table without a headline label.

## 7. Stratum verdict and decision rule

Per decision stratum (cs.CL, cs.CV, separately):

- **Directional finding "margins shrinking beyond ordinary drift":** ≥2 of 4 metrics with
  A_ext in the collapse direction — AND the control condition below.
- **Headline state:** majority vote among metrics showing any anomaly (CONTINUE and
  NEW-ONSET pool together); no majority → **MIXED**, reported metric-by-metric.
- **Kill condition (the offer's own):** if ≤1 metric shows any collapse-direction anomaly
  in reference or extension windows, the stratum reads **NO SIGNAL BEYOND ORDINARY DRIFT**;
  if both decision strata read so, the Dossier ships that negative result with full weight
  and the inquiry closes.

**Control stratum (math.NT):**

- **Validity precondition:** math.NT's *marker channel* (§8) must NOT itself meet the
  anomaly rule (excess direction) over 2023H1–2026H1 against its own envelope. If it does,
  math.NT is **downgraded to comparison stratum** (informative, no veto) — declared here,
  before measurement.
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
- **Statistic per cell:** marker tokens per 1,000 tokens over the whole cell (all abstracts,
  no sampling). **Re-baselined by construction:** the envelope (same §4 method) is fitted on
  THIS corpus's own 2015–2022 half-year rates per stratum — the published list's PubMed
  baseline rates are never imported.
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
