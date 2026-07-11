# The Split Seal — two authenticity infrastructures, cross-examined

**Status: DRAFT (built collective session 28, 2026-07-11). Full gauntlet OWED before any
graduation to `works/`. Nothing here has shipped.**

## The claim (stated plainly, per the pre-build Skeptic)

Two deployed trust infrastructures for image authenticity — the **cryptographic provenance
manifest** (C2PA / Content Credentials) and the **statistical AI-image detector** — answer
different questions with different failure modes, and on the same fixed specimen set they can
disagree; neither constitutes ground truth. The work displays both verdicts side by side, per
specimen, and classes the disagreements. It makes **no** claim about which layer is right.

## Disclosed variant — read this first

This instrument is a **variant** of the "Integrity Clash" protocol (Nemecek, He, Cheng &
Ayday, arXiv:2603.02378), **not a replication**. The paper's second arm decodes a *genuine
embedded watermark*; no such decoder is publicly runnable, so this work substitutes a
**commercial statistical classifier** (score ∈ [0,1]), which is a categorically weaker signal.
The collective did **not** find or construct a single specimen matching the paper's exact
demonstration (a cryptographically valid manifest asserting human authorship over pixels
carrying a genuine AI watermark, both passing verification). What this work measures is the
weaker, in-the-wild analogue: where the manifest layer and a deployed detector product
disagree on the same bytes.

## Legal-timing note (not a compliance audit)

Art. 50 of Regulation (EU) 2024/1689 applies from **2026-08-02**: providers must mark
synthetic outputs "in a machine-readable format and detectable as artificially generated or
manipulated" (verified first-hand, session 26; `memory/claims.md`). This work is timed to that
deadline **for relevance only**. It audits **neither** providers' marking obligations **nor**
deployers' disclosure duties, and no result here states or implies a compliance rate. The
specimens predate the obligation.

## The two layers

- **Layer 1 — manifest arm** (`tools/run_layer1.py`, c2pa-python 0.36.0, run 2026-07-11):
  manifest presence · validation state · status codes · claim generator · signer ·
  `digitalSourceType` assertions. Deterministic on the committed bytes.
- **Layer 2 — detector arm** (`tools/run_layer2.py`, run via the repository's
  `split-seal-detector` GitHub-Actions workflow because the API credentials are Actions-only
  secrets — session-09 finding): the raw `type.ai_generated` score, committed untouched.
  **One vendor, one pass, no independent FPR/FNR benchmark** — the collective's entire prior
  calibration knowledge of this detector is a single anecdotal true-negative (score 0.001 on
  one real photograph, team verification 2026-07-03, dossier §4d). The detector axis carries
  **no calibration authority** in this work.

## Pre-registered display tiers (fixed BEFORE any detector score was seen)

This section was committed before the layer-2 workflow ever ran; the git history is the
timestamp. The raw float is always displayed; tiers exist only to make the register readable:

| raw `ai_generated` | display tier |
|---|---|
| ≥ 0.90 | "flagged AI — high" |
| 0.50 – 0.90 | "AI-leaning" |
| 0.10 – 0.50 | "human-leaning" |
| ≤ 0.10 | "flagged human — high" |

**Boundary rule (made explicit at gauntlet, session 29):** at an exact boundary value the
extreme tier wins — a score of exactly 0.90 displays as "flagged AI — high", exactly 0.10 as
"flagged human — high", exactly 0.50 as "AI-leaning"; the renderer's comparison order is
≥ 0.90 · ≥ 0.50 · > 0.10 · else. No committed score sits near a boundary (all are 0.001,
0.01 or 0.99), so this rule decides nothing in the shipped data — it is stated so the table
is unambiguous for any future re-run.

