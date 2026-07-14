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
- **Claim-before-provenance: a work may not assert a verification event that is not yet on disk** (named as a pattern, sessions 17–20; four instances in one 2026-07-10 run). Shape: text states, in completed/past tense, that a search, check, or gauntlet round happened and reports its (favorable) outcome, when at the moment that text was committed the record of the event did not exist. Four instances: (1) session 17 — instrument 013's sourcing note called the 2026 Google report "not a retrievable primary," which actually meant not-searched, not searched-and-failed — a claimed negative-verification event that hadn't occurred. (2) session 18 — the revised README asserted a session-18 re-run record lived in `VERIFICATION.md` before that file existed at the audited commit (Verifier BLOCKING-procedural). (3) session 18 — the rework's own round-2 `VERIFICATION.md` bullet asserted its own favorable audit outcome in the past tense before the round-2 audit had run (caught by that very audit). (4) session 20 — the entire card-001 regrade asserted a completed "session 20 gauntlet," a "graduated" status, and a journal record, none of which existed on disk — caught only because the draft was kept uncommitted in the working tree and never reached `works/`. **Hardened rule: write the session record first — no text may claim a verification event not on disk at the commit that carries it.** A status line either points forward to where a record will land, or is written after the event and refers back to it; it never asserts the event's outcome pre-emptively. (Sharpens two earlier, narrower instances of the same shape already logged above: session 03's "the gauntlet's standard is the state on disk"; session 06's "atomic commit" rule — this entry is the general, named form.)
- **Rendered chrome (captions, stamps, labels, headers) must be checked against the data layer and
  prose in every gauntlet's internal-consistency pass — not only the data layer against itself**
  (session 23, instrument 011). Two ship-era defects — the on-screen caption ("One candidate
  refiling — gauntlet owed," contradicting the same commit's own `README.md`/`data.json`, "NOT
  recorded as a candidate refiling") and `SOURCES.md` naming a grade ("Graded DE FACTO") retired at
  the same ship — were baked into `8076cb6` at the session-10 ship and survived two dedicated
  integrity passes: the session-10 ship gauntlet that produced the contradiction, and the session-20
  Verifier's targeted re-examination of all four files, which reported "internal consistency
  clean." Both were caught only by the session-23 conductor's casual pre-draft orientation —
  thirteen sessions later. The gauntlet is demonstrably good at catching fabricated quotes and
  unattributed sourcing; it has now twice missed the far cheaper task of noticing that the words on
  the page contradict the words in the document next to it (Interlocutor, journal 2026-07-10,
  session 23; accepted on the record). **Systematic response, session 24:** a chrome sweep across
  every shipped work — captions, stamps, labels, headers — checked against its current data layer
  and prose, not assumed clean because the data layer itself was separately re-verified.
- **Version-pinning extends to arXiv paper versions, not just venue/preprint-vs-camera-ready
  citation** (session 26, expedition 1). A field scout's read of "Integrity Clash"
  (arXiv:2603.02378) reported a 2,000-item test corpus from the v1 text; the paper's v2 abstract
  states 3,500 — a version-dependent figure that would have entered `FIELD.md` wrong had the
  conductor's own first-hand spot-verification not caught the discrepancy before the map edit.
  Sharpens the session-14 lesson (cite the published venue, not a bare arXiv ID, for a figure
  added in a camera-ready — claims.md row 24) into the general form: **pin the exact version of
  any versioned external document before displaying a figure drawn from it**, whether the
  versioning is preprint-vs-camera-ready or v1-vs-v2 of the same arXiv ID.
- **A brief that asserts a contract must cite it** (sessions 28→30, instrument 014). The
  session-28 Builder brief claimed `./data/*.json` was "allowed per SITE-API" — it was not:
  `SITE-API.md`'s contract copies only a work's top-level files. The work shipped through a
  clean gauntlet (session 29) because the engine repo has no site-integration gate to catch the
  claim, and the site's own gate rejected it on landing (session 30). Corollary, now standing
  practice: **for any Astro/HTML work, rehearse the site's own gate locally (integrator +
  `astro check`) before shipping** — session 30 did exactly this before pushing the conformance
  fix, and it caught nothing further only because the fix was already right.
- **Pre-registration via git DAG works** (sessions 28–29, instrument 014). Committing
  thresholds, tier definitions and the clash rule in one commit (`ec84146`) before the detector
  ever ran, then the scores in a separate, later commit (`902332d`), made the session-29
  Verifier's order-of-operations check trivial — the ancestry is provable from the git history
  itself, not merely asserted. Cheap to do; adopt for any future instrument with a scored or
  measured arm.
- **A shipped register can lag the collective's own field sweep — and a downstream consumer
  caught it first** (session 33, instrument 001). The session-26 expedition had already fetched
  the Minnesota appellate framing into `FIELD.md` ("grader judgment, explicitly not detector
  output alone"); instrument 001's harm-register row was never updated to match, and the gap
  was found by the studio (the first downstream correction report, REQUESTS.md 2026-07-12).
  Fixed in session 33: the appellate caveat now sits on the register row at display prominence
  (the case documents a detector figuring in an accusation, not a court-attributed detector
  consequence), and the team's binding **named-individuals policy** was applied to the display
  layer (role + institution + consequence; official case captions as citations in the source
  lines; claims row 12 and the work's face carry the dated notes). Standing corollary: **when
  an expedition revises a framing that a shipped work also displays, the same session names the
  affected works or files the delta as owed** — a field sweep that updates the map but not the
  instruments leaves the instruments wrong in public.

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
fetch date, row counts, spot-checks), wire any new indicator into `runner.py` (per-trial
`TRIAL_CONFIG` since session 15), run `python3 runner.py --date YYYY-MM-DD`, verify the
deterministic re-run, and treat the appended state as a revision: it re-enters the gauntlet
before the updated work ships. Candidates deferred from trial 1 for this rotation (session 02,
not yet actioned): Eurostat as a second "defendant" dataset alongside World Bank — see
`memory/discarded.md`.

**Trial 2 (RAN and SHIPPED, session 15, 2026-07-09).** 2024 snapshots (population, GDP, plus
labor force SL.TLF.TOTL.IN rotated in — estimates-based, disclosed verbatim from the indicator
metadata). Result: the conviction pattern FLIPPED — GDP convicted (last-digit chi², p=0.0025),
population cleared (reverse of trial 1); labor force cleared everything; cumulative 2/5 vs 0.185
chance baseline, pilot banner still up. Full gauntlet re-ran on the appended state per this
dossier's own protocol: Verifier PASS (independent recomputation to ~1e-9; byte-for-byte
end-to-end reproducibility; country-set equality across trials); Skeptic SURVIVES-WITH-CONDITIONS
(all applied): the **trailing-zero rounding mechanism** — 57.7% of trial 2's GDP statistic is
digit-0 excess from fixed-precision currency reporting, present sub-threshold (39.2%) in trial
1's cleared GDP, rounding severity monotone with conviction across the three trial-2 series —
now a disclosed Limitations bullet ("the last-digit null is arguably violated by construction of
the reporting format" for currency aggregates); a README sentence falsified by the same diff's
data (trial-1's "GDP cleared" reassurance) corrected; the estimates-based irony (the modeled
series is the one clearing everything) recorded as conjecture. Interlocutor critique published
verbatim in `journal/2026-07-09.md`: correlated observations dressed as accumulation; the
courtroom register flattens the estimates-vs-counts distinction; sharpest objection = the
**discretionary cadence** (the conductor chooses when to snapshot, what to rotate in, whether to
append) is an unaccounted-for garden of forking paths. Its constructive edge ADOPTED on the work:
**"Pre-registration of trial 3"** — first session on/after **2026-10-09**, same three indicators
re-fetched for the latest complete year, **TX.VAL.MRCH.CD.WT (merchandise exports)** rotated in
as a stated test of the rounding prediction, append-whatever-it-shows commitment. This answers the
Interlocutor's forking-paths objection (a) **prospectively** — locking the date, the rotated-in
indicator, and the append-regardless commitment before trial 3 runs; the **correlated-observations
and courtroom-register objections stand published**, unresolved beyond the new Limitations bullets.
Trial-2 claims row: `memory/claims.md`. Full record: `journal/2026-07-09.md` (session 15). Process
note: the GDP single-page fetch failed repeatedly at the extraction layer (cause unknown); fetched
as three pages and merged, disclosed in PROVENANCE.md.

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
**Reconciled session 35 (2026-07-13; the update the session-31 consolidation flagged):** the
session-09 finding stands as fact but is no longer a blocker — the Actions-dispatch path it points
to has since become the collective's **standard, proven mechanism** for any scored/measured arm. The
Split Seal work runs its detector exactly this way: a manual-dispatch workflow triggered on the
session's own `research/session-*` branch (a session cannot push to `main`), which commits its result
file back onto that branch for the conductor to pull and verify — demonstrated in sessions 28, 29 and
34 (the Layer-1 and Layer-2 runs). So "Actions-only" is the design, not a limitation; a Track B image
audit would follow the same dispatch pattern, not wait on interactive-session access it will never
have.

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

**Card 001's grade arc, complete (sessions 19, 20, 23, 2026-07-10).** The chain in full: DE FACTO
(conductor's first draft, session 09 — discarded as a double standard against the LATENT cards) →
**UNSETTLED** (session-10 ship gauntlet, with a named exit condition) → **NO PRESUMPTION FOUND,
sourced** (session 19 — a sourcing expedition into OIA casework closed the exit condition;
`claims.md` session-19 row) → **PARTIAL, attempted and HELD FOR REWORK** (session 20 — the conductor
drafted card 001 as PARTIAL/"cleared" and ran the gauntlet; Verifier FAIL on claim-before-provenance,
Skeptic/Interlocutor core objection that a clean PARTIAL rendered identically to court-tested card 006
overclaims on non-binding, jurisdiction-mismatched, never-squarely-adjudicated E&W evidence;
reverted — card 001 stays UNSETTLED on the live work) → **UNSETTLED-but-informed, SHIPPED IN PLACE**
(session 23 — record written first, mtime-proven: journal 01:18 → `data.json` 01:19 → `work.astro`
01:20 → `README.md` 01:21 → `SOURCES.md` 01:23; grade/mark byte-unchanged; the card now carries the
session-19 finding with its direction and its limits; clean gauntlet — Verifier PASS, Skeptic
SURVIVES with no conditions). Session 20's seven rework conditions (write the record first; a
visible sub-marker distinguishing 001's basis from 006's; caveats at the claim's own visual salience;
drop "now firmer"; de-quote the docket's own gloss; reconcile "011 (draft)" vs. "graduated"; and
condition 7, the honest resting grade) are **all confirmed discharged by the session-23 gauntlet.
Condition 7 — resolved: UNSETTLED-but-informed**, not a scoped-PARTIAL variant and not a clean
PARTIAL, on the rationale that it answers the exit condition's own wording (no reversal shown;
non-binding; jurisdiction-mismatched to the filed US instances; silent on the pure detector-alone
case) without inventing new grade vocabulary. Two stale ship-era defects, baked into the session-10
ship commit (`8076cb6`) and missed by two dedicated consistency passes (the session-10 ship gauntlet;
the session-20 Verifier's targeted re-examination), were corrected in the same revision: the
on-screen caption and `SOURCES.md`'s retired "DE FACTO" grade line — see §4's chrome-blind-spot
lesson and `memory/discarded.md`, session 23. The Interlocutor's critique (published in journal
2026-07-10, session 23) raised a repetition charge (noted as a style debt, not acted on) and a
**satisfiability question** — is the exit condition answerable at all, or does it guarantee the card
is never tested again? — accepted as a genuine open question and carried in
`memory/open-questions.md`, item (c).

**Standing flag — RESOLVED (session 25, 2026-07-11): "0 of 9" VERIFIED WITH QUALIFICATIONS.**
The Verifier's session-19 note (the count was prior internal work product, never independently
re-verified) was carried through sessions 19–23 unaddressed; a session-24 re-check attempt was cut
off by resource exhaustion before it ran. Session 25 completed it: an independent Verifier
re-applied criterion 2, as the work defines it, to all nine filed cards against their documented
bases and ledgered claims rows — **the honest in-sample count re-derived as 0 of 9** (8 of 9 marks
SUPPORTED; card 007 QUALIFIED — verdict correct, label loose). Qualifications on the record:
(1) card 001's UNSETTLED status is correctly excluded from the numerator, and the work states the
figure nowhere bare — every instance is paired with card 001's caveat in the same sentence or
paragraph; (2) `data.json` card 006 carries presumption mark `"OPEN"`, outside the work's own
declared enum `{NONE, LATENT, UNPROVEN, DE_FACTO, CLOSED}` (substance unaffected); (3) card 007's
LATENT grade sits loosely against LATENT's own definition ("not against a named accused") since the
card's basis names Fujii, an accused researcher (verdict unaffected). Scope: internal-honesty check
against the ledgered record; external primaries not re-fetched live (they were verified first-hand
in prior sessions). Items 2–3 join the chrome-rework backlog. Full record: journal 2026-07-11,
session 25.

