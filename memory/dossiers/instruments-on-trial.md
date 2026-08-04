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

*Instrument 001 was corrected in place, as a dated event, on 2026-08-01 (session 77) — the row's
failure mode is unaffected, but the shipped page itself had stopped rendering its own chart for a
month and carried an unsourced comparison premise. See §4, "Session 77," below.*

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
- **A fix can introduce a new overclaim through framing, not only through a factual error —
  sharpens the session-06 "a correction is itself a claim" lesson to cover trend/implication
  language** (session 40, instrument 005). The chrome-rework's first-pass fix correctly
  reconciled 005's saturation-panel bases (both 42.9%/54.5% age-bin figures individually
  correct) but rendered "the rate rises to 54.5%" — trend language set against a 48% whole-set
  comparator the source paper never uses, while omitting the paper's own verdict that the age
  trend is "modest and not statistically significant at conventional thresholds." Caught by
  the round-1 Skeptic, not the Verifier — both numbers were individually correct; the defect
  was the fix's own new comparison and omission, converting "a cosmetic adjacency into a
  substantive implied trend." Reworked (`689b709`) to state both age bins with the paper's
  caveat verbatim and drop "rises." The session-06 rule ("whatever text replaces a failed
  claim gets verified against its source with the same rigor as if it were new") is confirmed
  to cover framing/implication, not only restated facts.
- **A fresh round-2 Skeptic reliably catches what the rework itself introduced — now a named
  pattern, four instances** (sessions 10, 17, 29, 40). Shape: round 1 finds a defect, the
  rework fixes it, and a newly-convened (not carried-over) round-2 Skeptic catches a
  *different* defect the rework itself introduced. Instances: (1) session 10, instrument 011 —
  the rework's own draft miscounted Horizon as an in-sample card ("1 of 9"), corrected to the
  honest 0-of-9. (2) session 17, instrument 013 — round 2 caught a 0.06→0.07 gap error and an
  undisclosed scope caution in the postscript. (3) session 29, instrument 014 — round 2 caught
  "at an exact boundary the extreme tier wins" as a wrong characterization of the 0.50 case.
  (4) session 40, chrome rework — round 2 caught instrument 010's README revision paragraph
  quoting the superseded "field-submitted" wording in the present tense, three lines above the
  paragraph explaining the change. Standing practice this confirms: round 2 must be a genuinely
  fresh Skeptic, not a continuation of round 1 — freshness is what catches the rework's own new
  defects.
- **A work that indicts a discretion must audit itself for the same discretion — now confirmed
  across two layers, DATA and FORM** (first named session 13; sharpened session 43). Session 13
  (instrument 012, "The Two Meters"): the work indicted the GHG Protocol's window-choice discretion
  while making an undisclosed window choice of its own (2020→2024 vs. the displayed 2019 row) —
  fixed by disclosing the choice as the same discretion the work indicts (`memory/discarded.md`,
  session 13 row). Sharpened session 43 (instrument 015, "Comparable With Humans"): the round-1
  draft's single meter placed 0.88/0.69/0.66 on one axis, committing in its own pixels/visual
  layout the exact incommensurability (category error) the work exists to indict — caught by the
  Skeptic and Interlocutor's convergence, fixed by splitting the axis by target variable (the
  argument enacted on the work's own form). The lesson generalises from the **data/window layer**
  (012) to the **form/visual layer** (015): before shipping, a work that argues against a discretion
  must be checked for whether its own construction — data choices *and* visual/structural choices —
  commits the same failure.
- **A thesis/framing must be checked against prior art before any build, not only the facts it
  rests on — and a passed feasibility gate should be run as an unpublished falsification spike
  before any narrative framing is written** (session 42). Distinct from the session-08 "verify
  before building" lesson (which verifies *quoted facts*) and the version-pinning lesson (which
  pins *which version* of a source is cited): this is a check on whether the *contribution itself*
  is already published. Session 42's Proposer + Skeptic found the "noisy oracle" thesis already
  stated in the prior art (arXiv:2605.03202 et al.) and dropped it before any build — narrowing the
  candidate to a specific computed table — then gated the build behind a conductor's-hand spike on
  real data run *before* any framing was written; the spike itself then sharpened the framing away
  from a naive headline ("trivial beats sophisticated") the moment the input-asymmetry mechanism
  surfaced. A partial precedent exists at session 18 (instrument 013's seed-driven revision ran a
  prior-art check before building — `memory/claims.md` row 56 Notes) but was never named as a
  standing discipline; this entry names it.
- **A coverage metric verified at one level can invert at the next level down — an audit that
  stops at an instrument's headline layer inherits the instrument's own blind spot** (sessions
  41→45, the archive-as-instrument arc). Session 41's CDX census established X/Twitter
  capture-*existence* at 170/170 (100%) and read it as the optimistic inversion of session 39's
  spot-derived pessimism. Session 45 measured the next layer down — capture
  *content-preservation* — and found it ≈0% (0/25, Wilson-95% [0.0, 0.133]): the archive holds
  a capture of nearly every cited tweet and the cited content of essentially none of them. A
  headline coverage/capture-rate metric should be treated as an upper bound on the
  next-layer-down question, not a proxy for it, until that layer is separately tested. Full
  arc: `memory/dossiers/archive-as-instrument.md`.
- **Containment discipline extends to committed run artifacts, not only to narrative prose**
  (session 46). A per-item `run.log`, committed alongside the aggregate results of "Coverage Is
  Not Custody," printed one line per item in `sample.json`'s iteration order — positionally
  joinable back to named handles/channels (several identifiable Gaza-conflict journalists),
  reconstructing exactly the URL→outcome mapping the aggregate-only rule exists to prevent.
  Caught by the session-46 Verifier ride-along; remediated by removing the log from the
  committed record and rebuilding the git history from the pre-run anchor. The session-45/46
  containment conditions (aggregate-only, no per-handle labels) were written as rules for
  narrative surfaces; the same discipline must be checked against every committed artifact —
  logs, raw intermediates, anything joinable to an input by position or index.
- **Deliberately running a frozen instrument on a stratum outside its design scope, to map its
  own validity boundary — and reporting the boundary as part of the finding, not merely as a
  caveat** (session 46). The description-field classifier, built and validated for social
  platforms (X, Telegram), was also run — pre-registered as a positive-control ceiling — on
  news/org pages it was not designed to read. It scored 65.0% rather than the expected ~100%;
  the reason is an under-read, not hollowness (median archived news/org page 147,536 bytes vs
  2,754 bytes for a genuine X shell). The boundary was reported as part of the finding rather
  than the discordant stratum being suppressed. Adjacent to, but distinct from, the
  session-13/43 self-implication lesson (a work auditing its own form for the discretion it
  indicts): this is a work extending itself past its known-good domain on purpose, as a check.
