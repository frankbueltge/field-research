# Domain specialist — multiplicity, indirect standardisation and exact discrete tests

*Session 117, 2026-08-13. Convened because this session used an estimator stack it had not used
before in this arc — leave-one-out indirect standardisation, exact Poisson-binomial tails,
Benjamini–Hochberg, and a Monte-Carlo family-wise check — and needed it audited by someone who was
not part of building it. The report is published **unedited**, on **version 1 of `INCREMENT-7.md`
at `f6d8d4d`**. Discharge: `CONDITIONS-DISCHARGED-117.md`.*

---

## Overall verdict

**SOUND WITH QUALIFICATION.** The arithmetic is clean (every figure I checked reproduces exactly from the JSON/code), the DP tail and BH implementations are textbook-correct, and the leave-one-out standardisation is engineered in the right direction. But the instrument has one real, undisclosed internal inconsistency (pooled vs. leave-one-out rates between the scan and the power script) and one real, undiscussed statistical gap (the exact test cannot separate an elevated per-unit rate from within-page dependence, e.g. a single correlated removal event) — the second is the more important omission, because it is precisely the ambiguity ("event, topic, or sweep") the whole session was convened to chase, and the write-up never names it as a property of the test itself.

## 1. Leave-one-page-out standardisation — SOUND

This is a correct, recognised form of *internal* indirect standardisation (rates drawn from the study population itself, minus the unit under test — the standard fix for the circularity of naive internal standardisation). I verified the direction and size of the bias it corrects: for Paraguay's cell (`3-4y × W-article`, n=437 corpuswide), the pooled rate including Paraguay's own 16 absences is 14.65%; excluding Paraguay it is 11.57% — a 26.6% relative deflation. Using the pooled rate as "expected" would have understated the excess for exactly the page most likely to be tested. LOO removes that specific self-fulfilling contamination, and it does so in the correct direction (more sensitive, not less).

Qualification: the reference pool is still **internal**, not external. LOO removes only the tested page's own contamination — it does nothing to protect against contamination from *other*, unscanned (n<5) pages sharing the same narrow cell. Paraguay's cell is defined by a 14.9-day-wide age window tied to one 2023 event; if other small pages about the same event also sit in that cell and are themselves anomalously absent or anomalously present, the "clean" 11.57% baseline is not actually clean, and the direction of that residual bias is unknown and unbounded. Nothing in the pipeline checks for this. That's a real limitation of internal standardisation generically, not a bug, but it is not disclosed in either the pre-registration or INCREMENT-7.

The fallback rule (`MIN_CELL=30`, stratum margin, then global margin, all also computed leave-one-out) is internally consistent and sound. Moot for this run (`fallback_share = 0.0`, confirmed).

## 2. Exact Poisson-binomial tail — SOUND

`poisson_binomial()` is the standard DP recursion (`nxt[k]+=v(1-p); nxt[k+1]+=v·p`), all-nonnegative accumulation, no cancellation risk. I re-ran it on 40 synthetic probabilities: pmf sums to 1.0, min ≈ 8.9e-24, no underflow to zero, no NaN — safe at n=40 (and well beyond).

`tails()`: `low = sum(d[:a+1])` = Pr(X≤a), `up = sum(d[a:])` = Pr(X≥a). Both inclusive of `a`, matching exactly what §1 of INCREMENT-7 and the pre-registration claim. Correct.

Minor inefficiency, not a correctness issue: `fwer_monte_carlo` calls `tails(ps, a)`, which rebuilds the full O(n²) DP from scratch, once per page per Monte-Carlo draw (540,000 rebuilds for 54 pages × 10,000 draws), even though `ps` — and hence the whole pmf — is fixed per page across all draws. Only `a` varies. Wasted compute, not a wrong answer.

## 3. Composite alternative — SOUND WITH QUALIFICATION, and this is the audit's central finding

The null tested is: 22 units absent **independently**, each at its own cell's rate. Rejection licenses exactly one statement: *this page's joint absence pattern is incompatible with independent draws at the corpus's age/stratum baseline.* It does **not** by itself distinguish:

- (a) a genuinely elevated per-unit probability specific to this page/subject (real page-level signal), from
- (b) **positive dependence among the units on the page** — e.g. one correlated removal action, a single moderation sweep, or a bulk takedown triggered by the shared event — which would produce an equally extreme Poisson-binomial tail under the assumed-independent model even if no individual unit's true marginal probability were elevated at all.

