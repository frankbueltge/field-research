# A1, Layer 2 — the reading rule, pre-registered before any score exists

**Committed collective session 81, 2026-08-02, before the detector job was queued and therefore
before a single score existed.** The git history is the timestamp, exactly as it is for the anchor
itself. Nothing in this file may be re-cut once `a1/layer2.json` lands; a rule changed after the
data arrives is worth nothing, and this practice has said so in its own minutes.

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

**The consequence, stated here before any score exists, because it is a property of the capture and
not of the data that has yet to arrive:** A1 has **zero** rows in state `unmarked-at-capture`
(`a1/a1-results.json`: 16 of 17 specimens carry no manifest, and every one of them is
`indeterminate-at-capture`; the seventeenth is `machine-readable-marked`). **So
`unmarked-but-detector-flagged` will be empty at A1 no matter what the detector returns.**

Writing that down now, rather than discovering it after the fact, is the whole point of a
pre-registration. It also means the honest description of this job is not "the analytic payload the
pre-registration promised Layer 2 would carry" — that payload is unreachable at this anchor for
reasons fixed on 2026-08-02. What the job does deliver is R4, and nothing beyond it.

## R4 — What Layer 2 therefore does deliver at A1

Four things, each descriptive, none of them a directional or compliance claim:

1. **The `deferred` marker is discharged.** The second limb of the statutory sentence is *read*
   rather than *unread*. A row that says "we did not measure this" and a row that says "we measured
   it and here is what came back" are different rows, and only one of them can be argued with.
2. **Three further true-negative observations on the camera-capture control.** `c01`–`c03` are
   hardware-capture provenance specimens (the 014 lineage). Descriptive only; no accuracy rate is
   computed from three files, and none may be.
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

## R7 — Failure semantics, and why they are asymmetric

- **sha256 mismatch → abort before any upload, exit non-zero.** The queue keeps the entry, the job
  goes red, and a human sees it. This costs no budget, so a daily red is the right price.
- **Any per-specimen interface failure → recorded in the output file, run continues, exit 0.** The
  file is written and the queue entry is consumed.

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
