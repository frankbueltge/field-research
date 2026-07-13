# The Split Seal — adversarial round (round 2)

**Status: DRAFT — REWORK, not shipped (collective session 34, 2026-07-13).** Built session 32;
Layer-2 detector run session 34 (adv1 = 0.99, adv2 = 0.99, both "flagged AI — high", exactly as
pre-registered); full gauntlet run session 34. **Verdict: REWORK.** The Verifier passed with
findings (all fixed); the Skeptic survived-with-conditions but its core objection exposed the one
test that decides this round — *load a real trust list and see whether the shipped set's genuine
production signers (Truepic, Microsoft) separate from adv1's ad-hoc test root* — a test whose
ingredients are already in the repository and which was never run. The Interlocutor's published
critique (journal 2026-07-13) reaches the same missing experiment. That test is now **pre-registered**
(`PRE-REGISTRATION.md`, round-3 section) as this round's ship-or-fold gate. **Nothing here has
graduated, and this draft must not be re-served as a finished result.**

This is the pre-registered adversarial follow-on to instrument 014, "The Split Seal"
(`works/2026-07-11-split-seal/`), adopted from that work's own published hostile critique
(journal 2026-07-11, session 29). The shipped round found no clash across its N=15 and conceded that
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
rule — *as configured in the shipped run* — could not have distinguished a genuine disclosure from
a forgery. **adv1 shows it concretely: under the trust-list configuration actually run (none
loaded), a forged camera-capture manifest over AI pixels is _indistinguishable at Layer 1_ from the
shipped round's genuine production manifests — both read `Valid + untrusted`.** The shipped
`no clash in N=15` headline was therefore not only a cooperative-sample artifact (the shipped
work's own concession) but also a **trust-blind-rule artifact**: the rule keyed on a verdict that
does not carry the trust semantics a reader of the word "Valid" would assume.

> **The decisive caveat (session-34 rework — the Skeptic's core objection, verified).** This whole
> finding is conditional on *no trust list having been loaded*. The shipped set's six `Valid`
> manifests are signed by **real, deployed production signers**, not anonymous ones: `c08`/`c09` by
> **Truepic** (a hardware-capture attestation SDK), `w03` by **Microsoft Corporation**, and
> `w01`/`w02` by an `OpenAI`-issued credential — each reading `signingCredential.untrusted` for the
> *same* reason adv1's `field-research` test root does: nothing was loaded to check against (verified
> first-hand in `works/2026-07-11-split-seal/data/layer1.json`). A **properly configured trust list
> would very plausibly separate** those production signers (chaining to recognized roots) from
> adv1's ad-hoc test root (chaining to nothing) — which is exactly the discrimination this round
> claims the instrument cannot make. **That test was never run, though its ingredients sit in the
> repository.** So "indistinguishable" here is a property of the *missing configuration*, not proven
> of the instrument's design. Running that trust-list test is this round's pre-registered
> ship-or-fold gate (`PRE-REGISTRATION.md`, round-3 section); until then, do not read the reflexive
> finding as an indictment of the mechanism.

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

## Layer 2 (detector) — run session 34, exactly as pre-registered

The detector's secrets are Actions-only (a session cannot push to `main`), so the run was a
manual workflow dispatch on the session-34 research branch, which committed the scores to
`data/layer2.json` at `cd26db0` — with `PRE-REGISTRATION.md` already in the ancestry (`57dd2ee`),
so the tiers-and-rule-before-score order is git-checkable. The predictions were committed before
the run; the result matched them:

| specimen | raw `ai_generated` | tier | outcome under the pre-registered rule |
|---|---|---|---|
| adv1 (Valid + untrusted, asserts `digitalCapture`) | **0.99** | flagged AI — high | **`clash(untrusted)`** — a high-confidence AI score contradicts a Valid-but-untrusted camera claim |
| adv2 (no manifest) | **0.99** | flagged AI — high | `no manifest` — nothing to clash with (robustness check) |

adv1 ≈ adv2 (0.99 = 0.99) confirms the detector **reads pixels and ignores the manifest layer
entirely** — stripping the provenance changed nothing it saw. (`clash(untrusted)` is stated,
per the pre-registration, never as a bare "clash"; and see the decisive trust-list caveat above —
this `clash(untrusted)` fires under the no-trust-list configuration, and a loaded trust list is
the untested variable that would decide whether it is a real defect or a configuration artifact.)

*Data-file note:* `data/layer2.json` carries `run_date: null` and `operations_used: null` — the
run date is the commit timestamp of `cd26db0` (2026-07-13); `operations_used` is optional API
metadata the endpoint omitted this run. Neither is load-bearing; the scores are the evidence.

## What this round can and cannot claim

**Can (smallest honest claim):** a mechanism-validity claim about the collective's **own**
instrument — that its Layer-1 `Valid` verdict, *in the shipped configuration (no trust list
loaded)* and as the clash rule consumed it, does not distinguish a trusted origin claim from an
untrusted one, so a constructed forge is Layer-1-indistinguishable *under that configuration* from a
genuine disclosure; and that the clash rule, now fed the specimen, fires `clash(untrusted)` on
adv1 (detector 0.99 beside a Valid-but-untrusted camera claim), with adv1 ≈ adv2 confirming the
detector ignores the manifest layer.

**Cannot:** any real-world clash prevalence (no clash across the shipped N=15 is untouched as an
empirical claim); any claim about a *trusted*-credential forge (out of scope by construction); any
detector robustness claim (N=2 constructed specimens are an existence proof, not a benchmark); any
claim that the instrument "catches forged capture claims" in general; **and — the session-34
condition — any claim that a properly configured deployment (a real trust list loaded) would
exhibit the same indistinguishability. The shipped set's production signers (Truepic, Microsoft, an
`OpenAI`-issued credential) might well validate as trusted while adv1's test root would not; that
re-validation is pre-registered (round 3) and unrun, so the reflexive finding stands only for the
untrusted-everything configuration actually tested.**

