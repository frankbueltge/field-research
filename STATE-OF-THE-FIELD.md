# State of the field — carried

*Protocol v4 §5. Read in full at every session open, before the bulletins and before the work.
**At most 2,500 words.** Maintained in the session that changes it. Depth lives in `memory/`
(claims, open questions, discards, dossiers — some 150,000 words), in the artifacts, and in the
house's paper register; consulted through recall, never carried.*

**Compressed 2026-09-03, 2026-09-06 and again 2026-09-07 (session 154)** to stay under the cap:
entries are shortened, never withdrawn; every figure remains in its artifact, and struck sentences
stay visible with their replacement.

---

## 1. Standing position

### Cycle 002 (opened 2026-09-03) — the constructive question

**PRESENTED 2026-09-07 (session 154), `presentations/cycle-002/`** — page, summary, data, and a
`check.py` that rebuilds every figure offline and fails on a hand-edited one. **The cycle's answer,
four parts, all from the loop failing:** (1) the mechanical middle automates cleanly and is
calibrated; (2) automation moves the failure **upstream into the question space** — findings linear
in question count, invisible from inside; (3) the step that resists is **recognising that what you
hold is what the world already has** (by name works, by description does not, and an invention has
no name); (4) **an unattended loop needs an instrument for its own liveness** or it reports success
while measuring nothing. Two travel; two are ours alone.

**Question 41 closed, our own prediction refuted (K2 fired).** Not the frozen corpus we
pre-registered: a fresh fetch shares **0 of 66** outcomes with the night before. Two real causes —
`corpus_sha256` hashes a *file* carrying a timestamp (two fetches 97 s apart: different file
digests, **identical records, Jaccard 1.000**), and **arXiv posts Sunday–Thursday, announcing
nothing Friday or Saturday** (`info.arxiv.org/help/availability`, at source), announcements at
00:00 UTC. P1, P3, P5 held; P4 void. Details in §4.1.

**Adversary against session 153's artifact, which had none: two fatal**, four serious, three minor,
nine failed attacks. *"All five firings share a top record"* is **four of five** — our own table had
shown the fifth all along; and the predictions table rendered P1 **refuted** where the prose said
**void** (now two held, two refuted, two void). Both hand-typed on a page claiming none were.
**Recorded, not patched:** K1's leak check has no power for four of ten targets; a 9/10 denominator
switch; the firing no-target probe fires on an unfiltered numeral; the earlier failing reachability
probe is asserted but **not committed**. **Thirty adversary-found defects across this cycle's four
artifacts (3, 5, 13, 9). The presentation itself was not attacked.**

*Compressed 2026-09-07: sessions 151–153 shortened to load-bearing figures, the presentation now
carrying the cycle. Nothing withdrawn; full detail in each artifact.*

**Session 153, `artifacts/cycle-002/2026-09-06-does-it-know-it-is-known/`.** Built
`tools/autoloop/priorart.py`, **stage PRIOR-ART**, mechanical, **no model inside it**: description →
three fixed queries → Crossref + PubMed → six lists fused by reciprocal rank fusion. Benchmarked on
ten methods the loop uses, nine sources confirmed at record. **Blind, from prose never naming the
method: 0 of 9 at any rank. From the bare name alone: 3 of 9, two at rank one, Tarone 1990 among
them.** The prose is worse than the name inside it. **Verdict uninformative both ways:** 1 of 4
no-target probes, 5 of 9 real targets while pointing at the wrong record every time; on live claims
5 of 10, **four of those five** topped by the same figure caption *(corrected 2026-09-07 — was
published as all five)*. **Not reproducible:** 51 of 58 re-issued queries identical, every
disagreement Crossref's, PubMed 30 of 30 — so the stage is behind `--priorart`, **not** on nightly.
**Our own defect:** Arm B appended the name *after* a 350-character truncation, so 5 of 10 query
sets were byte-identical to blind — **P1 void**; P5 void; **P3, P4 refuted; P2, P6 held** *(tally
corrected 2026-09-07: two held, two refuted, two void)*.

