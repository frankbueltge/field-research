# The amended census, scored against what was predicted before it ran

**2026-08-06 (session 93). Conductor's own hand. Unreviewed at the time of writing — the gauntlet
is convened after it.** Every number below is read from `results/inventory.json`,
`results/controls.json` and `results/probe.json` in this directory, all committed. Nothing is
retyped from prose; where a figure is quoted it is quoted from those files.

This file does not edit `results/probe.json`, `PREREGISTRATION.md`, `PREREGISTRATION-V2.md` or
`FINDINGS.md`. The v1 record stands with its errors intact, which is the only reason this comparison
is worth anything.

---

## 0. What ran

| | v1 (2026-07-31) | v2 (2026-08-06) |
|---|---|---|
| corpus | 20 works, commit `0138e79d` | **21 works, commit `712a013`** |
| identifier occurrences | — | **865** |
| unique `evidence` URLs probed | 162 | **193** |
| controls | C1–C5 | C1–C5, unchanged; **99 hosts swept**, 5 answer 2xx to a nonsense path |
| stop rule | passed | **passed** — C1 fired `GONE`, C3 fired `SOFT-GONE` |
| census timestamp | `2026-07-31T04:16:41Z` | **`2026-08-06T03:54:26Z`** |

**This is a dated record. It expires on production.** It is not an assertion about this repository,
and no verdict here may be cited as a standing property of any work without a re-run.

## 1. The census

| verdict | n |
|---|---|
| `OK` | 121 |
| `BLOCKED` | 39 |
| `NOT-A-DOCUMENT` (new, A2) | 18 |
| `UNRELIABLE-OK` | 5 |
| `NOT-A-LOCATOR` | 4 |
| `NETFAIL` | 4 |
| `GONE` | **1** |
| `SOFT-GONE` | 1 |
| **total** | **193** |

**One `GONE` in the whole archive, and it is the identifier this practice itself withdrew and
published a correction for**: `https://doi.org/10.3030/101135953`. Its presence is the subject of §2.

`SOFT-GONE` is the already-known Kaggle deleted-dataset-version, disclosed by this practice on
2026-07-27. The four `NETFAIL`s were each re-checked from the second vantage the design requires,
and **the second vantage agreed with the first in all four cases**; two are the pair `FINDINGS.md`
§2 adjudicated by hand in v1 (`jabfm.org`, `marcellodibello.com` — both resolve with a `www.`
prefix), and two are new (`cambridge.org`, and a DOI that redirects to it), both read-timeouts
against the same host.

**Only 2 of 21 works come back with nothing but `OK`.**

## 2. P1 — REFUTED

P1 predicted all five v1 `GONE` would leave the bucket, each by the amendment naming it.

| v1 `GONE` | predicted by | v2 verdict | held? |
|---|---|---|---|
| `doi.org/10.3030/101135953` | A1 | **`GONE`** | **no** |
| `export.arxiv.org/api/query` | A2 | `NOT-A-DOCUMENT` (QUERY-ENDPOINT) | yes |
| `github.com/…/dataset-hub/blob/a7024008…/` | A2 | `NOT-A-DOCUMENT` (BASE-PATH) | yes |
| `raw.githubusercontent.com/…/a7024008…/` | A2 | `NOT-A-DOCUMENT` (BASE-PATH) | yes |
| `reuters.com/article/world/fact-check-…` | A3 | `BLOCKED`, status **401** | yes |

Four of five landed exactly where predicted, by exactly the named rule. **P1 is refuted by the
fifth**, and the reason is worth more than the prediction was.

**A1 did what it was written to do and it was not enough.** The occurrence D1 names —
`works/2026-07-01-fairness-trap/work.astro:590` — *is* reclassified `correction-record`; so are all
three occurrences in that work's `CORRECTIONS.md`. The DOI is nevertheless still in the census,
because a **different work** cites it as ordinary evidence:
`works/2026-07-26-unable-to-ring-its-own-bell/VERIFICATION-2026-08-04.md:68`, whose line reads that
the fairness-trap corrections entry *"independently confirms the DOI … / instrument 006 story"*.
That line carries no correction marker, so A1 cannot see it.

