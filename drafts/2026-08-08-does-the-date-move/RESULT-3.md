# RESULT — increment 3B: what the printed date resolves

*Session 102, 2026-08-08. Scores `PREREGISTRATION-3B.md` exactly as written. Data:
`observations-3b.json` (239 measured pages, one row each), `scored-3b.json` (the scoring and the
cluster listings), `run3b.log`. The increment this replaces, `PREREGISTRATION-3.md`, is **NOT RUN**
and none of its predictions are scored — the reason is documented first-hand in `BLOCKED-3.md`.
Unregistered work of the same session is kept out of the scored file and lives in §5 below.*

**Headline: on 329 NIST publication pages the date the page prints about itself takes only 24
distinct values, three of which cover 74.8 % of them — on documents published between 1982 and 2016.
On 80 EPA news releases the same measurement finds 61 distinct values in 80 pages, and we had
predicted the opposite, in writing, before the fetch. The instrument's positive control passed, so
the difference between the two authorities is a property of the authorities and not of the method.**

## 1. The scoreboard

| | prediction | value | verdict |
|---|---|---|---|
| **Q1** | EPA cross-year sharing ≥ 50 % | **11.3 %** | **NOT HELD** |
| **Q2** | EPA modal share ≥ 20 % | **3.8 %** | **NOT HELD** |
| **Q3** | NIST cross-year sharing ≥ 40 % | **87.3 %** | **HELD** |
| **Q4** | distinct-value ratio < 0.6 on NIST *and* EPA | NIST **0.177**, EPA **0.763** | **NOT HELD** |
| **Q5** | *control:* GOV.UK ratio > 0.8 **and** modal share < 10 % | **0.863** / **3.8 %** | **HELD** |
| **Q6** | validity violations < 2 % | **0 %** on all three | **HELD** |
| **Q7** | *falsifier:* the date is document-specific on both US authorities | — | **did not fire** |
| **Q8** | *obligation:* the largest cluster's members are read by hand, ≥ 4 of 5 unrelated | 24 of 24 unrelated (NIST) | **HELD** (see §3) |

**Three of seven predictions failed, and two of the three failures are about EPA.** That is recorded
first because it is the part a reader should weigh most: this session predicted EPA's printed date
would be a deploy artifact and it is not.

## 2. What was measured

One live fetch per page on 2026-08-08. No archive. **239 of 240 pages measured**; one NIST page's
selector did not match and is excluded from every denominator and never imputed.

| authority | in scope? | n | distinct values | ratio | modal value | modal share | cross-year sharing | publication years |
|---|---|---|---|---|---|---|---|---|
| **NIST** `/publications/` | scope yes, criterion unclear (§4) | **79** | **14** | **0.177** | 2017-02-19 | **30.4 %** | **87.3 %** | 1982–2015 |
| **EPA** `/newsreleases/` | **yes** — "News, press releases" | **80** | **61** | **0.763** | 2024-02-20 | 3.8 % | 11.3 % | 2019–2021 |
| **GOV.UK** *(positive control, out of scope)* | no | **80** | **69** | **0.863** | 2026-07-20 | 3.8 % | 21.3 % | 2003–2026 |

NIST's four largest values: **2017-02-19** (24 pages), **2018-11-10** (22), **2021-10-12** (13),
**2026-05-07** (8). Those four cover **85 %** of the sample.

**The control is what makes the NIST number readable.** GOV.UK generates its printed date from a
publisher-maintained change history, and the same instrument, run the same way in the same hour,
returns 69 distinct values in 80 pages there. So a low distinct-value ratio is something this
instrument *can fail to find* when the date is document-specific. It found it on NIST and not on EPA.

## 3. The hand-check, which was an obligation and not only a prediction

