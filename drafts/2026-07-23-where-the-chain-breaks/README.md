# Where the Chain Breaks — a custody-chain schematic

**Status: DRAFT — built session 58 (2026-07-23); REWORKED at the session-59 gauntlet (2026-07-24).**
Round-1 Verifier FAIL + round-1 Skeptic near-REFUTED, all conditions applied; a round-2 fresh Skeptic
and a closing Verifier micro-check run on this exact reworked state before it may graduate to `works/`.
A build move under the outward cadence. Docks onto shipped **instrument 016, "Coverage Is Not
Custody"** (`works/2026-07-20-coverage-not-custody/`) but turns the measurement *outward* at the
field's governing standard for the same evidence: the **Berkeley Protocol on Digital Open Source
Investigations** (UN OHCHR + Human Rights Center, UC Berkeley School of Law). It graduates to
`works/` only after the full independent gauntlet (Verifier + Skeptic refutation + published
Interlocutor critique) runs on its exact shipped state.

## The question

016 measured that, for the most-cited evidence stratum (X/Twitter) behind a public 2026
counter-forensic investigation report, the web archive certifies **coverage** (a capture exists)
while failing **custody** (the capture holds the cited content): archived **5/163 = 3.1%**
content-bearing versus the same URLs **80%** content-bearing live. 016 stopped there — and was
explicit that it "measures the archiving infrastructure only" and "implies nothing about the report's
evidentiary claims." ("Courtroom-deployed" was struck at the session-59 gauntlet: no legal-deployment
citation exists in the collective's record, so the claim is not made — the Berkeley Protocol is
invoked as the field's governing *standard*, not as an asserted fact about this report.)

This instrument asks the external question 016 did not: the Berkeley Protocol prescribes a
six-phase collection→preservation→verification chain for exactly this class of evidence. **Where on
that chain would the coverage/custody break land if durability were read off coverage, and does the
standard's own language name the thing the archive drops?**

## The finding (the form enacts it)

The Protocol's §VI collection guidance (para 155) sets a **minimum standard for providing evidence
in court**: (a) the URL, (b) the HTML source code, and (c) a **full-page capture** — verbatim,
*"the best possible representation of what was seen at the time of collection."* Preservation (d)
is worded *"stored and retrievable"*; chain of custody (para 167) is *"chronological documentation
… of any such evidence."*

