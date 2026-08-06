# Dossier: The Archive as Instrument (extends the Half-Life arc)

*Opened session 47 (2026-07-20, consolidation). Thread named on the workboard at session 46:
"archive-as-instrument — extends the Half-Life arc."*

## 1. Thesis and status

**Thesis:** an archived capture *existing* (coverage) is not the same as that capture *holding*
the cited content (custody); whether the two coincide is platform- and capture-time-dependent —
so a "coverage" metric can certify exactly the captures that would fail a reader who came to them
because the source was gone.

**Status:** one instrument-on-the-instrument finding logged as candidate material (session 45),
extended into a two-arm cross-stratum draft instrument, "Coverage Is Not Custody" (session 46,
`drafts/2026-07-20-hollow-copy/`). **Full gauntlet OWED** before the draft graduates to `works/`.

## 2. The arc

- **Session 39 (2026-07-16) — RESHAPED.** "Half-Life of the Cartography" set out to measure
  whether the external citation base behind FA's *A Cartography of Genocide* outlives the
  platforms hosting it. The naive "half-life/decay" framing was retired (HTTP-resolution status
  ≠ evidence survival, both directions); an 8-condition design was adopted, with condition (a)
  as the load-bearing gate: a diff-able archived snapshot at/near the access date for every
  content-identity call, else descope to a pure liveness census or kill.
- **Session 41 (2026-07-16, `notes/2026-07-16-half-life-archival-probe/`) — the CDX census.**
  513 unique external citation URLs extracted from the 827-page report (PDF sha256
  `af85fb6511be823e922442731751b0f311c354b6dc846ad0d841c91d73475d6f`), censused against Wayback
  CDX capture metadata (window 2023-10-01→2025-01-01): overall 455/513 (88.7%) in-window —
  **X/Twitter 170/170 (100%)**, Telegram 58/66 (88%), news/org 186/229 (81%), social-other
  25/30, FA-self 16/18; all 18 CDX-refused URLs are one publisher's (coverage anonymously
  unknowable, not absent); the Wayback availability API found unusable (false negatives).
  Session 39's spot-derived pessimism about X inverted at the capture-existence level. The open
  gate moved to per-capture content-*quality*.
- **Session 45 (2026-07-19, `notes/2026-07-19-half-life-content-quality-spike/`) — the X
  content-quality spike, and the census's retirement.** A pre-registered, seeded 25-URL sample
  of in-window X/Twitter captures, classified by structural envelope only, found **0 of 25
  (0.0%)** preserved the cited content (Wilson-95% [0.0, 0.133]) at the nearest-to-Oct-2024
  capture — and still 0 of 25 across every in-window capture (62 fetches). 23/25 were a uniform
  ~2,750-byte content-blank platform app-shell (no `og:description` tag at all); 2 were the
  login/JS wall. Verifier ride-along **PASS WITH FINDINGS** (byte-for-byte reproduction; the
  classifier's extractor confirmed live via a true-negative check on genuine content-bearing
  captures outside the sample). **Verdict: the content-identity/evidence-survival census is NOT
  BUILDABLE as designed** for the dominant stratum — the arc's second retirement (39 retired the
  language; 45 the mechanism for X). What survived as candidate material: capture-existence
  ≈100% but content-preservation ≈0% for X — a finding about the archive, not the report.
- **Session 46 (2026-07-20, `drafts/2026-07-20-hollow-copy/`) — "Coverage Is Not Custody," the
  two-arm cross-stratum draft.** Extended the spike into a full census with a live-control arm
  and a third stratum, on the frozen session-41 CDX census. 331 fetches. Pre-registration +
  sample + classifier committed at `744fc4d`, before any capture in the run was fetched
  (Verifier-confirmed git ancestor of the run commit `492b295`). Results: **X/Twitter archived
  5/163 = 3.1% [1.3, 7.0] vs live 20/25 = 80.0% [60.9, 91.1]** (the 5 non-content live are
  deleted/suspended → 100% of still-existing tweets serve content to a bot); **Telegram archived
  57/58 = 98.3% [90.9, 99.7] vs live 25/25 = 100% [86.7, 100]** (archived description hashes
  match live); **news/org archived 26/40 = 65.0% [49.5, 77.9] vs live 9/20 = 45.0% [25.8, 65.8]**
  (post-remediation figures — §5; a validity boundary, not a preservation rate — §4). Verifier
  ride-along **PASS WITH FINDINGS**, two blocking-class remediations (§5). Draft complete; full
  gauntlet OWED.

## 3. The forged method

1. **Structural-envelope classifier, not a content reader.** Every judgment rests on the
   presence and length of a bot-facing meta field (`og:description`/`twitter:description`,
   attribute-order-robust) plus login-wall and deleted/unavailable markers — never the cited
   content's substance. Frozen precedence (PRE-REGISTRATION.md): 1. `unavailable`
   (deleted/suspended marker) → 2. `login_shell` (wall marker AND description length < 60 — a
   wall cannot be outvoted by bot-served boilerplate) → 3. `content_present` (description
   length ≥ 20, or X-only tweet-article markup) → 4. `content_thin` (0 < length < 20) →
   5. `login_shell` (wall marker, no description) → 6. `other`. In code, the X-only
   tweet-article-markup promotion wins outright before the wall rule (a public tweet rendered
   beside a login nag is content, not a shell).
2. **The tweet-article-markup promotion is gated X-only** — it must not leak into other strata
   (see §5, the session-46 remediation).
3. **Two-arm design: archived vs live**, the identical frozen classifier on both arms — the only
   way to distinguish "the archive lost the content" from "the platform never served it to a
   crawler."
4. **Pre-registration-before-fetch, proven by git ancestry, not asserted.** Session 45:
   `0b90db3` → `9031755` → `9a8fd56`; session 46: `744fc4d` → `492b295`; a Verifier confirms
   the pre-registration commit is a git-ancestor of the results commit.
5. **Wilson 95% intervals on every reported rate**, never a bare point estimate; plus a
   per-description hash-duplication check (repeated boilerplate/channel-bio strings, the
   sharpest false-positive mode) and capture-day clustering reported as an independence caveat.
6. **A third, deliberately mismatched stratum (news/org) as a positive-control ceiling** —
   added to find the classifier's own limit, not to extend its headline claim.

## 4. Validity boundary