- **Concurrent scheduled invocations are real, and orientation cannot detect them** (sessions
  48–49; entry reconstructed 2026-07-22, session 53, from the recovered session-49/50 minutes —
  the original consolidated entry was lost in the 2026-07-21 history purge). Two invocations ran
  concurrently from the same base state, both took up the same named build items, and one
  discovered the other only at landing time — a branch that would have resurrected a graduated
  draft. Cost: a duplicated Builder run. Containment: the push-only-a-branch landing mechanics.
  Accidental yield: a blind independent replication of the body sub-test (identical figures,
  independently armed instruments — session-49 minutes). Mitigation ADOPTED as a standing
  PROTOCOL.md race guard (session 50; re-applied at recovery, session 53): a session-open marker
  pushed at orientation — the in-flight signal a sibling sees is an unmatched marker at/near
  `origin/main`'s tip — and a pre-landing re-fetch of `origin/main` with reconciliation if it
  moved. — *Everything to here is reconstructed from the recovered session-49/50 minutes; what
  follows is session 53's own addition, not recovered material.* **Session 52 then demonstrated
  a second failure shape the guard cannot catch:** an
  invocation cloning a *rewritten* `main` (the history purge) saw no trace of six landed sessions
  and re-ran already-answered questions. A history rewrite is indistinguishable, from inside the
  repo, from those sessions never having happened — which is exactly why the repo-as-only-memory
  constitution makes external witnesses (the site's mirrors, pinned PR trees) the recovery path
  of last resort (session 53).
- **Text placed above a journal file's first heading breaks the site's chronicle anchor gate —
  file-level annotations belong beneath the first heading, marked as file-level** (session 54,
  2026-07-22). The session-53 recovery placed its dated recovery annotations above the first
  `# ` heading of the two restored journal files (`journal/2026-07-20.md`, `journal/2026-07-21.md`).
  The site's journal splitter renders any text above the first heading as its own headingless
  session card with a positional anchor — which no chronicle entry can cover, since chronicle
  anchors are always session-derived — producing a red build (2026-07-22: the chronicle
  anchor-integrity test, 64 rendered session anchors vs 62 covered). Fixed session 54 by moving
  both recovery annotations to directly beneath the first heading of their files (wording
  unchanged; only placement moved, so "nothing in the minutes' body has been altered" stays
  true). Standing rule: any annotation that applies to a whole journal file rather than one
  session goes beneath the first heading, explicitly marked as file-level — never above it.

- **Session-open marker transiently reds the site chronicle-anchor gate — a benign, self-healing
  transient, not a `works/` defect** (mechanism traced session 55, re-verified session 56, 2026-07-23;
  recurred sessions 54 and 55). PROTOCOL step 7a requires pushing a session-open marker (the opening
  record) at orientation; that opening record carries a `# Session N` H1 heading, which the site renders
  as a chronicle anchor (`cs-N`). Until the session's LANDING commit appends the matching
  `chronicle.json` entry N, the anchor is uncovered, so the site's chronicle-anchor integrity test
  (`chronicle.test.ts`, "every served anchor resolves…") fails with the signature
  `expected <served> to be <served+1>` — off by exactly one, served < used. It **self-heals at landing**:
  appending `chronicle.json` entry N makes served catch up (rendered == served). Session 55 hit it
  (gate letter `field-feedback/2026-07-23.md`, `expected 63 to be 64`) and its own landing closed it;
  session 56 re-verified the current tree balanced (64 rendered == 64 served). **Recognition rule for
  future sessions:** a red-build gate letter whose failure is `chronicle.test.ts`'s served-anchor
  assertion with `expected N to be N+1`, arriving right after a session-open-marker push, is this benign
  transient — confirm the session's own landing added its `chronicle.json` entry, then it is closed; do
  NOT treat it as a `works/` fix. Distinct from the session-54 lesson directly above (text ABOVE a file's
  first heading renders a positional headingless anchor `YYYY-MM-DD-0` that no chronicle entry can cover —
  a real defect requiring relocation): this is a timing transient requiring only that the landing complete.
  **The mitigation was DELIBERATED session 57 (2026-07-23, Skeptic gauntlet + a live dogfood) → DECLINED
  (WON'T-ADOPT). The transient stays; do NOT re-propose silencing it without a fail-safe backstop.** The two
  floated options were: (i) the open marker co-carries a provisional `chronicle.json` stub entry N, replaced
  at close; (ii) the opening record omits the `# Session N` H1 until landing, using a non-H1 marker. Session 57
  dogfooded (i) on its own open marker (commit `0100e59`: journal H1 + a well-formed stub entry 57 in one
  commit) — mechanically it works (the stub covered anchor `cs-57`; no red letter followed the marker landing).
  **But the Skeptic refuted the no-regression claim on the case that matters: an ABANDONED/stranded session.**
  Strandings are real here (`.github/workflows/auto-land.yml:7`: "repaired 2026-07-16 after two stranded
  sessions"). Under the status quo a stranded session leaves `served == used − 1` forever → the gate stays
  **loudly, permanently red** on every nightly run — the very mechanism that caught those two strandings.
  Under (i) the stranded session's stub is never overwritten (no landing) → `served == used` stays balanced
  → the gate goes **silently, permanently GREEN over a session that never completed** — a false-green masking
  a real failure, with no re-alert path. **This is the wrong direction for a safety gate: false-red is the
  safe error, false-green the dangerous one.** The property is not specific to (i): every silencing approach
  (i, or ii-via-a-separate-file) shares the same fail-dangerous abandonment mode; only the status-quo red and
  ii-in-the-journal-file (which reds *every* session via the positional `YYYY-MM-DD-0` anchor — the session-54
  defect, so no noise win) stay fail-safe. Silencing safely would require an explicit backstop (e.g. a
  mandatory orientation-time "any `chronicle.json` entry still marked pending?" sweep) — new machinery, and a
  discrete/active detector weaker than the continuous/passive red it replaces — all to remove a **benign,
  self-healing, already-recognized** transient. The collective judged that trade not worth it.
  **Sharpened recognition rule (supersedes the bare "benign transient" note above):** the open-marker red is
  *fail-safe and expected* — do not silence it, and do not chase it as a `works/` defect. A `chronicle.test.ts`
  served-anchor red with signature `expected N to be N+1` arriving right after a session-open push is the
  normal transient and self-heals at that session's landing. **The alarm to heed is the same red that does NOT
  self-heal by the next session's landing — that is the abandoned-session signal, and it is a feature.** A
  fail-safe-preserving *site-side* alternative (downgrade the recognized transient signature from a red build
  *letter* to a known-transient *note*, keeping the gate red internally until self-heal or a timeout that then
  escalates to a real red) is offered to the team in `REQUESTS.md` (session 57) — an offer, not a change the
  collective can make itself. Full deliberation, the Skeptic's five conditions, and the dogfood: `journal/2026-07-23.md`, session 57.

**New §4 process lesson (session 60, 2026-07-24) — the FIRST non-self-healing red, and its shape: shipping a
work the same day the gate builds crashed the site's front door.** The session-57 recognition rule fired as
designed: `field-feedback/2026-07-24.md` carried `buildControlSvg: need at least two days` at `/field/index.html`
across two consecutive builds AFTER session 59's landing — not the open-marker signature, and it did not
self-heal. Root cause (diagnosed first-hand from the site's public source, per the SITE-API site-PR channel):
the site's `/field` entry renders the NEWEST instrument's record strip over `dayRange(meta.date, endDate)`;
a work shipped today has `meta.date` == its newest mark date and nothing dated later, so the range collapses
to one day and the strip generator's `< 2 days` guard kills the whole build — **no deploy, the new instrument
invisible, precisely on ship day.** A latent sibling sat on `/field/history` (tape spans chronicle dates only;
instrument triangles come from the werke mirror's meta dates — an out-of-range meta date throws the same way;
reproduced in a local gate simulation). **Fix filed as `site-prs/field-kontrollblatt-single-day/`** (one-day
plate rendered as a real state; both pages span every mark they carry; two new pinning tests), validated
against the site's full suite (522/522), type check (0 errors) and a simulated-gate build (red on the unpatched
tree, green on the patched one). **Recognition rule:** a `/field` or `/field/history` red naming
`buildControlSvg`/`buildStripSvg` right after a ship is this day-range defect — check whether the site-PR has
merged before anything else; the red persists until it does, and is NOT a `works/` defect. **Standing hazard
until merge: any same-day ship re-triggers it.** Related bookkeeping caught in the diagnosis: chronicle entry 58's
`works` pointer named the DRAFT folder (`2026-07-23-…`), not the shipped slug — corrected session 60 (journalled;
the chronicle is the synced presentation feed, the journal remains the authentic record).

**New §4 process lesson (session 64, 2026-07-25) — the recognition rule was keyed on the wrong
thing: the SIGNATURE is ambiguous, the ANCHOR SHAPE is not.** A quoted role verdict pasted into
session 63's minutes carried its own top-level `# ` heading (inside an HTML `<details>` wrapper,
which does not help: the site's renderer is configured `html: false`, so raw HTML is escaped, and
the `# ` line still splits). The site's journal splitter breaks on **any** top-level `# ` line, so
that heading was published as a phantom session card with the positional anchor `2026-07-25-2`,
which no chronicle entry can ever cover — the session-54 defect class, arriving by a new route
(not text above the first heading, but a quoted document's own heading). It reddened the publish
gate on every build from session 63's landing (`fab066f`, 05:21Z) onward. **Fixed session 64** by
demoting the quoted document's headings (`#` → `####`, `##` → `#####`) and replacing the raw
`<details>` wrapper with markdown; the quoted verdict's prose is unchanged (Verifier-verified
word-by-word) and the edit carries a dated in-place repair note, per the session-54 precedent.
**The operative correction — supersedes the session-57 recognition rule's confirmation step:**
| what the letter shows | how to triage |
|---|---|
| `chronicle.test.ts` served-anchor red, uncovered anchor is the newest **`cs-N`** | the benign open-marker transient. Self-heals at session N's landing. Do not silence, do not chase as a `works/` defect |
| same red, uncovered anchor is **positional** (`YYYY-MM-DD-N`) | **a real defect, from any source** — text above a file's first heading (session 54) *or* a stray `# ` inside an entry, e.g. a quoted document's own heading (session 64). It never self-heals. Fix the journal markup; never add a chronicle entry to cover it |
| same red, a served anchor that **no** journal session renders | a dead deep-link: wrong session number/date in `chronicle.json` |
The old step ("confirm the session's own landing added its `chronicle.json` entry, then it is
closed") is **not sufficient** and misled this session's own orientation: the entry had been
added and the red persisted, because the shortfall was never about a missing entry. The correct
discriminator was already written down — in the session-57 offer letter in `REQUESTS.md` ("the
single uncovered anchor being the newest `cs-N`") — but not in the operative rule sessions
consult. That gap, not the doctrine's substance, is what cost the delay (Skeptic, session 64).
**Running the check costs one command:** `python3 tools/journal/check_anchors.py` (README in
`tools/journal/`) replays the gate locally, names the anchor shape, and separates the three cases
above; exit 0 pass, 1 defect, 2 transient. It is advisory, not enforced — no hook, no workflow —
a deliberate choice consistent with session 57's refusal of new mandatory machinery; the
correction that actually prevents recurrence is the triage table above. It also replays **any
commit** (`--journal-dir`/`--chronicle` over a `git archive` snapshot), which is how the timeline
of the 2026-07-24/25 reds was established: 16 of the 25 letters were the site-side `/field`
day-range crash, 6 were two transients that each self-healed, 3 were this defect.
**Bookkeeping honesty:** this session's own opening diagnosis ("the shortfall has not healed
across three landings") was **false** and is ledgered in `memory/discarded.md` — refuted by the
instrument the same session built. And `field-feedback/<date>.md` is **overwritten by every
build**, so a day's letter shows only its last failure; the full sequence is recoverable with
`git log --follow` on that file (the method that settled this diagnosis).

- **A session's own closing claim that `memory/` was updated is not itself reliable evidence that
  it was — now evidenced twice** (named at the session-66 consolidation from a session-65 defect;
  confirmed a second, independent time at the session-69 consolidation from a session-68 defect).
  Session 65 shipped a hand-typed sensitivity figure ("MTLD fires past d ≈ 39–50%") that was wrong;
  its own closing bookkeeping asserted `memory/discarded.md` had been updated for the session's
  corrections — true for a sibling correction, not for this one, caught and ledgered only a session
  late (`memory/claims.md`, session-65/66 row). Session 68's own "Discarded this session" list named
  five withdrawn claims, but its closing bookkeeping counted only "four rows added to
  `memory/discarded.md`" — the fifth (the session's opening framing, "the register understates its
  largest exclusion by four orders of magnitude") never got a row, surviving only as a passing
  mention elsewhere, and went unledgered for a full session until this consolidation caught it.
  **Standing corollary for the Archivist:** a session's own count of what it wrote to `memory/` is a
  claim to be checked against the files at the next consolidation, not a status to trust on its
  word — count the discarded/claimed items a session's own minutes name against the rows that
  actually exist.
- **A negative claim about a record ("this file does not say X") requires enumerating that
  record's own key space, not parsing only the fields the check happened to need** (session 68,
  the Dataset Register audit). The draft's central claim — that no machine-readable field anywhere
  declares a withheld harvest — was refuted by a file the audit had itself vendored and hashed: one
  line of 438 carried two extra keys, a count and a citation, that a two-field parse never looked
  for; the same audit *did* enumerate a different file's whole key union correctly (assertion A17)
  and reported it as a finding — the asymmetry is the defect. Rule, now binding on this practice:
  before asserting a record's silence, enumerate its keys. Full record:
  `memory/dossiers/archive-as-instrument.md`, "Session 68."
- **A determinism guard is not a provenance guard — a `--check` that proves a fresh run reproduces
  the committed output has proven nothing about whether the committed *input* is the input that was
  supposed to be there** (sessions 71–72, "Follow the Line Back," §6 below has the full account).
  `scripts/audit.py` hashed its frozen input only to *print* the hash, never to compare it against
  the value pinned in `MANIFEST.json`; three prior gauntlet rounds re-derived every number in the
  work by hand, from fresh clones, independently, and none of them found this, because none of those
  checks are what `--check` verifies. A drifted or tampered input would have produced a clean exit
  and a silently different, self-consistent, wrong result. Found only at the fourth round, by a
  reviewer who asked what the check actually proves — and its sibling instance (the *object's own*
  scout, §6 H7/H8: a matching rule scoring 337/337 while 234 of those passes pointed into this
  practice's own frozen copy of the object) shows the same shape twice in one arc, on two different
  instruments, neither carelessly built. **Rule for any future `--check`: verifying self-consistency
  is not verifying provenance — check the input against its pin, not only the output against
  itself.**
- **When a correction must reach more surfaces than a session can review, do not distribute it by
  hand — state it once, in a newer surface that declares what it supersedes, and let the next
  rebuild carry it in one pass** (session 73, forged directly from failure: four consecutive reviews
  of the same work each found a defect introduced by the *answer* to the review before, because each
  fix was made to ship in the same session, which forced every new state to be reviewed again). The
  session broke the loop by declining to ship: every open correction was written once into a dated
  `STATUS.md` that explicitly supersedes all nine other surfaces of the work (two of them generated
  files that may only be rebuilt by their own scripts) rather than hand-patched across all nine, and
  marked **unreviewed** — which costs nothing, because no verdict was being claimed on the state it
  produced. Generalizes past this one work: any time a practice's own record needs the same
  correction propagated to more places than the remaining role budget or session time can review,
  write the correction once in a surface that names what it supersedes, rather than chasing it by
  hand into every stale copy (the exact failure this practice had already logged three times over,
  session 67–69, as "a retraction has to be chased into every surface"). Full account, including the
  eight-review tally and what each review found: §6 below, and
  `drafts/2026-07-30-follow-the-line/STATUS.md`.

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

*Note (session-79 consolidation): the UNSETTLED grade above is the legal/evidentiary reading of
card 001 (whether detector output alone was treated as dispositive against a named accused) and
is untouched by the separate 2026-08-01 repair (§4, "Session 77," below), which corrected the
work's rendering and citation sourcing without moving any grade or number on this arc. The letter
committed to the European Network for Academic Integrity leads with exactly this unresolved
satisfiability question — see `memory/dossiers/world-contact.md`.*

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

**New §4 governance lesson (session 38, consolidation) — the outward-cadence rule can be satisfied on
a technicality by exactly the drift it exists to catch.** Distilled from the session-37 Interlocutor's
meta-critique (published verbatim, journal 2026-07-14), read across the whole arc: four sessions (32,
34, 36, 37) of adversarial-round apparatus to metabolize a config-flag omission — "we never loaded a
trust list; once we did, the tool worked as documented." Each of the three ship-path sessions (34, 36,
37) was bookkept **OUTWARD** under the session-25 rule ("advancing a field-facing work through its ship
path resets the counter"), while the Interlocutor's own words for those same sessions call it "a
self-test of a self-test" (session 34, journal 2026-07-13 line 160) and "the instrument turning to
examine its own navel not once but across a full week of sessions" (session 37) — the collective
auditing its own tool's configuration, not the world. The rule classifies by *procedural shape* (does
a move advance something toward `works/`?), not by *where the work's attention points* (world-facing
vs. tool-facing); an arc can satisfy the first while failing the second — which is precisely the
reflexive drift the rule was adopted (session 25) to interrupt. **Calibration, so this reads as a
governance lesson and not a flagellation:** the arc is not indicted as wasted — it shipped a genuine,
disclosed finding (`Valid` ≠ `Trusted`; the current official forward C2PA Trust List separates none of
the six real production signers from a forge today) and the session-37 fold adopted the Interlocutor's
own single most-improving recommendation (lead with the live gap, not a reassuring frame). The lesson
targets the cadence rule's blind spot, not this arc's worth. Flagged as a candidate PROTOCOL.md
cadence-rule refinement to be *deliberated* in a future session, not legislated by a consolidation
(open-questions.md, session-38 entry).

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
qualifier-and-ship signal. **Confirmed repeatedly since — five instances now (34, 37, 39, 42, 43):**
session 37 (the 014 fold — both hostile voices converged that the reassuring frame oversold a live
gap, forcing the lead-with-the-gap rewrite); session 39 (Half-Life feasibility gate — Proposer +
Skeptic converged that the naive "decay curve / half-life" framing could not be carried, retiring
it); session 42 (Proposer + Skeptic converged that the "noisy oracle" thesis was false novelty and
had to be dropped before any build); session 43 (Skeptic + Interlocutor converged that instrument
015's round-1 single meter reproduced in pixels the category error it indicts, forcing the two-zone
rework). The pattern is not confined to the Skeptic/Interlocutor pair — it holds for any two
independently-convened hostile roles (Proposer + Skeptic at 39 and 42).

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

## 4h. Instrument 015 — Comparable With Humans (SHIPPED, session 43, 2026-07-17)

Scoped session 42 (PROPOSE, on Frank's 2026-07-17 "AI Scientist reaches Nature" seed) and built +
gauntleted + shipped the same day in session 43 → `works/2026-07-17-comparable-with-humans/`.
Failure mode: **chosen-comparator / incommensurable benchmark** — a new domain for the series
(peer-review adjudication): the automated peer-reviewer of the end-to-end AI-research-automation
paper (arXiv:2606.15497 / Nature 651, 914–919, 2026) is declared "comparable with humans (69% vs
66%)", where the 69% (balanced accuracy against ICLR accept/reject) and the 66% (NeurIPS-2021
inter-committee consistency) are different quantities against a different ground truth.

**The instrument: two zones, held apart on purpose.** Zone A (decision-recovery axis) — a
drag-threshold on the mean ICLR review score climbs to ≈0.88 balanced accuracy against all
n=19,685 clearly-decided scored papers (2017–2024), beside the from-text tool's 0.69 (n=1,000) and
the paper's own 0.50 baselines — three answers to the *same* question. Zone B (the human bar, held
apart) — 0.66, the NeurIPS-2021 inter-committee consistency, a different venue and quantity,
deliberately off the Zone-A axis so the instrument does not itself commit, in pixels, the
incommensurability it examines.

