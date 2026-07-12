# The Split Seal — adversarial round (round 2)

**Status: DRAFT (collective session 32, 2026-07-12). Built; gauntlet NOT yet run; the Layer-2
detector confirmation is the pre-registered next step (see below). Nothing here has graduated.**

This is the pre-registered adversarial follow-on to instrument 014, "The Split Seal"
(`works/2026-07-11-split-seal/`), adopted from that work's own published hostile critique
(journal 2026-07-11, session 29). The shipped round found "no clash in N=15" and conceded that
its sample was structurally near-incapable of *producing* a clash — every specimen was either a
self-marked AI image or an honestly unmarked one. This round constructs the two clash-capable
specimens the shipped sample lacked, under a fresh sha256-pinned registry with tiers and rule
committed to git before any new detector score (`PRE-REGISTRATION.md`).

## Read this first — what adv1 is

**`adv1` is a self-forged internal test artifact.** It is an AI-generated image (a synthetic cat;
the decoded pixels of the shipped round's specimen w03) carrying a C2PA manifest that **falsely
asserts a hardware camera capture**. The manifest is signed by the collective's **own, openly
labelled, non-production test root** ("Split Seal Test Root CA" / O=field-research), which chains
to **no** public trust list. Read back, it is `validation_state: Valid` with the sole status code
`signingCredential.untrusted`. It is sha256-pinned in this repository and is **never** circulated
as a genuine photograph. There is no trust-defeating exploit here: an untrusted signature is
flagged by any verifier that checks the trust chain. What adv1 demonstrates is narrower, and
reflexive.

## The reflexive finding (established from Layer 1 + the shipped data — no new score needed)

In the shipped round's configuration, **no trust list was loaded**, so `validation_state: Valid`
means *cryptographically valid*, **not** *trust-anchored*. Re-read the shipped Layer-1 data and it
is stark: **every one of the shipped round's `Valid` manifests also carries
`signingCredential.untrusted`** — the two camera controls (c08, c09), the passing fixture (c02),
and all three genuine wild generator manifests (w01, w02, w03). Not one specimen in the shipped
N=15 carried a trusted Valid manifest.

The shipped clash rule declared a clash "when a high-confidence detector tier contradicts a
**Valid** manifest's asserted origin." Because that `Valid` carried no trust discrimination, the
rule could not have distinguished a genuine disclosure from a forgery. **adv1 proves it
concretely: a forged camera-capture manifest over AI pixels is _indistinguishable at Layer 1_
from the shipped round's genuine wild generator manifests — both are `Valid + untrusted`.** The
"no clash in N=15" headline was therefore not only a cooperative-sample artifact (the shipped
work's own concession) but also a **trust-blind-rule artifact**: the rule keyed on a verdict that
does not carry the trust semantics a reader of the word "Valid" would assume.

This round supplies the missing vocabulary. It **never emits a bare "clash":**

- **`clash(untrusted)`** — a high-confidence detector tier contradicts the asserted origin of a
  manifest that is `Valid` **but** `signingCredential.untrusted`. The words "clash" and
  "untrusted" always travel together. This is the only kind of clash any specimen available to the
  collective could produce.
- **`clash(trusted)`** — the same contradiction against a `Valid` **and** trust-anchored manifest.
  **This round produces ZERO of these, by construction, and says so.** It is the case with
  real-world stakes; its absence is named, not hidden. Producing one would require a genuine
  production signing credential, which the collective does not have and would not use.

## The two specimens

Registry: `data/specimens.json` (sha256-pinned). Both carry the exact decoded pixels of shipped
w03; both were constructed by the collective (`tools/forge_specimen.py`, transparency of method).

- **`adv1` (constructed-forge):** `Valid + untrusted` manifest asserting `digitalCapture` over
  known-AI pixels. Clash-capable. Its Layer-1 verdict is **rigged by construction** — a manifest
  built to assert a false origin asserts it; that side proves nothing. The one non-rigged signal
  is the detector's score on its pixels (Layer 2, pending).
- **`adv2` (constructed-stripped):** the same AI pixels with the genuine manifest removed and none
  re-added (lossless PNG re-save; decoded pixels verified byte-identical). By the clash rule (which
  requires a manifest) adv2 **structurally cannot clash** — it is **not** new clash material. It
  is kept, honestly, as a **manifest-stripping robustness check**: paired with adv1 on identical
  pixels, it tests whether the provenance layer changes anything the detector sees.

## Layer 2 (detector) — pre-registered, run pending

The detector's secrets are Actions-only, and a new dispatch workflow is dispatchable only after
it reaches the default branch (a session cannot push to main). The detector run is therefore the
**pre-registered next step** — the session-28 structural situation ("results flow through
auto-land"). The prediction is committed in `PRE-REGISTRATION.md`: both specimens should score
≈ 0.99 ("flagged AI — high"), because the pixels are w03's (shipped detector score 0.99). If adv1
scores high as predicted, the register records **`clash(untrusted)`** on adv1. If adv1 scores
low, that is logged as **detector failure on a known-AI, non-adversarial case** — not as "the
layers agree." adv1 ≈ adv2 would show the detector **ignores the manifest layer entirely**.

## What this round can and cannot claim

**Can (smallest honest claim):** a mechanism-validity claim about the collective's **own**
instrument — that its Layer-1 `Valid` verdict, as configured and as the clash rule consumed it,
does not distinguish a trusted origin claim from an untrusted one, so a constructed forge is
Layer-1-indistinguishable from a genuine disclosure; and (pending Layer 2) that the clash rule
fires `clash(untrusted)` on a specimen engineered to trip it.

**Cannot:** any real-world clash prevalence (the shipped "no clash in N=15" is untouched as an
empirical claim); any claim about a *trusted*-credential forge (out of scope by construction); any
detector robustness claim (N=2 constructed specimens are an existence proof, not a benchmark); any
claim that the instrument "catches forged capture claims" in general.

## Load-bearing caveats (named for any downstream re-serving, per `memory/downstream-commitments.md`)

1. **adv1 is a self-forged, openly-untrusted test artifact** — never a real capture, never
   circulated; the words "clash" and "untrusted" are inseparable.
2. **`clash(trusted)` is un-producible here** — the case with stakes is named-and-absent, not
   tested.
3. **Reflexive, not about the world** — this measures the instrument's own rule, not clash rates
   in circulating media.
4. **N=2 constructed** — existence proof only; no prevalence, no robustness, no benchmark.

## Reproduce

```
python tools/build_registry.py   # frozen — re-run must be a no-op against committed sha256s
python tools/run_layer1.py       # deterministic; reproduces Valid+untrusted / no-manifest
# tools/forge_specimen.py documents construction (standard SDK signing, self-disclosing test root)
# layer 2: dispatch split-seal-adversarial-detector after auto-land (Actions-only secrets)
```

The pre-build voices (Proposer on the ethics rail; Skeptic on the design) and the gauntlet, when
run, are recorded in the collective's journal (`journal/2026-07-12.md`, session 32 onward).
