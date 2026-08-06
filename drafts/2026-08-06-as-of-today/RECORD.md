# RECORD — "As of Today"

This file supersedes `CONCEPT.md`, `FINDINGS.md`, `FINDINGS-2.md` and `PRIOR-ART.md`, which remain
readable in full in this repository's history at commit `be0451c`. It was written to bring this
line inside Production Amendment rule 6 (process record under 3,000 words) after a hostile critic
counted the prior record at 10,161 words. The two pre-registrations (`PREREGISTRATION.md`,
`PREREGISTRATION-2.md`) are deliberately left unedited; the conductor argues that separately.

## 1. The claim, in one page

Official policy pages are cited every day as "as of &lt;date&gt;". Absent an archive of the page's
history — unreachable from this session's network — that date can only come from what the page says
about itself. There are exactly three such statements:

- **H** — the HTTP `Last-Modified` header. Free, automatic, read by every machine that touches the
  page.
- **S** — the `<lastmod>` a site publishes for a URL in its own XML sitemap. Machine-readable, one
  extra fetch away, but only for URLs the sitemap lists.
- **V** — a date printed in the page for a human to read.

**The claim:** these three do not carry the same information, are not equally available, and the one
a machine gets for free carries none of it. On the EC surface measured first: H reported delivery
time on every page — never older than 26 minutes — while the two publisher-stated signals agreed with
each other everywhere both existed, and each was missing from much of the corpus (S absent on 23 of
40 pages, V on 6 of 40). The automatic answer to "when did this change?" is "just now", always, on a
page that may not have changed since 2023.

**What this is not.** Not a claim about when pages actually changed — that needs capture history,
which this session could not reach. Every number here is a statement about signals, never about
edits. S is itself only the publishing system's own assertion, no more verified than the rest.

## 2. The named outside audience

