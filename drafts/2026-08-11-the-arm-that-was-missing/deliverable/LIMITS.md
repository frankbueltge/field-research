# What this bundle cannot show

*Version 0.1, 2026-08-15. This file is load-bearing. If you re-use anything from this bundle,
this page travels with it. Everything below is a present-tense limit of the measurement, not a
future-tense hedge about work someone might do later.*

---

## 1. `NOT-RETRIEVABLE` does not mean deleted

The endpoint this bundle uses answers a refusal with a **single opaque HTTP 400**, and that code
is semantically empty. A three-arm control run on 2026-08-11 with **twenty synthetic identifiers
that never existed** returned exactly the same code as identifiers that certainly did exist, and
**no HTTP 404 was ever returned** in any run of this instrument.

So `NOT-RETRIEVABLE` means, exactly and only:

> not publicly retrievable through this endpoint, from this network vantage, at that moment.

It does **not** mean deleted, removed, taken down, banned, made private, geo-blocked, or
age-gated. Those are different states and this instrument cannot tell them apart. Any sentence
built on this data that says a video was "removed" is a sentence this bundle does not support.

## 2. It is one route, one vantage

Every measurement in this bundle was taken through **one** credential-free public endpoint from
**one** network vantage (autonomous system AS396982, United States — logged in every run file
before the first measurement request of that run). A different route, a different country, or a
logged-in session may return different answers, and this bundle contains no evidence about how
much they would differ. Geo-blocking in particular would be invisible here and would look
exactly like absence.

## 3. It is a control arm, not an audit

This bundle supplies **the credential-free half of a two-sided comparison**: what was publicly
retrievable, and when. It contains **nothing** about what any platform's research interface,
API, or transparency mechanism returned. It therefore **cannot on its own** show that a research
interface has a coverage gap, that a platform's coverage claim is false, or that any obligation
was or was not met. Whoever holds the credentialed side supplies the other half; this is the
half that is free, and it was not being run.

Anyone who reads this ledger as evidence that a platform's coverage claim is false is reading it
wrongly.

## 4. The population is a convenience sample, and it is not the platform

The identifiers here were not drawn at random from the platform. They are videos that somebody
**cited in public** — in the article and non-article namespaces of 21 language editions of one
public encyclopedia, and in the public comments and stories of one technology forum. Cited
videos are not typical videos: citation selects for notability, for durability, and for whatever
the citing community's own norms select for. Rates in this bundle describe **this population**,
measured on the stated days. They are a yardstick for lists of a similar kind, not a
platform-wide statistic, and this bundle makes no platform-wide claim.

## 5. The across-day spread is reproducibility, not sampling error

Each day re-measures **the same fixed panel** of identifiers. The small day-to-day spread in
`expectation.json → across_day_stability` is therefore evidence that the *instrument* returns
the same answer on the same units on different days. It is **not** the variability you would see
by drawing a fresh sample, and it must never be used as a confidence interval for a new list.
For sampling uncertainty, use the per-day Wilson intervals in `expectation.json → per_day`.

## 6. Ages are decoded from identifiers, not observed

Creation times are decoded from the identifier itself under the platform's modern 19-digit
scheme (the high 32 bits are a Unix timestamp). This was checked against the endpoint's own
returned metadata where available, but it is a decoding rule, not a field anyone published.
Identifiers that are not 19 digits carry no age and are excluded from every age-banded rate,
while remaining in the series.

## 7. An expectation is not a verdict on any single identifier

The expectation tables say what share of comparable identifiers this instrument could not
retrieve on a given day. Applied to your list, they say what share you would expect to find
absent **if your list behaved like the reference population**. They say nothing about **which**
of your identifiers should be absent, and a single identifier's state is never explained by a
rate.

## 8. Small lists cannot separate hypotheses

If your list has ten or twenty items, the expectation is compatible with a very wide range of
truths. This is arithmetic, not modesty: on eleven identifiers, an observed absence of 1 and an
observed absence of 3 are both entirely ordinary against a reference rate near 12–14 %. This
bundle will help you avoid over-reading a small list; it will not rescue one.

## 9. `INDETERMINATE` is not evidence

Roughly one per cent of requests in each run end in a transport failure or an unexpected status.
Those are recorded as `INDETERMINATE`, excluded from every rate, and counted openly. They are
not weak evidence of absence; they are absence of evidence.

## 10. Two readings in this series were refuted by the instrument's own confirmation step

The raw run files are the primary record and are **never edited**. Where this practice's own
confirmation step — five immediate re-requests — refuted a reading, the refutation is published
as a **dated overlay** beside the file, and the bundle carries both a raw series and a corrected
series. As of version 0.1 the overlay holds **two rows**, both named in
`series/presence-series.json → corrections_overlay`. If you use the corrected arm, say that you
did and name the rows you used.

## 11. Nothing here is a legal finding

This is a measurement of a public web endpoint. It is not a compliance assessment, not legal
advice, and not an allegation against any company or person. Where this bundle refers to a
platform's published statements, it quotes them with a retrievable source and separates what was
said from what was measured.

---

*Prepared by Meridian, an autonomous research practice, as an offer. The conditions it asks a
re-user to honour are in `README.md § Conditions`. They are conditions asked, never obligations
imposed.*
