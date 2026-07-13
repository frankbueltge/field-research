# Pre-registration — The Split Seal, adversarial round (round 2)

**This file is committed to git BEFORE any Layer-2 (detector) score for the two constructed
specimens is seen.** The git history is the timestamp; the credibility of everything downstream
rests on that order (the shipped round proved the method: tiers-before-scores, `9237865` →
`f3992e3`). If a later commit shows a detector score whose parent commit does not already contain
this file, the pre-registration is void.

> **Citation note (added in the session-34 rework, after the scores; the pre-registered content
> below is unchanged).** The two hashes above were written in session 32 as `ec84146` → `902332d`;
> the repository's full history was rewritten on 2026-07-12 (commit messages and author metadata
> only — no file content, no ordering changed), which changed every commit ID. The live
> equivalents are `9237865` → `f3992e3` (resolved via `notes/2026-07-12-history-rewrite-map.md`);
> the ancestry order they prove is intact. This round's own pre-registration → score order is
> `57dd2ee` (this file) → `cd26db0` (the adv1/adv2 scores), independently checkable.

Round frozen registry: `data/specimens.json` (two specimens, sha256-pinned). Layer 1 already run
(`data/layer1.json`) — it is deterministic manifest reading, not a score, and reading it does not
compromise pre-registration. Layer 2 has NOT run for adv1/adv2 at the time this file is committed.

## What this round is, and is not

It is a **reflexive self-test of instrument 014** ("The Split Seal"), not a finding about the
world. The shipped round found "no clash in N=15" and conceded that the sample was structurally
near-incapable of producing a clash (every specimen self-marked AI or honestly unmarked). This
round constructs the two clash-capable specimens the shipped sample lacked and asks a **narrow,
mechanical** question: *when the register's own clash rule is finally fed a specimen engineered to
trip it, what happens — and what does that expose about the rule itself?*

## The claim this round can support (and the claims it cannot)

**Smallest honest claim it can support:** the register's clash rule, fed a cryptographically
valid manifest asserting a false origin over known-AI pixels, either fires or fails to fire as
pre-registered here — and, either way, the exercise exposes whether the rule distinguishes a
*trusted* Valid manifest from a *cryptographically-valid-but-untrusted* one. This is a
mechanism-validity claim about the collective's own instrument.

**Claims it CANNOT support (pre-committed, so no later drift):**
1. No claim about real-world clash prevalence or base rate. The shipped "no clash in N=15" is
   neither strengthened nor weakened as an empirical claim about circulating media.
2. No claim that a real adversary could obtain a manifest chaining to a genuine production trust
   anchor. That scenario — the one with real stakes — is out of scope and untested BY DESIGN. We
   cannot and will not forge a trusted credential.
3. No general robustness claim about the detector across generators, prompts, or edits. Two
   constructed specimens are an existence proof, not a benchmark.
4. No claim that the instrument "catches forged capture claims" in general — only that this one
   pre-registered case did or did not trip the rule.

## Display tiers (unchanged from the shipped round; the raw float is always shown)

| raw `ai_generated` | display tier |
|---|---|
| ≥ 0.90 | flagged AI — high |
| 0.50 – 0.90 | AI-leaning |
| 0.10 – 0.50 | human-leaning |
| ≤ 0.10 | flagged human — high |

Boundary rule (identical to the shipped round): a boundary score belongs to the first band that
captures it in the comparison order (≥ 0.90 · ≥ 0.50 · > 0.10 · else).

## The clash rule — REFRAMED, with the trust gate the shipped rule lacked

The shipped rule declared a CLASH "when a high-confidence detector tier contradicts a **Valid**
manifest's asserted origin." **Reflexive finding of this round (already established from Layer 1
+ the shipped data, before any new detector score):** in the shipped configuration **every**
`validation_state: Valid` also carries `signingCredential.untrusted` — no trust list was loaded,
so `Valid` means *cryptographically valid*, NOT *trust-anchored*. The shipped rule therefore
keyed on a verdict that carries **no trust discrimination at all**. Under it, the forged specimen
adv1 (Valid + untrusted, asserting a camera capture over AI pixels) is **indistinguishable at
Layer 1** from the shipped round's genuine wild generator manifests (w01–w03, also Valid +
untrusted).

Accordingly this round splits the outcome vocabulary and **never emits a bare "CLASH":**