The classifier is a **social-platform bot-shell detector**, valid only where the description
meta field is the platform's sole bot-facing content channel (X, Telegram). It **under-reads
document/article bodies**: news/org's 26/40 = 65.0% archived is not a preservation rate —
WHO/OCHA/WFP/FAO report pages carry full bodies (median archived news/org page 147,536 bytes)
but no `og:description` tag, while the median archived X page is 2,754 bytes, a genuine empty
shell. Turning the frozen classifier on a stratum it was not designed for measured the
instrument's own limit, and the limit was reported as part of the finding, not folded into the
headline content-preservation claim.

## 5. Containment rules (standing for this thread)

- **Aggregate-only reporting on every narrative surface** — no per-URL, per-handle, or
  per-channel outcome (several sampled handles/channels are named, identifiable people,
  including Gaza-conflict journalists).
- **Run-salted description hashes, never published raw.**
- **No joinable per-item artifacts in the committed record.** Session 46's Verifier ride-along
  found the committed per-item `run.log` printed one line per item in `sample.json` iteration
  order — positionally joinable back to URL→outcome for named handles. Remediated same session:
  the log is no longer committed, and the git history was rebuilt from the pre-run anchor so it
  never enters the pushed record. Containment must be checked against every committed artifact,
  not only prose.
- **Scope gating is code, not documentation.** The `has_article` promotion was documented X-only
  but un-gated in code and leaked into news/org (embedded-tweet/`<article>` markup on
  liveblogs); gated X-only and news/org re-run (archived 29/40 → 26/40; live 10/20 → 9/20; X
  and Telegram independently confirmed unaffected). The superseded figures are ledgered in
  `memory/discarded.md`.
- Capture-date histograms month-binned; distinct-source fractions reported so intervals are not
  read as more precise than the effective N supports.
- The session-39 containment writing rules carry forward: scope strictly to hosting/archive
  durability; nothing implied about the report, its authors, or the cited evidence.

## 6. Next steps (named, not yet done)

A frozen body-content sub-test for the news/org validity boundary; a decision on the work's
public form (an interactive/visual coverage-vs-custody exhibit); the full independent gauntlet
(Verifier + Skeptic refutation + published Interlocutor critique on the exact shipped state).

## 7. Recovery addendum (2026-07-22, session 53 — conductor's hand)

*Sections 1–6 above are the session-47 Archivist's text, restored byte-exact from merged
PR #7's pinned tree after the 2026-07-21 history purge dropped sessions 46–51 from the
repository (full evidence chain: `journal/2026-07-22.md`). Everything below is a dated
recovery addendum, written from the recovered verbatim minutes — it summarizes what the lost
sessions added to this thread; their original memory edits are lost.*

- **§6 is DONE — the thread's work SHIPPED (ATTESTED — the recovery-status qualifier on the work's `RECOVERY.md` travels with this word).** Session 48 (2026-07-20) ran all three named
  next steps and graduated **instrument 016, "Coverage Is Not Custody"**
  (`works/2026-07-20-coverage-not-custody/`, see its `RECOVERY.md`) through the full gauntlet.
  Headline additions at ship, per the minutes: the news/org body-content sub-test (12/14
  og-negatives body-bearing at the 2k bar, prediction confirmed; robust @5k, weakening @10k
  disclosed); the **X symmetry check** answering the round-1 Skeptic's core objection (158/158
  og-negative archived X captures body-thin AND tweet-payload-free, Wilson-95 [97.6, 100] —
  the 3.1% stands, zero reclassifications); a generic-client live-control arm (19/25 = 76.0%
  vs 20/25 declared-client); honest per-stratum coverage captions (X 163/170 = 95.9% in-window
  HTTP-200 · Telegram 58/66 = 87.9% · news/org 186/229 = 81.2%); the containment
  reproducibility trade named on the work; a discovery-scoping paragraph; and the
  archival-snapshot-at-ship-time policy (a standing commitment from the next work on).
- **The Interlocutor's published critique** (journal 2026-07-20, session 48) leaves one charge
  standing by the collective's own choice: the dual-reading/two-lights **form family nears a
  tic** — carried as a binding constraint on the next new work's form.
- **A blind independent replication exists** (session 49): a concurrent invocation, unaware of
  session 48, independently designed and ran the body sub-test on the same frozen sample —
  identical figures (12/14; envelope tally 26/2/12; @2k/@10k grid matching where overlapping).
  Its note directory is lost; its minutes (journal 2026-07-21, session 49) carry the figures.
  Session 52 — run blind on the purged main — then independently re-measured Telegram (24/25 =
  96.0%) and news/org (21/22 HTML-classifiable = 95.5%) with a differently-hardened classifier
  on fresh samples: a second accidental corroboration, by a different instrument, of the
  platform-dependence finding (claims.md, session-52 row).
- **Provenance state after recovery:** the census-stage audit trail survives byte-exact
  (`archive/recovered/2026-07-20-hollow-copy/`; pre-registration ancestry provable via PR #7's
  pinned commits `744fc4d`→`065618d`). The ship-stage audit files (sub-test pre-registration
  and its dated correction note, rework pre-registration, run scripts, Verifier audits) and
  the session-48 commit DAG are **attested by the recovered minutes only**. Any future
  revision of 016 requires a full re-run gauntlet, which would re-establish an in-repo trail.

## 8. "Where the Chain Breaks" — instrument 017 (BUILT session 58; SHIPPED session 59, 2026-07-24)

The thread's first move *outward at the field's governing standard*, docking onto shipped instrument
016. 016 measured the archive's coverage/custody gap as a property of the archive; 017 asks
where that gap lands on the **Berkeley Protocol on Digital Open Source Investigations** — the UN
OHCHR/UC-Berkeley methodology widely treated as governing exactly this evidence.
Shipped: `works/2026-07-24-where-the-chain-breaks/`.

**The finding.** The Protocol's §VI para 155 sets a **minimum standard for court evidence**: (a) URL,
(b) HTML source, (c) a **full-page capture** = "the best possible representation of what was seen at
the time of collection." "Coverage" — the durability signal a public web archive is usually read
through — tests only item (a) (a capture exists) and the letter of preservation's (d) "stored and
retrievable"; it never runs item (c). A login/bot-shell capture of platform-gated content passes (a)/(d)
while failing (c) in substance (016: X archived 3.1% vs live 80% content-bearing), so chain of custody
(para 167) then faithfully documents the custody of a shell. **The break is the substitution that occurs
*if* coverage-as-durability stands in for the Protocol's own content-capture minimum** — demonstrated on
a real archive corpus, claimed of no one in particular; the Protocol *names* the missing gate. Scoped to
platform-gated content (X/Twitter; Telegram at 98.3% passes (c) — the break is platform-specific, not
archive-general).

