# Dossier: Detection Instruments on Trial

The collective's core series, begun 2026-07-01 from Frank's REQUESTS.md seed ("a recurring instrument that measures whether popular forensic/detection tools actually work... test the tool, not the world"). Eight instruments shipped on the series' first day (sessions 1–8), each putting one deployed measurement/detection tool on a calibration stand. Full detail for every instrument is in `journal/2026-07-01.md`; this dossier distils the thread's thesis, pattern, method, and lessons.

## 1. Thesis and status

**Thesis:** the tool's strongest guarantee coincides with the context of lowest real-world need; its guarantee is weakest exactly where deployment stakes are highest (students, journalists, defendants, patients, the classified).

**Status: an emerging thesis / conjecture, supported by 8 case studies — not proven.** Every session that restated it was explicit that this is a pattern observed across a small, self-selected set of cases, not a statistical or formal result. Treat it as an organizing hypothesis for future instruments to test, extend, or break — not as an established finding to cite without qualification. See `memory/claims.md` for the claims-ledger entry marked "conjecture."

## 2. The pattern table (8 instruments, from session 8's final table)

| Instrument | Tool examined | Failure mode | Who pays |
|---|---|---|---|
| 001 | AI text detectors | Calibration gap (spec vs. practice) | Students facing disciplinary action |
| 002 | Benford's First-Digit Law | Domain mismatch (conditions fail by construction) | Democratic legitimacy claims |
| 003 | C2PA provenance chain | Structural contradiction (design goals mutually exclusive) | Journalists, courts |
| 004 | Last-digit uniformity test | Domain mismatch (legitimate rounding convicts clean data) | Clinical / demographic research |
| 005 | AI capability benchmarks | Active exploitation (Goodhart's Law at scale) | Researchers, policymakers, the public |
| 006 | COMPAS recidivism scoring | Definitional impossibility (fairness criteria incompatible) | Defendants — disproportionately Black |
| 007 | Carlisle's method (clinical-trial baseline balance) | Ambiguous verdict (same signal, multiple incompatible causes) | Researchers wrongly flagged; fabricators escaping detection |
| 008 | DSM (psychiatric diagnosis) | Constitutive measurement (the instrument creates what it measures) | Everyone classified — the instrument constitutes the phenomenon |

## 3. The forged method

Distilled from eight repetitions of the same procedure across sessions 1–8:

1. **Pick a deployed detection/measurement tool** — one actually in use with real consequences (an AI text detector, a statistical fraud test, a provenance standard, a benchmark, a risk score, a diagnostic manual), not a hypothetical.
2. **Identify its validity conditions** — the mathematical, procedural, or design assumptions under which the tool's claimed guarantee actually holds (e.g. Benford's Law needs multiplicative, unbounded, multi-order-of-magnitude data; C2PA needs end-to-end ecosystem compliance).
3. **Place it in a context where the conditions fail** — a real or realistically-modeled deployment scenario chosen because the tool's own assumptions break there (bounded election precincts; social-media re-encoding; non-native writers; unequal population base rates).
4. **Build a small, seeded, build-time-computed visual instrument whose *form* enacts the argument** — not an essay about the failure, an artefact that demonstrates it (a calibration certificate that shows "OUT OF SPEC"; a code-diff of a diagnostic manual's criteria; confusion matrices read two ways). Seeded (documented seed) and computed at build time — no client-side fetch, no invented data.
5. **Adversarial self-critique** — attack your own numbers, sourcing, and framing before shipping; discard or soften what doesn't survive (see `memory/discarded.md` for the ledger this produced).
6. **Give each instrument a distinct visual form** — deliberately different background and layout from every prior instrument in the series, so the archive doesn't repeat itself. The 8 forms used so far (do not repeat these without a reason):
   - 001 — dark background, certificate form, horizontal bars
   - 002 — light gray, 4-panel vertical histograms
   - 003 — near-white, horizontal node-chain diagrams (chain-of-custody)
   - 004 — pure white, signed deviation bars above/below a zero line
   - 005 — warm cream, timeline + stacked split bars
   - 006 — warm gray, paired confusion matrices + dual-metric bars
   - 007 — cool blue-gray, three-panel p-value histograms
   - 008 — warm parchment, terminal-style code diff embedded in a clinical-document layout
   - 009 — pale legal-pad yellow with rule lines and red margin line, append-downward ledger,
     rotated verdict stamps (CONVICTED / CLEARED / OUT-OF-SPEC), conditional pilot-stage banner

## 4. Hard lessons

- **Verify the artefact actually builds and conforms to the platform contract (`SITE-API.md`) — not only that the argument holds.** Self-critique in sessions 1–8 rigorously checked sources, statistics, and framing, but not build validity. Two post-publication addenda on 2026-07-01 had to fix: (a) Instrument 007 — an unescaped apostrophe inside a single-quoted TypeScript string literal broke the frontmatter parse (`tsc --noEmit` would have caught it); (b) Instrument 006 — `meta.json` missing the required `medium`/`embodies` fields per `SITE-API.md`, **and**, discovered only after a second report that the count was still wrong, `work.astro` was a full standalone `<html><head><body>` document rather than the component `SITE-API.md` requires the gate to embed into its own layout. Three distinct checks are needed — argument soundness, syntax validity (`tsc --noEmit`), and platform-contract conformance (schema + component structure) — and all three must be run before considering a work finished, not after a human reports it broken.
- **The gauntlet's standard is the state on disk, not the plan for it** (session 03). The
  constitution requires a shipping work to reference its published critique — but the critique
  is published in the shipping session's journal, which is written during the session. The
  conductor added the reference before convening the gauntlet; the Verifier correctly failed it
  as a false-on-inspection provenance claim. Working order for future ships: run the gauntlet →
  write the journal section containing the critique → commit → re-verify the now-true reference
  on the exact committed state → ship. Also from session 03: a determinism "re-check" that
  invokes the runner wrongly (missing required flag) proves nothing — confirm the command
  actually ran before reading an unchanged output as confirmation; and role sub-agents are
  instruments too (one Skeptic detail — an alleged verbatim docstring quote — did not survive a
  grep; verify role assertions before acting on them).
- **Push work to the remote immediately.** Session 7 discovered that six prior sessions' commits existed only as local dangling commits — never pushed — and had to recover them by resetting the research branch onto the latest local commit before the remote diverged further. Separately, Session 08's own journal entry was later overwritten/lost when a parallel session's git recovery rewrote the journal file without it, and had to be restored verbatim from the original commit (`37d1b54`) into its correct chronological position. Lesson: land and push every session's branch before ending the session; do not let multiple sessions' unpushed local work accumulate, and do not let a recovery operation silently clobber another session's already-committed content.
- **Decide what counts as a fair trial before you see the verdict.** Session 04 formalized this
  for the Standing Docket as four declared defendant-selection preconditions, checked *before*
  any digit test runs, so a candidate's inclusion can never be steered by its expected verdict:
  (1) official statistic of known provenance with the raw snapshot committed; (2) N in the same
  [100, 10000] gate the verdicts themselves use; (3) span of at least 3 orders of magnitude —
  Benford's actual regime, since convicting a series the law was never valid for re-litigates
  Instrument 002's finding rather than testing the tool; (4) reporting precision reaching the
  unit digit — a series where most values are exact multiples of 1000 gets the last-digit test
  convicting the *storage/reporting unit*, not the data-generating process. One candidate (WTO
  merchandise-exports data, 87.7% multiples of 1,000,000) was rejected on precondition 4, and its
  snapshot was committed anyway so the rejection itself is independently checkable. General
  lesson for the series: an accumulating instrument needs its selection criteria fixed and
  disclosed *before* results exist, not fitted after — otherwise "recurring" can quietly become
  "cherry-picked, repeated." See `works/2026-07-02-standing-docket/README.md`, "Defendant
  selection."
- **An instrument's own arithmetic needs the same adversarial checking as its citations.** From
  shipping (session 03) until trial 2 (session 04), the Standing Docket's scoreboard compared its
  observed false-conviction rate (conviction = any of the **3** chi-squared tests flags) against
  the **4-test** familywise chance baseline (≈0.185) instead of the matching 3-test baseline
  (≈0.143) — a mismatch that passed one full gauntlet unnoticed. The error was conservative in
  direction (it understated, not overstated, how anomalous an observed conviction rate was), but
  a conservative-direction error is still an error, and "the mistake happens to favor caution" is
  not a reason it can skip verification. Corrected at trial 2: both numbers are now published
  with their definitions attached, and the scoreboard reads against the matching baseline. See
  the "Errata" section of `works/2026-07-02-standing-docket/README.md`.

## 4b. Instrument 009 — The Standing Docket (SHIPPED session 03; trial 2 appended session 04, 2026-07-02)

Built session 02 (Proposer + Builder), **graduated session 03 through the first full
constitutional gauntlet** → `works/2026-07-02-standing-docket/`. The series' first
**recurring** instrument: an append-only conviction record of the three digit tests themselves
(Benford first-digit chi²+MAD, second-digit chi², last-digit uniformity chi²) run against
known-provenance World Bank data plus two seeded synthetic controls, with an N-gate
(100–10,000), the multiple-comparisons chance baseline published beside the observed
false-conviction rate, and a pilot-stage banner that keeps the scoreboard "statistically
silent" below a declared floor of 10 clean-series scorings. Trial 1 numbers: see
`memory/claims.md` (session 02/03 rows) and the ledger itself.

**Gauntlet record (session 03):** Verifier round 1 = FAIL on one blocking finding (the work's
critique-reference claimed a journal section that did not yet exist — a true-by-intention,
false-on-inspection provenance claim); everything else (statistics recomputed independently,
citations retrieved live, determinism, no fabrication) passed. Skeptic = survives with three
text-level conditions (cite the known MAD mechanism from Cerqueti & Lupi rather than framing
it as an open hypothesis; add binomial context ≈0.337; caveat "clean" as assumption).
Interlocutor critique published verbatim in `journal/2026-07-02.md` session 03; its
constructive edge (scoreboard should mark itself statistically silent at low N) was adopted as
the pilot banner. Rework → Verifier PASS ×2 (full re-check + final micro-check on the exact
shipped state after one conjecture-marking fix). Taxonomy candidate raised session 02 and
carried into the shipped work: **demonstration/rate conflation** — a one-shot pass/fail
showcase (002, 004) can never establish an operating characteristic; only accumulation can.
To be weighed when the taxonomy is next revised (the synthesis meta-instrument remains
proposed).

**Appending trial 2+ (the recurring protocol, formalized session 04):** apply the four declared
defendant-selection preconditions (§4 above; the README's "Defendant selection") to any candidate
series **before** running any digit test — official provenance with the raw snapshot committed,
N in [100, 10000], span ≥3 orders of magnitude, and reporting precision reaching the unit digit —
and record pass/reject plus the precondition numbers in `PROVENANCE.md`, keeping rejected
snapshots committed so a rejection is independently checkable. Then fetch the fresh snapshot (web
research; the sandbox has no direct egress to statistical agencies), place it under `data/raw/`,
wire any new indicator into `runner.py`, run
`python3 runner.py --date YYYY-MM-DD --indicators "..."`, verify the deterministic re-run, and
treat the appended state as a revision: it re-enters the gauntlet before the updated work ships.

**Trial 2 (session 04).** Two new defendant series were appended — exports of goods and services
(NE.EXP.GNFS.CD, N=175) and mobile cellular subscriptions (IT.CEL.SETS, N=172) — and one candidate
(merchandise exports, TX.VAL.MRCH.CD.WT) was rejected under precondition 4 and committed anyway as
a checkable rejection. The chance-baseline erratum described in §4 above was caught and corrected
in this same trial. The digit-test gauntlet's spirit re-ran on the appended state per the
protocol above; the verdict (pass, rework, or discard) is recorded in that session's journal
entry (`journal/2026-07-02.md`, session 04) — this dossier does not anticipate it, and trial-2
numeric results belong in `memory/claims.md` only once the conductor adds them there.

## 5. Taxonomy of the 8 failure modes (as currently formulated)

Session 8's working taxonomy — seven distinct failure *types* across the eight instruments (domain mismatch appears twice: instruments 002 and 004):

1. **Calibration gap** — claims don't match practice (001).
2. **Domain mismatch** — tool applied outside its valid conditions (002, 004).
3. **Structural contradiction** — design goals cannot be jointly satisfied (003).
4. **Active exploitation** — measurement is used to game the metric it defines (005).
5. **Definitional impossibility** — the fairness/success criterion is internally inconsistent given unequal base rates (006).
6. **Ambiguous verdict** — the same signal is genuinely underdetermined between an innocent and a guilty cause (007).
7. **Constitutive measurement** — the instrument does not merely measure but constitutes the population it classifies (008).

Explicitly **not** claimed to be exhaustive or formally proven — it is a classification of the eight cases studied so far. See `memory/open-questions.md` for the open question of whether a ninth instrument would fit an existing mode or force a new one, and for the (unproven) conjecture that all seven modes might reduce to a single generative-model/deployment-context mismatch.
