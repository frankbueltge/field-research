# Findings — What the Record Rests On

*Draft, 2026-08-01. Not shipped. No gauntlet verdict exists for this state. Every number below is
produced by `analyse.py` from `inventory.json` and `probe-2026-08-01.json`, and every one of them
carries the interval `results.json` computes for it. The probe ran from 03:56:45Z to 04:39:15Z on
2026-08-01, from one datacenter address behind a forward proxy.*

## The short version

Of 260 sampled citations in a public register of AI harms, **64.3% [56.8–71.9]** still delivered
the passage the register stored, to this vantage, on this day.

The interesting part is the other third, because it is not what a link-rot study expects:

| what happened at the other end | weighted estimate | 95% interval |
|---|---|---|
| the document is **gone** — 404, 410, or the host no longer resolves | **2.7%** | [1.1 – 4.3] |
| the document was **withheld from this vantage** — 401, 402, 403, 451 | **23.6%** | [16.7 – 30.5] |
| the citation **redirected to the site root** (the soft-404 case) | 0.1% | [0.0 – 0.3] |
| everything else that did not answer — 4xx and 5xx other than the above, timeouts, TLS and connection failures | **5.1%** | [2.0 – 8.2] |
| the page answered and the stored passage is **no longer in it** | 2.0% of pages that served a document | [0.1 – 4.0] |
| the page answered and **still holds** the stored passage | 95.2% of pages that served a document | [92.1 – 98.2] |

The first four rows are the whole of what did not answer with a document: they sum to 31.5%, and
the estimate for "did not answer 200" computed independently is 31.4% [24.1 – 38.8]. The 0.1-point
gap is rounding of each row, not a missing class. That residual row — 19 of 260 records: six other
4xx, six timeouts, three 5xx, two unclassified statuses, one TLS failure, one connection failure —
was **missing from the first version of this table**, which printed only the named classes and left
5 weighted points off the page. It was put back after a hostile reader added the rows up.

**Almost none of the loss is decay. Most of it is access control.** Refusal outnumbers
disappearance here by roughly nine to one, and the two are not the same fact about the world: a 403
says a document was not served *to us*, and a 404 says it is not there.

That distinction is not a hedge. It is the finding, and the control layer is what turns it from an
excuse into a measurement.

## The control layer, and why the refusals are not a hole in the data

For every case where the live page did not clearly still hold the stored passage, the instrument
fetched the **archived capture nearest to and not after the date the register recorded downloading
the document**, and ran it through the same extractor against the same fingerprint.

- **97 cases were sent to the control. 63 could be decided. In 53 of those 63, the archived copy
  still holds the stored passage** — most of them at an overlap of 0.98 to 1.00.
- Of the **82 citations that would not serve this vantage at all**, 44 have an archived capture from
  at or before the register's own download date that still contains the passage the register stored.

So the extractor works, the register's stored copies are faithful to what was on those pages when it
took them, and for a large share of the citations this vantage could not open, **the evidence is
still retrievable — from the archive, not from the publisher.**

Where the control comes back negative it is reported as negative: in 8 cases the archived copy did
not hold the passage either, which means the mismatch predates today and cannot be called drift. One
of the five outright `ABSENT` cases is of that kind, and it is not counted as live-web loss anywhere
in this document.

## The archive is doing the custody work

| | weighted estimate | 95% interval |
|---|---|---|
| a public archive holds at least one capture of the cited URL | **98.0%** | [95.6 – 100.0] |
| it holds one from **at or before** the date the register cited it | **90.1%** | [84.7 – 95.5] |

The second number is the one that matters and it is the one nobody usually reports. An archive that
first captured a page a year after a register cited it is not evidence of what was cited; it is
evidence of what the page later became. Nine citations in ten are covered at the right time. The
rest are covered at the wrong time, or not at all.

For 24 of 260 URLs (9.2%) the capture index itself refused this vantage after four attempts with
backoff. Those are recorded as `CDX_UNAVAILABLE` and are excluded from both archive estimates —
never counted as an absence of captures.

## Five documents that answered and no longer say what they were cited for

These are the whole `ABSENT` class, listed individually because at this sample size a rate would
hide more than it shows. Four of the five have an archived copy from the register's download date
that holds the passage at 0.91–1.00 overlap, which is what makes them attributable to the live page
rather than to the instrument:

| report | overlap live | overlap archived | reading |
|---|---|---|---|
| 121 | 0.000 | 0.981 | page answers, cited text not in what it serves |
| 488 | 0.000 | 1.000 | page answers, cited text not in what it serves |
| 796 | 0.000 | 0.999 | page answers, cited text not in what it serves |
| 6881 | 0.027 | 0.908 | page answers, cited text not in what it serves |
| 1521 | 0.000 | 0.000 | **not attributable** — the archived copy does not hold it either |

Two further pages returned 200 and yielded so little text that nothing could be compared
(`SHELL`), while their archived copies from the register's download date hold the passage in full.
Those are not counted as drift; they are counted as pages that no longer serve a document to a
reader like this one.

## The vantage measured itself, and the result was the opposite of the assumption

Every non-200 was retried once with an honest, self-identifying research user-agent. **Seven URLs
that refused a browser-like string answered 200 to the research string.** The instrument's primary
request imitates a desktop browser because the comparison literature does — and on this corpus, that
choice *cost* seven documents rather than winning any. The assumption that a crawler must look like
a browser to be let in did not survive its own test here.

Both outcomes are recorded per URL in `probe-2026-08-01.json`. The headline numbers above use the
primary request only; using the better of the two would lower the withheld rate by roughly 2.7
points and is not done, because a rate assembled from whichever attempt worked is not a rate.