Both produce the same p = 3.836e-11 under this test, because the test's independence assumption is exactly what (b) violates. If the truth is (b), the "16 independent bits of evidence" the exact tail is built on are really closer to one correlated event, and the effective-n problem is the same one this arc already built machinery for at the account level (`cluster_model.py`'s ICC/DEFF apparatus) — but that machinery was never extended to the page-level test in `coloss_117.py`. INCREMENT-7 is admirably disciplined about **not** claiming page-vs-account mechanism (§2, correctly gated by the pre-registered power floor), and the title itself only claims "this corpus cannot say why." But nowhere does the document, or the pre-registration, name the *dependence-vs-rate* ambiguity as a property of the statistical test itself — the "event, topic, or sweep" framing quoted from session 114 gestures at it but is never connected explicitly to what the exact tail can and cannot license. That connection should be made explicitly before this is called an "instrument."

What the rejection does **not** license, stated plainly: it does not license "this subject was targeted," "this page is causally special," or "the loss is concentrated" in any sense stronger than "the joint pattern deviates from age-only iid prediction, for reasons this test cannot decompose into rate vs. dependence, let alone page vs. account."

## 4. Benjamini–Hochberg — SOUND, and I checked BY

`bh()` is the standard step-up computation (monotonised minimum of `p·m/rank` from the largest rank down), matching `statsmodels`' `fdr_bh` output structure exactly, verified by hand-tracing the code — correct.

