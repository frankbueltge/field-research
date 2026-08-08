# PRE-REGISTRATION — increment 3: does the printed date move when the document's own text changes?

*Session 102, 2026-08-08. Written and committed **before `measure3.py` existed**, as at sessions 100
and 101. Everything below — population, sample, extraction rules, classification thresholds,
predictions and the decision rule — is fixed here and is scored exactly as written in `RESULT-3.md`.
Anything this session learns afterwards goes in `PROBES.md` or `CORRECTIONS.md`, never into this file.*

## 0. What this increment is for, and what it deliberately is not

Increment 2 established that the public capture record can hold **a document against itself**: 223 of
236 measured document pages (94.5 %) have two captures at least 30 days apart. It did not measure a
single date. This increment does.

It measures the **V arm only** — the date a page prints for a human about itself, against that page's
own text, between two archived captures of the same document. **The H arm (`Last-Modified`) stays
parked**, because `RESULT-2.md` names a debt that gates every H claim in this arc — whether the
archive's pipeline can preserve a stale or conditional-request-derived `Last-Modified` — and no
session has run it. The V arm does not depend on that pipeline: the printed date is in the page body
the archive replays.

**The population is chosen to answer the adversary's charge 6** (`INTERLOCUTOR-2.md`): the receiver's
standard says it applies to *"Executive branch agency websites and digital services that are intended
for use by the public"*. **NIST** (Department of Commerce) and **EPA** are exactly that; the
receiver's own 16-page meta-site is not, and it is **excluded from every scored prediction below**.
**GOV.UK is not in the standard's scope and is not treated as if it were** — it is here for one
methodological job named in §4: it is the only authority in this house's corpus that publishes its own
change history, so it is the only place where this instrument's content-change detector can be scored
against a publisher's own account of what changed.

## 1. Population and sample — fixed here

From `census.json` (increment 2, seed 20260808), taking rows **in the order the census recorded
them**, restricted to rows with `pairable == true`:

| authority | frame | n |
|---|---|---|
| NIST `www.nist.gov/publications/` | census `authorities.nist` | first **40** pairable |
| EPA `www.epa.gov/newsreleases/` | census `authorities.epa` | first **40** pairable |
| GOV.UK `www.gov.uk/government/publications/` | census `authorities.govuk` | first **30** pairable (calibration arm only) |

**110 URLs, 220 archive fetches.** No new timemap queries: the pair is taken from the capture
timestamps the census already recorded (`first`, `last` — first and last 200-status capture in
2024-08-01…2026-07-31, span ≥ 30 days). Sample size is set by the rate limit increment 2 hit at
roughly 250 archive queries, not by a power calculation, and that is a limitation of this increment.

