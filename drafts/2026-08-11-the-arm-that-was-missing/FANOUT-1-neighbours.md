# Neighbours check: TikTok public-availability time series

Research date: 2026-08-11. All URLs below were fetched directly (via HTTP GET or a fetch tool) on this date unless marked otherwise.

---

## Q1 — Does any third party publish a free, continuous, at-scale public-availability series for TikTok videos (or a comparable platform)?

**Short answer:** One project exists that matches the *shape* of the measurement (daily availability checks, published dashboard, no platform credential) but it is neither at-scale (11 videos, not thousands) nor currently updating (frozen since 2026-01-14, confirmed by HTTP `Last-Modified` header even though today is 2026-08-11). No other continuous, published, at-scale availability tracker for TikTok was found. For comparable large platforms (YouTube, Twitter/X), the closest analogues are one-off or bounded academic studies, not standing public dashboards.

| item | URL | date | what it actually is | scale/cadence |
|---|---|---|---|---|
| TikTok Research API — Availability Dashboard | https://playground.tiktok-audit.com/api-na/ | page content generated 2026-01-14; server confirms no changes since (checked 2026-08-11) | A public dashboard run by AI Forensics/tiktok-audit.com that daily-checks a small set of videos known to be missing from TikTok's Research API, to see if TikTok fixes the gap. Not a general "is this video still up" tracker — it specifically tracks API-vs-platform mismatch, and only for videos already flagged as problem cases. | 11 videos tracked total; date axis in the page runs 2025-04-09 to 2026-01-14; HTTP `Last-Modified: Wed, 14 Jan 2026 20:53:43 GMT` on 2026-08-11 fetch shows the page has not regenerated in ~7 months despite claiming "daily" checks |
| mrtn3000/tiktok-audit (GitHub) | https://github.com/mrtn3000/tiktok-audit | repo active into 2025 | Source/data repo behind the tiktok-audit.com blog and (apparently) the playground dashboard; contains audit code, schemas, blog posts, not a public per-video availability time series export | Not quantified in README as a video-availability series |
| "Video Unavailable": Analysis and Prediction of Deleted and Moderated YouTube Videos (Kurdi, Albadi, Mishra) | https://ieeexplore.ieee.org/document/9381310 | IEEE/ACM ASONAM 2020 | A **comparable-platform** near-miss: a one-off academic study, not a continuously running public dashboard | ~73,000 YouTube videos tracked over **one week** |
| A Longitudinal Assessment of the Persistence of Twitter Datasets (Zubiaga) | https://arxiv.org/abs/1709.09186 | submitted 2017-09-26 | Comparable-platform near-miss: re-collected 30 Twitter datasets (147M+ tweets) once, years apart, to measure what fraction of tweet IDs were still resolvable — a bounded academic re-check, not a running public series | 147M+ tweets, 30 datasets, single before/after comparison (2012–2016 vs. May 2016) |

**Quoted load-bearing text:**

- Dashboard prose (fetched HTML): "TikTok offers an API for researchers that allows access of public TikTok data, but sometimes videos are not available through the API although they are available on the platform... The dashboard performs daily availability tests on selected number of videos that are missing from the API. Note that although this dashboards only monitors a dozen of videos, we have identified the same issue on thousands of other pieces."
- Dashboard footer (fetched HTML): "Dashboard generated on: 2026-01-14 21:53:41 ... Methodology: Automated daily availability checks of selected videos."
- HTTP response header on 2026-08-11 GET of the dashboard: `last-modified: Wed, 14 Jan 2026 20:53:43 GMT` against `date: Tue, 11 Aug 2026 04:03:16 GMT` — i.e. the "daily" dashboard has not actually updated in roughly seven months.
- Stat cards in the fetched HTML: "11 / Total Videos Tracked", "0 / Available Videos", "0 / Unavailable Videos", "11 / Videos with Errors".