Validity under dependence: BH is proven valid under independence or PRDS (Benjamini–Yekutieli 2001); it is **not proven** valid under arbitrary dependence. Here, page-level p-values are not independent — they share nuisance-parameter estimation (every page's expectation is built from cell rates that other pages also feed into). This is a real, unaddressed gap in rigor: nothing in the design demonstrates PRDS holds. I computed the dependence-robust Benjamini–Yekutieli correction directly (`c(54) = ΣH_54 ≈ 4.575`) on the actual 54 upper-family p-values: **BY still flags the same 2 pages** — Paraguay's BY q-value is 9.48e-9 (vs BH 2.07e-9) and 瀬乃真帆子's is 1.46e-3 (vs BH 3.20e-4), both comfortably under q=0.05. So the answer to "would BY change the conclusion" is concretely **no**, at these q-values, by roughly four orders of magnitude of headroom. This should be stated in the document as evidence rather than left as an unaddressed theoretical gap, since I've now closed it.

## 5. Monte-Carlo family-wise check — SOUND WITH QUALIFICATION

The mechanics are a legitimate minP-style family-wise procedure: draw the full 54-page null jointly per replicate (correctly preserving the same simultaneous multiplicity structure as the real test), track the minimum tail across pages, compare the observed minimum against that null distribution. I verified `k=0` (zero of 10,000 draws produced a minimum tail ≤ 3.836e-11), giving `(0+1)/(10000+1) = 9.999e-5` exactly as reported — this is the smallest value 10,000 draws can express, and the document says so correctly.

What 9.999e-5 **means**: among 10,000 simulated realisations of the entire null (54 pages simultaneously), none came anywhere close to as extreme as what was observed — the observed minimum sits below even the null's 5th percentile (2.35e-3) by seven orders of magnitude, not marginally. What it **does not mean**: it is not a precise, resolution-unlimited family-wise p-value — it is floor-limited by draw count, and it draws under the **estimated** LOO ps treated as ground truth, ignoring their sampling uncertainty. Given the observed tail is ~1e-11 against a null 5th percentile of 2.35e-3 (seven orders of magnitude), plausible estimation error in the underlying rates (cells mostly have hundreds of units, SE on the order of 1–2 points) could not plausibly move the conclusion — so the qualification does not threaten "not a multiple-testing artefact," but the number 9.999e-5 should not be quoted as if it were an exact, tight, unconditional bound; it is a floor-resolution sanity check that happens to be uninformative about *how* extreme the result is beyond "far beyond what 10,000 draws can resolve."

## 6. Detectability floor in `coloss_power_117.py` — inconsistency confirmed, materially small

Confirmed by reading `detectability()`: it computes `ps` from **pooled** cell rates over all attributed rows (`a_cell[cell]/n_cell[cell]`), not the leave-one-page-out rates the actual scan uses. This is a real inconsistency: for the same page/run, `coloss-117.json` reports Paraguay's expected = 2.5446 while `coloss-power-117.json` reports expected = 3.2220 for the identical 22 units — a silent 26.6% discrepancy with no cross-reference or explanation anywhere in either JSON or INCREMENT-7. A reader who opens both files side by side would reasonably conclude something is broken.

I quantified the practical impact by recomputing the whole 54-page detectability sweep under LOO instead of pooled: **the aggregate summary statistics barely move** — median detectable share is identical (66.7% both ways), the range is identical (22.9%–100%), median detectable excess shifts from 4.260 to 4.247 videos (0.3%). For Paraguay specifically, min-detectable-absent shifts from 10 (pooled) to 9 (LOO) out of 22. So: the Bonferroni-vs-BH framing ("upper bound," which is provably true since BH's rejection region is always a superset of Bonferroni's, they coincide at rank 1) is the dominant source of conservatism, and the pooled-vs-LOO choice, while a genuine engineering inconsistency, contributes only a small additional conservative nudge, concentrated almost entirely on the one or two heaviest pages (because most of the 54 pages are a negligible fraction of their cell). **The "66.7% median" statement is a fair, if slightly conservative, characterisation of what the pre-registered BH scan could detect** — but the inconsistency should still be fixed or at minimum disclosed, because right now the two output files disagree about a basic quantity for the same page without saying so.

## 7. Other errors — none found beyond items above

I recomputed every number in `coloss-derived-117.json` independently from the raw ledger data and the scan output: observed/expected ratio (6.2879), absent/expected shares (72.73%/11.57%), corpus rate (434/3569 = 12.1603%), age span (14.9047 days ÷ 365.2425 = 0.040808 years) — all match to full float precision. Distinct-page count (2,630), pages ≥5 units (54, 519 units), zero fallback units, all baseline-state counts (15/6/1), account counts (20 total, 18 single-video) — all reproduce exactly from the code and data. No arithmetic errors found. The one correction the session already self-flagged (the double-counted `off_page_units` figure) is handled properly — superseded value retained and labelled, not silently dropped.

## 8. What I would have done differently, in order of value

1. **Name the dependence-vs-rate ambiguity explicitly as a limitation of the test itself** (item 3), and — if this instrument is meant to graduate beyond a case note — extend the account-level ICC/DEFF machinery this arc already built (`cluster_model.py`) to the page level, so a page-level "effective n" or intra-page concordance check accompanies the exact tail. Right now the Herfindahl check answers "where does the excess live" but nothing answers "is the excess one correlated event or many independent ones," which is the actual scientific question the session was chasing.
2. **Fix the pooled/LOO inconsistency** in `coloss_power_117.py::detectability()` so it uses the same leave-one-out rates as `coloss_117.py::scan()`, or at minimum add one sentence disclosing the discrepancy and its (now measured) small size — don't leave two JSON files silently disagreeing about "expected" for the same page.
3. **Report what fraction of a page's reference cell comes from other small, unscanned (n<5) pages sharing the same narrow age window**, as a direct check on the "internal reference is clean" assumption — cheap to compute from data already collected, and it's exactly the kind of contamination the leave-one-out fix does *not* protect against.
4. Lower priority: cache the per-page pmf once in `fwer_monte_carlo` instead of recomputing it 10,000 times per page (pure efficiency), and consider folding rate-estimation uncertainty into the Monte-Carlo null rather than conditioning on point estimates — though given the seven-order-of-magnitude margin, this would not change any conclusion in this run.

## Figures I could not reproduce

None among the quantitative scan/power/derived figures — every number I checked against `coloss-117.json`, `coloss-power-117.json`, `coloss-derived-117.json`, and by re-running `cluster_model.load` / `cluster_keys.page_index` / `coloss_117.scan` directly against the ledger, matched exactly. The §7 "neighbours" section (external DOIs, HTTP status codes, the Küpfer 2024 citation, HRW report) is outside this audit's scope — those are live web claims, not arithmetic on the JSON/code, and I did not attempt to re-verify them.

## Qualifications I insist be published alongside this

- The exact Poisson-binomial rejection for Paraguay (p=3.836e-11) is evidence against **independent** age-standardised absence on that page. It is not, by itself, evidence of a page-specific elevated rate as opposed to a single correlated removal event — the document should say this in as many words, not just gesture at "event, topic, or sweep" as unresolved background.
- `coloss-power-117.json`'s "expected" for Paraguay (3.2220) is computed on pooled cell rates and disagrees with `coloss-117.json`'s LOO "expected" (2.5446) for the identical page and run; the aggregate detectability statistics quoted in INCREMENT-7 §4 are only mildly sensitive to this (median share unchanged, median excess off by 0.3%), but the discrepancy itself is real and undocumented.
- BH's validity here rests on an unproven PRDS-type assumption across shared-nuisance-parameter tests; I checked the BY alternative directly and it does not change which pages flag (same 2, headroom of 3–4 orders of magnitude), which should be stated as evidence rather than left as an open gap.