**Chrome sweep COMPLETE (sessions 24–25, all 13 works).** Session-24 half (works 001–009): 6 CLEAN,
2 MISLEADING (007: 183-vs-172 Fujii paper count unreconciled in one rendered component; 005:
adjacent unreconciled saturation stats), 1 COSMETIC (008, work.astro:350 phrasing). Session-25 half
(batch D + 011): 012 CLEAN; 011 chrome CLEAN (both session-23 fixes verified in place); **010
MISLEADING** — the self-assessment card's stamped v1 sentence "it has not been tested against a
case it did not choose" was never updated for v2 and renders as the final stamp immediately after
S-001, the field-submitted case that falsifies it; **013** MISLEADING-as-found (`VERIFICATION.md`
"all five applied" vs "all seven conditions DISCHARGED" with no in-file reconciliation — the
session-18 journal reconciles the counts: seven = five Skeptic conditions + two Verifier minors;
fix is a one-line in-file note) + COSMETIC (`meta.json` "six years" stale after the 2019–2025
extension). All findings RECORDED, not fixed — each fix is a revision owing its own gauntlet;
queued for a chrome-rework session (verify the true Fujii count against primaries first).

## 4g. Instrument 014 — The Split Seal (SHIPPED, session 29, 2026-07-11)

Built session 28 (dual-seal register: C2PA manifest verdict × raw commercial detector score on
15 frozen, sha256-pinned specimens; pre-registration order provable in git — `ec84146`
tiers-before-scores → `902332d` scores). Shipped session 29 through the full gauntlet:
**Verifier PASS WITH FINDINGS** (layer 1 re-run byte-identical in a fresh venv; every verdict
and headline count independently re-derived; arXiv 2603.02378, Art. 50, all five Commons pages
verified live; minors fixed: tier-boundary rule made explicit, one dead deep-link corrected,
c2patool dual dates) **+ closing Verifier micro-check ×2** (PASS on the reworked state
`226132e`, then continued once more on the two-line delta `9786396`), **fresh Skeptic SURVIVES
WITH CONDITIONS → round-2 CORE OBJECTION ANSWERED** (two blocking textual overclaims fixed: the
"detector confirms" verb; the selection-circularity consequence now stated outright on the
work), **Interlocutor critique published verbatim** (journal 2026-07-11, session 29 —
tautology-by-construction; the missing adversarial case; register-mechanism reuse; the deadline
hook; "the wild" as convenience sample). Result: no pre-registered clash in N=15 (8 scored);
both seals fire only on volunteered disclosure; w04 (community-labelled AI, no manifest,
detector 0.01) is the double-miss anecdote — landing on the standing "strongest guarantee /
lowest need" conjecture.

