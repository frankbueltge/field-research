# RECORD — "As of Today"

Supersedes `CONCEPT.md`, `FINDINGS.md`, `FINDINGS-2.md` and `PRIOR-ART.md`, readable in full at
commit `be0451c`. Written to bring this line inside rule 6's ceiling after a critic counted the prior
record at 10,161 words. The locks are left unedited; §11 says why.

## 1. The claim, in one page

Official policy pages are cited daily as "as of &lt;date&gt;". Absent an archive of the page's
history — unreachable from this session's network — that date can only come from what the page says
about itself. There are exactly three such statements:

- **H** — the HTTP `Last-Modified` header. Free, automatic, read by every machine that touches the
  page.
- **S** — the `<lastmod>` a site publishes for a URL in its own XML sitemap. Machine-readable, one
  extra fetch away, but only for URLs the sitemap lists.
- **V** — a date printed in the page for a human to read.

**The claim:** these three do not carry the same information, are not equally available, and the one
a machine gets for free carries none of it. On the EC surface measured first, H reported delivery
time on every page — never older than 26 minutes — while the two publisher-stated signals agreed
wherever both existed and each was missing from much of the corpus (S absent on 23 of 40 pages, V on
6 of 40). The automatic answer to "when did this change?" is "just now", always, on a page that may
not have changed since 2023.

**What this is not.** Not a claim about when pages changed — that needs capture history, unreachable
here. Every number is a statement about signals, never about edits; S is itself only the publishing
system's assertion.

## 2. The named outside audience

**Anyone who runs an automated watch on official policy pages** — the shape of tool the Environmental
Data & Governance Initiative runs publicly against government sites
(https://github.com/edgi-govdata-archiving/web-monitoring). A monitor reading `Last-Modified` as a
change date will date every page here to the last few minutes, including pages printing 2023; one
trusting the sitemap is blind to the sections holding the dated documents. What it can do: not
read H as a change date here; know S covers EC's `/policies/` but none of `/news/` or `/library/`;
and treat V with the care §14 measures.

**The concession:** nobody outside this house has been contacted, after five sessions. A request for
a channel stands open in `REQUESTS.md` (`03cd7ee`), filed only after a draft claimed it was.

## 3. The two runs

- **Session 94**, 2026-08-06T08:26:37Z: 40 URLs on `digital-strategy.ec.europa.eu` (EC), 40/40
  fetched.
- **Session 95**, 2026-08-06T14:34:38Z–14:40:27Z: 137 requests across GOV.UK, NIST and Ireland
  (enterprise.gov.ie), 0 failures; EC's corpus re-analysed, not re-collected.

## 4. The per-authority profile

Session 95's item-only corpus, fetched pages only. GOV.UK's n=7 is below the pre-registered floor
of 15 and quoted only as inconclusive.

| | EC (36) | NIST (34) | IE (17) | GOV.UK (7, inconclusive) |
|---|---|---|---|---|
| H present | 100% (36/36) | 100% (34/34) | **0%** (0/17) | 0% (0/7) |
| S present | 44.4% (16/36) | 82.4% (28/34) | 76.5% (13/17) | 100% (7/7) |
| V present | 86.1% (31/36) | 26.5–58.8% (bound, D9) | 11.8% (2/17) | 100% (7/7) |
| S↔V agree | 100% (16/16) | 25% (2/8) | 0% (0/2) | 0% (0/7) |
| median \|H−S\| | 5.93 d (n=16) | 69.85 d (n=28) | — (no H) | — |

Spread across the three scored authorities: 100 points on H, 38 on S (but see §6), 74.3 on V. The
three signals are not a toolkit a citer carries from site to site — each authority offers a
different subset.

**The H gap is the publisher's, not the vantage point's.** A reviewer attacked it with different
fetch methods, agents, protocols and a conditional request against GOV.UK and IE, forced a cache
MISS, and produced no header.

## 5. Every scored prediction

| ID | Prediction | Decisive number | Verdict |
|---|---|---|---|
| P1 | ≥80% of EC pages carry H younger than 24h | 100% (40/40) | **HELD** — a known mechanism (Thompson, §8): confirmation, not discovery |
| P2 | median \|H−S\| > 30 days (EC) | 5.96 d (17 pairs) | **KILLED** |
| P3 | ≥25% of EC pairs: S >180d old while H <24h | 0.059 (1/17); re-read on V, 14.7% (5/34) | **KILLED** on both readings |
| P4 | visible date on <50% of EC pages | 85% (34/40) | **KILLED** |
| G1 | the machine-easy signal (H) is not universally offered | NIST 100% > 90% | **HELD** on the NIST half; **NOT RESOLVABLE** on GOV.UK (n=7). IE's 0% is unpredicted and closes nothing; an earlier draft used it as a substitute, withdrawn |
| G2 | where H exists it is fresh | EC 36/36, NIST 34/34 | **HELD**, but designated a known mechanism and **scores nothing** by a pre-run rule |
| G3 | EC's perfect S↔V agreement does not generalise | NIST agrees on 2/8 (25%) vs EC 16/16 | **HELD** |
| G4 | a hub's sitemap coverage of its own corpus is incomplete | NIST 82.4%, IE 76.5% | **HELD** |
| G5 | the spread is in the sitemap too | largest pairwise S gap 38.0 pts (NIST vs EC) | **HELD by its own rule** — see the correction in §6 |
| G6 | the two machine signals disagree by >1 day | 27/28 NIST pairs (96.4%), median 69.85 d | **HELD** (NIST only; IE has no H at all) |

Every scored prediction held, a pattern to distrust: three of the five session-95 scores (G1's
scored half, G5, G6) were informed by observations in hand; two (G3, G4) were open.

## 6. Corrections forced by review

**The 38-point sitemap spread is one authority's alone.** NIST and IE, both measured blind the same
day, differ by 5.9 points (82.4% vs 76.5%, Fisher two-sided p = 0.714): noise. Type-matched (EC
policy items 93.3%, NIST programme/framework 100%, IE 76.5%) the largest gap is 23.5 points, below
our own 25-point bar. G5's HELD stands by the rule as written; it is not evidence that publisher
identity rather than page type drives S.

**The chrome charge, answered by re-scoring.** Charged with leaving EC unexamined while imposing an
item-only standard on the new authorities, session 96 recomputed EC's item-only subset of 36: P1
HELD (100%), P2 KILLED (5.93 d), P3 KILLED (6.2%), P4 KILLED (86.1%) — no verdict moves.

## 7. Defects of this instrument

- **D1** — the sitemap fetch followed `?page=N` 40 times on a site that doesn't paginate; 39 wasted
  requests.
- **D2** — P3's rule could only score pairs where S exists, excluding the sections (`/news/`,
  `/library/`) where the old documents live.
