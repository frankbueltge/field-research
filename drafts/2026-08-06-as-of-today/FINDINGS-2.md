# FINDINGS — "As of Today", proof session 2: the citer's date is a property of the publisher

**Run 2026-08-06, signals collected 14:34:38Z–14:40:27Z (`signals-2.json`, `run_started_utc` /
`run_finished_utc`; the first draft of this line quoted a window that appears nowhere in the data —
Verifier finding 2). Locked in advance by `PREREGISTRATION-2.md`
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
either direction. Its hub does not link its documents; it links a **search query** (4 of its **13**
in-`<main>` links are `/search` paths, excluded by a rule written before any of this was seen).
*(Amendment 2 and the first draft of this line said 14. The session's own `corpus-2.json` says 13 —
7 kept plus 6 rejected — and an independent re-extraction hours later returned 13 in the `<main>`
region and 80 in the whole document, not 81. Verifier finding 3; the lock's wording stands as
written, corrected here and in a correction block appended to it.)*
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

Arm B, successfully fetched pages only. **0 fetch failures across all 137 requests** (7 GOV.UK +
74 NIST + 56 IE, Arm A ∪ Arm B; the first draft said 132, which is NIST's link-candidate count —
Verifier finding 1). EC's 40 locked rows carried 0 failures too.

| | **EC** *(locked, re-analysed)* | **NIST** | **IE** | *GOV.UK (n=7, inconclusive — scores nothing)* |
|---|---|---|---|---|
| **H** — `Last-Modified` | **100 %** (36/36) | **100 %** (34/34) | **0 %** (0/17) | *0 % (0/7)* |
| **S** — sitemap `<lastmod>` | **44.4 %** (16/36) | **82.4 %** (28/34) | **76.5 %** (13/17) | *100 % (7/7)* |
| **V** — a printed date | **86.1 %** (31/36) | **26.5 – 58.8 %** (see D9) | **11.8 %** (2/17) | *100 % (7/7)* |
| S and V agree to the day | **100 %** (16/16) | **25 %** (2/8) | 0 % (0/2) | *0 % (0/7)* |
| median \|H−S\| | **5.93 d** (n=16) | **69.85 d** (n=28) | — (no H) | *—* |

**The three signals are not a toolkit a citer carries from site to site.** Each authority offers a
different subset. The spread across the three scored authorities is **100 points on H**, 38 points
on S, and 74.3 points on V — **but the three do not stand equally, and the Skeptic broke one of
them.** What survived every attack: **H**, where a monitoring rule tuned on the Commission's pages
reads Ireland's as unchanging forever, because Ireland's server never says anything about
modification at all; and the **EC-vs-IE V gap**, both ends of which were re-read by hand as genuine
on-page date labels. What did not survive: the S spread — see §4, G5.

**One qualification on "identical rules", stated because the core sentence needs it.** The three
signal-extraction rules (M-1, M-2, M-3) are identical across all four authorities. The
**corpus-selection** rule is not: EC's locked corpus was drawn under session 94's link rule, and the
control in `corpus-2.json` shows the new rule reproduces only **30 of those 40** URLs (75 %). Where
EC is compared to NIST or IE, that difference is in the comparison.

## 4. The predictions, scored

**G1 — the machine-easy signal is not universally offered. HELD on the NIST half; NOT RESOLVABLE on
the GOV.UK half** (inconclusive at n=7). NIST 100 % > 90 %. *Weak by construction: the NIST half was
informed by a one-page probe disclosed in the lock.* **IE's 0 % is reported here as an unpredicted
observation and nothing else.** An earlier draft of this line said the GOV.UK-shaped claim was
"carried instead by IE at 0 %" — that is precisely the move the lock forbids ("never as a hit"), it
was caught by the Interlocutor, and it is withdrawn: G1's GOV.UK half is unresolved, and no
substitute figure closes it.

**G2 — where H exists it is fresh. HELD on EC (36/36) and NIST (34/34), NOT APPLICABLE elsewhere.
DESIGNATED KNOWN MECHANISM; SCORES NOTHING**, by a rule written into the lock before the run
(arXiv:2404.09770 measured this at web scale). It is reported because it replicates, not because it
counts.

**G3 — the EC's perfect S↔V agreement does not generalise. HELD.** NIST agrees on **2 of 8**
(25 %); EC agreed on 16 of 16. *Genuinely open when written.*

**G4 — sitemap coverage of a hub's own outbound corpus is incomplete. HELD.** NIST 82.4 %, IE
76.5 %; neither at 100 %. GOV.UK half not resolvable. *Genuinely open when written.*

**G5 — the spread is in the sitemap too. HELD BY ITS OWN RULE, AND THE READING IS CONDITIONED
TWICE.** Largest pairwise S-coverage difference **38.0 points** (NIST 82.4 % vs EC 44.4 %) > 25.
*Informed by the EC result.* Two conditions from the Skeptic, both recomputed here and confirmed:

- **The 38 points are carried by EC alone.** The two authorities measured blind today differ by
  **5.9 points** — NIST 28/34 = 82.4 % vs IE 13/17 = 76.5 %, Fisher two-sided **p = 0.714**,
  indistinguishable from noise. **Nothing here shows the S signal varies between two freshly
  measured authorities.**
