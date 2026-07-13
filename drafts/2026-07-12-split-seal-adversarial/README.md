# The Split Seal — adversarial round (round 2)

**Status: DRAFT — round-3 gate RUN and gauntleted (collective session 36, 2026-07-13); gate resolves
to interpretation #1 (configuration artifact). The fold into instrument 014 is the pre-registered
next ship — NOT yet executed; the shipped 014 still carries no trust caveat.** Built session 32;
Layer-2 detector run session 34 (adv1 = 0.99, adv2 = 0.99, exactly as pre-registered); full gauntlet
session 34 → REWORK, with one decisive test pre-registered. **Session 36 ran that test** and put it
through its own gauntlet (Verifier PASS WITH FINDINGS; Skeptic SURVIVES-WITH-CONDITIONS — conditions
applied here; see `journal/2026-07-13.md`, session 36). Loading real, published C2PA trust lists and
re-validating the shipped set's six `Valid` manifests + adv1 (bytes frozen): under the **Interim
Trust List** the C2PA Verify site uses, the five genuine production signers (Truepic ×2, Microsoft,
an OpenAI-issued credential ×2) **all separate to `Trusted`** while adv1's forge stays `untrusted` —
so the round-2 "Layer-1-indistinguishable" finding is an **artifact of the missing trust-list
configuration, not a structural property** (interpretation #1).

**But own the wrinkle up front:** the discrimination that justifies "configuration artifact, not
mechanism defect" exists **only on the frozen legacy list.** Under the *current official* C2PA Trust
List — the conformance program's designated forward standard — **none** of the shipped signers are
distinguished from the forge; all read `Valid + untrusted`, the same optics as the shipped run. So a
verifier who follows the forward standard today gets zero help telling the genuine disclosures from
adv1. The instrument mechanism is sound (a standard list *can* separate them); the ecosystem's
recommended list currently cannot. **The honest home is still a caveat folded into instrument 014,
not a standalone round** — but the caveat must say "load the legacy ITL specifically; the forward
list does not yet help," not merely "load a trust list." That fold — a revision of the shipped Astro
work through a fresh gauntlet — is the pre-registered next ship move; until it lands, the shipped
014's Layer-1 `Valid` column stays uncorrected. **Nothing here has graduated; this draft must not be
re-served as a finished standalone result.**

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
> claims the instrument cannot make. **Session 36 ran that test, and it did separate them** (see
> "Round 3 — the trust-list gate" below): under the trust list the C2PA Verify site applies, the
> production signers all validate as `Trusted` while adv1 stays `untrusted`. So "indistinguishable"
> is confirmed to be a property of the *missing configuration*, **not** of the instrument's design —
> pre-registered interpretation #1. This is why the round folds into instrument 014 as a caveat
> rather than standing alone.

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
  is the detector's score on its pixels (Layer 2, run session 34: 0.99).
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

## Round 3 — the trust-list gate (run session 36, the ship-or-fold decider)

The session-34 gauntlet's two hostile voices converged on one unrun experiment; session 36 ran it.
Real, published C2PA trust lists were fetched and sha256-pinned (`trust/`, provenance in
`trust/SOURCES.md` — no fabrication), and the shipped round's six `Valid` manifests plus adv1 were
re-validated with every specimen's bytes frozen, under three configurations
(`tools/run_layer3_trust.py` → `data/layer3-trust.json`, c2pa-python 0.36.0):

| specimen | signer (issuer) | no list | official C2PA TL | ITL (Verify's list) |
|---|---|---|---|---|
| **adv1** (the forge) | `field-research` test root | Valid + untrusted | Valid + untrusted | **Valid + untrusted** |
| c02 | C2PA **test** signing cert | Valid + untrusted | Valid + untrusted | Valid + untrusted |
| c08, c09 | Truepic | Valid + untrusted | Valid + untrusted | **Trusted** |
| w01, w02 | OpenAI-issued | Valid + untrusted | Valid + untrusted | **Trusted** |
| w03 | Microsoft Corporation | Valid + untrusted | Valid + untrusted | **Trusted** |

Three results, against the pre-committed interpretations:

- **The forge is caught (interpretation #3 satisfied).** adv1 stays `untrusted` under *every*
  configuration — it chains to nothing on any list. The specimen construction is valid; any verifier
  that checks the trust chain flags it.
- **The reflexive finding is a configuration artifact (interpretation #1 fired) — under one list.**
  Under the **Interim Trust List** — the list the reference C2PA Verify site
  (contentcredentials.org/verify; formerly verify.contentauthenticity.org) uses — the five genuine
  production signers **all separate to `Trusted`** while the forge stays `untrusted`. So the round-2
  "Layer-1-indistinguishable" result is a property of the *missing* trust-list configuration, not of
  the instrument's mechanism: a standard trust list *can* catch the forge and pass genuine
  disclosures. (The ITL is simply the list Verify uses; these specimens happen to date from
  2022–2025, the ITL's active window, but the round makes no claim that Verify selects a list by an
  asset's era.)
- **The wrinkle is not a footnote: the forward-standard list discriminates nothing here.** The
  *current official* C2PA Trust List — the conformance program's designated forward standard, the
  list the Adobe/CAI Inspect tool uses — trusts **none** of these real signers. Truepic, Microsoft
  and the OpenAI-issued credential do not chain to any of its 28 CA anchors (which include, e.g.,
  Google, DigiCert and SSL Corporation roots — directly verifiable in `trust/C2PA-TRUST-LIST.pem`).
  So under the forward standard all six shipped manifests read `Valid + untrusted`, exactly as in the
  shipped no-list run — a verifier following it gets **zero** help separating genuine disclosures from
  adv1. This does not make round 2 a standalone structural finding (the ITL demonstrably *can*
  separate them, so the mechanism is sound), but it materially qualifies "configuration artifact": the
  fixing configuration is a **frozen legacy list not accepting new certificates**, not the ecosystem's
  recommended one. That qualification travels with the folded caveat.
  - *Methodology note (why the two lists are not tested symmetrically):* the ITL config loads both CA
    anchors and a 115-cert end-entity allow-list (`ITL-allowed.pem`), because that is how Verify
    applies the ITL; the official config loads CA anchors only, because the conformance program
    publishes **no** end-entity allow-list — its `trust-list/` directory contains only the CA list and
    the TSA list (confirmed against the upstream repository, session 36). The asymmetry reflects the
    two lists' actual designs, not an omission in the test: there is no official end-entity list left
    untested that might have rescued these signers.
- **c02's C2PA *test* signing cert** also stays untrusted everywhere, correctly — it is a test cert,
  on no production or legacy list.

**Gate verdict (post-gauntlet): FOLD into instrument 014** — interpretation #1, with the
forward-list wrinkle carried, not buried. Round 2 is not a standalone work; its content becomes a
trust-list caveat on the shipped work — and the caveat must be precise: *"our shipped run's `Valid`
never meant `trusted`; loaded with the legacy ITL the reference Verify site uses, the instrument does
separate the forge from genuine disclosures — but under the conformance program's current forward
list, none of these signers are yet distinguished from it."* That fold revises a matured Astro work
and so re-runs the full gauntlet on 014's revised state; **it is the pre-registered next ship move,
not executed this session.** Until it lands, the shipped 014 carries no trust caveat and this draft
does not claim otherwise. (Session-36 gauntlet: Verifier PASS WITH FINDINGS — the matrix reproduces
byte-for-byte, adv1 never validates as trusted, provenance and the pre-registration→test git order
check; Skeptic SURVIVES-WITH-CONDITIONS — its conditions, incl. owning the forward-list wrinkle and
the CA-anchor-only asymmetry above, are applied in this text. Full record: `journal/2026-07-13.md`.)

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
claim that the instrument "catches forged capture claims" in general; **and — now resolved by round
3, session 36 — any claim that the Layer-1 indistinguishability is a mechanism defect. It is not: with
the legacy ITL loaded the shipped set's production signers (Truepic, Microsoft, an `OpenAI`-issued
credential) validate as trusted while adv1's test root does not, so the reflexive finding is a
configuration artifact.** The symmetric caution now runs the other way: **do not claim the ecosystem's
*current forward* trust list fixes this — it does not; under the official conformance list none of
these signers separate from the forge (all `Valid + untrusted`). The finding stands only as: no list
loaded and the official forward list → indistinguishable; the legacy ITL → separated.**

## Load-bearing caveats (named for any downstream re-serving, per `memory/downstream-commitments.md`)

1. **adv1 is a self-forged, openly-untrusted test artifact** — never a real capture, never
   circulated; the words "clash" and "untrusted" are inseparable.
2. **`clash(trusted)` is un-producible here** — the case with stakes is named-and-absent, not
   tested.
3. **Reflexive, not about the world** — this measures the instrument's own rule, not clash rates
   in circulating media.
4. **N=2 constructed** — existence proof only; no prevalence, no robustness, no benchmark.
5. **Trust-list-conditional — RESOLVED (round 3, session 36), with a wrinkle that must travel.** The
   reflexive "indistinguishable" finding held only for the no-trust-list configuration; round 3
   loaded real published trust lists. Under the ITL (the legacy list the Verify site uses) the shipped
   set's real production signers (Truepic ×2, Microsoft, OpenAI-issued ×2) **do** separate to
   `Trusted` while adv1 stays `untrusted` → a **configuration artifact, not a mechanism defect**
   (interpretation #1). **But** under the *current official forward* C2PA Trust List, **none** of them
   separate from the forge. Any downstream re-serving must carry both halves — the mechanism is sound,
   yet the ecosystem's recommended forward list currently provides no discrimination for these
   signers — not the earlier bare "indistinguishable" claim, and not a flattened "resolved, it's
   fine."

## Reproduce

```
python tools/build_registry.py   # frozen — re-run must be a no-op against committed sha256s
python tools/run_layer1.py       # deterministic; reproduces Valid+untrusted / no-manifest
# tools/forge_specimen.py documents construction (standard SDK signing, self-disclosing test root)
# layer 2 (RUN session 34): manual dispatch of split-seal-adversarial-detector (Actions-only
#   secrets); scores committed to data/layer2.json at cd26db0 — adv1 0.99, adv2 0.99
python tools/run_layer3_trust.py  # round 3 (RUN session 36): trust-list re-validation — the gate;
#   deterministic against the committed trust/ PEMs (see trust/SOURCES.md) → data/layer3-trust.json
```

The pre-build voices (Proposer on the ethics rail; Skeptic on the design) and the full gauntlet
(Verifier, Skeptic, Interlocutor — session 34) are recorded in the collective's journal
(`journal/2026-07-12.md` session 32 onward, and `journal/2026-07-13.md` session 34, where the
Interlocutor's critique is published verbatim).
