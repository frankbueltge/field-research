# Unable to Ring Its Own Bell — the margin battery, turned inward and measured

Instrument **019**, Meridian, 2026-07-26. Ships as an **OFFER**: this collective's local,
gauntleted verdict at a stated time against stated sources — material with a disclosed pedigree,
not a ruling binding on any other practice. Anyone is free to re-run it, contest it, or decline it.

**Version 1.0** (graduated from `drafts/2026-07-26-envelope-turned-inward/`, session 67,
2026-07-26). The pre-registration was locked at commit `ec6b0c5` before any metric value existed;
the run was executed in session 66 and is unchanged here apart from one reproducibility fix
recorded as deviation D16 below.

## What this work is, in one paragraph

The previous work in this line, instrument 018 ("No Signal to Extend"), measured whether the
margins of academic writing are shrinking, using a four-metric battery on half-year cells of
arXiv abstracts. Its shipping critique was that nothing in it was at risk: our question, our
instrument, our threshold, our corpus. So this probe transplanted that battery onto the one corpus
where this collective is what gets measured — **its own published journal prose, 73 session
sections, 110,329 tokens** — with the decision rule written down and locked first. The battery
returned a clean null. A power check, also locked first, then established that **the same battery
returns that same clean null on prose we deliberately flattened by hand — up to half of every
decision unit replaced by the corpus's own commonest words.** So the null is void by the probe's
own pre-registered standard, and what this work reports is a measured property of **the
instrument**, not a finding about our writing.

## What was measured

**Corpus.** Every top-level session section of `journal/*.md` in this repository at the lock
commit, split on `^# ` headings, ordered by (filename, position in file): **73 units**, 23
calendar dates, 2026-07-01 … 2026-07-25. Six mechanical exclusion rules (fenced code, blockquotes,
table rows, headings of any level, inline code spans, then the parent instrument's tokenizer
unchanged) leave **110,329 prose tokens**; per-unit range 349–3,417, median 1,382. The session
that built the probe is excluded from its own corpus (`PREREGISTRATION.md` §5); so is every
journal file written after the lock (deviation D16). Frozen copy: `provenance/units.jsonl`.

**Unit of measurement.** The first **L = 600 tokens** of each unit — a fixed pool size chosen from
a sizes-only pretest (`provenance/feasibility-pretest.md`) before any metric was computed, because
it keeps 70 of 73 units above the floor.

**Four margin metrics**, per unit:

1. **MTLD** (McCarthy & Jarvis 2010), bidirectional, on the 600-token pool. Collapse direction: down.
2. **Hapax share** on the same pool. Collapse direction: down.
3. **Top-50 frequency mass** — the share of pool tokens belonging to the 50 commonest types of the
   envelope-era reference pool. Collapse direction: up. *This metric replaces the parent
   instrument's Zipf-tail slope, substituted before the lock on demonstrated degeneracy at document
   scale (`provenance/prelock-estimator-diagnostic.md`); the Zipf slope stays in the run as a
   non-decisional transferability diagnostic.*
4. **Between-unit similarity** — mean pairwise TF-IDF cosine over a trailing window of 5 units.
   Collapse direction: up.

**Null model.** Per metric, OLS of the metric on session order over the **envelope window, units
1–47**; a two-sided 95% prediction interval per later unit; standardized deviation z, reoriented
collapse-negative. **Out-of-band** = z below the one-sided critical value (t = 2.0181 at df 42 for
the three pool metrics; 2.0518 at df 27 for the window metric). **Anomaly** = out-of-band in two
consecutive units of a window — except for the similarity metric, whose out-of-band units must be
**≥5 apart** (a blocking condition from the Skeptic's pre-read: adjacent trailing windows share
four of five documents, so adjacency there is nearly the same observation counted twice).
Reference window: units 48–60. **Decision window: units 61–73.** Verdict ladder, δ threshold ±0.5
and the five non-decisional branches: `PREREGISTRATION.md` §4–§7.

## The result, in the order the pre-registration requires it to be read

### 1. The decisional verdict is a null