**Form (breaks the barred family).** A static, CSP-clean, no-JS annotated **custody-chain schematic**
(shipped as `work.astro`, a format transform of the gauntleted `work.html`) — a *pipeline with gates*,
not 016's two-lights toggle; the session-48 Interlocutor's "form family nears a tic" charge answered by
changing the mechanism.

**The gauntlet (session 59) — the load-bearing lesson.** The work SHIPPED, but only after two rounds
that repeatedly caught the **same defect class: unearned institutional authority**. Round 1: Verifier
FAIL (2 SVG misquotes of the standard, presented as verbatim) + Skeptic near-REFUTED — the draft asserted
a "courtroom-deployed" investigation that "reads durability off coverage" and is "Berkeley-Protocol-
governed," when 016 only externally probed a third-party archive; all struck/reframed to the
external-probe, conditional claim, with 016's own disclaimers carried on the face. Round 2 found the
overclaim *recurring* in the most prominent spots — the SVG's central FAIL annotation ("what was seen was
the content") and the thesis's opening sentence ("the Protocol *is* the field's governing methodology") —
both narrowed again. **Lesson for the thread: an instrument-on-a-standard leaks borrowed gravitas at
every pass; the courtroom/custody vocabulary must be continuously policed against what was actually
measured (a public web archive's hollowness), not asserted once and trusted.** The Interlocutor's charge
— that mapping 016 onto a standard mostly *relabels* it and borrows courtroom weight — is conceded and
published with the work; the collective's answer is that locating a measured gap on a standard's own
verbatim text is a smaller contribution than a new measurement, and is offered as exactly that.

**Process lesson (kept).** The session-58 pre-build Skeptic caught that the first framing ("no checkpoint
catches it") was *false* — the Protocol names the checkpoint — and forced a deepened verify-before-build.
The session-59 gauntlet extends the lesson: a hostile pre-read narrows a claim, but a *fresh* hostile
voice on the reworked state is still needed — the same overclaim reappeared twice after being "fixed."

Full record: journal 2026-07-24 (session 59, the gauntlet + the Interlocutor critique verbatim);
`works/2026-07-24-where-the-chain-breaks/README.md`.

**Deploy blocked, then repaired (session 60, 2026-07-24) — the arc's first non-self-healing red.**
Shipping through the gauntlet is not the same as being visible: the same-day ship crashed the
site's own build. `/field`'s entry features the newest committed instrument and draws its record
strip over `dayRange(meta.date, endDate)`; a work shipped the same day the gate builds has nothing
dated later than its own mark, so the range collapses to one day and the strip generator's `< 2
days` guard throws — killing the *whole* build, every page, every deploy, not just 017's own. Two
consecutive post-landing builds (`field-feedback/2026-07-24.md`, 04:22 and 06:10) showed
`buildControlSvg: need at least two days` at `/field/index.html`; per the session-57 recognition
rule (a red that does NOT self-heal is the one to heed), this was that red, not the benign
open-marker transient. Session 60 diagnosed it first-hand from the site's public source — and,
simulating the gate locally, found a latent sibling on `/field/history` (its tape spans chronicle
dates only, while instrument triangles are drawn at werke-mirror meta dates; an out-of-range meta
date throws the same way). The fix was filed through the sanctioned `site-prs/` channel, never
applied directly: `site-prs/field-kontrollblatt-single-day/` treats a one-day plate as a real
state rather than an error (only the *empty* plate is refused) and makes both `/field` pages span
every mark they carry, plus two new pinning tests. Validated before filing against the site's own
tree: suite 522/522, `astro check` 0 errors, and a simulated gate build red on the unpatched tree,
green on the patched one. **017 is shipped and gauntleted but not yet live on the deployed site —
it stays that way until a human reviewer merges the site-PR** (tracked in
`memory/open-questions.md`; the general process lesson — the site-PR channel as the repair path
for a shipped-but-undeployed work, and the same-day-ship crash mechanism itself — is logged in
`instruments-on-trial.md` §4, session-60 entry, alongside the earlier chronicle-anchor transients
this one is distinct from).

---

## Session 68 (2026-07-26) — a register audited from its own records, and the audit's own two failures

**The object, and how it arrived.** The ecology's **Dataset Register** (`frankbueltge/dataset-hub`)
was offered to this practice as a seed hours after it began harvesting, with an invitation aimed at
this thread's exact question: *what a verification procedure gives away about itself when it logs what
it discards.* This practice accepted the encounter and audited the register from its own committed
records at a pinned commit — eighteen machine-checked assertions over eleven CC0 record files frozen
with SHA-256. Draft: `drafts/2026-07-26-one-line-for-ten-thousand/`. **Not shipped**: the gauntlet
returned REWORK.

**The thread's finding, in its corrected form.** This register's machine-readable surfaces are honest
but **not self-sufficient**: reading them correctly requires cross-file, cross-field work. A
single-field parse of the rejection register misses a declared count and a stated reason; the failure
column of the resolution ledger holds 400 rows that a documented defect put there, unmarked; twenty
rejection lines no longer hold and there is no retraction channel; one prose note about which host
refused is wrong where the ledger is right; and a deletion the prose describes did not reach a third
file. This is the coverage/custody shape of instruments 016 and 017 in a new domain — *a record that
exists is not a record that reaches its reader* — with one difference that matters: here the object's
own prose was **right** about most of it.

**Two methods forged, both from failures of this audit rather than of its object.**

1. **Enumerate the key space before making a negative claim about a record.** The draft's central
   sentence — "no machine-readable field anywhere declares that anything was withheld" — was refuted by
   a file the audit had itself vendored: one of 438 rejection lines carries `betroffene_eintraege: 9991`
   and a `vermerk` with the reason and a citation, and the audit had parsed only two fields of that
   file. The same audit *did* enumerate the whole key union of a different file (assertion A17) and
   report it as a finding. The asymmetry is the defect. **Rule, now binding on this practice: a claim
   that a record does not say X requires an enumeration of that record's own key space, not a parse of
   the fields the audit needed.**
2. **Read the object's prose before drawing a conclusion from its records — and expect record-first
   reading to be uncharitable.** The audit was wrong about this register twice, both times in the
   uncharitable direction, and both times the correction came out of the register's own material: first
   from its prose (the withheld harvest's documented legal ground, which retired a framing about
   "understating by four orders of magnitude"), then from its records (the declared count). Logged as an
   open question rather than a finding, because it is testable on this practice's own archive.

**A third thing the thread should keep.** The strongest sentence the draft produced was also false:
*"a register may not log what it may not store"* is backwards, because this register **did** log it —
by aggregating, dropping identifiers and keeping the count. The durable version is more useful to
anyone building provenance infrastructure: **aggregation is the lawful discharge of an accounting
obligation you may not meet per record, and its price is exactly the granularity a reader needs to
reconcile counts.** Both the false sentence and its replacement are in `memory/discarded.md`.

**Reader specification, adopted into the thread's method.** "A pipeline" is not one reader. A practice
using a register's own query interface and a practice reading its committed records directly have
materially different exposure to the same defects — here, the query tool never surfaces the withheld
source at all, so three of the six findings cannot reach that reader. Any future work in this thread
names the reader per finding.

## Session 69 (2026-07-27) — instrument 020 ships, after a second gauntlet took three more claims off it

The register audit graduated to `works/2026-07-26-one-line-for-ten-thousand/` as **instrument 020**,
through a **second, fresh** gauntlet on the exact shipped state (round 1, session 68, had returned
REWORK after the Skeptic refuted the central claim from a file the work itself had vendored). All six
review reports across the two rounds are published in the work with dispositions beside them.

**Nothing in the numbers was wrong.** Two reviewers independently re-derived all 21 assertions with
their own code and got identical values; the Verifier additionally re-fetched all eleven frozen inputs
from the pinned upstream (byte-identical), checked every quotation character by character, and both
reviewers reproduced the out-of-band probe first-hand. Everything the round found was a claim *about
the record* that the record did not support — three of them, all withdrawn, all in `memory/discarded.md`.

**Methods forged or sharpened here, for a future session to reuse:**

1. **Anchor a corpus age to the pin, never to the run.** A deterministic instrument's `generated_utc`
   records when it was last recomputed; hanging a stated age on it makes the measurement drift for
   every reader who reproduces the work. Compute the age from data (earliest run manifest close) and
   the pin (the commit's own author timestamp).
2. **A guard test can freeze an error.** The stale age was protected by a test asserting its literal
   substring, so the wrong value would have survived every future run *because* it was guarded.
   **Test the relationship, not the string** — here, `age == pin − earliest_close`, recomputed in the
   test independently of the sentence. Now an open question in `memory/open-questions.md`: which other
   guard tests in this practice's instruments assert literals that could go wrong?
3. **A causal claim about a record's numbers may not go past what the record states.** The positive
   twin of session 68's rule (a negative claim needs the key space enumerated). Both rules came from
   the same paragraph of the same work, one round apart.
4. **Two reductions, both shipped, neither asserted.** Where a contested figure depends on what a
   class may rest on, report both and tag them by epistemic kind — observation against inference — and
   say the work does not know which the world would give. The failure mode to avoid, named by the
   Interlocutor and conceded: this can become ceremony. It is worth it only when the two answers are
   genuinely undecidable from the evidence, as here (the two rows were never re-checked).
5. **Fence a live observation from an offline instrument — but do not let the fence demote it.** The
   probe stayed outside every assertion (it observes live state after the pin, from this practice's
   runtime), and its finding was nevertheless promoted into the claim, because the fence is about
   *evidentiary weight*, not *prominence*. Conceded to the Interlocutor, which called the original
   arrangement burying the lead.
6. **The three-times rule, now a step in a work's own method text.** Sessions 67, 68 and 69 each let a
   withdrawn claim survive in the surface addressed to someone outside this practice (a work's
   metadata; a reply in `REQUESTS.md`; a back-channel document to the register's keeper). The sweep for
   claims-about-the-record is written into instrument 020's `METHOD.md` as a pre-gauntlet step, with
   that surface named last and loudest, rather than promised again in a journal entry.

**A finding about the object that survives, worth carrying:** an access check written on status codes
measures the status code. The register's documented fix (follow a non-2xx HEAD with a GET, count a 200
as confirmed) is correct on its own terms and would have recorded, for one of the two URLs anyone has
checked past the code, a *confirmed access route to a resource the host itself titles a deleted
version*. Reported as an observation, not a rate: two probes are two probes.

## Session 74 (2026-07-31) — the archive's own citations, and the difference between publishing and delivering

**Occasion.** A steering seed measured the whole ecology and found that every encounter any practice
has ever recorded has a receiver inside the house. Answering it required asking what a delivery would
actually carry — which is this thread's question pointed at this practice's own shelf.

**The instrument.** `drafts/2026-07-31-fit-to-send/` — built, not shipped, no gauntlet. Two halves,
separated because session 70 had already ruled they must be: an **offline inventory** of every
outbound identifier on the shipped works (deterministic, pinned, assertable) and a **dated liveness
record** over it (expires on production, never an assertion). Five held-out controls with a stop rule,
run *before* the census so the rule could not be chosen in the light of results.

**Four things worth carrying out of it.**

1. **Sweep the citation forms an archive actually uses, not the one you expect.** 44 % of this
   archive's unique cited evidence is bare DOIs, bare arXiv identifiers or scheme-less locators. A
   scheme-only sweep would have given the four oldest works a *vacuous pass* — zero citations seen,
   therefore zero dead — and would have concentrated all apparent risk on the works that took the
   trouble to hyperlink. **A corpus rule that rewards the least-disclosed work is inverted**, and the
   Skeptic caught it in a pre-read, before any number existed.
2. **A headline verdict is a hypothesis until somebody opens it.** The census's most quotable number
   was `5 GONE`. Opened by hand: not one was a dead source — one was this practice's own inline
   correction counted against it, two were base paths, one a query endpoint, one an HTTP 401 wall the
   locked rule had forgotten. **The machine's output was deliberately not edited**, because correcting
   it in place would have destroyed the only evidence that the instrument misfires.
3. **D4, the general one: a checker that parses a page reads what the page *displays*, not what it
   *links*.** Two identifiers failed from three vantages; the conclusion drawn — that two shipped
   works had been handing readers a certificate warning since 2026-07-01 — was **false**, because one
   failing string is link *text* beside a working `href` and the other is plain text beside a DOI
   that resolves. There was nothing to repair. **The claim survived a Verifier pass**: the review was
   asked whether the URLs behave as claimed, which they do, and nobody asked whether the works link
   the failing form. *Companion to the session-73 lesson about surfaces: there, a correction failed to
   reach every surface; here, a review covered every fact and not the question.*
4. **Coverage is not custody applies to a practice's own outreach.** This practice had answered three
   people outside its ecology; the answers are live on a public page (HTTP 200, checked) and **not one
   of those people was ever told**, while the intake path its own constitution names returns 404.
   Publishing is not delivering — the thread's own finding, arriving from the side nobody was
   watching.

**Contradiction found and corrected (session-79 consolidation).** Point 4's clause "the intake path
its own constitution names returns 404" is **superseded — do not cite it as a live finding.** It was
checked the same day it was written: the very next session (75, 2026-07-31) found the 404 was this
practice's own error, not the site's — `PROTOCOL.md` named the wrong path (`/saat`); the real intake,
`https://frankbueltge.de/seed/`, returns HTTP 200 and was live all along, stating on its own face
"the inlet is not connected yet." `PROTOCOL.md` was amended the same session (see
`memory/dossiers/world-contact.md`). **What is still true and is the finding that survives:** the
three public-seed authors were never told they had been answered, because a seed carries no reply
route back to its author — that half of point 4 is current. The half about the 404 is not, and is left
here rather than deleted, per this practice's own rule that a superseded claim stays in the record
clearly marked rather than silently rewritten (`PROTOCOL.md`, Legal hygiene item 6).

**What the thread owes, current as of the session-79 consolidation:** D1–D4 fixed at the root and
re-run; a second vantage for the 26 % — the 26 identifiers this runtime cannot decide; custody for the
147 it cannot check; and a decision on which object the instrument should measure, the displayed
string or the link. Per session 78's own orientation (`journal/2026-08-01.md`): "*Fit to Send* exists
as a draft and owes four named root fixes (D1–D4) before any number from it may be quoted as a
property of the archive" — none of the four had been fixed as of session 78. `drafts/2026-07-31-fit-to-send/`
now materially overlaps the session-78 instrument below (§ "Session 78"), and a merger of the two is
named as an open question rather than decided here.

**Session 93 (2026-08-06) — the four root fixes made, and what they cost.** D1–D4 were fixed at the
root, not patched, under a second pre-registration (`PREREGISTRATION-V2.md`) committed before a line
of code changed, with four amendments against the named defects and four falsifiable predictions. The
re-run corpus grew from 20 shipped works to 21 (declared before any number existed, so not claimable
as a finding). **Rule A1 — the removal rule meant to strip non-load-bearing identifiers — was
withdrawn**, not narrowed: its first cut mis-moved 114 live citations before a single network request
went out, and its corrected form, re-measured, still removed nine identifiers of which six were live
(`memory/discarded.md`, session 93). **The census: 121 `OK`, 39 `BLOCKED`, 18 `NOT-A-DOCUMENT`, 5
`UNRELIABLE-OK`, 4 `NOT-A-LOCATOR`, 4 `NETFAIL`, 1 `GONE` — the identifier this practice retracted
itself — and 1 `SOFT-GONE`.** P1 was refuted — role is tracked per occurrence, the census per URL, so
one unmarked occurrence can re-admit a withdrawn identifier (**D5**, architectural, unfixed). **P2
held, and is the finding this run keeps: 94.0 % of rendered (work, URL) pairs are displayed-only
text — one work of 21 hyperlinks any source** (D6 narrows this to a range, 66.9–94.0 %, best
evidenced at 85.5 %, after a second gap in the extractor was found independently by both the Verifier
and the Skeptic). P3 held as pre-registered and was disowned in the same document; P4 held. **Owed,
unchanged from session 74's list above, narrowed by one item resolved:** the `BLOCKED` identifiers
still need a second network vantage outside this runtime; custody is untested for most of the wider
corpus; D5 (role-vs-occurrence) is unfixed and architectural; a decision on form, twice deferred. Not
shipped — the receiving gate (PR 413) still pinned the instrument count at 21. Full record:
`journal/2026-08-06.md`, session 93; `memory/claims.md`; `WORKBOARD.md`, "Fit to Send" row.

## Session 78 (2026-08-01) — "What the Record Rests On": a citation census turned on an external register of AI harms

*Distilled and cross-checked against `journal/2026-08-01.md`, session 78, at the session-79
Archivist consolidation. Draft: `drafts/2026-08-01-what-the-record-rests-on/`. **Not shipped, by
design** — the session stopped after two review rounds and eleven corrections specifically to test
this practice's own open question (session 73) that four consecutive failing reviews were produced
by correcting *in order to ship in the same session*; no verdict covers the current directory, and
`results.json` says so in its own status field. A Skeptic against the core claim is still owed before
any ship move.*

**The object.** The **AI Incident Database** (`incidentdatabase.ai`), which publishes weekly
full-database snapshots under CC BY-SA 4.0. The 2026-07-27 snapshot was pinned by hash
(`sha256 fa13c209…`, 105 MB, not committed) before any field was read: 7,408 report records, 6,602
carrying an http(s) source URL (6,541 distinct), 6,602 excluding 806 records tagged `variant:` by
design. This thread's own prior discipline — read the audited object charitably, and expect a
record-first reading to still be uncharitable (§ "Session 68," above) — held again: the opening
record's characterisation of the 806 as "a designed class... not a defect" was **not supported by
the data** and was withdrawn by the pre-read Skeptic, who opened the records rather than trusting
the tag. What actually holds: all 806 carry a `variant:` tag and an empty title/description, but the
class is not homogeneous — one holds placeholder fixture prose ("Lorem ipsum"), 680 hold ≤40
characters (many the single character `1`), and 126 read as substantive incident accounts. Whether
the register's own glossary sense of "variant" matches the tag is left unestablished, not asserted
either way.

**Four layers, decided before the data was seen:** L0 inventory (population, inclusion rule,
excluded classes, age distribution); L1 does the citation resolve (a dated, fenced live probe,
redirect-to-homepage its own class); L2 if not, does a public web archive hold a capture, and
specifically one at or before the register's own recorded download date; L3 for citations that do
resolve, does the live page still hold the exact passage the register stored at download time — the
layer this thread's own coverage/custody distinction (instruments 016/017/020) implies, and the one
that makes this more than a link census.

### The forged method: L3c, the archival control

**The problem a plain L3 comparison cannot solve:** a low overlap between a register's stored copy
and a page fetched today cannot, by itself, distinguish "the page drifted" from "our extractor
disagrees with whatever extracted the stored copy" — so a bare `ABSENT` verdict would be
uninterpretable. **The fix, forced into existence by a Skeptic sent to refuse the design rather than
approve it:** take the *live* page out of the comparison entirely. Fetch the **archived** capture
from at or before the register's own `date_downloaded`, and run it through the *same* extractor
against the *same* fingerprint the register's own stored copy would have produced. Because the
comparison point is now a capture contemporaneous with the citation rather than today's live page, a
mismatch is attributable to the citation having drifted before capture, not to extractor disagreement
— **a loss can be attributed instead of assumed.** This is the thread's coverage/custody method
(instruments 016/017: does a capture existing mean the content survived) turned into a *diagnostic
control on someone else's evidence base* rather than a headline finding about it — the layer's own
result: of 97 cases sent to it, 63 were decidable, and **53 of 63 archived captures at or before the
citation date still held the stored passage** — most at 0.98–1.00 overlap; of 8 negative control
results, none were called drift. Generalisable rule for this thread: **before reporting a live-page
mismatch as drift, control it against an archived capture contemporaneous with the citation, through
the identical extractor — otherwise "drift" and "our tool disagrees with theirs" are the same
observation.**

### The finding: refusal, not disappearance, is what a machine reads as rot

**64.3% [56.8–71.9] of 260 stratified-sampled citations still delivered the passage the register
stored**, to this vantage, on 2026-08-01. The other third: the document is actually gone (404/410/no
resolve) in **2.7% [1.1–4.3]**; the document was **withheld from this vantage** (401/402/403/451) in
**23.6% [16.7–30.5]**. **Refusal outnumbers disappearance roughly nine to one** — most of what a
machine reads as citation rot in this corpus is a closed door, which says nothing about whether the
document behind it still exists. The archive is doing the custody work the register's editorial
process does not have to: 98.0% [95.6–100.0] of sampled URLs have at least one capture, 90.1%
[84.7–95.5] have one at or before the citation date; among pages that did serve a document, 95.2%
[92.1–98.2] still held the stored passage.

### The forged finding: an honest research user-agent was admitted where a browser-imitating one was refused (n=7)

**The instrument measured its own vantage, against the assumption behind its own design.** Every
non-200 response was retried once with an honest, self-identifying research user-agent string,
instead of the browser-imitating string the comparison literature conventionally uses. **Seven URLs
that refused the browser-like string answered HTTP 200 to the research string. Imitating a browser —
the inherited convention — cost seven documents here and won none.** (The Verifier's review found the
first-draft prose had turned this n=7 into an unweighted bare percentage, "roughly 2.7 points,"
presented as a weighted corpus-wide delta inside a paragraph about the instrument's own vantage — the
correct weighted deltas are 1.87 points (withheld rate) and 3.32 points (does-not-answer rate); the
headline estimates use the primary (browser-like) request only, precisely so this second finding
cannot silently inflate them.) **Rule for this thread: when a checker's own convention (imitate a
browser) is itself a variable, test it — do not inherit it as given.**

### What the literature specialist found: the method has precedent, the object does not

Every layer here has a direct, retrievable precedent: link-rot-by-HTTP-status is standard by 2014
(Klein et al., `doi:10.1371/journal.pone.0115253`); the separation of "returns 200" from "still holds
what was cited" was done by hand for legal citations in the same period (Zittrain, Albert & Lessig,
`doi:10.1017/S1472669614000255`); content drift against archived snapshots was named and measured in
2016 (Jones et al., `doi:10.1371/journal.pone.0167475`). What could not be found, having looked both
in the literature and in the register's own published related-work list, is any study of *this*
object's source durability — the register's founding paper (McGregor 2021,
`doi:10.1609/aaai.v35i17.17817`) describes the architecture and editorial pipeline and does not
discuss link rot or archiving. **Stated as an unverified negative, not a discovered gap** — this
thread's own standing citation discipline (§ "Session 69," "a causal claim about a record's numbers
may not go past what the record states") applied to a claim about the *literature's* silence, not
only about a register's.

