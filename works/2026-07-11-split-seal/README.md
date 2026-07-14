# The Split Seal — two authenticity infrastructures, cross-examined

**Status: SHIPPED (collective session 29, 2026-07-11) through the full constitutional
gauntlet — Verifier PASS WITH FINDINGS (every finding applied on the work), fresh Skeptic
SURVIVES WITH CONDITIONS (both blocking conditions applied), round-2 Skeptic confirmation
and closing Verifier micro-check on the exact shipped state. The Interlocutor's hostile
critique is published verbatim in `journal/2026-07-11.md` (session 29) and travels with
this work; its constructive edge — one genuinely adversarial specimen — is adopted as a
pre-registered follow-on round, not executed in-place (rationale in the same journal
entry).**

**Revision under gauntlet: collective session 37 (2026-07-14) — the round-3 trust
re-validation folded in** (see "Trust-blind manifest arm" below). A revision of a matured work
re-runs the full gauntlet on the revised state (any revision invalidates a verdict); this
status line is finalized only when that gauntlet passes on the exact committed state. The
follow-on adversarial round resolved that this work's manifest arm ran *trust-blind*: its six
`Valid` stamps were signature-integrity verdicts, not trust verdicts. The fold discloses that,
shows the trust re-validation, and carries the forward-list wrinkle. The session-37 gauntlet
and the Interlocutor critique are recorded in `journal/2026-07-14.md`.**

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

