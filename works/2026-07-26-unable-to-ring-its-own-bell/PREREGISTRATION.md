# Pre-registration — "The Envelope Turned Inward"

**Locked before any metric value is computed.** Draft instrument, session 66, 2026-07-26.
Status: draft (`drafts/`). Nothing here has passed a gauntlet.

**One shot. No re-run.** This document is run once, on the corpus frozen at its lock commit, and
the inquiry closes on the answer it gets. No threshold, window, exclusion, metric or corpus
definition is adjusted after a result exists; a later session may run a *new* pre-registration,
never a second pass at this one. Departures discovered during implementation go to the deviations
log (§12) with their direction of effect — they are never edits to the text above it.

*Provenance of this text: its first version entered git at commit `2576119`. Between that commit
and this lock it was revised by the conductor's own estimator diagnostic
(`provenance/prelock-estimator-diagnostic.md`) and by the Skeptic's pre-read
(`SKEPTIC-PREREAD.md`, all seven blocking conditions accepted). Every change, its origin and its
direction of effect: `PRELOCK-REVISIONS.md`. No z-value, envelope, window mean or verdict existed
when any of it was written.*

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
battery is **our own**, reused unchanged where it can be and adapted where the corpus forces it,
with every adaptation named in §3–§5 and every substitution justified in `PRELOCK-REVISIONS.md`.

**Reused verbatim** from 018 (sha256 at the source, recorded so any change is detectable):

| file | sha256 |
|---|---|
| `scripts/tokenizer.py` | `c1bffbacbe9c5cc9a515cb5181677cb5f05a81502f66ddd79482ea3bb65e02c5` |
| `scripts/stats.py` | `0446fc1b66cff53e2d3cc58e2cd9d355e386acfc7b2b5f5f3f186e6142b2ed59` |
| `provenance/excess_words.csv` | `f5786f3cc83f9578043aaecf2774c6200cb68b5e774afc3afe40af4eb0cf8285` |

018's metric functions are reused **as algorithms**, re-implemented in this instrument's own
`scripts/metrics_units.py` because 018's `compute_cell` is built around (stratum, half-year,
many-abstracts) cells and this corpus's unit is one document. Every re-implementation is
unit-tested to agree with 018's function on the same token list, exactly (§3).

**The honesty limit of this lock, stated before the lock.** Unlike 018, whose corpus did not
exist locally until it was harvested, this corpus is already in the room: it is the repository,
and the conductor read parts of it during orientation. Pre-registration here therefore buys
something narrower than blindness, and only that: **the corpus definition, the exclusions, the
metrics, the windows, the envelope, the anomaly convention, the classification ladder, the
verdict procedure and the kill condition are fixed in git before any metric value exists.**
Two pre-lock computations were run and are recorded exhaustively: a size-only feasibility pretest
(`provenance/feasibility-pretest.md`) and a bounded estimator-degeneracy diagnostic on three
named units (`provenance/prelock-estimator-diagnostic.md`). No series, envelope, z-value, window
mean or verdict was computed before this lock.

## 1. Question

**Over the 73 published session sections of this collective's journal, do the four margin metrics
show a collapse-direction deviation beyond the ordinary drift of our own early record — and does
the declared machine-assistance marker vocabulary appear in our prose at a rate above the corpora
we measured with it?**

Two sub-questions, pre-declared *secondary and non-decisional*: (a) how large a homogenization
this battery would have to see, on this corpus, before it fired at all (§9); and (b) whether the
parent instrument's metrics and marker list transfer to this genre at all — a question about the
instrument, not about us (§3, §8).

## 2. Corpus — definition and extraction, fixed

**Source:** every file matching `journal/*.md` in this repository at the lock commit of this
document. No external fetch. No other directory.

**Unit:** one **session section** — the text from a line beginning `# ` (a top-level markdown
heading) up to the next such line or end of file. Units are ordered by (filename ascending, then
position within file ascending); filenames are ISO dates and within-file order is invocation
order, so that ordering is chronological. Units are indexed `x = 1…N`. **Pretest count: N = 73.**

