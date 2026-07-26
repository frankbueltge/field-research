# Pre-registration — "The Envelope Turned Inward"

**Locked before any metric value is computed.** Draft instrument, session 66, 2026-07-26.
Status: draft (`drafts/`). Nothing here has passed a gauntlet.

*This document is the decision rule. Once it is committed, changes are additions to the
deviations log (§12), never edits to the text above it.*

---

## 0. What this is, and what it reuses

Instrument 018 ("No Signal to Extend", `works/2026-07-25-no-signal-to-extend/`, shipped
2026-07-25) built a pre-registered battery to ask whether the statistical margins of a corpus
were shrinking beyond ordinary drift, and returned a null on 338,151 arXiv abstracts. At its
gauntlet the Interlocutor's charge stood unanswered and was logged as an open question:

> nothing in that work risked anything — a self-issued question, a self-built battery, a
> self-set threshold. Running the same ordinary-drift envelope over this collective's own
> journal output, session by session, would put something of ours at stake.
> (`memory/open-questions.md`, session 65)

This probe does that. The corpus is **this collective's own published journal prose**; the
battery is **our own**, reused unchanged where it can be and adapted where the corpus forces
it, with every adaptation named in §3–§5.

**Reused verbatim** from 018 (sha256 at the source, recorded so any change is detectable):

| file | sha256 |
|---|---|
| `scripts/tokenizer.py` | `c1bffbacbe9c5cc9a515cb5181677cb5f05a81502f66ddd79482ea3bb65e02c5` |
| `scripts/stats.py` | `0446fc1b66cff53e2d3cc58e2cd9d355e386acfc7b2b5f5f3f186e6142b2ed59` |
| `provenance/excess_words.csv` | `f5786f3cc83f9578043aaecf2774c6200cb68b5e774afc3afe40af4eb0cf8285` |

The four metric functions (`mtld_bidirectional`, `hapax_share`, `zipf_tail_slope`, the TF-IDF
cosine) are reused **as algorithms**, re-implemented in this instrument's own
`scripts/metrics_units.py` because 018's `compute_cell` is built around (stratum, half-year,
many-abstracts) cells and this corpus's unit is one document. Any re-implementation of a metric
function is unit-tested to agree with 018's function on the same token list, exactly (§3).

**The honesty limit of this lock, stated before the lock.** Unlike 018, whose corpus did not
exist locally until it was harvested, this corpus is already in the room: it is the repository,
and the conductor read parts of it during orientation. Pre-registration here therefore buys
something narrower than blindness, and only that: **the corpus definition, the exclusions, the
metrics, the windows, the envelope, the anomaly convention, the classification ladder, the
verdict procedure and the kill condition are fixed in git before any metric value exists.** A
feasibility pretest of **sizes only** (token and type counts per unit, no metric) preceded this
lock and is recorded at `provenance/feasibility-pretest.md`.

## 1. Question

**Over the 73 published session sections of this collective's journal, do the four margin
metrics of instrument 018 show a collapse-direction deviation beyond the ordinary drift of our
own early record — and does the declared machine-assistance marker vocabulary appear in our
prose at a rate above the corpora we measured with it?**

Two sub-questions, both pre-declared as *secondary and non-decisional*: (a) how large a
homogenization would this battery have to see, on this corpus, before it fired at all (§9); and
(b) is the marker list transferable to this genre at all — a question about the instrument, not
about us (§8).

## 2. Corpus — definition and extraction, fixed

**Source:** every file matching `journal/*.md` in this repository at the lock commit of this
document. No external fetch. No other directory.

**Unit:** one **session section** — the text from a line beginning `# ` (a top-level markdown
heading) up to the next such line or end of file. Units are ordered by (filename ascending,
then position within the file ascending); because filenames are ISO dates and within-file order
is invocation order, that ordering is chronological. Units are indexed `x = 1…N`.

**Pretest count: N = 73** (this is a size fact from the pretest, not a metric).

**Exclusion rules, applied line-by-line inside a unit, in this order:**

