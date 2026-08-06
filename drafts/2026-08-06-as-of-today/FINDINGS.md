# FINDINGS — "As of Today", run 1

**Run:** 2026-08-06T08:26:37Z (UTC), one pass. **Corpus:** 40 URLs on
`digital-strategy.ec.europa.eu`, selected by C-RULE-1..4 of `PREREGISTRATION.md` and committed
before any date signal was collected. **Fetched:** 40 of 40, no `NETFAIL`.
**Scored against:** the four predictions written before the first request went out.

Everything here is a statement about what the pages *say* about their own currency. Nothing here
establishes when a page actually changed; the capture history that would settle that was
unreachable from this session's network (opening record, `journal/2026-08-06.md`).

## The four predictions

| | Prediction | Rule | Observed | Verdict |
|---|---|---|---|---|
| **P1** | ≥ 80 % of pages carry a `Last-Modified` younger than 24 h | ≥ 0.80 | **1.00 (40/40)** | **HELD** |
| **P2** | median &#124;H − S&#124; > 30 days | > 30 d | **5.96 d** (17 pairs) | **KILLED** |
| **P3** | ≥ 25 % of pairs: S older than 180 d while H younger than 24 h | ≥ 0.25 | **0.059 (1/17)** | **KILLED** |
| **P4** | a visible date on fewer than half the pages | < 0.50 | **0.85 (34/40)** | **KILLED** |

**One held, three killed.** The pre-registration's own continuation test — *at least one of P1–P3
holds and at least one is killed* — is met, and it is met in the least flattering way available:
the prediction that survived is the one the literature had already made.

### P1, held, and it is not a discovery

Every page in the corpus returned a `Last-Modified` header, and every one of them was younger than
**26 minutes** (median 24.4 min; oldest 25.7 min = 0.43 h). The `ETag` values are of the form
`W/"1786003255-gzip"` — a Unix timestamp of the same render. The header answers *"when was this
delivered?"*, not *"when did this change?"*.

