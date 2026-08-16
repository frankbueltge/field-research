# What this bundle cannot show

*Version 0.3, 2026-08-16. This file is load-bearing. If you re-use anything from this bundle, this
page travels with it. Everything below is a present-tense limit of the measurement, not a
future-tense hedge about work someone might do later.*

---

## 1. `NOT-RETRIEVABLE` does not mean deleted

The endpoint this bundle uses answers a refusal with a **single opaque HTTP 400**, and that code
is semantically empty. A three-arm control run on 2026-08-11 with twenty synthetic identifiers
that never existed returned exactly the same code as identifiers that certainly did exist, and
**no HTTP 404 was ever returned** in any run of this instrument.

So `NOT-RETRIEVABLE` means, exactly and only:

> not publicly retrievable through this endpoint, from this network vantage, at that moment.

It does not mean deleted, removed, moderated, geo-blocked or made private. Those are different
claims and this instrument cannot tell them apart. A derived headline that drops this caveat is
measuring something it cannot name.

## 2. One vantage, one endpoint

Every run is taken from **one** network vantage (autonomous system AS396982, United States —
logged into every run file before the first measurement request) through **one** credential-free
endpoint. A result that differs from another vantage is not a contradiction of this bundle; it is
a second reading this bundle cannot make.

## 3. The population is a cited population, not a sample of the platform

The panel is videos **cited in public** — in the article and non-article namespaces of language
editions of one encyclopedia, and posted to one public technology forum. Videos that nobody cited
are not in it and nothing here describes them. **A yardstick cited without its population is a
verdict wearing a yardstick's clothes:** any expected-absence figure taken from this bundle
carries the population, the run identifier and the date that produced it.

## 4. Six events is not a rate

The whole panel has produced a handful of confirmed state changes across its measurement days
(§3 of `README.md`). That is a count of events, not a hazard, and no reuse may render it as one.
Reading a single cross-section's age gradient forward as a rate of disappearance is a claim this
practice has made in public and **withdrawn in public**.

## 5. The reference table has a date, and using it later is an error that grows

This table is a measurement of one population on one day. A tool that ages a caller's list at
**today** and looks the result up here is doing arithmetic against a clock that stopped. The size
of that error was measured before it was disclosed (`reference-drift.json`): **0.2264 pp** after a
month of shelf-life and **2.4225 pp** after a year, on the reference population itself.

That drift is **arithmetic, not a forecast.** Nothing was re-measured at any horizon. It says how
far the printed expectation moves as the table ages, not what retrievability does.

**Corrected here, and it is a correction to this practice's own words.** Version 0.1 of this
file said a 26-day threshold in the tool was the point past which drift exceeded the largest
defect this practice had caused, and the tool warned past it. That claim was **withdrawn** at the
gauntlet of 2026-08-16: the crossover is a family of values running from 1 day to 26 depending on
which comparand is chosen, the comparand was chosen after the fact, and 26 was the most forgiving
member. The fixed threshold is **deleted** from the tool. Version 0.3.1 instead reports the
caller's own drift, computed on the caller's own list, and refuses to print a drift at all when
the two readings it would compare have different denominators.

## 6. Ages are decoded, not looked up

Creation times are decoded from the identifier itself under the platform's modern 19-digit scheme
(the high 32 bits are a Unix timestamp), checked against the endpoint's own returned metadata
where that metadata exists. Identifiers that are not 19 digits carry no age, stay in the series,
and are excluded from every age-banded rate.

## 7. Two arms are excluded from every rate, by design and in advance

A control arm of display-truncated identifiers that are **not** videos is excluded from every
rate and reported separately — including it would manufacture absence. Observations that failed
in transport (`INDETERMINATE`) are excluded and counted, never imputed.

## 8. The raw record is primary and is never edited

`states` in `presence-series.json` is what the instrument returned. `states_corrected` applies an
overlay of readings this practice's own confirmation step refuted with 5 immediate
re-requests. **No archived run file is ever edited**, and where the two arms differ, both are
published.

## 9. What this bundle is not

It is the **control arm** of a two-sided comparison: what was publicly retrievable, measured
without any credential. It is **not** an audit of any research interface, it makes no claim about
what any credentialed interface returns, and it cannot on its own show that any platform's
coverage claim is false. What it can do is give a reading of a research interface something to be
compared against.
