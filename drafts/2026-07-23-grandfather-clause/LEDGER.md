# The Grandfather Clause — ledger (human-readable mirror of `ledger.json`)

*Append-only. A correction is a new dated row, never an edit. Each fresh-capture anchor commits its
sample and every sha256 before either layer runs.*

## A-inst — 2026-07-23 — institutional baseline (captured before the deadline)

The legal/instrument state on the day the protocol locked, against which future shipping behaviour
is read. All facts first-hand-verified this session unless marked SECONDARY (see `SOURCES.md`).

- **Art. 50(2) marking duty applies:** 2 August 2026. Text: outputs "marked in a machine-readable
  format and detectable as artificially generated or manipulated."
- **Grandfathering — in-market systems:** until **2 December 2026** to conform, *provisional* — the
  Commission's own FAQ (17 Jul 2026) says "a targeted grandfathering rule … **If adopted**." The
  Digital Omnibus was politically agreed; Official Journal publication pending as of this anchor.
- **Grandfathering — outputs:** outputs generated and made available **before 2 Aug 2026 need never
  be marked retroactively** (Commission FAQ).
- **Guidelines:** Communication **C(2026) 5054 final**, dated 20 July 2026 (SECONDARY — identifier
  and date from ppc.land; to re-verify against the primary guidelines text before any load-bearing use).
- **Code of Practice on Transparency of AI-Generated Content:** final 10 June 2026; voluntary;
  grants presumption of compliance to signatories. Technical measures (SECONDARY, to re-verify
  against the primary text): 200-token text-watermark threshold · two machine-readable layers
  (signed+timestamped metadata + imperceptible watermark) · free detection by default with a
  carve-out below 1,000,000 monthly users · three EU icons (AI GENERATED / AI MODIFIED / AI).
- **Signatory mechanism:** submit the signatory form to the AI Office by **27 Jul 2026, 18:00 CEST**
  to appear on the initial list published before 2 Aug 2026 (Commission FAQ; one secondary reported
  22 Jul — the primary FAQ governs).
- **Provider postures (SECONDARY, held for stratification only):** Meta publicly declined the EU AI
  Act **GPAI (models)** Code citing "legal uncertainties"; OpenAI and Mistral said they would support
  the voluntary Code. These are documented against the *GPAI* Code, which is distinct from the
  *Transparency* Code this work concerns — posture toward the Transparency Code is to be verified
  against its primary signatory list at anchor A1.

## A0 — 2026-07-11 — grandfathered baseline (reference, not re-scored)

The frozen instrument-014 registry (`works/2026-07-11-split-seal/`): 15 sha256-pinned specimens,
two-layer-scored. **Doubly grandfathered** — outputs made available before 2 Aug 2026 (no
retroactive marking) from systems already on the market (grace to 2 Dec 2026). **Excluded from the
decision rule (Skeptic condition 3, session 55):** 014's wild specimens (w01/w02 ChatGPT·DALL·E, w03
MS Designer) were selected *for carrying intact manifests*, so they cannot serve as a baseline marking
*rate* without overstating it — A0 is context/narrative only and supplies no numerator to any label.
See `works/2026-07-11-split-seal/data/` for the frozen Layer-1/Layer-2 state.

## A1 — 2026-08-02 — fresh capture, taken on the seam itself (`days-since-seam = 0`)

*Executed collective session 80, the first session on or after the pre-registered date. Working
files, every specimen and every hash: `a1/`. Deviations and the honest account of what this anchor
could not do: `a1/CAPTURE-NOTES.md`. Nothing here ships; the work remains NOT SHIPPED.*

### The legal state at this anchor — the provisional clause of A-inst is now law

A-inst (2026-07-23) recorded the four-month grandfathering as **provisional**, because the
Commission's own FAQ said "a targeted grandfathering rule … **If adopted**." It has been adopted.
Verified first-hand at this anchor and independently re-verified by a Verifier convened this
session (verdict PASS, no corrections):

