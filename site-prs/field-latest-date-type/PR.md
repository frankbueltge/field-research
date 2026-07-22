# field: narrow the featured instrument's meta date so /field passes astro check

Answers `field-feedback/2026-07-21.md` (build red, no deploy). All three errors are the same
type gap in `src/pages/field/index.astro`: it reads `meta.date` from `latestInstrument()` at
lines 43/44 (mark + row construction) and 78 (`dayRange(meta.date, endDate)`), but
`LatestInstrument.meta` is typed `InstrumentMeta`, whose `date` is optional — so `astro check`
sees `string | undefined` flowing into `string` parameters.

The runtime guarantee already exists: `latestInstrument()` throws on a missing committed date
("fails loud … rather than fall back to a stale default"). This change makes the type system
carry that guarantee instead of asking every consumer to re-check it:

- `LatestInstrument.meta` becomes `InstrumentMeta & { date: string }`.
- `latestInstrument()` destructures `date`, keeps the existing throw, and returns
  `{ ...meta, date }` — behaviour unchanged, no new fallback introduced.

No change to `orderInstruments` (it must still tolerate undated entries for ordering), no
change to the page, no change to test behaviour (`latest.test.ts` pins derivation, numbering
and the two fail-loud throws — all unaffected; the narrowed return type is
assignment-compatible everywhere the tests read it).

Written by the practice as part of session 53 (2026-07-22), whose minutes document the red
build's diagnosis alongside the session's recovery work.
