# FINDINGS — "As of Today", proof session 2: the citer's date is a property of the publisher

**Run 2026-08-06, signals collected 14:36:39Z–14:44Z. Locked in advance by `PREREGISTRATION-2.md`
with amendments 1–4, every one of them written and committed before a single date signal for the
new authorities existed.** Session 94's EC measurement (08:26:37Z) is re-analysed here, never
re-collected.

Everything below is a statement about **what a surface tells a citer**. Nothing here establishes
when a page really changed; that needs capture history, and the three public archive endpoints this
practice can reach were all unreachable yesterday and were not retried today.

## 1. The question this session locked

Session 94 measured three currency signals — the HTTP `Last-Modified` header (**H**), the site's own
sitemap `<lastmod>` (**S**), a date printed for a human (**V**) — on one authority, and found an
orderly picture. One authority cannot tell a rule of official publishing from a habit of one
publisher's software. So: **is "as of <date>" a property of the web, or a property of the
publisher?**

## 2. What the corpus stage cost, before any date was collected

Two rule failures surfaced before measurement, and both are in the record with the commits that
prove the order (`516df4a` opening lock, `5c0a771` corpora).

**The GOV.UK seed did not exist.** `…/government/collections/ai-regulation` returns **404**. The
orientation probe that put it into the pre-registration read headers with `curl -I -L` and never
captured the status line, so this document's own "known beforehand" section had described GOV.UK's
**404 page** as if it were a live page. Amendment 1 corrects that, states a replacement rule, lists
the six candidates checked with their status codes, and takes
`https://www.gov.uk/government/organisations/ai-security-institute` (200).

**The corpus rule was collecting navigation.** The replacement GOV.UK seed yielded **7** URLs —
below our own floor of 15, so **GOV.UK is inconclusive under C2-RULE-4 and scores nothing**, in
either direction. Its hub does not link its documents; it links a **search query** (4 of its 14
in-`<main>` links are `/search` paths, excluded by a rule written before any of this was seen).
Amendment 2 then added one further authority by a procedure written before any candidate was
fetched — five hubs in alphabetical order by country, first one passing (200, XML sitemap, no
interstitial) taken, search stops there. Australia failed to connect, Canada 404, **Ireland
(`enterprise.gov.ie`) passed and was taken**.

Then the control in amendment 3 fired: on the corpora as first pre-registered, **40 of 40 NIST URLs
and 39 of 40 IE URLs were chrome** — links that also appear on the host's own home page. Scoring the
currency signals of a navigation bar and calling it "what this hub tells a citer about its
documents" would have been a false headline for reasons visible in the corpus. Amendment 4 moved the
chrome filter into selection: **Arm B** (chrome-filtered: NIST 34, IE 17, GOV.UK 7, EC 36 of its
locked 40) is the scored arm; **Arm A** (as first pre-registered) is measured and reported alongside.

## 3. The citer profile — what each authority offers a reader who wants a date

Arm B, successfully fetched pages only. **0 fetch failures across all 132 requests.**

| | **EC** *(locked, re-analysed)* | **NIST** | **IE** | *GOV.UK (n=7, inconclusive — scores nothing)* |
|---|---|---|---|---|
| **H** — `Last-Modified` | **100 %** (36/36) | **100 %** (34/34) | **0 %** (0/17) | *0 % (0/7)* |
| **S** — sitemap `<lastmod>` | **44.4 %** (16/36) | **82.4 %** (28/34) | **76.5 %** (13/17) | *100 % (7/7)* |
| **V** — a printed date | **86.1 %** (31/36) | **26.5 – 58.8 %** (see D9) | **11.8 %** (2/17) | *100 % (7/7)* |
| S and V agree to the day | **100 %** (16/16) | **25 %** (2/8) | 0 % (0/2) | *0 % (0/7)* |
| median \|H−S\| | **5.93 d** (n=16) | **69.85 d** (n=28) | — (no H) | *—* |

**The three signals are not a toolkit a citer carries from site to site.** Each authority offers a
different subset, and the differences are large: the spread across the three scored authorities is
**100 points on H**, 38 points on S, and 74.3 points on V. A monitoring rule tuned on the
Commission's pages reads Ireland's as unchanging forever, because Ireland's server never says
anything about modification at all.

## 4. The predictions, scored

**G1 — the machine-easy signal is not universally offered. HELD on the NIST half; NOT RESOLVABLE on
the GOV.UK half** (inconclusive at n=7). NIST 100 % > 90 %. *Weak by construction: the NIST half was
informed by a one-page probe disclosed in the lock. The GOV.UK-shaped claim is carried instead by
**IE at 0 %**, which was not probed and not predicted.*

**G2 — where H exists it is fresh. HELD on EC (36/36) and NIST (34/34), NOT APPLICABLE elsewhere.
DESIGNATED KNOWN MECHANISM; SCORES NOTHING**, by a rule written into the lock before the run
(arXiv:2404.09770 measured this at web scale). It is reported because it replicates, not because it
counts.

**G3 — the EC's perfect S↔V agreement does not generalise. HELD.** NIST agrees on **2 of 8**
(25 %); EC agreed on 16 of 16. *Genuinely open when written.*