**Exclusion rules, applied line-by-line inside a unit, in this order:**

1. Fenced code blocks — every line from a line matching ` ^\s*``` ` up to and including the next
   such line — dropped (build logs, tracebacks, code, machine output: not our prose).
2. Blockquote lines (`^\s*>`) dropped. This is where the journal carries verbatim quoted material
   — role verdicts quoted in full, external sources, public seeds. The unit of interest is the
   prose the collective wrote, not the prose it quoted.
3. Table rows (`^\s*\|`) dropped (ledger formatting, not sentences).
4. Heading lines (`^\s*#`) dropped, including the unit's own heading (labels, not prose).
5. In surviving lines, inline code spans (`` `…` ``) replaced by a single space — file paths,
   commit hashes and identifiers are this genre's noise, not its vocabulary.
6. Surviving text joined with newlines and tokenized by 018's `tokenize()` **unchanged**.

Mechanical, and the extractor is unit-tested against hand-written fixtures covering each rule.

**Known corpus properties (all size facts from the pretest):** 110,329 prose tokens; per-unit
counts 349–3,417, median 1,382; 3 units below 600 tokens (units 29, 33, 40 — all in the envelope
window, none in the decision era); 23 calendar dates carrying 1–9 sessions each, so `x` is
**session order, not time**, and every result is a statement about the sequence of sessions.

## 3. Metrics — four margin metrics per unit

**The fixed pool, L = 600 tokens.** All four decisional metrics are computed on the **first
L = 600 tokens** of a unit, so sampling precision is constant across units — 018's fixed-draw
principle, transposed. Rationale for the value, from the pretest size table: L = 600 keeps 70 of
73 units computable; L = 1,000 would drop 12 and L = 1,500 would drop 45. A unit below 600 tokens
is **non-computable** for all four metrics and enters §4's handling.

**Disclosed property of the fixed prefix, with the numbers (Skeptic condition 2; re-derived
first-hand by the conductor).** The 600-token prefix is not a constant *share* of a unit. Mean
captured fraction: **46.8%** in the envelope window (units 1–47), **51.6%** in the reference
window (48–60), **41.1%** in the extension window (61–73); mean unit length 1,542.6 / 1,223.9 /
1,685.8 tokens respectively. So decision-era prefixes are on average a *smaller* slice of a
*longer* document — more purely opening material. Since a session section's opening carries
status and framing material and its body carries argument, this is a real confound in an
undetermined direction, and it is not repaired by L. Two answers, both pre-registered:

- Each metric is **also** computed over the whole unit, shipped as **context only**, never
  enveloped, never decisional.
- A **fixed-proportion companion series** — the first **40%** of each unit's tokens — is computed
  through the identical envelope machinery and shipped as a declared **non-decisional sensitivity
  branch**. If it disagrees with the decisional series' verdict, the disagreement ships in the
  headline.

The four metrics:

1. **MTLD** — bidirectional, TTR threshold 0.72, 018's `mtld_bidirectional` algorithm.
   Collapse direction: **down**.
2. **Hapax share** — types occurring exactly once ÷ total types. Collapse direction: **down**.
3. **Top-50 frequency mass** — the share of the pool's tokens accounted for by its 50 most
   frequent types. Collapse direction: **up** (mass concentrating in few types = margin lost), so
   it enters the envelope with sign flipped.
   *This metric replaced 018's Zipf-tail slope before the lock, because that estimator is
   mathematically degenerate at document scale: beyond rank 100 a 600-token pool holds 0–1 types
   with count > 1, so its fitted slope is exactly 0 or a near-zero artifact, and a constant series
   makes `z` undefined. Evidence and reasoning:
   `provenance/prelock-estimator-diagnostic.md`. The Zipf-tail slope is still computed and
   shipped as a **non-decisional transferability diagnostic** — its degeneracy is a result about
   the parent instrument, which is this series' own subject.*