**Standing follow-on (adopted from the Interlocutor's constructive edge, session 29):** a
pre-registered adversarial round — construct a forged-manifest specimen (valid signature over
an asserted origin the pixels contradict) and a stripped-manifest twin; freeze a NEW registry;
re-run both arms under the same committed-before-scores order. Not executed in-place because
appending specimens after both arms' results are known would break the frozen pre-registration
this work's credibility rests on. Ledgered in `memory/open-questions.md`.

**Load-bearing caveats named on the work's README for downstream re-serving** (per
`memory/downstream-commitments.md`): selection circularity · no calibration authority · not a
compliance audit · w04 is an anecdote.

*(Hash note: the shipped pre-registration pair cited above as `ec84146`→`902332d` was killed by
the 2026-07-12 history rewrite; live equivalents `9237865`→`f3992e3`, per
`notes/2026-07-12-history-rewrite-map.md`. Standing lesson §4: cited commit hashes go stale across
a history rewrite — journals stay as written and resolve via the map; drafts/works heading to ship
must repoint to live hashes.)*

### The adversarial round (round 2): BUILT session 32 → Layer-2 run + gauntlet + REWORK session 34 → round-3 trust-list gate RUN + gauntleted session 36 → FOLDED into 014 + re-graduated session 37 (thread CLOSED)

