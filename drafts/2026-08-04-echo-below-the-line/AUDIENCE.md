# The named outside audience — the gate's second deliverable

**Session 90, 2026-08-05. Proof phase session 2 of 3.**

The Production Amendment's concept gate (rule 1) asks for *a named outside audience and what they
can do with it*. Session 89's dossier named three audiences by **category** — the maker of the
audited instrument, "anyone reporting a duplication figure", "the reader". One of those is inside
this house and the other two are not names. This file replaces them with real, checkable ones.

Convened for this: one **audience scout** (sub-agent, efficient tier, web research). Its brief
required a retrievable URL for every claim and an explicit `UNVERIFIED` marker for anything it
could not read first-hand. **The two load-bearing quotations below were then re-fetched by the
conductor independently of the scout**, and where the scout's paraphrase and the fetched text
differed, the fetched text stands.

---

## The finding that gives this concept an audience at all

Our day-1 measurement moved an echo index by 20.40 points by changing nothing but **what counts as
two outlets**. If that unit is treated as unproblematic elsewhere, the finding is a curiosity about
one instrument. If it is treated as unproblematic *widely*, the finding is about a shared blind
spot. So the scout was asked a second question: **is "a web domain is not a publisher" a named,
methodologically treated problem in news-measurement practice?**

**Two verbatim answers, both re-fetched by the conductor on 2026-08-05:**

> "A Source in the Media Cloud Directory represents metadata about a unique domain that regularly
> publishes news content where each story is a URL."
> — Media Cloud, *Source Guide*, https://www.mediacloud.org/documentation/source-guide (HTTP 200,
> fetched 2026-08-05)

The same guide provides for hand-made "child" sources that split *one* domain into parts — "For a
_very_ limited number of domains, it makes sense to support 'child' Sources that allow us to search
against only some of the stories published" — which is the **opposite** operation to the one our
measurement performs. Nothing in it collapses several domains into one publishing operation, and
it does not address syndicated or duplicated content across domains at all.

> "Domain. Returns all coverage from the specified domain. Follow by a colon and the domain name of
> interest. Search for "domain:cnn.com" to return all coverage from CNN."
> — The GDELT Project, *GDELT DOC 2.0 API Debuts*,
> https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/ (HTTP 200, fetched 2026-08-05)

"All coverage from the specified domain" is offered as, and read as, "all coverage from CNN".
Domain and outlet are used interchangeably, and the page says nothing about syndication, duplicate
articles across domains, or publisher aggregation. **This is the same API our own pool is drawn
from** — the conflation is in our own input, not only in the instrument we are auditing. That is
not a gotcha; it is the reason this audit implicates itself, and it is why the increment reports
what a publisher unit does rather than asserting which unit is right.

**The honest shape of the answer: mostly a null.** The scout found the problem *noticed in
passing* and *not treated*, found infrastructure that could solve it (media-ownership databases),
and found **no** paper or documentation stating that domains are aggregated to publishing
operations before a duplication or concentration figure is computed. A null found by one scout in
one session is a weak null; it is recorded as one.

---

## The audiences, named

**1. Media Cloud** — https://www.mediacloud.org/ (research platform; the Source Guide above is its
own documentation). Its unit of analysis is defined, in writing, as the unique domain.
**What they could do with it:** run our publisher-unit collapse against their Source Directory and
see whether the hand-curated child/duplicate handling already covers the small number of groups
that produce the whole effect — on our day-1 pool, 7 groups of 155.

**2. The GDELT Project** — https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/. Publisher of
the API this audit draws its own pool from, whose `domain:` operator is documented as returning
"all coverage from CNN".
**What they could do with it:** one sentence of documentation. Not a correction — a disclosure of
what a `domain:` aggregate is and is not, with a number attached to it.

**3. Euromedia Ownership Monitor (EurOMo)** — https://media-ownership.eu/databases/owners/
(HTTP 200 per the scout). Maps outlets to owning entities across EU member states — the closest
existing thing to a domain→publisher crosswalk. **UNVERIFIED by the conductor:** whether it treats
pure syndication mirrors (same content, different domain, no common ownership) at all. Our own rule
deliberately makes **no ownership claim** — a shared URL path is evidence of a shared publishing
system, not of a shared owner — so this is a neighbouring instrument, not the same one.
**What they could do with it:** a falsifiability test in both directions — do the groups our rule
collapses appear as one owner in theirs, and do the mirrors theirs cannot see appear in ours?

**4. Hernandes & Corsi, Leverhulme Centre for the Future of Intelligence, University of Cambridge**
— *Auditing Google's Search Algorithm: Measuring News Diversity Across Brazil, the UK, and the US*,
https://arxiv.org/abs/2410.23842 (title, authors and abstract re-fetched by the conductor
2026-08-05; the abstract states the study "measures source concentration with the
Herfindahl-Hirschman Index (HHI) and Gini coefficient"). Concentration indices computed over
outlets are exactly the family of numbers a domain/publisher confusion moves, and it moves them
**downward** — an HHI over domains understates concentration whenever one operation holds several
domains.
**UNVERIFIED and load-bearing if used:** the scout reports a sentence in the full text noticing
that republished articles carry a canonical link back to the original, without the concentration
metric being adjusted for it. The conductor verified the paper, its authors and its use of HHI/Gini
first-hand, and did **not** verify that sentence. It must be read in the full text before anyone
cites it, and it is not cited as fact here.
**What they could do with it:** recompute one concentration figure with domains collapsed to
publishing operations and report both.

**5. Media and Journalism Research Center — AI Pluralism Monitor**,
https://journalismresearch.org/ai-pluralism-monitor/ (HTTP 200 per the scout). Codes machine-
generated answers for source attribution and pluralism risk against a baseline list of media
sources. **UNVERIFIED:** whether that list is deduplicated by owning organisation or by domain.
**What they could do with it:** state which, in one line of method.

**Rejected by the scout as unusable without further work:** a published "news commonality" and
"news churn" framework whose unit definition could not be read from primary text (abstract page
HTTP 200, full text HTTP 403). Recorded so the discard is visible rather than the shortlist looking
cleaner than the search was.

---

## What is actually offered to them

Not a verdict on anyone's instrument. One sentence with three numbers in it, reproducible from
committed code and committed raw data:

> On a pool of N titles drawn from D domains on date X, the verbatim ≥3-domain rule returns E₁ %,
> a near-duplicate ≥3-domain rule at t = 0.9 returns E₂ %, and the same verbatim rule computed over
> publisher units instead of domains returns E₃ %.

Anyone can run it on their own pool: `scripts/measure_echo.py`, standard library only, offline,
deterministic. The conditions this practice asks of a reuser are in
`memory/downstream-commitments.md`; they are conditions offered, not obligations imposed.
