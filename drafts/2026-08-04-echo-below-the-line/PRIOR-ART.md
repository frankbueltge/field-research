# Prior art — what is already known, and what is genuinely absent

*Compiled by a prior-art scout convened for this session, 2026-08-04. Every source below was opened
by the scout; where a primary source could not be opened, that is said in the line itself rather
than hidden behind the citation.*

## The methods this increment uses are not new, and are not ours

| Method | Primary source |
|---|---|
| Shingling / resemblance over k-word shingle sets | Broder, Glassman, Manasse, Zweig, *Syntactic Clustering of the Web*, SRC Technical Note 1997-015 (WWW6, 1997) — https://www.microsoft.com/en-us/research/wp-content/uploads/1997/01/src-tn-1997-015.pdf |
| The operational near-duplicate version | Broder, *Identifying and Filtering Near-Duplicate Documents*, CPM 2000 — [link removed 2026-08-19 — a course page hosting another author's text; rights unsettled] |
| SimHash / LSH for cosine similarity | Charikar, *Similarity Estimation Techniques from Rounding Algorithms*, STOC 2002, pp. 380–388 — https://dl.acm.org/doi/10.1145/509907.509965 |
| TF-IDF cosine | Salton & Buckley, *Term-Weighting Approaches in Automatic Text Retrieval*, Information Processing & Management 24(5):513–523, 1988, DOI 10.1016/0306-4573(88)90021-0 |
| **The news-specific version — closest prior work** | Alonso, Fetterly, Manasse, *Duplicate News Story Detection Revisited*, MSR-TR-2013-60 (AIRS 2013) — https://www.microsoft.com/en-us/research/wp-content/uploads/2013/05/paper-1.pdf |

## The absence this concept stands on

**No published number was found for the size of the paraphrase gap in news headlines** — that is,
for the share of near-duplicate coordination that an exact/verbatim rule misses. Alonso et al.
(2013), the closest primary work, quantify *detection quality* (F1, Matthews correlation) across
methods and thresholds on 5.5M news pages; they do not report the quantity above. The scout
reports this as a well-evidenced absence rather than a failed search, and this dossier treats it
as exactly that: an absence, which a later search may fill.

## Established figures on wire copy and repackaging — the wider context

- **UK, 2008:** Lewis, Williams, Franklin, Thomas, Mosdell, *The Quality and Independence of British
  Journalism* (Cardiff University) — 60% of UK press articles and 34% of broadcast stories wholly or
  mainly wire-copy or PR-derived. **Provenance caveat:** the primary PDF at orca.cardiff.ac.uk was
  behind a verification wall and could not be opened; the figure is taken from a contemporaneous
  account that was opened — https://pressgazette.co.uk/churnalism-study-claims-news-mainly-pr-and-wire-copy/ —
  and is therefore **second-hand in this dossier** and must be re-sourced before it appears in any
  shipped work.
- **US, 2010:** Pew Research / Project for Excellence in Journalism, *How News Happens: A Study of
  the News Ecosystem of One American City* (Baltimore, week of 19–25 July 2009) —
  https://www.pewresearch.org/journalism/2010/01/11/how-news-happens/ — of 715 studied stories, 80%
  repeated or repackaged previously published information; 17% contained new reporting. Opened.

## Limits of the sampling frame, from the operator's own documentation

From https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/ and
https://blog.gdeltproject.org/updates-doc-2-0-api/ (both opened by the scout):

1. **`maxrecords` is hard-capped at 250 in article-list mode, with no pagination.** Any pool built
   this way is a capped sample, never a daily census. This binds the audited instrument exactly as
   it binds us.
2. **Rolling coverage window** — by default the last three months are searchable.
3. **Non-English coverage is machine-translated** (65 languages, ~98.4% of non-English volume). An
   "English-language" beat therefore mixes native-English outlets with machine-translated copy —
   which is a *translation-fidelity confound* for any near-duplicate comparison over titles, and is
   the same phenomenon the season brief calls "translation echo".
4. **The operator does not document its own internal deduplication** in the DOC 2.0 documentation.
   Treat within-run duplicate handling as undisclosed, not as absent.

## On the threshold

The literature does **not** support a single portable threshold. Alonso et al. (2013) state
explicitly that "there is no intrinsic correlation between the thresholds for different methods; it
makes sense to select a value for each that typically performs well", and report cutoffs that
cluster only loosely (roughly 0.25–0.5 depending on weighting), with one variant's F1 flat across
0.25–0.75. Henzinger (2006), cited there, reports method-dependent precision (shingling 0.38,
SimHash 0.50, combined 0.79) rather than one cutoff. **Therefore the increment reports a sweep and
refuses a single headline threshold.**

## The strongest reason this is not novel — stated by our own scout

Alonso, Fetterly and Manasse (2013) already ran the general-purpose version of this comparison on a
large syndication-heavy news corpus. A reviewer can fairly say our contribution is "the same
experiment on one particular eight-beat pool", not a new method and not a new empirical fact about
duplication in general. **That objection is accepted as fair.** What remains, if anything remains,
is the *applied* number for a specific live instrument, on a specific day, published before that
instrument's own next version is built — and the audit's usefulness stands or falls on that being
worth having.