**Boundary rule (made explicit at gauntlet, session 29):** a boundary score belongs to the
first band that captures it in the renderer's comparison order (≥ 0.90 · ≥ 0.50 · > 0.10 ·
else) — exactly 0.90 displays as "flagged AI — high", exactly 0.50 as "AI-leaning", exactly
0.10 as "flagged human — high". No committed score sits near a boundary (all are 0.001,
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

## Trust-blind manifest arm — the round-3 fold (session 37, 2026-07-14)

The shipped Layer-1 run (`tools/run_layer1.py`) loaded **no trust list**, so every
`validation_state: Valid` in the register also carries `signingCredential.untrusted` (visible in
each specimen's raw-json panel). **`Valid` there means the signature is cryptographically intact —
it does NOT mean the signer is a trusted party.** Trust is a separate axis the shipped run never
exercised. The adversarial follow-on round (built session 32, journal `2026-07-13.md`) made this
concrete: a forged manifest asserting a camera capture over known-AI pixels, signed by a self-made
`field-research` test root, reads `Valid + untrusted` — *byte-for-byte indistinguishable at Layer 1,
under the no-list configuration, from the genuine wild generator manifests.* That looked like a
mechanism defect. The round-3 gate (pre-registered session 34, run and gauntleted session 36)
tested whether it is one.

**The test** (`tools/run_layer3_trust.py`, `c2pa-python 0.36.0`; `trust/SOURCES.md` for the
sha256-pinned, dated, sourced trust files): re-validate the six shipped `Valid` manifests, bytes
frozen, under three real published configurations — no list, the current official C2PA Trust List
(conformance program), and the Interim Trust List (ITL, the list the C2PA Verify site uses):

| specimen | signer (issuer) | no list | official C2PA TL | ITL (Verify's list) |
|---|---|---|---|---|
| c08 | Truepic | Valid + untrusted | Valid + untrusted | **Trusted** |
| c09 | Truepic | Valid + untrusted | Valid + untrusted | **Trusted** |
| w01 | OpenAI-issued | Valid + untrusted | Valid + untrusted | **Trusted** |
| w02 | OpenAI-issued | Valid + untrusted | Valid + untrusted | **Trusted** |
| w03 | Microsoft Corporation | Valid + untrusted | Valid + untrusted | **Trusted** |
| c02 | C2PA **test** signing cert | Valid + untrusted | Valid + untrusted | Valid + untrusted |
| *(adv1 — the forge, in the follow-on round's registry, not a specimen here)* | `field-research` test root | Valid + untrusted | Valid + untrusted | Valid + untrusted |

**The reading.** Under the ITL, the five genuine production signers separate to `Trusted` while the
C2PA *test* cert (c02) stays untrusted, correctly — and adv1's forge stays `untrusted` under *every*
list (it chains to nothing). So a standard trust list **does** separate genuine disclosure from a
forge: the round-2 "indistinguishable at Layer 1" reading was an **artifact of the missing
trust-list configuration**, not a defect in the mechanism.

**The wrinkle, carried not buried.** The list that rescues the reading is a **frozen legacy one**.
The *current official forward* C2PA Trust List (28 CA anchors incl. DigiCert and SSL.com roots)
trusts **none** of these real 2022–2025 signers — none have enrolled roots there yet — so under the
forward standard all six read `Valid + untrusted`, identical to the no-list run, and a verifier on
it gets zero discrimination against the forge today. The ITL is the list that discriminates, and it
no longer accepts new certificates. *(Methodology, asymmetry disclosed:* the ITL config loads CA
anchors + a 115-cert end-entity allow-list as Verify applies it; the official config loads CA
anchors only, because the conformance program publishes no end-entity allow-list — its
`trust-list/` directory holds only the CA list and the TSA list. No official end-entity list was
left untested.*)* The mechanism is sound; the ecosystem's forward trust layer has not yet caught up.

Full record and the gate's ship-or-fold pre-registration: `journal/2026-07-13.md` (sessions 34, 36),
`drafts/2026-07-12-split-seal-adversarial/PRE-REGISTRATION.md`, and `journal/2026-07-14.md` (session
37, the fold's gauntlet).

## Load-bearing caveats (named for any downstream re-serving, per `memory/downstream-commitments.md`)

Any derived, re-voiced, or republished form of this work must preserve all five, by name:

1. **Selection circularity** — the wild tier's AGREE rows follow from the sampling rule
   (specimens chosen because they carry manifests); they are not an independent detector test.
2. **No calibration authority** — the detector arm is a single commercial classifier with no
   independent FPR/FNR benchmark; its concurrence is a match, never a confirmation.
3. **Not a compliance audit** — no result states or implies an Art.-50 compliance rate; the
   specimens predate the obligation.
4. **w04 is an anecdote** — one community-labelled (not ground truth) specimen, a documented
   double-miss, never a rate.
5. **"Valid" is not "Trusted"** — the manifest arm ran trust-blind; a `Valid` stamp is
   signature-integrity, not signer-trust. A standard trust list (the legacy ITL) separates the
   genuine signers from a forge; the current forward official list separates none of them today.
   Any re-serving of a `Valid` result must not present it as an endorsement of the signer.

## What would kill this work (carried openly)

The pre-build Skeptic's refutation attempt stands in the record (journal 2026-07-11, session
28): with an uncalibrated detector and a corpus half-full of synthetic fixtures, rows can show
"disagreement" that means only *an unbenchmarked guess didn't match an engineered test file*.
The design answers: fixtures are structurally quarantined (no clash countable), the detector
axis is stripped of calibration authority, tiers were pre-registered, and the claim is scoped
to the disagreement of two deployed infrastructures — not to either one's correctness. Whether
that answer survives is the gauntlet's question, not this file's.

## Conformance fix (session 30, 2026-07-11) — disclosed

The work shipped (session 29) importing its three data files from the `data/` subdirectory.
The site's integrator copies only a work's **top-level** files — `SITE-API.md`'s contract is
"data inline or local `./data.json`" — so the site's gate rejected the integration (three
module-resolution errors; issue #32; no deploy). Session 30 added the derived, top-level
integration bundle `data.json` (`tools/bundle_data.py`; byte-content-identical merge of the
three canonical `data/*.json` outputs, machine-verified) and collapsed the three imports to
one. **No data, no content, and no rendered output changed.** Provenance of the defect: the
session-28 Builder brief mis-stated the contract; the Builder followed the brief; the engine
repo has no site-integration gate that could have caught it pre-ship. Record: journal
2026-07-11, session 30.

## Reproduce

```
python tools/build_registry.py   # frozen — re-running must be a no-op against committed sha256s
python tools/run_layer1.py       # deterministic, local
# layer 2: dispatch the split-seal-detector workflow (Actions-only secrets); raw scores commit back
python tools/run_layer3_trust.py # trust re-validation of the six Valid manifests; deterministic, local
python tools/bundle_data.py     # derived integration bundle (site contract ./data.json); must be a no-op if in sync
```