**Session 152, `artifacts/cycle-002/2026-09-05-which-questions-count/`.** Built
`tools/autoloop/liveness.py`, a **PRE-CHECK stage merged into the nightly loop**: a question is
**asleep** when no labelling consistent with the corpus margins can push its p below α, so its
verdict is reachable before the first test. **Sound:** 0 rejections in 99,400 calls across
thirty-five empty worlds — but only **22,400** informative, and **zero** on the three *registered*
datasets, so every informative test of the instrument is post-hoc. **The reversal:** with
impossible questions out of the divisor the two corpora are **indistinguishable** (4.72 % / 4.73 %,
±0.20 points) where published disjoint — **session 151's P5 was refuted by a denominator, not by
the world**, and **vacuously** (here *asleep* and *no p-value* are the same list). Where they
differ (120 Crossref records) the awake denominator recovers **two survivors**. **Post-hoc:** at 40
random Crossref records 38 of 66 live, 2.82 % against 4.89 %. **The neighbour, found after the
build: Tarone, *A modified Bonferroni method for discrete data*, Biometrics 46(2):515–522, 1990**
(PMID 2364136, read at PubMed) — *untestable hypotheses* in significant pattern mining (arXiv
1407.0316, 1407.1176, abstracts at source). One query, run afterwards; the house register matched
**zero** of nine terms. Adversary: **thirteen defects**, one fatal; sixteen failed attacks
published.

**Session 151, `artifacts/cycle-002/2026-09-04-the-dial/`.** k ∈ {4…66}, redundancy varied at fixed
k, 400 paired empty worlds per cell, on **two** corpora: arXiv (2,039) and **Crossref** (2,400; the
reach-outside source; OpenAlex answered **429** to everything). **The dial is a line** —
through-origin slope **0.04691** (R² 0.99978) arXiv, **0.04264** (R² 0.99298) Crossref, over a
sixteen-fold range of k in two unrelated literatures *(the lean arm; mean-centred, Crossref is
0.981, under the registered bar)*. **Its own central claim died by its own falsifier:** P2, P3, P4
all failed — **redundancy is statistically inert**; what it inflates is **the count**: 66 questions
that are 51, 17 findings that are 14, 13 survivors that are 11. **Adversary: five defects, four
binding** — the post-hoc "claimable" trim does not rescue P5; the centred R²; BH's duplicate
self-correction fails under the largest-p representative; and **`fetch_crossref.py` sorts by
*deposit* date — 1,485 of 1,921 dated records in the last eight days of a fourteen-week window,
unrepaired and disclosed.**

**Question:** *How can end-to-end automation of AI research be realised? Build it, and measure
where it breaks.* The direction of 2026-09-03 (`REQUESTS.md`) **rests the counter-measurement remit
for this cycle** and asks for construction. Failure conditions it named: nothing built that runs
unattended by session three; a finding true of one loop offered as a finding about loops; an
artifact shipped without pre-registration, falsifier or kill condition. **All three met.**

**Session 150, `artifacts/cycle-002/2026-09-03-a-loop-that-finds-things/`.** Built
`tools/autoloop/`: six stages (enumerate → fetch → test → analyse → write → review), unattended,
~90 s, on a nightly schedule writing one row to `series/series.jsonl`. On 2,034 arXiv records, 66
pre-registered questions, **14 findings** (10 survive BH; 7 of 14 survive a split, 13 of 14 keep
their sign). Permuted null world, 500 replicates: **3.22 findings per run**, per-test rejection
**4.88 % (CI 4.66–5.12)** — calibrated, refuting our own prediction that it would not be. **The
loop manufactures findings because it asks 66 questions and for no other reason: throughput and
error control are the same dial.** What no stage could see and a person saw in one sitting: the 66
questions rest on **51 distinct variable pairs**; 3 of 10 survivors are publication plumbing; its
largest real survivor is significant alone in 1 of 7 category strata — **the loop cannot see that
it has a sampling frame.** Adversary: three defects, worst a multiplicity denominator differing
from the registered one; all published.

### Cycle 001 (2026-08-30 – 2026-09-03), compressed

*Compressed again 2026-09-07; every figure stands in its artifact.*

- **The yield of our own loop falls as output rises** (`yield-of-a-loop/`): 0.29 works per session
  in the first half of 139 sessions, 0.04 in the second; 48 sessions, 25 days, 769 commits, 1,213
  draft files, nothing shipped. *The interesting failure is not a bad output — it is a loop that
  keeps producing and stops delivering.* Rests on one system: itself.
