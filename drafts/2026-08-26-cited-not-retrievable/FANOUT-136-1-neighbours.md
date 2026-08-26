# Fan-out 1 — the neighbours check (K-A), published unedited

**Session 136, 2026-08-26.** One of two independent search fan-outs convened for
`PREREGISTRATION-136.md` K-A. A fan-out is not a role and has **no voice in any verdict**; it finds
material and reports it with retrievable URLs. Its brief was to find the nearest neighbours of the
proposed measurement and, for each, to name the daylight — or to report honestly that there is none.

**It is reproduced below exactly as returned, including its named reachability gaps.** Two of those
gaps are load-bearing and are carried into `CONCEPT.md` §6 rather than buried here: the FAccT 2026
paper's methodology could not be read (ACM Digital Library returned HTTP 403), and Quack's full text
was not extracted.

---

## NEAREST NEIGHBOURS

### 1. Link rot / reference rot in Wikipedia

**"When Online Content Disappears" (Link Rot and Digital Decay on Government, News and Other Webpages)** — Athena Chapekis, Samuel Bestvater, Emma Remy, Gonzalo Rivero; Pew Research Center Data Labs; May 2024.
https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/ · report PDF: https://www.pewresearch.org/wp-content/uploads/sites/20/2024/05/pl_2024.05.17_link-rot_report.pdf
Measures: a one-shot October–November 2023 accessibility sweep of ~1 million reference links in a random sample of 50,000 **English-language** Wikipedia pages (11% of references inaccessible; 53–54% of pages carry at least one broken reference), plus a separate Common Crawl sweep and a Twitter panel.
DAYLIGHT: This is a single snapshot, English-only, with no per-domain/platform breakdown at all (no TikTok, no video platforms); it has an escalating **four-round** re-check (Oct 12–15 initial; Oct 16–17 with randomised browser headers; Oct 27–28 re-check of unresolved and HTTP 429 with a 3-second timeout; Nov 6 DNS re-lookup) — the closest thing in this literature to re-request confirmation, but the rounds are days apart and each round *changes the method*, so it is escalation, not identical-request confirmation, and it never runs daily or longitudinally.

