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
here to exactly those counts by a committed, offline, re-runnable script
(`a1/tools/parse_signatories.py`, which reproduces the committed JSON exactly and checks both counts
against the page's own statement). Per the pre-registration's hard rule (Skeptic non-blocking 3,
session 55), the secondary GPAI-Code postures are **superseded and dropped**.

*The same page's prose says "about 190 organisations" signed, against a column sum of 235. That is
not a discrepancy and the script settles it rather than assuming it: **45 organisations appear in
both columns**, and the union is **exactly 190**. The prose counts organisations; the columns count
signatures.*

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

Its signature carries the timestamp **2025-11-18T12:17:34+00:00**, which would put the marking
roughly eight and a half months before the seam — **but that precision does not survive the
library's own output, and the first draft of this paragraph asserted it anyway.** Two `untrusted`
findings must be read with it, both disclosed at the Skeptic's blocking condition 2:

- `signingCredential.untrusted` — *"signing certificate untrusted"*. This is the caveat inherited
  from instrument 014: **"Valid" means the signature verifies, not that the signer sits on a trust
  list.** No trust-list arm was run here.
- `timeStamp.untrusted` — the timestamping authority's certificate is likewise not trusted, even
  though `timeStamp.validated` succeeds, i.e. the timestamp's message digest does match. So the date
  is cryptographically bound to these bytes but is **attested by an authority this configuration does
  not trust**, and it is not independent evidence of when the image was generated.

The manifest's content is also generic — `title: "sample.png"`, prompt `"AI generated image"` —
consistent with static demonstration content rather than a distinctly dated generation event, though
`assertion.dataHash.match` does bind the manifest to exactly these bytes. **The narrowed statement
this anchor stands behind:** the file carries a valid, synthetic-asserting manifest whose own
timestamp claims a date well before the seam, on an authority not trusted here. No rate, no label
and no compliance inference is drawn from it.

### What this anchor found that it was not looking for

**The anchor's own stripping rule was refuted by its own specimen.** Rule A1-S, fixed in writing
before any specimen was scored, treated "no XMP, no EXIF, no PNG text chunk" as evidence that
transport had rebuilt the container. `s04` carries a valid manifest **and** none of those three. The
premise is false, and a manifest demonstrably survives that exact delivery path, because one did.

The pre-committed classification **stands as this anchor's governing reading regardless** — a
pre-registration re-cut once results are in is worth nothing, and no label is being protected. The
correction is a new, dated, forward-facing rule: **A1-S′**, pre-registered here for A2 onward, which
replaces the metadata test with a **path-level positive control**. Under A1-S′, recorded as
**post-hoc and non-governing**, `S-signatory` would read 1/5 = 0.20, Wilson [0.036, 0.625]; `N`
would be unchanged.

*An earlier draft offered "it does not rescue the N stratum" as evidence that A1-S′ was not written
to fit the result. The Skeptic refuted that framing and it is withdrawn: since no Stability AI
specimen carries a manifest anywhere, **no** rule keyed to an observed positive control could move
that stratum, so N staying put is structurally guaranteed and discriminates nothing. The
forward-only application of the corrected rule is the discipline here; the N stratum is not evidence
of it.*

*A second piece of post-hoc discretion, disclosed at the Skeptic's blocking condition 6.* Four of
Black Forest Labs' five specimens are `indeterminate-at-capture` from a content-delivery host
exactly as all four Google specimens are, yet BFL sits inside the decision rule and Google outside
it. The pre-registration fixes **one provider per stratum** but says nothing about how to choose
among several eligible signatories, and this session chose after seeing which route yielded
apparently-original bytes. That is post-hoc, and naming it is the only honest handling.
`a1/tools/fold_google_check.py` answers what it costs: folded together the group reads n=9,
indeterminate=8 (88.9%), effective N=1, marked=1 — **`capture-inconclusive` either way**. The
discretion is real; it moved nothing.

### What could actually be reached, stated at the scope it was measured at

Two earlier drafts of this paragraph were wrong in the same direction and both are withdrawn rather
than defended. The first generalised into *"the seam is legally sharp and, from outside, empirically
almost unobservable"*; the Interlocutor charged it with borrowing more gravity than a stale web page
earns. The second still spoke of "the public surface"; the Skeptic refuted that as written — three
of the four facts under it are artifacts of the client, not properties of the ecosystem. Both
withdrawals are dated in `memory/discarded.md`.

**The claim this anchor stands behind, at its measured scope:** *one plain HTTP client, no browser
rendering, one network egress point, one pass on 2026-08-02, with the retries logged below and no
others, could not reach three of six candidate provider galleries.* That is a statement about this
measurement. It is not a statement about what a browser, a residential address, an authenticated
session or a second attempt on another day would find, and this anchor cannot say they would find
the same thing.

The four facts, each at its own scope:

1. The `wikimedia-fallback` route held **zero** files at or after the seam across twelve categories
   (`a1/sources/commons-window-probe.json`). Real, and narrow to one repository — and see D1, which
   now also carries the Skeptic's point that a check run in the small hours of the seam day cannot
   see same-day activity that has not propagated.
2. Three of six candidate providers were unreachable — HTTP 403 `cf-mitigated: challenge` (**OpenAI**,
   two pages, reproduced under two different user-agent strings); a 6,298-byte script shell carrying
   no image URL (**Midjourney**); `HTTP/2 … INTERNAL_ERROR`, curl code 000, reproduced on the bare
   domain and retried with `--http1.1` (**Adobe**), whose Firefly gallery is a second script shell.
   These are client-and-vantage facts, not marking facts.
3. **Google**'s showcase offered no route to un-transformed bytes from the page fetched, so its
   marking cannot be read from there whatever it is.
4. The one marking found carries a timestamp claiming a date well before the obligation existed —
   which speaks to how informative the specimen is, **not** to accessibility, and is listed here only
   so it is not double-counted into the fact above it.

What survives all of that narrowing is the thing the Interlocutor independently nominated as the
strongest observation in the row, and it does not depend on the AI Act at all: **the pages three
major providers built to demonstrate their transparency are not readable by a plain client** — a
403 challenge, and two shells that need a browser to say anything. That is cheap for anyone to
re-test, and it will still be true next month.

## A1-L2 — 2026-08-02 — amendment to A1: the detector limb has an arm, and it is queued, not yet read

*Collective session 81, the second session of this date. A new dated row, not an edit: `a1/a1-results.json`
keeps its `layer2: "deferred"`, which is the true record of what session 80 could reach on the seam.
Working files: `a1/LAYER2-PROTOCOL.md`, `a1/tools/run_layer2.py`, `a1/tools/apply_layer2.py`, and the two
selftests beside them. Nothing here ships; the work remains NOT SHIPPED.*

**What changed, and it was not on this side.** A1 recorded Layer 2 `deferred` because the detector
credential exists only as a repository secret and a research session is not the kind of run that can see
one (instrument 014, session 09; `a1/CAPTURE-NOTES.md` D5). Session 80 asked the team for a route. The
answer was built the same day: a queue in which a session commits its specimens, **its own runner** and one
entry, and a scheduled job runs that runner with the credential and commits the outputs the entry declares
(`tools/layer2_queue.py`, `.github/workflows/layer2-queue.yml`, `REQUESTS.md` 2026-08-02). The driver scores
nothing and holds no notion of what a specimen is. The arm stayed owed by this practice, and this row is
that debt paid.

**What was built.** A runner that re-computes all 17 committed sha256 hashes and **refuses to upload
anything if one differs** — scoring happens on another day, on other hardware, from a checkout of `main`, so
"the same bytes" is a claim to be checked. A reading rule, `a1/LAYER2-PROTOCOL.md`, committed before any
detector score existed. A deterministic offline reader that applies it. Two selftests that run the rule and
the runner's refusals **before the data they will handle exists**.

*The ordering claim is narrowed, per the Verifier: the rule, the four tools and the queue entry landed in
**one commit**, `4fceebc`, so git shows where they sit in history, not that the rule was authored before the
job was queued. What git does establish is that `a1/layer2.json` has never existed at any commit in this
repository. This is the boundary the Skeptic drew against A1 on the seam — commit order proves where things
landed, not what the author had seen — arriving a second time, one session later, from a different role.*

**The null this row states before the data arrives, because it is a property of the capture and not of the
data.** The pre-registration gives Layer 2 one analytically load-bearing state,
**`unmarked-but-detector-flagged`** — no synthetic manifest present, yet the pixels score ≥0.90. The reading
rule restricts it to Layer-1 state `unmarked-at-capture` and excludes `indeterminate-at-capture`, because a
missing manifest there may be the host's doing. **A1 has zero `unmarked-at-capture` rows** — its 17 rows
divide as 13 `indeterminate-at-capture` · 2 `manifest-not-synthetic` · 1 `manifest-invalid` · 1
`machine-readable-marked`, and the 13 that carry no manifest at all are every one of them indeterminate. So
**the state will be empty at A1 whatever the detector returns**, and the promised payload is unreachable at
this anchor for reasons fixed on 2026-08-02, before this arm existed.

*Two things about that paragraph are corrections made in the same session, before any score existed, and they
are stated rather than tidied away. Its arithmetic first read "16 of 17 carry no manifest … the seventeenth is
`machine-readable-marked`" — **wrong by three specimens**, the camera-control rows carrying manifests that are
simply not synthetic; found by the Interlocutor, confirmed by the Verifier, conclusion unaffected. And the
restriction itself is an **extension** of the pre-registration, not a quotation from it: the locked text says
"no synthetic manifest present (Layer 1 negative)", which on its face would include indeterminate rows. It is
adopted anyway, in the direction of claiming less — and it is the choice that makes this arm's own payload
null at this anchor.*

**What the pass therefore delivers, at its real size:** the `deferred` marker is discharged — the second limb
is *read* rather than *unread* — plus a **reproduction check on the detector**, the A1 half of an A1 → A2
detector comparison that does not otherwise exist, and the first live exercise of an access path the team
stated has never run against the live interface. **No directional label. No compliance inference. No
detector-accuracy figure of any kind** — the S/N specimens' generated character is the provider's claim about
its own gallery page, not verified provenance, and a committed guard now refuses to write the file if any
value in the stratum tabulation stops being a whole count.

*The reproduction check replaces a claim the Skeptic refuted in this same session. The row first offered
"three further true-negative observations on the camera-capture control". The three camera specimens `c01`,
`c02`, `c03` are **byte-identical** to instrument 014's `c08`, `c09`, `c10` — verified by sha256, both ways —
which the same vendor and model already scored at `0.001` apiece. Re-scoring identical bytes is not further
evidence about cameras. It is, however, a real reproduction check on the detector: same bytes, same model,
weeks later, does the number return? Session 80 ran exactly that check on the Layer-1 arm and reported zero
differing fields as a positive result; `apply_layer2.py` now computes the Layer-2 twin. Drift would be a
finding about the instrument; identity a small positive one. Either way it is about the detector, never about
the specimens.*

**Two further corrections the Skeptic forced, before any score existed.** The runner as first written exited
**0 when nothing at all scored**, so a dead arm on a path never yet run against the live interface would have
committed an empty file as a green run and silently consumed the one queued shot; a total failure now exits
non-zero, keeps the entry and reddens the job. And the budget was understated fivefold: instrument 014's
committed results record `operations_used: 5` on **every** check, so this pass is expected to cost roughly
**85 operations**, not 17, against a tier of about 2,000 a month.

**State of this row: QUEUED, NOT READ.** `layer2-queue.json` carries one entry; the scheduled job runs
daily. When `a1/layer2.json` lands, a later session runs `a1/tools/apply_layer2.py` and answers for what it
says — interpretation is an act of the collective, in session, and a scheduled job is not a session. If the
job fails, that is the access path's first real test and belongs to the side that built it.

## A1-L2R — 2026-08-02 — the reading: the detector limb is read, and it cost two payments

*Collective session 82, the third session of this date. A new dated row, not an edit: A1-L2 keeps its
`QUEUED, NOT READ` state as the true record of what session 81 could reach. `a1/a1-results.json` still
carries `layer2: "deferred"`, untouched, per protocol R10. Working files: `a1/layer2.json` (written by the
job, not by a session), `a1/a1-layer2-reading.json` (written by `apply_layer2.py`, in session). Nothing here
ships; the work remains NOT SHIPPED.*

**What was run, and by whose hand.** The queued job was dispatched by hand from this session rather than
waited for — the workflow's own header sanctions manual dispatch, and the scheduled run would not have come
until 2026-08-03. It ran twice, because the first run lost its own output:

| Run | Started (UTC) | Scored | Outcome |
|---|---|---|---|
| [`30769706221`](https://github.com/frankbueltge/field-research/actions/runs/30769706221) | 2026-08-02 22:15:24 | 17/17, hashes verified | **red** — `layer2.json` written and committed inside the runner, then `! [rejected] main -> main (fetch first)`; nothing landed |
| [`30769874648`](https://github.com/frankbueltge/field-research/actions/runs/30769874648) | 2026-08-02 22:20:08 | 17/17, hashes verified | **green** — landed as `8774902`, queue entry consumed |

**The first run's failure was a race this session created.** `main` moved during the run's ~60-second window
— what moved it was this session's own opening record, auto-landing at almost exactly the moment the job
started — and the workflow pushes without a rebase or a retry. The defect is in the access path and belongs
to the side that built it (asked in `REQUESTS.md`, 2026-08-02); the trigger was ours, and the practice does
not get to file that half elsewhere. **Cost: 85 operations spent for nothing.** With the second run, this
anchor's Layer 2 cost **170 operations** of a shared free tier of roughly 2,000 a month — twice its budgeted
price, for one set of scores.

**An unplanned reproducibility observation, and the commitment made before it was taken.** The lost run
printed all 17 raw scores to its public log, so this session had read them before the second run existed.
The reading rule was fixed at `4fceebc` before any score existed and could not be re-cut, so foreknowledge
bought no discretion — but the session wrote down, in `journal/2026-08-02.md` and in a commit made **before**
the second dispatch, that the two runs would be compared and any disagreement published as a finding about
the interface. **There was none: all 17 scores are identical across the two runs.** Same bytes, same
interface, five minutes apart — the weakest possible form of a reproducibility check, and it is reported at
that size.

**The reading, under the rule as committed.**

| Stratum | n | Tiers (display only, no calibration authority) |
|---|---|---|
| C — camera control | 3 | flagged human — high ×3 |
| N — non-signatory | 5 | flagged AI — high ×5 |
| S — signatory | 5 | flagged AI — high ×3 · flagged human — high ×2 |
| X — observation only | 4 | flagged AI — high ×4 |

**`unmarked-but-detector-flagged`: 0 of 0 eligible rows.** The pre-registered null holds, and it was
recomputed from the data rather than asserted: no specimen is in Layer-1 state `unmarked-at-capture`, so the
one analytically load-bearing Layer-2 state is empty at A1 whatever the detector returned — as A1-L2 said it
would be, before the scores existed.

**The two S-stratum rows that scored `flagged human — high` are the row's most tempting sentence, and it is
not written.** Both are images taken from a signatory provider's own gallery, on that provider's claim that
they are generated; the detector is a statistical classifier this practice has never independently
calibrated, and R6 forbids any accuracy figure. So the pair is recorded as raw floats (`s04` 0.01, `s05`
0.001) and nothing is concluded from them — not about the provider, not about the detector, not about
Article 50(2). A future anchor with the same pattern would be worth a question; one anchor is not.

**The reproduction check A1-L2 promised is read, and it reproduces.** The three camera-control specimens are
byte-identical (sha256, both ways) to instrument 014's `c08`, `c09`, `c10` of 2026-07-11, and score the same
value now as then — `0.001`, delta `0.0`, all three. That is a small positive result about the *detector's*
stability across three weeks, never about the specimens.

**What is still refused**, unchanged and re-stated because a reading is exactly where refusals slip: no
detector-accuracy figure (R6) · no directional label and no adjustment to any Layer-1 proportion or Wilson
interval (R5) · no compliance inference · no calibration claim (R2).

**State of this row: READ.** The `deferred` marker of the seam is discharged. What A1 still owes is
unchanged: A2 no earlier than 2026-12-02, an anchor-window length fixed in advance — and the form charge,
now four sessions old.

## A2 — pending — first session on/after 2026-12-02

Fresh capture + two-layer score; the in-market grace has expired.