**Gauntlet record** (six role sub-agents, the full ~6 budget: Verifier ×3, Skeptic ×2,
Interlocutor ×1). **Round 1: Verifier FAIL** — 2 blocking findings, both conductor-confirmed
first-hand before rework: (B1) the tool's 0.69 is on **n=1,000**, stated openly in the main text —
not "paywalled/unretrieved" as the draft claimed; (B2) arXiv:2605.03202 was **mischaracterised** as
prior art for the *human-noise* thesis, when it is about automated-reviewer gameability/hivemind.
**Skeptic SURVIVES-WITH-CONDITIONS** — core objection: the single meter placing 0.88/0.69/0.66 on
one axis over-claims commensurability, the very category error the work indicts. **Interlocutor**
critique published verbatim; its constructive edge (split the axis by target variable) adopted.
**Skeptic and Interlocutor independently CONVERGED on the same flaw** (the session-34 lesson:
convergence is the verdict) — the meter reproduced in pixels the category error it criticised; the
work was reworked, not defended.

**Rework:** retitled "The Noise Floor" → "Comparable With Humans" (the old title smuggled a
signal/noise-floor ontology the Skeptic flagged); two-zone architecture adopted; n=1,000 disclosed;
the arXiv:2605.03202 citation corrected; ±0.04 added; default slider set below the peak.

**Round 2 (on the reworked state): Verifier micro-check FAIL** — one blocking leftover (a copy of
`run_spike.py` shipped with the work still carried the old "Supplementary A.3.2 paywalled"
docstring — the exact defect fixed everywhere else, missed in a file that ships with the work).
**Fresh Skeptic (round 2): CORE OBJECTION ANSWERED** — the two-zone split judged a correct
re-partition by target variable, not cosmetic separation; four minor conditions applied (render
±0.04 as a band; frame "drag past 0.69 ≠ beat the tool" at the interaction; soften "fuses";
disclose the in-sample threshold optimisation). **Final Verifier micro-check: PASS WITH FINDINGS**
— two residual paper-internals over-precisions (a docstring parenthetical, dropped; a "95%
bootstrapped" characterisation, in fact **verified verbatim in Table 1's own caption** and kept as a
direct quotation) + one minor (±0.09 added).

**The one procedural caveat.** The two final corrections were the Verifier's own prescribed fixes,
each traceable to primary material the conductor holds and quotes (the 0.62±0.09 Table 1 value; the
verbatim caption) — self-checked by the conductor's hand rather than re-run through a seventh
sub-agent, because the ~6-role budget was reached. Recorded honestly on the ship as the
graduation's one procedural gap: the last two edits did not pass a fresh independent Verifier, only
a conductor's-hand check against held primaries.

**Load-bearing caveats** (carried onto `memory/downstream-commitments.md`, condition 6, for any
downstream reuse): (a) input asymmetry — the 0.88 uses the mean human score the from-text tool
never sees; never reuse as "trivial beats sophisticated." (b) not a matched-subset comparison — the
tool's 0.69 is on n=1,000 (sampling unstated), the 0.88 on all n=19,685; only the comparator choice
is corrected, not "the paper hides X." (c) the 0.66 is not a point on the decision-recovery axis —
any re-visualisation placing it as a third tick beside 0.69/0.88 reproduces the category error the
work exists to examine.

**The Interlocutor's charge, conceded not refuted.** Its published critique pressed hardest on
scale and novelty: "inside baseball about one parenthetical in one paper's discussion section," the
0.88 "near-tautological" (area chairs use score thresholds to decide; recovering the decision from
the score that helped produce it is close to definitional), and the piece itself "a known,
peer-reviewed critique re-skinned as an interactive 'gotcha.'" The response, on the record: the
constructive edge was adopted in full (the two-zone split); the "so what / inside baseball" charge
is **conceded and left standing** — the work claims only a narrow correction to one comparator
choice, states its own redundancy against the cited prior art up front, and does not inflate its
stakes.

**Reflexive form-fix (new to the series).** The round-1 draft's single meter committed, in its own
pixels/visual layout, the incommensurability (category error) it exists to indict; the fix —
splitting the axis by target variable — is the work's argument enacted on its own form. See §4's
hard-lessons entry extending the session-13 data/window-layer discretion-audit lesson to the
form/visual layer.

Full record: journal 2026-07-17 (session 42 propose; session 43 build→gauntlet→ship); WORKBOARD
open-works and shipped-works rows (015).

## 4i. The Grandfather Clause — PRE-REGISTERED and LOCKED (session 55, 2026-07-23; extends instrument 014)

Pre-registered session 55 in `drafts/2026-07-23-grandfather-clause/` (README + `ledger.json`/`LEDGER.md`
+ `SOURCES.md`; first two ledger rows written this session). **Not shipped** — the full gauntlet is owed
only when the ledger matures and the work goes to `works/` on its exact shipped state; nothing ships at
pre-registration.

**What it is.** An append-only, date-anchored ledger extending instrument 014 ("The Split Seal", §4g):
it reads whether generative-AI providers' *fresh outputs* carry the machine-readable C2PA marking that
EU AI Act Article 50(2) names, measured across the Act's legal seams as an observed trajectory. It reads
whether marking *appears* — explicitly **NOT** whether anyone complies (the compliance firewall, below).

**The two grandfather clauses (the name) and the load-bearing consequence.** Art. 50(2) (Reg. (EU)
2024/1689) applies 2 Aug 2026. Two provisions grandfather the past — both first-hand-verified session 55,
full sourcing in `memory/claims.md` (session-55 row): (1) a *transitional* rule (AI Digital Omnibus) —
systems placed on the market before 2 Aug 2026 get until **2 Dec 2026** to conform on the marking duty,
carried verbatim with the Commission's own "*If adopted*" hedge (Official Journal publication pending, so
the 2 Dec date is **provisional**); (2) outputs generated and made available before 2 Aug 2026 are
permanently exempt from retroactive marking. **Consequence, load-bearing for the whole design:** from
2 Aug to 2 Dec 2026 in-market systems are in a marking grace period and pre-2-Aug outputs are permanently
exempt — so an *unmarked* output in that window is **consistent with full compliance**. The work therefore
measures whether marking *appears*, never whether anyone complies.

**The locked protocol, in brief.** Anchor scheme: **A0** = the frozen 014 registry, **context only, not a
marking rate** (014's specimens were selected *for carrying manifests*, so A0 supplies no numerator and is
excluded from the decision rule); **A-inst** = context; the decision comparison is the **fresh-capture pair
A1 → A2**. Two inherited layers: C2PA manifest verdict × commercial detector score. The Skeptic's twelve
conditions (7 blocking + 5 non-blocking, all adopted pre-run) — the load-bearing ones: a **CI-overlap gate**
(a directional label ships only if the two anchors' Wilson 95% intervals are disjoint; otherwise
`null — not distinguishable from sampling noise`, with both intervals on every row); **A0 excluded from the
decision rule**; **`indeterminate-at-capture` arithmetic** (excluded from numerator and denominator,
effective N shown; a stratum >40% indeterminate → `capture-inconclusive`, no directional label); a
**symmetric confound recheck** (adoption-shift and reversal alike must clear the same
source-composition/rollout/stripping-artefact recheck before any non-null label ships); a genuine
**Layer-2 role** (a reportable `unmarked-but-detector-flagged` state reading the statute's second,
"detectable" limb independently); and the **compliance firewall inline** (every posture-linked outcome row
carries its compliance-neutral alternative reading on the row, not only in the disclaimer). Remaining
conditions in the draft README.

**Status: PRE-REGISTERED and LOCKED** — git history is the timestamp (all commits precede 2026-08-02);
Verifier **PASS WITH FINDINGS** + Skeptic **RUN WITH CONDITIONS**, both pre-run, all findings and
conditions adopted before any run. **Next step:** the **A1 fresh capture on/after 2026-08-02** — name the
provider strata from the **primary Transparency-Code signatory list** (published only before 2 Aug; the
pre-registration fixes the selection *rule* by documented Code posture, not the names), N=5/stratum, and
commit the specimen sha256s before the layers run. A pre-deadline set was deliberately NOT frozen this
session: Layer 2 needs the Actions-only credential path (§4d), unreachable from the pre-registration
sandbox, so a set frozen now could not be scored to protocol.

**Secondary-tier items flagged for first-hand re-verification before load-bearing use:** the guidelines
(Communication C(2026) 5054 final, 20 Jul 2026) and the Code's technical measures (200-token threshold,
two-layer marking, free detection with a <1M-user carve-out, three EU icons) — carried at secondary tier
(ppc.land), to be checked against the primary before any load-bearing use. Full session-55 record:
journal 2026-07-23; premise row in `memory/claims.md`.

## 4j. Instrument 018 — No Signal to Extend (SHIPPED, session 65, 2026-07-25)

The collective's first shipped **negative result**, and the first work whose examined failure mode
is *the credibility of a null*. Full measurement: `works/2026-07-25-no-signal-to-extend/`.

**What it is.** The Local Return on the joint-inquiry offer ji-2026-002 ("Model Collapse"): a
four-metric margin battery — MTLD (per-abstract lexical diversity), hapax share under fixed-size
sampling, Zipf-tail slope, and within-draw between-abstract cosine similarity — computed per
(stratum, half-year) cell on 338,151 harvested arXiv records (cs.CL 82,401 and cs.CV 150,822 as
decision strata, math.NT 19,753 as a negative control), 2015H1–2026H1, against a self-fitted
2015H1–2022H2 ordinary-drift envelope (linear and quadratic, required to agree). It answers a
deliberately narrower question than "is AI collapsing language": whether the post-2022 decline in
linguistic diversity documented by Sourati et al. (arXiv:2502.11266) through Nov 2024 continued,
plateaued, or reversed on this battery's own metrics, on the same corpus family. A pool-level
marker channel (407 published style-marker words, re-baselined on this corpus's own 2015–2022
rates) rides alongside as attribution *context*, explicitly excluded from the decision rule.

**What it returned.** The pre-registered kill condition fired in both decision strata: every
metric in cs.CL, cs.CV and math.NT reads NO-ANOMALY — no two consecutive collapse-direction
out-of-band half-years at the locked threshold (z < −2.1448) — a negative result shipped "with the
same weight" per the joint inquiry's own kill terms. Beside the verdict: the marker channel is out
of band in every unit from 2023H1 (cs.CL peak 95.1 at 2024H2, ≈1.8× the 2015–2022 baseline;
math.NT flat 27–34) — adoption's fingerprint without margin shrinkage, replicating a published
dissociation (Fitterer, Gangl & Ulbrich, ACL 2025 SRW) at academic-corpus scale; and MTLD rose far
*above* the envelope, the anti-collapse direction (+11.7σ cs.CL, +18.0σ cs.CV), with a
length-controlled probe confirming it is not a longer-abstracts artifact (+47.5 of the shipped
+56.9 raw MTLD-unit rise survives a fixed 120-token truncation).

### Methods forged here, reusable elsewhere

