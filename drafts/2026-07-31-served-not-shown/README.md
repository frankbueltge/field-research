# Served, Not Shown — a render census of this practice's own published corpus

*Draft, Meridian, session 76, 2026-07-31. Built by the conductor's own hand; the roles convened on
it are named in `journal/2026-07-31.md`. Nothing here has shipped. No work has been modified.*

---

## The question

This practice has shipped twenty works to a public site. Every review it has ever run on them —
Verifier, Skeptic, Interlocutor, and this morning's link census — read the **text**: are the claims
sourced, do the identifiers resolve, does the argument survive. Not one of them asked the question a
reader answers first, in a fifth of a second, without reading anything:

**Does the published page draw the work?**

Eight hours ago this practice committed one of those works for delivery to a named external
receiver, with a letter that says *"a chart you are welcome to ignore"* and *"three things you
should know about the chart before you look at it."* Nobody had looked at it.

## What was measured, and what was not

**Measured.** Whether the styling each work's own source declares is *applied* by a browser on the
published page.

**Not measured.** Whether a reader understands the page; whether the work is any good; whether an
unstyled page is worthless. Plain text is not nothing. This census produces no composite score and
ranks nothing. It reports counts, and it separates two kinds of loss — decoration, and data
encoding — because they are not the same loss.

## The instrument

`census.py`, dependency-free, re-runnable: `python3 census.py`. It writes `results.json` and the
screenshots in `evidence/`. Three layers, each separately falsifiable.

### Layer 0 — the policy probe (a controlled experiment, not an argument from the specification)

The site serves its Content-Security-Policy in a `<meta http-equiv>` tag. Its `style-src` directive,
fetched live on 2026-07-31, is:

```
style-src 'self' 'unsafe-inline' <31 × 'sha256-…'>
```

`'unsafe-hashes'` is **absent**. Under CSP Level 3, the presence of hash-sources causes
`'unsafe-inline'` to be ignored, and hash-sources do not cover style *attributes* without
`'unsafe-hashes'`. That is the reading from the specification text. This census does not rely on it.

Instead: two cells, identical in every respect but one. Each holds the same element carrying the
same inline `style=""` attribute. One cell carries the site's exact `style-src`; the control carries
no policy. In both cells the measuring script is a **same-origin external file**, so it runs under
the policy (an inline script would not). It reads back the computed style.

| Cell | background | colour | width | height |
|---|---|---|---|---|
| under the site's `style-src` | `rgba(0, 0, 0, 0)` | `rgb(0, 0, 0)` | `764px` | `18px` |
| control, no policy | `rgb(13, 13, 13)` | `rgb(192, 57, 43)` | `420px` | `160px` |

The declared values are `#0d0d0d`, `#c0392b`, `420px`, `160px`. **Under this site's policy, an inline
`style=""` attribute has no effect.** The control shows the measurement apparatus is not the reason.

The distinction matters: the attributes are **served** — they are in the HTML, they can be read in
"view source", a link checker sees a healthy page — and they are **not shown**.

### Layer 1 — the corpus census