**The structural defect, stated as generally as the evidence supports it: role is assigned per
occurrence, and the census is keyed per unique URL.** A single unmarked occurrence anywhere in the
archive re-admits an identifier that another work has formally withdrawn. No refinement of A1's
marker list or scope can fix that, because it is not a marker problem. It is not fixed here; a rule
invented in the hour it is refuted is the thing this whole document exists to avoid. It is recorded
as **D5**, the first defect this instrument has found in its own architecture rather than in its
prose.

## 3. P2 — HELD as a bound, and corrected inside the session after the Verifier refuted its headline

**156 of 166 unique (work, URL) pairs in the rendered `site` tier are displayed-only by this
extractor's test — 94.0 %.** Predicted: at least 33 %. **P2 holds** on any reading below.

> **CORRECTED 2026-08-06, same session, on the Verifier's finding D, before landing.** This section
> first read: *"of 21 shipped works, **one** — `2026-07-01-fairness-trap` — hyperlinks any of its
> sources on its rendered page, ten of them. Every other work prints its citations as text"*, and
> claimed that `2026-07-01-calibration-gap`'s four `href`s "are not citations". **All of that is
> false, and the withdrawn wording is quoted here so it cannot read as a live assertion.** The
> Verifier read those four `href`s and found what they are: `href={c.source_url}`,
> `href={c.source_url_secondary}`, `href={sp.url}`, `href={s.url}` — **dynamic attribute bindings
> that render that work's citations, supplied from its `data.json`, as real links.** The extractor
> cannot see them, because the URL it finds sits in the data file with no link opener in front of
> it, and the opener sits in the component with no URL behind it. Neither half looks like a link on
> its own.

**What the correction costs, measured rather than estimated.** Checked by hand across all 21 works:
**four** carry dynamic `href={…}` bindings in `work.astro` — `2026-07-01-calibration-gap` (4),
`2026-07-06-two-meters` (3), `2026-07-09-the-floor` (3), `2026-07-11-split-seal` (1). Those four
works account for **45 of the 156 displayed-only pairs** (calibration-gap 24, the-floor 9,
split-seal 8, two-meters 4). Together with `2026-07-01-fairness-trap`'s ten literal links, **at
least 5 of 21 works render clickable citations, not one.**

**So 94.0 % is an upper bound on displayed-only, not a measurement of it.** Three further readings,
each computed and each stating what it assumes:

| reading | figure | what it assumes |
|---|---|---|
| as the extractor reports it | **156 / 166 = 94.0 %** | no binding is a link — known false |
| the Skeptic's, tracing `calibration-gap`'s `data.json` field by field: 14 URLs confirmed reaching a rendered `<a>` | **142 / 166 = 85.5 %** | only the 14 it verified are links |
| every pair in that one work counted as linked | **132 / 166 = 79.5 %** | its remaining 10 pairs are links too — unverified |
| every pair in all four binding works counted as linked — **the floor** | **111 / 166 = 66.9 %** | all 45 are links — an upper bound on the correction |

The Skeptic's second attack, computed independently and reproduced here to the digit: restricting
both sides to `work.astro`/`work.html` and dropping the data files gives **63 of 73 = 86.3 %** —
which is why the denominator objection was reported by the Skeptic itself as an attack that failed
to move the magnitude.

**The true figure lies between 66.9 % and 94.0 %, and the best-evidenced point in that range is
85.5 %.** This session did not narrow it further: doing so needs an extractor that resolves a
binding to its data field, which does not exist here and is not being written in the hour its
absence was found.

Still true, and hand-checked: the `work.astro` files of `2026-07-01-the-edition`,
`2026-07-01-digit-mirror` and `2026-08-03-where-the-reader-declines` contain **no `href` at all**.

What this now licenses, in these words and no stronger: **on the face this archive renders, between
two thirds and 94 % of its rendered-tier citations are text a reader must copy, and most of its
works give a reader nothing to click.**

**D6 — the extractor is blind to the archive's own dominant linking idiom.** A1's opener list can
match `href={"` and `href={'` but not `href={c.source_url}` — a bare expression with no quote after
the brace, which is how every one of these works links. The URL sits in the data file behind a JSON
key; the opener sits in the component with nothing behind it. **Neither half looks like a link on
its own, and the extractor only ever sees halves.**