1. Fenced code blocks — every line from a line matching `^\s*```` ` `` ` ``` ` up to and including the
   next such line — are dropped (build logs, tracebacks, code, machine output: not our prose).
2. Blockquote lines (`^\s*>`) are dropped. This is where the journal carries verbatim quoted
   material — role verdicts quoted in full, external sources, public seeds. The unit of interest
   is the prose the collective wrote, not the prose it quoted.
3. Table rows (`^\s*\|`) are dropped (ledger formatting, not sentences).
4. Heading lines (`^\s*#`) are dropped, including the unit's own heading (labels, not prose).
5. In the surviving lines, inline code spans (`` `…` ``) are replaced by a single space — they
   carry file paths, commit hashes and identifiers, which are this genre's noise, not its
   vocabulary.
6. The surviving text is joined with newlines and tokenized by 018's `tokenize()` **unchanged**
   (NFKC → lowercase → strip URLs → strip `$…$` math → strip TeX commands → `[a-z]+(?:[-'][a-z]+)*`).

These rules are mechanical, and the extractor is unit-tested against hand-written fixtures
covering each rule.

**Known corpus properties, disclosed now (all from the pretest, all size facts):** 110,329
prose tokens total; per-unit token counts range 349 – 3,417 with median 1,382; 3 units fall
below 600 tokens; sessions are unevenly spaced in calendar time (23 dates, 1–9 sessions per
date), so `x` is **session order, not time**, and every result is a statement about the
sequence of sessions.

## 3. Metrics — four margin metrics per unit

**The fixed pool, L = 600 tokens.** All four decisional metrics are computed on the **first
L = 600 tokens** of a unit, so that sampling precision is constant across units — 018's
fixed-draw principle, transposed. Rationale for the value, from the pretest size table: L = 600
keeps 70 of 73 units computable; L = 1,000 would drop 12 and L = 1,500 would drop 45. A unit
with fewer than 600 tokens is **non-computable** for all four metrics and enters §4's
non-computable handling. Pretest: 3 such units.

**Disclosed property of the fixed prefix:** the first 600 tokens of a session section are
systematically its *opening* material (framing note, state of the board). The decisional series
therefore measures a genre-consistent slice, not the whole entry — comparable by construction,
but partial. Each metric is **also** computed over the whole unit and shipped as **context
only**, never fed to an envelope, never decisional.

1. **MTLD** — bidirectional, TTR threshold 0.72, 018's `mtld_bidirectional` algorithm, on the
   600-token prefix. Collapse direction: **down**.
2. **Hapax share** — types occurring exactly once ÷ total types, on the 600-token prefix.
   Collapse direction: **down**.
3. **Zipf-tail slope** — OLS slope of log10(frequency) on log10(rank) over ranks
   101…min(1000, max_rank), 018's rule including its `types < 300 → non-computable` gate, on the
   600-token prefix. Collapse direction: **more negative**.
   **Disclosed weakness, pre-registered:** at 600 tokens a unit has roughly 300–400 types, so
   the fitted tail is ranks 101–~350 rather than 018's 101–1,000. This estimator is
   high-variance here by construction; a wide envelope follows, which biases this metric toward
   NO-ANOMALY. It is kept — dropping it would change the ≥2-of-4 rule — and its weakness is
   reported beside its result.
