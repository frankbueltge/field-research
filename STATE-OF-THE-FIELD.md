# State of the field — carried

*Protocol v4 §5. Read in full at every session open, before the bulletins and before the work.
**At most 2,500 words.** Maintained by this practice in the session that changes it. Depth lives
in `memory/` (claims, open questions, discards, dossiers — some 150,000 words), in the artifacts
themselves, and in the house's paper register; all consulted through recall, never carried.*

**Compressed 2026-09-03 (session 150)** to stay under the cap when cycle 002 opened: the cycle-001
entries below are shortened, not withdrawn, and every figure remains in the artifact it came from.
Struck sentences are left visible with their replacement.

---

## 1. Standing position

### Cycle 002 (opened 2026-09-03) — the constructive question

**Session 152, artifact `artifacts/cycle-002/2026-09-05-which-questions-count/`.** Built
`tools/autoloop/liveness.py`, a **PRE-CHECK stage merged into the nightly loop**: a question is
**asleep** when no labelling consistent with the corpus margins (N, group size, the outcome's value
multiset — exactly what permutation preserves) can push its p below α, so the verdict is reachable
before the first test. **Sound:** asleep questions took **0 rejections in 99,400 calls** across
thirty-five empty worlds — but only **22,400** were calls the statistic can answer at all, and on
the three *registered* datasets that informative count is **zero**, so every informative test of the
instrument is post-hoc. K3 re-ran the modified loop on session 150's corpus: all 66 claims
identical. **The reversal:** with the impossible questions out of the divisor the two corpora become
**indistinguishable** (4.72 % / 4.73 %, Monte-Carlo error ±0.20 points) where they were published
disjoint — **session 151's P5 was refuted by a denominator, not by the world.** **P4 and P5
refuted, and that is the better half:** every asleep question was *already* killed by the loop's own
review stage, one step too late; and BH had not counted them **on these three corpora, where
*asleep* and *no p-value* are the same list — so P5 was refuted vacuously.** Where the lists differ
(120 Crossref records) the awake denominator recovers **two survivors**: **one denominator diluted
here, a second diluted on smaller corpora.** **Post-hoc, the awake curve:** on a random subsample
of 40 Crossref records 38 of 66 questions are live and the calibration reads 2.82 % against 4.89 %
— the smaller the corpus, the more of a fixed question space is not a test.
**And the neighbour, found after the build:** the rule is **Tarone, *A modified Bonferroni method
for discrete data*, Biometrics 46(2):515–522, 1990** (PMID 2364136, record read at PubMed),
standard in significant pattern mining as *untestable hypotheses* (arXiv 1407.0316, 1407.1176,
abstracts at source). One query found it, run afterwards; the house's own 752-entry register matches **zero** of nine
search terms for it. **An automated research loop has no stage asking whether the answer is already
known — and neither did this practice.** A convened adversary then took **thirteen defects** off the
page, one fatal (the lead contradicted the page's own table); all repaired, sixteen failed attacks
published.

**Session 151, artifact `artifacts/cycle-002/2026-09-04-the-dial/`.** Turned session 150's dial:
k ∈ {4…66}, two families holding k fixed while varying redundancy, 400 paired empty worlds per
cell, on **two** corpora — arXiv (2,039) and **Crossref** (2,400; the §5.3 reach-outside source,
not in the house register; OpenAlex was tried first and answered **429** to everything after one
request). Both spaces: 66 questions on 51 distinct pairs, by construction.
**The dial is a line** — through-origin slope **0.04691** (R² 0.99978) arXiv, **0.04264**
(R² 0.99298) Crossref, over a sixteen-fold range of k in two unrelated literatures. **Its own
central claim died by its own falsifier:** P2 (variance ratio 1.069, 0.975), P3 (McNemar p = 0.60,
0.29) and P4 all failed, so **redundancy is statistically inert**. What it inflates is **the count,
not the statistics**: 66 questions that are 51, 17 findings that are 14, 13 survivors that are 11
(Crossref 28 → 21 twice). **P5 refuted:** null rates **4.72 %** [4.47–4.98] and **4.08 %**
[3.85–4.33], disjoint — **overturned 2026-09-05, see above.** **Mechanism:** nine Crossref
questions never could fire; `has_fulltext_link` is true for 2,400 of 2,400.
**An adversary found five defects, four of which still bind:** (1) the post-hoc "claimable
questions" restriction **does not rescue P5** — a rationale-free trim of the same size moves the
rate as much (**this is the objection session 152 answered, by deriving the trim from margins
instead**); (2) the through-origin R² is the lenient convention — **centred, Crossref is 0.981**,
under the registered bar; (3) BH's self-correction for exact duplicates held under the canonical
and smallest-p representative but **not** the largest-p one, so it is not a theorem; (4) the
Crossref fetcher sorts by *deposit* date — **1,485 of 1,921 dated records in the last eight days**
of a fourteen-week window, Elsevier's 300 undated: a known, dated, unrepaired defect in
`fetch_crossref.py`.

**Question:** *How can end-to-end automation of AI research be realised? Build it, and measure
where it breaks.* The direction of 2026-09-03 (`REQUESTS.md`) **rests the counter-measurement
remit for this cycle** and asks for construction, not observation. Its stated failure conditions:
nothing built that runs unattended by session three; a finding true of one loop offered as a
finding about loops; an artifact shipped without pre-registration, falsifier or kill condition.

**Session 150, artifact `artifacts/cycle-002/2026-09-03-a-loop-that-finds-things/`.** Built
`tools/autoloop/`: six stages (enumerate questions → fetch → test → analyse → write → review),
unattended, ~90 s end to end, now on a nightly schedule writing one row to
`tools/autoloop/series/series.jsonl`. On 2,034 arXiv records it asked 66 pre-registered questions
and reported **14 findings** (10 survive Benjamini–Hochberg; 7 of 14 survive a split of the same
corpus, 13 of 14 keep their sign). In a permuted null world, 500 replicates, it reports **3.22
findings per run** with a per-test rejection rate of **4.88 % (CI 4.66–5.12)** — calibrated, which
refutes our own prediction that it would not be. **The loop manufactures findings because it asks
66 questions and for no other reason: throughput and error control are the same dial.**
What no stage could see, and a person saw in one sitting: the 66 questions rest on **51 distinct
variable pairs** (two "findings" were one 2×2 table asked twice, identical p to every digit);
3 of 10 survivors are publication plumbing; and its largest real survivor is significant alone in
1 of 7 category strata — the loop cannot see that it has a sampling frame. A convened adversary
found three defects, the worst being a multiplicity denominator that differed from the registered
one (12/9 registered against 10/7 as run — same claim set); all published.

### Cycle 001 (2026-08-30 – 2026-09-03), compressed

- **The yield of our own loop falls as output rises** (`2026-08-30-yield-of-a-loop/`): 0.29 works
  per session in the first half of 139 sessions, 0.04 in the second; 48 sessions over 25 days
  produced 769 commits, 1,213 draft files, nothing shipped. *The interesting failure of an
  automated research loop is not a bad output — it is a loop that keeps producing and stops
  delivering.* Rests on one system: itself.
- **The last step, measured outside** (`2026-08-31-links-in-the-abstract/`): 613 abstracts
  advertising automated research against 613 matched `cs.AI`. The automation cohort hands over an
  address more often (18.3 % vs 12.9 %, p = 0.009) but **81.7 % hand over none**; whether links
  open shows no difference this design could see. Genre is the likeliest innocent explanation.
- **The response side** (`2026-09-01-how-long-a-warning-stands/`): **47.1 %** of public journal
  concerns become a retraction within five years (n = 1,277), median wait **291 days**, unchanged
  from 263 days nine years earlier. Two feeds disagree **7.3 %** of the time; design effect ≈ 8.
- **The receiver side** (`2026-09-01-a-door-to-knock-on/`, re-measured `the-sign-and-the-door/`):
  **27 of 40** publishers publish a route for raising a concern; **14 of 40 (35 %)** refuse a bare
  automated knock, not the 45 % first published; the 13 that refuse everything **cannot be
  attributed from one network address** to the institutions rather than to the address.
- **The review step** (`the-injection-that-remains/`, `who-may-hide-a-prompt/`): five arXiv papers
  ever carried a hidden reviewer-steering prompt, **0 currently serve one**, 4 of 5 removed it
  before the July 2025 press event. A floor, not a census. Nine venue-year policy documents: 5 of 9
  forbid authors with a named consequence, 3 of 9 are silent.
  ~~The rule is drawn on who is doing the act.~~ **Corrected 2026-09-03, found by the Studio: the
  line is drawn on *purpose* first — ICML permits authors the same act to detect LLM use by
  reviewers and forbids it for a favourable review — and on *actor* in the consequence.**
- **Our own review step** (`who-finds-the-error/`): of 18 corrections to shipped work, **14 found
  by us, 4 from outside** — refuting our own digest's claim that outsiders find our errors. A
  published error stood a median 7 days. Our sharpest instrument, a convened adversary, is aimed
  almost entirely at unpublished work (22 of 36 draft corrections, 2 of 18 shipped).
- **Cycle 001's answer** (`presentations/cycle-001/`): all four measurements fail at the same step
  — *the handover, where work must leave the system that made it* — and that boundary is one of
  **consent, not competence**, which does not move when the instrument improves.

## 2. The literature, as it stands

**Not ours to re-derive:** AI-Scientist-class systems that ideate, code, run experiments and write
papers end to end; autonomous laboratories in chemistry and materials; a large benchmark
literature on what agents achieve on fixed tasks. Every wet-lab validation among the *Nature*-
published systems was executed by humans (field map §1.1, site repo).
**The standing gap we occupy:** benchmarks measure *task success* on curated problems; almost
nothing measures the *yield, calibration and delivery* of a research loop running unattended over
time. Cycle 002 is placed exactly there, and now from the inside of a loop we built.

**Response side (surveyed 2026-09-01):** time-to-retraction is well measured; action rates after
flagging are very low — the "under 2 %" figure from a 2026 fabricated-reference audit is **known
here only through delegated search; the publisher returned 403 and the passage has not been read
at source. Do not carry it as ours.** Thin: the interval from a *public flag* to an editorial
decision on a general corpus, and anything about institutions as distinct from publishers.

**The rule that binds hardest (§5.2):** when a finding rests on someone else's result, read the
source and cite the passage. A figure reconstructed from memory is fatal here in a way it is not
elsewhere.

## 3. Neighbours — so "has this been done already" is answered from memory

- **House registers, one fetch each:** `/papers/index.json`, `/papers/register.json`,
  `/datasets/register.json`, `/atlas/werke.json`. Shapes in `SITE-API.md`. Feeds, never mirrored.
- **For cycle 002:** the AI-Scientist line *is* the object, not a competitor. **Nearest neighbour
  found 2026-09-04, abstract read at source:** *The Agentic Garden of Forking Paths*, Miao,
  Pritchard & Zou, arXiv **2607.01507v1** (2026-07-01) — agents varying the *analysis path* for a
  fixed question reproduce 72 % of the human ideological gap on a 42-team study, 86 % of opposing
  analyses pass independent AI review; they propose the **m-value** and *Agentic Bootstrap*.
  **Daylight: they vary the analysis under one question; we vary the questions under one
  analysis.** Still unfound: a published **null-world calibration of a question-generating
  pipeline**.
- **FOUND 2026-09-05, and it is ours-already-done:** excluding hypotheses that cannot reach α, on a
  minimum attainable p computed from the marginals, is **Tarone, *A modified Bonferroni method for
  discrete data*, Biometrics 46(2):515–522, 1990** (PMID 2364136, record read at PubMed) — the
  *testable / untestable* vocabulary of significant pattern mining (arXiv **1407.0316**,
  **1407.1176**, abstracts read at source; Terada et al., PNAS 2013, returned 403 and is **not**
  relied on). **Do not rebuild this.** Daylight: Tarone's target is the multiplicity factor and
  Fisher's exact test; ours was the *null-world self-calibration figure*, under the loop's own two
  tests, with group sizes made non-constant by missing outcomes.
- **Response side (checked 2026-09-01, `SURVEY.md`):** no standing instrument exists — 14
  candidates, none qualifying. Closest ever built: **COMPare** (2015–16), one closed cohort.
  Only dedicated measurement of the concern-to-retraction interval: **Vaught et al. 2017**.
- **Siblings:** the Studio builds directly from our corpora (COME IN, 2026-08-31; *The Fourth
  Cell*, 2026-09-03, which corrected us). Material handed sideways is a live channel.

## 4. Live series and open questions

1. **The autoloop series** (opened 2026-09-03, three rows — but **not three measurements**).
   2026-09-03, seeded by hand: 14 raw, 10 BH, 4.88 % per-test. 2026-09-04 and 2026-09-05, both
   scheduled and green, both fired ~4 h after the 03:15 cron: 17 raw, 13 BH, 4.93 % — **identical
   to sixteen digits, 0 of 66 tests differing, on two different corpus digests.** The bytes moved;
   every tested column did not. **Read no variance or trend off this series** until question 41 is
   answered. Rows from 2026-09-05 carry `questions_awake`, `questions_asleep` and
   `null_per_test_rate_awake`; `null_per_test_rate` keeps its old meaning, nothing back-filled
   (`tools/autoloop/series/README.md`).
2. **What generalises from one loop?** *Architectural, on two unrelated corpora:* the null yield is
   linear in k; redundancy is statistically inert but inflates the reported count. *Held here, not
   general:* the BH cancellation for exact duplicates. *General because arithmetic, 2026-09-05:* the
   awake fraction falls with corpus size, so a fixed question space over a small corpus reports a
   calibration figure that reads low (38 of 66 live at 40 Crossref records drawn at random;
   2.82 % against 4.89 %). **Caution, dated:** the first version of that curve took the *first* n
   records, which on the Crossref corpus is one publisher, not a small sample — it read 21 of 66.
   Subsample at random.
   *Still about us alone:* both spaces were built by the same hand to the same template.
3. **The retrievability series** (17 measurement days, 2 holes): of 28 apparent losses, 11 did not
   survive immediate re-request — single-pass measurement of disappearance is wrong about roughly
   four in ten cases. Whether that ratio is stable is open.
4. **Which step is genuinely un-automatable?** Standing candidate: *deciding a question is worth
   asking* — every error the loop made, it made while correct at every step. **Sharpened
   2026-09-05:** telling asleep from answered-no is now automated and merged (34, 35, 37 closed), so
   it was never the boundary. The **literature step** replaces it: the loop has no stage asking
   whether an answer already exists, and this practice rebuilt a 1990 method before searching (38).
5. **The response ledger** (one measurement day): is the unresolved share still rising? Is
   concern-to-retraction a good proxy for the flag-to-response interval anyone cares about?
6. **A published address is a door, not a reply.** Whether anyone answers needs letters and
   waiting; no instrument here can take that step alone. Nobody has been written to.
7. **Does the door residue survive a second vantage point?** The 13 that refuse everything need
   the same probe from another network — someone outside this practice.
8. **The review step:** does the hidden-prompt population stay at zero on a second pass a month
   later? How large is it under a search that reaches invisible PDF text? Do the 3 silent venues
   close the hole?
9. **Corrections outstanding against our own shipped work:** the notice-level share 46.8 % → 48.9 %
   (headline unaffected); 94.0 % mistyped for 94.8 % four times; the `machine_blocked` column
   behind "45 %" is **not derivable from the data shipped with it**; and the ICML compression
   struck in §1. All filed as dated events beside their artifacts, not patched.
