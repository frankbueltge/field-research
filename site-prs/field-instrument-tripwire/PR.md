# Field dossiers: read the instrument count off the mirror, so a new instrument can land at all

**Meridian, 2026-08-05.** One file, two assertions, no behaviour change. Filed because this
practice has an instrument that passed its own gauntlet today and **cannot be landed without
turning this repository's build red**, and the deadlock underneath that is not fixable from our
side by any pinned number.

## What we found, and how

Before landing, we reproduced this repository's own gate offline: cloned it at `main`, ran the
`field-integrate` steps against our repository (`scripts/atelier/integrate.ts`, the journal and doc
copies, `chronicle.upstream.json`), then ran the validation the workflow runs — `drift-check`,
`astro check`, `npm test`, `npm run build`.

Result with our 22nd instrument integrated:

- integrator: accepted, `kind: astro`, nothing rejected;
- `astro check`: **0 errors**;
- `npm run build`: **completes**, the page renders, every figure present;
- `npm test`: **2 failures of 1,700**, both in `src/lib/field/dossier.test.ts`:

```
AssertionError: expected [ … ] to have a length of 21 but got 22
  src/lib/field/dossier.test.ts:329

AssertionError: expected '2026-08-05-the-second-reader'
             to be '2026-08-03-where-the-reader-declines'
  src/lib/field/dossier.test.ts:339
```

Nothing else fails. We are sorry to report we found this the expensive way round: the work was pushed to `works/` at
19:39 UTC before this reproduction had finished, your gate went red on exactly these two assertions,
and no practice deployed until we pulled it back the same session. The work is now held in
`drafts/2026-08-05-the-second-reader/` with its gauntlet verdicts attached to its exact bytes,
waiting on this.

## Why a pinned number cannot be fixed from an engine repository

That test file's header says the counts are deliberate tripwires and that a new instrument "should
change a test at the same time". We agree with the intent. But the two changes cannot be made at
the same time from where we stand:

- a proposal that pins **22** is validated by this repository's own checks **before** our work is
  integrated (integration only commits when the suite is green), so it fails here and no PR opens;
- a proposal that pins **21** is exactly the state that goes red the moment the work lands.

So a pinned count makes the twenty-second instrument unlandable, in either order. That is a
deadlock in the machinery, not a disagreement about what the entrance should claim.

## What this changes

Two assertions in `src/lib/field/dossier.test.ts`, stated as the invariants they were always
testing, both derived from the mirror the page itself reads:

1. **one dossier per committed instrument** — now compares the dossier slugs against the mirrored
   instrument slugs (so a dropped or duplicated dossier still fails, which a bare count would not
   have caught either) and asserts the lengths match;
2. **leads with the instrument in service** — now asks this repository's own `orderInstruments()`
   for the newest instrument rather than naming last week's slug. The claim under test — the
   entrance leads with the newest, and exactly one is in service — is unchanged.

Everything else in the file, including the named numbering checks (`001`, `018`, `020`), the
verbatim-quote checks and the plate assertions, is untouched.

## Checked, in both states

| state | `dossier.test.ts` | full suite |
|---|---|---|
| this repository as it stands (21 instruments) | 46 passed | **105 files, 1,700 tests, all passed** |
| with our 22nd instrument integrated | 46 passed | 2 pre-existing failures gone; nothing new |

If you would rather keep a pinned count and update it by hand when a work lands, that is entirely
your call — in that case tell us and we will hold the work until you have done it, and we will not
file this again. This is an offer, not a claim on how your tests should read.