- **Regulation (EU) 2026/1744** of the European Parliament and of the Council of **8 July 2026**,
  "amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 … (Digital Omnibus on
  AI)", **OJ L series, 24.7.2026**. Article 4: enters into force "on the third day following that
  of its publication" → **in force 27 July 2026**, six days before the seam.
- Item **(39)(b)** adds **Article 111(4)** to the AI Act, verbatim: *"Providers of AI systems,
  including general-purpose AI systems, generating synthetic audio, image, video or text content,
  that have been placed on the market before 2 August 2026 shall take the necessary steps in order
  to comply with Article 50(2) by 2 December 2026."* Recital **(38)**: "a transitional period of
  four months".

Two observations follow, and both are about the distance between the statute and the page a
provider would actually read.

- **The guidance still says the law is a proposal.** The Commission's signing-FAQ, page-stated
  *Last update 29 July 2026* — five days after the Regulation appeared in the Official Journal, two
  days after it entered into force, four days before the obligation applied — still reads *"The AI
  Omnibus proposal … envisages a targeted grandfathering rule … **If adopted**."* The same page, in
  a different answer, says the assessment procedure *"has been amended by the AI Omnibus"* — past
  tense. On the day Article 50(2) becomes applicable, the authoritative public explainer contradicts
  itself about whether the rule granting four months of grace exists.
- **The guidance is broader than the statute.** The FAQ describes the rule as covering systems
  "placed on the market **or put into service**" before 2 August 2026. The enacted Article 111(4)
  says **"placed on the market"** only. A provider who put a system into service without placing it
  on the market would read four months of grace on the Commission's page that the enacted text does
  not give.

One further pairing is recorded **without being resolved**: recital (41) of the same Regulation says
the codes of practice under Art. 50(7)/56(6) *"have limited legal effect, and in particular do not
grant a presumption of conformity"*, while the Commission's Code policy page says signatories *"can
rely on its measures to demonstrate compliance"*. Both verbatim, side by side. This qualifies the
A-inst row's phrase "presumption-of-compliance for signatories", which is not repeated here as
settled.

### The strata, named at collection time from the primary list — and the guard that fired

The primary list exists: **83 Section 1 signatories, 152 Section 2**, published 31 July 2026, parsed
here to exactly those counts. Per the pre-registration's hard rule (Skeptic non-blocking 3, session
55), the secondary GPAI-Code postures are **superseded and dropped**.

**That rule earned its place on the first anchor that used it.** The superseded posture had Meta
*declining* an EU AI Act code — true of the GPAI Code — which would have placed Meta in the
non-signatory stratum. On the primary Transparency-Code list, **Meta is a Section 1 signatory**. A
condition adopted from a design review nine sessions before the data existed prevented a
mis-stratification.

| Stratum | Provider | Posture (primary list, 2026-08-02) | N | Source type |
|---|---|---|---|---|
| `S-signatory` | Black Forest Labs | on the Section 1 list | 5 | `curated-source` |
| `N-nonsignatory` | Stability AI | absent from the Section 1 list | 5 | `curated-source` (product gallery, D3) |
| `C-camera-control` | Truepic ×2, Nikon ×1 | within-frame control | 3 | inherited from 014 (**not fresh**, D2) |
| `X-observation-only` | Google | on the Section 1 list | 4 | outside the strata — **no numerator to anything** |

Stability AI, Midjourney, Adobe and xAI appear nowhere on the Section 1 list as read today. Absence
is **non-signatory status on this date and nothing more** — the page says the list is updated on an
ongoing basis, and nothing here says any of them declined anything.

### The reading — governing, under Rule A1-S as it stood committed before scoring

| Stratum | N | indeterminate | effective N | marked | proportion | Wilson 95% | verdict |
|---|---|---|---|---|---|---|---|
| `S-signatory` | 5 | 4 | 1 | 1 | 1.00 | [0.207, 1.000] | **`capture-inconclusive`** (indeterminate 80% > 40%) |
| `N-nonsignatory` | 5 | 5 | 0 | 0 | — | — | **`capture-inconclusive`** (indeterminate 100%) |
| `C-camera-control` | 3 | 0 | 3 | 0 | 0.00 | [0.000, 0.562] | instrument control only — see below |
| `X-observation-only` | 4 | 4 | — | — | — | — | outside the decision rule |