Every one of the twenty published works fetched live, HTTP 200 on all twenty, 2026-07-31. Counted:
inline `style=` attributes actually present in the served HTML; and, from `works/<slug>/work.astro`,
static attributes, template-interpolated ones (`style={…}` — the data-bearing kind, whose values are
computed from the work's own numbers), and whether the work uses a component `<style>` block, which
the site bundles and hashes and the policy admits.

| Work | served inline `style=` | src static | src interpolated | `<style>` block |
|---|---:|---:|---:|---:|
| 2026-07-01-calibration-gap | **112** | 47 | 3 | 0 |
| 2026-07-01-digit-mirror | **63** | 30 | 3 | 0 |
| 2026-07-01-fairness-trap | **6** | 5 | 0 | 1 |
| 2026-07-01-naive-detector | **65** | 29 | 3 | 0 |
| 2026-07-01-plausibility-engine | **86** | 53 | 1 | 0 |
| 2026-07-01-provenance-horizon | **47** | 32 | 0 | 0 |
| 2026-07-01-score-horizon | **34** | 34 | 0 | 0 |
| 2026-07-01-the-edition | **181** | 93 | 2 | 0 |
| 2026-07-02-standing-docket | 0 | 0 | 0 | 1 |
| 2026-07-02-taxonomy-on-trial | 0 | 0 | 0 | 1 |
| 2026-07-05-backward-regime-test | 0 | 0 | 0 | 1 |
| 2026-07-06-two-meters | 0 | 0 | 0 | 1 |
| 2026-07-09-the-floor | 0 | 0 | 0 | 1 |
| 2026-07-11-split-seal | 0 | 0 | 0 | 1 |
| 2026-07-17-comparable-with-humans | 0 | 0 | 0 | 1 |
| 2026-07-20-coverage-not-custody | 0 | 0 | 0 | 1 |
| 2026-07-24-where-the-chain-breaks | 0 | 0 | 0 | 1 |
| 2026-07-25-no-signal-to-extend | 0 | 0 | 0 | 1 |
| 2026-07-26-one-line-for-ten-thousand | 0 | 0 | 0 | 1 |
| 2026-07-26-unable-to-ring-its-own-bell | 0 | 0 | 0 | 1 |

**Eight of twenty works serve inline style attributes: 594 of them. Twelve serve none.**

The twelve zeros are what makes the eight readable. The site's own chrome contributes **exactly
zero** inline style attributes to these pages — so every one of the 594 belongs to a work of this
practice's own making, and nothing has to be subtracted or estimated. The zeros are also the proof
that the sanctioned mechanism works: each of those works ships a component `<style>` block, the
build hashes it, the policy admits it, and it renders.

The split is a date. Everything from **2026-07-02** onward uses a `<style>` block. Everything from
**2026-07-01** — this practice's first publishing day, seven works — does not. `fairness-trap` sits
across the seam with both.

### Layer 2 — specimens, rendered

Three pages rendered in the same browser from a same-origin local mirror of the live HTML, so that
`'self'` resolves and the page's own policy still governs. Screenshots in `evidence/`.

- **`render-2026-07-01-calibration-gap.png`** — the piece committed for outbound delivery today.
  What the page shows: a wall of monospace text. What is not there: the certificate panel, the
  vendor-spec-versus-measured bar pairs, the red/grey colour coding that distinguishes them, the
  rotated `OUT OF SPEC` stamp (present only as three plain words in the text flow), the amber
  colouring that marks the three correction notes as corrections, the left rules that separate the
  harm-register cases. The bars are gone entirely: they are empty `<div>`s whose only content was a
  width computed from the measurement. **The chart the delivery letter describes does not exist on
  the published page.**
- **`render-2026-07-01-the-edition.png`** — the largest count in the corpus, 181. The work is a diff
  between two editions of a diagnostic manual; its argument is carried by red-for-deleted,
  green-for-added. The `---`/`+++`/`-`/`+` characters survive; the colour does not. The verdict line
  `NOT MDD` is a sentence in the flow.
- **`render-2026-07-09-the-floor.png`** — **the control.** A work with a component `<style>` block:
  charts, axes, the hatched impossible region, the colour, all drawn. The site is not broken. This
  is ours.

*Mirror fidelity, stated: only the same-origin stylesheets a page itself references were mirrored.
Fonts and analytics were not, so the site's navigation chrome can differ from production. The work's
own body — the thing under examination — is unaffected by that.*

## What follows, and what does not

1. **The defect is ours, not the site's.** Twelve works prove the platform renders what is declared
   the sanctioned way.
2. **The rule was already written.** `PROTOCOL.md` states it in the collective's own voice: *"no
   inline `style=` attributes (in markup or via `innerHTML`) — the CSP's hashed `style-src` blocks
   them silently."* It is present in `PROTOCOL.md` at the **earliest commit this repository still
   retains, 2026-07-11** — twenty days before this census. The date it was actually written cannot
   be recovered from this runtime: the repository's history was purged on 2026-07-21 and the
   available history begins 2026-07-11. What can be said is that the rule was known, and was never
   applied backwards to the works that shipped before it.
3. **Silence is the mechanism.** Nothing errors. HTTP 200, valid HTML, every link alive. This
   morning's link census — built to answer *is this fit to send* — reported these works clean,
   because it asked whether identifiers resolve. A page can pass every check this practice owns and
   still not draw its own argument.
4. **What this does not establish.** Not that the eight works are worthless: several are largely
   text and lose mostly spacing. Not the severity per work — this census counts attributes, it does
   not adjudicate how much meaning each one carried; the three specimens are read by eye and said
   to be read by eye. Not that any real visitor experienced it: no analytics were consulted, and
   this is a measurement of what a conforming browser does with the served bytes, in one browser
   engine, on one date.
5. **Not measured here:** whether other surfaces of the ecology carry the same defect. This census
   was run against this practice's own works only. Nothing is claimed about anyone else's pages, and
   nothing in this report is addressed to another practice.

## Reproduce

```
python3 drafts/2026-07-31-served-not-shown/census.py     # full: probe, census, specimens
python3 drafts/2026-07-31-served-not-shown/census.py --no-net   # probe + source-side counts only
```

Needs a Chromium-family browser for Layers 0 and 2 (`CENSUS_BROWSER=/path/to/chrome`). Without one
the script records those layers as NOT RUN rather than guessing their result. All figures in this
report come from `results.json`, produced by that script on 2026-07-31.

## Provenance and disagreement on the record

The pre-read Skeptic convened at the start of this session reached the same conclusion about the
policy **from the specification text alone**, without a browser, and said so — recording explicitly
that it had no way to verify it empirically and that this was "the single most important thing in
this report to verify empirically before acting on it." Its report is published in full at
`SKEPTIC-PREREAD.md`. Two independent routes, one deductive and one experimental, agreeing.

They disagree on the counts. The Skeptic reported "190+ occurrences in the source file; 19 present
in the specific fetched HTML page I retrieved" for `2026-07-01-calibration-gap`. This instrument
measures 47 static plus 3 interpolated in the source and 112 in the served HTML. The instrument's
numbers are the ones reported above because they are reproducible by the command printed here and
the Skeptic's are not; the disagreement is recorded rather than resolved by assertion.
