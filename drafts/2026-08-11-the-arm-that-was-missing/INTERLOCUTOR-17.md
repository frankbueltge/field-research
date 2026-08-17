# Interlocutor report — deliverable-v0.3.3 gauntlet, 2026-08-17

*Two obligations in one pass: (a) attempt to refute the core claim — blocking; (b) the hostile
critique — non-blocking, published unedited beside the work.*

`deliverable-v0.3/` was read in full (30 files) plus the source `ledger/` files, `errata_check.py`
and the errata registry it references, which live in the wider repository this bundle is built
from. Nothing inside `deliverable-v0.3/` was edited. All computations below were run read-only
against the bundle as it sits.

## The core claim, in one sentence

This bundle claims to deliver a credential-free, single-vantage, once-daily, independently
checkable measurement of whether a large fixed panel of publicly-cited video identifiers on a
large video platform remain publicly retrievable — 12.18% not retrievable on the reference day,
rising with age (p = 1.47×10⁻⁹) — offered to an outside research team as a comparison population
("a yardstick, not a verdict") against which a single reading of their own smaller list can be
given an expectation.

---

## (a) The refutation attempt — BLOCKING

I did not attack the prose. Five gauntlets already did that. I attacked the arithmetic, the
sampling frame, and the chain of custody, by recomputing everything I could recompute and by
running the practice's own verification tooling against the frozen state myself.

**1. [ATTACK FAILED] Chain-of-custody / hash integrity.** I recomputed sha256 for all 30 files
listed in `MANIFEST.json` against the bundle on disk: 0 mismatches, 0 files missing, 0 files
present but unlisted. I then went further than the bundle asks a receiver to and verified the
13 *upstream* run/sidecar files it cites by path+hash but does not ship inline (`ledger/baseline-union.json`,
the five daily `ledger/run-*.json` files, the five `ledger/transition-confirm-*.json` sidecars,
`ledger/corrections.json`) against the actual files in the parent repository: all 13 matched
exactly. The confirmation-record's 9 transition events, the manifest's 6 daily run files, and the
2 correction rows all trace to real, hash-verified bytes. This attack found nothing.

**2. [ATTACK FAILED] Statistics.** I independently recomputed, from the raw counts in
`gradient-test.json` and `expectation.json`, every Fisher exact test (pooled and all three
strata) and the pooled Wilson confidence interval for 2026-08-16. Every p-value, every ratio, and
both confidence-interval bounds reproduced to the last published digit (pooled ratio 3.5981148…,
p = 1.4735989×10⁻⁹; Wilson CI [0.111478…, 0.132908…]). The claim that the age gradient survives
stratification (W-article p = 5.76×10⁻⁶, W-other-ns p = 1.74×10⁻⁴, only the small F-forum stratum
underpowered at p = 0.103) also checks out and rules out the most obvious confound — that the
gradient is an artefact of which source contributes the oldest identifiers.

**3. [ATTACK FAILED] Regression of previously-published corrections.** I ran `errata_check.py
deliverable-v0.3` from the parent repository, unmodified, exactly as its own docstring
instructs. Result: 21 files scanned, **0 regressions**, and by `--coverage`: 53 published errata,
36 registered as checkable wording, 17 individually reasoned as un-checkable-by-wording (each
reason legible), 0 unaccounted, 0 broken mappings. Every one of the four prior gauntlets' findings
that *can* be expressed as a sentence is verifiably absent from this state, not merely claimed
absent.

