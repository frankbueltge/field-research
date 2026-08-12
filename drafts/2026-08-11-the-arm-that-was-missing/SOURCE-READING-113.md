# Reading the receiver's report to the end — session 113, 2026-08-12

*This arc's signature error, recorded six times, is quoting a page it did not read to the bottom.
Standing check 2 exists because of it. This session applied the check to the one document the whole
arc rests on — and the check fired, against us.*

**Source.** *TikTok's Research API: Problems Without Explanations*, Carlos Entrena-Serrano, Martin
Degeling, Salvatore Romano, Raziye Buse Çetin. arXiv:2506.09746v2, submitted 2025-06-11, revised
2025-06-12. Abstract page: `https://arxiv.org/abs/2506.09746v2`. Full report also published by the
authors' organisation at `https://aiforensics.org/work/tk-api`.

**How it was read.** The abstract and the arXiv comment field were fetched from the abstract page.
The full 18-page PDF was fetched from `https://arxiv.org/pdf/2506.09746v2` and its text extracted
locally, because the HTML rendering returns HTTP 404 and the full-text conversion tool on this
machine failed on a missing system library. **Every quotation below is from that extracted PDF text,
with its section named — with one stated exception: the arXiv comment-field quotation in §4, which
comes from the abstract page and is not in the PDF at all.** *(Corrected after the fact, condition 5
of `INTERLOCUTOR-5.md`: the sentence originally read "every quotation below is from that extracted
text", which was false for that one instance. The adversary checked the quotation itself against the
live abstract page and found it verbatim accurate; what was wrong was this sentence about sourcing,
in a document whose reason for existing is this practice's own history of imprecise sourcing.)*
Sessions 109–112 quoted this work **from its abstract only.**

---

## 1. What sessions 109–112 had, and what it left out

Every previous session on this arc quoted the abstract:

> *"Our experiment reveals that the API fails to provide metadata for one in eight videos provided
> through data donations, including official TikTok videos, advertisements, and content from
> specific accounts, without an apparent reason."*

`OBJECT-ANSWER.md` (session 112) built its D2 on that sentence and on the dashboard page. Neither
document in this repository had read the report's own **Experiment 1** section or its **Summary of
findings**. Both sections were three clicks away for four sessions.

## 2. The passage that changes this arc's framing

**Experiment 1, Data Donation** — quoted in full, including the sentence that matters most to us:

> *"From an initial sample of approximately 260,000 TikToks, we were initially unable to retrieve
> metadata for 70,239. TikTok's API did not have informative error codes that specified why some
> post metadata could not be downloaded (e.g., explaining they had been removed or they were posted
> by private accounts). At this point, to investigate further, we had to rely on scraping TikTok to
> check if the unavailable posts were publicly available on the platform."*

And then:

> *"After scraping TikTok, we confirmed that, out of the 70,239 posts, approximately 36% were not
> public – either deleted, private, or only visible to friends. The other 62.7% were all publicly
> available on the platform, but not retrievable through the API."*

**They ran the public-presence arm.** In 2025, on 70,239 identifiers, and they published the split.

## 3. Summary of findings — the decomposition, quoted whole

> *"The chart below (Figure 6) summarizes our findings by showing what we found about the 70,239
> videos we investigated. We were able to successfully retrieve, after multiple attempts, only 18%
> of the videos for which we missed metadata. Among the 83 percent that remained unavailable, the
> largest share (36%) of videos can be attributed to the videos being deleted or set to private.
> This means that the remaining 46% of the videos were public, but not available via the API. While
> one part of this can be attributed to known limitations of the API (Videos from Canada) we found
> that a similar share of videos is not available because they were marked as advertisements. For
> the remaining 21% of videos, we do not know why the API did not return any information, while
> some might contain minors (another known limitation of the API), a random check did not reveal
> this as the only reason. For the original research based on data donations (which collected a
> total of ≈260k TikToks), this means that roughly 1 in 8 posts (12,46%) of videos could not be
> analyzed."*

## 4. The dashboard, in the report's own words

> *"We decided to create a public dashboard to ensure that the problems we identified are consistent
> over time. We set up a script to regularly check a set of videos that should be available through
> the Research API but were not."*

> *"We monitored the availability of 10 selected videos over one month and found that the majority
> of the videos were consistently not available."*

> *"Our records indicate that certain functionalities have been unavailable since a test conducted
> in December 2024."*

**And the arXiv comment field, which is part of the published record and which no session here had
read:**

> *"We revised our analysis after confirming that several videos we had previously classified as
> content from Chinese creators are actually advertisements. We believe now this is the reason why
> they are not retrieved by the API"*

## 5. What the report does **not** contain, checked rather than assumed

- **No upload dates, no age distribution, no time range for the ~260,000 donated videos.** Searched
  for across the extracted text. The only dated collection window in the report belongs to a
  different experiment: *"we collected the metadata of the first 100 videos shown on the German FYP
  daily for one week (May 14-20, 2025) without being logged in."*
- **No count of how many of the 70,239 fall in each named category** beyond the percentages above.

**This absence is the reason the deliverable of this session is a function and not a number.** We
cannot condition on an age profile the source does not publish, and we will not invent one.

---

## 6. What this does to this arc's own claims — three corrections, all against us

**Correction 1 — the arc did not know the report had already run a coarse, one-time version of its
own arm. Its framing was narrower than that failure, and the first draft of this section overstated
it.** *(Rewritten after condition 2 of `INTERLOCUTOR-5.md`, which sent this practice back to its own
founding documents. What follows is what they actually say, checked here by hand.)*

The founding texts were **already scoped to the dashboard**, and correctly so.
`PREREGISTRATION.md` line 30: *"The claim is about the **arm the dark instrument never had**. That
instrument asked, of eleven videos each day: does the research interface return this video?"* —
*that instrument* is the dashboard. `CONCEPT.md`: *"Their instrument compares one thing against
nothing: it asks the research interface about eleven videos and records the answer, and when the
answer is bad it cannot tell whose fault it is."* Also the dashboard. **On the dashboard the claim
was and remains true.** So the arc's central framing was not in error, and saying it was would be a
different inaccuracy in the opposite direction.

**What is a real failure, and it is a failure of this practice's own standing rule.** Session 108
disclosed plainly that it had read only the abstract — `drafts/2026-08-10-one-receiver-to-the-floor/
DERIVED.md`: *"The paper-index tool and the PDF-to-text conversion both failed on this machine. The
abstract page was fetched directly instead, and no claim in `RESULT.md` depends on the paper's body
text — only on its abstract, authors and submission history, all read from the fetched abstract
page."* That disclosure was honest **on the day it was made**. The standing rule stated in the same
paragraph is: *"a page that fails one route is retried on another before anything depends on it."*
Over the four sessions that followed, a concept gate, an arc, and an object answer all came to depend
on this work — **and no session retried the route.** This session retried it and it succeeded on the
first attempt.

**What the body then showed.** They scraped 70,239 identifiers in 2025 to check public availability
and published the split. So a coarse, one-time version of this arc's arm **already existed in the
public record**, and the arc's account of its own novelty — which turned on the arm being absent
rather than on its being un-repeated — needed narrowing. What is genuinely absent from their
published work is **repetition, dating, and the rate as a function of age.** That is a smaller claim
than this arc has been making in its looser moments, and it is the claim the increment now makes.

**Correction 2 — the one-in-eight is already net of public absence.** Computed in
`receiver_comparison.py`, not asserted: 46 % of 70,239 is 32,310, which is **12.43 %** of 260,000
against the published **12.46 %**. The published headline reproduces the **summary section's
public-but-not-in-API share**. So the videos their own scrape found not to be public are **already
excluded** from the one-in-eight. **A public-presence null cannot deflate their headline, because
they applied one themselves.** The premise this session's own move was reaching for — that their
number was missing a null — is false, and it was false before the session started.

**Correction 3 — on this one axis their instrument is better than ours.** Their scrape distinguished
*"deleted, private, or only visible to friends"*. Ours cannot: session 109's three-arm control with
twenty synthetic identifiers established that this endpoint returns one opaque HTTP 400 for every
kind of absence, including for identifiers that never existed. **We measure a coarser quantity than
they did.** That belongs at the front of anything this arc offers them, not in a limitations
paragraph.

## 7. Two observations about the report, recorded neutrally

Neither is offered as an error found, and neither is load-bearing for anything here. They are
recorded because a document this arc quotes should be quoted accurately, including where it is
internally hard to reconcile.

1. **The public-but-unavailable share appears twice with different values.** The method section says
   **62.7 %** of 70,239; the summary section says **46 %**. They reconcile if the method section's
   split is read as *before* the 18 % recovered on retry and the summary's as *after*
   (62.7 − 18 = 44.7 against 46, residual −1.3 pp). The method section's own two shares sum to
   **98.7 %** rather than 100, and the summary's *"18%"* and *"the 83 percent that remained
   unavailable"* sum to 101.
2. **The abstract compresses the body's decomposition.** The abstract's *"one in eight … without an
   apparent reason"* names advertisements inside that eight, and the body then attributes a share to
   advertisements and a share to a known API limitation, leaving **21 % of 70,239 — 14,750 videos,
   5.67 % of the sample, about one in eighteen — as the share the report says it cannot explain**
   (*"we do not know why the API did not return any information"*). Both figures are the authors'
   own; the difference is which question each answers, and a reader who takes the abstract's phrase
   as applying to the whole one-in-eight is off by roughly a factor of two. **This is a remark about
   compression in an abstract, not about the quality of the work**, and this practice makes it while
   holding a record of six of its own quotation failures.

## 8. What survives, and it is the thing this session builds

Their public-presence check was **one-time, in 2025, on their own corpus, undated in its published
form**. Three things are still absent from the public record and are what this arc can supply:

1. **The rate as a function of video age**, with intervals, from an independent corpus — so that any
   measured non-public share can be compared against what age alone would produce.
2. **A repeatable, credential-free instrument** that any third party can point at any list on any
   named day, producing the same measurement from their own vantage.
3. **A dated series** rather than a snapshot.

Under (1), one bound can be stated **without** knowing their corpus's ages, and it is stated in the
increment: a weighted mean cannot exceed its largest component, so **no age composition of our
reference population reaches their 36 %** (worst band 5y+: 17.80 %, upper bound 21.95 %). That is
evidence **for** their reading — their API-failure set is enriched for non-public content beyond what
age explains — and it is the direction the arithmetic actually points.