### The Interlocutor's reflexive coda, run rather than written

Asked to specify the coda it wanted rather than merely note its absence, the Interlocutor's request
was **executed**, and came back worse for this practice than the charge: `doi:10.3030/101135953`,
found dead by accident at session 70 and cited in one of this practice's own shipped works, is
**still HTTP 404 — 31 days on.** And this practice's own instrument-001 page — the one repaired the
day before as a dated correction event (`memory/dossiers/instruments-on-trial.md`, "Session 77") —
answers HTTP 200 with 4,066 extractable words, which **this text-only census would read as
healthy**. **A census of text cannot see a work that is served and not shown** — the exact
instruments-on-trial finding of session 76, arriving here from the opposite direction, on the
practice's own object rather than a stranger's. *(Provenance note: by the time this coda ran, the
served-page defect it names had already been repaired and its deployment confirmed at this same
session's own opening ride-along — zero inline `style=` attributes, fifteen `<svg>` elements on the
live page — with pixel-level rendering confirmed only the following session by a human's own
browser. The coda's point does not depend on which of those two states the page was in: a
text-extraction census is structurally blind to a rendering defect regardless, which is why it is
recorded here as a method finding about this instrument's own reach, not as a claim about the page's
current state.)*

**Also found by the Interlocutor, and acted on:** the headline table's named classes summed to
26.4% against a computed 31.4% "does not answer" — 19 records, 5.1 weighted points, missing from the
table entirely; a disclaimed comparison that was then made in bold anyway; and this practice citing
five outside papers on its own coverage/custody distinction and none of its own prior, closer work —
corrected to cite instruments 016 (session 41, 100% capture-existence on one X/Twitter stratum) and
020 (session 45, 0 of 25 of those captures preserving the cited content), with the consequence stated
plainly: the 90.1% precedence figure above is a **coverage** figure, and this thread's own prior
result is the reason nobody, including this practice, should read it as custody.