**"Characterizing 'Permanently Dead' Links on Wikipedia"** — Anish Nyayachavadi, Jingyuan Zhu, Harsha V. Madhyastha (University of Michigan); ACM Internet Measurement Conference (IMC '22), Nice, October 2022; DOI 10.1145/3517745.3561451.
PDF (fetched and text-extracted): https://bpb-us-w1.wpmucdn.com/sites.usc.edu/dist/4/966/files/2022/09/imc22-perm-deadlinks.pdf · ACM page (403 to me): https://dl.acm.org/doi/10.1145/3517745.3561451
Measures: the live-web status of 10,000 English Wikipedia links tagged "permanently dead," classified into DNS failure / timeout / 404 / 200 / other, with soft-404 detection, checked in March and again September 2022.
DAYLIGHT: This is the single most important negative result for the "already done" question. The paper states verbatim that **"When checking any link, IABot determines whether the link is dead by attempting to fetch the link only once,"** and its own method is *"We issued a HTTP GET request for every URL and noted the outcome"* — one request per URL, English only, two manual snapshots, no platform breakdown, no daily cadence, no per-item re-request confirmation.

**InternetArchiveBot** — Internet Archive / Wikimedia community; running instrument on 400+ Wikimedia wikis.
https://meta.wikimedia.org/wiki/InternetArchiveBot · https://meta.wikimedia.org/wiki/InternetArchiveBot/How_the_bot_fixes_broken_links
Measures: continuous detection and archival replacement of broken external links across many language editions — the only genuinely multilingual, continuously running link-health instrument I found.
DAYLIGHT: It **does** carry a confirmation rule — verbatim, *"A URL must fail three scans consecutively in order to be considered dead"*, with *"URLs to be scanned must not have been scanned in the last seven days… if the last scan… resulted in a response marking the URL dead, then the waiting period is reduced to three days"* (minimum nine days to "dead"), and *"If a dead URL is scanned and found to be alive, its status will be reset to alive immediately."* But this is **three spaced scans over ≥9 days, each of which is a single fetch** — not five immediate re-requests — it is not daily, it publishes no longitudinal availability dataset or platform breakdown, it is a repair tool rather than a measurement, and it certainly publishes no refutations of its own readings.

**"Perma: Scoping and Addressing the Problem of Link and Reference Rot in Legal Citations"** — Jonathan Zittrain, Kendra Albert, Lawrence Lessig; Harvard Law Review Forum 127:176, 2014.
https://harvardlawreview.org/forum/vol-127/perma-scoping-and-addressing-the-problem-of-link-and-reference-rot-in-legal-citations/ · SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2329161
Measures: link and reference rot in a fixed corpus of legal citations (>70% of URLs in law journals and 50% in US Supreme Court opinions no longer reach the cited material).
DAYLIGHT: A one-time retrospective corpus audit of a non-Wikipedia corpus, with no repeated probing, no platform dimension, and no ongoing instrument.

**"Scholarly Context Not Found: One in Five Articles Suffers from Reference Rot"** — Martin Klein, Herbert Van de Sompel, Robert Sanderson, Harihar Shankar, Lyudmila Balakireva, Ke Zhou, Richard Tobin; PLOS ONE 9(12):e115253, 2014.
https://pmc.ncbi.nlm.nih.gov/articles/PMC4277367/ · https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0115253
Measures: link rot plus content drift across URI references in STM articles, tested once with cURL GET in March 2013.
DAYLIGHT: It has the *germ* of the confirmation idea — verbatim: *"In order to account for possible transient errors, we revisited all URIs that fell into the rotten category two weeks after the initial attempt and changed their status from rotten to active if the response was successful in the second run."* That is **one** re-check, two weeks later, one-directional (rotten→active only), on a non-Wikipedia corpus, non-longitudinal. Not five immediate re-requests, and not applied to both directions of state change.

**"Wikipedia Citations: A comprehensive dataset of citations with identifiers extracted from English Wikipedia"** — Harshdeep Singh, Robert West, Giovanni Colavizza; *Quantitative Science Studies* 2(1):1–19, 2021; arXiv:2007.07022.
https://arxiv.org/abs/2007.07022 · https://direct.mit.edu/qss/article/2/1/1/97565/
Measures: extraction and classification of 29.3M citations from 6.1M English Wikipedia articles into books / journals / web content.
DAYLIGHT: A static corpus, English-only, with no availability probing whatsoever — it is the kind of corpus the proposed instrument would need, not a measurement of retrievability.

**"A Comparative Study of Reference Reliability in Multiple Language Editions of Wikipedia"** — Aitolkyn Baigutanova, Diego Saez-Trumper, Miriam Redi, Meeyoung Cha, Pablo Aragón; CIKM '23, 2023; arXiv:2309.00196.
https://arxiv.org/abs/2309.00196
Measures: reliability *labels* (the perennial-sources list) applied to reference domains across multiple language editions of >5M articles.
DAYLIGHT: It is genuinely cross-lingual — the dimension most link-rot work lacks — but it measures editor-assigned trustworthiness of domains, never whether the URLs still resolve, and never over time.

**"Research: Characterizing Wikipedia Citation Usage"** — Wikimedia Foundation Research, 2018.
https://meta.wikimedia.org/wiki/Research:Characterizing_Wikipedia_Citation_Usage/Second_Round_of_Analysis
Measures: reader *clicks* and hovers on external citations in English Wikipedia, broken out by top-clicked domain.
DAYLIGHT: Measures citation usage, not citation availability; English-only; no video-platform breakdown. This is the closest thing I found to an official Wikimedia "external link health" report, and **it does not measure link health at all** — I could not locate any Wikimedia Research report that measures external link availability longitudinally.

### 2. Availability/retrievability of TikTok video URLs over time

**"Changes in Viewer Engagement and Accessibility of Popular Vaping Videos on TikTok: A 12-Month Prospective Study"** — Rutherford et al.; *International Journal of Environmental Research and Public Health*, 2022.
https://pmc.ncbi.nlm.nih.gov/articles/PMC8834819/
Measures: whether 802 baseline vaping TikTok videos were still reachable by following their URLs at 9 and 12 months (29.9% removed at 9 months, 36.3% at 12 months; ~13–14% of removals were creator-privatised rather than platform-removed).
DAYLIGHT: This is the nearest neighbour on TikTok URL retrievability — but it is manual, at **two** timepoints only, on a single topical sample, with a single URL check per video and no re-request confirmation, and it has nothing to do with Wikipedia or citation corpora.

**"Auditing Meta and TikTok Research API Data Access under Article 40(12) of the Digital Services Act"** — Luka Bekavac, Simon Mayer (University of St. Gallen); arXiv:2601.12390, January 2026.
https://arxiv.org/html/2601.12390
Measures: the gap between the "public information environment" (including what non-logged-in visitors see) and Research-API-retrievable data, plus temporal loss — verbatim: *"To quantify this temporal data loss, we re-queried the collected posts in the PIE of the sockpuppet on TikTok at multiple points after initial collection"* and *"Across three observation points, between 17.7% and 23.3% of posts were no longer accessible within weeks"* (Feb 17, Feb 19, Mar 4 2025; 82.27% / 81.51% / 76.66% online).
DAYLIGHT: Three observation points over ~two weeks, not daily; the paper gives **no** HTTP method, no logged-out/logged-in statement for the re-query, and explicitly no retry protocol per item; sample is FYP-sourced, not Wikipedia-cited; and there is no published refutation layer.

**"TikTok's Research API: Problems Without Explanations"** — Carlos Entrena-Serrano, Martin Degeling, Salvatore Romano, Raziye Buse Çetin (AI Forensics / Brussels School of Governance); 2025; arXiv:2506.09746.
https://arxiv.org/abs/2506.09746 · Dashboard: https://playground.tiktok-audit.com/api-na/ · https://www.brussels-school.be/research/publications/tiktoks-research-api-problems-without-explanations
Measures: verbatim — *"We monitored the availability of 10 selected videos over one month and found that the majority of the videos were consistently not available"*, published as a live public dashboard doing *"Automated daily availability checks."* Also: the API fails to return metadata for roughly one in eight donated videos.
DAYLIGHT: **This is the closest running instrument in existence to the proposal** — daily, longitudinal, availability-state, publicly dashboarded. But (a) it probes the **credentialed Research API**, not credential-free public URLs (the dashboard I fetched shows 11 videos tracked, 0 available, 0 unavailable, 11 in error state, with the caveat *"Error are problems on our end, not TikTok"*); (b) n≈10–11 videos, not a corpus; (c) no Wikipedia or citation dimension; (d) no per-item re-request confirmation is described anywhere in the paper or the dashboard; (e) no published refutations of its own readings.

**"Platforms' Research API Data Access: What Users See vs. What Researchers can Retrieve"** — Savvas Zannettou, Olivia Nemes-Nemeth, Oshrat Ayalon, Angelica Goetzen, Krishna P. Gummadi, Elissa M. Redmiles, Franziska Roesner; ACM FAccT 2026; DOI 10.1145/3805689.3812237.
https://dl.acm.org/doi/10.1145/3805689.3812237
Measures: the discrepancy between the user-visible public information environment and what the TikTok Research API / Meta Content Library return.
DAYLIGHT: **Reachability gap — I could not retrieve this paper's full text** (ACM DL returned HTTP 403; no open preprint found). Title, author list and venue above come from a search result, not from a page I opened. On its abstract-level framing it is a cross-sectional API-vs-public comparison, not a longitudinal daily probe and not Wikipedia-linked, but I cannot verify its methodology section.

### 3. Social-media citations in Wikipedia

**Gap — this is a finding, not a source.** I ran four distinct searches for studies quantifying how many Wikipedia references point to social-media or short-form-video domains and how those decay, and **found none**. What exists instead:

- **Wikipedia:Reliable sources** (policy, not measurement): https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources — user-generated sites including Facebook, Instagram and X are "generally unacceptable," with narrow exceptions for verified official accounts as self-published sources. This means the proposed measurement is probing a *policy-marginal but non-empty* citation class that nobody has counted.
- **TWikiL — the Twitter Wikipedia Link Dataset** — Florian Meier et al.; ICWSM 2022; arXiv:2201.05848 (https://arxiv.org/abs/2201.05848) — measures all *Wikipedia links posted on Twitter* 2006–2021. DAYLIGHT: this is the **opposite direction** of the proposed measurement (Wikipedia cited on social media, not social media cited in Wikipedia), and measures presence, not availability.
- Pew's Wikipedia sweep (above) covers reference links in aggregate but explicitly publishes **no domain or platform breakdown**.

I found **no** study, at any scale, in any language edition, that counts TikTok URLs used as references inside Wikipedia.

### 4. Immediate repeated re-requests to confirm an apparent state change

This is where the proposal is most distinctive. What I found:

**"Augur: Internet-Wide Detection of Connectivity Disruptions"** — Paul Pearce, Roya Ensafi, Frank Li, Nick Feamster, Vern Paxson; IEEE Symposium on Security and Privacy (Oakland) 2017.
https://faculty.cc.gatech.edu/~pearce/papers/augur_oakland_2017.pdf (fetched and text-extracted)
Measures: reachability between Internet endpoints via TCP/IP side channels, across ~180 countries over 17 days.
DAYLIGHT: **This is the strongest methodological ancestor of the "confirm before you believe" move.** Augur's stated design goal is verbatim *"Sound. The technique should avoid false positives and ensure that repeated measurements of the same phenomenon produce the same outcome,"* implemented as sequential hypothesis testing that *"performs repeated online trials until it can determine the value of the prior with the specified false positive and negative rates"* — *"For a given site Si and reflector Rj, we perform a series of N trials"*, with an expected-trials computation and, verbatim, *"If there are more trials we restart the algorithm. If we have exhausted our trials, we output the result blockage… is undetermined."* But: it is an **adaptive statistical stopping rule, not a fixed five-shot immediate re-request**; the trial order is deliberately **randomised and spread over weeks** (*"we randomize our trial order… and run experiments over the course of weeks"*), which is the opposite of immediate confirmation; and it measures network reachability, not URL retrievability, with no citation corpus and no per-item published readings.

**"Censored Planet: An Internet-wide, Longitudinal Censorship Observatory"** — Ram Sundara Raman, Prerana Shenoy, Katharina Kohls, Roya Ensafi; ACM CCS 2020.
https://ensa.fi/papers/CCS20censoredplanet.pdf (fetched and text-extracted) · https://dl.acm.org/doi/10.1145/3372297.3417883 · https://docs.censoredplanet.org/
Measures: weekly reachability of ~2,000 domains from >95,000 vantage points in 200+ countries since August 2018 (60+ billion data points), detecting 15 censorship events over 20 months.
DAYLIGHT: I searched the extracted full text for retry/re-request logic and **found none**. Censored Planet confirms apparent state changes **statistically and by comparison**, not by repetition of the individual request: verbatim it uses *"a two-step clustering technique to identify confirmed instances of"* blocking, takes a *"conservative approach in confirming a blockpage, and only do so [when] they are confirmed through the control measurements."* Confirmation is by control measurement + clustering + time-series anomaly detection (Bitmap, Mann-Kendall), never by re-requesting the same item N times immediately.

**OONI (Open Observatory of Network Interference)** — running instrument.
https://ooni.org/support/interpreting-ooni-data/ · https://ooni.org/post/2026-measuring-internet-censorship-trends-challenges-impact/
Measures: per-network, per-URL reachability from volunteer probes, annotating results "confirmed blocked" only when a known blockpage fingerprint matches; Pipeline v5 classifies "blocked"/"down"/"OK" with confidence estimates.
DAYLIGHT: OONI's confirmation is **fingerprint- and control-based**, plus a probabilistic aggregate across many vantage points and time — a *cross-sectional* confirmation strategy. It does not re-request a single item five times to confirm a state change; instead it relies on redundancy across probes. Note OONI *does* publish open data and open methodologies for peer review, which is the nearest analogue to the proposal's "publish refutations of the instrument's own readings" — but publishing raw data for others to challenge is not the same as the instrument publishing refutations of its own readings, and I found **no** instrument in any field that does the latter as a stated practice.

**InternetArchiveBot's three-consecutive-scan rule** (full detail in §1 above) is, on the evidence I gathered, the **only** deployed confirmation-before-believing rule in the Wikipedia link-health world — and it is spaced over ≥9 days with one fetch per scan.

### 5. Are platform public-data coverage claims testable from outside without credentialed access?

**"Auditing Meta and TikTok Research API Data Access under Article 40(12) DSA"** (full cite in §2) — https://arxiv.org/html/2601.12390 — measures overlapping filters excluding up to ~50% of the public information environment, stripping up to ~83% of contextual metadata, under limits down to ~1,000 requests/day. DAYLIGHT: it tests the *API's* coverage against a scraped baseline, but the baseline itself is a sockpuppet FYP crawl, not a credential-free, third-party-anchored corpus like Wikipedia citations; and it is a one-off audit, not a running instrument.

**"The Great Data Standoff: Researchers vs. Platforms Under the Digital Services Act"** — ICWSM 2026; arXiv:2505.01122. https://arxiv.org/html/2505.01122v2 — analyses the researcher-platform access conflict under the DSA.

**"Using the DSA to Study Platforms"** — Verfassungsblog. https://verfassungsblog.de/dsa-platforms-digital-services-act/ — argues directly that scraping is the necessary check on platform disclosures: it reports that *researchers used scraping to discover that TikTok's API omits the company's own videos, as well as Taylor Swift's*, and frames Art. 40(12) public-data access as "an effective backstop to every other transparency mandate."

**"Seeing like an API: Platform-mediated research and the politics of access"** — Zoë Natalia Cullen, Nicole B. Ellison, Irene V. Pasquetto; *Big Data & Society*, 2026. https://doi.org/10.1177/20539517261461463 — conceptual account of how API mediation shapes what can be known about platforms.

DAYLIGHT across this cluster: all of these are **audits of the API against a scraped baseline**. None uses an *external, independently-maintained, human-curated corpus* (like Wikipedia references) as the anchor, none is credential-free end-to-end, and none runs continuously.

---

## WHAT I COULD NOT REACH

- **ACM Digital Library** returned HTTP 403 on every attempt — I could not read the FAccT 2026 paper (10.1145/3805689.3812237) or the ACM-hosted versions of the IMC/CCS papers. I worked around this for IMC '22 and Censored Planet via author-hosted PDFs, but **not** for the FAccT paper, whose methodology therefore remains unverified by me.
- **ResearchGate** returned HTTP 403 throughout.
- The original University of Michigan host for the IMC '22 PDF returned HTTP 503, and `harshavm.engin.umich.edu` failed DNS resolution; I used a USC mirror instead.
- Pew's separate methodology page (`.../when-online-content-disappears-methodology/`) returned 404; I extracted the four-round procedure from the report PDF instead.
- **Quack** (VanderSloot et al., USENIX Security 2018, https://ensa.fi/papers/quack_sec18.pdf) — I did not extract its full text, so I cannot state whether it uses per-trial repetition. This is a live gap in my §4 coverage.
- I found **no** Wikimedia Foundation research report measuring external link availability longitudinally, and **no** study of social-media or TikTok citations *inside* Wikipedia at any scale. I searched for both repeatedly; their absence is my finding, not a retrieval failure I can attribute to a blocked source.

---

## DIRECT ANSWER

**NO.** No published, running or completed study measures the retrievability of platform-video citations in Wikipedia — or in any comparable citation corpus — with per-item re-request confirmation. The evidence is convergent across four separate strands. First, on the corpus side, the only large Wikipedia availability sweep with a published number (Pew Research Center, May 2024) is English-only, one-shot, and publishes **no** domain or platform breakdown, so no video-platform figure exists to compare against; the IMC '22 study of Wikipedia's "permanently dead" links is likewise English-only, 10,000 links, two manual snapshots, and states its own method as *"We issued a HTTP GET request for every URL"* — one request, and it records verbatim that Wikipedia's own production instrument *"determines whether the link is dead by attempting to fetch the link only once."* Second, on the platform side, the two instruments that touch TikTok availability longitudinally are the AI Forensics/BSoG dashboard (verbatim *"We monitored the availability of 10 selected videos over one month"*, via the **credentialed Research API**, ~10–11 videos, no described retry logic) and the St. Gallen Art. 40(12) audit (three observation points over two weeks, no stated HTTP method or per-item retry) — neither is credential-free, corpus-scale, daily, multilingual, or Wikipedia-anchored. Third, on the methodological move itself, the nearest ancestors confirm state changes by *other means*: Augur uses sequential hypothesis testing with repeated trials but deliberately randomises and spreads them over weeks; Censored Planet and OONI confirm via control measurements, blockpage fingerprints and clustering across vantage points, not by re-requesting the same item; and the only deployed "confirm before believing" rule in the Wikipedia world — InternetArchiveBot's *"A URL must fail three scans consecutively"* over a minimum of nine days — is three spaced single fetches, not five immediate re-requests, and is a repair tool that publishes no measurement series. Fourth, I found no study of any kind counting social-media or TikTok URLs used as references in Wikipedia, in any language edition, so the proposed instrument's corpus does not yet exist as a measured object. The one caveat on this NO is that I could not retrieve the full text of the FAccT 2026 paper "Platforms' Research API Data Access: What Users See vs. What Researchers can Retrieve" (ACM DL 403, no open preprint located); its abstract-level framing is a cross-sectional API-versus-public comparison with no Wikipedia dimension, but its methodology section is unverified by me and should be checked before the NO is treated as final. I also did not extract Quack's full text, leaving a small gap in the censorship-measurement retry survey. Separately, and worth stating plainly: I found **no** instrument in any field that publishes refutations of its own readings as a stated practice — the closest analogue is OONI's open-data-plus-open-methodology posture, which invites external challenge rather than issuing self-refutations, so that element of the proposal appears to have no neighbour at all.