**4. [ATTACK ATTEMPTED, THEN REVERSED ITSELF ON THE DATA — informative, not blocking.** The
headline 12.18% and every age-band cell are pooled from the *daily ledger*, which — by the
bundle's own account (`README.md` §3, `LIMITS.md`, `ledger.py`) — takes **one pass per identifier
per day** and confirms only apparent day-to-day *transitions*, not the bulk of stable readings.
By the bundle's own standard ("a single reading is not a finding," README §3), that looked like a
real crack: the ~437 absent units on any given day were never individually re-requested the way a
receiver's own list would be. I tested this directly against `series/presence-series.csv`. Of the
non-control panel (3,620 identifiers, arms A/A2/A-new/B), only **7** ever show more than one
determinate state across the six independent days; **412 of the 446** identifiers that are ever
absent are absent on *every* day they were measured (92%). A one-off network glitch recurring
identically across six independently-scheduled daily runs, hours apart, is not what per-request
noise looks like — the persistence pattern is itself strong indirect confirmation of the bulk of
the absent readings. **This is a real finding the bundle does not make or cite anywhere** — it
leans entirely on a 9-event transition-confirmation sample while sitting on a much larger, more
convincing piece of evidence in its own series data. I list this as a failed attack, and flag the
missed opportunity in (b).

**5. [BLOCKING] The citation panel's own construction date and exposure to citation/dead-link
maintenance are undisclosed anywhere in the 30-file bundle, and this is a real gap in the
"reference population" half of the claim, not a wording issue.** I grepped every prose file
(`README.md`, `LETTER.md`, `LIMITS.md`, `VERSIONS.md`, `FIGURES.md`) and every JSON file for any
date, dump identifier, or extraction method behind "videos cited in public... across 37
encyclopedia language editions... and posted to one public technology forum." There is none. The
practice logs and cross-checks the reference-table clock down to the second (`t_ref_utc`,
`ages_computed_at_utc`, the 2.6803-day bookkeeping defect it caught and fixed, the drift table
computed to four decimal places) — every other clock in this bundle is treated as load-bearing and
stated. The one clock that is never stated is *when the citation list itself was pulled*. That
matters substantively, not just as a missing footnote: Wikipedia editions differ enormously in how
aggressively they prune or archive-fix dead citations, and that pruning intensity is itself a
function of how long a citation has sat unedited — i.e., of the same "age" variable the age-band
table is built on. A receiver cannot rule out that part of the observed gradient — 4.86% absent at
0-1y rising to 17.48% at 5y+ — reflects which already-dead citations had already been scrubbed
from the pool this practice draws from by the time it was assembled, rather than purely reflecting
the platform. The bundle's own robustness check (persistence within-stratum) does not touch this,
because it is a property of the *sampling frame*, not of the measurement instrument. This is the
one objection in this pass that is genuinely new — it is not on the errata registry, not in
`LIMITS.md`'s ten numbered limits, and not addressed by anything the four prior gauntlets forced
into the record.

**6. [NON-BLOCKING] "The run files... are all here" (`LETTER.md`, item 3) overclaims locality.**
The run files are not inside `deliverable-v0.3/` — only their sha256 and a small transcribed
excerpt are. Checking them requires the wider `frankbueltge/field-research` repository. I
confirmed that repository is genuinely public and reachable, and that the hashes it publishes
match the actual bytes (finding 1), so the substantive claim — "checkable without asking us
anything" — survives. The sentence "are all here," read as describing the 30-file folder a
receiver actually gets, does not.

### Verdict

**CORE CLAIM SURVIVES, NARROWED**

It survives, and survives well, on its measurement half: every number I could independently
recompute from the shipped and hash-verified source data — the daily counts, the age-band cells,
both Fisher tests, the confidence intervals, the 92% within-panel persistence of absent readings,
and the zero-regression state of 53 previously published corrections — checked out exactly. This
is the first pass on this bundle, in this arc, that found the arithmetic itself sound wherever it
was tested.

It narrows on the "reference population" half of the claim. As shipped, the age-banded table in
`reference-baseline.json` / `expectation.json` cannot be read as a general yardstick for "cited
videos of age X" — only as "what this specific, undated citation snapshot showed on 2026-08-16."
The gap is a missing methods disclosure (when and how the panel was pulled) that the practice's
own standard of care — applied to every other clock in the bundle — would normally require, and
its absence leaves the age-gradient's representativeness, not its arithmetic, open. What would
close this: one dated statement of when the Wikipedia/forum corpus was snapshotted, plus an
acknowledgment (even unquantified) that citation-list maintenance is a candidate confound distinct
from platform-side removal. Nothing about the panel needs to be re-measured to fix this — it needs
to be dated.

---

## (b) Hostile critique — NON-BLOCKING, published as written

Is this slop? No. Judged purely as engineering, this is unusually disciplined work: hash-pinned
provenance for every figure, an errata-regression harness that I ran myself and that came back
clean, statistics that reproduce to the last digit from raw counts a stranger can recount. Most
"data journalism" one-offs do not survive this level of adversarial poking. This one did, on
every arithmetic and chain-of-custody check I threw at it.

But "not slop" is not the same question as "worth the receiver's time," and the honest answer to
that one is more mixed. Strip away the apparatus and the deliverable to the actual named receiver
— the operator of a public dashboard that reports "0 Available, 0 Unavailable, 11 Errors" on
eleven videos — reduces to one sentence: *ten of your eleven videos are fetchable right now from
an ordinary vantage with no account, so your dashboard's blanket "Error" is very likely a fault in
your own harness, not evidence the platform is hiding them.* That sentence is genuinely useful,
genuinely checkable, and could have been an email. Instead it arrives wrapped in 30 files, a
statistical apparatus built to defend a "reference population" whose own construction date is
unstated, and a letter that spends more words disclaiming what it cannot say than saying the one
thing it found. The bundle's own table concedes as much, more bluntly than I would have dared
put it: *"this is a demonstration of the harness, not a discovery about the platform"* — a
sentence honest enough to undercut the "control arm" language the letter leads with in its own
title. When your own showpiece exhibit prices itself down before a reader gets to it, the framing
above it was oversold.

The self-correction machinery has become the actual product. Look at what a receiver has to wade
through to get to that one sentence: a manifest, two figure-provenance files, a versions ledger
recounting four failed internal reviews, a confirmation-record built from nine events, a drift
table computed to four horizons nobody asked about, and eight tool scripts — for a measurement
that, at bottom, is "we hit one public endpoint once a day for six days and 12% of requests came
back HTTP 400." The practice has gotten extremely good at catching itself lying to itself — the
errata registry I ran (53 corrections, 0 live regressions) is a genuinely impressive record of
that — but an audit trail this large, defending a claim this modest, reads less like a delivered
finding and more like an organization that has started grading its own homework instead of
turning it in.

Which is the sharpest thing to say about it: the previous adversary called this "careful, honest,
well-instrumented motion — and it is still motion in place," and on the numbers, that charge is
now *less* true than it was — the measurement itself finally held up under real pressure, for the
first time across this many gauntlets. But operationally the charge stands unchanged and is about
to become irreversible: by this practice's own filed pre-registration, the measurement window
closes 2026-08-18. Today is 2026-08-17. Version 0.3.3 carries, in its own words, "NO VERDICT... no
reviewer has read this state," exactly as version 0.3 and 0.3.2 did before it, and this is the
fifth review in a row that has not resulted in the letter reaching the mailbox it names. Twenty
days of work have gone into six days of measurement, four rebuilds, and a letter that, as of this
review, has still been sent to nobody. What would actually change the verdict on "motion in
place" is not more instrumentation — the instrumentation is, as of this pass, sound — it is
sending the letter. The one identifiable, unfixed content gap (finding 5 above) is closeable with
a single dated sentence. Every other blocking finding across five gauntlets has already been
fixed. There is, as of today, no remaining technical reason for this bundle to still be sitting on
disk instead of in an inbox — which makes the fact that it still is the most damning finding in
this report, and it is not a finding about the platform, or about the measurement. It is a finding
about the practice.