- **`clash(untrusted)`** — a high-confidence detector tier contradicts the asserted origin of a
  manifest that is `Valid` but `signingCredential.untrusted`. Every report of this outcome MUST
  co-state `Valid` and `untrusted` in the same sentence/figure. This is the ONLY kind of clash
  this round (or the shipped round) could ever have produced, because no specimen available to
  the collective carries a trusted Valid manifest.
- **`clash(trusted)`** — the same contradiction against a manifest that is `Valid` AND trust-
  anchored. **This round pre-declares it can produce ZERO of these, by construction.** It is the
  case that would matter; it is named here precisely so its absence is on the record, not hidden.
- **`tension`** — a *lean* (not high-confidence) tier contradicting a manifest. Recorded, never a
  clash (unchanged from the shipped round).
- **`no manifest`** — nothing to clash with; documents the absence column (adv2's case).

## Specimen roles and the reclassification the Skeptic forced

- **adv1 (constructed-forge):** Valid+untrusted manifest asserting `digitalCapture` over known-AI
  pixels. The clash-capable specimen. Its Layer-1 verdict is rigged by construction (a manifest
  built to assert a false origin asserts it) — that side proves nothing. The **only non-rigged
  signal** is the detector's score on its pixels.
- **adv2 (constructed-stripped):** the same AI pixels with NO manifest. By the clash rule (which
  requires a manifest) adv2 **structurally cannot produce a clash** — it is NOT new clash
  material. It is kept, honestly relabelled, as a **manifest-stripping robustness check**: it
  tests whether removing the provenance layer changes anything the detector sees. Its value is the
  paired comparison with adv1 on identical pixels.

## Pre-committed predictions and their interpretations (BEFORE the scores)

Both specimens carry the **exact decoded pixels of shipped w03**, which the detector scored
**0.99** in the frozen shipped round. The prediction and the meaning of each possible outcome are
fixed here so nothing is read off the result after the fact:

1. **Predicted:** adv1 and adv2 both score high (≈ 0.99, "flagged AI — high"), because the pixels
   are those of w03. A fresh run on the actual specimen bytes is the rigorous confirmation (the
   embedded manifest changes file bytes; the detector may re-decode).
2. **If adv1 scores high (as predicted):** the register records **`clash(untrusted)`** on adv1 —
   a Valid (untrusted) manifest asserting a camera capture stands beside a high-AI detector score
   on the same pixels. Interpretation: the two layers *can* contradict on a clash-capable
   specimen; and the contradiction is the untrusted kind, which any trust-checking verifier would
   already have flagged. The headline is the reflexive one: the instrument's Layer-1 "Valid" did
   not distinguish this forge from a genuine disclosure.
3. **If adv1 scores low/ambiguous (contrary to prediction):** this is recorded as **detector
   failure on a known-AI, non-adversarial case** (ground truth is AI by construction) — NOT as
   "the layers agree, no clash." A miss here is an unflattering datapoint about the uncalibrated
   detector, logged as such.
4. **adv2 vs adv1:** if the two scores are ≈ equal (predicted), that demonstrates the detector
   **ignores the manifest layer entirely** — stripping the provenance changes nothing it reads.
   If they diverge materially, that divergence is itself the finding (re-encoding/manifest bytes
   affected the detector), logged honestly.

## Binding build/handling conditions (from the pre-build Proposer and Skeptic)

1. The signing root is permanently, literally labelled non-production ("Split Seal Test Root CA" /
   O=field-research); no committed file ever presents the specimens as genuine captures.
2. Specimen pixels contain **no identifiable real person** (a synthetic cat). Provenance of the
   base pixels (shipped w03, Commons-licensed, vetted) is disclosed in `data/specimens.json`.
3. Tiers, clash rule, null-result interpretation, and predictions are committed here BEFORE any
   adv1/adv2 detector score — verifiable by commit order.
4. The specimens live ONLY sha256-pinned in this repository; they are never circulated as
   standalone images. No private signing key is committed (only public certs, under `test-ca/`).
5. Any published display foregrounds — not in an appendix — that adv1 is a self-forged internal
   test artifact signed by an openly non-trusted root; and never separates the word "clash" from
   "untrusted".
6. The write-up documents the construction for disputability but frames it as standard SDK
   signing with a self-disclosing untrusted root, NOT as a trust-defeating exploit (there is no
   trust-defeating exploit here — an untrusted signature is caught by any verifier that checks).
7. The shipped round's registry stays frozen and untouched; this round is separate.
8. The generalizability ceiling (N=2 constructed; existence claim only) travels with every output.

## Deviation from a literal pre-build condition, disclosed

The Proposer's condition 2 said adv1's pixels should be "the collective's own generation, not
lifted imagery." The round as pre-registered (open-questions, session 29) specifies "a
stripped-manifest twin **of a wild specimen**" — i.e. wild (lifted) pixels — and using the
*same* wild pixels for both specimens is what lets the forge be compared to a genuine manifest and
to a stripped twin on identical bytes, which is the whole mechanism. The substance of condition 2
(no real person; licensed; already vetted) is honored by using shipped w03. The conductor records
this as a deliberate, disclosed deviation for the gauntlet to weigh, not a silent one.

---

## POST-SCORE ADDENDUM — the gauntlet, and the decisive test it exposed (session 34, 2026-07-13)

*(Everything above this line was committed before any adv1/adv2 detector score, at `57dd2ee`. This
addendum is written after the scores and after the gauntlet; it does not alter a single
pre-registered prediction — it records what happened and what the round is missing.)*

**The scores, as predicted:** adv1 = 0.99, adv2 = 0.99 ("flagged AI — high"), landed via the
manual detector dispatch at `cd26db0` (workflow run 29221075143). Prediction #1 confirmed;
`clash(untrusted)` recorded on adv1 per the pre-committed rule; adv1 ≈ adv2 confirms the detector
reads pixels and ignores the manifest layer (prediction #4).

**The gauntlet's decisive objection (the Skeptic's core, verified against the shipped data).** The
round's reflexive finding — "Layer-1-indistinguishable" — rests entirely on the fact that **no
trust list was loaded** when Layer 1 ran. But the shipped set's six `Valid` manifests are not
anonymous: `c08`/`c09` are signed by **Truepic** (issuer `Truepic`, CN "Truepic Lens SDK … in
Vision Camera"), `w03` by **Microsoft Corporation**, and `w01`/`w02` by an `OpenAI`-issued
credential — all **real, deployed production signers**, each reading `signingCredential.untrusted`
for the *same* reason the ad-hoc `field-research` test root does: nothing was loaded to check
against. (Verified first-hand in `works/2026-07-11-split-seal/data/layer1.json`, session 34.) A
**properly configured trust list would very plausibly separate** these production signers (chaining
to recognized roots) from the "Split Seal Test Root CA" (chaining to nothing) — which is precisely
the discrimination this round claims the instrument cannot make. **That test was never run, and its
ingredients are already in the repository.** Until it is, "indistinguishable" is a property of the
*missing configuration*, not of the instrument's design.

**Verdict (conductor, session 34): REWORK — NOT SHIPPED.** The draft is corrected to remove the
overclaim (see the README's trust-list disclaimer and the reworded "under the configuration
actually run" language) and the decisive test is **pre-registered below**. The round graduates only
after that test resolves; the Interlocutor's published critique (journal 2026-07-13) reaches the
same missing experiment from the other side and is thereby adopted, not merely filed.

## PRE-REGISTRATION of the decisive test (round 3 — the trust-list re-validation)

*Committed here BEFORE the trust-list test is run.* Load a standard C2PA trust configuration (the
c2pa library's own bundled trust anchors and/or the published C2PA known-certificate list — sourced
and disclosed at build time, no fabrication) and **re-validate** the shipped round's six `Valid`
manifests (`c02`, `c08`, `c09`, `w01`, `w02`, `w03`) together with adv1, holding pixels and bytes
frozen. Pre-committed interpretation:

1. **If the production signers (Truepic / Microsoft / the generator-tool credential) validate as
   trusted while adv1's `field-research` test root stays `untrusted`** → the Layer-1
   indistinguishability shown in round 2 is an **artifact of the missing trust-list configuration**,
   not a structural property. The honest finding becomes: *the shipped "no clash" was a trust-blind
   **rule** artifact that a standard trust list corrects — and once corrected, the forge adv1 is
   caught (untrusted) while genuine disclosures pass (trusted).* That is a shippable configuration
   finding, most honestly folded into instrument 014's own reading.
2. **If some production signer does NOT validate as trusted under a standard trust list** (e.g. the
   generator-tool credentials are not on common trust lists) → a **real structural finding**: even
   a properly configured deployment cannot cleanly separate a genuine disclosure from the forge for
   that class of signer. That would be a standalone result.
3. **Either way**, adv1's test root must remain `untrusted` (it chains to nothing); if it somehow
   validated, the specimen construction is void and is discarded.

This is the experiment both gauntlet critics pointed to. It is the round's ship-or-fold gate.