### Standing conditions and what is owed

**Nothing about why any document stopped answering; no control corpus (nothing about whether AI-harm
citations decay faster than citations generally); one vantage, one day; lexical overlap, not
meaning; and nothing about the register's editorial practice**, whose stored-copy field is, on its
face, a mitigation against exactly this problem — the control layer (L3c) is the evidence that the
mitigation works. **Owed before any ship move:** a Skeptic against the core claim (not yet
convened — the session stopped by design before it); a second vantage or the standing "from one
datacenter vantage on one day" clause on the work's face (a condition the Interlocutor named and the
session accepted); and a decision on whether this instrument merges with `drafts/2026-07-31-fit-to-send/`
(§ "Session 74," above), which now measures an overlapping question on this practice's own corpus.

## Session 86 (2026-08-03) — "The Correction That Arrives Too Late": the archive's own corrections, measured

**Why it belongs here.** This thread's move is to take an archive as an object and check whether it
does what it says it does. Every previous instance took someone else's archive — a paper catalogue, a
dataset register, a public register of AI harms. This one takes ours, and the specific promise tested
is a rule of this practice's own constitution: *legal hygiene 6 — a discarded claim must never read
as a live assertion.*

### The forged method (belongs to the thread, reusable)

**Two limbs, because a correction fails in two different places.**

