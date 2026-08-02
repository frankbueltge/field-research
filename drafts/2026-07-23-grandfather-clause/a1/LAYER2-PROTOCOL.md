# A1, Layer 2 — the reading rule, pre-registered before any score exists

**Committed collective session 81, 2026-08-02, before a single detector score existed.** Nothing in
this file may be re-cut once `a1/layer2.json` lands; a rule changed after the data arrives is worth
nothing, and this practice has said so in its own minutes.

> **What this file is blind to, and what it is not — the Skeptic's blocking condition C1, applied.**
> "Before any score exists" covers the *detector's* number and nothing else. It does **not** mean
> this document was written blind: `a1/a1-results.json`, carrying the complete Layer-1 partition of
> all 17 specimens, was committed at `80edc46`, **2026-08-02 03:54 UTC**, and this file at
> `4fceebc`, **19:21 UTC** the same day — more than fifteen hours later. So R3's eligibility rule was
> authored by an author who already knew exactly how the 17 rows fell, and therefore already knew
> what that rule's consequence would be. The phrase "before any score exists" was doing work it had
> not earned; that is corrected here rather than left for a reader to notice. The one blindness this
> file can honestly claim is the one that matters for a *detector* rule, and it is the only one it
> claims from here on.

> **What the git record does and does not prove here — narrowed 2026-08-02 after the Verifier's
> finding V7, in the same session.** This paragraph first read *"before the detector job was queued
> and therefore before a single score existed. The git history is the timestamp, exactly as it is
> for the anchor itself."* The second half is withdrawn. This file, all four tools and the
> `layer2-queue.json` entry landed in **one commit**, `4fceebc` — so git shows *where* they sit in
> history, not that the rule was authored before the job was queued. What git does establish, and it
> is the part that matters: **`a1/layer2.json` has never existed at any commit in this repository**,
> and the scheduled job cannot run against a branch that has not landed. So the rule is fixed before
> the data, which is what a pre-registration is for; the stronger ordering claim was not checkable
> and should not have been made. This is the same boundary the Skeptic drew against anchor A1 on the
> seam — commit order proves where things landed, not what the author had or had not seen — applied
> to this practice a second time, by a different role, one session later. Logged in
> `memory/discarded.md`.

## Why this file exists at all

Anchor A1 (`journal/2026-08-02.md`, session 80) read the first limb of Article 50(2) of Regulation
(EU) 2024/1689 — outputs "marked in a machine-readable format" — and recorded the second limb,
"detectable as artificially generated", as **`deferred`**. The reason was an access path, not a
measurement limit: the detector credential exists only as a repository secret, and a research
session is not the kind of run that can see repository secrets (instrument 014, session 09).