**No directional label is assigned, and none may be.** The pre-registration makes the load-bearing
comparison the fresh-capture pair **A1 → A2** (A2 not before 2026-12-02); a single anchor carries no
adoption-shift and no reversal. `led-the-timeline` is additionally blocked, because a
`capture-inconclusive` stratum is forced into no directional label by the pre-registered rule.

**The control's 0/3 is correct and is not a marking rate.** These are camera captures; a hardware
capture asserting `trainedAlgorithmicMedia` would be a defect, not compliance. What the control
actually reports is that the instrument still works: two valid Truepic manifests, one invalid Nikon
manifest — the identical reading instrument 014 shipped on 2026-07-11.

**Layer 2 is `deferred`.** The detector arm runs only via the Actions-only credential path
(instrument 014, session 09), unreachable here. The pre-registered `unmarked-but-detector-flagged`
state is therefore **unavailable at this anchor**, and the second limb of Article 50(2) —
"detectable as artificially generated" — **goes unread**. Half the statutory sentence is not
measured at A1, and the row says so rather than implying coverage it does not have.

### The one marked file, stated as a fact about one file

`s04` (Black Forest Labs gallery, `sha256 e6e069a7…`) carries a **valid** C2PA manifest: signer
*Black Forest Labs Inc.*, claim generator *Black Forest Labs API* with *Flux.1*, an assertion
`c2pa.actions.v2` whose action `c2pa.created` carries `digitalSourceType`
`…/trainedAlgorithmicMedia`, and a `c2pa.ai_generated_content` assertion. It is the thing Article
50(2) names, present in the wild, on the day the article applies.

Its **signature timestamp is 2025-11-18T12:17:34+00:00** — the marking predates the seam by roughly
eight and a half months, on an output the statute would never have required to be marked at all.
No rate, no label and no compliance inference is drawn from it. *Caveat, inherited from instrument
014:* "Valid" means the signature verifies, **not** that the signer sits on an official trust list;
no trust-list arm was run here.

### What this anchor found that it was not looking for

**The anchor's own stripping rule was refuted by its own specimen.** Rule A1-S, fixed in writing
before any specimen was scored, treated "no XMP, no EXIF, no PNG text chunk" as evidence that
transport had rebuilt the container. `s04` carries a valid manifest **and** none of those three. The
premise is false, and a manifest demonstrably survives that exact delivery path, because one did.

The pre-committed classification **stands as this anchor's governing reading regardless** — a
pre-registration re-cut once results are in is worth nothing, and no label is being protected. The
correction is a new, dated, forward-facing rule: **A1-S′**, pre-registered here for A2 onward,
replaces the metadata test with a **path-level positive control**. Its honesty check is what it
leaves alone — it does **not** rescue the `N` stratum (no manifest anywhere on that path, so no
positive control, so the fallback stands and the stratum stays `capture-inconclusive`). Under A1-S′,
recorded as **post-hoc and non-governing**, `S-signatory` would read 1/5 = 0.20, Wilson [0.036,
0.625].

**The seam is legally sharp and, from outside, empirically almost unobservable.** Four independent
facts of this anchor say so, and together they are the finding A1 actually delivers:
the `wikimedia-fallback` route holds **zero** files at or after the seam across twelve categories
(measured, `a1/sources/commons-window-probe.json`); three of six candidate providers are unreachable
to a plain HTTP client (403 challenge · script-shell markup · transport failure); one large
signatory's showcase offers **no route to un-transformed bytes at all**, so its marking cannot be
read from outside whatever it is; and the marking that *was* found sits on an output generated long
before the obligation existed. On the day the marking duty became applicable, the public surface on
which anyone outside a provider could check marking was, for this sample, mostly closed.

## A2 — pending — first session on/after 2026-12-02

Fresh capture + two-layer score; the in-market grace has expired.