The limitation was pre-registered — `PREREGISTRATION-V2.md` §5 concedes that a link the extractor
does not parse reads as `displayed` — and §3 then wrote a sentence that ignored the concession made
two files earlier. **The Skeptic's third attack sharpens even the concession, and it is right:** §5
named *a client script* as the blind spot, when the actual blind spot is **server-rendered
component templating, sitting in the committed source and fully checkable**. The disclosed limit
was not merely under-honoured by the prose; it was itself pointed at the wrong thing.

v1 could not have found this. Its every verdict was already a statement about a displayed string,
and it did not know that about itself until `FINDINGS.md` §2 stumbled on it.

## 4. P3 — HELD as written, and the practice does not believe it

Pre-registered: the non-`OK` share among displayed-only differs from the share among linked by
≥ 5 points.

**Displayed-only 37.7 % (69 of 183) · linked 30.0 % (3 of 10) · gap 7.7 points. P3 holds.**

It should not be reported as a result, for two reasons found after the number existed and stated
here rather than left for a reviewer:

1. **The linked arm is ten URLs, and all ten belong to one work.** A comparison whose treatment
   group is a single work's citations cannot support a claim about the archive.
2. **The gap is manufactured by the design buckets.** `NOT-A-DOCUMENT` and `NOT-A-LOCATOR` are
   assigned before any fetch and land only in the displayed-only arm. Removing the never-fetched
   categories and comparing fetch outcomes only — a post-hoc cut, labelled as such — gives
   **displayed-only 29.2 % (47 of 161) against linked 30.0 % (3 of 10): the gap reverses direction
   and collapses to 0.8 points, far under the threshold.**

   > **CORRECTED 2026-08-06, same session, on the Verifier's blocking finding 1, before landing.**
   > This paragraph first read *"displayed-only 26.1 % (42 of 161)"*. **That was wrong**, and the
   > withdrawn figure is quoted here so it cannot read as a live number. It came from a script that
   > counted `UNRELIABLE-OK` as `OK` in the post-hoc cut while the pre-registered figure above
   > counts it as non-`OK` — a definitional switch between two numbers printed side by side, made
   > by the conductor and disclosed nowhere. Under the strict `verdict != OK` rule used everywhere
   > else in this document, the five `UNRELIABLE-OK` records (all displayed-only) count against, and
   > the figure is 47 of 161. **The direction of the conclusion is unchanged; the number and the
   > count were both wrong.** Third session in a row on which this practice printed confident prose
   > over arithmetic it had not re-derived.

**So: P3 is scored HELD by its own written rule, and the claim it was written to license is not
supported.** The rule was met by an artefact of bucket assignment. That the pre-registered form and
the obvious alternative disagree in sign is the finding, and it is a finding against this design.

## 5. P4 — HELD

**`BLOCKED` = 39 of 193, 20.2 %** — 38 answering 403 and **one answering 401**, which is the
`reuters.com` article A3 was written for. One fifth of this archive's outbound citations remain
undecidable from where this practice stands, and the amendments did not convert that admission into
a pass.

## 6. What A1 removed from the census, probed anyway

A1 moved **49 identifier occurrences** out of their v1 role: **9 from `evidence`** and 40 from
`object-data` (all 40 in one single-line HTML specimen file, which is `sub` tier and was never
probed). The nine `evidence` moves are listed in full in `results/INVENTORY.md`.

Because publishing the list was A1's only promised defence, the nine were **probed as well** — not
part of the census, changing no census number, added after the change-list was seen and before the
census ran:

**6 `OK` · 2 `BLOCKED` · 1 `GONE`.**

Six of the nine identifiers A1 removed from the census were live and working. **That is A1's
false-positive rate, measured rather than feared: two thirds.** Of the nine, exactly one — the
`work.astro:590` DOI — is the case A1 was written for. The over-catching risk
`PREREGISTRATION-V2.md` §2 named as the amendment's own danger is real, it is the amendment's
dominant behaviour, and A1 as it stands is not fit to ship.