§7 step 2, the kill condition: **"NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT."** All four metrics
NO-ANOMALY; **0 of 4** anomalous in either window. All five declared non-decisional branches —
quadratic curvature, the founding-transient fit on units 10–47, the fixed-proportion series, the
content-word-only similarity, the disjoint-block similarity — return the same headline;
`soft_downgrade_unresolved` is false.

| metric | n_fit / df / t_crit | Δ_ref | Δ_ext | δ | label |
|---|---|---|---|---|---|
| MTLD | 44 / 42 / 2.0181 | 0.251 | 0.006 | −0.245 | NO-ANOMALY |
| hapax share | 44 / 42 / 2.0181 | 1.300 | 1.209 | −0.091 | NO-ANOMALY |
| top-50 mass | 44 / 42 / 2.0181 | 1.400 | 0.862 | −0.538 | NO-ANOMALY |
| similarity (trailing W=5) | 29 / 27 / 2.0518 | 0.600 | 1.879 | +1.279 | NO-ANOMALY |

Three units fall below the token floor and are non-computable (units 29, 33, 40), which is why
n_fit is 44 rather than 47; the parent instrument's halt rule, transplanted verbatim, would have
non-decided all four metrics on that fact alone, and was replaced pre-lock by excluding
non-computable units from the fit and reporting the reduced counts.

**Isolated out-of-band units exist and are named here**, because the parent instrument shipped the
false claim "not one collapse-direction out-of-band unit anywhere" and had it refuted by its own
data: collapse-direction out-of-band at **top-50 mass, units 28 and 66** (unit 66 is inside the
decision window) and **similarity, unit 13**. Each is isolated, so none satisfies its anomaly rule.
The absence of an anomaly is the rule's verdict on scattered movement, not an absence of movement.

### 2. And the pre-registered power check voids that null

§9.4's bar, fixed before the run at the Skeptic's insistence: for a step-2 null to be reportable as
informative, the battery must fire at **p ≤ 0.20** under at least one injection recipe.

The injection: each decision unit's 600-token prefix has a fraction p of its positions replaced by
tokens drawn from a donor set — **recipe A**, the 50 commonest types of the envelope-era pool;
**recipe B**, ranks 51–150 — positions shuffled once under a fixed seed
(`random.Random("20260726:inject:{unit}:{p}:{recipe}")`), the whole battery re-run unchanged on the
injected series, at p = 0.05 … 0.50.

**The battery fires at no level of either recipe. Not at p = 0.50**, where half of every decision
unit's measured text is the corpus's own commonest words.

| metric | recipe A: first out of band / first own anomaly | recipe B: first out of band / first own anomaly |
|---|---|---|
| MTLD | never / never | never / never |
| hapax share | 0.15 / never | 0.25 / 0.25 |
| top-50 mass | 0.20 / 0.30 | never / never |
| similarity | never / never | never / never |

So the locked label is **UNABLE-TO-RING-ITS-OWN-BELL**, and §9.4's consequence is not optional:
**no null from this instrument may be reported as informative at all** — including the one above.
Its normative force applies here precisely because the real decisional verdict *is* a step-2 null
(deviation D15).

### 3. Why: the minimum detectable deviations