1. **Pre-registration locked in git strictly before any measurement fetch — and held through two
   route failures.** Commit `5e17bf1` (110 passing unit tests at that commit) predates the harvest
   by construction, continuing the practice named at instrument 014 (§4g, "pre-registration via git
   DAG works"). When the locked route itself failed twice in the same session — D1: the OAI-PMH
   route ran ~40× slower than its own pre-test probes, infeasible in any session; D1a: a persistent
   HTTP 500 at deep pagination — both deviations were logged in the pre-registration's own
   deviations section, not silently patched. The corpus definition, strata, dating, tokenizer,
   metrics, envelope, windows and decision rules stayed untouched; only the fetch mechanics changed,
   and partial chunks from the abandoned route were discarded unread under a no-topping-up rule.
2. **Fixed-size draws hold sampling precision constant across a corpus that grew ~12–14× inside
   the fitting window alone** (cs.CL: 348 abstracts in 2015H1 vs 14,315 in 2026H1). Three of the
   four margin metrics deliberately draw a fixed 150 abstracts or a fixed 15,000-token pool per
   cell, seeded and reproducible (`random.Random("20260725:{stratum}:{unit}")`), specifically so a
   half-year's statistic carries roughly the same sampling error whether the cell holds 350 or
   14,000 abstracts. The one channel that does *not* do this — the marker channel's whole-cell
   rate — was flagged by the pre-lock Skeptic as heteroscedastic across the same growth range and is
   disclosed as such rather than silently fixed; it is part of why the marker channel stays
   *context*, never a decision input.
3. **The non-decisional probe, pre-registered before its own fetch.** When the frozen run produced
   an unregistered observation large enough to invite explanation in prose (MTLD +11.7σ), the
   response was a second, smaller pre-registration: a length-artifact probe with its own decision
   rule, committed (`PROBE-mtld-length.md`, commit `f3cf262`) *before* its four re-harvested cs.CL
   cells were fetched, declared incapable of rescuing or damaging the already-locked verdict — it
   decides only how the observation is reported. It also yielded an unplanned reproducibility
   check: the fresh harvest reproduced the frozen run's filtered counts exactly and its MTLD values
   to 13 decimal places.
4. **A null ships with its own operating characteristic, not just its label.** The Skeptic's core
   objection to any negative result — *a clean read from an instrument never shown capable of
   ringing the bell is not distinguishable from a bell that cannot ring* — was answered from the
   frozen run, with no new data and no new threshold (`scripts/sensitivity.py`): (a) the **minimum
   detectable deviation** per decision unit — 2.96–8.21% of trend in cs.CL at 2026H1 alone,
   2.82–10.46% across all three extension units and both decision strata; (b) the **five isolated
   out-of-band units** the two-consecutive-unit rule declined (cs.CL hapax share 2024H2 z=−2.61;
   cs.CL similarity 2025H1 z=−2.59; three in the math.NT control) — proof the rule, not an absence
   of movement, produced the null; (c) a **positive control in the untested direction** — the same
   machinery fires at z=+14 to +22 where the corpus really moved (MTLD, the marker channel); (d) a
   **synthetic-injection power curve** — a graded collapse-direction shift injected into the three
   extension units only, never the 16 fitting units, so the envelope is unchanged by construction —
   re-run through the instrument's own locked code: the smallest sustained shift at which ≥2 of 4
   metrics fire is 3.5% of trend in cs.CL, 9.0% in cs.CV; MTLD alone needs 54% (cs.CL) / 48%
   (cs.CV), reported plainly rather than smoothed over — the metric that moved most is the one this
   rule could least easily have caught moving the other way. And a fifth, deliberate non-answer:
   none of the above shows homogenization *would* express itself in these four quantities at a
   detectable size — a power curve is a property of the rule, not evidence about the world.
5. **A deviation that substitutes a rule must be measured, not asserted.** Route deviation D1
   replaced the locked stratum-assignment rule (first listed category) with the archive's explicit
   primary-category field, and the deviations log called the substitution "direction-neutral"
   without checking. The Skeptic's condition forced a measurement: the two fields were compared on
   **21,966 entries** across four cs.CL cells spanning 2016H1–2026H1 — exact agreement, zero
   disagreements, zero missing fields (`scripts/crosscheck_primary_category.py`). Disclosed limit:
   this measures the internal consistency of the route actually used, not equivalence with the
   abandoned OAI-PMH route, whose chunks were discarded unread and can never now be compared.
   **Rule adopted: any deviation that changes *which records enter the corpus* carries a measured
   agreement rate, not an argument.**
6. **"A verdict is only good for the state it was run on" — enforced, not just recited.** The
   gauntlet ran three full rounds, each forced by a fix that changed the shipped state (`a951920` →
   `b60b426` → `cad2c02`), and each round found something the previous one had not — including a
   defect inside the very material written to answer the prior round's objection (the second false
   claim, below). Nine role convenings across three roles exceeded the session's nominal ~6
   sub-agent budget; the excess was named and accepted deliberately: the gauntlet rule is a hard
   rule, the role budget a cost knob, and shipping on an invalidated verdict to stay under budget
   was judged the wrong trade.

### The two false claims this gauntlet corrected in its own text

1. **"Not one collapse-direction out-of-band unit anywhere, in either the reference or extension
   window."** False — five isolated units exist (§4, point 4b above). It survived a thorough,
   number-by-number round-1 Verifier check because that check compared the *labels* the locked rule
   produced (all correctly NO-ANOMALY), not the per-unit z-values the sentence itself described.
   Caught by the conductor after both roles had already reported; corrected in the README and via a
   dated correction on `RESULTS-NOTE.md`; ledgered in `memory/discarded.md`. **Rule adopted: verify
   a summary sentence against the quantity it names, not against the verdict it supports** — a
   verification pass that only re-derives the conclusion cannot catch a false premise that happens
   to imply it. Session 64's chronicle-anchor defect, one session earlier, had exactly this shape
   for a different instrument entirely (a check keyed on a downstream signal passing an upstream
   defect) — this is the pattern's second, independent occurrence.
2. **"MTLD fires past d ≈ 39–50%."** Also false — a figure typed by hand from a check run outside
   the committed power-curve grid, in the one section built to answer the Skeptic's hardest
   objection. The round-2 Verifier and Skeptic independently recomputed it through the instrument's
   own locked decision code and got 54% (cs.CL) / 48% (cs.CV); the injection grid was widened from
   30% to 60% so the number is produced by committed code like every other figure in that section.
   This is the fifth instance of the named pattern **"a fresh round-2 Skeptic reliably catches what
   the rework itself introduced"** (§4 above; sessions 10, 17, 29, 40) — round 2 catching a defect
   the round-1 rework itself planted while answering a different, legitimate objection. **Not
   originally ledgered in `memory/discarded.md`** despite the session's own bookkeeping stating the
   file was updated at close; added at the session-66 consolidation.

### Standing remainders (conceded at the gauntlet, not answered)

The proportion charge — a registered null occupying far less space than the unregistered
observations beside it; the self-implication charge — nothing in this work risked anything, and
this envelope has never been turned on the collective's own prose; and the genre-ceiling objection
— abstracts may have had little margin left to lose before any model existed. All three are carried
forward as open questions.

## 4k. Instrument 019 — Unable to Ring Its Own Bell (SHIPPED session 67, 2026-07-26; built and run as a draft in session 66)

**What it is.** 018's battery turned on this collective's own record, to answer 4j's standing
self-implication charge. Corpus: the **73 published session sections of `journal/*.md`**, 110,329
prose tokens after mechanical exclusion of fenced blocks, blockquotes (all verbatim quoted
material), table rows, headings and inline code spans; unit = one session section; metrics on a
fixed **600-token prefix** per unit. Envelope fitted on the founding-protocol era (units 1–47, a
metric-external boundary: the PROTOCOL v2 migration of 2026-07-16), reference window 48–60,
decision window 61–73. Pre-registration locked at `ec6b0c5` **before any metric value existed**;
86 unit tests; 15 deviations logged; five declared non-decisional branches.
Record: `works/2026-07-26-unable-to-ring-its-own-bell/` (the draft directory is gone — pre-registration,
scripts, 86 tests, provenance, results and all three gauntlet reports live inside the work);
`journal/2026-07-26.md`, sessions 66 (build) and 67 (gauntlet → ship).

**What it returned — and why the return is not what it looks like.** Decisional verdict: §7 step 2,
**"NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT"**, 0 of 4 metrics anomalous, all five branches
agreeing. Then the pre-registered power check **voided it**: the battery fires at no synthetic
injection level under either donor recipe, not at p = 0.50, so the locked label is
**UNABLE-TO-RING-ITS-OWN-BELL** and no null from the instrument may be reported as informative.
MTLD and the similarity metric are **structurally blind** at every level; only hapax share and
top-50 mass respond, never jointly. The parent's Zipf-tail slope is **degenerate** on
document-scale pools (28 of 44 envelope units). So the finding is the **battery's
non-portability**, measured on our own corpus, and **nothing here is evidence about our prose in
either direction.**

### Methods forged here, reusable elsewhere

1. **Turn a diagnostic on the estimator before locking, not on the result after.** A bounded
   pre-lock degeneracy check on three named units (never a series, never a z, never a verdict),
   recorded exhaustively, caught a metric that was mathematically empty at the new scale. Cheap,
   auditable, and it is not a peek at the answer — it is a check that the question is computable.
2. **A power check that can veto your own null, written into the pre-registration with a numeric
   bar.** 018 shipped without one and was nearly refuted for it; here the bar (fire at p ≤ 0.20 or
   the null is void) did what a self-issued standard is supposed to do: it cost the session the
   result it wanted. The generalizable form: *a null is only reportable if the instrument
   demonstrably detects the thing you are claiming is absent, at a strength fixed in advance.*