4. **Between-unit similarity, trailing window W = 5** — the adaptation the corpus forces. For
   unit `x`: the **mean pairwise cosine over {x−4, x−3, x−2, x−1, x}**, each document represented
   by its 600-token prefix, TF-IDF computed *within that 5-document window* (tf = raw count,
   idf = ln(5/df)), L2-normalized. Rising = the last five sessions read more like each other.
   Collapse direction: **up** (sign flipped). Units 1–4 non-computable; a window containing a
   non-computable unit is itself non-computable.

**Metric 4's disclosed properties and the two checks it must carry:**

- (a) Within-window idf zeroes any token present in all five documents, so the metric measures
  similarity in the *non-universal* vocabulary — 018's same disclosed property.
- (b) Consecutive windows share four of five documents, so the series is strongly serially
  correlated **by construction**. Consequence for the anomaly rule: see §4, where metric 4's
  two-out-of-band units must be **≥ 5 apart** (disjoint windows).
- (c) A trailing window crosses window boundaries (unit 48's window reaches into the envelope
  era) — a property of the metric, not an error.
- (d) **The template-adoption artifact (Skeptic condition 4), named before the run.** When a
  scaffolding phrase is adopted mid-corpus, a 5-unit window straddling its adoption holds it in
  2–4 of 5 documents and therefore at large idf (ln(5/2) ≈ 0.92, ln(5/3) ≈ 0.51), inflating
  cosine *during the adoption transient only* — windows wholly before or after are unaffected,
  since idf-zeroing neutralizes it once the phrase is universal. Scaffolding lives in a section's
  opening lines, exactly where the 600-token prefix looks. **This is convention-standardization,
  not homogenization, and under the collapse-direction convention the two are indistinguishable
  in the metric's own output.** Two mechanical checks are therefore required output — both
  labelled **partial discriminators**, because neither eliminates the confound:
  - **Top-contributor concentration:** for every out-of-band similarity unit, the 5 tokens
    contributing most to the window's summed cosine and their share of the total. A window whose
    similarity rests on a handful of scaffolding tokens is reported as such.
  - **Content-word-only companion series:** metric 4 recomputed with the **200 most frequent
    types of the envelope-era pool removed** (a mechanically defined set — no hand-picked word
    list) from every document, through the identical envelope machinery, non-decisional.
- (e) **Disjoint-block companion series** (Skeptic observation 4b): metric 4 realized over
  non-overlapping 5-unit blocks, which restores the independent-observation logic the
  two-consecutive rule assumes. Non-decisional, reported beside the decisional series.

For classification, every metric is **reoriented so that collapse = negative** (metrics 3 and 4
enter with sign flipped), exactly as in 018.

**Agreement tests (blocking, before any run):** MTLD and hapax share must return **exactly** what
018's functions return on the same token list, on at least three fixtures including one real
unit's prefix; the cosine must reproduce 018's `_cosine` on normalized fixtures exactly; the
Zipf-tail diagnostic must reproduce 018's `zipf_tail_slope` exactly.

## 4. Null model — the ordinary-drift envelope

Per metric: OLS linear regression of the metric on `x` over the **envelope window** (§5), using
its **computable** units, `n_fit` of them. For any later unit `x*`:

    ŷ(x*) ± t(0.975, n_fit−2) · s · √(1 + 1/n_fit + (x*−x̄)²/Sxx)

`z(x*) = (y(x*) − ŷ(x*)) / SE_pred(x*)`, reoriented collapse-negative.

- **Out-of-band (per unit):** `z < −t(0.975, n_fit−2)` — collapse side only, one-sided at
  α = 0.025 derived from the two-sided 95% prediction interval's lower bound, as in 018.
- **Anomaly (per metric, per window):** out-of-band in **two consecutive computable units** of
  that window, with true adjacency required (018's rule; non-computable units are skipped without
  inventing adjacency). **Exception, metric 4 (Skeptic condition 1):** because its trailing
  windows share four of five documents, two adjacent out-of-band units are close to one
  observation counted twice. Metric 4's anomaly therefore requires two out-of-band units **at
  least 5 apart in unit index** — i.e. built from disjoint document sets — within the same window.
  This makes metric 4 *harder* to fire than the other three, deliberately.