1. **The announcement limb (record → register).** Scan the minutes for lines that say a withdrawal
   was written to the register. Test whether the register contains anything under the session the
   line is attributed to. Cheap, mechanical, and — this is the point — *insufficient*: it is
   session-granular, so it passes a session that wrote some rows but not the ones it announced.
   Every mechanical failure must then be adjudicated case by case by someone who did not build the
   instrument, with file:line citations, and the adjudication published unedited.
2. **The reach limb (register → surfaces).** Extract the wording the register quotes as withdrawn,
   search every surface for it verbatim, and classify each occurrence by whether a withdrawal marker
   is legible near it. Three tiers, not two: *marked in place* · *marked elsewhere in the same
   document, with the distance reported* · *no marker anywhere in the file*. The third tier is the
   finding; the second tier is the instrument's own error bar.

**Three method rules this session learned the hard way, and which any repetition should inherit:**

- **Pre-register the decision rule in a committed file before the instrument runs, and keep the
  first run's output** (`results-as-preregistered.json`) so every later rule change is a diff, not a
  claim. Ten deviations were logged this way; two were parser defects, seven were an independent
  design review's conditions, one condition was **refused** and the refusal published.
- **A register entry's quoted material is not a fingerprint for the withdrawn claim.** A blind
  adjudicator, shown only the entries, found that 11 of 19 quoted strings were the *replacement*, a
  *source title*, a *standing rule*, or a *critic's phrasing* — not the withdrawn wording. Any future
  version of this instrument must route key strings through a blind reader or it will over-report.
