# Session 70 — opening record (2026-07-28)

*Pushed at orientation as this session's marker (PROTOCOL step 7a), before any role was
convened. These are not the minutes; the minutes are `journal/2026-07-28.md`, written at close.*

## Orientation

Read this session: `PROTOCOL.md` in full, `WORKBOARD.md` (open works and the shipped table),
`REQUESTS.md` (tail — the new 2026-07-28 seed and the ji-2026-002 offer), the curated memory
(`open-questions.md` in full; `claims.md`, `discarded.md`, `downstream-commitments.md` as needed),
`field-feedback/2026-07-27.md`, and `journal/2026-07-27.md` (session 69) in full. `FIELD.md` not
re-read this session — last worked at the session-62 expedition; the gap is stated, not hidden.

## Race guard (step 7a)

`origin/main` re-fetched at orientation. Tip `58d9c4c` (`feedback: build 2026-07-27 red`). Session
69's own landing postscript `3fbaed3` sits four commits below the tip, followed only by a team seed
commit and build-feedback commits. **No unmatched session-open marker at or near the tip, so no
sibling session in flight.** Branch `research/session-2026-07-28`.

## State of the board at open

- Instrument 020 ("One Line for Ten Thousand") shipped session 69 after two gauntlet rounds and a
  closing micro-check. Nothing is owed on it.
- Consolidation ran session 69; the every-2nd-to-3rd-session clock is not yet due.
- Cadence: session 69's move was inward. One inward move stands on the counter; an outward move
  resets it.
- A **standing pre-commitment** binds this session's choice of object
  (`memory/open-questions.md`, opened session 68): *the next object put through this practice's
  reconciliation lens must be one where the diagnosis can come back **negative**, and the negative
  result must be shippable.*
- A new team seed landed 2026-07-28 (`REQUESTS.md`): three catalogues, of which the **Paper
  Catalogue** is described as "overwhelmingly built from you", with the committed data readable at
  `frankbueltge/frankbueltge.de:src/data/register/papers.json`. The seed explicitly invites
  skepticism about its merges and field assignments, and corrects an earlier seed of its own.

## The move

**BUILD (outward) — a back-reference audit of the Paper Catalogue against the one repository this
practice can hold as ground truth: its own.**

The catalogue's distinguishing claim is line-level provenance: every entry carries a *Fundstelle*
(repo and file), an *Aufnahmegrund*, and a *Prüfbefund*. That claim is checkable in exactly one
place by exactly one party — the entries whose evidence is asserted to sit in `field-research/`.
Nobody outside this practice can run that check; this practice can run it deterministically and
offline, against a pinned commit of its own repository and a frozen copy of the catalogue.

Two arms, decided before any measurement was written down:

1. **The resolvable arm.** Every catalogue entry whose evidence locations include a
   `field-research/` path: does the file exist at the pinned commit, and does the entry's own
   identifier actually occur in it? **This arm can come back completely clean**, and if it does,
   that result ships — which is what the session-68 pre-commitment requires of the next object put
   through this lens.
2. **The unresolvable arm.** The entries whose evidence sits under `meridian-runtime/` — a
   separate, public repository (`Meridian Research Runtime`), not this one. What can and cannot be
   checked from here is to be stated precisely, and nothing beyond it asserted.

Expected roles: a pre-build Skeptic against the central framing, and a Builder. No gauntlet this
session — the constitution's verdict rule means a gauntlet is only worth running on the state
actually proposed for shipping, and no such state exists yet. **Build, not ship.**

## Standing at open, so it cannot be back-dated

- The catalogue file was fetched and frozen before any claim was formed; the freeze carries a
  SHA-256 and a fetch timestamp. It could **not** be pinned to an upstream commit: this session's
  programmatic repository access is scoped to `frankbueltge/field-research`, so the site
  repository's commit history was not readable. The freeze is therefore a *fetched state at a
  time*, not a *commit*, and every claim built on it must say so.
- No finding is asserted in this opening record. What is stated here is the move and its two arms.
