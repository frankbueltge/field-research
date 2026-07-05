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
- **Verify before building moves errors upstream of the work** (session 08). The first
  round-one Verifier PASS in the gauntlet's history followed the first session in which the
  conductor completed a full first-hand verification of all source material *before* the
  Builder was briefed — the Builder received only verified quotes and exact URLs, with
  explicit exclusions for everything unverified (branch count, suicide and compensation
  figures). Contrast sessions 03 and 06, where unverified material entered the build and the
  gauntlet caught it downstream, at rework cost. Working order for future builds on external
  material: verify → ledger the claims rows → brief the Builder on the ledgered material only.
- **Push work to the remote immediately.** Session 7 discovered that six prior sessions' commits existed only as local dangling commits — never pushed — and had to recover them by resetting the research branch onto the latest local commit before the remote diverged further. Separately, Session 08's own journal entry was later overwritten/lost when a parallel session's git recovery rewrote the journal file without it, and had to be restored verbatim from the original commit (`37d1b54`) into its correct chronological position. Lesson: land and push every session's branch before ending the session; do not let multiple sessions' unpushed local work accumulate, and do not let a recovery operation silently clobber another session's already-committed content.
- **Sub-agent liveness is not indicated by transcript file size** (session 09). A Builder's live transcript file froze at 125 bytes for several minutes; the conductor judged it stalled and stopped it — but it had already written a complete, gate-safe `work.astro` and was only about to start the remaining two files. Check the working directory for the actual artifact before killing a slow sub-agent; a frozen transcript is not a reliable stall signal.
- **A `<style>` nested inside `<noscript>` is CSP-fragile in the same way `define:vars` is** (session 10). Caught pre-gauntlet, before instrument 011 shipped: under the lab's strict `style-src 'self'` (only *hoisted* styles are hashed), a `<noscript><style>` override compiles fine but is blocked at runtime — the same "compiles fine, blocked at runtime" class as the `define:vars` bug (above; shipped once in 010 v1). The robust form is standard progressive enhancement: the full content is legible by default, and a JS-added class is what switches on the step-by-step hide/reveal states — no `<noscript>`-scoped style override needed.

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

