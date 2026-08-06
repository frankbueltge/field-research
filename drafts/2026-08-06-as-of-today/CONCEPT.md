# CONCEPT — "As of Today"

**Concept gate document, Production Amendment rule 1. Proof session 1 of at most 3.**
Opened 2026-08-06 (session 94). Status: **concept argued, first increment run, not shipped**
(the receiving gate pins the instrument count at 21 while PR 413 is open).

## The claim, in one page

Official policy pages are cited every day in the form *"as of &lt;date&gt;"*. If the citer has no
archive of the page's history — and a great many citers do not; this session could not reach one
either (see the journal's opening record) — then the date can only come from what the page says
about itself. There are exactly three such statements, and no more:

- **H**, the HTTP `Last-Modified` header the server returns. Free, automatic, read by every
  machine that touches the page.
- **S**, the `<lastmod>` the site publishes for that URL in its own XML sitemap. Machine-readable,
  one extra fetch away, but only for URLs the sitemap lists.
- **V**, a date printed in the page for a human to read.

**The claim:** these three do not carry the same information, they are not equally available, and
the one a machine gets for free is the one that carries none. Concretely, on the surface measured
here: **H reported delivery time on every page in the corpus — never older than 26 minutes** — while
the two publisher-stated signals said the same thing as each other on every page where both existed,
and were unavailable on 6 of 40 and 23 of 40 pages respectively. The automatic answer to *"when did
this change?"* is *"just now"*, always, on a page that may not have changed since January 2023.

**What this claim is not.** It is not a claim about when these pages actually changed. Capture
history would be needed for that and this session could not reach any. Every number here is a
statement about the *signals*, not about the edits — and `S` is itself only the publishing system's
assertion, no more verified than the rest.

## The named outside audience, and what they can do with it

**Anyone who runs an automated watch on official policy pages** — the shape of tool that polls a
page and reports "this changed". The pattern is real and has real users: the Environmental Data &
Governance Initiative maintains a public "Website Monitoring" project for exactly this on government
sites (https://github.com/edgi-govdata-archiving/web-monitoring). A monitor of that kind that reads
`Last-Modified` as a change date will, on this surface, date every page to the last few minutes —
including pages whose own printed date is 2023 — and a monitor that instead trusts the sitemap will
be blind to the sections where the dated documents actually live.

**What is measured and what is not, on this point.** Measured: all 40 headers younger than 26
minutes, and `ETag` values of the form `W/"<unix-timestamp>-gzip"` matching them. **Not measured:
whether a conditional request eventually returns a false "changed".** A probe run this session
re-sent the collected validators for one page seven times over 9 minutes 21 seconds and received
`304 Not Modified` every time (`probe_conditional.log`), so the validators are stable at least that
long, and the interval at which the delivered object is re-rendered — which is what would decide it
— is unknown. The sentence above is therefore about *dating a page*, not about *polling* it.

**What they can do with it, concretely:** (1) not read `H` as a change date on this surface — what
a conditional request does over longer intervals is untested here and is named above as untested;
(2) know that `S` covers `/policies/` here and covers **none** of
`/news/` or `/library/` — the guidelines, notices and press items a reader is most likely to cite;
(3) fall back to the printed `V` label, which was present on 34 of 40 pages and on **all 32** item
pages, and is the only date most of these pages offer at all.

**A second, plainer audience:** anyone writing "as of &lt;date&gt;" about one of these pages. For
the 40 measured here, at 2026-08-06T08:26:37Z, the date they could defend was the printed one, and
the one their tooling handed them was that morning. Whether that holds for a page outside this
corpus is not established by this run.

## The first checkable increment — run, in this session

Committed in this directory: the pre-registration (written before any code), the corpus rule and
corpus, the collection script, the raw signal table, the analysis script, and `FINDINGS.md` with
four pre-registered predictions scored — **one held, three killed**. 40 URLs, one authority, one
moment: 2026-08-06T08:26:37Z. Anyone can re-run `collect_corpus.py`, `collect_signals.py`,
`analyse.py` and get their own numbers; the numbers will differ, because the surface moves.

## Nearest neighbours, and the daylight

Established by a prior-art reconnaissance convened this session (sources checked and returned with
retrievable URLs; the specialist's summary is in `PRIOR-ART.md`):

- **Reference rot and content drift are thoroughly measured.** Klein et al., *PLOS ONE* 2014
  (https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0115253); Zittrain, Albert &
  Lessig, *Harvard Law Review Forum* 2014
  (https://harvardlawreview.org/forum/vol-127/perma-scoping-and-addressing-the-problem-of-link-and-reference-rot-in-legal-citations/).
  **Daylight:** they ask whether a cited page still resolves or still says the same thing. This asks
  something upstream and cheaper: whether the page can tell a citer when it last changed *at all*.
- **The mechanism behind our P1 is already known and already measured once, at web scale.**
  Thompson, WebSci'24 (https://arxiv.org/abs/2404.09770) found `Last-Modified` present on only ~17 %
  of responses and, in one crawl, 53 % of those stamped within 0.0 s of the crawl itself. **So P1
  is not a discovery and this concept does not claim it as one.** What is not in that paper: this
  surface, the three-way comparison, and the coverage asymmetry.
- **Crawler-freshness research routes around the problem rather than measuring it** — Cho &
  Garcia-Molina, *ACM TODS* 2003 (https://dl.acm.org/doi/10.1145/958942.958945) estimate change
  frequency statistically instead of trusting declared timestamps. The largest crawler's own public
  guidance says it trusts `<lastmod>` only "if it's consistently and verifiably accurate"
  (https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
- **Nobody found measuring the agreement between a page's self-declared update metadata and its
  observed change history, on a government or policy corpus.** Reported as *not found* by the
  specialist, which is a claim about a search, not about the world.

**The daylight in one sentence:** the unreliability of `Last-Modified` is folklore with one
web-scale measurement behind it; what nobody has published is the *citer's-eye triangulation* —
which of the three available signals exists, on which pages of a live regulatory surface, and what
a person is left with when the machine-readable ones are absent or wrong.

## What the arc would be, if the gate holds

**Proof session 2:** a second authority, so that nothing here is mistaken for a fact about
government pages in general — and a repeat run against this same corpus, which turns a single
snapshot into the beginning of a change record this practice can hold. **Proof session 3:** the form
decision, and whether the useful object is a ledger, a lookup a citer can query, or a one-page
finding. **If the arc is licensed**, the work it argues for is a dated, append-only register of what
each of a set of official surfaces tells a citer about its own currency — an instrument that is
worth more the longer it runs, and that is checkable by anyone with `curl`.

**The condition on all of it (`memory/downstream-commitments.md`):** whatever ships from this line
ships as an offer, with its date, its corpus, its scripts and its stated limits — and the limit that
travels first is that these are measurements of signals, never of edits.
