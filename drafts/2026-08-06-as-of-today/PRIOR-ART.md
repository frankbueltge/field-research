# PRIOR-ART — what a prior-art specialist returned, 2026-08-06

*Convened as an ephemeral specialist in session 94, before the concept was written up, with the
instruction to return only real retrievable URLs and to say "not found" where nothing exists.
Transcribed here as returned, lightly cut for length; the load-bearing items were independently
re-checked by the Verifier the same session (see the session's journal entry for the verdict).*

## 1 — Reference rot and content drift (established, heavily measured)

- Klein, Van de Sompel, Sanderson, Shankar, Balakireva, Zhou, Tobin (2014), "Scholarly Context Not
  Found: One in Five Articles Suffers from Reference Rot", *PLOS ONE* 9(12): e115253 —
  https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0115253 — measured: ~1 in 5
  articles overall (up to ~70 % of articles that contain web references) cannot have their cited
  web context revisited.
- Zittrain, Albert, Lessig (2014), "Perma: Scoping and Addressing the Problem of Link and Reference
  Rot in Legal Citations", *Harvard Law Review Forum* 127:176 —
  https://harvardlawreview.org/forum/vol-127/perma-scoping-and-addressing-the-problem-of-link-and-reference-rot-in-legal-citations/
  — measured: >70 % of URLs cited in three Harvard law journals and ~50 % in US Supreme Court
  opinions suffer reference rot.
- Liebler & Liebert (2013), "Something Rotten in the State of Legal Citation", *Yale Journal of Law
  & Technology* —
  https://yjolt.org/something-rotten-state-legal-citation-life-span-united-states-supreme-court-citation-containing
  — of 430 internet-link citations in Supreme Court opinions 1996–2010, 29 % dead.
- SalahEldeen & Nelson (2012), "Losing My Revolution", TPDL 2012 — https://arxiv.org/abs/1209.3026
  — ~11 % of shared resources lost after one year, ~27 % after 2.5 years.

## 2 — The specific neighbour: are `Last-Modified` and sitemap `lastmod` reliable change signals?

- Thompson (2024), "Improved methodology for longitudinal Web analytics using Common Crawl",
  ACM WebSci'24 — https://arxiv.org/abs/2404.09770 — **the closest directly-measured hit.**
  Reported by the specialist as: `Last-Modified` present on only ~17 % of successful responses in
  the sampled crawl; for a September 2023 crawl, 53 % of the offsets between claimed
  `Last-Modified` and actual crawl time were exactly 0.0 and 70 % within three seconds — i.e. most
  values are stamped at request time, not at content-change time.
- Cho & Garcia-Molina (2003), "Effective Page Refresh Policies for Web Crawlers", *ACM TODS*
  28(4):390–426 — https://dl.acm.org/doi/10.1145/958942.958945 — the canonical crawler-freshness
  line, which estimates change frequency from observed recrawl history rather than trusting
  declared signals.
- Search-engine documentation on building sitemaps —
  https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap — states that
  `<lastmod>` is used "if it's consistently and verifiably accurate (for example by comparing to the
  last modification of the page)".

**The specialist's stated gap:** no peer-reviewed study was found that isolates `Last-Modified`
accuracy as its primary object, and none measuring sitemap `<lastmod>` accuracy against ground-truth
change history. That is a claim about a search, not about the world.

## 3 — The exact question: self-declared update metadata vs. observed change history

**Not found.** No study located that measures agreement between a page's own stated update metadata
and its actual observed change history, on a government or policy corpus. Closest adjacent item
returned: an analysis of the presence/absence of metadata tags on US government homepages
(https://govfresh.com/thoughts/analyzing-government-website-metadata), which the specialist checked
by direct fetch and reports does *not* address temporal accuracy.

## 4 — Citation practice for pages that change

- Bluebook Rule 18.2.1(d) (archiving cited internet sources; "last visited" only where the source
  gives no other date) —
  https://www.law.georgetown.edu/wp-content/uploads/2018/07/Rule-18-Handout-1.Secara-1.pdf
- APA style, elements of reference list entries (retrieval dates only for sources "designed to
  change over time" and not archived) —
  https://apastyle.apa.org/style-grammar-guidelines/references/elements-list-entry
- Perma.cc, permanent citable snapshots for legal citation — https://perma.cc
- Memento, HTTP datetime negotiation against archives (RFC 7089) — https://mementoweb.org/about/ ;
  https://arxiv.org/abs/0911.1112

## 5 — The daylight, in the specialist's own judgement

Reference rot and "cite a snapshot, not a live date" are settled ground and would add nothing if
re-measured. The gap is in section 2: that `Last-Modified` is often request time is *believed* by
practitioners and stated by search-engine operators themselves, but barely *measured* in the
literature — the 2024 methodology paper is the one concrete quantification found, and it is a
by-product of a paper about something else. Nobody in the retrieved literature has run the
three-way comparison of header, sitemap and printed date on official policy pages as its own
object.

**The specialist's own caution, recorded because it is the sharpest thing it said:** because the
mechanism is already understood and publicly stated by search-engine operators, a reader from the
crawling literature may find the *explanation* unsurprising even if the *comparative measurement* is
new. The contribution has to be framed as an empirical triangulation on a policy surface, **not as
a discovery that `Last-Modified` can be stale.**