**Fetch route:** `https://web.archive.org/web/<ts>id_/<url>` — the raw original payload, no archive
banner — with the gzip/deflate decoding fix from increment 1's defect D1 applied by magic bytes.
1.5 s between fetches, single-threaded. **A URL whose two fetches do not both succeed is reported as
unmeasured and excluded from every denominator; it is never imputed** (increment 2's rule).

## 2. What is extracted from each capture — fixed here

**(a) The printed date V, by an explicit per-authority selector, not by a general heuristic.** This
is deliberate: kill criterion (d) in `CONCEPT.md` says a per-authority V claim is illegitimate unless
V's *referent* is established outside EC, and increment 1's defect D3 came from a general extractor
reading a listed item's date. Selectors were read first-hand off one live page per authority today,
before this file was written:

- **NIST** — the element whose text matches `Created <date>, Updated <date>`; V is the **Updated**
  half. (Live example: `<div class="text-italic font-sans-2xs">Created December 1, 1992, Updated
  November 10, 2018</div>`.)
- **EPA** — the element with class `l-page__footer-last-updated`, text `Last updated on <date>`.
  (Live example: `Last updated on August 17, 2023`.) EPA's `<time datetime=…>` near the headline is
  the **release** date, is not an update date, and is recorded separately as `v_published`, never
  scored as V.
- **GOV.UK** — the `<time class="gem-c-published-dates__change-date">` values and the `Published
  <date>` line inside the published-dates block; V is the **latest change date**.

If the selector finds nothing on a capture, V is `null` for that capture and the pair is
**UNSCORABLE for V**, reported as such.

**(b) The content text, with the dates removed from it.** The subtree of the authority's content
container (NIST `nist-page__region--content`; EPA `<main id="main">`; GOV.UK `<main id="content">`),
with `script`, `style`, `nav`, `form`, and the date-bearing blocks themselves removed (NIST's
`Created…Updated…` line; EPA's `l-page__footer-last-updated`; GOV.UK's `gem-c-metadata`,
`gem-c-published-dates` and `full-publication-update-history`), then: hex-like tokens of ≥ 16 chars
removed (cache busters), **every date-shaped string removed** (`Month D, YYYY`, `D Month YYYY`,
`YYYY-MM-DD`), whitespace collapsed.

**Removing the dates from the compared text is not cosmetic and is fixed here as a rule:** if the
printed date stayed inside the compared text, a page whose *only* change was its date would be scored
as a content change, and the instrument would confirm its own hypothesis by construction. This
increment must be unable to do that.

**(c) Classification of a pair**, on that date-stripped text:
`IDENTICAL` (sha256 equal) · `TRIVIAL` (similarity ratio ≥ 0.98) · `SUBSTANTIVE` (ratio < 0.98).
V is `MOVED` if the two normalised V strings differ, `STILL` if equal, `UNSCORABLE` if either is null.
The 0.98 threshold is inherited unchanged from increment 1 so the two increments stay comparable.

**(d) GOV.UK only:** every declared change event (timestamp + note) inside the published-dates block
of the *later* capture, used in §4.

## 3. Predictions — NIST and EPA, the population the standard governs

- **P11 (the referent).** The fixed selector locates a self-referential update date on **≥ 90 %** of
  successfully fetched capture pages, for NIST and for EPA **separately**. *If P11 fails for an
  authority, this instrument cannot make a V claim about that authority at all and must say so on its
  face rather than in a caveat (kill criterion (d)).*
- **P12 (the headline, the failure direction).** Among pairs classified `SUBSTANTIVE`, pooled over
  NIST + EPA, the printed date is `STILL` in **≥ 25 %** of pairs.
- **P13 (the false-alarm direction).** Among pairs whose date-stripped content is `IDENTICAL`, pooled
  over NIST + EPA, the printed date `MOVED` in **< 10 %** of pairs.
- **P17 (the anti-contamination check, and it is an obligation, not only a prediction).** Twenty pairs
  classified `SUBSTANTIVE` — or all of them if there are fewer than twenty — sampled by
  `random.Random(20260808).sample` over the sorted pair keys, have their diffs **read by hand** and
  judged against the receiver's own words (*"a substantive change is one that impacts the information
  in a way that is relevant to your audience"*). Prediction: **≥ 60 % are genuinely substantive.**
  *If under 60 %, the class is contaminated as it was at increment 1 and **no fidelity number from
  this increment ships** — the finding becomes a methods finding about the detector.*

## 4. Predictions — GOV.UK, the calibration arm only

GOV.UK publishes the publisher's own account of what changed, so it can score this instrument's
detector rather than the publisher's honesty. Only pairs where the later capture's change history is
readable are scored.

- **P14 (sensitivity).** Among GOV.UK pairs with **≥ 1 declared change event strictly inside** the
  pair's interval, this instrument classes the pair as changed (`TRIVIAL` or `SUBSTANTIVE`) in
  **≥ 70 %**.
- **P15 (specificity).** Among GOV.UK pairs with **no declared event inside** the interval, this
  instrument classes the pair as changed in **< 30 %**.

No claim about US federal compliance is made from GOV.UK data, in this file or in `RESULT-3.md`.

## 5. The arc-killer, fixed before the numbers exist

- **P16.** If, pooled over NIST + EPA, `SUBSTANTIVE`-and-`STILL` is **< 5 %** *and*
  `IDENTICAL`-and-`MOVED` is **< 5 %**, then the printed date is faithful on the population the
  standard governs, **the core claim of `CONCEPT.md` is false**, and the arc ends in a published
  **negative** finding — not a per-authority profile, and not a quiet re-scoping.

## 6. The decision rule for the gate — fixed before the numbers exist

This is gate session **3 of at most 3**. `RESULT-2.md` bound this session to answer the adversary's
charges 4 and 6 or discard the concept with a one-page finding. The rule:

1. **P11 fails on both NIST and EPA** → the V arm is unmeasurable on the governed population → the
   concept is **rewritten as a coverage finding and discarded** with one page.
2. **P17 fails** (< 60 % genuinely substantive) → no fidelity number ships; the gate does **not**
   pass; what survives is a methods finding about the detector, and the arc parks.
3. **P16 fires** → the arc ends with a negative finding, published; the concept as written is
   **falsified**, which is an outcome, not a failure.
4. **Otherwise** — a per-authority fidelity number exists on the governed population, and the gate
   passes **only if** charge 4 is also answered in one page from the receiver's own text, and the
   Interlocutor convened today does not refute the gate claim. Charge 6 is answered by this
   increment's population or not at all.

The one thing this increment cannot do is make charge 4 go away by arithmetic. That is answered in
`CHARGE-4-AND-6.md`, from the receiver's own page, and it is answerable in the negative.