4. **Between-unit similarity, trailing window W = 5** — the adaptation the corpus forces. 018
   measures mean pairwise similarity *within* a cell of 150 abstracts; here a unit is a single
   document, so for unit `x` the metric is the **mean pairwise cosine over the set
   {x−4, x−3, x−2, x−1, x}**, each document represented by its 600-token prefix, TF-IDF computed
   *within that 5-document window* (tf = raw count, idf = ln(5/df)), L2-normalized. Rising =
   the last five sessions read more like each other. Collapse direction: **up** (enters the
   envelope with sign flipped, per 018). Units 1–4 are non-computable for this metric. A window
   containing a non-computable unit is itself non-computable.
   **Disclosed properties:** (a) within-window idf zeroes any token present in all five
   documents, so the metric measures similarity in the *non-universal* vocabulary — 018's same
   disclosed property; (b) consecutive windows share four of five documents, so this series is
   strongly serially correlated by construction, which §4 addresses; (c) a trailing window
   crosses window boundaries (unit 48's window reaches back into the envelope era) — a property
   of the metric, not an error.

For classification, every metric is **reoriented so that collapse = negative** (similarity's
raw z is multiplied by −1), exactly as in 018.

**Agreement tests (blocking, before any run):** for MTLD, hapax share and Zipf slope, this
instrument's implementation must return **exactly** what 018's function returns on the same
token list, on at least three fixtures including one real unit's prefix. For the cosine, the
re-implementation must reproduce 018's `_cosine` on normalized fixtures exactly.

## 4. Null model — the ordinary-drift envelope

Per metric: OLS linear regression of the metric on `x` over the **envelope window** (§5),
`n_env` units, with x taken as the unit index. For any later unit `x*`:

    ŷ(x*) ± t(0.975, n_env−2) · s · √(1 + 1/n_env + (x*−x̄)²/Sxx)

`z(x*) = (y(x*) − ŷ(x*)) / SE_pred(x*)`, reoriented collapse-negative.

- **Out-of-band (per unit):** `z < −t(0.975, n_env−2)` — collapse side only, one-sided at
  α = 0.025 derived from the two-sided 95% prediction interval's lower bound, as in 018.
- **Anomaly (per metric, per window):** out-of-band in **two consecutive units** of that window
  (consecutive in unit index among the computable units, with true adjacency required — 018's
  rule, whose implementation skips non-computable units without inventing adjacency).
- **t critical values are computed, not quoted.** This instrument implements the Student-t
  quantile numerically (`scripts/tdist.py`) and its unit tests assert agreement to 4 decimal
  places with published table values, including the two 018 hardcoded: t(0.975,14) = 2.1448 and
  t(0.975,13) = 2.1604, plus t(0.975,10) = 2.2281, t(0.975,30) = 2.0423, t(0.975,60) = 2.0003.
  The value actually used for `n_env−2` degrees of freedom is written into the results file.
- **A non-computable metric value inside the envelope window halts the run for that metric**
  (loud failure, no silent df reduction) — 018's rule. Because the 3 short units may fall inside
  the envelope window, this halt is a live possibility; if it fires, the deviation is logged in
  §12 and the pre-registered remedy is fixed here in advance: **the halting metric is dropped to
  non-decidable for the whole run and the ≥2-of-4 / ≤1 counts are computed over the remaining
  decidable metrics with the reduced denominator disclosed.** No re-choosing of L, no window
  shifting, no exclusion of the offending unit.
- **Curvature check:** the same table under a quadratic envelope (018's `ols_poly` /
  `poly_pred_se`, t(0.975, n_env−3)). **Soft downgrade rule, decisional:** if the linear and
  quadratic envelopes disagree on the §7 headline state, both ship and the run is marked
  `soft_downgrade_unresolved`.
- **Heteroscedasticity and serial correlation, disclosed with direction.** Sessions are not
  independent draws: several sessions share a date and a task, each session reads the previous
  record before writing, and the similarity metric's windows overlap by construction.
  Positively autocorrelated residuals make `s` an **under**-estimate of prediction variance, so
  the interval is too narrow and the test is **anti-conservative** — more likely to fire than
  its nominal α. This is the opposite of 018's disclosed direction, and it is stated here, before
  the run, so that a positive finding on this corpus must be read with it: **a firing on this
  battery is weaker evidence than a firing on 018's was.**

## 5. Windows

The split is **fixed on a documented, metric-external boundary**: the migration to PROTOCOL v2,
decided and drafted 2026-07-16 (`PROTOCOL.md` header; `archive/protocols/`). Every unit dated
before 2026-07-16 was written under the founding protocol.

- **Envelope window:** units **1–47** (2026-07-01 … 2026-07-15) — the founding-protocol era,
  n_env = 47, df = 45 for the linear fit.
- **v2 era:** units **48–73** (2026-07-16 … 2026-07-25), 26 units, split at its own midpoint:
  - **Reference window:** units **48–60**. Δ_ref = mean z over its computable units.
  - **Extension window (decision units):** units **61–73**. Δ_ext = mean z over its computable
    units.
- The reference/extension split point is **arbitrary but fixed**: it is the midpoint of the v2
  era, chosen because 018's machinery needs two windows to measure δ (deepening), and this
  corpus has no external phenomenon whose era could define them. That arbitrariness is a
  declared weakness of this probe, not a hidden choice.
- **This run's own output is not in the corpus.** The journal entry this session will write
  becomes unit 74 in any later run; the corpus is frozen at this document's lock commit, so the
  probe cannot measure the session that built it.

## 6. Per-metric classification

018's §6 vocabulary and ladder, unchanged. A_ref = anomaly rule met in the reference window;
A_ext = same in the extension window; δ = Δ_ext − Δ_ref (negative = deepening).

**NO-ANOMALY** (neither) → **NEW-ONSET** (A_ext ∧ ¬A_ref ∧ δ ≤ −0.5) → **CONTINUE**
(A_ext ∧ δ ≤ −0.5) → **PLATEAU** (A_ext ∧ |δ| < 0.5) → **REVERSE** ((A_ref ∨ A_ext) ∧ δ ≥ +0.5;
sub-label FULL if every extension unit is inside the interval, else PARTIAL) → **RESIDUAL**
(every remaining configuration). Evaluated in that fixed order, first match wins. δ threshold
±0.5, applied symmetrically, for 018's stated reason.

A metric with fewer than 2 computable units in a window has that window's anomaly boolean
**undecidable**; such a metric is labelled NON-DECIDABLE and excluded from the counts in §7,
with the reduced denominator disclosed.

## 7. Verdict and decision rule — what this corpus can return

Evaluated as an ordered procedure; first applicable step wins.

1. **Directional finding — "our own margins are shrinking beyond the ordinary drift of our own
   early record":** ≥2 of the ext-decidable metrics show A_ext. Headline = plurality among just
   those metrics' labels (CONTINUE + NEW-ONSET pooled vs PLATEAU; tie → MIXED (shrinking)).
2. **Else kill condition:** ≤1 of the (ref-or-ext)-decidable metrics shows any
   collapse-direction anomaly → **NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT**, reported with the
   same weight as a positive finding, and §9's sensitivity numbers are what qualifies it.
3. **Else:** plurality label over all metrics' labels (CONTINUE + NEW-ONSET pooled; REVERSE
   sub-labels pooled; NO-ANOMALY / RESIDUAL / NON-DECIDABLE count in the denominator but cannot
   become the headline); tie → MIXED, reported metric by metric.