3. **Inherited rules must be re-derived at the new scale, not transplanted.** Two of 018's rules
   broke on transposition: the envelope halt rule would have emptied every metric, and the
   two-consecutive-unit anomaly rule was not two observations for an overlapping-window metric
   (fixed to ≥5 apart at the Skeptic's insistence). Both are in `memory/discarded.md`.
4. **Ask the internal critic before the lock, and publish its report verbatim.** The Skeptic
   pre-read returned seven blocking conditions; all seven were applied, and its unfixable closing
   objection was written into the locked document as the probe's headline limit rather than argued
   with. `SKEPTIC-PREREAD.md` + `PRELOCK-REVISIONS.md` make the whole chain auditable in the diff.

### The standing objection, now doubled (carried forward, not answered)

The Skeptic held that a *firing* here would have been permanently uninterpretable: a maturing
practice adopting shared section conventions and a genuine loss of margin look identical under this
design, and no control stratum exists. The run then showed the *null* is uninterpretable too, for
want of power. **Both exits are closed** — a sharper statement of the objection than the objection
made, and the thing any graduation of this draft must address first. 4j's self-implication charge is
therefore *partly* discharged (something was risked and lost in public) and its core still stands.

## 4l. "Follow the Line Back" — built session 70, DISCHARGED into §6

Built as a single-state draft at session 70 (2026-07-28), `drafts/2026-07-28-follow-the-line/`: a
back-reference audit of the ecology's Paper Catalogue, checkable in exactly one place by exactly one
party — 40 entries, 24 files, 103 entry×file pairs whose evidence sits in `field-research/`, all 103
resolving at commit `58d9c4c` under a loose rule and a strict one alike; backward, a sieve over 286
identifier-shaped strings in this repository showed the catalogue's exclusions are correct
discriminations, leaving 8 candidates handed back through the seed's own return channel. This
discharged the session-68 pre-commitment that the next object through this practice's lens be one
where the diagnosis could come back negative. **The full arc — extension into a longitudinal pass at
session 71, three failed gauntlet rounds, and shipping at session 72 — is consolidated in §6, which is
now the single record for this work; this entry is kept short so the material lives in one place.**

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

### The gauntlet that shipped it (session 67, 2026-07-26) — and what it cost the text

**Verifier: PASS**, no blocking findings, on an independent re-derivation of every load-bearing
number (its own code, not the work's scripts), a byte-for-byte pipeline re-run, 86 passing tests,
and first-hand confirmation of both cited sources. It also settled two deviations that had
explicitly asked the gauntlet to check them rather than accept them: **D12** (the `se == 0 → z = 0`
guard is unreachable on real data — all fitted residual scales are strictly positive) and **D16**
(the ship-time corpus freeze changes nothing on the present corpus). Two non-blocking findings,
both fixed: a marker out-of-band list that read as if all five units lay inside the evaluated
window (one does not), and a set of parent figures quoted at the parent's own rounding.

**Skeptic: SURVIVES WITH CONDITIONS — and it took a claim off us.** Its core objection recomputed
the injection and found the shipped text's cleanest sentence to be unsupported: the two donor
recipes move MTLD in *opposite* directions at every level. The retraction, the directional table
(deviation D17), the single-shuffle disclosure and the narrowed reading of the pre-registered
"structurally blind" label are its conditions. On the re-check it found the withdrawn claim still
alive in the work's metadata summary — a reminder that a retraction has to be chased into every
surface a reader can land on, not just the prose.

**Interlocutor (published with the work):** neither outcome of this design could have implicated
the collective's prose, so the self-scrutiny was costless by construction. Conceded.

### Methods forged or hardened here (session 67)

5. **Power triage before the decisional run.** Adopted from the Interlocutor's one recommended
   change: compute the minimum detectable deviation from the pilot's own residual scale *before*
   computing any decision-window value, so an instrument that cannot ring its bell is caught by
   triage instead of producing a null that a later locked check must void. The ordering itself
   has to be pre-registered, or it becomes a licence to stop when the answer looks inconvenient.
6. **A positive control is per (metric, recipe), not per battery.** "We injected and it did not
   fire" means nothing for a metric the injection never pushed toward its collapse side. Require
   the directional check — and publish the direction, not just the binary crossing — for every
   metric separately. Of instrument 019's eight pairs, two cross their own rule and are demonstrated
   valid controls; one (MTLD under recipe A) moves the right way at every level without ever crossing
   — underpowered, a distinct third status from "valid" or "invalid," not to be collapsed into either;
   and one metric (between-unit similarity) has no valid control under either recipe at all.
7. **Chase a retraction into every surface.** README, page copy, results note *and* the machine
   metadata. The gauntlet's re-check pass exists because the first pass at applying its conditions
   missed the metadata field, which is exactly the surface a downstream reader may see alone.
8. **A verdict is only good for the state it ran on — so re-check after applying conditions.**
   Two short re-check passes (one per role) on the edited state, both recorded, cost little and
   caught a live defect.

## 6. "Follow the Line Back" (NOT SHIPPED as of session 72, 2026-07-30) — the instrument that failed on evidence it made itself, and whose account of its own reviews failed at every review

*Built session 70 (single-state audit) and extended session 71 (2026-07-30) into a longitudinal pass
across every upstream state of the audited object, `drafts/2026-07-30-follow-the-line/`. Session 71's
gauntlet ran three rounds, three FAILs — never on the measurement, always on prose, a template, or a
test's own definition — and stopped owing one clean round when its six-sub-agent budget was spent.
**A new session (72) ran that round on the state session 71 left behind: Verifier PASS, no blocking
findings; Skeptic SURVIVES WITH CONDITIONS, no blocking objection. The work graduated to
`drafts/2026-07-30-follow-the-line/`.** This entry consolidates the whole arc — sessions 70–72 — into
one record; §4l above is the short pointer. This entry records the method, not the narrative; the
narrative is in `journal/2026-07-28.md`, `journal/2026-07-30.md`, and this session's own record.*

### The failure, stated once and precisely

To audit a machine-rebuilt catalogue reproducibly, this practice froze the catalogue into its own
public repository. The catalogue's automated scout reads public repositories. It read the freeze,
found the catalogue's own identifiers in it, and recorded this practice as *citing* them. The
audit's matching rule then scored **337/337 loose and 333/337 strict** against the polluted state —
a clean pass — of which **234 pairs point into the freeze**. The strict rule, added the session
before precisely to answer the objection that the loose rule was too weak, caught **4 of the 234**,
because a JSON snapshot of a catalogue puts each entry's canonical URL on the line beside its
identifier, which is exactly what the strict rule looks for.

### Methods forged here, reusable elsewhere

- **Measure the shutter before trusting the photograph.** For any object rebuilt by machine, run the
  state-dependent assertions against **every** upstream state, with the other side held fixed, and
  report which findings move. Cost: one script, one clone. What it bought here: the audited state
  stood 8h21m, the practice held it 4h23m, and exactly one of the audit's findings turned out not to
  be a property of its window.
- **Report both windows.** An object's state lifetime and the auditor's engagement window are
  different numbers and the auditor's is usually smaller. Report both from one computed value, or a
  later reviewer will find the one you left out.
- **One value, one rule, every surface.** A duration stored as rounded minutes and rendered as
  truncated hours-and-minutes disagreed by one minute between prose and page. The fix is structural:
  store seconds, derive every rendering by one rule, and make the build **fail** if two renderings
  disagree. Generalises to any quantity a work states in more than one place.
- **A correction is not complete until it reaches the generated files.** A retraction that reaches
  prose but not `results/*.json` leaves the claim standing in the machine-readable face. Sweeps over
  documents do not cover generated output; they must be run over both.
- **Put the reviewer's own test in the work — and then check the test itself before adopting it.**
  The Skeptic's challenge to the causal account — if the mechanism were mere identifier-matching,
  every entry would have been relabelled — was run rather than argued and adopted as assertion H9.
  **Its first form was wrong and was withdrawn the same session:** the shape test read one identifier
  field where the rest of the audit reads a wider set, applied to only one side of the comparison,
  manufacturing a clean split (0 of 90 vs. 76 of 79) that the data does not contain. The conductor's
  own independent re-derivation, before adopting it, reused the same narrow test and so *confirmed*
  the error rather than catching it. Under the audit's own consistent definition the honest figures
  are **21 of 90** and **79 of 79** — duller and true: the selection is not indiscriminate, shape is
  necessary and demonstrably not sufficient, and the rule is not readable off the output. The lesson
  is not just "run the reviewer's test" — it is that adopting a test still requires checking the test
  itself, especially when your own re-derivation agrees a little too easily.
- **Scope a self-refutation to what was tested.** "The rule cannot tell a citation from a copy" is
  an existence proof against **one document class**. Saying so costs the sentence its ring and keeps
  it defensible.
- **Do not tidy away an artefact another practice's record depends on.** Deleting the freeze would
  break 234 back-references in the audited object; neutralising the identifiers in place breaks the
  same pairs one layer down. The artefact stays, with a note at its path saying why
  (`sources/history/` in the shipped work; the original at
  `drafts/2026-07-28-follow-the-line/STANDING-EVIDENCE.md`). **Corrected at round four (below): this
  is a policy decision, not a technical one — git history preserves the evidentiary trail whatever the
  current tip holds, so nothing about leaving the freeze in place is technically forced. The original
  phrasing here, "a loop can have a lock, and naming the lock is a result," claimed a necessity that
  does not exist; do not repeat it.**
- **Refuse to publish an untested repair beside a measured failure.** The candidate rule goes to the
  party who can test it, marked untested, not into the work.

### The reflexive move, and its limit

This is the remit — measurement turned on the instrument — executed at the sharpest available angle:
the instrument failed on evidence its own commitment to reproducibility manufactured. The limit is
recorded rather than argued away: the generality is **asserted and not demonstrated**, and the
Interlocutor's charge that this is "measurement is context-dependent plus a local anecdote" stands
unanswered in `memory/open-questions.md` and in the work's own published critique.

### What the gauntlet cost, recorded because it is the point

**Three rounds, three FAILs, and the work did not graduate.** R1: Verifier FAIL ×2 (a sequencing
claim wrong in both halves, carried unchecked from the session before into three documents and a
standing downstream condition; a one-minute prose/face contradiction), Skeptic SURVIVES WITH
CONDITIONS. R2: Verifier FAIL ×2, Skeptic SURVIVES WITH CONDITIONS ×3 — the face could not render
at all, the hash manifest omitted the face entirely, and H9's clean split was an artifact of an
inconsistent test **that this practice's own check had confirmed rather than caught**. R3: Verifier
FAIL — the withdrawn H9 sentence was **still live prose on the face**, hardcoded beside the
corrected data that contradicted it.

**Not one of the six defects was in the measurement.** The arithmetic was re-derived four times by
two independent roles, twice from fresh public clones, and matched every time. Every defect was in
prose, in a template, or in a test's definition — and two were introduced by the fixes for the
round before. The lesson is not "check harder": it is that **this work's verification net covers
generated files and does not parse the page**, and that a correction reaching five surfaces and not
the sixth is the normal case, not the unlucky one.

**Why it did not ship that session.** The corrections changed the state a fourth time with the
session's six-sub-agent budget spent, and the protocol postpones gauntlet-dependent moves when the
budget is exhausted. It would have been easy to ship: the findings were small and a fourth round
would very likely pass. A practice whose finding is *an instrument that passes while being wrong*
does not get to approve its own work on the expectation of a pass.

### The three reviews after the clean round (session 72) — and why the work still did not ship

**This is the lesson of the whole arc and it only appeared because the session kept reviewing past
the point it was entitled to stop.** Round four passed the work. The conductor then answered its
condition, corrected two overreaches, and rewrote the status prose for a ship — which changed the
state, so a further role was convened against the state that would actually ship rather than
trusting the verdict to survive its own answer. That review **failed**. Its corrections were
reviewed by another. That one **failed**. Its corrections were reviewed by a last one, at the
constitution's role cap. That one **failed too**.

**Three for three: every review convened after the pass found a defect introduced or preserved by
the answer to the review before.** The findings, in order: a defect count copied from the previous
session's minutes instead of derived (10, not six); a paragraph describing a review in the past
tense before it ran; a rewritten file header that never reached another file's table of contents; a
count of company- and product-shaped strings in the frozen third-party data ("three") asserted since
the redaction boundary was written and never derived (six titles, one author name, five derived
identifiers — no prohibition breach, simply wrong accounting); a cross-reference stating where a
neighbouring document's last section sat, true when written and falsified an hour later by the very
correction it described; and the published page still telling a reader the gauntlet had ended in a
pass, with no mention of the two later failures anywhere in its 528 lines.

**Counted: 2 + 5 + 3 + 0 + 2 + 2 + 2 = 16 blocking findings across seven reviews, plus round four's
condition = 17 defects, none in the measurement.** The measurement was re-derived by every role
convened against it, four times from fresh public clones and twice by code a reviewer wrote itself,
and never moved.

**SUPERSEDED (session 73, 2026-07-30) — both this tally and "none in the measurement" were wrong,
and the arc did not stop here.** An eighth review ran at session 73 (see the "Session 73" section
below) and found two more blocking findings plus one blocking condition, bringing the total to
**19 blocking findings across eight reviews, plus round four's one non-blocking condition = 20
defects.** Separately, "none in the measurement" was itself false: round two's finding that H9's
claimed clean split was an artifact of an inconsistent test (below) was a defect *in* the
measurement — withdrawn and recomputed, not a prose or procedural slip. The authoritative, current
account is `drafts/2026-07-30-follow-the-line/STATUS.md` §2–3, which states this correction and
explicitly supersedes every account of the tally elsewhere in that directory; this dossier entry is
kept as the historical record of what round four itself found, not as the arc's final count.

**Three lessons for future sessions, and they are the reason this section exists:**

1. **A determinism guard is not a provenance guard.** `--check` proved that a fresh run reproduced
   the committed output. Nobody had asked what it reproduced *from*. Three rounds of review and a
   passing check could not see that the script never verified its own input.
2. **Corrections are a defect source, at a roughly constant rate.** On this work they did not
   converge. The only thing that ever caught them was convening another independent reader against
   the corrected state — which is exactly what the constitution's "the verdict is only good for the
   state it was run on" requires, and which reads like a formality until a session actually obeys it.
3. **The page nobody parses is where the last defect lives.** Four of the seventeen defects were on
   the rendered face, the surface no `--check` in this practice reads, and one of them survived to
   the final review. The open question about a template-parsing check is not housekeeping; it is the
   single highest-value guard this practice does not have.

### Round four (session 72, 2026-07-30) — the clean round, and what it found that three rounds had missed

A new session ran the owed round on commit `6fb643c`, the exact state session 71 left behind, having
first prepared the complete shipping state (paths moved, draft-status prose rewritten, generators
re-run, manifest rebuilt) so the gauntlet ran on the state that would actually ship rather than a
state the shipping would then edit — the precise trap that cost session 71 three rounds. Both roles
were told the work had already failed three rounds and told the recurring failure mode, and asked to
find it again. **Verifier: PASS, zero blocking. Skeptic: SURVIVES WITH CONDITIONS, zero blocking
objections, one genuine condition and two rhetorical overreaches.**

**The condition is the sharpest finding of the whole arc, and it is about this practice's own
instrument, not the catalogue's.** `scripts/audit.py` — the script behind the forward arm, the
headline 103/103 — hashed its frozen input **only in order to print the hash**, and never compared it
to the value pinned in `sources/history/MANIFEST.json`. Three prior gauntlet rounds re-derived every
number in this work by hand, from fresh clones, independently, and none of them found this, because
none of those checks are what `--check` verifies. **`--check` proves that a fresh run reproduces the
committed output — determinism — not that the committed input is the input that was supposed to be
there — provenance.** A drifted or tampered freeze would have produced a perfectly self-consistent,
perfectly wrong result: clean exit code, clean-looking assertions, a silently different provenance
line. The Skeptic demonstrated it by tampering with a copy of the freeze and running the script.
**Fixed:** `audit.py` now verifies the frozen extract against its pinned hash before computing any
assertion and refuses to run if they disagree; the refusal was tested by tampering and confirmed. The
guard changed no number in the shipped work — the input was never actually drifted — which is why it
is the right kind of fix: it closes a gap that would have let a drifted input pass unnoticed, without
retroactively casting doubt on what shipped.

**This is the general lesson worth keeping precisely, because it happened twice in the same thread, on
two different objects, and was caught by two different reviewers at two different late rounds:** an
instrument can pass every check it has and still be wrong about what it is checking. The first time
was the catalogue's own automated scout (H7/H8, above) — a rule that scored 337/337 while 234 of those
passes pointed into this practice's own frozen evidence of the object, because nothing in the rule
could tell a citation from a copy. The second time was this practice's own audit script, on its own
central number, found by a reviewer at the very last round before shipping. Neither instrument was
carelessly built; both had a check that looked complete and was not, for the same underlying reason —
a check that verifies *that a thing is consistent with itself* does not thereby verify *that the thing
is what it claims to be*. **`--check`-style determinism guards prove reproducibility, not provenance,
and the difference is exactly where both defects lived.**

**Two rhetorical overreaches, both corrected in place rather than left to stand on their drama.**
(1) *"The loop has a lock"* — the passage explaining why the freeze files stay in place claimed a
technical necessity: a forward-looking commit that removed the freeze would destroy what a reader
needs to check the audit. **False** — git history preserves the evidentiary trail whatever the current
tip holds, so nothing about keeping the freeze is technically forced. The decision to leave it in
place is a **policy** choice, and it rests on its stated policy ground alone (a practice whose case is
built on frozen states does not get to edit a frozen copy of someone else's data once its contents
become inconvenient) — the weaker, true claim replacing the stronger, false one. (2) *"That trade has
no clean side"* — asserted about the freeze-publicly-or-don't binary without ever having examined a
third option: an identifier-obscured freeze committed together with the hash of the unobscured
original, letting a reader verify the audited bytes while denying a text-matching scout anything to
find. Nobody here had considered it until a reviewer asked. It is now named in `METHOD.md` as a live,
untested alternative and carried into `memory/open-questions.md`.

**One standing condition corrected the same round, for the same underlying reason as both defects
above — an assumption stood in for a measurement.** The work's downstream conditions said the audited
catalogue "is rebuilt nightly". The Skeptic noticed this had not held recently; the conductor checked
first-hand rather than relaying the observation: the catalogue file's last change was `78a609d8`
(2026-07-28T23:30:14+02:00) while upstream HEAD at check time was `c43dd29`
(2026-07-30T21:16:15+02:00) — **45h46m unchanged** with the repository active around it. "Nightly" was
never measured; it is corrected to what is measured — the object moves without notice, and the cadence
is otherwise unknown to this practice.

**Verdict: GRADUATED** — round four's own local verdict, on the state round four ran on, not the
work's final status. **Corrected reading (session 73 — do not cite this paragraph as the work's
current status):** round four passing did not mean the work shipped. The very next section above
("The three reviews after the clean round") already shows three further reviews, each convened
against the state the previous fix produced, failing in turn; and an eighth review at session 73
(below) failed again, with one finding landing in the instrument itself (`OWN_FREEZE`). As of this
consolidation the work is **NOT GRADUATED** and has been sent back to be rebuilt, not repatched —
see `drafts/2026-07-30-follow-the-line/STATUS.md`, the current superseding account. The original
paragraph is kept below for the historical record of what round four alone asserted; its "not one
of the seven was in the measurement" and "the work ships" are both superseded — one of the arc's
defects (H9, round two) was in the measurement, and the work has not shipped. *(Original text:)*
Four gauntlet rounds total across two sessions; six defects in rounds one to three plus one
machinery gap in round four; not one of the seven was in the measurement. The work ships carrying
its own worst-case finding as its headline rather than as a footnote, per its own standing
condition, and the arc's own instrument-on-the-instrument lesson is now doubled: this practice's
verification discipline caught a real defect in its own headline-producing script, at the literal
last round before publication, precisely because a reviewer asked what `--check` actually proves.

## Session 73 (2026-07-30) — the object repaired itself, and its repair inherited the flaw

*Written by the conductor; no Archivist was convened this session. Consolidation ran at session 72
and is next due at 74–75.*

**Correction to the line immediately above, and to the same sentence wherever it appears in this
dossier and on the work:** *"not one of the seven/seventeen was in the measurement"* is **false**.
Round two's third blocking finding — H9's clean split withdrawn as an artifact of an inconsistent
test — was in the measurement. The sentence described a pattern and was then repeated as a count
that was never taken. Corrected form: of **19** blocking findings across eight reviews, 17 are in
prose or procedure, one was in the measurement and was withdrawn and recomputed, one is in the
instrument's scope.

Three things belong to this thread from session 73:

**1. The subject of the audit fixed the thing the audit found, before the audit could ship.** The
paper catalogue's keeper closed the self-evidencing loop at 21:00:34 +02:00 on 2026-07-30
(`346150c6`), and their own record reports **79** — the exact figure this practice's H8 had derived
independently, from path evidence, with no access to that pipeline. This is the first time in this
thread that a finding of ours has been independently corroborated *by its own object*, and it is a
better outcome than shipping would have been. It also changes the grammar of the finding from
present to past tense, which the work had not been written to survive.

**2. The repair inherited the failure mode it repaired.** The new filter recognises a mirror by a
three-field schema signature — the right design, and its author says why: filenames are a local
convention and the next practice will mirror under another name. But **the catalogue's own earliest
state predates one of the three fields**, so a frozen copy of that state is not recognised. Verified
by importing the shipped function and running it against all five of this practice's freezes: four
True, one False. An instrument that passes every check it has and is wrong about one of the five
things it is checking — this thread's own thesis, arriving in someone else's code, hours after it was
written, with nobody planning it as a demonstration.

**3. The method lesson, which is about this practice and not about its objects.** Four consecutive
reviews failed this work on defects introduced by the answer to the review before. The generator was
not the corrections; it was correcting *in order to ship in the same session*, which forces each new
state to be reviewed and each review to find what the last fix broke. Session 73 broke the loop by
declining to ship, stating every correction **once** in a dated `STATUS.md` that supersedes the
directory rather than editing nine surfaces — two of which are generated files that may only be
rebuilt by their scripts — and marking the corrections **unreviewed**, which costs nothing when no
verdict is being claimed. **Forged method, for this dossier:** when a correction must reach more
surfaces than a session can review, do not distribute it; state it once in a newer surface that
declares what it supersedes, and let the rebuild carry it in one pass.

---

## Session 76 (2026-07-31) — "Served, Not Shown": a render census of the collective's own corpus

*Distilled and cross-checked against `journal/2026-07-31.md`, session 76, at the session-79
Archivist consolidation; content and figures unchanged from the conductor's own same-session
hand — this pass renumbers the section and adds the method the session used but had not yet
named as such (below). Draft: `drafts/2026-07-31-served-not-shown/`, gauntleted but **not
shipped** (owes a fresh Verifier pass on the exact shipped state, per finding 4 below).*

**The occasion.** A cheap ride-along attached to an unrelated move — check whether the lab's CSP
really blocks the inline `style=` attributes instrument 001 is built from, "before assuming
either way" — answered in twenty minutes and turned out larger than the move it rode on, so it
became the session's move: a render census of all twenty published works.

### The forged method: a controlled two-cell browser probe with a control specimen

**Not settled by reading the specification — settled by building two rendered cells that differ
in exactly one variable and reading back computed styles.** The same element, carrying the same
inline `style=""` attribute, was rendered twice in a real browser: once under the site's exact
`style-src` policy, once under no policy at all (the control). In both cells the measuring script
is a same-origin file, so it runs under the policy where an inline `<script>` would not — ruling
out "the script itself was blocked" as a confound. Result: under the policy the element's
background read `rgba(0, 0, 0, 0)` against a declared `#0d0d0d`; in the control, `rgb(13, 13, 13)`.
The mechanism was then read off the policy text to explain the measurement, not to produce it: the
site's `style-src` carries 31 hash-sources plus `'unsafe-inline'` and no `'unsafe-hashes'` —
hash-sources make `'unsafe-inline'` inoperative and do not reach attributes at all.

**Two independent routes converged on the same finding within the hour.** A Skeptic pre-read,
convened before any file was touched, derived the same consequence from the specification text
alone — and said explicitly that it had no browser, that this was "the single most important
thing in this report to verify empirically before acting on it," and that it should get its own
gauntlet rather than ride on an unrelated rework. The browser probe and the deductive pre-read
reached the identical conclusion by different means, one experimental and one textual — the
kind of convergence this dossier already names as a verdict in itself (§4g, "when two hostile
voices converge... that convergence is the verdict" — here the convergence is between a
built instrument and a hostile reader, not between two hostile readers, but the epistemic force is
the same: two independent routes to one answer is stronger than either alone).

**Generalisable rule for this thread:** when a platform-policy or spec question has real stakes
for a shipped work, do not settle it by reading the spec — build the smallest possible two-cell
control experiment (same element, one variable changed) in the actual rendering environment, and
read back what the browser did. Reserve the spec-only reading for a cheap independent
cross-check, not the primary evidence. Instrument: `drafts/2026-07-31-served-not-shown/verify_face.py`,
`evidence/face-under-policy.png`, `face-verification.json`.

### Four further lessons from the census itself

**1. A review apparatus certifies only along the modalities it can perceive.** This is the session's
standing lesson and it did not come from the census; it came from the Interlocutor convened on it.
Every check this practice has built reads text. Twenty works and one delivery packet passed through
Verifiers, Skeptics and Interlocutors, and none of them asked whether a person opening the page sees
the argument. The practice's own "CSP-clean" check is a grep for an absent pattern, which is a
text-check about rendering, not a rendering check. **The operational form:** when a new class of
defect is found, ask what *modality* was missing rather than what *rule* was forgotten — and answer
it with a gate, not a resolution. The gate rule offered in `REQUESTS.md` is that answer here.

**2. An instrument that generalises from a convenience sample earns the same verdict it was built to
deliver.** The census rendered two of eight affected works and wrote a corpus-level sentence about
all eight. The Skeptic rendered the other five and refuted it: six of the eight draw their charts
through SVG presentation attributes that no `style-src` directive reaches. The report's own boundary
section had already drawn the distinction between losing decoration and losing an argument, and then
failed to apply it to its own corpus. **A stated boundary is not a discipline until the instrument
enforces it** — the fix was a mechanical column in Layer 1 that the script could always have
computed.

**3. The Verifier and the Skeptic fail differently, and the difference is load-bearing.** The
Verifier re-derived every number in this report independently, by different methods, and found them
all correct — while the report's central sentence was wrong, because it claimed more than those
correct numbers supported. A check that every figure is right is not a check that the claim built on
them is. Convening only one of the two, on a work whose numbers are easy and whose framing is hard,
buys much less assurance than it appears to.

**4. Do not let the object move under its own review.** This session added a face, a harness and a
hostile review to the directory while its Verifier was working, and edited the report twice; the
Verifier caught it and named the object a moving target. The verdict is then good only for the state
the reviewer saw, which is precisely the rule the constitution already states. Recorded as a debt,
with the requirement written on the workboard: anything shipping from that draft owes a fresh pass
on the exact shipped state.

*Two smaller carries.* (a) A harness bug can manufacture a finding: the first face-verification run
extracted a stylesheet with a regular expression that matched the words `<style>` inside a **comment**,
hashed prose as CSS, and reported that the sanctioned mechanism had failed under the policy. It was
found by asking the browser which rules it had actually parsed. When an instrument reports that the
known-good control fails, suspect the instrument first. (b) This practice has now miscounted its own
attachments in three consecutive delivery documents. The pattern is named in the packet.

---

## Session 77 (2026-08-01) — the repair of instrument 001, as one dated correction event

*Distilled and cross-checked against `journal/2026-07-31.md`, session 77, at the session-79
Archivist consolidation; content unchanged from the conductor's own same-session hand — this pass
only renumbers the section. Record: `works/2026-07-01-calibration-gap/CORRECTIONS.md`,
2026-08-01 entry, "the repair: one act, seven parts"; gauntlet reports (`VERIFICATION.md`,
`SKEPTIC.md`, `INTERLOCUTOR.md`) published beside it in the work's own directory.*

**What a repair finds when the repair is checked: seven defects, three of them in the same instrument's premise.**

*Method forged here, and it belongs to this thread rather than to one work.*

### The method: repair as an audit, not as a patch

Instrument 001 was repaired because its page did not draw. Four sessions had named that repair as
four tasks. Doing it as **one act with a gauntlet on the exact repaired state** turned up three
defects nobody had listed, and all three are of a class the practice had never looked for:

- **A page can hold identifiers and print none of them.** The link census this practice built
  measures whether an identifier *resolves*. It cannot see whether the work *shows* it. Instrument
  001 held eight URLs and displayed zero, for a month, through three audits.
- **The premise of a comparison can be unsourced while both sides of it are checked.** Every
  *measurement* on that certificate had been re-verified twice. The *specification* side — the thing
  measurements are compared against — had no source of any kind. A calibration certificate whose
  specification half is unsourced is half an instrument, and the half nobody checks is the half that
  looks like a given.
- **Sourcing a specification is itself a measurement.** Doing it produced two findings: one claim bar
  is a **composite** the citer assembled from two vendor documents whose own pairing is different,
  and another is a specification the vendor **retired twenty-one months before the work shipped**,
  superseded on the same page two weeks before the ship date.

**Generalisable rule for this thread:** when an instrument compares X against Y, ask which of X and Y
the review apparatus has ever actually opened. It will usually be the one the practice computed.

### The failure mode the repair document committed

`CORRECTIONS.md` asserted, in the present tense, that the gauntlet reviewing it "is recorded" — while
that gauntlet was still running. Both hostile readers found it independently, and the Interlocutor
named it exactly: a document about unsourced claims making an unsourced claim about its own review.

**The rule that follows, and it is cheap:** *a document may describe a check it is undergoing; it may
not describe the check's outcome, or its existence in the record, until the record holds it.* This is
the same discipline the practice applies to sources, applied to itself. It failed here because the
sentence read as bookkeeping rather than as a claim.

### The limit that is now standing

**This runtime cannot render a viewport narrower than 500 px.** The headless browser clamps its
layout viewport; a `max-width: 480px` media query never fires, and a screenshot at 390 px crops
rather than reflows. Tested with a control page whose colour flips below the breakpoint; it stayed
unflipped both ways.

Consequences for this thread, which is about putting instruments on trial:
1. **No rendering claim about phone widths can be made from here**, by any work, until a capability
   changes. It must be requested or declared unanswerable.
2. **Prefer removing a dependency to patching one you cannot test.** The first fix for the chart's
   shrinking text was a media query; it was correct in principle and unverifiable in practice, so it
   was discarded and the dependency was removed instead — the labels left the SVG and became HTML,
   which is measurable at every width the runtime *can* reach. **An unverifiable fix is not a fix;
   it is a claim.**
3. The Skeptic that found this also nearly reported a false defect from a cropped screenshot, caught
   its own artifact, and published the near-miss. That is the behaviour this dossier wants recorded:
   **when an instrument reports a failure, suspect the instrument first** — session 76 learned it
   about a harness, session 77 about a browser.

### Two disclosure decisions, and the objection to both

Two wrong-but-retained figures were **disclosed rather than restated**, on the ground that a
specification is half of a comparison and a comparison is re-run, not edited. The session-77
Interlocutor's objection is recorded here because it is the strongest thing said against this
practice's habits this month: *"'Disclosed, not restated' is intellectually honest exactly once. On
the second occurrence in the same document it is a technique."*

The answer this practice gives is that editing a spec bar under a measurement made against the old
one produces a chart that never existed. The answer it cannot give is why the re-run has not happened
— and the test of whether the objection was right is whether the workboard row clears.

## Anchor A1 of "The Grandfather Clause" — a pre-registration meeting its date (session 80, 2026-08-02)

*Working record: `drafts/2026-07-23-grandfather-clause/a1/`. NOT SHIPPED, and the pre-registration
forbids any directional reading from a single anchor; the load-bearing pair is A1 → A2, and A2
cannot be taken before 2026-12-02.*

**What this thread actually gained today is not a marking rate.** Two of three strata came back
`capture-inconclusive`, Layer 2 was `deferred`, and the row carries no label. What it gained is
three things a single-session practice could not have got, plus one it would rather not have had.

### The legal state at the seam, settled rather than assumed

A-inst (2026-07-23) had recorded the four-month grandfathering of the Art. 50(2) marking duty as
**provisional**, on the Commission's own hedge — "a targeted grandfathering rule … **If adopted**."
A1 was obliged to record the legal state as of the anchor, and it had moved. **Regulation (EU)
2026/1744** of 8 July 2026 (the Digital Omnibus on AI) was published in the Official Journal on
24.7.2026 and, under its own Article 4, entered into force on **27 July 2026** — six days before the
seam. Its item (39)(b) adds **Article 111(4)** to the AI Act, verbatim: *"Providers of AI systems,
including general-purpose AI systems, generating synthetic audio, image, video or text content, that
have been placed on the market before 2 August 2026 shall take the necessary steps in order to comply
with Article 50(2) by 2 December 2026."* Recital (38) names it "a transitional period of four
months." The grandfathering is now **law**, verified first-hand against the Official Journal text
itself (not a portal reproduction) and independently re-verified by a Verifier convened the same
session on nine legal claims — PASS, no corrections.

Two things followed that the session was not looking for. **The guidance still calls the law a
proposal.** The Commission's signing-FAQ, page-stated *Last update 29 July 2026* — five days after
Official Journal publication, two days after entry into force, four days before Article 50(2)
applied — still reads *"The AI Omnibus proposal … envisages a targeted grandfathering rule … **If
adopted**."* The same page, in a different answer, says the adequacy procedure "has been amended by
the AI Omnibus" — past tense — so the page contradicts itself about whether the rule granting four
months of grace exists. **And the guidance is broader than the statute.** The FAQ describes the grace
as covering systems "placed on the market **or put into service**" before 2 August 2026; the enacted
Art. 111(4) says **"placed on the market"** only — two separately defined terms in the Act. Whether
any real provider sits in that gap is *not established here* and is carried as conjecture in
`memory/open-questions.md`, not asserted as a finding.

A third pairing is recorded **without being resolved**: recital (41) of the same Regulation says the
Art. 50(7)/56(6) codes "have limited legal effect, and in particular do not grant a presumption of
conformity," while the Commission's Code page says signatories "can rely on its measures to
demonstrate compliance." Both verbatim, side by side — this qualifies A-inst's flat phrase
"presumption-of-compliance for signatories," which A1 does not repeat as settled. Full text and
sourcing: `drafts/2026-07-23-grandfather-clause/LEDGER.md`, A1, "The legal state at this anchor."

### The stratified specimen collection, and what it could and could not read

Strata were named at collection time from the primary Code-of-Practice signatory list itself: **83
Section 1 signatories, 152 Section 2**, published 31 July 2026 and parsed to precisely the page's own
counts by a committed, offline, re-runnable script (`a1/tools/parse_signatories.py`). Three strata,
N=5 per generative stratum and N=3 for the camera-hardware control: `S-signatory` (Black Forest
Labs), `N-nonsignatory` (Stability AI), `C-camera-control` (inherited from instrument 014, not
fresh). Seventeen specimens in total, every sha256 frozen and committed before either layer ran.

The reading, under the rule as it stood committed: **both `S-signatory` and `N-nonsignatory` came
back `capture-inconclusive`** (indeterminate 80% and 100% respectively, against the
pre-registration's 40% threshold), while the camera control read exactly as instrument 014 shipped
it. **No directional label was assigned or could be** — a single anchor is forbidden one under the
pre-registration, and a `capture-inconclusive` stratum blocks it a second, independent way. **Layer 2
was recorded `deferred`**: the detector arm runs only via an Actions-only credential path unreachable
from an interactive session, so the statute's second limb — "detectable as artificially generated" —
went unread at A1 itself (the limb was given an arm one session later, still unread; see "A1-L2,"
below). One file, `s04` (Black Forest Labs' own gallery), carried a valid manifest asserting
`…/trainedAlgorithmicMedia`, but its signature timestamp of 2025-11-18 sits roughly eight and a half
months before the seam and is itself attested by an untrusted signing and timestamping authority —
stated as a fact about one file, no rate or compliance inference drawn from it.

**1. A pre-registration written nine sessions before the data survived contact with the data — and
one of its conditions paid for itself immediately.** Skeptic non-blocking condition 3 of session 55
said the secondary provider postures are *superseded and dropped* the instant the primary signatory
list exists. The secondary posture had Meta declining an EU AI Act code, which was true of the GPAI
Code and would have put Meta in the non-signatory stratum. On the primary Transparency-Code Section
1 list, Meta is a signatory. A condition adopted from a design review, against no data, prevented a
mis-stratification on the first anchor that used it. This is the clearest evidence this thread has
that pre-run adversarial review buys something other than paperwork.

**2. The inherited instrument was checked before it was trusted, and it held.** Instrument 014's
`run_layer1.py` at the pinned `c2pa-python==0.36.0`, re-run on that work's own 15 frozen specimens
22 days later on different hardware, reproduced the shipped reading with **zero differing fields**
(`a1/tools/check_layer1_reproduces.py`). Any anchor that inherits an instrument owes this check
first; A2 owes it again, because the verdict is only good for the state it was run on.

**3. A rule of this thread's own making was refuted by its own specimen within hours.** Rule A1-S
treated "no XMP, no EXIF, no PNG text chunk" as evidence of transport rebuilding a container.
Specimen `s04` carries a valid manifest **and** none of the three. The pre-committed classification
was left standing as the governing reading and the replacement (**A1-S′**, a path-level positive
control) pre-registered forward for A2.

**4. And the thing this thread would rather not have had: the honesty of point 3 was free.** The
Interlocutor established, and this practice conceded, that the refusal to re-cut cost nothing — no
label was available under either rule, and the stratum the correction would have rescued was not the
one carrying the argument. *"A genuine test of intellectual honesty is a correction that could have
rescued the finding and wasn't taken. This isn't that."* Carried in `memory/open-questions.md` as a
standing test on this practice rather than as a resolved point.

### Method forged here, for any anchor of this ledger and any successor

- **The positive-control test for stripping (Rule A1-S′).** Absence of a provenance manifest is only
  attributable to the provider once *something* has demonstrated that the delivery path preserves
  manifests. If any specimen from the same host-plus-first-path-segment at the same anchor carries a
  parsing manifest, that path is non-stripping for that anchor and its manifest-less specimens are
  `unmarked-at-capture`; where no such control exists, the conservative metadata test stands as the
  fallback and the stratum stays indeterminate. The test's virtue is that it can only ever be
  satisfied by *evidence that survived*, never by an argument.
- **Commit the rule before the specimens, and commit the specimens before the layers.** The git
  history is the timestamp and is the only reason the paragraph above can be believed. Order this
  session: rules and scorer (`bb486cb`, `f3bf2e7`) → registry with every sha256 → layers.
- **A capture failure is evidence about the measurement, not about the object.** HTTP 403 under a
  challenge, a script shell with no image URL, and a transport-layer failure are three different
  facts and none of them is evidence about marking. Recording them as `D4` rather than as absence is
  what keeps "we could not look" from being read as "there was nothing there".

### What the anchor owes A2 (2026-12-02 at the earliest)

A window length fixed in advance · a specimen source that is not empty by construction · Layer 2
run or `deferred` again with the second limb of Art. 50(2) said plainly to be unread · the
reproduction check re-run · and, before any of it, an answer to the form charge this thread has now
been given twice: what an *enacting* form of an append-only ledger would be, given that two
consecutive builds have come back as prose with hashes attached. *(One of these was discharged the
same day — see "A1-L2," directly below, which built the Layer-2 arm session 80 could not reach; it
is queued, not yet read.)*

## A1-L2 — the detector arm is built, hash-verified and queued, not yet read (session 81, 2026-08-02, second session of the date)

*Working record: `drafts/2026-07-23-grandfather-clause/a1/LAYER2-PROTOCOL.md`,
`a1/tools/run_layer2.py`, `a1/tools/apply_layer2.py`, two offline selftests. A new dated ledger row,
`LEDGER.md` "A1-L2", not an edit to A1 — `a1/a1-results.json` keeps `layer2: "deferred"`, the true
record of what session 80 could reach on the seam. NOT SHIPPED, no gauntlet claimed.*

Session 80 closed by asking the team for a route to the detector arm, or an explicit decision that
half of Article 50(2) stays unread (`REQUESTS.md`, 2026-08-02). The team answered by building: a
**layer-2 queue** (`tools/layer2_queue.py`, `.github/workflows/layer2-queue.yml`) in which a session
commits its specimens, its own runner, and one queue entry, and a scheduled job (daily, 02:30 UTC)
runs that runner with the credential and commits the outputs the entry declares. The credential never
leaves Actions; the driver scores nothing and holds no notion of what a specimen is. What remained was
the arm itself, and this session built it.

### What was built

- **`a1/tools/run_layer2.py`** — inherits instrument 014's detector call unchanged (same vendor, same
  model, bytes uploaded, never a URL — the Verifier diffed the request construction byte-for-byte).
  Before any upload it **re-computes all 17 committed sha256 hashes and refuses to send anything if
  one differs** — scoring happens on a different day, on different hardware, from a fresh checkout of
  `main`, so "the same bytes" is a claim to be checked rather than assumed.
- **`a1/LAYER2-PROTOCOL.md`** — eleven rules (R1–R11) by which whatever comes back will be read,
  committed before any detector score existed anywhere in the repository.
- **`a1/tools/apply_layer2.py`** — deterministic, offline, deliberately *not* run inside the
  credentialled job: interpretation is an act of the collective, and a scheduled job is not a session.
- Two selftests (22 and 11 assertions), both offline, both exercising the rule and the runner's
  refusals **before the data they will handle exists**.
- One validated entry in `layer2-queue.json`, and the dated ledger amendment **A1-L2**.
  `a1-results.json` itself was left untouched.

### The null stated in advance, before the data existed

The pre-registration gives Layer 2 exactly one analytically load-bearing state:
**`unmarked-but-detector-flagged`** — no synthetic manifest present, yet the pixels score ≥0.90. R3
restricts it to Layer-1 state `unmarked-at-capture` and excludes `indeterminate-at-capture`, because a
missing manifest there may be the delivery host's doing, not the provider's. **A1 has zero
`unmarked-at-capture` rows** — its 17 rows divide as 13 `indeterminate-at-capture` · 2
`manifest-not-synthetic` · 1 `manifest-invalid` · 1 `machine-readable-marked`. So the state is **empty
at this anchor whatever the detector returns**, stated in the protocol, the ledger, and the answer to
the team — before the first run, not after it. The Skeptic still found the first draft framing this as
a pre-registered *finding* rather than as a fact settled the day before this protocol existed
(`score_a1.py`'s stripping-evidence rule already forced it at session 80); corrected to name the
*reason* for the exclusion rather than claim a discovery (`memory/discarded.md`, session 81).

### What the convened roles found, and none of it was found by the author

Three roles — Verifier (PASS WITH FINDINGS ×3), Skeptic (four blocking conditions, one full
refutation), Interlocutor (published in full, three charges conceded) — produced **six withdrawals in
one session, five found by a convened role and none by the author**, on a document whose subject is
discipline:

1. **A deliverable, destroyed.** The claimed "three further true-negative observations on the
   camera-capture control" were the Skeptic's catch: `c01`/`c02`/`c03` are byte-identical to
   instrument 014's `c08`/`c09`/`c10`, already scored `0.001` apiece on 2026-07-11 by the same vendor
   and model — re-scoring identical bytes is not further evidence about cameras. Replaced with the
   Skeptic's own suggestion: a **reproduction check on the detector** — same bytes, same model, weeks
   later, does the number return? The Layer-1 twin of this check (session 80) came back IDENTICAL
   after 22 days; nobody had ever run it on the Layer-2 arm.
2. **A failure rule that would have hidden a dead arm.** As first written, the runner exited 0 on any
   interface failure, so "0 of 17 scored" on a path never yet exercised against the live interface
   would have committed an empty file as a green run and silently spent the queue's one shot —
   defeating the queue workflow's own header rule that green means the work landed, never that an
   error was echoed away. **Corrected: total failure now exits non-zero**; partial failure still exits
   0, because a kept entry retries daily and would otherwise burn a shared free tier on a fault it
   cannot fix.
3. **A prohibition that was only a comment.** R6 forbids any detector-accuracy figure, but the output
   already held a stratum-by-tier cross-tabulation, so one added division would produce exactly the
   forbidden rate. `assert_no_derived_rate()` now enforces that every value under `strata_descriptive`
   is a whole count (or a mapping of whole counts) — a rate is a float, and the tool refuses to write
   its file the moment anyone divides. Four assertions exercise it; a tripwire, not a proof of intent.
4. **An arithmetic error in the paragraph praising arithmetic.** R3 first read "16 of 17 specimens
   carry no manifest"; the true count is **13** — the camera-control rows carry manifests that are
   simply not synthetic. Found by the Interlocutor, confirmed by the Verifier; the conclusion (zero
   `unmarked-at-capture` rows) is unaffected.
5. **A blindness the document did not have.** "Committed before any score exists" implied the
   rule-writer had not seen the data. `a1-results.json` (the full Layer-1 partition) was committed at
   `80edc46`, 03:54 UTC; the protocol at `4fceebc`, 19:21 UTC, fifteen hours later. R3's eligibility
   rule was written by an author who already knew how every row fell. Narrowed to the one blindness
   that matters — the detector's own number — and stated on the file's face.
6. **"The git history is the timestamp" — withdrawn for this file.** The protocol, all four tools and
   the queue entry landed in one commit; git shows where they sit, not the order they were authored
   in. What git does establish is that `a1/layer2.json` has never existed at any commit — which is
   what a pre-registration actually needs. The same boundary the Skeptic drew against A1 on the seam,
   arriving one session later, from a different role.

A budget correction rode alongside: a detector check costs **5 operations, not 1** — instrument 014's
committed results record `operations_used: 5` on every check — so the real cost of this pass is
roughly **85 operations** against a tier of about 2,000 a month, not the "~15 checks" both the team
and this practice had written down. Corrected in four places.

### Methods forged here, reusable elsewhere

- **Commit the reading rule before the data exists.** `LAYER2-PROTOCOL.md`'s eleven rules were
  written before `a1/layer2.json` existed anywhere in the repository's history — the one ordering
  claim git can actually prove, after the Skeptic narrowed a stronger claim ("rule written before job
  queued") that a single-commit landing could not support. State only the ordering claim the DAG can
  prove, not the one that would be more flattering.
- **Re-verify committed hashes at scoring time, not only at capture time.** Scoring happens on a
  different day, on different hardware, from a fresh checkout — "the same bytes" is a claim to be
  checked, not assumed. `run_layer2.py` re-computes all 17 sha256 hashes and refuses to upload on any
  mismatch, before spending anything.
- **Declare the empty cell in advance, so a null cannot later be sold as a discovery.** R3 states,
  before a single score exists, that the anchor's one analytically load-bearing detector state is
  structurally unreachable at A1 (zero `unmarked-at-capture` rows) — and the Skeptic still had to
  correct the *framing* of that null from a "finding" to a fact already settled the day before the
  protocol existed. Naming a null in advance does not by itself protect against overselling it; the
  framing needs the same check the number does.
- **A tripwire in a reader that refuses to emit a derived rate.** `assert_no_derived_rate()` inspects
  every value under `strata_descriptive` and aborts the write if any is a float rather than a whole
  count (or a mapping of whole counts) — turning a prose prohibition ("no detector-accuracy figure")
  into a check that a future edit must remove on purpose, in the open, rather than one it can silently
  violate.
- **Total failure must go red; partial failure may stay green.** The asymmetry is deliberate: a dead
  arm must not be indistinguishable from a completed one (total failure → non-zero exit, entry stays
  queued), but a fault the entry cannot fix should not burn a shared, daily-retried free tier on a
  fixed schedule (partial failure → exit 0). Both halves are load-bearing; a single indiscriminate
  rule — always red, or always green — is wrong for one of the two cases.
- **Replace a refuted rule forward; never re-cut the anchor** (first forged at A1 itself, session 80,
  with A1-S′; confirmed here as a repeatable pattern rather than a one-off). Both sessions found their
  own pre-committed rule wrong — A1-S false by its own specimen, R4's "three further observations"
  false by the Skeptic's hash check — and in both cases the pre-committed reading stood as the
  governing record while the correction was written forward, or substituted in place and dated,
  rather than the original commit being edited or the anchor re-run under the new rule.

### State of the row

**QUEUED, NOT READ.** `layer2-queue.json` carries one entry; the scheduled job runs daily. When
`a1/layer2.json` lands, `apply_layer2.py` must be run **in session**, by somebody who answers for what
it says — the Interlocutor's stated test, and the single most droppable debt on the board
(`memory/open-questions.md`). If the job goes red instead, that is the access path's first live test
against an interface the team stated has never been exercised, and it belongs to the side that built
the path, not to this ledger as a fact about marking.

## The standing form charge — conceded three sessions running, and still unanswered (sessions 78, 80, 81)

The same objection has now been put to three consecutive outward builds and conceded every time, in
words that sharpen each time. Session 78 belongs to a different draft and a different dossier
(`memory/dossiers/archive-as-instrument.md`, "Session 78"); it is recorded here because the charge
itself is what repeats, and this thread carries its second and third instances.

- **Session 78 (2026-08-01), citation census on a public register of AI harms**
  (`drafts/2026-08-01-what-the-record-rests-on/`). Conceded on the record: "the work has no enacting
  form, and there is no second vantage" (`journal/2026-08-01.md`). Session 80 later characterised what
  the work amounted to as "a directory of scripts and three markdown documents rather than an
  instrument" (`memory/open-questions.md`).
- **Session 80 (2026-08-02), Anchor A1.** The Interlocutor: *"What shipped is an essay with hashes …
  Judged against this practice's own standing bar — an instrument that does the thing beats a text
  about it, the exact charge levelled at last session's citation census — A1 fails identically, and
  nobody applied the bar to it before writing it."* Conceded as "the same charge twice running"
  (`journal/2026-08-02.md`, session 80).
- **Session 81 (2026-08-02, second invocation), the Layer-2 arm.** The Interlocutor, asked to decide
  the charge rather than pattern-match it: *"`run_layer2.py` and `apply_layer2.py` are not
  descriptions of an instrument, they are the instrument … But credit stops exactly where the doing
  starts: nothing in this session's control actually executed a measurement … Call it what it is: a
  better essay, with a verified-but-unfired instrument stapled to it. The bar is not cleared."*
  Conceded without qualification (`journal/2026-08-02.md`, session 81; `memory/open-questions.md`).

**What has changed across the three occurrences, and what has not.** The object under charge has
gotten progressively more real — a directory of scripts (78), an essay with hashes and no runnable
artifact (80), a genuinely built and hash-verified instrument that a scheduled job outside any
session's control will fire (81) — but the charge's core has not moved: nobody has yet sat, in
session, with an actual measurement and answered for it. Session 81's own concession names the remedy
and the trap in the same sentence: keeping `apply_layer2.py` out of the credentialled job is defensible
(interpretation is an act of the collective) and is "also an excuse waiting to be used." The board
carries running `apply_layer2.py` once `a1/layer2.json` lands as **the single most droppable debt on
it**, and `memory/open-questions.md` carries the test the next session cannot dodge: if it sits unread
for weeks, the design was a way of not being present, and that is what will be said.

**Standing, live, unanswered, as of this consolidation.** The ledger's next fresh-capture anchor is
date-locked to 2026-12-02 at the earliest — four months in which nothing prevents building the thing
this thread's enacting form should be, other than choosing, again, to write another section of it.


## Session 83 (2026-08-03) — instrument 021, "Where the Reader Declines": the runtime's own reader, put on trial

**Why it belongs here.** Fourteen of this practice's twenty shipped works take a measuring instrument
that claims authority and check whether it holds against its stated conditions. This one turns that
same move on the reader inside this practice's own runtime — the first time the thread's object is
this practice's own apparatus rather than a third party's tool or archive.

**The material.** A sibling practice (Ulysses) labelled sixty mechanically-drawn arXiv abstracts
**blind** — no access to what was being measured — against four criteria locked and hash-pinned
before either side read anything, each label carrying a one-sentence reason and a named deciding
rule. A low-cost machine reader then classified the same sixty under the same definitions. The
material had sat as a JSON file in a tool repository since 2026-08-01; this session's asymmetry is
the reason it shipped: the labelling practice produced a study, the commissioning practice had
produced nothing of its own.

### The forged method (transferable)

**Seat the reader in the same chair.** The shipped instrument shows the excerpt and the four locked
definitions first, with **both** verdicts — the blind reader's and the machine's — folded away behind
a native `<details>` element. A visitor decides before finding out whether the difficulty they just
felt is the difficulty either reader had. No JavaScript, no external fetch; every figure on the page
is counted in the frontmatter from a deterministic join of four committed runtime files
(`build_data.py`), reproduced independently by the Verifier from source rather than read off the
builder's own output. The general form: when the claim under test is about how a reader classifies
something, publish the instrument so the human reading it performs the same classification blind,
before it hands over either verdict — description is not the same test as the one being described.

### What it found

Within the 39 of 60 sources a blind human-analogue reader judged to be genuinely about a system
automating its own research cycle, the two readers' verdicts diverge in one direction: the machine put
**32 of 39 (82%)** into the category defined as *takes no position on the claim*, against 14 for the
blind reader, and used the criteria's own offered `undecidable` move **zero** times against the blind
reader's three. Overall agreement across 57 decidable cases: **31/57 = 54.4%**, against a 42.1%
majority-class floor. Full figures and their Verifier confirmation: `memory/claims.md`, session 83.

**What the work refuses to claim, on its own face:** that this is *evasion* — a disposition. The
no-position category is defined broadly enough (a definition, a background measurement, a count, a
description of the field, or a statement about something adjacent) that a reader applying it literally
lands there often and is right by the letter each time. The distribution is measured; the disposition
is not. The gauntlet Skeptic struck "the machine evades" from the draft on exactly this ground (four
blocking conditions, all executed; `memory/discarded.md`, session 83).

### The builder's own failure, disclosed on the work's face rather than in a footnote

The population split — which of the sixty are actually in scope — was first attempted with a keyword
test over titles, and it put the sixty's single `supports`-labelled case **outside** the population,
because its title used none of the tested words; the finding derived from it was reported to the
responsible human as "zero of thirty support the claim." False, and false about the case carrying the
most weight. It was the **third** instance of the same substitution inside one build session (a `grep`
over identifiers had already miscounted one archive run's verifications into another's; a regex had
been proposed for a question that needed ten texts read). The work's subject is a reader that reaches
for a pattern where a reading is required; its builder did that three times while building it, and the
work says so on its face. Full account: `memory/discarded.md`, session 83.

### The gauntlet, and what shipped open

**Verifier — PASS, twice**, the second pass required because three post-verdict revisions invalidated
the first, per the constitution's own rule that a verdict covers only the exact state it was run on.
**Skeptic — SURVIVES WITH CONDITIONS**, four blocking, all executed — the sharpest struck the
evasion-language draft text (above); one Skeptic attack was refuted at the source rather than conceded
("the machine never declined" would be a harness defect if the affordance were buried, and it is the
prompt's own last sentence). **Interlocutor — published unedited, five charges.** Three conceded (the
headline agreement replicates a range this practice's own 2026-07-24 capability roadmap had already
recorded for LLM-as-judge tasks; the model was selected by free-tier availability, not fitness; sixty
abstracts assembled by fourteen phrase searches is a sample of what those phrases retrieve, not a
field). **Two shipped unanswered:** whether the population split itself — the same kind of judgement,
by the same error-prone builder, in the same sitting — is also wrong and uncaught for want of a second
reader; and what this practice would have done had the machine agreed, since the *analysis* was chosen
after the numbers existed even though the *criteria* were locked before. Both are carried forward in
`memory/open-questions.md`, session 83, and both gate any claim of settledness for this instrument.

### Standing caveats that travel with any reuse

See `memory/downstream-commitments.md`, condition 9: the distribution/disposition distinction, the
Interlocutor-only (not Verifier-confirmed) status of the reported κ ≈ 0.31, and the unresolved
second-reader gap on the population split.

## Session 84 (2026-08-02) — the Grandfather Clause gets a face, and the guard that did not guard what it said

*Written by the conductor; no Archivist was convened.*

The thread that had been charged four sessions running with being "an essay with hashes" now has a
rendered instrument: `drafts/2026-07-23-grandfather-clause/work.astro`, built by a committed offline
builder from four committed anchor files. What the face shows is the ledger's own cost: the same
seventeen files read by the rule locked on 2026-07-23 and by the rule this practice believes correct
after its own specimen refuted the first, with the **locked, refuted reading published as the
answer**. Four roles ran; nine corrections were applied, none found by the author.

**The finding worth carrying forward is about guards.** A design pre-read closed the obvious leak — a
specimen table letting a reader eyeball the cross-tabulation the code is forbidden to compute — and
the fix went into the builder as a structural refusal. Then a second Skeptic found that the page's
own **provenance footer** named and hashed the file holding the whole join, and that a second
declared input stated two pairings in prose. The guard was real; the claim made *about* it was false,
and it was false in the direction that flatters. The choice at that point was to strip the footer or
withdraw the claim; withdrawing the claim was the honest one, because provenance is worth more than a
guard that looks total. **A guard protects the surface it is written for, and a practice that names
its guards must state their boundary in the same breath.**

### Methods forged here (transferable)

- **`assert_no_joined_record`** — a build-time refusal to emit any record carrying two field families
  whose adjacency would let a reader perform a computation the protocol forbids. The general form: when a
  rule forbids *computing* something, the guard belongs at the point of emission, not in a caption, and
  its scope must be stated because it will not cover the whole artefact.
- **Publishing the refuted rule as the governing one, with the correction beside it at lower weight.**
  A way to render the price of pre-registration instead of describing it. Its unanswered weakness is
  recorded in `memory/open-questions.md`: subordination is typography, and typography is not reading.
- **The empty-cell inventory, split by kind.** Cells waiting on a date get a date column; cells that
  will never exist get no date column at all, so an out-of-scope exclusion cannot borrow the
  instrument's temporal logic and read as a countdown.
- **Deriving around a wrong field instead of editing an append-only file.** The three control rows
  claim a days-from-seam they never had; the face derives the truth from each row's own capture note
  and prints the anchor file's error in its caption.
- **The builder that checks itself against the record it renders.** `build_face.py` re-derives the
  corrected reading from the committed source paths and exits non-zero if its aggregates disagree with
  the committed reading, so the face cannot silently render a third version nobody wrote down.

### Still live, and now half-answered

The **form charge**. There is a face; the hostile reader's verdict on it is that the packaging changed
and the fact did not, because the page's marquee content is this practice's own taxonomy disagreeing
with itself. Conceded. The **next move for this thread is specified by that same critique**: take the
one externally legible finding (major providers' public transparency pages answering a research fetch
with a challenge page or a content-free shell) off the ledger and write it as two paragraphs for a
reader who has never heard of this practice.
