# PRE-REGISTRATION — increment 3B: what does the printed date resolve?

*Session 102, 2026-08-08. Written and committed **before `measure3b.py` existed**, after
`BLOCKED-3.md` established that the pre-registered increment 3 cannot run. Scored exactly as written
in `RESULT-3.md`. `PREREGISTRATION-3.md` is not revised and none of its predictions are scored.*

## 0. The idea, and why it survives without an archive

Increment 3 asked: *when the content changes, does the printed date move?* — a question about two
observations of one page over time, which is why it needed capture history. **This increment asks a
question that one observation of many pages can answer**, and it is a necessary condition of the
same promise:

> If the date a page prints about itself is reporting **that page's own** last substantive change,
> then unrelated documents — different authors, different subjects, published years apart — have no
> reason to carry the **same** printed update date.

So: fetch many unrelated documents from the same authority, **live, today**, and look at how many
distinct printed update dates there are. A date that hundreds of unrelated documents share to the
day is not resolving those documents. It is resolving something else — a migration, a template
change, a bulk re-publication.

This is the *human-visible printed* date, which `CONCEPT.md` §4 identified as the least-studied of
the three signals and which the receiver's **binding** acceptance criterion is about.

**The interpretation limit, fixed here before the numbers exist, because it is the obvious
counter-attack:** a shared date does **not** prove the pages did not change that day. A site-wide
migration genuinely touches every page, and a publisher who stamps every touched page is following
the letter of an implementation tip. What a shared date *does* establish is narrower and is all this
increment will claim: **as deployed, the printed indicator cannot distinguish a document's own
substantive change from a site-wide operation** — and a reader cannot tell which one they are looking
at. `RESULT-3.md` may not state it more strongly than that sentence.

## 1. Population — chosen to answer the adversary's charge 6

The receiver's standard applies to *"Executive branch agency websites and digital services that are
intended for use by the public"* (fetched today; §3 below).

**In scope, and the only authorities any claim is made about:**

| authority | frame | n |
|---|---|---|
| **NIST** `www.nist.gov/publications/` | `census.json → authorities.nist` (seed 20260808, increment 2) | **80** |
| **EPA** `www.epa.gov/newsreleases/` | `census.json → authorities.epa` (same seed) | **80** |

**The positive control, explicitly not in the standard's scope and never treated as if it were:**

| **GOV.UK** `www.gov.uk/government/publications/` | `census.json → authorities.govuk` | **80** |

GOV.UK prints an update date that is generated from a publisher-maintained change history with
per-event notes (probe B, session 101: 80/80 documents have one). It is here to answer the question
*"can this test detect a document-specific date when one exists?"* If GOV.UK's distinct-value ratio
is not high, **the method is broken and no NIST/EPA number is reported** — that is a falsifier for
the instrument, stated before it runs.

## 2. What is extracted — one live fetch per URL, no archive

Selectors are those read first-hand off one live page per authority today and already fixed in
`PREREGISTRATION-3.md` §2(a):

- **NIST** — `Created <date>, Updated <date>`; `v_updated` is the Updated half, `v_created` the other.
- **EPA** — the element with class `l-page__footer-last-updated` (`Last updated on <date>`);
  separately, the release `<time datetime=…>` near the headline as `v_published` — **never scored as
  the update date**.
- **GOV.UK** — the latest `gem-c-published-dates__change-date`; `Published <date>` as `v_published`.

Fetch: live HTTPS, 0.7 s apart, single-threaded, one attempt plus one retry. **A URL that does not
return HTTP 200 with the selector matching is reported as unmeasured and excluded from every
denominator; it is never imputed.**

Definitions, fixed:
- **distinct-value ratio** = distinct `v_updated` values ÷ measured pages.
- **modal share** = pages carrying the single most common `v_updated` ÷ measured pages.
- **cross-year sharing** = share of measured pages whose `v_updated` is shared with ≥ 1 other
  measured page whose own `v_published`/`v_created` falls in a **different calendar year**.

## 3. Predictions

**In scope:**

- **Q1 (EPA cross-year sharing) ≥ 50 %.**
- **Q2 (EPA modal share) ≥ 20 %.**
- **Q3 (NIST cross-year sharing) ≥ 40 %.**
- **Q4 (resolution)** distinct-value ratio **< 0.6** on NIST **and** on EPA.
- **Q6 (validity)** fewer than **2 %** of measured pages carry a `v_updated` in the future relative
  to the fetch date, or (NIST) earlier than their own `v_created`. This is increment 1's defect-D2
  test, kept as a standing check on the extractor rather than on the publisher.

**The positive control:**

- **Q5 (control)** GOV.UK distinct-value ratio **> 0.8** and modal share **< 10 %**.
  *If Q5 fails, no NIST/EPA number is reported and the finding is about the method.*

**The falsifier for the whole test:**

- **Q7.** If NIST **and** EPA both show a distinct-value ratio ≥ 0.9 **and** modal share < 5 %, the
  printed update date is document-specific on the governed population, this test finds nothing, and
  that negative result is published as the increment's result.

**The obligation, not only a prediction:**

- **Q8 (hand-check).** For the largest cluster on each in-scope authority, **five** member pages are
  opened by hand and checked to be genuinely unrelated documents (different subjects, different
  publication years). Prediction: **≥ 4 of 5 on each authority are unrelated.** If a cluster turns out
  to be an artifact of the sample (e.g. all one series), the cluster is reported as such and not used.
  This is the standing answer to the contamination that sank increment 1 and to the adversary's
  charge 5: nothing counted here ships without something being read by hand.

## 4. What this increment does not do

It does not measure movement over time, so it cannot score `P12`/`P13` or replace increment 3; those
stay owed. It says nothing about `Last-Modified` (the H arm stays parked). It says nothing about
energy.gov, about any authority not listed, or about US federal compliance from GOV.UK data. And it
cannot, on its own, pass the gate: charge 4 is answered from the receiver's own text in
`CHARGE-4-AND-6.md` or it is not answered.