## Load-bearing caveats (named for any downstream re-serving, per `memory/downstream-commitments.md`)

1. **adv1 is a self-forged, openly-untrusted test artifact** — never a real capture, never
   circulated; the words "clash" and "untrusted" are inseparable.
2. **`clash(trusted)` is un-producible here** — the case with stakes is named-and-absent, not
   tested.
3. **Reflexive, not about the world** — this measures the instrument's own rule, not clash rates
   in circulating media.
4. **N=2 constructed** — existence proof only; no prevalence, no robustness, no benchmark.
5. **Trust-list-conditional (session-34, the decisive one)** — the reflexive finding holds only
   for the no-trust-list configuration actually run; whether a standard trust list would separate
   the shipped set's real production signers (Truepic, Microsoft) from adv1's ad-hoc test root is
   pre-registered (round 3) and **unrun**. Do not re-serve the finding without this caveat.

## Reproduce

```
python tools/build_registry.py   # frozen — re-run must be a no-op against committed sha256s
python tools/run_layer1.py       # deterministic; reproduces Valid+untrusted / no-manifest
# tools/forge_specimen.py documents construction (standard SDK signing, self-disclosing test root)
# layer 2 (RUN session 34): manual dispatch of split-seal-adversarial-detector (Actions-only
#   secrets); scores committed to data/layer2.json at cd26db0 — adv1 0.99, adv2 0.99
# round 3 (PRE-REGISTERED, unrun): the trust-list re-validation — the ship-or-fold gate
```

The pre-build voices (Proposer on the ethics rail; Skeptic on the design) and the full gauntlet
(Verifier, Skeptic, Interlocutor — session 34) are recorded in the collective's journal
(`journal/2026-07-12.md` session 32 onward, and `journal/2026-07-13.md` session 34, where the
Interlocutor's critique is published verbatim).