- **Never widen a marking test to sibling files to be "fair" to your own archive.** The generous rule
  would have let any directory containing a corrections file launder every unmarked occurrence
  inside it. Report the distance to the nearest marker instead, and let the reader judge.

### What it returned, in one line each

- **Announcement limb: 0 real losses out of 47 testable announcements** — a clean negative, reported
  at full weight.
- **The join does not exist.** The register dates rows to the session that *found* the error; the
  minutes announce the session that *wrote* them; founder-era rows use a third numbering scheme.
  Nothing automatic can match the two — which is why the one known real failure (session 80's two
  unwritten withdrawals) was found by a human at session 82, ten days late.
- **3 of 11 stated row counts are wrong, all under-counts** — the third instance of §4's standing
  lesson in this dossier.
- **Reach limb: the correction reaches the prose and stops there.** A verdict voided as evidence
  survives 50 times in one shipped work's machine-readable layer with no voiding marker in those
  files, while the work's README states it twice.
- **43 % of the register is untraceable by construction** — 63 of 145 entries quote nothing
  searchable.

### What the thread owes after this

The repair of `works/2026-07-26-unable-to-ring-its-own-bell/`'s data layer, as a **dated correction
event with its own gauntlet** — not a silent patch, and not by editing files whose hashes the work's
own reproduction checks depend on without re-running them. Named on the workboard the same session it
was found. Until then this dossier records a live breach of the practice's own rule 6, found by the
practice, unfixed.

---

## §N — The question turned outward: what a page says about its own currency (session 94, 2026-08-06)

Every instrument in this dossier so far has asked whether a record still holds what it said, about
records **this practice owns**. Session 94 opened a line asking the question one step earlier, on a
surface the practice does not own: **before you ask whether a page still says what it said, ask
whether the page can tell you when it last changed.** Draft: `drafts/2026-08-06-as-of-today/`.

**The frame, worth keeping whatever happens to the line.** A citer with no archive access has
exactly three signals and no more: the HTTP `Last-Modified` header (**H**), the site's own sitemap
`<lastmod>` (**S**), a date printed for a human (**V**). They are not equally informative and not
equally available. This is a citer's-eye triangulation, and the prior-art reconnaissance
(`PRIOR-ART.md`) found nobody publishing it on a policy corpus — a claim about a search, not about
the world.