- **The last step, measured outside** (`links-in-the-abstract/`): 613 automation-advertising
  abstracts vs 613 matched `cs.AI` — 18.3 % vs 12.9 % hand over an address (p = 0.009), but
  **81.7 % hand over none**; genre is the likeliest innocent explanation.
- **The response side** (`how-long-a-warning-stands/`): **47.1 %** of public journal concerns become
  a retraction within five years (n = 1,277), median **291 days**, vs 263 nine years earlier. Two
  feeds disagree **7.3 %** of the time.
- **The receiver side** (`a-door-to-knock-on/`, `the-sign-and-the-door/`): **27 of 40** publish a
  route for a concern; **14 of 40** refuse a bare automated knock — not the 45 % first published;
  the 13 refusing everything **cannot be attributed from one network address**.
- **The review step** (`the-injection-that-remains/`, `who-may-hide-a-prompt/`): five arXiv papers
  ever carried a hidden reviewer-steering prompt, **0 currently serve one** — a floor, not a census.
  Of nine venue-year policies, 5 forbid authors with a named consequence, 3 are silent.
  ~~Drawn on who acts.~~ **Corrected 2026-09-03 by the Studio: drawn on *purpose* first, on *actor*
  in the consequence.**
- **Our own review step** (`who-finds-the-error/`): of 18 corrections to shipped work, **14 found by
  us, 4 from outside** — refuting our own digest. A published error stood a median 7 days, and our
  adversary was aimed almost entirely at *unpublished* work (2 of 18 shipped). **Cycle 002 moved
  that: all four of its adversaries attacked published artifacts.**
- **Cycle 001's answer** (`presentations/cycle-001/`): all four measurements fail at the same step —
  *the handover, where work must leave the system that made it* — a boundary of **consent, not
  competence**, which does not move when the instrument improves.

## 2. The literature, as it stands

**Not ours to re-derive:** AI-Scientist-class systems that ideate, code, run experiments and write
papers end to end; autonomous laboratories; a large benchmark literature on agent task success.
Every wet-lab validation among the *Nature*-published systems was executed by humans (field map
§1.1, site repo). **The standing gap we occupy:** benchmarks measure *task success* on curated
problems; almost nothing measures the *yield, calibration and delivery* of a research loop running
unattended over time. Cycle 002 sits exactly there, from inside a loop we built.

**Response side (remit rested this cycle):** time-to-retraction is well measured; post-flag action
rates are very low — the "under 2 %" figure is **known here only through delegated search and is
not ours to carry.** Thin: *public flag* → editorial decision, and institutions vs publishers.

**The rule that binds hardest (§5.2):** when a finding rests on someone else's result, read the
source and cite the passage. A figure reconstructed from memory is fatal here as nowhere else.

## 3. Neighbours — so "has this been done already" is answered from memory

- **House registers, one fetch each:** `/papers/index.json`, `/papers/register.json`,
  `/datasets/register.json`, `/atlas/werke.json` (shapes in `SITE-API.md`). Feeds, never mirrored.
- **For cycle 002:** the AI-Scientist line *is* the object, not a competitor. **2026-09-04,
  abstract at source:** *The Agentic Garden of Forking Paths*, Miao, Pritchard & Zou, arXiv
  **2607.01507v1** — agents varying the *analysis path* under a fixed question reproduce 72 % of
  the human ideological gap on a 42-team study. **Daylight: they vary the analysis under one
  question; we vary the questions under one analysis.** Still unfound: a published **null-world
  calibration of a question-generating pipeline**.
- **2026-09-06, nearest to the prior-art stage:** *NoveltyRank*, Yan, Li & Feng, **arXiv
  2512.14738** (abstract at source) — learned representations plus retrieval, scoring conceptual
  novelty. **Daylight: it scores novelty and takes retrieval as given; we measure the retrieval
  alone, model-free, from a name-free description of a known target.** Still unfound: a published
  recall measurement of that kind inside a research pipeline.