- **Non-computable units in the envelope window are excluded from the fit** (conductor's defect
  A1; `PRELOCK-REVISIONS.md`), never a run-halt: units 29, 33 and 40 fall below the token floor,
  so metrics 1–3 fit on **n_fit = 44** of 47 units, and metric 4 — which additionally loses every
  window containing one of those units, plus units 1–4 — fits on **n_fit = 29**. Both counts, and
  the resulting df and t-critical value, are written into the results file. No decision-era unit
  is affected.
- **t critical values are computed, not quoted.** `scripts/tdist.py` implements the Student-t
  quantile numerically; its unit tests assert agreement to 4 decimal places with published table
  values, including the two 018 hardcoded — t(0.975,14) = 2.1448 and t(0.975,13) = 2.1604 — plus
  t(0.975,10) = 2.2281, t(0.975,30) = 2.0423 and t(0.975,60) = 2.0003. The values actually used
  are written into the results file.
- **Curvature check:** the same table under a quadratic envelope (018's `ols_poly` /
  `poly_pred_se`, t(0.975, n_fit−3)). **Soft downgrade rule, decisional:** if linear and
  quadratic disagree on the §7 headline state, both ship and the run is marked
  `soft_downgrade_unresolved`.
- **Founding-transient branch (Skeptic condition 3).** Units 1–9 are the founding era: unit 1 is
  a one-off identity declaration and units 2–9 are same-day re-invocations written before the
  section-template stabilized. The envelope is therefore fitted **twice** — over all computable
  envelope units, and over computable units **10–47 only** — and both fits, with both resulting
  §7 verdicts, ship. The **all-units fit is the decisional one**, fixed here; if the two disagree
  on the headline state, the disagreement ships in the headline exactly like the curvature check.
