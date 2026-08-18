# What this bundle cannot show

*Version 0.3.3, 2026-08-16. This file is load-bearing. If you re-use anything from this bundle, this
page travels with it. Everything below is a present-tense limit of the measurement, not a
future-tense hedge about work someone might do later.*

---

## 1. `NOT-RETRIEVABLE` does not mean deleted

The endpoint this bundle uses answers a refusal with a **single opaque HTTP 400**, and that code
is semantically empty. A three-arm control run on 2026-08-11 with twenty synthetic identifiers that never existed returned
that same code — **nineteen of the twenty** did; the twentieth returned **no code at all**, a
transport failure, which is the absence of a code rather than the same one (first gauntlet, E1).
**No HTTP 404 was ever returned** in any run of this instrument.

So `NOT-RETRIEVABLE` means, exactly and only:

> not publicly retrievable through this endpoint, from this network vantage, at that moment.

It does not mean deleted, removed, moderated, geo-blocked or made private. Those are different
claims and this instrument cannot tell them apart. A derived headline that drops this caveat is
measuring something it cannot name.

## 2. One vantage, one endpoint

Every run is taken from **one** network vantage (autonomous system AS396982, United States).
The vantage is logged into each daily run file before that run's first measurement request, with
**one** exception the manifest names: the baseline entry is a union of component runs, and its own
vantage field says the vantage was *carried from the producing runs* rather than logged before a
first request (first gauntlet, E2). Every run uses **one** credential-free endpoint. A result that differs from another vantage is not a contradiction of this bundle; it is
a second reading this bundle cannot make.

## 3. The population is a cited population, not a sample of the platform

The panel is videos **cited in public** — in the article and non-article namespaces of language
editions of one encyclopedia, and posted to one public technology forum. Videos that nobody cited
are not in it and nothing here describes them. **A yardstick cited without its population is a
verdict wearing a yardstick's clothes:** any expected-absence figure taken from this bundle
carries the population, the run identifier and the date that produced it.

## 4. 7 events is not a rate

The whole panel has produced **7** apparent state changes across its measurement days,
of which **5** survived immediate re-request (the section of `README.md` headed *The
measurement that refuted version 0.1*). That is a count of events, not a hazard, and no reuse may render it as one.
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

## 6. Small lists cannot separate hypotheses

On a list of a dozen identifiers, this bundle can tell you how far your count sits from what a
reference population of that age showed — and it cannot tell you why. An observed absence of one
and an observed absence of three are both entirely ordinary against a reference rate near
12.18 %. **Any reading of a short list is an expectation, never a verdict on any identifier**,
and it cannot distinguish removal from a private account, a geo-block, a rename or a network
refusal. This section existed in version 0.1 under a different number, was lost when this file was
rewritten, and is restored here as a dated correction rather than quietly re-added.

## 7. Ages are decoded, not looked up

Creation times are decoded from the identifier itself under the platform's modern 19-digit
scheme (the high 32 bits are a Unix timestamp). **They are not checked against anything the
endpoint returns**: this probe stores no creation time from the endpoint, so no such check exists
and none is claimed (first gauntlet, E3). Identifiers that are not 19 digits carry no age, stay in the series,
and are excluded from every age-banded rate.

## 8. Two arms are excluded from every rate, by design and in advance

A control arm of display-truncated identifiers is excluded from every rate and reported
separately, because including it would manufacture absence. It is **not** the case that every
member is certainly not a video: **248 of 249 do not resolve, and one is a real video**
predating the platform's current identifier scheme (first gauntlet, E7). Observations that failed
in transport (`INDETERMINATE`) are excluded and counted, never imputed.

## 9. The raw record is primary and is never edited

`states` in `presence-series.json` is what the instrument returned. `states_corrected` applies an
overlay of readings this practice's own confirmation step refuted with 5 immediate
re-requests. **No archived run file is ever edited**, and where the two arms differ, both are
published.

## 10. What this bundle is not

It is the **control arm** of a two-sided comparison: what was publicly retrievable, measured
without any credential. It is **not** an audit of any research interface, it makes no claim about
what any credentialed interface returns, and it cannot on its own show that any platform's
coverage claim is false. What it can do is give a reading of a research interface something to be
compared against.

<!-- SESSION-126:PANEL-DATE:BEGIN - generated by session126_sections.py; do not edit by hand -->

## 11. The panel has no recorded construction date, and this is the width of that gap

*Added 2026-08-18. This is the blocking objection of the gauntlet of 2026-08-17, conceded in full. It is a property of the sampling frame, not a wording defect, and it cannot be closed by re-measuring anything.*

Every age-banded figure in this bundle rests on a panel of cited identifiers, and **no record of when that panel was collected exists anywhere in this arc.** 47 corpus files were examined and 1 carries any timestamp at all — and that one is the *newest citation in the pool*, not the moment the pool was pulled.

The record can only bracket it. The pull is at or after **2026-08-01T22:33:14+00:00** (it cannot precede its own newest row) and before **2026-08-11T11:24:06Z** (the first completed run over the panel): a window of **9.5353 days**. Until a collection time is recovered, that bracket is the honest statement of this panel's date, and it travels with any reuse of an age-band cell, an age-gradient row or an expectation figure.

**And a confound is open that this bracket does not close.** Encyclopedia editions prune and archive-fix dead citations, and they do so at rates that are themselves a function of how long a citation has sat — *the same axis the age table is built on*. So a rising absence rate with age is consistent with two different stories that this bundle cannot separate: videos going away, or citation lists being maintained. **This is a candidate explanation distinct from platform-side removal, and no robustness check in this arc addresses it.** The arithmetic is not in question; the representativeness is. The age gradient is what this specific, undated snapshot showed on the dates measured, and it is **not** a general yardstick for cited videos of a given age.

The asymmetry is worth stating against ourselves: this arc dates its reference clock to the second, measured a bookkeeping drift in that clock to four decimals, and published a table of how far it moves per month — while the clock behind the population every one of those figures rests on was never written down.

<!-- SESSION-126:PANEL-DATE:END -->
