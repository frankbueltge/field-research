# A1, as first specified, was refuted by its own change-list

**2026-08-06 (session 93), conductor's own hand, before any network request was made and before
any role was convened. Unreviewed at the time of writing.**

`PREREGISTRATION-V2.md` §2/A1 named over-catching as the risk this amendment carries, and required
the re-run to publish **every** identifier the rule moves out of `evidence`, "one line each, …so
that a reviewer can dispute any one of them". That requirement was the only defence the design had.
It fired on the first run, and it fired on the design that wrote it.

## What happened

A1's scope was specified as: *from the marker's character offset to the first of a blank line, or a
block-break token (`<br`, `</p>`, `<p `, `<li`, `</li>`, `<h`)*.

**A compact `data.json` contains none of those.** No blank line, no markup. So in every such file a
single occurrence of `corrected`, `discarded` or `correction` — words this archive's own prose uses
constantly, because it documents its own errors — gave the marker a scope running to the end of the
file.

**First run, offline: 114 identifiers moved from `evidence` to `correction-record`.** Whole
citation blocks of `works/2026-07-01-calibration-gap/data.json` and
`works/2026-07-01-calibration-gap/evidence/specimen.html` were among them: arXiv abstracts, DOIs,
court dockets, vendor pages — live sources, none of them corrections. Under that rule the census
would have reported a healthier archive by the simple device of no longer looking at most of it.

## The correction

The scope is additionally capped at **the end of the marker's own line** — the rule becomes
line-local and forward-only. That is the narrowest reading of A1's *"within the same block"* that
still catches the case D1 exists for, where marker and identifier sit on one line
(`works/2026-07-01-fairness-trap/work.astro:590`).

**What this costs, stated rather than discovered later:** a correction note whose withdrawn
identifier sits on a *following* line is no longer caught. That is a known, narrower failure, and
it fails in the direction of counting a withdrawn identifier as live evidence — a false alarm
against this practice — rather than in the direction of hiding live citations, which is the failure
that flatters.

## Why this is a finding and not a patch

The rule was changed **after seeing output**, and that must be said plainly rather than buried:
the output it was changed after is the **offline Layer-0 change-list**, produced by the very
mechanism A1 mandated for this purpose, **before any request was sent and before any liveness
verdict existed**. No `GONE`, no `OK`, no `BLOCKED` had been computed under either form of the rule.
The predictions in `PREREGISTRATION-V2.md` §4 are scored against the corrected form, and P1's
subject — the withdrawn DOI at `work.astro:590` — is the case both forms were built around.

The first form's number is kept here, in the record, so that "114" cannot later read as an
unnoticed near-miss.
