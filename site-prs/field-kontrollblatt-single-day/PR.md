# field: a work shipped today must not crash /field — render the one-day plate, span every mark

Answers `field-feedback/2026-07-24.md` (build red at 04:22 and 06:10, no deploy; instrument 017
invisible on the site). The failing page is `/field/index.html`:
`buildControlSvg: need at least two days`.

## Root cause

`/field` features the newest committed instrument and builds its record strip over
`dayRange(meta.date, endDate)`, where `endDate` is the latest of the current encounter's
`status.as_of` and the mark dates. When a work ships the same day the gate builds — instrument
017, committed date 2026-07-24, its only chronicle stamp dated 2026-07-24, `as_of` 2026-07-22 —
the range collapses to a single day and `buildControlSvg`'s `< 2` guard throws, taking the whole
build (and every deploy) down. This fires **every time** the engine ships a new work and the gate
builds before anything later-dated touches it — i.e. on the day the site most wants to publish.

A sibling of the same defect sits on `/field/history`: the tape spans only the chronicle's date
range, while the instrument triangles come from the werke mirror's meta dates. A work whose
committed date lies outside the chronicle range (a fresh work synced before its session's
chronicle entry — reproduced in a local gate simulation) throws
`buildStripSvg: date … is not on the tape` and kills the build the same way.

## The change

- `src/lib/field/strip.ts` — `buildControlSvg` accepts a **one-day plate**: an instrument shipped
  today has exactly one wall-clock day of service (built mark, ship stamp and pen on the same
  date); that is a real state, not an error. Geometry degenerates cleanly (every mark at X0);
  only the empty plate is refused. `buildStripSvg` is unchanged.
- `src/pages/field/index.astro` — the plate spans **every mark**, not just `[meta.date, …]`: a
  chronicle stamp or ledger event dated before the featured work's committed date would
  otherwise fall off the plate (`dx` throws). `startDate` = earliest of `meta.date` and all mark
  dates; `endDate` computation unchanged apart from including `meta.date` explicitly.
- `src/pages/field/history.astro` — the tape spans the **union** of chronicle dates and
  instrument meta dates, so every triangle it draws is on the tape. Quiet-day handling unchanged.
- `src/lib/field/strip.test.ts` — two new cases pin the behaviour: a single-day plate renders
  (marks, stamp, pen present), and only the empty plate throws.

No visual change to any state that built before; the only new renderings are states that
previously crashed.

## Validation (local, on this exact tree)

- `vitest run`: 522/522 pass (including the two new cases).
- `astro check`: 0 errors, 0 warnings.
- `npm run build` in a simulated gate state (instrument 017 copied into the werke mirror,
  engine chronicle synced to `chronicle.upstream.json`): reproduces both crashes on the
  unpatched tree, completes green on this tree — including the one-day `/field` plate for 017.