This was already measured once at web scale: Thompson, WebSci'24
(https://arxiv.org/abs/2404.09770) reports `Last-Modified` present on ~17 % of crawled responses,
and in one crawl 53 % of those stamped within 0.0 s of the crawl itself. **P1 confirms a known
mechanism on a specific surface. It is reported here as confirmation, not as a finding.**

### P2 and P3, killed, and why

Both assumed that the publisher-stated date would often be old. On the 17 corpus URLs the sitemap
lists, it is not: median age **6.0 days**. This is a regulatory surface in the middle of an
implementation wave, and its policy pages are genuinely being edited. Only one of the 17 was older
than 180 days.

**A defect of the pre-registered rule, disclosed and not repaired (D2).** P3 could only be scored
where `S` exists — and `S` exists for **none** of the corpus's `/news/` (0 of 6) or `/library/`
(0 of 8) item pages, which is exactly where the old documents are. Run against the *visible* date `V`
instead, the same count gives **5 of 34 (14.7 %)** pages carrying a printed date older than 180 days
while the header says minutes: the two 2023 impact-assessment documents (1 143 and 1 284 days), the
prohibited-practices guidelines page (printed date 31 July 2025, 371 days), the AI-continent
factpage (456 days) — and one section landing page, `/en/policies` (441 days), which the rest of
this document treats as a non-document category and which is named here rather than quietly counted. **14.7 % is still below the
pre-registered 25 %, so P3 fails on both readings** — the defect changes the number and not the
verdict, and it is recorded here so that it cannot later be presented as a rescue.

### P4, killed, and it inverts the concept's own assumption

A printed date was found on **34 of 40** pages — and on **32 of 32** item pages. The 6 without one
are all section landing pages (`/en/news`, `/en/library`, `/en/funding`, `/en/consultations`,
`/en/activities`, `/en/shaping-europes-digital-future`) — indexes rather than documents, which is a
fair reason for them to carry no date and is stated as such rather than counted as a failure.

## Unpredicted observations — reported as observations, scored as nothing

1. **The two publisher-stated signals are one signal in two places.** Where both exist (17 pages),
   `S` and `V` agree **to the day, 17 of 17**. No disagreement anywhere in the corpus. The most
   economical reading is that both are emitted from the same field in the publishing system;
   this is inference, not established here.
2. **The machine-readable signal is missing exactly where dated documents live.** Counting item
   pages only: `S` covers 15 of 16 `/policies/` items, the single `/faqs/` and the single
   `/factpages/` page — and **0 of 8 `/library/` and 0 of 6 `/news/` items.**
3. **Coverage is inverted from what a tool would want.** The date a *human* can read: 34/40. The
   date a *machine* can read reliably: 17/40. The date a machine gets for free: 40/40, and it is
   the useless one.
4. **Six pages state no date at all** other than the delivery header. All six are landing pages.
5. **Post-hoc split, disclosed as post-hoc** (one path segment after `/en/` = landing page, two or
   more = item page): landing pages 8 — `S` on 0, `V` on 2; item pages 32 — `S` on 17, `V` on 32.

## What the Skeptic recomputed, and what it did to the claim

*Convened this session against the state at commit `0f0a1d8`. Verdict: **SURVIVES WITH CONDITIONS**,
one blocking objection. Three of its attacks it reported as failed attacks, in its own words.*

- **Blocking, and acted on.** The concept's practical payoff for a change-monitor was written as
  "will be told the page changed on every poll". Not shown: a conditional request with the collected
  validators returned `304 Not Modified` on every probe. The sentence was withdrawn and replaced
  with what is measured, before the verdict arrived (commit `3ccfbcc`, from the conductor's own
  probe); the Skeptic's independent objection is what fixes it in the record. **The cheapest test it
  names — re-send the same validators after 24–48 h and see whether `H` moves while `S` and `V` do
  not — is owed by proof session 2.**
- **Failed attack (its own label): "the header might be real edit time."** It checked the `ETag`
  against the header independently and found the embedded Unix timestamp equal to `Last-Modified`.
  Re-run here across the whole corpus: **equal on 40 of 40**, and `Cache-Control` is
  `public, max-age=300, s-maxage=300` on 40 of 40.
- **Failed attack: "the missing sections are a collection artifact."** It fetched the live sitemap
  itself: one flat `<urlset>`, 805 `<loc>` entries, byte-identical to `?page=2`, **zero matches for
  `/news/` or `/library/`**, and `robots.txt` declaring no sitemap. The absence is a property of the
  site.
- **Failed attack: "the inversion is an artifact of counting landing pages."** Its recomputation:
  drop the 8 landing pages and `S` = 17/32 while `V` = 32/32 — the gap **widens** to 47 points. Drop
  the 16 `/news/` + `/library/` items instead and `S` = 17/24, `V` = 20/24 — the gap narrows to 12.5
  points but does not reverse. **The headline "23 of 40" is corpus-composition-sensitive between
  12.5 and 47 points**, and that range belongs next to it.
- **Non-blocking, accepted.** One sentence in `CONCEPT.md` addressed "anyone writing 'as of' about a
  Commission guidance page" as a standing prescription rather than about the 40 pages measured at
  one timestamp. Rescoped.

## What the Verifier found — PASS WITH FINDINGS, three of them blocking

*Convened this session, independently of the builder, against commit `0f0a1d8`. It recomputed every
figure from `signals.json` with its own code rather than re-running `analyse.py`, and checked each
external citation by fetching it. Its full verdict is summarised in the session's journal entry.*

**Blocking, all three fixed at the root rather than in prose:**

1. **A denominator was wrong in this instrument's own code (D7).** `sitemap_coverage_by_section`
   counted a section's *landing* page inside that section's total, inflating three denominators by
   one each. The published figures were "15 of 17 `/policies/`, 0 of 9 `/library/`, 0 of 7 `/news/`";
   the correct item-page figures are **15 of 16, 0 of 8, 0 of 6**. `analyse.py` is fixed, the run
   re-analysed from the untouched `signals.json`, and every affected number restated here, on the
   workboard, and in `memory/claims.md`. **No verdict moves** — the sections still contain zero
   sitemap entries — but the numbers were wrong and were printed.
2. **`CONCEPT.md` stated the central asymmetry backwards.** "…unavailable on 6 of 40 and 23 of 40
   pages respectively" pairs, in the order the sentence introduces them, `S`=6 and `V`=23 — the
   inverse of the data. Rewritten without "respectively" and with each figure attached to its signal.
3. **The concept cited a file that did not exist at the audited commit.** `PRIOR-ART.md` was written
   after the reviewers were dispatched and committed at `4662309`. Conceded in full; the
   Interlocutor charged the same thing independently, and the answer is in the journal.

**Non-blocking, accepted and applied:** the median `H` age is 24.4 minutes, not 25 · D1's
"byte-identical" overstated a log that recorded only length and URL count · the `V3` fallback matched
a **future** date on `/en/events` (02 December 2026 — an upcoming-event date, not a currency signal),
so the 34/40 count carries at least one false positive; **P4 is killed either way** (33/40 is still
above half), and this is now D6 · the prose date for one P3-vs-`V` hit disagreed with the measured
one · one of those five hits is a landing page, now named as such.

**What the Verifier reproduced exactly:** all four prediction values and their denominators; the
5.96-day median; the 1/17 and 5/34 counts; `S`↔`V` agreement 17/17; `V` on 34/40 and on all 32 item
pages; the `ETag`-equals-`Last-Modified` identity on 40/40; that `analyse.py`'s thresholds and
comparison directions match the pre-registration verbatim, with no threshold moved and no killed
verdict softened in prose. On citations: the load-bearing arXiv paper's two figures were confirmed
against its own text; two publisher pages returned 403 to every route and are recorded as
corroborated by index rather than fetched.

## Defects of this instrument, named by this run

- **D1 — wasted requests.** `collect_signals.py` followed `sitemap.xml?page=N` up to 40 pages on the
  assumption that the site paginates. Every request returned the **same byte-length and the same URL
  count** (171 552 bytes, 805 URLs); the bodies themselves were not hashed, so byte-for-byte identity
  is not evidenced by the committed log — the Skeptic's independent fetch did report page 1 and
  `?page=2` byte-identical. 39 of the 40 sitemap requests were pointless. The URL index is unaffected.
- **D2 — the scoring set excluded the phenomenon.** See P3 above.
- **D3 — one authority, one moment.** 40 URLs from a single site at a single timestamp. Nothing here
  supports a statement about official pages in general, and none is made.
- **D4 — `V` is extracted by a fixed pattern set** (`PREREGISTRATION.md` M-3). It found a label on
  34 pages; it cannot prove it found every label a human would see. Session 93's D6 is the precedent
  for exactly this failure, so the figure is stated as *found by these patterns*, not as *present*.
- **D6 — the `V3` fallback is not scoped to currency.** `<time datetime>` matched an upcoming-event
  date on `/en/events`, a date in the future. At least one of the 34 `V` hits is a false positive.
  D4 named only false negatives; this is the opposite error, found by the Verifier.
- **D7 — a landing page was counted in its own section's denominator.** Fixed in `analyse.py` and
  restated everywhere the wrong figures appeared. See the Verifier section above.
- **D5 — `S` is a claim too.** The sitemap's `<lastmod>` is the publishing system's assertion. Its
  agreement with `V` shows internal consistency, not correctness.

## What this run supports, stated at the strength it can carry

On this surface, on this date: **a citer or a tool asking "when did this page last change?" gets an
answer that is always "just now" if it asks the transport layer, gets no answer at all on 23 of 40
pages if it asks the sitemap, and gets a plausible answer on 34 of 40 if a human reads the page.**
Whether those printed dates are true is not established here and would need capture history.

## Reproduce

```
python3 collect_corpus.py      # rebuilds corpus.json from the live seed page
python3 collect_signals.py     # fetches the 40 pages + the sitemap -> signals.json
python3 analyse.py             # scores P1-P4 -> results.json
```
The surface moves; a re-run will not reproduce these numbers, and the committed
`signals.json` is the record of this moment.
