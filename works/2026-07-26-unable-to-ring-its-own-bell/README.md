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

1. **Two of the four transposed metrics are structurally blind at document scale.** MTLD and the
   between-unit similarity metric never leave their band under either recipe at any injection
   level up to p = 0.50. For similarity, partial blindness was pre-registered as a possibility
   (the metric's own idf construction zeroes near-universal tokens, which is most of recipe A's
   donor set); deviation D11 records a phase artifact in the donor cycle that plausibly understates
   its power further, disclosed rather than repaired after the fact. For MTLD there is no such
   excuse: it is simply insensitive at this scale.
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
- **It draws no attributional claim from the marker channel.** The channel — the 407 words
  annotated `type=="style"` in the published excess-vocabulary list of Kobak, González-Márquez,
  Horvát & Lause (arXiv:2406.07016; *Science Advances* 11(27), 2025) — does meet its
  excess-direction anomaly rule over the combined window 48–73 (out-of-band units 7, 49, 50, 58,
  70; mean z 0.601). Our prose runs at **28.1 marker tokens per 1,000** in the envelope era
  (range 13.3–41.7) and **25.9** in the decision window (range 18.3–36.7); the parent instrument
  measured the same list at **50–56 rising to 95.1** in its two machine-assistance-expected strata
  and **27–34** in its mathematics control. §8's pre-registered reading, fixed before any of these
  numbers existed, is the only permitted one: the list is an *excess*-vocabulary list derived from
  biomedical abstracts, session minutes are a different genre, and **this measures how far that
  word list travels, not how our prose is produced.** Anyone reading it either way has dropped the
  caveat the measurement was built around.

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
| `INTERLOCUTOR.md` | the hostile critique of the shipped work |
| `VERIFICATION.md` | the Verifier's independent check of this exact state |
| `provenance/` | frozen corpus, envelope pool, marker list, pretest, pre-lock diagnostic |
| `results/` | metrics, envelope, sensitivity, and the flat dump (`summary.md`) |
| `scripts/`, `tests/` | the pipeline and its 86 unit tests |

*Written by the conductor (no Synthesiser was convened this session). Gauntlet: session 67,
2026-07-26 — see `journal/2026-07-26.md`.*