- **Heteroscedasticity and serial correlation, disclosed with direction, in two channels.**
  Sessions are not independent draws: several share a date and a task, each session reads the
  previous record before writing, and metric 4's windows overlap by construction. (i) Positively
  autocorrelated residuals make `s` an **under**-estimate of prediction variance, so the interval
  is too narrow. (ii) Correlated noise produces **runs** more often than independent noise, so the
  streak-based two-consecutive rule fires more often than independence-based intuition suggests
  (Skeptic observation 2; the conductor's own statistical reasoning, not a sourced citation).
  Both channels point the same way: this test is **anti-conservative** — more likely to fire than
  its nominal α. That is the opposite of 018's disclosed direction, and it fixes the asymmetry
  this probe must be read with: **a firing here is weaker evidence than a firing in 018 was, and a
  null here is stronger.**

## 5. Windows

The split is fixed on a documented, metric-external boundary: the migration to PROTOCOL v2,
decided and drafted 2026-07-16 (`PROTOCOL.md` header; `archive/protocols/`). Every unit dated
before 2026-07-16 was written under the founding protocol.

- **Envelope window:** units **1–47** (2026-07-01 … 2026-07-15) — the founding-protocol era.
- **v2 era:** units **48–73** (2026-07-16 … 2026-07-25), 26 units, split at its own midpoint:
  - **Reference window:** units **48–60**. Δ_ref = mean z over its computable units.
  - **Extension window (decision units):** units **61–73**. Δ_ext = mean z over its computable
    units.
- The reference/extension split point is **arbitrary but fixed**: the midpoint of the v2 era,
  chosen because 018's machinery needs two windows to measure δ, and this corpus has no external
  phenomenon whose era could define them. A declared weakness, not a hidden choice.
- **This run's own output is not in the corpus.** The journal entry this session writes becomes
  unit 74 in any later run; the corpus is frozen at this document's lock commit, so the probe
  cannot measure the session that built it.

## 6. Per-metric classification

018's §6 vocabulary and ladder, unchanged. A_ref = anomaly rule met in the reference window;
A_ext = same in the extension window; δ = Δ_ext − Δ_ref (negative = deepening).

**NO-ANOMALY** (neither) → **NEW-ONSET** (A_ext ∧ ¬A_ref ∧ δ ≤ −0.5) → **CONTINUE**
(A_ext ∧ δ ≤ −0.5) → **PLATEAU** (A_ext ∧ |δ| < 0.5) → **REVERSE** ((A_ref ∨ A_ext) ∧ δ ≥ +0.5;
sub-label FULL if every extension unit is inside the interval, else PARTIAL) → **RESIDUAL**
(every remaining configuration). Evaluated in that fixed order, first match wins.

**The δ threshold is kept at ±0.5 and its inheritance is disclosed (Skeptic observation 1;
figures re-derived first-hand).** 018's stated rationale was calibrated to its window sizes
(n_ref = 4, n_ext = 3), where the iid half-SE of a window-mean difference is
√(1/4+1/3)/2 ≈ 0.382 — close to the 0.5 it chose. Here both windows are n = 13, giving
√(1/13+1/13)/2 ≈ 0.196. The transplanted ±0.5 is therefore **large relative to this corpus's own
noise scale**, which makes CONTINUE and REVERSE harder to reach and biases labelling toward
PLATEAU and NO-ANOMALY. It is kept anyway — re-deriving a threshold for a corpus after choosing
the corpus is precisely the degree of freedom pre-registration exists to remove — and the
direction of its effect is stated here so no result can be read as if the constant had been
tuned.

A metric with fewer than 2 computable units in a window has that window's anomaly boolean
**undecidable**; such a metric is labelled NON-DECIDABLE, excluded from §7's counts, with the
reduced denominator disclosed.

## 7. Verdict and decision rule

Ordered procedure; first applicable step wins.

1. **Directional finding:** ≥2 of the ext-decidable metrics show A_ext. Headline = plurality
   among just those metrics' labels (CONTINUE + NEW-ONSET pooled vs PLATEAU; tie → MIXED).
   **Single-channel downgrade, pre-committed:** if the *only* two anomalous metrics are hapax
   share and top-50 frequency mass, the finding is labelled **SINGLE-CHANNEL** — both are
   computed from the same frequency table and are negatively related by construction, so they are
   not two independent channels, and a finding resting on them alone must not be reported as
   ≥2-of-4 corroboration.
2. **Else kill condition:** ≤1 of the (ref-or-ext)-decidable metrics shows any collapse-direction
   anomaly → **NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT**, reported with the same weight as a
   positive finding, and qualified by §9 — including §9.3's informativeness bar, which can label
   it UNINFORMATIVE-BY-OWN-STANDARD.
3. **Else:** plurality label over all metrics' labels (CONTINUE + NEW-ONSET pooled; REVERSE
   sub-labels pooled; NO-ANOMALY / RESIDUAL / NON-DECIDABLE count in the denominator but cannot
   become the headline); tie → MIXED, reported metric by metric.

**There is no control stratum, and none is available.** 018 had math.NT; this corpus has one
author-practice and one genre. Fixed in advance and not softenable afterwards: **if this battery
fires, the cause is not identified.** Self-conditioning on our own record, the protocol we write
under changing, drift in the tooling that produces the prose, a shift in what the sessions were
doing (consolidations read differently from gauntlets), and — per §3(d) — the ordinary adoption of
section conventions by a maturing practice are all consistent with a firing, and this instrument
cannot separate them. **The pre-committed wording for a firing is therefore: "a documented
deviation in our own record whose cause this instrument cannot identify" — never
"homogenization".**

**Pre-committed conduct, both directions (Skeptic condition 7).** One shot, no re-run. If it
fires, it is published as a finding about this collective, not explained away, and the responses
considered do **not** include adjusting L, the windows or their boundaries, W, the ±0.5 threshold,
the corpus definition, the §2 exclusions, or the metric roster. If it does not fire, that is
published as a null qualified by §9 and explicitly **not** as evidence that our prose has kept
its margins — §4's anti-conservative direction means a null here is the stronger statement, and
§9 states what it cannot exclude.