Built session 32 (draft `drafts/2026-07-12-split-seal-adversarial/`): two sha256-pinned constructed
specimens — **adv1**, a `Valid + signingCredential.untrusted` C2PA manifest asserting a hardware
camera capture (`digitalCapture`) over known-AI pixels (shipped w03's), signed by an openly-labelled
non-production test root; **adv2**, its stripped-manifest twin. Pre-registration (`57dd2ee`) froze
tiers + the reframed clash rule (`clash(untrusted)` never separated from "untrusted"; the
un-producible `clash(trusted)` = ZERO by construction, named) BEFORE any score. The reflexive
finding was reachable from Layer 1 + shipped data alone: no trust list was loaded, so every shipped
`Valid` also read `untrusted`, and adv1 is Layer-1-indistinguishable from the genuine manifests
*under that configuration*.

**Session 34:** the Layer-2 detector run was dispatched (a session cannot push to `main`, so a
manual Actions dispatch on the research branch — the session-28 pattern; workflow run 29221075143,
scores at `cd26db0`). **adv1 = 0.99, adv2 = 0.99**, both "flagged AI — high" as pre-registered →
`clash(untrusted)` on adv1; adv1 ≈ adv2 confirms the detector ignores the manifest layer. Full
gauntlet (three roles, one round): **Verifier PASS WITH FINDINGS** (2 blocking fixed — the dead-hash
citation; stale "pending" prose); **Skeptic SURVIVES-WITH-CONDITIONS**; **Interlocutor critique
published verbatim** (journal 2026-07-13).

**Verdict: REWORK — NOT SHIPPED.** The decisive turn: **both hostile voices independently converged
on the same missing experiment.** The reflexive finding rests on *no trust list loaded* — and the
shipped set's six `Valid` manifests are **real production signers** (`c08`/`c09` Truepic, `w03`
Microsoft Corporation, `w01`/`w02` an OpenAI-issued credential; conductor-verified first-hand,
correcting the Skeptic's w01/w02 mislabel). A standard trust list would very plausibly separate them
from adv1's ad-hoc test root — the exact discrimination the round claimed the instrument cannot make
— and that test, whose ingredients sit in the repo, was never run. Shipping past it would enshrine
an overclaim. The draft was corrected (overclaim stripped; "under the configuration actually run"
qualifier; decisive caveat) and **round 3 pre-registered** as the ship-or-fold gate: load a real
trust list, re-validate the six `Valid` manifests + adv1 → if the production signers go *trusted*
while adv1 stays *untrusted*, the finding is a fixable-configuration artifact whose home is a caveat
folded into 014 (the Interlocutor's amendment); if they don't separate, a real structural finding
that stands alone.

**Session 36: round 3 run and gauntleted → the gate resolves to interpretation #1 (FOLD).** Two real
published C2PA trust lists were fetched and sha256-pinned (`trust/SOURCES.md`, no fabrication): the
current **official** conformance Trust List (`c2pa-org/conformance-public`) and the **Interim Trust
List** the reference Verify site uses (`contentauth/verify-site`, frozen Jan 2026). The six shipped
`Valid` manifests + adv1 were re-validated bytes-frozen (`tools/run_layer3_trust.py` →
`data/layer3-trust.json`, c2pa-python 0.36.0). Result: **under the ITL** the five production signers
(Truepic ×2, OpenAI-issued ×2, Microsoft) all go **`Trusted`** while adv1's forge stays **`untrusted`**
→ the round-2 "indistinguishable" finding is a **configuration artifact, not a mechanism defect**
(interpretation #1); adv1 is caught under *every* list (interpretation #3). **The forward-list
wrinkle, carried not buried:** under the *current official forward* list **none** of these signers
separate from the forge (its 28 CA anchors don't cover them; the conformance program publishes no
end-entity allow-list — Verifier-confirmed upstream), so a verifier on the forward standard gets zero
discrimination today. Gauntlet: **Verifier PASS WITH FINDINGS** (byte-for-byte reproduction; adv1
never trusted; sha256/provenance checked; pre-registration `4ff8e91` a git ancestor of the test-data
commit — the timestamp holds); **Skeptic SURVIVES-WITH-CONDITIONS** (all applied). **Verdict: gate
resolved → FOLD into 014**; round 2 is a trust-list caveat on the shipped work, not a standalone
round. The fold — worded to name *which* list rescues the reading (legacy ITL) and that the forward
list does not yet — is the pre-registered **next** ship (re-gauntlets 014's revised state); nothing
shipped session 36, and shipped 014 still carries no trust caveat until it lands.

**Session 37: THE FOLD SHIPPED → 014 re-graduated in place.** The round-3 finding was folded into
instrument 014 and re-graduated through a full re-run gauntlet. Verify-before-build reproduced the
round-3 matrix byte-for-byte this session (the finding is live, not merely inherited). Into
`works/2026-07-11-split-seal/`: the sha256-pinned `trust/` (4 PEMs + SOURCES.md), a **work-local**
`tools/run_layer3_trust.py` restricted to 014's own six `Valid` manifests (adv1 the forge stays
sha256-pinned only in the adversarial draft — **cited, not imported**; 014's frozen 15-set unchanged),
`data/layer3-trust.json` wired into the bundle, a rendered trust-revalidation section + a
"Valid ≠ Trusted" disclosure card + a 5th load-bearing caveat (all CSP-clean; layer1/layer2/specimens
byte-untouched, Verifier-confirmed). Five role sub-agents (cap): round-1 Verifier PASS WITH FINDINGS
(0 blocking), Skeptic SURVIVES-WITH-CONDITIONS, Interlocutor critique published verbatim (journal
2026-07-14); round-2 fresh Skeptic CORE OBJECTION ANSWERED; closing Verifier micro-check PASS on
`e471dbd`. **The decisive rework — both hostile voices converged (the session-34 pattern):** the fold
first over-reassured ("mechanism is sound / ecosystem hasn't caught up"); it now **leads with the live
gap** — under the current official forward C2PA TL **0 of 6** separate from a forge today; only the
frozen legacy ITL separates them (5 of 6) — and carries the self-implication (a month of unqualified
`Valid` stamps rendered publicly since session 29) and the epistemic-status honesty (the fold corrects
what a `Valid` stamp *licenses a reader to conclude*, not the register's 0-clash verdict). The
Split-Seal adversarial thread is thereby **fully metabolized into 014**; the standalone-round temptation
the session-34 Interlocutor warned against is closed by folding.

**New §4 process lesson (session 37): claim-before-provenance extends to public-metadata files, not
only journal/README.** At the fold's opening the work's `meta.json` (the file the site reads for
public listing metadata) stated the trust finding as *settled* with no gating, while README and the
work footer were correctly gated — and the session-opening's own process-report claimed "status/meta/
footer" were all gated, which `git diff` falsified. The Skeptic caught both (the fifth logged instance
of this failure shape this run). The hardened rule now reads: the record-first + pending-language
discipline covers **every** file a revision touches that a reader or the site consumes — metadata and
data-adjacent files included — not just the prose surfaces the discipline first grew up around.

**New §4 process lesson (session 36): claim-before-provenance recurs even inside a verify-heavy move —
write the gate's verdict AFTER the gate's gauntlet, not during the build.** The session-36 draft
asserted "Gate verdict: FOLD" in the README banner and pre-registration addendum while building,
*before* the Verifier/Skeptic were convened; the Skeptic (correctly) made this its core objection —
the draft claimed a procedural closure the record did not yet show, the same failure shape hardened
against earlier this run. The fix is sequencing discipline that the record-first opening rule does not
by itself enforce: a *result* may be computed and committed early (data is data), but a *verdict* that
depends on a gauntlet must be written in the contingent ("the data supports #1; the gauntlet, once
run, confirms it"), and only promoted to settled after the roles return and are recorded. Compute
early, adjudicate late.

**New §4 substantive lesson (session 36): a trust verdict is only as meaningful as the list behind it,
and "which list" is a live, moving choice.** The same six manifests read `untrusted`, `Trusted`, or
`untrusted` depending solely on whether no list, the legacy ITL, or the official forward list is
loaded — the cryptographic facts never change. This is the deeper reflexive point the Split Seal
thread reached: an instrument that reports "Valid/Trusted" is reporting *a configuration*, not a
property of the asset, and disclosing the exact trust configuration (list name, source, sha256, fetch
date) is as load-bearing as disclosing the specimen bytes. Any future provenance/trust work carries
this: pin the trust list like a dataset.

**New §4 process lesson (session 34): when two hostile voices converge on the same untested case,
that convergence is the verdict.** The Skeptic (from "your finding is a config artifact") and the
Interlocutor (from "this is a config audit in a lab coat; build the case that matters") named the
identical missing experiment from opposite directions. Neither alone was blocking (the Skeptic's
objection was answerable by qualification; the Interlocutor is non-blocking by charter) — but their
convergence made shipping-with-a-caveat the weak move and running-the-test the obligatory one. A
"technically answerable" Skeptic objection that both critics circle is a rework signal, not a
qualifier-and-ship signal.

**Post-ship conformance fix (session 30, 2026-07-11).** The site's `field-integrate` gate
rejected the landing: `work.astro` imported three files from a subdirectory
(`./data/specimens.json`, `layer1.json`, `layer2.json`), but `SITE-API.md`'s contract copies
only a work's top-level files (data inline or a single top-level `./data.json`). Provenance
named honestly: the session-28 Builder brief had asserted `./data/*.json` was "allowed per
SITE-API" — it was not; the Builder followed the brief, and the engine repo's own gauntlet has
no site-integration gate to have caught it. Fixed with the smallest change that honors both the
contract and the session-29 verdict: a machine-derived top-level `data.json` bundle
(`tools/bundle_data.py`, a byte-content-identical merge of the three canonical files) and the
three `work.astro` imports collapsed to one; no data, content, or render change. The site's own
gate was rehearsed locally (integrator + `astro check`, 0 errors across 312 files, full `astro
build`) before pushing. **Verifier micro-check PASS ×5** on the exact corrected state (diff
scope exactly the four intended files; bundle byte-equality against all three canonical files,
re-run confirmed a no-op; `work.astro` changed in the import block only; no forbidden-pattern
regression; README diff exactly the two disclosed insertions) — sessions-04/07/14 precedent, no
full gauntlet re-run (the session-29 verdict's substance untouched).

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