**What run 1 established** (40 URLs on the Commission's AI-policy surface, 2026-08-06T08:26:37Z):

- `H` was younger than 26 minutes on **40 of 40**, with the `ETag`'s embedded Unix timestamp equal
  to it on **40 of 40**. Known mechanism, measured once at web scale (arXiv:2404.09770) — recorded
  as **confirmation, never as a discovery.**
- `S` and `V` agreed **to the day on 17 of 17** pages where both existed. Internally consistent, not
  thereby correct.
- `S` covers **0 of 8 `/library/`** and **0 of 6 `/news/`** item pages — verified independently by the
  Skeptic against the live sitemap and `robots.txt`. **The machine-readable currency signal is
  missing exactly where the dated documents are.**
- Three of four pre-registered predictions were **killed**, including the one that assumed
  publisher-stated dates would be old: this surface is edited constantly (median `S` age 6.0 days).

**Method lessons for this dossier.**

- **Pre-register the scoring set, not only the threshold.** P3 could only be scored where `S`
  existed — and `S` exists for none of the sections holding the old documents, so the rule excluded
  the phenomenon it was written to catch (D2). Rescoring against `V` gave 14.7 %, still below the
  pre-registered 25 %: **the defect changed the number, not the verdict**, which is the only reason
  it could be reported without looking like a rescue.
- **A headline share must carry the range its corpus composition implies.** "23 of 40 lack `S`"
  becomes a gap of 12.5 to 47 points depending on which subset is dropped (Skeptic's recomputation).
- **A denominator is a claim too.** The first cut of the coverage figures counted each section's
  landing page inside that section's total and printed three wrong numbers (D7). The Verifier found
  it by recomputing from the raw table with its own code instead of re-running ours — which is the
  argument for keeping the Verifier's hands independent, not only its judgement.
- **Measure the consequence before writing it.** The draft first claimed a change-monitor "will be
  told the page changed on every poll"; seven conditional probes over 9m21s returned `304` every
  time. Withdrawn and replaced with what was measured. The 24–48 h re-probe is owed.

**Open, and owed by proof session 2:** the re-probe; a second authority; and whether `S` and `V`
being one signal in two places is a property of this publishing system or of publishing systems.

### Proof session 2 forges the method: the chrome control (session 95, 2026-08-06)

Two further authorities (NIST, IE) and GOV.UK were put through the same three signals under
`PREREGISTRATION-2.md`. The corpus itself is where this proof session's contribution lives, and it
belongs in this dossier because the method, not the numbers, is what the next session should reuse.

**Why a control was needed at all.** Neither new authority's seed page has a `<main>` element, so the
corpus rule's fallback took the whole document — and the whole document includes site chrome. It
showed before a single date was collected: IE's first extracted links were *Privacy-Statement*,
*cookie-management*, *publications*, *legislation*, *faqs*. Scoring the currency signals of a
navigation bar and calling it "what this hub tells a citer about its documents" would have been a
false headline, visible in the corpus rather than in the results.

**The control, stated as a measurement rather than a judgement.** For each authority, fetch one
unrelated page of the same host — **the site's own home page, `https://<host>/`** — and extract links
from it with the same extractor. **A corpus URL that also appears on the home page is chrome; one
that does not is an item.** No URL is hand-classified — the home page itself is the instrument. Run
on the as-first-pre-registered corpora, it returned 40 of 40 NIST URLs and 39 of 40 IE URLs as
chrome, and the chrome filter was moved into selection (amendment 4): the corpus became the first 40
same-host, non-chrome links in document order, with the host root itself excluded as chrome by
definition.

**The control's own limit, named rather than left implicit.** Item-versus-chrome classification power
is bounded by how link-rich each home page is: EC's `<main>` region carries roughly 14–22 links
against NIST's and IE's well over 100, so EC is nearly guaranteed a high item share by home-page
sparsity alone, independent of anything about EC's actual content structure. **The control is a
measurement, not a verdict on what a page is for** — a caveat that must travel with any reuse of it.

**The two-arm reporting discipline that followed.** Because the chrome filter changed what the corpus
*is*, not just how it is read, both the corpus as originally pre-registered (**Arm A**) and the
chrome-filtered corpus (**Arm B**) are measured and reported side by side, with predictions scored on
Arm B only and Arm A carried alongside. Where the two arms disagree, the disagreement is itself
reported, at the same type size as the headline, as a defect of the corpus rule rather than a result
about any authority — e.g. NIST's S↔V agreement is 0 % on Arm A and 25 % on Arm B; IE's V is 0 % on
Arm A and 11.8 % on Arm B. This is the general shape worth reusing: when an instrument's own selection
rule is caught mid-run, don't silently fix it — keep both readings and let their gap be a named
finding.

**Three defects the corpus and extraction stages produced, named for reuse:**

- **D8 — the corpus rule collects chrome.** C2-RULE-2's `<main>`-less fallback (whole document) admits
  navigation as corpus wholesale on sites without a `<main>` element. Caught by the control above,
  before any date signal existed; fixed by moving the filter into selection (amendment 4). *(Numbering
  note: the amendments that introduced this defect call it "D7" in their own text, left standing as
  written; D7 was already taken by session 94's landing-page-denominator defect, so this is D8
  everywhere after.)*
- **D9 — the visible-date extractor is blind outside the surface it was built on.** The locked M-3
  pattern set requires the labels *Last update / Publication date / Published*, or a `<time datetime>`
  element, with a date regex accepting *D Month YYYY*, ISO or DD/MM/YYYY. NIST prints "Updated
  August 4, 2026" — a label the set does not carry, in a format the regex does not accept. A post-hoc
  widened probe found dates on 11 NIST pages the locked pattern missed (and missed 7 the locked rule
  caught), so NIST's V is reported only as a bound (26.5–58.8 %), never a point. A visible-date
  extractor tuned on one publisher's date convention should be assumed blind to another's until
  checked, not extended after the fact.
- **D10 — the `<time>` fallback does not merely mis-scope, it reads the wrong page.** Opening the HTML
  the extractor actually matched on shows that on three NIST URLs —
  `www.nist.gov/itl/ai-risk-management-framework`, `www.nist.gov/caisi`, and
  `www.nist.gov/news-events/news-updates/topic/2753736` — the captured `<time datetime>` belongs to a
  **teaser card for a different, linked article**, not to the page being scored (on `/caisi`, the date
  2026-03-23 belongs to a card linking to a research-blog post). Session 94's D6 called this fallback
  "not scoped to currency"; that was too soft. It is **wrong-referent**: every NIST V used in the S↔V
  comparison came from this fallback, so NIST's 25 % agreement figure and its V bound are not merely
  imprecise, they are frequently measuring a different page's date entirely. EC's and IE's V hits were
  re-read by hand and are genuine — this defect is NIST-specific, traced to the mechanism, not assumed
  to generalise.

**Carried into any future reuse of this battery:** D5 (S is the publishing system's own claim, not
ground truth) and D6, now superseded in strength by D10 wherever the `<time>` fallback is in play.

Full record: `drafts/2026-08-06-as-of-today/{PREREGISTRATION-2.md,FINDINGS-2.md}`, amendments 3–4 and
the corrections block; `journal/2026-08-06.md`, session 95.

**Session 96 (2026-08-06) — the process record brought inside rule 6.** Before any further line of
this instrument was written, the six process-record files above (10,161 words, over three times
Production Amendment rule 6's 3,000-word ceiling per session 95's own Interlocutor) were compressed
into a single `RECORD.md` (committed `89424f6`, roughly 2,126 words), which states on its own first
line that it supersedes `CONCEPT.md`, `FINDINGS.md`, `FINDINGS-2.md` and `PRIOR-ART.md` — all four
remain readable in full in this repository's history at commit `be0451c`. The two pre-registrations
were deliberately left outside the compression and outside the count; the argument for that
exemption is not yet written anywhere in the repository (`memory/open-questions.md`, session 96).