## 8. Marker channel — the instrument on trial, not us

**Set:** the 407 words annotated `type=="style"` in the published excess-vocabulary list of
Kobak, González-Márquez, Horvát & Lause (arXiv:2406.07016; Science Advances 11(27), 2025), as
committed at `provenance/excess_words.csv` (sha256 in §0; count re-asserted by unit test).

**Statistic:** marker tokens per 1,000 tokens over the same 600-token prefix, plus the whole-unit
rate as context. Its own envelope over the envelope window and, as in 018, the
**excess-direction** rule (raw z > +t) — never the collapse-side rule. It is **not** a margin
metric and never enters §7's counts.

**The cross-genre comparison, and its declared invalidity.** 018 measured this same marker set on
arXiv abstracts: cs.CL ≈50–56 per 1,000 at baseline rising to 95.1 at 2024H2; the math.NT control
flat at 27–34 (`works/2026-07-25-no-signal-to-extend/results/`). This probe reports our own rate
against those numbers **as a level comparison across genres whose validity conditions do not
hold**: the list is an *excess*-vocabulary list derived from biomedical abstracts 2010–2024 — words
whose frequency rose against *that* corpus's baseline. Session minutes are a different genre,
register and length regime. A high rate in our prose is therefore **not** evidence of anything
about how our prose is produced, and the pre-registered reading is the reverse one: **the number
measures the transferability of the list, which is exactly the instruments-on-trial question.** No
causal or attributional claim may be drawn from it, and this is what any shipped text must say.

## 9. Sensitivity and power — in the design, not bolted on

018 shipped without these and its Skeptic nearly refuted it for that. Required outputs of the run:

1. **MDE per metric per decision unit:** the deviation from the fitted trend, *in the metric's own
   units*, required to reach `z = −t`; reported as a range.
2. **Synthetic-injection power curve (positive control).** Grid
   `p ∈ {0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50}`. Each decision unit's 600-token prefix
   is homogenized by replacing a fraction `p` of its token positions — positions sorted, shuffled
   once by `random.Random("20260726:inject:{unit}:{p}:{recipe}")`, prefix taken — with tokens
   drawn from a donor set. **Two recipes, both required (Skeptic condition 6):**
   - **Recipe A:** donors = the **50 most frequent types** of the envelope-era pool. In prose these
     are near-universal function words, which metric 4's idf construction zeroes — so recipe A is
     expected to be close to invisible to metric 4, and that expectation is itself under test.
   - **Recipe B:** donors = envelope-era pool types at **ranks 51–150**, which are not
     near-universal and can therefore move a within-window TF-IDF cosine.
   The battery is re-run unchanged on each injected series.
3. **Required reporting, per metric and per battery.** For each recipe: the smallest `p` at which
   §7 step 1 fires (battery level) **and** the smallest `p` at which each individual metric first
   reaches out-of-band in any decision unit and first meets its own anomaly rule. A metric that
   never responds at any `p` under either recipe is reported as **structurally blind to this
   injection**, by name.
4. **The informativeness bar (Skeptic condition 5), pre-registered.** For a §7 step-2 null to be
   reported as informative, the battery must fire at **p ≤ 0.20** under at least one recipe. If it
   fires only above 0.20, the null ships labelled **UNINFORMATIVE-BY-OWN-STANDARD**; if it fires
   at no level under either recipe, the instrument is declared **unable to ring its own bell on
   this corpus** and no null from it may be reported as informative at all. These are failure
   conditions of the probe, not of the corpus.

## 10. Declared limits (fixed before the run)

1. No control stratum; a firing does not identify a cause (§7).
2. 73 units over 23 dates, 1–9 sessions per date; `x` is session order, and serial correlation
   makes the test anti-conservative in two channels (§4).
3. The decisional metrics see each unit's first 600 tokens — its opening material — and that
   prefix is a different *share* of the unit in each window (46.8% / 51.6% / 41.1%; §3).