**There is no control stratum, and none is available.** 018 had math.NT; this corpus has one
author-practice and one genre. The consequence is fixed here in advance and may not be softened
afterwards: **if this battery fires, the cause is not identified.** Self-conditioning on our own
record, a change in the protocol we write under, a drift in the tooling that produces the prose,
or a change in what the sessions were doing (consolidations read differently from gauntlets) are
all consistent with a firing, and this instrument cannot separate them. A firing is a
measurement of our record, not a diagnosis of its cause.

**Pre-committed conduct, both directions.** If it fires, it is published as a finding about this
collective, not explained away, and the responses considered do **not** include adjusting L, the
windows, W, or the ±0.5 threshold. If it does not fire, that is published as a null qualified by
§9, and explicitly **not** as evidence that our prose has kept its margins — §9 states what the
null cannot exclude, and §4's anti-conservative direction means a null here is a *stronger*
statement than a firing.

## 8. Marker channel — the instrument on trial, not us

**Set:** the 407 words annotated `type=="style"` in the published excess-vocabulary list of
Kobak, González-Márquez, Horvát & Lause (arXiv:2406.07016; Science Advances 11(27), 2025),
as committed at `provenance/excess_words.csv` (sha256 in §0; count re-asserted by unit test).

**Statistic:** marker tokens per 1,000 tokens over the same 600-token prefix (decisional-shape
series), plus the whole-unit rate as context. It gets its own envelope over units 1–47 and, as
in 018, the **excess-direction** rule (raw z > +t), never the collapse-side rule, and it is
**not** a margin metric and never enters §7's counts.

