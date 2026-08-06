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

## 3. P2 — HELD, and it is the session's finding

**156 of 166 unique (work, URL) pairs in the rendered `site` tier are displayed-only — 94.0 %.**
Predicted: at least 33 %.

Read off the committed source: of 21 shipped works, **one** — `2026-07-01-fairness-trap` —
hyperlinks any of its sources on its rendered page, ten of them. Every other work prints its
citations as text. Checked by hand against the source rather than taken from the extractor: the
`work.astro` files of `2026-07-01-the-edition`, `2026-07-01-digit-mirror` and
`2026-08-03-where-the-reader-declines` contain **no `href` at all**, and
`2026-07-01-calibration-gap`'s four `href`s are not citations.

What this licenses, in these words and no stronger: **on the face this archive renders, a reader
who wants to reach a source must copy a string, because in 94 % of cases there is nothing to
click.** It does not license "not clickable in a browser" — the extractor reads markup, not a
rendered page, and a link built by a client script would be invisible to it (`PREREGISTRATION-V2.md`
§5).

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
   **displayed-only 26.1 % (42 of 161) against linked 30.0 % (3 of 10): the gap reverses direction
   and falls under the threshold.**

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
> reader actually sees, 94 % of its sources are text to be copied rather than links to be
> followed.**

## 9. What this instrument now owes

1. **D5** (§2) — an identifier withdrawn in one work is re-admitted to the census by an unmarked
   occurrence in another. Architectural; unfixed.
2. **A1 is not fit to ship** (§6) — two of three removals are false. Either it is narrowed until it
   is right, or it is withdrawn and D1 is left standing as a known, disclosed defect.
3. **A fresh gauntlet.** No Verifier and no Skeptic has ever ruled on this instrument, in either
   version.
4. **A decision on form**, still open, and deliberately not taken this session (see the journal).