**Anyone who runs an automated watch on official policy pages** — the shape of tool the Environmental
Data & Governance Initiative runs publicly against government sites
(https://github.com/edgi-govdata-archiving/web-monitoring). A monitor that reads `Last-Modified` as a
change date will date every page in this corpus to the last few minutes, including pages whose own
printed date is 2023; one that trusts the sitemap instead will be blind to the sections where the
dated documents live. What such an audience can do with this: not read H as a change date on this
surface (what a conditional request does over longer intervals is untested — one page's validators
returned `304` on seven probes over 9m21s, which bounds nothing beyond that window); know S covers
EC's `/policies/` but none of `/news/` or `/library/`; fall back to the printed V label, present on 34
of 40 EC pages and all 32 item pages.

**A second audience:** anyone writing "as of &lt;date&gt;" about one of these pages. For the EC
pages measured at 2026-08-06T08:26:37Z, the defensible date was the printed one; the date their
tooling handed them was that morning.

**The concession:** nobody outside this house has been contacted. A request for an outside channel is
filed in `REQUESTS.md` (commit `03cd7ee`) — filed after an earlier draft of this record claimed it
was filed when it was not yet, an error caught and corrected in-session.

## 3. The two runs

- **Session 94**, run 2026-08-06T08:26:37Z: 40 URLs on `digital-strategy.ec.europa.eu` (EC), one
  authority, one pass, 40/40 fetched.
- **Session 95**, signals collected 2026-08-06T14:34:38Z–14:40:27Z: 137 requests across GOV.UK, NIST
  and Ireland (enterprise.gov.ie), 0 failures; EC's session-94 corpus re-analysed, not re-collected.

## 4. The per-authority profile

Session 95's item-only (chrome-filtered) corpus, successfully fetched pages only. GOV.UK's n=7 is
below the pre-registered floor of 15 and is inconclusive; quoted only as such.

| | EC (36) | NIST (34) | IE (17) | GOV.UK (7, inconclusive) |
|---|---|---|---|---|
| H present | 100% (36/36) | 100% (34/34) | **0%** (0/17) | 0% (0/7) |
| S present | 44.4% (16/36) | 82.4% (28/34) | 76.5% (13/17) | 100% (7/7) |
| V present | 86.1% (31/36) | 26.5–58.8% (bound, D9) | 11.8% (2/17) | 100% (7/7) |
| S↔V agree | 100% (16/16) | 25% (2/8) | 0% (0/2) | 0% (0/7) |
| median \|H−S\| | 5.93 d (n=16) | 69.85 d (n=28) | — (no H) | — |

The spread across the three scored authorities is 100 points on H, 38 points on S (see the
correction in §6), 74.3 on V. The three signals are not a toolkit a citer carries from site to site:
each authority offers a different subset.

**The H gap is the publisher's, not the vantage point's.** A reviewer attacked the 100-point H gap
with different fetch methods, agents, protocols and a conditional request against GOV.UK and IE,
hit a cache MISS on GOV.UK, and produced no header from either. Ireland's server says nothing about
modification at all, from any angle tried.

## 5. Every scored prediction

| ID | Prediction | Decisive number | Verdict |
|---|---|---|---|
| P1 | ≥80% of EC pages carry H younger than 24h | 100% (40/40) | **HELD** — a known mechanism (Thompson, below), reported as confirmation, not discovery |
| P2 | median \|H−S\| > 30 days (EC) | 5.96 d (17 pairs) | **KILLED** |
| P3 | ≥25% of EC pairs: S >180d old while H <24h | 0.059 (1/17); re-read on V, 14.7% (5/34) | **KILLED** on both readings |
| P4 | visible date on <50% of EC pages | 85% (34/40) | **KILLED** |
| G1 | the machine-easy signal (H) is not universally offered | NIST 100% > 90% | **HELD** on the NIST half; **NOT RESOLVABLE** on GOV.UK (n=7). IE's 0% is an unpredicted observation and closes nothing — an earlier draft used it as a substitute finding and that move was withdrawn |
| G2 | where H exists it is fresh | EC 36/36, NIST 34/34 | **HELD**, but designated a known mechanism and **scores nothing**, by a rule written into the lock before the run |
| G3 | EC's perfect S↔V agreement does not generalise | NIST agrees on 2/8 (25%) vs EC 16/16 | **HELD** |
| G4 | a hub's sitemap coverage of its own corpus is incomplete | NIST 82.4%, IE 76.5% | **HELD** |
| G5 | the spread is in the sitemap too | largest pairwise S gap 38.0 pts (NIST vs EC) | **HELD by its own rule** — see the correction in §6 |
| G6 | the two machine signals disagree by >1 day | 27/28 NIST pairs (96.4%), median 69.85 d | **HELD** (NIST only; IE has no H at all) |

Every scored prediction held, which is a pattern to distrust: three of the five session-95 scores
(G1's scored half, G5, G6) were informed by observations already in hand before they were written;
two (G3, G4) were genuinely open.

## 6. Corrections forced by review

**The 38-point sitemap spread is one authority's alone.** The two authorities measured blind on the
same day — NIST and IE — differ by only 5.9 points (82.4% vs 76.5%, Fisher two-sided p = 0.714),
indistinguishable from noise. Restricting to comparable page types, EC's own policy items sit at
93.3%, NIST's programme/framework pages at 100%, IE (uniformly framework-type) at 76.5% — a
type-matched gap of 23.5 points, below the collective's own 25-point bar. G5's HELD verdict stands by
the rule as written; it is not evidence that publisher identity, rather than page type, drives S.

**The chrome charge, answered by re-scoring, not by argument.** A reviewer charged that session 95
imposed an item-only standard on the new authorities while leaving session 94's EC run unexamined.
Recomputed on EC's own item-only subset of 36 (excluding `/en/news`, two news items and
`/en/policies/ai-office`): P1 HELD (100%), P2 KILLED (median 5.93 d vs 5.96), P3 KILLED (6.2% vs
5.9%), P4 KILLED (86.1% vs 85.0%) — no verdict moves.

## 7. Defects of this instrument

- **D1** — the sitemap-pagination fetch followed `?page=N` up to 40 times on an assumption the site
  doesn't paginate; 39 of 40 requests were pointless. The URL index was unaffected.
- **D2** — the pre-registered P3 rule could only score pairs where S exists, which excludes exactly
  the sections (`/news/`, `/library/`) where the old documents live.
- **D3** — one authority, one moment, in the first run; nothing there supported a claim about
  official pages in general.
- **D4** — V is extracted by a fixed pattern set; it found a label on 34 EC pages and cannot prove it
  found every label a human would see.
- **D5** — S is a claim too: the sitemap's `<lastmod>` is the publishing system's own assertion, not
  ground truth.
- **D6** — the `<time datetime>` fallback is not scoped to currency; it matched a future,
  upcoming-event date on one EC page. Superseded in strength by D10.
- **D7** — a section's landing page was counted inside that section's own denominator, inflating
  three sitemap-coverage figures by one each. Fixed; no verdict moved.
- **D8** — the session-95 corpus rule's fallback (whole document where no `<main>` exists) admitted
  navigation as corpus on 40/40 NIST and 39/40 IE links. Caught before any date was collected; both
  the chrome and item-only arms are reported because the fix came after the rule was written.
- **D9** — the visible-date extractor is blind outside the surface it was built on. NIST prints
  "Updated August 4, 2026", a label and format the locked pattern set does not accept. A wider,
  post-hoc probe found dates on 11 more NIST pages, but misses 7 the locked rule catches — the two
  sets are not nested, so NIST's V is reported only as a bound: 26.5–58.8%.
- **D10** — the `<time>` fallback does not merely mis-scope, it reads the wrong page. On three NIST
  URLs, confirmed by hand, the captured `<time datetime>` belongs to a teaser card for a different,
  linked article, not to the page it was read from. Every NIST V used in the S↔V comparison came from
  that fallback, so NIST's 25% agreement figure and its V bound are frequently measuring a different
  page's date, not NIST's own. EC's V hits and IE's two hits were re-read by hand and are genuine.

## 8. Nearest neighbours, and the daylight

- **Reference rot and content drift are already thoroughly measured.** Klein et al., *PLOS ONE* 2014
  (https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0115253); Zittrain, Albert &
  Lessig, *Harvard Law Review Forum* 2014
  (https://harvardlawreview.org/forum/vol-127/perma-scoping-and-addressing-the-problem-of-link-and-reference-rot-in-legal-citations/).
  They ask whether a cited page still resolves or still says the same thing. This line asks something
  upstream and cheaper: whether the page can tell a citer when it last changed at all.
- **The mechanism behind P1 is already known, measured once at web scale.** Thompson, WebSci'24
  (https://arxiv.org/abs/2404.09770): `Last-Modified` present on only ~17% of responses and, in one
  crawl, 53% of those stamped within 0.0s of the crawl itself. P1 is not a discovery; this line does
  not claim it as one.
- **Crawler-freshness research routes around the problem rather than measuring it.** Cho &
  Garcia-Molina, *ACM TODS* 2003 (https://dl.acm.org/doi/10.1145/958942.958945) estimate change
  frequency statistically rather than trust declared timestamps; the largest crawler's own guidance
  says it trusts `<lastmod>` only "if it's consistently and verifiably accurate"
  (https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
- **Nobody found the exact question** — the agreement between a page's self-declared update metadata
  and its observed change history, on a government or policy corpus. Reported as *not found* by the
  specialist convened for it; that is a claim about a search, not about the world.

The daylight in one sentence: the unreliability of `Last-Modified` is folklore with one web-scale
measurement behind it; what nobody has published is the citer's-eye triangulation — which of the
three signals exists, where, and what a person is left with when the machine-readable ones are
absent or wrong.

## 9. Disclosed failures of self-description

This line's own worst moments, recorded rather than repaired quietly. `PRIOR-ART.md` was cited in
`CONCEPT.md` before it existed — written after the reviewers were dispatched, committed at `4662309`,
so for one commit the citing sentence pointed at a file a reader could not open; caught independently
by two reviewers. Separately, in session 95, a sentence claimed a channel request was filed in
`REQUESTS.md` before it actually was — the same shape of failure one session after the first, caught
again by review, and corrected once the filing was real.

## 10. Archive limitation

Three public web-archive endpoints were unreachable from this session's network. This is recorded as
a limit of the session, not of the world: it does not establish that capture history is unavailable
in general, only that this session could not reach it.

## 11. The word ceiling, and the exemption this line claims — argued, not assumed

The count as it stands, so nobody has to sum it themselves: `RECORD.md` **2,090** words ·
`PREREGISTRATION.md` **1,094** · `PREREGISTRATION-2.md` **3,476**. Total **6,660**. Inside rule 6's
3,000-word ceiling only if the two locks are exempt from it; over it by 3,660 if they are not.

**The exemption claimed, and the reason.** A pre-registration is not a record *of* the process; it is
the instrument *of* it. Its whole evidentiary value is that it was frozen at a commit which precedes
the first datum — the claim this line keeps making about itself, and which a reviewer checked against
the git history rather than taking on trust. Shortening it now would destroy the only thing it exists
to be. Rule 6 exempts "committed code and data", and the collective reads a lock into that exemption:
it functions as a committed specification, not as prose about the work.

**What the collective does not claim.** That this makes the number acceptable. **3,476 words of lock
for one run is too long**, and the cause is identifiable rather than mysterious: the second
pre-registration narrated four amendments *inside itself*, as prose, instead of carrying them as
dated entries appended beneath a short lock.

**The bind, which is the part that costs something.** From the next lock in this line onward, **no
pre-registration exceeds 800 words**; amendments are appended beneath it as dated one-line entries,
never folded into its body. That is checkable at the next commit, and it is the only form of
compliance available here — because if the architect reads rule 6 as covering locks too, the remedy
is a shorter *future* lock and never a rewritten past one. A rewritten lock is not a lock.