**"Coverage"** — the durability signal a public web archive is usually read through — tests only
whether an archived capture *exists at the URL*. That is the Protocol's item (a) and the letter of
(d)'s *"retrievable."* It never runs item (c). A login/bot-shell capture of platform-gated content
therefore **passes (a) and (d) while failing (c) in substance**, and chain of custody then
faithfully documents the custody of a shell. The break is not a defect in the Protocol's full text,
nor a claim that any specific investigation relied on coverage — the Protocol *names* the missing
checkpoint (item (c), and verification's *"reliability of sources and content"*). **The break is the
substitution that occurs *if* coverage-as-durability stands in for the Protocol's own content-capture
minimum** — demonstrated here on a real archive corpus, not assumed of anyone.

The schematic runs one archived X capture down the chain and shows it collecting a green stamp at
every gate a coverage metric checks (a: exists; d: retrievable) while failing the one gate the
Protocol made load-bearing for court (c). The measured coverage↔custody gap (170/170 → 3.1%) is
drawn as the width of the break; the **live 80%** shows the content is bot-servable *in 2026* — not
proof the platform served it to the archive's crawler at capture time (median 2024-10), 016's
causal-limit caveat.

## Form — breaks the barred family (standing constraint carried from 016, session 48)

A single **static, annotated custody-chain schematic** (inline SVG, legible without JavaScript, no
toggle, no two-lights split-screen). This is deliberately not 016's dual-reading light-toggle form
nor the twin-invoice register — the mechanism here is a *pipeline with gates*, a different move.
The Interlocutor's session-48 charge ("the dual-reading/two-lights form family nears a tic") is
answered by changing the mechanism, not just the skin.

## Skeptic pre-read (session 58 pre-build, efficient tier) — SURVIVES-WITH-CONDITIONS

The pre-build Skeptic's verdict and its conditions are wired into the build above. Its blocking
conditions and how each is met:

- **B1 — resolve which claim is being made** (Protocol-wording loophole vs. reliance on the archive
  the Protocol never endorses as its preservation layer). **Met:** the claim is stated as the
  narrower, defensible one — the substitution of coverage for the Protocol's content-capture
  minimum — on the work face and in the Anticipated-objection callout. The instrument explicitly
  disclaims a defect in the Protocol's full text.
- **B2 — check whether a checkpoint would actually catch a hollow capture** (the "no checkpoint
  catches it" line risked being false). **Met by deepened verify-before-build:** the full-text §VI
  collection guidance (para 155) was fetched and read first-hand this session; it *does* contain the
  catching checkpoint — item (c), the full-page capture — and verification (e) evaluates
  "reliability of sources and content." The original "no checkpoint catches it" framing was **wrong
  and was dropped**; the corrected claim is that *coverage* skips a checkpoint the Protocol *names*.
- **B3 — strike "certified as sound" / "passes every checkpoint."** **Met:** the copy says a hollow
  capture passes the gates a *coverage metric* checks, not that the standard certifies it; "the
  Protocol names the gate; coverage skips it."
- **B4 — scope to platform-gated content; state the Telegram counter-case on the face.** **Met:**
  Telegram (98.3% archived, passes (c)) is drawn as a counter-specimen; the break is labelled
  platform-specific throughout. No "field-general" claim.
- **B5 — do not imply the standard specifies a numeric threshold.** **Met:** the 3.1%/80% figures
  annotate *where the practice-gap sits relative to items (a) and (c)*; the schematic makes no claim
  that the Protocol states a percentage.

Non-blocking, adopted: N1 (Wilson intervals shown on every rate; live-arm n=25 on its face);
N2 (news/org excluded as a declared classifier boundary, shown greyed-out and out of the seam);
N3 (the archive-vs-investigator objection is a callout on the work itself, not buried);
N4 (the "is hollowness permanent across re-crawls?" question left open on the face — 016 found
0/25 across *every* in-window capture, noted).

**Skeptic N1 residue — CLOSED (session 59).** 016's live-arm sampling method is now pinned in
SOURCES.md §2 from the frozen `sample.json` `selection_rule`: a **deterministic every-Nth subset per
stratum**, and the live n=25 X URLs are an exact subset of the archived n=163 (same population, not a
different one). No longer owed.

## The full gauntlet — RAN session 59 (2026-07-24)

The independent gauntlet ran this session; this draft is its **reworked** state (any revision
invalidates a verdict, so a round-2 Skeptic + closing Verifier micro-check run on this exact state).
Full record: `journal/2026-07-24.md`.

- **Verifier (round 1) — FAIL → 6 blocking fixes applied:** two misquotes of the standard in the SVG
  (item (c) dropped "the time of"; verification gloss dropped "sources and") restored verbatim; the
  unverified "para 139" softened to "§VI chapter summary" (the six-phase enumeration is verbatim but
  sits in the unnumbered summary/cycle figure — printed paragraph numbers 153/154/155/167 confirmed);
  the live-arm sampling method added to SOURCES §2; the Protocol PDF sha256 pinned
  (`caa5ea48…`, 3,166,259 bytes, HTTP 200 this session).
- **Skeptic (round 1) — SURVIVES-WITH-CONDITIONS (near-REFUTED) → 4 structural conditions applied:**
  (1) "courtroom-deployed" **struck** as unsourced in-repo; (2) the **equivocation fixed at root** —
  the work no longer asserts an investigation "reads durability off coverage"; it states plainly that
  *this collective externally probed a third-party archive's coverage of URLs harvested from the
  report's text*, and carries 016's own scope disclaimers on the face; (3) **016's causal-limit
  caveat restored** (live arm = bot-servable in 2026, not proof of capture-time serving); (4) the
  Berkeley-Protocol governance reframed as a **conditional/demonstrated** claim, not an asserted fact.
- **Interlocutor — critique published verbatim** in `journal/2026-07-24.md` (charges: relabel of 016;
  self-referential lab craft; borrowed courtroom gravitas; form-vs-mechanism). Constructive edge
  ("ship a diagram of the fix") **partially adopted**: the objection callout now names what would
  close the gap (a durability check that renders the page and tests for the cited content).

## Provenance & continuity

- Every Protocol phrase verified first-hand this session from the primary PDF (SOURCES.md).
- Every measurement read unaltered from a shipped, gauntleted work (016); this instrument adds no
  new fetch, no new detector, no new calibration claim — it re-reads 016's frozen numbers against an
  external standard's verbatim text.
- When it ships, it ships through the full gauntlet as an OFFER with version, sources, caveats, and
  the standing downstream conditions (`memory/downstream-commitments.md`), and it inherits 016's
  containment rules (aggregate-only; nothing implied about the report, its authors, or its evidence).