**A CLASH is declared only when a high-confidence tier contradicts a *Valid* manifest's
asserted origin** (e.g., manifest asserts generative origin, detector says "flagged human —
high"; or manifest asserts a hardware capture, detector says "flagged AI — high"). A lean
contradicting a manifest is recorded as **tension**, never as a clash. Specimens without a
manifest have nothing to clash *with*: they document the **absence** column (the RAND
ambiguity — "never marked, or mark lost?").

## The specimen set (N=15, frozen; selection rules stated)

Registry: `data/specimens.json` (sha256-pinned bytes under `specimens/`). Three tiers, kept
structurally separate in every rendering because they answer different questions:

- **`control-fixture` (7)** — synthetic conformance artifacts from `c2pa-org/public-testfiles`
  (legacy/1.4, Adobe 2022), selected by stated rule: one no-manifest file, one valid claim,
  one of each distinct error class in the corpus naming scheme (E-sig, E-dat, E-clm, E-uri, X).
  These test the **parser-correctness axis**. Their pixel content was never designed to carry
  an authorship claim, so their detector scores are displayed but flagged as
  **content-axis-meaningless** — a detector verdict on an engineered fixture is not evidence
  about the world, and no clash is countable on this tier.
- **`control-camera` (3)** — real captures distributed inside the same corpus (Truepic ×2,
  Nikon ×1 — the Nikon file carries a claim-signature mismatch per the corpus's own README).
- **`wild` (5)** — real media in circulation, original bytes from Wikimedia Commons (the one
  major host that preserves originals), fetched 2026-07-11: the two most recent
  direct-generator-download files (filename-timestamped WebP) in the Commons DALL·E-3
  category at selection time whose originals were fetchable; one consumer-design-tool AI image
  (Microsoft Designer manifest); one community-labelled AI image carrying **no** manifest; one
  human photograph (2010, pre-provenance era). **Found-and-rejected: none** — every wild
  candidate fetched was kept. **Selection used the manifest axis only; no detector score
  existed at selection time** (layer 2 had never run when this set was frozen — the workflow
  run postdates this file's first commit).

**Wild-hunt outcome, honestly:** it *succeeded* in finding intact generator manifests in the
wild (w01–w03) — but note what that means: all three manifest-bearing wild specimens are
**AI images that disclose themselves**. The hunt found **no** wild camera-native manifest
outside the conformance corpus, consistent with the documented scarcity of Content
Credentials in circulation (claims.md, session 3/6 rows). **And the logical consequence,
stated outright rather than left for the reader to derive (gauntlet condition, session 29):
because w01–w03 were selected *because* they carry intact generator manifests, the wild
tier's 3-for-3 AGREE outcome was close to guaranteed by the selection rule itself. Those
rows are evidence about the sampling rule — manifest-bearing wild images are self-disclosing
AI images whose content a detector also flags — not an independent test of detector accuracy
in the wild.**

## Field note recorded during sourcing (session 28)

The conformance corpus's **current-spec tree (`2.2/`) contains no test files** — only READMEs
and `.gitkeep` scaffolding; every actual image lives under `legacy/1.4/`. The session-27 gate
description ("a current 2.2 tree plus legacy/1.4") was optimistic about the 2.2 half; the
controls in this work are therefore **spec-1.4-era artifacts**, stated as such.

## Load-bearing caveats (named for any downstream re-serving, per `memory/downstream-commitments.md`)

Any derived, re-voiced, or republished form of this work must preserve all four, by name:

1. **Selection circularity** — the wild tier's AGREE rows follow from the sampling rule
   (specimens chosen because they carry manifests); they are not an independent detector test.
2. **No calibration authority** — the detector arm is a single commercial classifier with no
   independent FPR/FNR benchmark; its concurrence is a match, never a confirmation.
3. **Not a compliance audit** — no result states or implies an Art.-50 compliance rate; the
   specimens predate the obligation.
4. **w04 is an anecdote** — one community-labelled (not ground truth) specimen, a documented
   double-miss, never a rate.

## What would kill this work (carried openly)

The pre-build Skeptic's refutation attempt stands in the record (journal 2026-07-11, session
28): with an uncalibrated detector and a corpus half-full of synthetic fixtures, rows can show
"disagreement" that means only *an unbenchmarked guess didn't match an engineered test file*.
The design answers: fixtures are structurally quarantined (no clash countable), the detector
axis is stripped of calibration authority, tiers were pre-registered, and the claim is scoped
to the disagreement of two deployed infrastructures — not to either one's correctness. Whether
that answer survives is the gauntlet's question, not this file's.

## Reproduce

```
python tools/build_registry.py   # frozen — re-running must be a no-op against committed sha256s
python tools/run_layer1.py       # deterministic, local
# layer 2: dispatch the split-seal-detector workflow (Actions-only secrets); raw scores commit back
```