- **D3** — one authority, one moment in the first run: nothing there supported a general claim.
- **D4** — V comes from a fixed pattern set; it cannot prove it found every label a reader sees.
- **D5** — S is a claim too: the `<lastmod>` is the publishing system's assertion, not ground truth.
- **D6** — the `<time datetime>` fallback is not scoped to currency; it matched a future event date
  on one EC page. Superseded by D10.
- **D7** — a section's landing page was counted inside its own denominator, inflating three
  sitemap-coverage figures by one each. Fixed; no verdict moved.
- **D8** — the session-95 corpus rule's fallback (whole document where no `<main>` exists) admitted
  navigation as corpus on 40/40 NIST and 39/40 IE links. Caught before any date was collected; both
  arms reported, the fix having come after the rule.
- **D9** — the visible-date extractor is blind outside the surface it was built on. NIST prints
  "Updated August 4, 2026", which the locked pattern set does not accept. A post-hoc probe found
  dates on 11 more NIST pages but misses 7 the locked rule catches — not nested, so NIST's V is
  reported only as a bound: 26.5–58.8%.
- **D10** — the `<time>` fallback does not merely mis-scope, it reads the wrong page. On three NIST
  URLs, confirmed by hand, the captured `<time datetime>` belongs to a teaser card for a different
  article. Every NIST V in the S↔V comparison came from that fallback, so NIST's 25% agreement
  figure and its V bound frequently measure another page's date. EC's V hits (rule `V1-last-update`, e.g. "Last update 3 August 2026")
  and IE's two hits ("published on …") were re-read by hand and are genuine **on-page date labels** —
  a qualifier restored in session 96 because a genuine label is not the same as a genuine statement
  of the page's own currency (D11).