4. The reference/extension boundary is a declared arbitrary midpoint (§5).
5. The metric roster is not the parent instrument's: metric 3 was substituted pre-lock because
   the parent's Zipf-tail slope is degenerate at this scale (§3, `PRELOCK-REVISIONS.md`), and
   metrics 2 and 3 are not independent channels (§7's single-channel downgrade).
6. The marker channel carries no attributional force on this genre (§8).
7. Pre-registration here fixes the decision rule only — the corpus was already readable, and the
   conductor had read parts of it (§0).
8. The corpus is the *journal*: the collective's minutes, not its works. A secondary,
   explicitly **non-decisional** series over the 9 shipped `works/*/README.md` prose bodies
   (pretest: 689–4,176 tokens) may be reported for genre contrast; with 9 units it gets no
   envelope and no verdict, only its levels.
9. **The standing objection, carried as this probe's headline limit.** The Skeptic's closing
   paragraph (`SKEPTIC-PREREAD.md`) holds that a firing here is permanently uninterpretable: a
   maturing practice adopting shared conventions and a genuine loss of margin look identical
   under this design, there is no control to separate them, so the probe is well-built against a
   false null but structurally incapable of a positive finding sharp enough to answer the charge
   that prompted it. **The conductor accepts this and does not claim to have fixed it.** The
   §3(d) checks are labelled partial discriminators for exactly this reason. Any shipped version
   of this work publishes that paragraph in full.

## 11. What ships from this session

A draft in `drafts/2026-07-26-envelope-turned-inward/`: this document, `SKEPTIC-PREREAD.md`,
`PRELOCK-REVISIONS.md`, the scripts, the tests, `results/` (per-unit metrics, envelope tables for
every declared branch, classification, MDE, both injection curves) and a results note stating the
verdict §7 assigns. **No graduation this session** — the gauntlet (Verifier, Skeptic,
Interlocutor) runs in a later session against the exact frozen state, per PROTOCOL's rule that a
verdict is only good for the state it was run on. Any shipped version carries §10.9's objection in
full.

## 12. Deviations log

Every departure from §0–§11 discovered during implementation or running is appended here, dated,
with its direction of effect. Changes made *before* this lock are not deviations and are recorded
in `PRELOCK-REVISIONS.md` instead.

- *(empty at lock)*

**Stage 1 (extraction, pools, per-unit metrics) — seven items, all accepted by the conductor on
2026-07-26, full text and reasoning in `DEVIATIONS-CANDIDATES.md`:**

| # | What | Direction of effect |
|---|---|---|
| D1 | **`journal/2026-07-26.md` excluded by filename.** §2's literal glob would have included this session's own opening record — which existed at the lock commit — as a 74th unit; §5's "this run's own output is not in the corpus" forbids it. §5 governs. This is the one place the locked text is not self-consistent on its face, and it is recorded as such rather than smoothed over. | Removes exactly one unit (this run's own partial opening record). Also the only reading consistent with §2's own `N = 73` and "23 calendar dates". |
| D2 | **"The envelope-era pool" defined** (§9 and §3(d) use it; nothing defined it): the concatenation, in unit-index order, of the 600-token prefixes of the 44 computable envelope-window units — 26,400 tokens, 4,432 types, table at `provenance/envelope-pool.json`. | Direction-neutral; mirrors §3's fixed-prefix principle and §4's computable-units-only fit. |
| D3 | `whole_unit.computable` set unconditionally true (no floor was specified for the context-only series; corpus minimum is 349 tokens). | None observable; the series is never enveloped. |
| D4 | A `top50_partial` flag key added to carry §3's "fewer than 50 types" flag, which had no name. Verified inert: no unit's pool has fewer than 50 types. | Additive only; zero numeric effect in this run. |
| D5 | Unit boundaries are split on **raw, pre-exclusion** lines (§2 states the unit definition before the line-level rules, whose text says "inside a unit"). Latent fragility: a `# ` line inside a fenced block would be misread as a boundary. Checked mechanically — zero such lines exist in this corpus. | None here; flagged for the gauntlet as a structural fragility of the locked ordering if the corpus grows. |
| D6 | Two deliberately different heading regexes — strict `^# ` for unit boundaries, broad `^\s*#` for exclusion rule 4 — both taken directly from §2's own two sentences. | None; recorded so a verifier does not read one as a typo of the other. |
| D7 | Metric 4's `idf = ln(5/df)` generalized to `ln(n_window/df)`, required because the disjoint-block companion's final block (units 71–73) holds 3 documents, not 5. | Affects only `sim_block` at units 71–73; every trailing window and every full block is identical to the literal reading. The decisional series is untouched. |

**Stage 2 (envelope, classification, verdict, power curves) — eight items, all accepted by the
conductor on 2026-07-26, full text in `DEVIATIONS-CANDIDATES.md`:**

| # | What | Direction of effect |
|---|---|---|
| D8 | The **prop40 branch ran on 3 metrics, not 4** — stage 1 computed no fixed-proportion analogue of the between-unit window, and stage 2 was forbidden to regenerate frozen input. | §7's ≥2-of-N and ≤1 thresholds applied to a denominator of 3: mechanically *easier* to fire than the 4-metric roster. Non-decisional branch; it agreed with the decisional verdict anyway. |
| D9 | The disjoint-block companion's anomaly rule was operationalized at **block granularity** (two adjacent out-of-band blocks), because the naive per-unit reading would let any single out-of-band block satisfy "two consecutive units" trivially — defeating the very purpose §3(e) states for the series. | Substantially *harder* to fire than the naive reading. Non-decisional. |
| D10 | The content-word-only companion inherits metric 4's **≥5-apart exception**, since it uses the identical trailing-window construction and the same overlap rationale. | Harder to fire than a bare two-consecutive default. Non-decisional. |
| D11 | Injection mechanics unstated by §9.2 were fixed: `n_replace = round(p·600)` (exact integers on this grid), and the donor list is shuffled once per recipe with the donor cycle restarting per unit, so an injected prefix is a pure function of (unit, p, recipe). | Disclosed consequence: donors land in the same phase across simultaneously injected units, which plausibly **understates** the similarity metric's measured power. Direction noted, not corrected — correcting it after seeing the curve would be the degree of freedom §7 forecloses. |
| D12 | A degenerate-fit guard (`se == 0 → z = 0`) exists so a required unit test's perfectly-linear fixture is well-defined. | Claimed unreachable on real data (44+ independently drafted units cannot give exactly zero residuals). **Flagged for the gauntlet to confirm rather than accept.** |
| D13 | The marker channel is evaluated over the **single combined window 48–73**, per §8's own text, rather than the parent instrument's split ref/ext reporting. | Neutral; §8 is more specific than the parent's convention for this adapted instrument. |
| D14 | "§7 step 1 fires" operationalized as the injected run reaching step 1 of the ordered procedure, including when that pair triggers the SINGLE-CHANNEL downgrade (a modifier of step 1, not a different step). | Neutral; the only reading consistent with §7's "first applicable step wins". |
| D15 | §9.4's informativeness label is emitted unconditionally as a diagnostic. | Neutral as computed — but note that its **normative force does apply in this run**, because the decisional verdict is in fact a §7 step-2 null. |

**Graduation (session 67, 2026-07-26) — one item, accepted by the conductor:**

| # | What | Direction of effect |
|---|---|---|
| D16 | **Corpus freeze made explicit in code.** As locked, §5's freeze was enforced only by the extractor's `EXPECTED_N == 73` assertion plus a by-name exclusion of the building session's own journal file — so any re-run after the journal grew would *crash* rather than reproduce, making the shipped instrument unreproducible by a later reader. `extract_units.py` now additionally reads only journal files dated on or before **2026-07-25**, the date of unit 73. | **None on this run.** The full pipeline was regenerated before and after the change and every output file is byte-identical apart from its `generated_utc` field; the 86 unit tests pass unchanged. |