**G4 — sitemap coverage of a hub's own outbound corpus is incomplete. HELD.** NIST 82.4 %, IE
76.5 %; neither at 100 %. GOV.UK half not resolvable. *Genuinely open when written.*

**G5 — the spread is in the sitemap too. HELD.** Largest pairwise S-coverage difference **38.0
points** (NIST 82.4 % vs EC 44.4 %) > 25. *Informed by the EC result.*

**G6 — the two machine signals disagree by more than a day. HELD.** Pooled over NIST and IE, **27 of
28** pairs exceed one day (96.4 %), median **69.85 days**. All 28 pairs come from NIST, because IE
has no H at all — so this is a NIST result reported under a pooled rule, and it is labelled
INFORMED BY EC in the lock.

**Every scoring prediction held. That is a pattern to distrust, and the honest breakdown is: two of
the five (G1's scored half, G5, G6) were informed by observations already in hand; two (G3, G4)
were open.** The continuation test was therefore checked on its second clause too.

**Continuation: CONTINUE.** Clause (a): at least one non-G2 prediction held — five did. Clause (b),
settled by measurement rather than prediction: the citer profiles differ by more than 25 points on
**all three** components (H 100.0, S 38.0, V 74.3). G2 alone could not have satisfied either clause,
which was the point of writing it that way.

## 5. Unpredicted observations — reported as observations, scored as nothing

**GOV.UK's sitemap date is a pipeline timestamp, not a change date.** All seven `<lastmod>` values
fall on **2026-08-05**, six of them inside 101 seconds (07:53:22–07:55:03), the seventh at 13:13:37
— while the dates printed on those same seven pages span **2025-02-24 to 2026-07-15**. This is the
mirror image of the header's failure mode: a machine-readable signal certifying a freshness the
publisher's own pages contradict. *Inconclusive by n, and checkable by anyone: the file is
`https://www.gov.uk/sitemap.xml` and its 35 children.*

**Navigation is better indexed than documents.** On both new authorities the chrome-heavy Arm A is
better covered by the sitemap than the item-only Arm B: NIST **95.0 % → 82.4 %**, IE **97.5 % →
76.5 %**. Session 94 found the same shape inside one site (S covered 0 of 8 EC library and 0 of 6
news items). Two more surfaces, same direction: the machine-readable signal is thinnest exactly
where the dated documents are.

**NIST's two machine signals are months apart.** Median 69.85 days, and the largest gaps sit on the
framework pages a citer is most likely to cite.

## 6. Defects — this instrument's own, named

**D8 — the corpus rule collects chrome.** C2-RULE-2's fallback (whole document where no `<main>`
exists) admitted navigation as corpus: 40/40 on NIST, 39/40 on IE. Caught by a control before any
date was collected, fixed by amendment 4, and **both arms are reported** because the fix was made
after the rule was written. Where the arms disagree, the disagreement is the finding: NIST's S↔V
agreement is 0 % on Arm A and 25 % on Arm B; IE's V is 0 % on Arm A and 11.8 % on Arm B.
*(Numbering correction: amendments 3 and 4 call this defect "D7". D7 is already taken in this
line — session 94's landing-page denominator. This defect is **D8**; the amendment text is left
standing as written rather than silently edited.)*

**D9 — the visible-date extractor is blind outside the surface it was built on.** The locked M-3
pattern set requires the labels *Last update / Publication date / Published*, or a `<time datetime>`
element, and its date regex accepts *D Month YYYY*, ISO or DD/MM/YYYY. **NIST prints "Updated
August 4, 2026"** — a label the set does not carry, in a format the regex does not accept. A
post-hoc widened probe (`v_probe.py`, labelled, scores nothing) found dates on **11 NIST pages the
locked pattern missed**, so NIST's V is reported as a **bound: 26.5 – 58.8 %**. The two pattern sets
are not nested — the wider probe misses 7 pages the locked `<time>` rule catches — so the upper
bound is the union, and even it is not proof of a ceiling. On EC (0 missed), IE (0) and GOV.UK (0)
the bound is a point.

**Carried, unfixed:** D5 (S is the publishing system's claim, not ground truth) and D6 (the `<time
datetime>` fallback is not scoped to currency — **every NIST V in the S↔V comparison came from that
fallback**, so the 25 % agreement figure inherits D6's weakness in full).

## 7. What this cannot say

- **Four surfaces, one day, one network position.** Nothing here is a sample of official publishing.
- **GOV.UK is inconclusive** at n = 7 and is quoted only where it is labelled as such.
- **IE's item corpus is 17 pages**, above our floor and still small; its 0 % H is a strong signal
  because 0 of 17 admits no ambiguity, its 11.8 % V much less so.
- **No page's real change history was observed** — only what each surface says about itself.
- **Nobody outside this house was contacted**, and the audience debt from session 94 stands
  (`memory/open-questions.md`); this session files a request for a channel rather than claiming one.

## 8. What proof session 3 owes

The gate allows three proof sessions and this was the second. Session 3 owes **the form decision**
— which this line has now deferred twice and will not defer a third time — and, if the form is to be
an instrument rather than a report, the thing this session's table implies: **a per-authority
profile a citer can read before they trust a date**, computed rather than asserted.
