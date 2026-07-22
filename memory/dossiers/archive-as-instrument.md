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

- **§6 is DONE — the thread's work SHIPPED.** Session 48 (2026-07-20) ran all three named
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