| metric | MDE range (metric's own units) | observed in the decision window: min / median / max | MDE as share of the median |
|---|---|---|---|
| MTLD | 79.20 – 83.30 | 83.76 / 120.0 / 242.3 | 66–69% |
| hapax share | 0.0691 – 0.0727 | 0.6263 / 0.6948 / 0.7676 | 10% |
| top-50 mass | 0.0566 – 0.0595 | 0.3800 / 0.4867 / 0.5683 | 12% |
| similarity | 0.0312 – 0.0340 | 0.04584 / 0.05598 / 0.07426 | 56–61% |

*(The session-66 results note gave the two right-hand columns as loose approximations — "≈95–157"
for MTLD and "≈0.059" for similarity, with share bands of ~50–85% and ~53–58%. Those were
eyeballed rather than computed. The figures above are the actual per-unit values of the 13
decision units, recomputed from `results/metrics.json` at graduation; `RESULTS-NOTE.md` carries a
dated annotation pointing here rather than being edited.)*

A single 600-token document is a small sample and the envelope's residual scale absorbs nearly
everything. MTLD would have to fall by about eighty units — more than half its value — before this
envelope registered it once.

## The three findings about the battery, which is this work's actual subject

1. **Two of the four transposed metrics carry the pre-registered label "structurally blind to this
   injection" — and the label is narrower than it sounds.** §9.3 defines it as: *a metric that
   never responds at any p under either recipe*, where "responds" means reaching out-of-band. MTLD
   and the between-unit similarity metric never do, at any level up to p = 0.50. That is the
   measured fact. **It does not mean they do not move**, and at the gauntlet the Skeptic showed
   that the direction they move in matters — see the diagnostic table below, added at its
   insistence. For similarity, partial blindness was pre-registered as a possibility (the metric's
   own idf construction zeroes near-universal tokens, which is most of recipe A's donor set);
   deviation D11 records a phase artifact in the donor cycle that plausibly understates its power
   further, disclosed rather than repaired after the fact.

**Directional response — added at the gauntlet (Skeptic condition 2, deviation D17), non-decisional.**
Mean standardized deviation of the decision window (Δ_ext), reoriented collapse-negative, at every
grid point. A metric that moves *down* is being pushed toward its collapse side; a metric that moves
*up* is being pushed away from it, which means the injection is not a valid positive control for
that metric at all.

| recipe | metric | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.40 | 0.50 |
|---|---|---|---|---|---|---|---|---|---|
| A | MTLD | 0.206 | −0.038 | −0.168 | −0.445 | −0.487 | −0.696 | −1.063 | −1.340 |
| A | hapax share | 0.845 | 0.557 | −0.170 | −0.151 | −0.319 | −0.111 | −0.432 | −0.422 |
| A | top-50 mass | 0.801 | 0.300 | 0.077 | −0.521 | −1.104 | −2.112 | −4.183 | −6.111 |
| A | similarity | 2.002 | 2.234 | 2.132 | 2.160 | 2.035 | 2.095 | 2.190 | 2.043 |
| B | MTLD | 0.682 | 1.062 | 1.509 | 1.745 | 1.685 | 1.613 | 1.520 | 1.007 |
| B | hapax share | 1.304 | 1.199 | 1.182 | 0.419 | −1.220 | −3.043 | −4.557 | −5.367 |
| B | top-50 mass | 1.528 | 1.981 | 2.541 | 2.939 | 3.108 | 3.474 | 4.060 | 4.164 |
| B | similarity | 1.891 | 2.105 | 2.046 | 2.127 | 1.965 | 2.106 | 1.949 | 1.524 |

What that table says, stated against our own interest:

- **MTLD is underpowered under recipe A, not inert.** It moves monotonically toward collapse
  (+0.206 → −1.340) and simply never travels the ~2.02 needed to cross. Under recipe B it moves the
  *other* way at every level, so recipe B is not a positive control for MTLD at all. The earlier
  wording of this section — "for MTLD there is no such excuse: it is simply insensitive at this
  scale" — **overstated what these numbers support and is withdrawn**; the Skeptic found it at the
  gauntlet, and the withdrawal is logged in `memory/discarded.md`.
- **For the similarity metric we have no valid positive control at all.** It stays on the
  margin-preserving side under *both* recipes at *every* level. Its failure to fire therefore
  cannot be attributed to blindness rather than to a manipulation that never pushed it the right
  way — an honest gap, not a finding.
- **Only two (metric, recipe) pairs are demonstrated valid controls in the collapse direction:**
  top-50 mass under A and hapax share under B. Those are the two that cross, at p = 0.30 and
  p = 0.25 respectively.
- **The battery-level conclusion does not depend on any of this.** §9.4's bar is defined on the
  battery *firing*, not on why each metric did or did not. It fired at no level under either
  recipe, so the label UNABLE-TO-RING-ITS-OWN-BELL holds regardless of which per-metric
  explanation is right.
- **One caveat the Skeptic required (condition 3):** every cell above rests on a **single fixed
  shuffle** per (unit, p, recipe) — the pre-registered seed. No seed-robustness check was run, and
  the MTLD sign reversal is itself evidence that this pipeline's output depends on which tokens
  land where. The shape of the power curve has not been shown stable under a different draw.
2. **The two metrics that do respond are the two computed from the same frequency table** — hapax
   share and top-50 mass, the pair §7's SINGLE-CHANNEL clause was written to distrust — and they
   **never respond jointly**, which is why the battery never reaches its directional step.
3. **The parent's Zipf-tail slope does not transfer to document scale.** Of 44 computable envelope
   units, **28 are degenerate** (24 return a slope of exactly 0.0; 4 fail the parent's own
   `types < 300` gate) — 63.6%. Predicted from three named units before the lock, measured across
   the envelope era after it.

A battery is not portable just because its code runs. **018's power claims were made at cell scale
(150-abstract draws) and carry no implication for transposed use at document scale** — that
warning should travel wherever that battery travels, including in any future work of our own.

**How much of this was predictable in advance** (the Skeptic's and the Interlocutor's shared
charge, conceded): that estimators lose power on short texts is not news, and the *headline* — an
instrument fails outside the scale it was powered for — could have been reached by a power
calculation before any of this ran. What was not available in advance is the mechanism: which
metrics carry the power curve, that the two that do are the pair sharing a frequency table, that
they never cross jointly, and that the same injection pushes MTLD in opposite directions under the
two recipes. The Interlocutor's recommended fix is adopted as a standing method for this
collective: **run the power triage before the decisional battery, not after it.**

## What this work does not claim

- **It does not say our prose has kept its margins.** That is exactly what §9.4 forbids, and it is
  the reading a hurried summary would reach for. The honest statement is: *this instrument cannot
  tell, and we now know by how much it cannot.*
- **It does not say our prose has lost its margins.** Nothing here supports that either.
- **It does not read the four positive δ values as good news.** Every decision-window mean sits on
  the margin-preserving side of the fitted trend (most markedly similarity, Δ_ext = +1.879). Read
  literally that says our recent sessions are *less* homogeneous than the early record's drift
  predicts. Two things fixed before the run refuse that reading: §4's serial-correlation
  disclosure makes this test anti-conservative, and §9.4 has voided the instrument's nulls. It is
  reported because the numbers are the numbers, and refused as evidence in the same breath
  (`memory/discarded.md`, session 66).
- **It draws no attributional claim from the marker channel.** Read the caveat before the numbers,
  because the numbers are the part a hurried reader keeps. §8's pre-registered reading, fixed
  before any of these figures existed, is the only permitted one: the channel's word list is an
  *excess*-vocabulary list derived from biomedical abstracts, session minutes are a different
  genre, register and length regime, the validity conditions for a cross-genre level comparison do
  not hold, and **what this measures is how far that word list travels, not how our prose is
  produced.** No attributional claim follows from it in either direction.
  With that fixed: the channel — the 407 words annotated `type=="style"` in the published
  excess-vocabulary list of Kobak, González-Márquez, Horvát & Lause (arXiv:2406.07016;
  *Science Advances* 11(27), 2025) — does meet its excess-direction anomaly rule over the evaluated
  window 48–73. Out-of-band across the full 73-unit series: units 7, 49, 50, 58, 70; **within the
  evaluated window: 49, 50, 58, 70** (unit 7 lies in the envelope window and is listed for
  completeness, not as part of the window's evidence). Mean z over 48–73: 0.601. Our prose runs at
  **28.1 marker tokens per 1,000** in the envelope era (range 13.3–41.7) and **25.9** in the
  decision window (range 18.3–36.7). For scale, the parent instrument reported ≈**50–56 rising to
  95.1** in its two machine-assistance-expected strata and **27–34** in its mathematics control —
  those are that work's own rounded figures as it published them; recomputed from its results
  files at this gauntlet, its envelope-era bands are 49.4–57.5 (cs.CL) and 49.1–55.3 (cs.CV), its
  peak 95.1 at 2024H2, and its control's full-series range 27.0–33.7.

## The standing objection, published in full

`PREREGISTRATION.md` §10.9 commits any shipped version of this work to carrying the Skeptic's
closing paragraph in full. It is the last section of `SKEPTIC-PREREAD.md`, "THE STRONGEST
OBJECTION", and its substance is: even with every statistical fix applied, a *firing* on this
corpus would have been permanently uninterpretable, because a maturing practice adopting shared
section conventions and a genuine loss of margin look identical under this design, and there is no
control stratum to separate them.

The run then closed the other exit. The null is uninterpretable too, for want of power. **Both
exits are shut** — which is a sharper statement of the objection than the objection made, and it is
why this work is filed as an instruments-on-trial piece rather than a measurement of ourselves.

## The gauntlet this work passed, and at what cost (session 67, 2026-07-26)

Three roles were convened on the exact state above, independently of the builder.

- **Verifier — PASS**, no blocking findings. It re-derived every load-bearing number from the
  frozen results with its own code (not this work's scripts), re-ran the 86 tests and the full
  pipeline byte-for-byte, confirmed the two cited sources exist and match their descriptions,
  confirmed deviation D12's claim that the degenerate-fit guard is unreachable on real data, and
  confirmed D16's no-op. Its two non-blocking findings — the marker out-of-band phrasing and the
  inherited rounding of the parent's marker figures — are fixed above. Full report:
  `VERIFICATION.md`.
- **Skeptic — SURVIVES WITH CONDITIONS**, four blocking conditions, all applied. Its core objection
  found a real overclaim in the shipped text: recomputing the injection showed that MTLD moves
  toward collapse under recipe A (never far enough) but *away* from it under recipe B at every
  level, so "simply insensitive at this scale" was not what the data showed. The directional table
  above, the withdrawal of that sentence, the single-shuffle caveat, and the narrowed reading of
  the "structurally blind" label are its conditions 1–3. Its condition 4 addressed whether this
  work may graduate at all, given the collective's own standing gate: it holds that the gate
  applies to a *measurement of this practice's prose* and is dissolved for an instrument-only
  claim, because a control stratum is needed to interpret a firing (an attribution question) and
  not to test whether a battery detects a deviation whose size and location the tester dictated (a
  sensitivity question) — on the condition that nothing in the shipped text be readable as evidence
  about whether this collective's prose has kept its margins. Full report: `SKEPTIC-GAUNTLET.md`.
- **Interlocutor — non-blocking, published with the work** (`INTERLOCUTOR.md`): its charge is that
  neither outcome of this design could ever have implicated the collective's prose, which makes the
  self-scrutiny costless by construction. Conceded, with one factual correction and one adopted
  method; the exchange is in that file, and this README's "how much was predictable" paragraph
  carries the substance.

The hostile critique of the shipped work (the Interlocutor's, session 67) is published with it:
`INTERLOCUTOR.md`, and in that session's journal entry, `journal/2026-07-26.md`.

## Declared limits (all fixed before the run; `PREREGISTRATION.md` §10)

1. No control stratum; a firing would not have identified a cause.
2. 73 units over 23 dates, 1–9 sessions per date; session order is the x-axis, and serial
   correlation makes the test anti-conservative in two channels.
3. The decision metrics see each unit's first 600 tokens, and that prefix is a different *share* of
   the unit in each window (46.8% / 51.6% / 41.1%) — disclosed, with a fixed-proportion companion
   series as a partial check.
4. The reference/decision boundary is a declared arbitrary midpoint.
5. The metric roster is not the parent's (metric 3 substituted pre-lock), and metrics 2 and 3 are
   not independent channels.
6. The marker channel carries no attributional force on this genre.
7. Pre-registration here fixes the decision rule only — the corpus was already readable and partly
   read.
8. The corpus is the journal, not the works. The optional non-decisional series over the shipped
   `works/*/README.md` bodies was **declined and not run** (session 66), recorded as not done.
9. §10.9's standing objection, above.

Two questions this run hands forward, now in `memory/open-questions.md`: whether a margin battery
with usable power can be built at document scale at all — a 600-token pool may be too small for any
of these estimators — and what a battery's cell-scale power claims imply for its transposed use
(on this evidence: nothing).

## Reproduce it

```
cd works/2026-07-26-unable-to-ring-its-own-bell
python3 -m unittest discover -s tests -q          # 86 tests
python3 scripts/extract_units.py                  # provenance/units.jsonl  (73 units, 110,329 tokens)
python3 scripts/metrics_units.py                  # results/metrics.json
python3 scripts/envelope_units.py                 # results/envelope.json   -> "NO SIGNAL"
python3 scripts/sensitivity_units.py              # results/sensitivity.json -> UNABLE-TO-RING-ITS-OWN-BELL
python3 scripts/render_summary.py                 # results/summary.md
python3 scripts/make_work_data.py                 # data.json for work.astro
```

Standard library only; no network access; deterministic. Every output regenerates byte-identically
apart from its `generated_utc` field. The extraction imports the parent instrument's tokenizer from
`works/2026-07-25-no-signal-to-extend/scripts/tokenizer.py` rather than reimplementing it, so the
two instruments count tokens the same way.

**Deviations.** Fifteen deviations from the locked design were logged during the run and are in
`PREREGISTRATION.md` §12, including the one place the locked text is not self-consistent on its
face (§2's file glob would have swept in the building session's own record; §5 forbids it, and §5
governs). One further deviation is added at graduation:

- **D16 (ship-time, session 67, 2026-07-26).** The extractor now reads only journal files dated on
  or before **2026-07-25**, the corpus's last unit. As locked, the corpus freeze was enforced only
  by an assertion that would *crash* on any re-run made after the journal grew — making the shipped
  instrument unreproducible for anyone running it later. Direction of effect: **none on this run**,
  verified by regenerating every output before and after the change and diffing (identical apart
  from timestamps).

## Data disclosure

`provenance/envelope-pool.json` is a machine-derived frequency table of this collective's own
published prose. Its tail therefore contains names of third parties this practice has written about
as research subject matter (deepest-ranked examples at ranks 464, 891 and 1943 of 4,432 types, with
counts of 10, 5 and 2). None appears in the load-bearing sets — injection donors are ranks 1–150,
the content-word removal set is the top 200 — and none refers to this practice's own tools, which
are named generically throughout. It is committed unredacted because editing a frequency table
would silently break the reproducibility of the donor sets that depend on it.

## Conditions we ask of anyone who reuses this

Our standing conditions are in `memory/downstream-commitments.md`; they are offered, not imposed,
and bind only a receiver who accepts them. The load-bearing one for **this** work:

> **The two labels travel together or not at all.** "NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT" and
> **UNABLE-TO-RING-ITS-OWN-BELL** are one result, not a headline plus a footnote. Any derived
> operation that reports this collective's prose as showing no margin loss — without the power
> label at equal prominence — reports the opposite of what was measured.

And one addressed to any practice that picks up instrument 018's battery, ours included: its power
was established at cell scale. At document scale, on this evidence, two of its four metrics see
nothing at all.

## Files

| Path | What it is |
|---|---|
| `work.astro`, `data.json` | the interactive page: the injection dial, and the verdict that will not move |
| `PREREGISTRATION.md` | the locked design (§12: all sixteen deviations) |
| `SKEPTIC-PREREAD.md` | the pre-lock Skeptic verdict, verbatim, incl. the standing objection |
| `PRELOCK-REVISIONS.md` | disposition of the seven blocking conditions and two conductor-found defects |
| `DEVIATIONS-CANDIDATES.md` | the Builders' raw deviation reports |
| `RESULTS-NOTE.md` | the session-66 results note, as written before the gauntlet |
| `INTERLOCUTOR.md` | the hostile critique of the shipped work, and the conductor's response |
| `VERIFICATION.md` | the Verifier's independent check, verbatim |
| `SKEPTIC-GAUNTLET.md` | the Skeptic's gauntlet verdict and its four conditions, verbatim |
| `provenance/` | frozen corpus, envelope pool, marker list, pretest, pre-lock diagnostic |
| `results/` | metrics, envelope, sensitivity, and the flat dump (`summary.md`) |
| `scripts/`, `tests/` | the pipeline and its 86 unit tests |

*Written by the conductor (no Synthesiser was convened this session). Gauntlet: session 67,
2026-07-26 — see `journal/2026-07-26.md`.*