That path now exists (`tools/layer2_queue.py`, `.github/workflows/layer2-queue.yml`, built by the
team in answer to this practice's request of 2026-08-02). What was missing on this side was the arm
itself. `a1/tools/run_layer2.py` is that arm; this document is the rule by which whatever it returns
will be read.

## R1 — What is scored, and the integrity stop

The **17 committed specimens** of `a1/specimens.json`, each of which was sha256-pinned and committed
before either layer ran at A1. The runner re-computes every hash and compares it to the committed
value **before any upload**. On any mismatch it aborts, having spent nothing.

This is not ceremony. The scoring happens on a different day, on different hardware, from a checkout
of `main` — so "the same bytes" is a claim that has to be checked rather than assumed.

## R2 — Tiers and the raw record

Inherited verbatim from instrument 014 and unchanged: `≥0.90` *flagged AI — high* · `0.50–0.90`
*AI-leaning* · `0.10–0.50` *human-leaning* · `≤0.10` *flagged human — high*. **The raw floats are the
record**; tiers are a display convention applied at reading time and carry **no calibration
authority** (014's standing caveat: this practice's entire independent calibration of this detector
is a single anecdotal true-negative). No new detector, no new calibration claim.

## R3 — `unmarked-but-detector-flagged`, and the null this rule forces

The pre-registration (`README.md` §"Scoring") defines the reportable state
**`unmarked-but-detector-flagged`**: no synthetic manifest present, yet the pixels score `≥0.90`.

**It applies only to rows whose Layer-1 state is `unmarked-at-capture`.** Rows in
`indeterminate-at-capture` are excluded. The reason is the pre-registration's own indeterminate
arithmetic: those rows are excluded from both numerator and denominator precisely because a missing
manifest there may be the host's doing, not the provider's. Reading such a row as "unmarked" would
assert the very absence the `indeterminate-at-capture` state exists to refuse.

> **This restriction is an extension of the pre-registration, not a quotation from it — labelled so
> after the Verifier's finding V5, same session.** The locked text defines the state as *"no
> synthetic manifest present (Layer 1 negative) yet the pixels score ≥0.90"*, and on its face
> "Layer 1 negative" would include `indeterminate-at-capture` rows, which also lack a synthetic
> manifest. The indeterminate-arithmetic passage the restriction leans on (Skeptic condition 4,
> session 55) governs the Layer-1 *proportion*, not this state. So this is **interpretive judgement
> applying the pre-registration's stated reason to a case its text does not decide** — defensible,
> in the direction of claiming less, and now on the record as a choice rather than as a rule that
> was already written down. It is also the choice that makes this arm's own payload null at A1: it
> costs this session something and is adopted anyway. **A2 inherits it**; a future session that
> wants the wider reading must argue for it as a change, in the open.

**The consequence, stated here before any score exists, because it is a property of the capture and
not of the data that has yet to arrive:** A1 has **zero** rows in state `unmarked-at-capture`. The
17 specimens of `a1/a1-results.json` divide as **13 `indeterminate-at-capture` · 2
`manifest-not-synthetic` · 1 `manifest-invalid` · 1 `machine-readable-marked`** — 13 carry no
manifest at all and every one of those is indeterminate; the other four carry a manifest, three of
them on the camera-capture control. **So `unmarked-but-detector-flagged` will be empty at A1 no
matter what the detector returns.**

> **Correction, 2026-08-02, same session, before any score existed.** The sentence above first read
> *"16 of 17 specimens carry no manifest, and every one of them is `indeterminate-at-capture`; the
> seventeenth is `machine-readable-marked`."* That is **wrong by three specimens**: only 13 carry no
> manifest, and the camera-control rows `c01`/`c02` (`manifest-not-synthetic`) and `c03`
> (`manifest-invalid`) carry manifests that are simply not synthetic. The conclusion — zero
> `unmarked-at-capture` rows — is unaffected, because that state requires no manifest *and* no
> stripping evidence and no row in this anchor has both. Found by the Interlocutor convened against
> this file, not by its author, in a document whose next paragraph praises recomputing counts from
> the data rather than asserting them; `apply_layer2.py` does recompute correctly, and the prose
> about that discipline had not been checked against the same file. Logged in `memory/discarded.md`.

Writing that down before the scores arrive is worth something — it removes any later temptation to
present an empty state as a result. But it is **not a discovery**, and the Skeptic was right to say
so (C2): the emptiness is a mechanical consequence of Rule A1-S, which was fixed at session 80 and
assigns `indeterminate-at-capture` to every manifest-absent row carrying stripping evidence
(`a1/tools/score_a1.py`). The literal state `unmarked-at-capture` was never going to appear in this
anchor under any Layer-2 rule whatsoever. What R3 adds is the *reason* for excluding indeterminate
rows and a commitment that binds A2, where the state is genuinely live; the arithmetic at A1 was
already settled the day before this file existed.

The honest description of this job is therefore not "the analytic payload the pre-registration
promised Layer 2 would carry". That payload is unreachable at this anchor. What the job does deliver
is R4, and nothing beyond it.

## R4 — What Layer 2 therefore does deliver at A1

Four things, each descriptive, none of them a directional or compliance claim:

1. **The `deferred` marker is discharged.** The second limb of the statutory sentence is *read*
   rather than *unread*. A row that says "we did not measure this" and a row that says "we measured
   it and here is what came back" are different rows, and only one of them can be argued with.
2. ~~**Three further true-negative observations on the camera-capture control.**~~
   **REFUTED, same session, by the Skeptic (C3), and replaced.** `c01`–`c03` are not merely "the
   014 lineage" — they are **byte-identical** to instrument 014's `c08`/`c09`/`c10`, which the same
   vendor and model already scored at `0.001` apiece
   (`works/2026-07-11-split-seal/data/layer2.json`). Verified here by sha256, both ways. Re-scoring
   identical bytes is not further evidence about cameras; it is a repeat of a known measurement, and
   calling it "further" was wrong.
   **What it is instead, stated as the purpose rather than discovered afterwards: a reproduction
   check on the detector.** Same bytes, same vendor, same model, weeks later — does the number come
   back the same? Session 80 ran precisely this check on the *Layer-1* arm and reported zero
   differing fields as a positive result; this is its Layer-2 twin, and `apply_layer2.py` computes
   it (`inherited_specimen_reproduction`), verifying byte-identity itself rather than trusting a
   filename. A drift here would be a real finding about the instrument; identity would be a small
   positive one. Either way it is about the detector, never about the specimens.
3. **The A1 half of an A1 → A2 detector comparison.** A2 is date-locked to 2026-12-02 at the
   earliest. Without this pass there is no A1 half to compare against, and the detector axis would
   be unavailable for the whole ledger.
4. **The first live exercise of a new access path**, which the team stated plainly has never run
   against the live interface. Whatever it returns is infrastructure feedback, and a failure is
   infrastructure's, not the ledger's.

## R5 — No label, in either direction

Layer 2 at A1 produces **no directional label, no compliance inference, and no adjustment to any
Layer-1 proportion or Wilson interval.** The load-bearing comparison remains the fresh-capture pair
A1 → A2 on Layer 1 (`README.md` §"Decision rule", Skeptic condition 2, session 55). A single anchor
cannot carry a direction on either layer.

## R6 — What a detector score is not

A score is **not** evidence that a specimen is or is not AI-generated. The S- and N-stratum
specimens come from providers' own published model galleries, so their generated character is **the
provider's claim about its own page**, not independently verified provenance. Therefore **no
detector-accuracy figure of any kind is computed at A1** — no true-positive rate, no false-negative
rate, no agreement statistic against stratum. `apply_layer2.py` does not compute one and must not be
extended to.

**And that prohibition is now checkable rather than merely stated** — the Skeptic's blocking finding
C6, applied. Its objection was exact: `strata_descriptive` already holds a stratum-by-tier
cross-tabulation, so *one added division* would produce the forbidden detector-flagged rate by
provider posture, and nothing but a comment stood in the way. `assert_no_derived_rate()` now
enforces the invariant that **every value under `strata_descriptive` is a whole count, or a mapping
of labels to whole counts.** A rate is a float; the moment anyone divides anything there, the tool
refuses to write its output. Four selftest assertions exercise the refusal. This is not proof of
good intent — it is a tripwire a future edit has to remove **on purpose, in the open**, which is all
a guard of this kind can honestly be.

## R7 — Failure semantics, and why they are asymmetric

- **sha256 mismatch → abort before any upload, exit non-zero.** The queue keeps the entry, the job
  goes red, and a human sees it. This costs no budget, so a daily red is the right price.
- **A partial interface failure → recorded in the output file, run continues, exit 0.** The file is
  written and the queue entry is consumed.
- **A total failure — not one specimen scored → exit non-zero.** The entry stays queued, the job
  goes red, and it gets looked at. *Added after the Skeptic's blocking finding C4, same session:* as
  first written this rule made "0 of 17 scored" indistinguishable from "17 of 17 scored" at the
  monitoring level, because the driver checks only that the declared output file exists and then
  pops the entry. On a path the team has said has never run against the live interface, a wrong
  secret name or a changed endpoint would have committed an empty file as a green run and silently
  spent the one queued shot. That defeats the driver's own stated rule — *green means the work
  landed, never that an error was echoed away* — and the budget argument does not cover it, because
  a run in which nothing succeeded has spent almost nothing and is cheap to retry.

The asymmetry is deliberate and is about a **shared, finite budget**. One pass is 17 checks against
a free tier of roughly 2,000 operations a month (014 dossier §4d). An entry that stays queued is
retried *daily*. A runner that exited non-zero on interface errors would therefore spend the
practice's shared budget every night on a fault it cannot fix — so the budget is spent **at most
once**, and errors land in the record where a session reads them instead of in a retry loop.

## R8 — The scoring date is not the capture date

`days_since_seam = 0` is a property of the **capture** and does not change. The runner records
`layer2_run_date` and `days_from_seam_to_layer2_scoring` as separate fields, and every reading must
display both. A pass run weeks after the seam must never be able to read as a same-day measurement;
this is the same discipline the pre-registration already imposes on capture lag
(`README.md`, Skeptic non-blocking 1, session 55).

## R9 — Budget: exactly one pass

One pass over the 17 specimens, once, for this anchor. The queue driver removes a finished entry, so
nothing is scored twice by that path. Should a re-run ever be warranted, it is a **new dated event**
with its own stated reason in the ledger — never a quiet second attempt at a nicer number.

**The cost, corrected after the Skeptic's finding C4 (non-blocking):** "17 checks" is accurate and
misleading. Instrument 014's committed results record `operations_used: 5` on **every one** of its
fifteen checks, so a 17-specimen pass is expected to cost roughly **85 operations** against the
~2,000-a-month tier — five times what the earlier phrasing invited a reader to assume. The runner
now records `operations_used_total` so the actual figure lands in the record instead of being
inferred.

## R10 — The amendment is a new dated event, never a patch

The arriving scores **do not edit `a1/a1-results.json`.** That file's `layer2: "deferred"` is the
true record of what session 80 could reach on the seam, and it stays. The scores land in
`a1/layer2.json`; `a1/tools/apply_layer2.py` reads that plus `a1-results.json` and emits a separate
`a1/a1-layer2-reading.json`. The ledger gains a new dated row. This is `PROTOCOL.md` §"Legal
hygiene" 6 applied to our own draft.

## R11 — Who reads it

`apply_layer2.py` is deterministic, offline, and committed **now**, before the data exists — that is
what makes its output a pre-registered reading rather than an interpretation invented to suit a
number. It is *not* run inside the credentialled job: interpretation is an act of the collective, in
session, and a scheduled job is not a session. A later session runs it, reads it, and answers for
it.

`apply_layer2_selftest.py` proves the rule executes and that its edge cases behave — against
constructed fixtures, clearly labelled as fixtures, containing no specimen and no measurement. It is
a test of the code, never a source of a finding.

## What this file does not claim

It does not claim that reading the detector limb answers the "detectable as artificially generated"
question in law. That limb is a legal property of the marking; a commercial classifier's opinion
about pixels is a different thing, and the pre-registration said so before this file existed
(`README.md` §"What this is NOT": *marking ≠ detector-flagging*). What is being discharged here is a
**`deferred`**, not a statute.
