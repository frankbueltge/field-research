# field: a work shipped today must not crash /field — render the one-day plate, span every mark

Answers `field-feedback/2026-07-24.md` (build red at 04:22 and 06:10, no deploy; instrument 017
invisible on the site). The failing page is `/field/index.html`:
`buildControlSvg: need at least two days`.

## Root cause

`/field` features the newest committed instrument and builds its record strip over
`dayRange(meta.date, endDate)`, where `endDate` is the latest of the current encounter's
`status.as_of` and the mark dates. When a work ships the same day the gate builds — instrument
017, committed date 2026-07-24; at incident time its only touching chronicle stamp was dated
2026-07-24 (entry 58 then pointed at the retired draft slug); `as_of` 2026-07-22 — the range
collapses to a single day and `buildControlSvg`'s `< 2` guard throws, taking the whole build
(and every deploy) down. This fires **every time** the engine ships a new work and the gate
builds before anything later-dated touches it — i.e. on the day the site most wants to publish.

Two adjacent hazards in the same family, both fixed here:

- The engine has since corrected chronicle entry 58 to the shipped slug, so 017 now also carries
  a stamp dated 2026-07-23 — **one day before `meta.date`**. Under the old
  `dayRange(meta.date, …)` lower bound that mark falls off the plate and `dx` throws
  (`date 2026-07-23 is not on the plate`) — independently verified by review: relaxing the
  `< 2` guard alone still crashes the build once that chronicle state syncs. The span widening
  below is load-bearing, not polish.
- `/field/history` spans its tape over the chronicle's date range only, while the instrument
  triangles come from the werke mirror's meta dates. A meta date outside the chronicle range
  throws `buildStripSvg: date … is not on the tape` the same way. Reproduced in a local gate
  simulation **specifically under the works-synced/chronicle-lagging ordering** (new work in the
  mirror, `chronicle.upstream.json` not yet carrying its session); with today's fully synced
  chronicle the range happens to cover it and the page builds — the hazard is the ordering, and
  it costs the same total outage when it lands.

## The change

- `src/lib/field/strip.ts` — `buildControlSvg` accepts a **one-day plate**: an instrument shipped
  today has exactly one wall-clock day of service (built mark, ship stamp and pen on the same
  date); that is a real state, not an error. Geometry degenerates cleanly (every mark at X0);
  only the empty plate is refused. New exported pure helper **`plateSpan(metaDate, markDates,
  asOf)`** — the plate's wall-clock span, from the earliest of the committed date and all mark
  dates to the latest of those and `as_of` — so the load-bearing derivation lives in a tested
  module instead of inline page frontmatter (the `latest.ts` precedent). `buildStripSvg`
  unchanged.
- `src/pages/field/index.astro` — replaces the inline `dayRange(meta.date, endDate)` computation
  with `plateSpan(...)`; every mark is on the plate by construction.
- `src/pages/field/history.astro` — the tape spans the **union** of chronicle dates and
  instrument meta dates, so every triangle it draws is on the tape. Quiet-day handling unchanged.
- `src/lib/field/strip.test.ts` — five new cases pin the behaviour: a single-day plate renders
  (marks, stamp, pen present); only the empty plate throws; `plateSpan` widens for a mark before
  the committed date, collapses to the legitimate one-day span, and extends to a later `as_of`.

No visual change to any state that built before; the only new renderings are states that
previously crashed.

## Validation (local, on this exact tree)

- `vitest run`: 525/525 pass (including the five new cases).
- `astro check`: 0 errors, 0 warnings.
- `npm run build` in a simulated gate state (instrument 017 copied into the werke mirror, engine
  chronicle synced to `chronicle.upstream.json`): the unpatched tree reproduces the `/field`
  crash (and, under the chronicle-lagging ordering, the `/field/history` crash); this tree
  completes green — including the plate for 017.
- Independent review (engine-side): root cause re-derived from the unpatched code; reversed-range
  impossibility, step=0 geometry, history-union output-stability (byte-identical page for current
  data) and TS strictness each checked; verdict PASS WITH FINDINGS — all three findings
  (two writeup inaccuracies, one test-coverage gap) adopted in this revision.
