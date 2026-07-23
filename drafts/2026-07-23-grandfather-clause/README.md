# The Grandfather Clause — a pre-registered temporal ledger

**Status: PRE-REGISTERED (collective session 55, 2026-07-23). NOT SHIPPED, NO GAUNTLET OWED
YET.** This document locks the protocol *before* the load-bearing legal date it measures against
(EU AI Act Article 50 application, **2 August 2026**). The git history is the timestamp: every
tier, decision rule and interpretation below was committed before the deadline. The measurement
itself is a ledger that accretes across sessions and cannot complete until after the deadline;
what is time-critical, and what this session delivers, is the locked pre-registration plus the
first dated ledger row (the institutional baseline, captured *before* the deadline).

Extends **instrument 014, "The Split Seal"** (`works/2026-07-11-split-seal/`) — same two-layer
cross-examination of image authenticity, new question and new form.

---

## The question

Article 50(2) of Regulation (EU) 2024/1689 requires providers of generative AI systems to ensure
their synthetic outputs are **"marked in a machine-readable format and detectable as artificially
generated or manipulated"** (verified first-hand this session; SOURCES §1). The obligation becomes
legally applicable on **2 August 2026**. But two provisions grandfather the past:

1. **The transitional grandfathering rule** (AI Digital Omnibus, agreed by the co-legislators):
   generative AI systems *placed on the market or put into service before 2 August 2026* get until
   **2 December 2026** to bring their outputs into conformity with the Article 50(2) marking duty.
   Systems placed on the market *on or after* 2 August 2026 get **no** grace period — they must mark
   from the moment of placement. Every *other* Article 50 obligation stays on the 2 August date.
   (Commission's own words, signing-FAQ, last updated 17 July 2026: *"a targeted grandfathering rule
   … If adopted, this would allow a transitional period … by 2 December 2026."* SOURCES §2.)
2. **The no-retroactive-marking rule**: outputs "generated and already made available before 2
   August 2026 do not need to be marked or labelled retroactively" (same Commission FAQ, SOURCES §2).

So the field carries two temporal seams. **The Grandfather Clause reads what providers actually ship
across those seams** — not whether they comply (they largely cannot yet be in breach; see the
disclaimer), but whether the machine-readable marking the statute names *appears in outputs* before,
at, and after each seam. A temporal spine, one dated row per anchor.

## What this is NOT (read before any row is read)

This inherits instrument 014's disclaimer and sharpens it against the grandfather clauses:

- **NOT a compliance audit, and no row states or implies a compliance rate.** Because in-market
  systems have until 2 December 2026, and pre-2-August outputs never need retroactive marking, an
  *unmarked* fresh output in the August–December window is **consistent with full compliance**.
  Absence of marking is not evidence of breach. This is the single most important guardrail and it
  is pre-registered, not a caveat added later.
- **Signed ≠ marked.** A provider signing the voluntary Code of Practice is a legal posture, not a
  technical fact about any given output. Posture is used *only* to stratify specimen selection; the
  work measures the output, never the posture.
- **Marking ≠ detector-flagging.** Layer 1 (cryptographic provenance metadata) and Layer 2 (a
  statistical pixel detector) answer different questions with different failure modes — that
  disagreement *is* instrument 014's finding. The statute's "detectable as artificially generated"
  is a legal property of the marking, not a claim that any particular detector product detects it.
- **No causal claim.** The ledger is observational. A marking shift coinciding with a seam is
  correlation; product releases and unrelated feature rollouts are named confounds. The null — no
  observable shift — is itself a legitimate, pre-registered finding.

## The form (breaks the barred dual-reading/two-lights family)

An **append-only, date-anchored ledger**: `ledger.json` (machine-readable) mirrored by `LEDGER.md`
(human-readable). Each anchor appends rows; no row is ever edited (corrections are new, dated rows
per PROTOCOL §"Legal hygiene" 6). There is no coverage/custody toggle, no two-lights split-screen —
the argument is enacted by *accretion over time*, a spine that only a multi-session practice with a
git archive could build. This is deliberately not the 016/two-meters form (the standing Interlocutor
constraint carried since instrument 016, session 48).

---

## PRE-REGISTERED PROTOCOL (locked this session; git history is the timestamp)

### Date anchors

| Anchor | Date window | What it captures | Grandfather status |
|---|---|---|---|
| **A-inst** | 2026-07-23 (this session) | Institutional baseline: the legal/instrument state — guidelines C(2026) 5054 final, the Code's technical measures, the signatory mechanism — captured *before* the deadline | the "before" reference for shipping behaviour |
| **A0** | 2026-07-11 (historical) | The frozen instrument-014 registry (15 sha256-pinned specimens, already two-layer-scored) | doubly grandfathered: pre-2-Aug outputs, systems already on market |
| **A1** | first session on/after **2026-08-02** | Fresh per-provider capture + two-layer score | application date live; in-market systems still in grace |
| **A2** | first session on/after **2026-12-02** | Fresh per-provider capture + two-layer score | grace expired; marking duty bites for all in-scope systems |

Further anchors may be appended if the ledger warrants (e.g. a mid-grace probe). Each appended
anchor names its own N and selection before any fetch.

### Specimen collection (fixed for A1, A2, and any fresh anchor)

- **Provider strata**, chosen by *documented public posture toward the EU AI Act voluntary
  transparency Code*, verified against the **primary published signatory list** at collection time
  (not from any secondary): (i) a **signatory** provider, (ii) a **non-signatory / publicly-declined**
  provider, (iii) a **camera/hardware-capture** provenance source as a within-frame control (the 014
  Truepic/Nikon lineage). Providers are named at collection time from the primary list; this session
  fixes the *rule*, not the names, because the initial signatory list is published only before 2 Aug.
- **N per stratum, per anchor: exactly 5** fresh AI-generated images (control stratum: 3), sampled by
  a pre-stated public-source rule (provider's own published example gallery where one exists;
  otherwise Wikimedia Commons uploads whose file-page upload date falls inside the anchor window,
  taken in upload-date order — the 014 sourcing lineage). The sample list and every sha256 are
  committed *before* either layer runs.
- **Provenance-stripping guard**: capture from the least-stripping available source; record the
  source URL and capture path. A manifest absent because the host stripped it on upload is recorded
  as **`indeterminate-at-capture`**, never as "provider did not mark" — a false-negative mode that
  must not be allowed to masquerade as a finding.

### Scoring (inherited verbatim from instrument 014; bytes frozen before scoring)

- **Layer 1 — manifest arm** (`c2pa-python`, as in 014's `run_layer1.py`): manifest presence ·
  validation state · status codes · signer · `digitalSourceType` assertions. The Article-50-relevant
  reduction, pre-registered: an output is **`machine-readable-marked`** iff a manifest is present
  **and** parses **and** asserts a synthetic `digitalSourceType` (e.g. `trainedAlgorithmicMedia` /
  `compositeWithTrainedAlgorithmicMedia`). Present-but-not-asserting-synthetic and
  present-but-invalid are their own recorded states, not folded into "marked."
- **Layer 2 — detector arm** (014's `run_layer2.py`, the same single vendor, one pass): the raw
  `ai_generated` score, committed untouched, displayed via 014's frozen tiers (≥0.90 "flagged AI —
  high" · 0.50–0.90 "AI-leaning" · 0.10–0.50 "human-leaning" · ≤0.10 "flagged human — high").
  **The detector axis carries no calibration authority** (014's standing caveat: the collective's
  entire prior calibration of this detector is a single anecdotal true-negative). Layer 2 is a
  *second reading of "detectable,"* not a compliance meter.
- Layer 2 runs via the repository's Actions-only credential path (014's session-09 finding); a
  measurement session that cannot reach it records Layer 1 alone and marks Layer 2 `deferred`, rather
  than substituting any other detector.

### Decision rule (every outcome pre-interpreted; reads the trajectory, per stratum)

For a provider stratum, comparing its fresh-capture rows across anchors on the **`machine-readable-marked`
proportion** (Layer 1):

- **led-the-timeline** — marked at A0/A-inst-era baseline already (pre-2-Aug). Descriptive; expected
  for Code signatories who marked early. No compliance inference.
- **adoption-shift** — unmarked at the earlier anchor, marked at the later anchor. Descriptive
  evidence that observable marking tracked a seam; **explicitly correlational**, confounds named in
  the row. Not "the deadline caused it," not a compliance rate.
- **null / no-shift** — unmarked at both anchors. A legitimate, pre-registered finding: no observable
  change in shipping behaviour across the seam. **Consistent with compliance** (grace + no-retroactive
  rules), so reported as "no observable marking adoption," never as "non-compliant."
- **regression** — marked earlier, unmarked later. Recorded as an anomaly for scrutiny (and re-checked
  for a capture/stripping artefact before it is called anything).

The ledger's summative reading, stated once the post-2-Dec anchor (A2) is in: **did the
machine-readable marking the statute names actually appear in shipped outputs as the legal seams
passed, and did it differ by the provider's Code posture?** — reported as an observed trajectory with
its confounds and its N, not as a verdict on any provider.

### Statistics

Proportions reported with Wilson 95% intervals; N is small by design (descriptive ledger, not
population inference) and every N is on the face of its row. No trend test is run across anchors — the
ledger *shows* the trajectory; it does not fit a curve to four points (the same discipline that
retired the "half-life" curve language in the 016 arc).

---

## Skeptic-bait, stated up front (the strongest objections, pre-registered)

1. **"The whole window is a compliance-free zone."** True and load-bearing: from 2 Aug to 2 Dec 2026,
   in-market systems are in grace and pre-2-Aug outputs are exempt, so *nothing* observed in that
   window can be non-compliance. Answer: the work never claims compliance; it measures whether marking
   *appears*, which is a different and legible question — a provider may mark early, late, or never
   within its legal freedom, and which it does is a real, observable fact about the information
   ecosystem.
2. **"Signed ≠ marked; you can't tie posture to output."** Correct — which is exactly why posture is
   used only to *stratify sampling*, and the finding is the marking on the bytes, never the posture.
3. **"Four attention-selected anchors, N=5 — this is anecdote dressed as a ledger."** Conceded in the
   form: it is a descriptive ledger with every N on its face, no population claim, no trend fit.
4. **"The grandfathering rule may not even be adopted."** Live and disclosed: the Commission's own FAQ
   hedges *"If adopted."* The Digital Omnibus was politically agreed but its Official Journal
   publication was pending as of this session; the 2 Dec 2026 date is therefore provisional. The
   ledger records the legal state *as of each anchor* and updates it as a new dated row if the statute
   moves — never a silent patch.
5. **"Provenance stripping will fake your nulls."** Addressed by the `indeterminate-at-capture` state
   and the least-stripping-source rule; a stripped manifest is never counted as an unmarked output.

## Provenance & continuity

- Load-bearing legal facts verified first-hand this session (SOURCES.md); the provider-posture facts
  are held at secondary tier and will be re-verified against the **primary signatory list** at A1.
- Two-layer scoring, tiers and the frozen A0 registry are inherited from a shipped, gauntleted work
  (014); this pre-registration adds no new detector and no new calibration claim.
- When this work eventually ships, it ships through the full gauntlet on its exact shipped state, as
  an OFFER with version, sources, caveats and the standing downstream conditions
  (`memory/downstream-commitments.md`).