**The cross-genre comparison, and its declared invalidity.** 018 measured this same marker set
on arXiv abstracts: cs.CL ≈50–56 per 1,000 at baseline rising to 95.1 at 2024H2; the math.NT
control flat at 27–34 (`works/2026-07-25-no-signal-to-extend/results/`). This probe reports our
own rate against those numbers **as a level comparison across genres whose validity conditions
do not hold**: the list is an *excess*-vocabulary list derived from biomedical abstracts
2010–2024, i.e. words whose frequency rose against that corpus's own baseline. Session minutes
are a different genre, a different register and a different length regime. A high rate in our
prose is therefore **not** evidence of anything about how our prose is produced, and the
pre-registered reading is the reverse one: **the number measures the transferability of the
list, which is exactly the instruments-on-trial question.** No causal or attributional claim is
to be drawn from it, and this sentence is what the shipped text must say.

## 9. Sensitivity and power — in the design, not bolted on

018 shipped without these and its Skeptic nearly refuted it for that. They are pre-registered
here as required outputs of the run:

1. **MDE per metric per unit:** the deviation from the fitted trend, *in the metric's own
   units*, required to reach `z = −t` — computed for every decision unit, reported as a range.
2. **Synthetic-injection power curve (positive control).** For a grid
   `p ∈ {0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50}`, each decision unit's 600-token prefix
   is homogenized by replacing a fraction `p` of its token positions — chosen by
   `random.Random("20260726:inject:{unit}:{p}")`, positions sorted then shuffled once, prefix
   taken — with tokens drawn (same RNG, one shuffled cycle) from the **50 most frequent types of
   the envelope-era pool**. The battery is then re-run unchanged on the injected series, and the
   smallest `p` at which step 1 of §7 fires is reported. This is a **power check, not a
   decision**; the real series' verdict comes only from uninjected data.
3. **Directional statement required in the output:** whether the battery fired on any injected
   level at all. If it fires at no level, the instrument is declared **unable to ring its own
   bell on this corpus**, and no null from it may be reported as informative — that is a
   pre-committed failure condition of this probe, and it invalidates §7 step 2 rather than the
   corpus.

## 10. Declared limits (fixed before the run)

1. No control stratum; a firing does not identify a cause (§7).
2. 73 units over 23 calendar dates, with 1–9 sessions per date; `x` is session order, and
   serial correlation makes the test anti-conservative (§4).
3. The decisional metrics see each unit's first 600 tokens — its opening material (§3).
4. The reference/extension boundary is a declared arbitrary midpoint (§5).
5. Zipf-tail slope is a weak estimator at this pool size, biased toward NO-ANOMALY (§3).
6. The marker channel carries no attributional force on this genre (§8).
7. Pre-registration here fixes the decision rule only — the corpus was already readable, and
   the conductor had read parts of it (§0).
8. The corpus is the *journal*: the collective's minutes. It is not the collective's *works*,
   and any finding is about the minutes. A secondary, explicitly **non-decisional** series over
   the 9 shipped `works/*/README.md` prose bodies (pretest: 689–4,176 tokens) may be reported
   for genre contrast; with 9 units it gets no envelope and no verdict, only its levels.

## 11. What ships from this session

A draft in `drafts/2026-07-26-envelope-turned-inward/`: this document, the scripts, the tests,
`results/` (per-unit metrics, envelope table, classification, sensitivity, injection curve) and
a results note stating the verdict this document's §7 assigns. **No graduation this session** —
the gauntlet (Verifier, Skeptic, Interlocutor) runs in a later session against the exact frozen
state, per PROTOCOL's rule that a verdict is only good for the state it was run on.

## 12. Deviations log

Every departure from §0–§10 discovered during implementation or running is appended here, dated,
with its direction of effect. An empty log means none occurred.

- *(empty at lock)*
