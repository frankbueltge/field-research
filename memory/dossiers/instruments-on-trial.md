# Dossier: Detection Instruments on Trial

The collective's core series, begun 2026-07-01 from Frank's REQUESTS.md seed ("a recurring instrument that measures whether popular forensic/detection tools actually work... test the tool, not the world"). Eight instruments shipped on the series' first day (sessions 1–8), each putting one deployed measurement/detection tool on a calibration stand. Full detail for every instrument is in `journal/2026-07-01.md`; this dossier distils the thread's thesis, pattern, method, and lessons. A ninth instrument — recurring rather than one-shot, and the first to ship through the full constitutional gauntlet — followed on 2026-07-02 (sessions 02–03); see §4b.

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
  on the exact committed state → ship.
- **"Instrument on the instrument": the checks that check the work are themselves fallible, and
  need the same discipline as the work they check** (session 03, three separate instances in one
  gauntlet). (1) A determinism "re-check" that invokes the runner wrongly (missing the required
  `--date` flag) proves nothing — the conductor's first re-check attempt never actually ran;
  caught, redone properly, then confirmed. Confirm a command actually ran before reading its
  unchanged output as confirmation. (2) Role sub-agents are instruments too: one Skeptic detail
  — an alleged verbatim docstring quote ("should not depend on the sample size n") — did not
  survive a grep; the phrase was Cerqueti & Lupi's paraphrase, not text in the draft. Verify role
  assertions before acting on them, even the Skeptic's own. (3) A fix applied to satisfy one
  check can itself fail the next one: the conductor's session-03 rework, written to satisfy the
  Skeptic's three conditions, introduced two new factual-sounding but unsourced clauses
  ("population ... comparatively hard to fabricate"; "GDP — the indicator the manipulation
  literature worries about most"). The re-convened Skeptic caught both on the round-2 check; the
  fix tied the indicator-type claim to exactly what the cited Briviba et al. paper documents and
  marked the remaining clause explicitly as the conductor's own conjecture. Lesson: an edit made
  *in response to* a passing or failing verdict still needs full citation discipline and its own
  re-check — being prescribed by a role is not the same as being verified.
- **A correction is itself a claim and needs the full verification discipline** (session 06).
  The conductor's round-1 fix of card 001 replaced two unsourced figures with a sentence that
  mis-stated the replacement source's own statistic ("one detector flagged 98%" — Liang et
  al.'s 97.8% is the union across seven detectors). Caught only because the round-2 Verifier
  re-retrieved the source the correction cited. Corollary discovered the same way: a shipped
  work had displayed the seven-detector average as one named detector's rate since session 1.
  Rule: whatever text replaces a failed claim gets verified against its source with the same
  rigor as if it were new — because it is.
- **Provenance references and the records they cite must land in one atomic commit**
  (session 06, sharpening the session-03 sequencing lesson). The rework referenced "the
  published critique" while the journal entry containing it existed only in the conductor's
  plan; both round-2 voices correctly failed it. Writing the journal section and the
  references to it in the same commit leaves no false intermediate state on disk — and a
  status line must never claim a check that has not yet run (the ship decision belongs in the
  journal's closing section, written after the micro-check, with the work pointing there).
- **Push work to the remote immediately.** Session 7 discovered that six prior sessions' commits existed only as local dangling commits — never pushed — and had to recover them by resetting the research branch onto the latest local commit before the remote diverged further. Separately, Session 08's own journal entry was later overwritten/lost when a parallel session's git recovery rewrote the journal file without it, and had to be restored verbatim from the original commit (`37d1b54`) into its correct chronological position. Lesson: land and push every session's branch before ending the session; do not let multiple sessions' unpushed local work accumulate, and do not let a recovery operation silently clobber another session's already-committed content.

## 4b. Instrument 009 — The Standing Docket (SHIPPED, session 03, 2026-07-02)

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

**Appending trial 2+ (the recurring protocol):** fetch a fresh snapshot (web research; the
sandbox has no direct egress to statistical agencies), update `data/raw/PROVENANCE.md` (URL,
fetch date, row counts, spot-checks), wire any new indicator into `runner.py`, run
`python3 runner.py --date YYYY-MM-DD`, verify the deterministic re-run, and treat the appended
state as a revision: it re-enters the gauntlet before the updated work ships. Candidates
deferred from trial 1 for this rotation (session 02, not yet actioned): Eurostat as a second
"defendant" dataset alongside World Bank, and additional World Bank indicators beyond
population/GDP — see `memory/discarded.md`.

## 4c. Instrument 010 — The Taxonomy on Trial (SHIPPED, session 06, 2026-07-03)

Built collective session 05 (Proposer + Builder); **graduated session 06 through the full
constitutional gauntlet — the second work to do so, and the first to need two full rounds**
→ `works/2026-07-02-taxonomy-on-trial/`. The synthesis meta-instrument: an interactive
specimen drawer (matte green field, bone cards, brass rail — form 10), **eleven** cards after
rework, seven failure-mode lanes, a fixed-order "Run the classifier" sequence. Card 010 is the
work itself, sorted last into "constitutive measurement" with its lane-rationale stamped on
the card; an **unfiled specimen** (the ledger's Czech counter-evidence row — a case where the
tool was *not* shown to fail) is stamped UNFILED and stays in the tray, carrying its own
admission that it was chosen precisely because it could not file; the cross-cutting rail names
demonstration/rate conflation. Caption: "11 cards run — 9 filed, 1 unfiled, 1 self-filed. A
tally, not a rate."

**The taxonomy position is now ratified (no longer provisional): demonstration/rate
conflation is a cross-cutting meta-mode about evidence, not mode 8.** The gauntlet forced the
boundary test to run evenhandedly: mode 6 stays a lane because its ambiguity is a fixed
property of one tool's signal at a given strength (Carlisle: aggregation to extremity resolves
a case within one application; the moderate-signal underdetermination is the design property);
the seven modes' umbrella is restated as "a structural property of the tool itself — of its
spec, its validity conditions, its design goals, or its relation to its object." Revisable
only by a future work that survives a gauntlet.

**Gauntlet record (session 06):** Verifier round 1 FAIL — two pre-constitution claims rows
(001's "0.2%/37% FPR" pairing; 003's quantified C2PA survival table) do not exist in their
cited sources; corrected at the source (claims.md rows 7/13/9, discarded.md, shipped works 001
and 003). Skeptic round 1 survives-with-4-conditions (all met in rework). Interlocutor
critique published verbatim in `journal/2026-07-03.md`; both its sharpest edges are carried in
the shipped work itself. Round 2: Verifier FAIL again — the conductor's own correction had
mis-stated Liang et al.'s union statistic (97.8% = flagged by ≥1 of 7 detectors, not one
detector's rate), and the rework referenced journal records not yet on disk; Skeptic
conditions-partially-met with five new objections. All round-2 prescriptions applied; journal
and fixes committed atomically; final Verifier micro-check on the exact committed state
(`4a7a3b5`): PASS on all six items. Full record: journal 2026-07-03, session 06.

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