## Age

Equal allocation gives 20 records per stratum, which is enough to estimate a corpus rate and **not**
enough to fit a decay curve, and none is fitted. What can be said:

- All 12 hard-gone citations (404 / 410 / no DNS) are in strata published **2022 or earlier**. The
  four most recent strata — 2023, 2024, 2025, 2026, 80 records — contain none.
- The oldest stratum is the worst served today: **7 of 20** citations published 2014 or earlier
  delivered their passage, against 11 to 15 of 20 in every other stratum.
- Withholding runs the other way: the highest refusal counts are in the newest strata (8 of 20 in
  2024, 6 of 20 in each of 2025 and 2026) against 0 of 20 in 2017. **Conjecture, not a finding:**
  access control is a property of the publisher today rather than of the document's age, and recent
  coverage sits behind more of it. Nothing here tests that, and a test would need the same URLs
  probed from more than one vantage.

## How this sits against published rates

Carefully, because these are different populations measured by different rules, and a comparison of
headline numbers across them is exactly the mistake this section exists to avoid.

The closest published comparator read first-hand for this work is Pew Research Center's 2024 study
(Chapekis, Bestvater, Remy, Rivero, https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/):
25% of sampled pages from 2013–2023 no longer accessible as of October 2023; 38% of pages that
existed in 2013 gone a decade later; 23% of news webpages carrying at least one broken link; 11% of
all Wikipedia reference links no longer accessible. Its rule is deliberately conservative — a page
counts as dead only on error codes that definitively signal the page or host is gone.

Measured by a rule of comparable strictness, this register's citations are gone at 2.7%. That is
far below the general-web and Wikipedia-reference figures above, for a corpus that is overwhelmingly
news journalism — the class the same study finds among the least durable. **This sentence is
orientation and not a result**, and it is written without emphasis on purpose: the populations, the
sampling frames and the dead-rules differ, and a reader who carries "an order of magnitude better"
away from here is carrying something this work did not measure. An earlier version of this paragraph
put that comparison in bold as its climax while the paragraph above it disclaimed exactly that move.
A hostile reader called it, and it was right to.

This work does not explain the gap and does not claim to. Three candidate explanations are
compatible with everything measured here, and nothing here separates them: the register's citations
skew to large publishers with durable URL schemes; much of the corpus is recent (2,036 of
6,602 sourced records were published in 2025 or 2026) and has not had time to rot; and the sampling
unit is a citation the register's editors chose, not a link found in the wild. **The honest reading
is that the number is real and its cause is not established.**

On content drift, the comparison is even less direct. The scholarly-drift study
(Jones et al. 2016, https://doi.org/10.1371/journal.pone.0167475) reports three in four references
leading to changed content — but it compares an archived snapshot against the live web and calls
anything short of maximum similarity "drifted." This instrument asks a weaker and more concrete
question: whether at least half the stored passage is still on the page. Against that question,
95.2% of the pages that served this vantage a document still hold it. **The two numbers are not in
conflict; they are answers to different questions**, and the difference between them is a fact about
thresholds, not about the web.

## What this does not say

Repeated from `METHOD.md` because it is the part most likely to be dropped in a summary:

- **Nothing about why.** No class here distinguishes an ordinary expiry from a deliberate removal.
- **No control corpus.** Nothing here says whether citations about AI harm decay faster or slower
  than citations in general. The Pew comparison above is orientation, not a control.
- **One vantage, one day.** A residential address would see a different withheld rate, and no one
  here can run that probe.
- **Lexical, not semantic.** A rewritten page that says the same thing scores as loss.
- **Not an editorial audit.** Nothing in HTTP status data supports a claim about the register's
  practices. The stored-copy field is, on its face, a mitigation this register built against exactly
  this problem — and the control layer above is what shows it works.

## The instrument turned on its own authors, and it cannot see the defect they shipped

Added after this work's Interlocutor observed that a measurement of somebody else's evidence base,
made by a practice with two known holes in its own, had performed no reflexive turn at all. Two
measurements, run with the same code path as everything above, on 2026-08-01:

| what was probed | L1 | what layer 3 would do with it |
|---|---|---|
| a citation in one of this practice's own shipped works, `https://doi.org/10.3030/101135953` | **HTTP_404** | not applicable — it does not answer |
| this practice's own repaired published page, `https://frankbueltge.de/field/werke/2026-07-01-calibration-gap/` | **HTTP_200**, 4,066 words extractable | comparable — it would be scored, and it would score as holding |

The first is the plain one: **that identifier is still dead.** It was published for a claim about
the EU AI Act on 2026-07-01, found dead by accident 27 days later, and it returns 404 today. This
practice's own archive contributes to the 2.7% class it just measured in somebody else's.

The second is the one worth the space. Two days ago this practice established that the same page
served its entire visual argument in inline style attributes the site's policy silently discards —
the words arrived, the drawing did not. **This instrument would have called that page healthy.** It
answers 200, it yields 4,066 words, and every measurement in this document is a measurement of text.
A page can pass all four layers here and still show a reader nothing.

That is not a caveat added for modesty. It is a limit of the design, it is stated as one, and it is
the strongest argument in this document for why a census of citations is not a census of evidence.

## The one sentence this work is for

A register of harms is only as good as what a reader finds when they follow it — and in this corpus
what a reader finds is mostly still there, mostly *because a third-party archive kept it*, while
nearly a quarter of the citations answer a machine with a closed door that says nothing at all about
whether the document behind it still exists.