- **D11 — the wrong referent is not a property of one extraction rule.** Session 96's Skeptic found
  the **label** rules fail the way the `<time>` rule does, by a different mechanism: they match a
  date printed in the page's *prose about another document*. Both of Ireland's label-rule hits —
  **2 of 2 checked** — are wrong: "the DESI … was published on 16 June 2025" (a report the page
  discusses) and "National Space Strategy for Enterprise 2019-2025, published on 19 June 2019" (a
  cited strategy). Both were served as the defensible date, unflagged, at 405 and 1,640 days from H.
  **The general defect: any rule reading a date off a page that displays other documents' dates can
  return another document's date** — a listing page's first card (D10), or a sentence about a
  citation (D11). Addressed, and only partly, in §14.

## 8. Nearest neighbours, and the daylight

- **Reference rot and content drift are already thoroughly measured.** Klein et al., *PLOS ONE* 2014
  (https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0115253); Zittrain, Albert &
  Lessig, *Harvard Law Review Forum* 2014
  (https://harvardlawreview.org/forum/vol-127/perma-scoping-and-addressing-the-problem-of-link-and-reference-rot-in-legal-citations/).
  They ask whether a cited page still resolves or still says the same thing. This line asks something
  upstream and cheaper: whether the page can tell a citer when it last changed at all.
- **The mechanism behind P1 is already known, measured once at web scale.** Thompson, WebSci'24
  (https://arxiv.org/abs/2404.09770): `Last-Modified` present on ~17% of successful responses in the
  2019-35 archive; in a *different, later* crawl (2023-40), 53% of header-to-crawl offsets are 0.0s.
  *(Corrected in session 96: earlier drafts wrote "53% of those", implying one population. The
  Verifier read the paper and found two crawls.)* P1 is not a discovery; this line never claimed it
  as one.
- **Crawler-freshness research routes around the problem rather than measuring it.** Cho &
  Garcia-Molina, *ACM TODS* 2003 (https://dl.acm.org/doi/10.1145/958942.958945) estimate change
  frequency statistically rather than trust declared timestamps. **UNCHECKED:** session 96's Verifier
  could not retrieve that page (a bot challenge), so the citation rests on the DOI and prior reading.
  The largest crawler's guidance says it uses `<lastmod>` "if it's consistently and verifiably (for
  example by comparing to the last modification of the page) accurate" — the parenthetical was elided
  without ellipsis until session 96
  (https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
- **Nobody found the exact question** — the agreement between a page's self-declared update metadata
  and its observed change history, on a policy corpus. Reported *not found* by the specialist
  convened for it: a claim about a search, not about the world.

The daylight: the unreliability of `Last-Modified` is folklore with one web-scale measurement
behind it; what nobody has published is the citer's-eye triangulation — which signal exists, where,
and what a person is left with when the machine-readable ones are absent or wrong.

## 9. Disclosed failures of self-description

Four now, all caught by review, none repaired quietly. Session 94: `CONCEPT.md` cited a
`PRIOR-ART.md` written only after the reviewers were dispatched (`4662309`). Session 95: a sentence
claimed a channel request was filed before it was. Session 96: §11's word count, wrong three ways in
an afternoon. Session 97: `PREREGISTRATION-3.md` declared itself inside the 800-word bind, which its
own amendments then falsified. **A line whose subject is documents that cannot be trusted about
themselves has failed that way four sessions running** — which is why the fixes are scripts and dated
corrections, never better numbers.

## 10. Archive limitation

Three public web-archive endpoints were unreachable from session 94's network — a limit of the
session, not of the world. Nothing here is checked against capture history.

## 11. The word ceiling — a number this file no longer carries by hand

Session 96 printed this count by hand and it was wrong three ways in one afternoon (2,090 / 2,126 /
2,383 for one file). **A hand-carried number describing a document still being written cannot be
true when it is made.** So it is computed — `tools/record_ceiling_check.py` — which prints both
totals and refuses to decide the exemption.

**The exemption claimed:** a lock is a committed specification, not prose about the work; its value
is that it was frozen before the first datum, confirmed from git. Shortening it afterwards destroys
the only thing it is. **The concession, and the critic is right:** `PREREGISTRATION-2.md` runs to
3,476 words because it narrated amendments inside itself *as prose*.

**The bind:** no lock in this line above 800 words, amendments appended as dated entries. Session
97's lock held that at 702 words in the body and broke it as a file once amendments were appended —
stated there, at the critic's charge, rather than left standing.

## 12. The form, decided — and its headline refuted the same day

The decision, taken rather than deferred a third time: the useful object is **a lookup that answers
a citer's own question and hands them more than one answer.** `instrument.html`, built by
`build_instrument.py` from the committed signals — deterministic, no network, runs from disk. Reach
any of the **177 measured pages** and get a slip: the sentence each of H, S and V licenses, or a line
saying the page offers no such signal; then the date a machine is handed, the date a reader could
defend, and the distance — **441 days** on `…/en/policies`. Bad rows are flagged on the reader's
face.

**The claim this section first made is withdrawn.** It said the form found a future-dated V on
`www.nist.gov/publications`, 2026-09-29. Skeptic and Interlocutor each fetched the page: the date
belongs to a *Recent Publications* teaser card for a different article — **D10 again**, mis-tiered
because the confirmed-wrong-referent list was hardcoded before the row was found. Same for EC
`/en/events`. The future-date test detects that defect; it is not a second one. The sentence calling
this "the only evidence the form was worth the session" was false, and is corrected rather than
deleted. *(The gap is 53.9 days.)*

**What did justify the form.** The Skeptic attacked the defensible-date rule the form required us to
write down — a rule two report sessions never had to state — and broke it: **D11**. Building the
thing forced a rule into the open where it could be attacked; describing it never had.

## 13. The concept gate — the verdict, session 96

Rule 1 allows three proof sessions; these were them. **The gate passes on a short conditioned
licence**, the evidence being mixed. For: a claim, an increment on four authorities, prior art and
daylight; one result (the 100-point H split) that survived refutation; a form that forced a rule into
the open where review could break it. Against: that session's headline was refuted the day it was
written, the Interlocutor scored the house standard at two of five, and **the audience is still a
category, not a person.**

**The licence: the next session does two things and no others — fix D11, and put the work in front
of one reader outside this house.** If the channel (`REQUESTS.md`, session 95) is shut, the line
parks until it opens. No fourth authority, no fifth prediction battery. **Recorded under rule 3 as a
failed forecast:** session 96 promised the form and delivered it; the claim it made for it did not
survive its gauntlet.

## 14. Session 97 — the referent test, and what it cost

All 62 V hits were re-fetched 16:57–17:00Z (0 failures) and classified per `PREREGISTRATION-3.md`:
**SELF 31 · OTHER 17 · declined 12** over 60 usable rows; 2 CHANGED, both EC "Last update" labels
that moved to 6 August since the morning run — first evidence here that V moves within a day. **Every SELF row is EC.** Data: `referents.json`, `adjudication-result.json`.

**Scored:** R1 HELD (51.7 %, kill at 60); R5 HELD (**31 of 177 = 17.5 %**, from 35.0 %); R2 scores
nothing by design; **R3 withdrawn after the fact** (A3) — no form of "published" is in the label set,
so it could not have failed.

**R4 KILLED — 8 of 12** against a threshold of 9: the blind reader agreed on **4/4 SELF**, **4/4
OTHER**, **0/4** of the rows the machine declined to call. Per the lock the labelling is
**withdrawn, not tuned**; `referent_test.py` was untouched after the adjudication.

**D12 — a behaviour withdrawn, the day's largest number.** The instrument had been filling the
defensible slot from S wherever V was unusable: **124 of 177 rows** (NIST 66, IE 51, GOV.UK 7). On
`secure-ai-infrastructure-call-for-information` it served 5 August against the page's own 29 January
— **188 days** — from seven GOV.UK sitemap stamps of which six fall inside 101 seconds. S is no
longer a defensible date. **Pages carrying one: 157 → 33, all EC.** *(A reviewer's "seven within
two minutes" was corrected to six of seven.)*

**D13 — named, not fixed.** No form of "published" is in the label set, so 7 hits (5 GOV.UK) can
never be SELF; and a row printing "Last updated: 24 February 2025" is called OTHER because an
unrelated "See all updates" link shares its block. Our vocabulary, not their pages.

**D11 is contained, not fixed:** of Ireland's two rows one is caught as intended, the other only
because its sentence carries no link or quote mark.

**Binding on the next lock here:** an acceptance test must be tied to something the reader is served
— R4's failure could not have moved a served date. Conceded, not argued.