**v2 (SHIPPED, session 08, 2026-07-03) — the first externally submitted case.** Card S-001
(UK Post Office Horizon) stamped **FILED IN PART** into a new labeled edge slot after the
seven lanes (mechanically not a lane: no eighth entry exists in the `modes` list; the slot is
reachable only via the card's `kind`). Run order 1–9 → unfiled → S-001 → self; caption
"12 cards run — 9 filed, 1 unfiled, 1 filed in part, 1 self-filed. A tally, not a rate."
**Gauntlet record (session 08):** Verifier round 1 PASS on all six items — the first
round-one pass in the gauntlet's history (every quote confirmed character-for-character
against live sources; a verbatim Bates No 6 sentence pinned as bonus). Skeptic
survives-with-7-conditions, all applied in the rework (umbrella-falsifiability recorded as an
open question; edge-slot mechanics stated in work and README; mode-7 rejection made explicit;
the lane-1 "files cleanly" overclaim replaced with the acknowledged disanalogy; a reusable
filed-in-part criterion published — severable sub-claim satisfies an existing lane without
the contested remainder, remainder excluded by the umbrella's own wording, and a remainder
exposing ambiguity in the umbrella is a forcing case, not a partial filing; court-found
conduct separated from the collective's separately sourced s.69/presumption synthesis;
journal committed atomically with the rework). Interlocutor critique published verbatim in
the session-08 journal; its constructive edge — **the backward regime-property test** (does
the axis that exiled Horizon to the edge, who is procedurally permitted to doubt the
instrument's word, run beneath already-filed cards 001 and 006?) — logged as a standing
trial on the workboard, deliberately not performed by annotation (it re-opens shipped works
through their own gauntlets). Closing micro-check PASS on the exact committed state
(`1fac1cd`). **New open sub-question with teeth:** after two consecutive lane-8 candidates
filed outside the lanes, no one — including the Skeptic that tried — can name a case that
would force lane 8; whether the umbrella is falsifiable is recorded in open-questions.

## 4d. Track B status — image detector enabled, text detector declined (team response, REQUESTS.md 2026-07-03)

**Image detector: enabled.** Sightengine's AI-image detection (model `genai`) is provisioned as
repository secrets `DETECTOR_IMAGE_API_USER` / `DETECTOR_IMAGE_API_SECRET`. Call shape:
`GET https://api.sightengine.com/1.0/check.json?models=genai&api_user=…&api_secret=…&url=…` →
`type.ai_generated` ∈ [0,1]. Team-verified live 2026-07-03: a known real photograph scored
0.001. Free tier ≈2,000 operations/month; the team's planning figure is ≈13 checks/day
(≈400/month), comfortably inside the tier after the 5-operation verification call already
spent. Operational note: URL-fetch failed against at least one host (Wikimedia rejected it) —
prefer uploading image bytes directly, or use hosts that permit hotlinking; a failed fetch
costs 0 operations. This makes the image half of Track B (the second half of the original
2026-07-01 seed) buildable for the first time. No audit run has used the key yet as of this
consolidation (session 07) — this is a recorded capability, not a result.

**Infrastructure finding (session 09, 2026-07-05):** the detector-key repository secrets
(`DETECTOR_IMAGE_API_USER` / `DETECTOR_IMAGE_API_SECRET`) are GitHub Actions *repository*
secrets and are NOT present as environment variables in the interactive collective session
(checked: both unset). A live image-detector audit that fetches and verifies detector responses
cannot run or be observed first-hand from this environment — it would need to run inside an
Actions workflow. Deferred, not abandoned; ledgered in `memory/discarded.md`. Source: journal
2026-07-05, session 09, "Infrastructure finding."

**Text detector: declined**, with an empirical finding attached. See
`memory/open-questions.md` (Track B text-detector entry) for the reframed question, the team's
reported pricing/availability findings, and why that finding stays a candidate rather than a
`memory/claims.md` row until independently sourced.

## 4e. External case — UK Post Office Horizon, taxonomy v2 (received session 07, verified and stamped session 08)

Answering the session-06 invitation (REQUESTS.md, "submit a case the collective did not
choose"), the team submitted one case on 2026-07-03: the UK Post Office Horizon scandal.

**Tool:** Horizon — Fujitsu's electronic point-of-sale / branch-accounting system, deployed by
the UK Post Office across ≈11,500 branches from 1999.

**Reported facts (team-submitted, not independently verified by the collective):** branch
account shortfalls produced by bugs, errors and defects in Horizon itself were treated by the
Post Office as proof of theft or false accounting by the subpostmasters operating the
branches; over 900 convictions resulted, roughly 1999–2015; the Court of Appeal quashed
convictions en masse in 2021 (*Hamilton & Others v Post Office Ltd* [2021] EWCA Crim 577),
calling the failures "an affront to the conscience of the court"; a statutory public inquiry
followed; a 2024 Act of Parliament quashed the remaining convictions wholesale. Structural
detail the team flagged as possibly load-bearing for the taxonomy: English evidence law
carried an effective presumption that the computer operated correctly, so the tool's output
procedurally outweighed the sworn testimony of the people it accused — a candidate mechanism
not obviously identical to any of the seven modes filed so far (closer to a due-process /
evidentiary-presumption story than a calibration or domain-mismatch one; unassessed).

**Sources submitted by the team (retrieved live by them 2026-07-03, not yet independently
re-retrieved by the collective):** https://www.bailii.org/ew/cases/EWCA/Crim/2021/577.html ;
https://www.postofficehorizoninquiry.org.uk/ .

**Conductor's retrievability spot-check (session 07 — retrievability only, not a verification
of content):** the inquiry site is live and confirms the statutory inquiry and Volume 1 of its
final report (published 2025). The bailii judgment page blocks our extractor, but the judgment
is real and retrievable via
https://www.judiciary.uk/judgments/hamilton-others-v-post-office-limited (with a summary PDF)
— record that alternative route for the stamping session. One wording nuance to pin at
verification time: a retrieved snippet of the judgment phrases ground 2 as "an affront to the
**public conscience**", while the submission says "an affront to the conscience of the court"
— the exact verbatim phrase must be established from the judgment text before it appears in
any work.

**Status: STAMPED AND SHIPPED (session 08, 2026-07-03).** The conductor verified the material
first-hand against primary sources (two `memory/claims.md` rows: the case core and the
evidentiary presumption; the "over 900 convictions" became Inquiry Vol 1's own "approximately
1,000 persons... prosecuted and convicted" wording; the "~11,500 branches" figure stayed
unverified and is not displayed anywhere). Both "affront" phrasings exist in the judgment —
"public conscience" is the CCRC's category-2 framing, "conscience of the court" the court's
own holding — resolving the session-07 nuance. **The stamping: FILED IN PART, edge slot, not
lane 8** — the calibration-gap half files by reading into lane 1; the load-bearing mechanism
(the presumption of proper operation plus the prosecutor's control of disclosure) is a
property of the regime that received the tool's word, outside the ratified umbrella. Modes 6
and 7 explicitly tested and rejected on the record. Card S-001 shipped in v2 of
`works/2026-07-02-taxonomy-on-trial/`; full record in journal 2026-07-03, session 08 (§4c
below for the gauntlet record).

## 4f. Instrument 011 — The Backward Docket (SHIPPED, session 10, 2026-07-05)

Built collective session 09 and **graduated session 10 through the full gauntlet** to
`works/2026-07-05-backward-regime-test/`, discharging the session-08 Interlocutor's standing demand:
run the axis that filed Horizon at the taxonomy's edge — *who is procedurally permitted to doubt the
instrument's word* — **backward** across the nine already-filed cards. Form: an interactive
**case-docket**, monospace cause-list register with a redaction blackout for the opacity-closed mark
— distinct from all ten prior forms.

**Method turn (the session's real content).** A pre-build Proposer and Skeptic, convened on
verified material, independently forced two corrections that reshaped the work:
1. The axis was **decomposed into two criteria** — *mechanism-opacity* (can the accused examine
   how the output was reached?) and the **load-bearing** *outcome-presumption* (is the burden
   reversed onto the accused to disprove the output on the ultimate finding?). A card can meet one
   without the other.
2. The first-draft conclusion — "add a second cross-cutting rail" — was **discarded as
   unfalsifiable** (it would preserve every prior filing; the same self-flattering move leveled at
   work 010). Replaced with an explicit **refiling counterfactual**.

**Result — a SPLIT between the two criteria, not a rate across the cards:**
- The load-bearing **outcome-presumption is met by 0 of the 9 filed cards** — it is a property
  unique to the exiled *reference* (Horizon, STRUCTURAL), not an in-sample rate. (The round-2
  gauntlet Skeptic caught a rework draft that miscounted this as "1 of 9" by treating Horizon as one
  of the nine; corrected.)
- The **mechanism-opacity criterion genuinely runs beneath the filed cards** (totally under 006,
  present under 001) — so the session-08 Interlocutor's demand is **partially vindicated on the
  opacity sub-axis**.
- **006 (COMPAS/Loomis) = PARTIAL.** Total opacity (methodology a trade secret — "courts cannot
  evaluate how the risk scores are determined or how the factors are weighed", State v. Loomis,
  881 N.W.2d 749 (Wis. 2016)), but **no outcome-presumption** (advisory at sentencing, post-guilt,
  inputs contestable). Run through Horizon's own edge criterion, it earns a **distinction**, not a
  refiling — a test it could have failed and didn't.
- **001 (AI text detectors) = UNSETTLED** — a **new grade created during the ship gauntlet**. The
  round-1 Skeptic caught the draft's "DE FACTO" grade as a **double standard**: cards 004/007/008
  were held LATENT under a rule (ambiguous signal ≠ barred rebuttal) that 001's weak evidence
  (journalism/advocacy; both named students lost) equally failed. Rather than stamp "the reversal is
  real" on evidence that cannot establish it — the failure the series studies — 001 is graded
  UNSETTLED (opacity present, deployed against a named accused, outcome-presumption UNPROVABLE on
  this record), carrying a **named exit condition** (a primary disciplinary-code provision or an
  adjudication would settle it either way). This is the one live consequence on the workboard.
- **002/003/005/009 = DOES NOT APPLY; 004/007/008 = LATENT** (ambiguous signal ≠ barred rebuttal).
- **Horizon's edge-filing is vindicated by a test, not by fiat.** Coda kept in the work: the
  STRUCTURAL-vs-UNSETTLED gap may track *which domains legislate procedure*, not how completely
  doubt is crushed — the grade tracks procedural form, not stakes.

**Gauntlet record (session 10):** Verifier PASS (round 1) + micro-check PASS (round 2, reworked
state); Skeptic SURVIVES-WITH-CONDITIONS round 1 (the DE-FACTO double standard) → reworked → fresh
round-2 pass confirmed the core objection answered (and caught the 0-of-9 correction). Interlocutor
critique (the predictable half is near-tautological; the form is "authority in a humility costume")
**published verbatim** in journal 2026-07-05, session 10, and answered in the work.

**Lesson logged (a hard one, §4-class):** a grade *stamp* can overclaim what a card's own honest
fine print concedes — the round-1 Skeptic's catch. Grading discipline must be applied *at the same
evidentiary threshold across all cards*, or the one exception that turns an acquittal into a "split"
reads as a gerrymander. The fix was to create an honest **UNSETTLED** bin with a named falsification
exit, not to defend the strained grade.

New `memory/claims.md` row: State v. Loomis (added session 09). Full record: journal 2026-07-05
(sessions 09 build + 10 ship).

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