- **2026-09-05, ours-already-done:** excluding hypotheses that cannot reach α is **Tarone 1990**
  — *untestable hypotheses* in significant pattern mining (arXiv **1407.0316**, **1407.1176**,
  abstracts at source; Terada et al., PNAS 2013 returned 403 and is **not** relied on). **Do not
  rebuild this.** Daylight: Tarone targets the multiplicity factor and Fisher's exact test; ours
  was the *null-world self-calibration figure*.
- **Response side (`SURVEY.md`):** no standing instrument exists — 14 candidates, none qualifying.
  Closest built: **COMPare** (2015–16). Only dedicated measurement of the concern-to-retraction
  interval: **Vaught et al. 2017**.
- **Siblings:** the Studio builds from our corpora and has corrected us (*The Fourth Cell*,
  2026-09-03) and corroborated us (2026-09-06, §4.4). Material handed sideways is a live channel.

## 4. Live series and open questions

1. **The autoloop series** (four rows, **two measurements** — question 41 closed 2026-09-07).
   2026-09-03, seeded by hand: 14 raw, 10 BH, 4.88 %. 2026-09-04/05/06, scheduled and green: 17
   raw, 13 BH, 4.93 %, **byte-identical across all three on three different recorded corpus
   digests** — those nights were **Fri/Sat/Sun** and the source posts Sunday–Thursday. **Count
   distinct test vectors, never nights**; expect **two duplicate rows a week**. From 2026-09-07
   rows carry `records_digest`, `test_vector_digest`, `vector_repeats_previous`; `corpus_sha256`
   keeps its meaning **and its defect**, nothing back-filled (`series/README.md`). A fetch on
   2026-09-07: 2,072 records, **0 of 66 outcomes shared with 2026-09-06**, 16 BH.
2. **What generalises from one loop?** *Architectural, on two unrelated corpora:* null yield linear
   in k; redundancy statistically inert but inflating the reported count. *Held here, not general:*
   BH cancellation for exact duplicates. *General because arithmetic:* the awake fraction falls with
   corpus size, so a fixed question space over a small corpus reports a calibration that reads low
   (38 of 66 live at 40 random Crossref records; 2.82 % vs 4.89 %) — **subsample at random**; over
   the *first* n it read 21 of 66, the Crossref corpus being written one publisher at a time.
   *Still about us alone:* both spaces were built by the same hand to the same template.
3. **The retrievability series** (17 days, 2 holes): of 28 apparent losses, 11 did not survive a
   re-request — single-pass measurement of disappearance is wrong four times in ten.
4. **Which step is genuinely un-automatable?** *Deciding a question is worth asking* was the
   standing candidate; **2026-09-05** closed 34, 35 and 37 by automating it. The **literature step**
   replaced it (38), and **2026-09-06 sharpens it without closing it**: the stage runs unattended,
   retrieval by *description* fails (0 of 9) where retrieval by *name* works (3 of 9), and an
   invention has no name. The candidate is **recognising that what you hold is what the world
   already has** — one route ruled out mechanically, the step not shown impossible. **Open (42):
   does a semantic index recover the nine?** Not run; both catalogues offering one answered 429.
   **Corroborated from outside this practice:** the Studio's Atlas checker returns nothing for
   **56.4 %** of queries and does *worst where descriptions are richest*. Two instruments, two
   corpora, same wall.
5. **New, 2026-09-07 (43): can an unattended loop detect its own dead nights in general?** Ours can
   now, by comparing test vectors — but that is detection after the fact. Nothing here schedules
   *against* a source's publication calendar, and no measurement exists of how many automated
   pipelines run nightly over a weekday-only source.
6. **Counter-measurement questions, held open while the remit rests** (they return with it): is
   the unresolved share still rising, and is concern-to-retraction a good proxy for the
   flag-to-response interval? A published address is a **door, not a reply** — settling it needs
   letters and waiting, and **nobody has been written to**. Do the 13 doors refusing everything
   still refuse **from another network**? Is the hidden-prompt population still zero a month on,
   and how large under a search reaching invisible PDF text? Do the 3 silent venues close the hole?
7. **Corrections outstanding against our own shipped work:** notice-level share 46.8 % → 48.9 %
   (headline unaffected); 94.0 % mistyped for 94.8 % four times; the `machine_blocked` column
   behind "45 %" is **not derivable from the data shipped with it**; the ICML compression struck
   in §1. Filed as dated events beside their artifacts, not patched.
