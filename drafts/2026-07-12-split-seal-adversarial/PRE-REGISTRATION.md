# Pre-registration — The Split Seal, adversarial round (round 2)

**This file is committed to git BEFORE any Layer-2 (detector) score for the two constructed
specimens is seen.** The git history is the timestamp; the credibility of everything downstream
rests on that order (the shipped round proved the method: tiers-before-scores, `ec84146` →
`902332d`). If a later commit shows a detector score whose parent commit does not already contain
this file, the pre-registration is void.

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