The pre-registration required the largest cluster's members to be **read**, because the previous
increment's central prediction died of exactly this: counting "changes" nobody had looked at. All
**24** members of NIST's 2017-02-19 cluster were listed and read. They are unrelated documents
published between 1982 and 2015 — among them a 1982 paper on security requirements for equipment
using the Data Encryption Standard, a 1997 report on a machine-checking experiment, a 2008 guideline
on cell phone and PDA security, a 2012 recommendation on a block cipher, a 2014 paper on X-ray and
optical spectroscopy of 19th-century Thai glass, and a 2015 users' guide to entropy-estimation tests.
**24 of 24 are unrelated documents. All print "Updated February 19, 2017".** Full listing:
`scored-3b.json → largest_cluster_members`.

EPA's largest cluster has only **three** members (all published within five days of each other in
January 2021), so the "five pages" the pre-registration asked for do not exist; all three are
reported instead, as the pre-registration required.

## 4. What this does and does not establish

**Does.** On the NIST arm, the printed update date is not resolving the individual document. A
reader of a 1982 paper and a reader of a 2015 users' guide are shown the same "Updated February 19,
2017". Whatever that date is reporting, it is not those two documents' separate histories.

**Does not — and this limit was fixed in the pre-registration before any fetch, not added now.** A
shared date does **not** prove those pages did not change that day. A site-wide migration genuinely
touches every page, and a publisher who stamps every touched page is following the letter of the
receiver's implementation tip. What the measurement establishes is exactly this and no more:

> **As deployed, the printed indicator cannot distinguish a document's own substantive change from a
> site-wide operation — and a reader cannot tell which one they are looking at.**

**Does not, either:** say anything about whether dates *move* when content changes. That question —
the one this investigation is named for — is still unanswered, and its evidence route was unavailable
today (`BLOCKED-3.md`).

**The scope caveat, volunteered.** EPA news releases are one of the six content types the receiver's
**binding** acceptance criterion names. NIST publication records are inside the standard's "Applies
to" line but are not obviously any of the six named types. **The effect is on the arm that is in the
standard's scope but not demonstrably in its criterion**, and the arm squarely inside the criterion is
the one where the date behaves well. `CHARGE-4-AND-6.md` states this on its face.

**No claim about US federal practice is drawn from GOV.UK data**, here or anywhere in this draft.

## 5. Unregistered probe, reported separately — does the NIST result hold at scale?

Run **after** `scored-3b.json` was written, and kept out of it. **250 further NIST publication pages**
drawn with a recorded seed from the same 3,339-URL frame, disjoint from the scored 80.
**250 of 250 measured. 19 distinct values. Three values — 2017-02-19 (78), 2018-11-10 (55),
2021-10-12 (54) — cover 74.8 %.** Combined with the scored arm: **n = 329, 24 distinct values, top
three 74.8 %**. Data: `probe-nist-scale.json`. It is a probe, not a scored prediction, and it is
reported here so nobody has to take the 79-page result on trust.

## 6. Prior art, from an independent search pass

No published study, audit, government report or academic paper was found measuring the accuracy or
resolution of the **human-visible printed** update date on web pages, and no audit of compliance with
this draft standard was found. The closest precedent is a search-engine operator's post about a
**machine-readable sitemap field** — a different signal — reporting that a common failure is
identical values across many URLs; that source is set aside unused under the same house rule that
set it aside at session 100 (`CONCEPT.md` §4). A US government automated scanning programme covering
roughly 26,000 federal domains was found; **no timeliness field was visible in its documented sample
output, but the full field dictionary could not be retrieved, so this is recorded as unconfirmed and
nothing rests on it.** Documentation of how NIST's or EPA's printed date is generated could not be
found for either flagship site — so the *mechanism* behind the clusters is **not established**, and
this draft does not name one.

## 7. The gate

`CHARGE-4-AND-6.md` answers charge 6 by construction and **concedes charge 4**. What that concession
costs is recorded as `CORRECTIONS.md` C3: the word *compliance* is withdrawn from this
investigation's account of its own artifact. What this increment adds is a measurement that survives
the concession, on the population the standard governs, with a control that could have failed and did
not.

**The gate verdict, the Interlocutor's unedited verdict, and what the arc does next are recorded in
the session's minutes** (`journal/2026-08-08.md`, session 102) — not here, because they were decided
after this file was written.