**Verdict on Q1:** No one publishes a free, continuous, at-scale (thousands+) public-presence series for TikTok videos. The one project close in spirit (tiktok-audit.com's dashboard) is small-scale (11 videos), narrowly scoped (only videos already known to be API-missing, not a random/representative sample of TikTok), and appears to have stopped updating around 2026-01-14 despite its own "daily checks" claim.

---

## Q2 — Published work measuring link rot / disappearance of social-media videos cited as sources (Wikipedia, news, academic papers), especially TikTok?

**Short answer:** General web/Wikipedia link-rot literature is well established and includes some figures for social-media content broadly, but nothing found is TikTok-specific *citation* decay (i.e., no study tracked TikTok URLs cited inside Wikipedia articles, news articles, or academic reference lists specifically). The closest TikTok-specific persistence numbers come from public-health content-analysis studies that re-checked TikTok video accessibility over time for their own sample, not from a citation-decay framing.

| item | URL | date | what it actually is | scale/headline numbers |
|---|---|---|---|---|
| Losing My Revolution: How Many Resources Shared on Social Media Have Been Lost? (SalahEldeen & Nelson) | https://arxiv.org/abs/1209.3026 | submitted 2012-09-13 | Classic study of link/resource loss for content shared on social media (not TikTok-specific — predates TikTok) | "about 11% lost and 20% archived after just a year... an average of 27% lost and 41% archived after two and a half years" |
| Characterizing "Permanently Dead" Links on Wikipedia | https://dl.acm.org/doi/10.1145/3517745.3561451 / https://web.eecs.umich.edu/~harshavm/papers/imc22.pdf | ACM IMC 2022 | Study of Wikipedia's dead external links generally; not social-media- or TikTok-specific | Not independently re-verified in this pass (found via search only, not fetched in full) |
| Pew Research Center link-rot analysis | reported via https://www.searchenginejournal.com/38-of-webpages-from-2013-have-vanished-pew-study-finds/516834/ | 2024 | General web/Wikipedia link-rot study, not TikTok- or social-media-video-specific | "38% of webpages from 2013 are no longer accessible a decade later"; "54% of Wikipedia pages have at least one link in their 'References' section pointing to a non-existent page" (secondary summary, not independently verified against the original Pew report in this pass) |
| Changes in Viewer Engagement and Accessibility of Popular Vaping Videos on TikTok: A 12-Month Prospective Study (Rutherford et al.) | https://pmc.ncbi.nlm.nih.gov/articles/PMC8834819/ | published 2022-01-20, Int. J. Environ. Res. Public Health | **TikTok-specific** video-accessibility persistence study — but of a topical sample (vaping videos), not of videos cited as sources elsewhere | 802 videos at baseline (Nov 2020); "562 (70.1%) remained publicly available" at 9-month follow-up (Aug 2021); "511 (63.71%) of the original videos remained publicly accessible" at 12 months (Nov 2021) |

**Quoted load-bearing text:**

- SalahEldeen & Nelson abstract (as fetched): "about 11% lost and 20% archived after just a year... an average of 27% lost and 41% archived after two and a half years."
- Rutherford et al. (as fetched): "Of the 802 videos in the original sample, 562 (70.1%) remained publicly available" at 9 months; "511 (63.71%) of the original videos remained publicly accessible" at 12 months.

**Verdict on Q2:** I found no study that measures link rot of TikTok videos specifically **as cited sources** in Wikipedia, news articles, or academic reference lists. What exists is (a) general web/Wikipedia link-rot literature that is not platform-specific, and (b) TikTok-specific but topic-sampled accessibility studies (vaping videos) that are not framed around citation/reference decay. This is a genuine gap, not a weak match — I am reporting it as "nothing found" for the citation-decay angle specifically.

---

## Q3 — Published work measuring a research API's coverage from the outside against an independently established ground truth (besides arXiv:2506.09746)?

**Short answer:** Yes — several others exist, including at least one published well after June 2025 that is very close in method to what arXiv:2506.09746 does, and goes further by using sockpuppet accounts as ground truth.

| item | URL | date | what it actually is | scale/headline numbers |
|---|---|---|---|---|
| Auditing Meta and TikTok Research API Data Access under Article 40(12) of the Digital Services Act (Bekavac & Mayer) | https://arxiv.org/abs/2601.12390 (HTML: https://arxiv.org/html/2601.12390v1) | submitted **18 Jan 2026** (confirmed via arXiv "Submission history": "Sun, 18 Jan 2026 12:59:11 UTC") | **This is the "other" post-June-2025 paper.** Reconstructs full information feeds for two controlled sockpuppet accounts (2024 US presidential election on TikTok; 2025 German federal election on Instagram) and benchmarks against what the Research APIs return — i.e. exactly the "ground truth vs. API" comparison the task describes | "researchers can access only around 75% (TikTok For You feed)... 50% (Instagram Explore feed) of the posts shown to users"; "For accessible posts, researchers can only access 17% (TikTok) and 42% [Instagram]" of metadata parameters; "between 17.7% and 23.3% of posts were no longer accessible within weeks" (temporal loss) |
| Beyond the margin of error: a systematic and replicable audit of the TikTok research API (Pearson, Silver, Robinson, Azadi, Schillo) | https://www.tandfonline.com/doi/full/10.1080/1369118X.2024.2420032 (paywalled, 403 on direct fetch; details via Semantic Scholar search listing) | Information, Communication & Society, Vol 28 No 3, pp. 452–470 (Nov 2024) | Predates 2506.09746; two research teams independently audited the TikTok Research API against the TikTok website/front-end (tobacco and elections use cases), comparing API vs. front-end metadata | Not independently re-verified with a direct fetch (source paywalled at 403); reported via secondary search summary only, flag as **not fully verified** |
| Revisiting Algorithmic Audits of TikTok: Poor Reproducibility and Short-term Validity of Findings (Mosnar et al.) | https://arxiv.org/abs/2504.18140 | submitted 25 Apr 2025, ACM SIGIR 2025 | Adjacent but **not a strong match**: studies reproducibility of sockpuppet *recommender-algorithm* audits over time, not API-vs-ground-truth data coverage | N/A — different measurement target (algorithm behaviour, not content/API availability) |
| The Accountability Paradox: How Platform API Restrictions Undermine AI Transparency Mandates (Burnat & Davidson) | https://arxiv.org/abs/2505.11577 | v1 submitted 16 May 2025; later revisions through 2026 | Comparative policy/structural audit framework across X/Twitter, Reddit, TikTok, Meta API restrictions; identifies "audit blind-spots" but abstract does not describe a quantitative ground-truth-vs-API measurement | Framework/policy paper, not quantified coverage numbers in the parts checked |
| Beyond the Checkbox: Strengthening DSA Compliance Through Social Media Algorithmic Auditing (Solarova, Mesarčík, Pecher, Srba) | https://arxiv.org/abs/2601.18405 | submitted 26 Jan 2026 | Reviews existing DSA audit *reports* generally (minors profiling, recommender transparency, targeted ads); does not itself run an API-vs-ground-truth coverage measurement and is not TikTok-specific | Not a quantitative coverage study |

**Quoted load-bearing text (2601.12390):**

- Abstract: "This paper presents a systematic audit of research-access modalities by comparing data obtained through platforms' Research APIs with data collected about the same platforms' user-visible public information environment (PIE)."
- Methodology: "reconstruct full information feeds for two controlled sockpuppet accounts during two election periods and benchmark these against the data retrievable for the same posts through the corresponding Research APIs."
- Headline numbers: "researchers can access only around 75% (TikTok For You feed) ... 50% (Instagram Explore feed) of the posts shown to users"; "only 17% (TikTok) and 42% [Instagram]" of metadata parameters survive; "between 17.7% and 23.3% of posts were no longer accessible within weeks."
- arXiv submission-history record (raw HTML, fetched directly): "[Submitted on 18 Jan 2026] ... Sun, 18 Jan 2026 12:59:11 UTC (1,438 KB)."

**Verdict on Q3:** Yes, others exist. The clearest post-June-2025 match is arXiv:2601.12390 (18 Jan 2026), which does the ground-truth-vs-API comparison directly and quantitatively for both TikTok and Meta, and additionally reports temporal content-removal rates (17.7–23.3% gone within weeks) — a data point that also bears on Q1/Q2. The Pearson et al. 2024 paper is an earlier "other" example but I could not independently verify its figures (paywalled).

---

## Q4 — Has any third party tested or commented on TikTok's Feb 26, 2026 changelog entry ("Updated data pipeline logic to ensure comprehensive coverage of all public video content")?

**Short answer:** The changelog entry itself is real and was verified by direct fetch. I found no third party — AI Forensics, academic, journalistic, or otherwise — that has tested, cited, or commented on this specific entry.

| item | URL | date | what it actually is | scale/cadence |
|---|---|---|---|---|
| TikTok Developer Products Changelog | https://developers.tiktok.com/doc/changelog | entry dated Feb 26, 2026; page fetched 2026-08-11 | Official TikTok changelog; contains the exact entry in question | N/A (changelog, not a data series) |

**Quoted text (verified via direct `curl` of the live page, not a summarizing tool):**
- Raw HTML fetch confirms the string is present verbatim: "February 26, 2026" and "comprehensive coverage of all public video content" both appear in the page as fetched on 2026-08-11.

**What I checked for a response and found nothing:**
- The AI Forensics tiktok-audit.com dashboard (the one entity actually running daily API-vs-platform checks) shows no activity after 2026-01-14 — i.e. it stopped updating *before* the Feb 26, 2026 changelog entry and has not resumed to test it (confirmed via HTTP `Last-Modified` header, see Q1/Q5).
- AI Forensics' publications list (aiforensics.org/work) has no TikTok/Research-API item after the original 2025-06-12 report; nothing referencing the Feb 2026 changelog.
- Web search for the entry text combined with "AI Forensics," "tested," "verify," "researchers," and "2026" returned no independent commentary — only TikTok's own changelog and SEO/marketing blog posts listing the change as one bullet among many API updates, none of which report having tested the claim.

**Verdict on Q4:** Nothing found. No third party appears to have tested or publicly commented on this specific claim. This is a clean negative, not a weak match.

---

## Q5 — Anything published since 2026-01-14 by AI Forensics about TikTok's Research API or the tiktok-audit.com dashboard?

**Short answer: I found nothing.** AI Forensics' most recent TikTok/Research-API-specific output is the 12 June 2025 report ("TikTok's Research API: Problems Without Explanations") and its underlying dashboard, and neither has been updated since 2026-01-14.

| item | URL | date | what it actually is | notes |
|---|---|---|---|---|
| Tiktok's Research API: Problems without Explanations (AI Forensics work page) | https://aiforensics.org/work/tk-api | page/report dated 12 June 2025 | Landing page for the report and dashboard | Fetched directly: "Regarding TikTok or Research API: No publications specifically about TikTok or the Research API appear to be dated after January 14, 2026." |
| TK_API Report PDF (v3) | https://aiforensics.org/uploads/TK_API__Report_v3.pdf | HTTP header confirms `last-modified: Tue, 17 Jun 2025 12:20:31 GMT` (checked via `curl -I` on 2026-08-11) | The full report PDF, version 3 | Not modified since 17 June 2025, well before the 2026-01-14 cutoff |
| playground.tiktok-audit.com dashboard | https://playground.tiktok-audit.com/api-na/ | HTTP header confirms `last-modified: Wed, 14 Jan 2026 20:53:43 GMT` (checked via `curl -I` on 2026-08-11) | The daily-check dashboard described in Q1 | Frozen exactly at the 2026-01-14 cutoff date — no update in the ~7 months since, despite the page's own claim of "daily" checks |
| AI Forensics /work listing, items dated ≥2026-01-14 | https://aiforensics.org/work | fetched 2026-08-11 | Full chronological list of AI Forensics publications from Jan 2026 onward | None concern TikTok or the Research API (see list below) |

**AI Forensics publications dated on/after 2026-01-14, per the fetched /work page (none are TikTok/Research-API related):**
- Jan 15, 2026 — Dutch Parliamentary Elections 2025 Report
- Jan 20, 2026 — AI-Generated Image Abuse: An Update on Grok Unleashed
- Feb 12, 2026 — On-Device Foundational Biases: How Summarization Can Perpetuate Biases
- Apr 1, 2026 — Artificial Elections 2.0: Generative AI in the 2026 French Elections
- Apr 8, 2026 — Harassment as Infrastructure: How Telegram's design enables TFGBV
- Apr 23, 2026 — Networks of Abuse, No Accountability
- May 13, 2026 — Snapchat's DSA Ad Transparency
- Jul 28, 2026 — Unmoderated by Design: How Hugging Face Enables NCII

**Quoted load-bearing text:**
- HTTP header from direct `curl -I` of the dashboard on 2026-08-11: `last-modified: Wed, 14 Jan 2026 20:53:43 GMT`.
- HTTP header from direct `curl -I` of the report PDF on 2026-08-11: `last-modified: Tue, 17 Jun 2025 12:20:31 GMT`.
- Fetched AI Forensics work-page summary: "No publications specifically about TikTok or the Research API appear to be dated after January 14, 2026. The most recent TikTok-related item is from December 3, 2025 (Agentic AI Accounts), and the Research API report is from June 12, 2025."

**Verdict on Q5:** Nothing published by AI Forensics about TikTok's Research API since 2026-01-14. This is a firm negative, backed by HTTP-header evidence (not just page text) on two separate AI Forensics assets, plus a full chronological scan of their publications list.

---

## WHAT I COULD NOT OPEN

| URL | status | notes |
|---|---|---|
| https://www.tandfonline.com/doi/abs/10.1080/1369118X.2024.2420032 | 403 Forbidden | "Beyond the margin of error" TikTok API audit — abstract/figures for this item are reported only via secondary search-result summaries (Semantic Scholar listing), not independently verified against the primary source |
| https://www.tandfonline.com/doi/full/10.1080/1369118X.2024.2420032 | 403 Forbidden | Same paper, full-text URL |
| https://www.researchgate.net/publication/385634547_Beyond_the_margin_of_error_a_systematic_and_replicable_audit_of_the_TikTok_research_API | 403 Forbidden ("ResearchGate — Temporarily Unavailable") | Mirror attempt for the same paper, also failed |
| https://arxiv.org/abs/2504.18140 (via WebFetch tool) | 503 Service Unavailable on first WebFetch attempt | Recovered via direct `curl`, so content was ultimately obtained — flagging the failed attempt for completeness |

Two arXiv-tool calls (`mcp__Arxiv__get_paper_data` for 2504.18140 and 2601.12390) also failed with `429`/generic HTTP errors from the arXiv API; both papers were successfully retrieved instead via direct `curl`/WebFetch of the arXiv abstract/HTML pages, so no information gap resulted.

---

## Summary judgment across all five questions

1. No continuous, at-scale, public TikTok availability tracker exists. The nearest thing (tiktok-audit.com dashboard) is small (11 videos), narrowly scoped, and has stopped updating.
2. No TikTok-specific citation/link-rot study was found; general web/Wikipedia link-rot literature exists but isn't platform- or citation-specific to TikTok, and TikTok-specific accessibility studies exist but aren't framed around citations.
3. Yes — arXiv:2601.12390 (18 Jan 2026) is a strong post-June-2025 "other" example doing exactly the ground-truth-vs-API comparison, with TikTok-specific coverage (~75% of feed accessible, ~17% of metadata fields survive) and even a content-persistence figure (17.7–23.3% gone within weeks).
4. No one has tested or commented on the Feb 26, 2026 TikTok changelog claim.
5. Nothing published by AI Forensics on TikTok/Research API since 2026-01-14 — confirmed both by page content and by HTTP `Last-Modified` headers on their two key TikTok assets.