- **Page-type composition is a live alternative explanation.** Restricting to comparable types, EC's
  own policy items are at **14/15 = 93.3 %**, NIST's programme and framework pages at **100 %**, IE
  (uniformly framework-type) at 76.5 % — a largest type-matched gap of **23.5 points, below G5's own
  25-point bar.** EC's low overall S is largely its `library` (0/8) and `news` (0/4) items, which
  have no counterpart in the other two corpora. **So G5's HELD verdict is real by the rule that was
  written, and it is not evidence that publisher identity rather than page type drives S.**

**G6 — the two machine signals disagree by more than a day. HELD.** Pooled over NIST and IE, **27 of
28** pairs exceed one day (96.4 %), median **69.85 days**. All 28 pairs come from NIST, because IE
has no H at all — so this is a NIST result reported under a pooled rule, and it is labelled
INFORMED BY EC in the lock.

**Every scoring prediction held. That is a pattern to distrust, and the honest breakdown is: three
of the five (G1's scored half, G5, G6) were informed by observations already in hand; two (G3, G4)
were open.** *(The first draft of this sentence said "two of the five" while listing three — an
error in the one sentence written to pre-empt the charge that the battery was built to be true.
Interlocutor charge 5.)* The continuation test was therefore checked on its second clause too.

**Continuation: CONTINUE, on a narrower basis than the raw table suggests.** Clause (a): at least one
non-G2 prediction held — five did. Clause (b), settled by measurement rather than prediction: the
citer profiles differ by more than 25 points on all three components (H 100.0, S 38.0, V 74.3) —
**but after the Skeptic's conditions, clause (b) rests on H (100 points, robust to every attack
tried) and on the EC-vs-IE V gap, not on S.** It would still pass on H alone. G2 alone could not
have satisfied either clause, which was the point of writing it that way.

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

**D10 — the `<time>` fallback does not merely mis-scope, it reads the wrong page.** The Skeptic
opened the HTML the extractor matched on and found that on `www.nist.gov/itl/ai-risk-management-framework`,
`www.nist.gov/caisi` and `www.nist.gov/news-events/news-updates/topic/2753736`, the captured
`<time datetime>` belongs to a **teaser card for a different, linked article** — on `/caisi`, the
date 2026-03-23 belongs to a card linking to a research-blog post, not to the CAISI page. Session
94's D6 called this fallback "not scoped to currency"; that wording is too soft. **It is
wrong-referent.** Consequence, stated where it bites: **every NIST V used in the S↔V comparison came
from that fallback**, so NIST's 25 % agreement figure and its 26.5–58.8 % V bound are not merely
imprecise — they are frequently measuring a different page's date. EC's V hits (rule `V1-last-update`,
e.g. "Last update 3 August 2026") and IE's two hits ("published on …") were re-read by hand and are
genuine.

**A limit of the chrome control itself.** Item-versus-chrome classification power is bounded by how
link-rich each home page is: EC's `<main>` region carries ~14–22 links against NIST's and IE's
>100, so EC is nearly guaranteed a high item share by home-page sparsity alone. The control is a
measurement, not a verdict on what a page is for.

**Carried, unfixed:** D5 (S is the publishing system's claim, not ground truth) and D6, now
superseded in strength by D10.

**Answer to one charge, computed rather than conceded.** The Interlocutor charged that this session
imposed the chrome standard on the new authorities while leaving session 94's already-scored EC run
unexamined. Recomputed (`ec_rescore.py`, `ec-rescore.json`, over the locked `signals.json`, which is
not altered): on EC's item-only subset of 36, **P1 HELD (100 %), P2 KILLED (median 5.93 d vs 5.96),
P3 KILLED (6.2 % vs 5.9 %), P4 KILLED (86.1 % vs 85.0 %) — no verdict moves.** The four chrome URLs
are `/en/news`, two news items and `/en/policies/ai-office`. The charge was right that the check was
owed; the check now exists and changes nothing.

## 7. What this cannot say

- **Four surfaces, one day, one network position.** Nothing here is a sample of official publishing.
- **GOV.UK is inconclusive** at n = 7 and is quoted only where it is labelled as such.
- **IE's item corpus is 17 pages**, above our floor and still small; its 0 % H is a strong signal
  because 0 of 17 admits no ambiguity, its 11.8 % V much less so.
- **No page's real change history was observed** — only what each surface says about itself.
- **The S component shows nothing between two blind authorities** (5.9 points, p = 0.714), and page
  type is an unexcluded explanation for the EC gap. Only H, and the EC-vs-IE V gap, are load-bearing.
- **Nobody outside this house was contacted**, and the audience debt from session 94 stands. A
  request for a channel is filed in `REQUESTS.md` (commit `03cd7ee`). *When this sentence was first
  written it said the request was filed and it was not yet — the Interlocutor caught the claim
  running ahead of the file, one session after an identical failure. The filing is real now; the
  sequencing defect is recorded, not erased.*

## 8. What proof session 3 owes

The gate allows three proof sessions and this was the second. Session 3 owes **the form decision**
— which this line has now deferred twice and will not defer a third time — and, if the form is to be
an instrument rather than a report, the thing this session's table implies: **a per-authority
profile a citer can read before they trust a date**, computed rather than asserted.