## 7. Custody is still thin, and the amendments did not touch it

At census level: **1 `HELD` · 32 `NOT-HELD` · 160 `NOT-AUTOMATICALLY-CHECKABLE`** of 193. Over the
69 structural bindings themselves: 2 `HELD`, 51 `NOT-HELD`, 16 `NOT-AUTOMATICALLY-CHECKABLE`.

In the same words v1 was obliged to use: **the custody layer of this instrument is thin, and its
`OK` means "something answered", not "the source still says what we said it says".**

## 8. The honest one-line reading, knowing that one line is a composite

A one-line summary of a 21-row table functions as a composite even though none was computed
(`PREREGISTRATION.md` §6). With that stated:

> **Nothing in this archive is dead except the one identifier the archive itself already
> retracted; one fifth of its citations cannot be checked from here at all; and on the page a
> reader actually sees, most of its sources are text to be copied rather than links to be
> followed — between two thirds and 94 % of them, best evidenced at 85.5 %.**

*(The sentence first written here ended "94 % of its sources are text to be copied". It is corrected
above on the Verifier's and the Skeptic's findings, both filed against §3, in the same session and
before landing. The withdrawn form is quoted so it cannot read as a live assertion.)*

## 9. A1 is withdrawn — the decision, and what it costs, in numbers

**Taken this session, on the Interlocutor's charge that reporting a defect had been substituted for
fixing one.** §6 measured A1 at a two-thirds false-positive rate and §9 first left the choice open.
Leaving it open is the evasion the charge names, so the choice is made: **amendment A1 is withdrawn.
D1 returns to being a known, disclosed, unfixed defect** — the honest state it was in before this
session, rather than a rule that suppresses two live citations for every correct one.

**What withdrawing it does to the census, computed rather than promised** (the eight identifiers A1
removed that are not otherwise in it re-enter, carrying the verdicts the §6 audit already
established for them):

| | with A1 (as run) | with A1 withdrawn |
|---|---|---|
| unique evidence URLs | 193 | **196** |
| `OK` | 121 | **122** |
| `BLOCKED` | 39 | **41** |
| `GONE` | 1 | **1** |
| everything else | unchanged | unchanged |

**The single `GONE` does not move**, because the identifier it names was already in the census by the
route D5 describes. **No headline in this document changes.** That is the strongest argument for the
withdrawal: A1 bought nothing and cost six live citations.

**The committed census stands as it was run, with A1 in it**, and is not re-run to match this
decision — a result recomputed to agree with a later choice is not a result. The next run of this
instrument runs without A1.

## 10. What this instrument still owes

1. **D5** (§2) — an identifier withdrawn in one work is re-admitted to the census by an unmarked
   occurrence in another. Architectural; unfixed, and not fixable by any marker rule.
2. **D6** (§3) — the extractor cannot see a data-bound `href={…}`, which is how this archive
   actually links. Until it can, every presentation figure here is a bound, not a measurement.
   > **ANSWERED 2026-08-07 (session 99) — see `RESULT-D6.md`; this file is not rewritten.** A
   > resolver now follows a binding back to the field it renders, and the served page was read to
   > grade it: **124 of 166 displayed-only, 74.7 %**, 42 links claimed and 42 found, zero
   > disagreements across the 18 works carrying a rendered-tier citation. **§3's "66.9 %" was not
   > a floor.** It assumed all 45 pairs in the four binding works are links; **32 are.** The true
   > value lies above that figure, and the reading labelled there as "an upper bound on the
   > correction" was wrong in the direction that flattered this archive. §3's range and its
   > 85.5 % point stand in this file as written, superseded rather than edited.
3. **A named outside audience.** The Production Amendment's concept gate requires one and this
   instrument has never had one. The Interlocutor's first charge, conceded without qualification.
4. **A decision on form**, still open. Not taken this session — see the journal, where the
   Interlocutor's charge that this is a standing permission slip is recorded and answered.
5. **A fresh gauntlet on the corrected state.** The verdicts this session earned were run on the
   state *before* §3, §4, §8 and §9 were corrected; by this practice's own rule they do not cover
   what now stands here.
