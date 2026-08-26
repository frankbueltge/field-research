# Fan-out 2 — the receiver and the regulatory ground (K-C), published unedited

**Session 136, 2026-08-26.** The second of two independent search fan-outs convened for
`PREREGISTRATION-136.md`. A fan-out is not a role and has **no voice in any verdict**. Its brief had
two halves: find real, named, reachable parties with a *published* interest in whether Wikipedia's
external citations are still retrievable; and establish whether any running public instrument already
tests a video platform's public-content coverage claims from outside, credential-free.

**It is reproduced below exactly as returned, including its long list of what it could not reach** —
EUR-Lex, the ACM Digital Library, the Internet Archive's own statistics endpoint, the Wayback
Machine, and a Wikimedia dashboard behind staff authentication. Two of its results are load-bearing
for `CONCEPT.md` and are carried there rather than left here: the maintenance bot's own documented
liveness test, and the European Commission's preliminary findings of October 2025.

---

## SEARCH FAN-OUT REPORT

Method: web search plus direct retrieval. Every URL below returned HTTP 200 to me unless flagged. Where I could not reach something, I say so. I have no view on any verdict.

---

# HALF 1 — WHO HAS A PUBLISHED INTEREST IN THE HEALTH OF WIKIPEDIA'S EXTERNAL CITATIONS?

### 1. InternetArchiveBot (Internet Archive + Wikimedia community) — STRONGEST
- **URL:** https://meta.wikimedia.org/wiki/InternetArchiveBot · FAQ: https://meta.wikimedia.org/wiki/InternetArchiveBot/FAQ · live management interface: https://iabot.wmcloud.org/
- **What:** A bot operated as a service of the Internet Archive in partnership with the Wikimedia community; maintainers named on the page as Cyberpower678, Harej, GreenC. Won the 2019 Coolest Tool Award (Impact).
- **Published statement:** the bot "identifies and replaces broken external links" and "makes other enhancements to references as well, including filling out bare reference templates and adding links to resources where appropriate." It "monitors every Wikimedia wiki for new outgoing links" across 300+ wikis.
- **Detection method (from FAQ, verbatim):** a link is treated as dead when "the site failed to validate as alive 3 times in a row, during 3 separately spaced out checks, or the site has blacklisted the bot from further access."
- **Short-form video?** **NO.** Neither the main page nor the FAQ mentions YouTube, video, or social media, nor any handling of soft-404s (a page that returns HTTP 200 while displaying "Video unavailable"). Its stated liveness test is exactly the test that a removed video's page would pass.
- **Gap:** the bot's own statistics page (`iabot.wmcloud.org/index.php?page=performancemetrics`) returned **HTTP 401 Unauthorized** to me. `meta.wikimedia.org/wiki/InternetArchiveBot/Statistics` returns **404**. There is no public IABot statistics page I could reach.

### 2. Internet Archive (as an institution)
- **URL (2018 written baseline):** https://blog.archive.org/2018/10/01/more-than-9-million-broken-links-on-wikipedia-are-now-rescued/
- **Quote (2018):** "we have successfully used IABot to edit and 'fix' the URLs of nearly 6 million external references that would have otherwise returned a 404… Now more than 9 million URLs, on 22 Wikipedia sites, point to archived resources."
- **Current figure — with a caveat:** Mark Graham (director, Wayback Machine) stated at the Internet Archive's 1-trillion-pages event that "we have identified and fixed more than 28 million broken links from Wikipedia articles… we've added more than 4.2 million links pointing to books and papers available from archive.org." This is a **spoken statement in a recorded event**, transcript at https://www.youtube.com/watch?v=EfKPJJQvIn0. I fetched https://blog.archive.org/trillion/ (HTTP 200) and it does **not** contain the 28-million figure. **I could not find a written Internet Archive publication stating 28 million.** Treat the number as unconfirmed in writing.
- **Short-form video?** **NO** — links in general only.

### 3. English Wikipedia's dead-link maintenance community
- **Live backlog (I retrieved this today):** https://en.wikipedia.org/wiki/Category:All_articles_with_dead_external_links — page text verbatim: *"The following 200 pages are in this category, out of approximately **364,370** total."*
- **WikiProject External links:** https://en.wikipedia.org/wiki/Wikipedia:WikiProject_External_links — active (last edit 7 July 2026). Stated goals include to "recover or remove dead external links." **Does not mention video or social media links.**
- **WP:Link rot** (how-to essay, not policy): https://en.wikipedia.org/wiki/Wikipedia:Link_rot — "URLs have a median lifespan of about one year"; beyond-404 errors "might account for 40% or more of all inoperable links." **Contains no mention of video, YouTube, or social media.**
- **WP:Archiving a source:** https://en.wikipedia.org/wiki/Wikipedia:Archiving_a_source — the *only* video-relevant line: Ghostarchive.org "uses the Webrecorder technology and is thus able to save dynamic content such as YouTube videos, JavaScript etc."
- **WP:List of web archives on Wikipedia:** https://en.wikipedia.org/wiki/Wikipedia:List_of_web_archives_on_Wikipedia — Ghost Archive is listed as the one service archiving YouTube videos (`ghostarchive.org/varchive/[YouTube_video_ID]`); the Wayback Machine and the rest are described as page-snapshot only. Wayback is stated as ~80% of all archive uses on en-wiki (data compiled by User:GreenC, dated **March 2017** — old).
- **Ghostarchive** itself: https://ghostarchive.org/ (HTTP 200).
- **Short-form video?** **Only obliquely** — via Ghostarchive's capability, not via any stated programme.

### 4. Wikimedia Foundation Research team — published agenda exists, but the topic is *reliability*, not *retrievability*
- **Programme page:** https://research.wikimedia.org/knowledge-integrity.html — the Knowledge Integrity programme aims to "extend the verifiability of content and increase resilience to misinformation," to "represent, curate, and understand information provenance," and works on "reference need" (sentences missing a citation) and "reference risk" (non-authoritative sources).
- **Team overview:** https://research.wikimedia.org/ — "Enhancing the ability of our communities to improve verifiability and detect policy violations through new technologies."
- **Current output — a hard gap.** I downloaded the most recent report, **Research Report Nº 13, published 18 December 2025** (https://research.wikimedia.org/report_13.html), and text-searched the full page. It contains **zero** occurrences of "citation," "reference," "external link," "link rot," "archive," or "verifiability." The only relevant hit is one line about attending a workshop to share "our research to assess source **reliability** on Wikipedia."
- **Knowledge Integrity Risk Observatory:** https://meta.wikimedia.org/wiki/Research:Wikipedia_Knowledge_Integrity_Risk_Observatory — led by Pablo Aragón with Diego Sáez-Trumper; **marked completed as of July 2024**. It defines a source category — "Usage and reliability of sources in articles. This category is directly inspired by one [of] the three principal core content policies of Wikipedia (WP:V) which states that readers and editors must be able to check that information comes from a reliable source" — but the dashboard shows that section as **"TBD"**, i.e. no metric was ever implemented. The v1 dashboard requires `wmf`/`nda` LDAP; **not publicly reachable.**
- **Short-form video?** **NO.** WMF Research's published agenda covers source *reliability* and *presence* of citations. I found **no** WMF Research work on whether cited sources remain retrievable, and none on video.

### 5. WikiSignals.org — current (August 2026) but about reliability
- **URL:** https://diff.wikimedia.org/2026/08/07/wikisignals-org-helping-editors-evaluate-reference-reliability/ (published **7 August 2026**, by WebRunner95 and Hearvox).
- "a searchable database of website credibility indicators," built at WikiCredCon 2025, to "help editors reliably evaluate external references."
- **Short-form video?** **NO** — and it does not address whether sources are still live at all. News domains only.

### 6. The Wikipedia Library (WMF)
- **URL:** https://wikimediafoundation.org/the-wikipedia-library/
- Stated as "supporting verifiability by helping Wikipedia editors access reliable sources." Partnerships with 100+ subscription databases; access gated at 500+ edits / 6 months.
- **Short-form video?** **NO.** It is about *acquiring* paywalled sources, not about retrievability of already-cited ones. Not a plausible receiver for this measurement.

### 7. Academic groups with standing programmes
- **University of Michigan (Harsha V. Madhyastha's group)** — "Characterizing 'permanently dead' links on Wikipedia," Anish Nyayachavadi, Jingyuan Zhu, Harsha V. Madhyastha, ACM IMC '22, Nice, 25–27 Oct 2022. DOI page: https://dl.acm.org/doi/10.1145/3517745.3561451 (ACM returned **403** to my automated fetch; the record is confirmed via the IMC 2022 accepted-papers list https://conferences.sigcomm.org/imc/2022/accepted/). Findings: many "permanently dead" links work today; where they don't, "it is rarely the case that no archived copies exist"; current policy for accepting archived copies is "too conservative"; "many URLs are archived for the first time only after they no longer work." Follow-on: "Reviving Dead Links on the Web with Fable," IMC 2023, https://dl.acm.org/doi/10.1145/3618257.3624832. **Links in general; no video.**
- **EPFL dlab (Robert West)** — "Quantifying Engagement with Citations on Wikipedia," Piccardi, Redi, Colavizza, West, WWW '20: https://arxiv.org/abs/2001.08614 and https://dlab.epfl.ch/people/west/pub/Piccardi-Redi-Colavizza-West_WWW-20.pdf. Finding: ~1 in 300 pageviews yields a reference click (0.29% overall). **Engagement, not retrievability; no video.**
- **Pew Research Center** — "When Online Content Disappears," **17 May 2024**: https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/. From 50,000 randomly sampled English Wikipedia pages (spring 2023 snapshot, ~1M reference links): "**11% of all references linked on Wikipedia are no longer accessible**" and "**54% of Wikipedia pages contain at least one link in their 'References' section that points to a page that no longer exists**." **Explicitly does not break out YouTube, video, or social-media links.**

### 8. Wikipedia's positions on video/social sources — reliability only
- **WP:RSPYT (YouTube):** https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources/all/YouTube — status "generally unreliable"; `last = 2026, inprogress=yes` (an active 2026 discussion). Text: "Most videos on YouTube are anonymous, self-published, and unverifiable, and should not be used as a reference." Note: "unverifiable" here means *unvetted*, not *unretrievable*.
- **WP:RSPTIKTOK:** https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources/all/TikTok — "generally unreliable," recency 2025.
- **WP:Video links** (explanatory essay, not policy): https://en.wikipedia.org/wiki/Wikipedia:Video_links — I read it; it addresses copyright and reliability and **says nothing about video links dying**.
- **WikiProject TikTok:** https://en.wikipedia.org/wiki/Wikipedia:WikiProject_TikTok — self-tagged **semi-active**; scope is article coverage of TikTok, not citation health.

### GAP — the specific thing you asked me to find, which I could NOT find
I searched Wikimedia Phabricator (`dead link archive external`, `youtube video unavailable citation`, `tiktok`) and English Wikipedia's project/talk namespaces via the MediaWiki search API (`soft 404 YouTube`, `insource:"video unavailable"`, `InternetArchiveBot YouTube video unavailable`, `citation video no longer available`).

- Phabricator has a real cluster on link rot: **T120433** "Migrate dead external links to archives," **T120850**, **T125575** "Find bots that find and/or migrate dead external links to archives," **T153354** "Automatic archive for new external links," **T177676**, **T125268** "Help to investigate existing dead link features."
- Phabricator's TikTok tasks are entirely about **traffic referrals and AR filters** (T340677 "TikTok referral data gaps," T324230, T305620, and a `[SFV]` short-form-video product series such as T409496) — **none about TikTok/video links as citations.**
- **I found no Phabricator task, no RfC, and no village-pump thread specifically about social-media or short-form-video citations being unretrievable.** I am reporting this as a gap, not as proof of absence; but it is a gap I looked for deliberately in four different ways.

### Scale, measured live by me (reproducible, not a published source)
English Wikipedia mainspace, via `https://en.wikipedia.org/w/api.php?action=query&list=search&srnamespace=0&srinfo=totalhits&srsearch=insource:"…"`, retrieved 26 Aug 2026:
- `youtube.com/watch` — **243,968** articles
- `youtube.com/shorts` — **1,302** articles
- `instagram.com/reel` — **2,300** articles
- `tiktok.com` — **~1,500** articles (CirrusSearch estimate; the round number suggests a capped approximation)
- `cite AV media` template — **93,815** articles

---

# HALF 2 — TESTABILITY OF PLATFORM PUBLIC-DATA COVERAGE CLAIMS FROM OUTSIDE

## 1. DSA Article 40 and the Delegated Act — status as of 2026

**Article 40 DSA (Regulation (EU) 2022/2065).** Two distinct regimes, and the distinction is the whole story here:
- **Art. 40(4)** — *non-public* data, for **vetted** researchers, on a reasoned request from the Digital Services Coordinator of establishment or the Commission.
- **Art. 40(12)**, verbatim: *"Providers of very large online platforms or of very large online search engines shall give access without undue delay to data, including, where technically possible, to real-time data, **provided that the data is publicly accessible in their online interface** by researchers, including those affiliated to not for profit bodies, organisations and associations, who comply with the conditions set out in paragraph 8, points (b), (c), (d) and (e)…"*
  Source used: https://www.eu-digital-services-act.com/Digital_Services_Act_Article_40.html (a text mirror — EUR-Lex bot-blocked my direct fetch, see below).

**Delegated Act.** **Commission Delegated Regulation (EU) 2025/2050 of 1 July 2025**, supplementing Regulation (EU) 2022/2065, laying down technical conditions and procedures for VLOPs/VLOSEs to share data with **vetted** researchers.
- Commission announcement, **2 July 2025**: https://digital-strategy.ec.europa.eu/en/news/commission-adopts-delegated-act-data-access-under-digital-services-act — quote: *"Today's delegated act complements DSA rules that oblige VLOPs and VLOSEs to grant access to researchers to publicly available data on their platforms."*
- Library page with the regulation number: https://digital-strategy.ec.europa.eu/en/library/delegated-act-data-access-under-digital-services-act-dsa
- EUR-Lex ELI: https://eur-lex.europa.eu/eli/reg_del/2025/2050/oj/eng and CELEX HTML: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A32025R2050 — **both returned HTTP 202 (bot challenge) to my automated fetch**; they resolve in a browser and are confirmed present in search indexes. I did not read the legal text directly.
- **Entry into force: 29 October 2025.** Applications open via the **DSA Data Access Portal**, https://data-access.dsa.ec.europa.eu/ (HTTP 200, live).

**The critical scope point.** The Commission's own official FAQ — European Centre for Algorithmic Transparency, **3 July 2025**, https://algorithmic-transparency.ec.europa.eu/news/faqs-dsa-data-access-researchers-2025-07-03_en — states: *"The delegated act specifies the procedures and technical conditions enabling the provision of access to data for vetted researchers **pursuant to Article 40(4)** of the DSA."* **Public-data access under Art. 40(12) is not covered by the delegated act.** There is, as of today, an obligation on platforms to give access to publicly accessible data, and **no delegated procedure specifying how it must be delivered or verified.**

## 2. Published third-party audits testing whether a video platform's research API returns the public content it claims to cover

**(a) AI Forensics — "TikTok's Research API: Problems Without Explanations"**
- Authors: Carlos Entrena-Serrano, Martin Degeling, Salvatore Romano, Raziye Buse Çetin. arXiv v1 **11 June 2025**, v2 12 June 2025: https://arxiv.org/abs/2506.09746 · project page: https://aiforensics.org/work/tk-api (the AI Forensics page carries a later date I could not independently confirm as the publication date) · also listed by the Brussels School of Governance: https://www.brussels-school.be/research/publications/tiktoks-research-api-problems-without-explanations
- **Abstract, verbatim:** *"Our experiment reveals that the API fails to provide metadata for one in eight videos provided through data donations, including official TikTok videos, advertisements, and content from specific accounts, without an apparent reason. The API data is incomplete, making it unreliable when working with data donations… To monitor the functionality of the API and eventual fixes implemented by TikTok, we publish a dashboard with a daily check of the availability of 10 videos that were not retrievable in the last month. The video list includes very well-known accounts, notably that of Taylor Swift."*
- Method includes verifying by web scraping that the missing videos **are publicly available**. Breakdown reported: for 69.3% of tested creators all 10 videos were available; for 1.5% none were (including @thesun and @barstoolsports); for 29.2% only a subset.
- **This is the closest existing precedent to a retrievability measurement of short-form video from outside.**

**(b) University of St. Gallen — "Auditing Meta and TikTok Research API Data Access under Article 40(12) of the Digital Services Act"**
- Luka Bekavac and Simon Mayer, University of St. Gallen, **18 January 2026**: https://arxiv.org/abs/2601.12390 · HTML: https://arxiv.org/html/2601.12390
- Method: sockpuppet accounts collected the TikTok "For You" feed (Jul–Nov 2024, US election) and Instagram "Explore" (Jan–Feb 2025, German election) — 4,000+ posts, 200+ hours — then queried each platform's Research API for the same content.
- Findings: on TikTok researchers could reach ~**75%** of the posts users saw but only ~**17%** of transmitted metadata parameters; on Instagram ~**50%** of user-visible posts and ~**42%** of parameters (one post transmits 236 parameters to a browser vs. 100 via the research API). Three loss mechanisms named: scope narrowing, metadata stripping, operational restrictions. Also reports **17.7%–23.3%** of TikTok posts no longer accessible within weeks.
- **This directly compares research-API results against independently observed public content — exactly the design in your question.**

**(c) Democracy Reporting International + AI Forensics — "Unpacking TikTok's Data Access Illusion"**
- Daniela Alvarado Rincón, Ognjan Denkovski, Salvatore Romano, Martin Degeling; **12 June 2025**: https://www.techpolicy.press/unpacking-tiktoks-data-access-illusion/
- Verbatim: *"TikTok's research API does not allow access to information on videos that have been posted by TikTok itself, videos that are posted as ads, as well as videos from an estimated 1.5% of accounts."* On the Virtual Compute Environment: *"During its active engagement with the VCE (from January to February), DRI never received a single results file, with queries stuck in limbo for months."*

**(d) Regulator — European Commission preliminary findings, 24 October 2025 (IP/25/2503)**
- https://ec.europa.eu/commission/presscorner/detail/en/ip_25_2503 · full PDF I extracted: https://ec.europa.eu/commission/presscorner/api/files/document/print/en/ip_25_2503/IP_25_2503_EN.pdf
- **Verbatim:** *"Today, the European Commission preliminarily found both TikTok and Meta in breach of their obligation to grant researchers adequate access to public data under the Digital Services Act (DSA). … The Commission's preliminary findings show that Facebook, Instagram and TikTok may have put in place burdensome procedures and tools for researchers to request access to public data. **This often leaves them with partial or unreliable data**, impacting their ability to conduct research, such as whether users, including minors, are exposed to illegal or harmful content."*
- Virkkunen quote, verbatim: *"With today's actions, we have now issued preliminary findings on researchers' access to data to four platforms."* (X received its preliminary findings 12 July 2024, https://ec.europa.eu/commission/presscorner/detail/en/ip_24_3761, including for failing to give researchers access to public data and for prohibiting independent scraping in its terms of service; the Commission fined X €120 million on 5 December 2025.)
- Exposure: up to **6% of total worldwide annual turnover**.

## 3. Organisations maintaining a monitor/dashboard of research-API completeness or outages

**(a) AI Forensics — TikTok Research API Availability Dashboard: EXISTS BUT STALE.**
- https://playground.tiktok-audit.com/api-na/ — HTTP 200.
- I downloaded the HTML and grepped it. The page's own footer reads, verbatim: **"generated on: 2026-01-14 21:53:41"**. That is the only timestamp in the file. It is **~7½ months stale** as of 26 August 2026.
- Current state of the 11 tracked videos: **"0 Available Videos," "0 Unavailable Videos," "11 Videos with Errors"** — with the page's own caveat "Error are problems on our end, not TikTok."
- The dashboard root https://playground.tiktok-audit.com/ returns **403 Forbidden** (nginx).
- **Verdict: reachable but not running.** It also requires the TikTok Research API, i.e. it is credentialed, not credential-free.

**(b) DSA 40 Data Access Collaboratory (Weizenbaum-Institut e.V., Berlin) — RUNNING, but about the application process, not content coverage.**
- Home: https://dsa40collaboratory.eu/ — PIs Ulrike Klinger (University of Amsterdam) and Jakob Ohme (Weizenbaum Institute); coordinator LK Seiling; funded by Stiftung Mercator.
- **Issue Tracker:** https://dsa40collaboratory.eu/issue-tracker/ — "Experiencing issues with data access? Check here if other researchers have already flagged the issue or submit one yourself." Only **two** past issues listed: Meta (reported Dec 2024) — "No applications could be submitted for Meta's data access mechanisms from December 2024 - April 2025"; and TikTok (reported Jan 2025) — **"TikTok Researcher API returned no data for 13-20 January 2025."**
- **Tracker Insights:** https://dsa40collaboratory.eu/tracker-insights/ — last updated **16 March 2026**: "46 complete applications have been registered," "34 have been decided by the platforms," "20 have been accepted and 14 rejected"; TikTok averaging 32.58 days to decide, X.com 69.17 days.
- **This is the only live, currently-maintained public instrument I found in this space — and it measures application outcomes and outages, not whether the API returns the public content it claims to cover.**

**(c) Coalition for Independent Technology Research + GWU IDDP — "DSA Data Access Audit"**
- https://independenttechresearch.org/introducing-the-dsa-data-access-audit/ (**14 March 2024**) — purpose: "auditing the state of researcher access to data," providing "independent, objective information to platforms, policymakers and the public about how well the data access tools being released by platforms are serving the research community." Related IDDP page: https://iddp.gwu.edu/platform-transparency-tools-brussels-effect
- **Gap: I found no public dashboard or published audit output from this project.** The page only solicits researcher survey participation. I could not establish that it produces a running monitor.

## 4. Published researcher statements that a platform's research API omits publicly visible content

- **AI Forensics (2b/2a above)** — the strongest and most explicit; missing videos verified as publicly available by scraping.
- **Bekavac & Mayer, University of St. Gallen (2026)** — API returns ~75% of what users actually saw on TikTok.
- **DRI/AI Forensics (2025)** — TikTok's own videos, ads, and ~1.5% of accounts excluded.
- **Cybersafety Research Center (formerly Cybersecurity for Democracy)** — Bruno Coelho, Lexie Barthelemess, Dominique Geissler, **15 November 2024**: https://cybersafetyresearch.org/issues-with-the-tiktok-research-api (the old `cybersecurityfordemocracy.org` path 301-redirects to the new domain root; I retrieved the article body via full-text extraction). Verbatim: *"A major issue with the TikTok Research API is the frequency with which it returns internal server errors when attempting to retrieve historical data… To our knowledge, these dates are random and can range from a few days to months for which no videos will be returned from the API… even though no data was returned this still decreases the daily quota."* And: *"Despite TikTok's documentation explicitly requesting for researchers to notify support when a 500 Internal Service Error has been returned, our reports have gone unanswered."*
- **TechPolicy.Press, on the 2024 European elections:** https://www.techpolicy.press/-researcher-data-access-under-the-dsa-lessons-from-tiktoks-api-issues-during-the-2024-european-elections/

---

# (A) STRONGEST CANDIDATES FOR A REAL, REACHABLE, NAMED RECEIVER

**1. InternetArchiveBot / the Internet Archive.** The only party that already operates a running, wiki-wide instrument on exactly this quantity, and the only one whose stated liveness test would visibly fail on a removed video. Published evidence of interest: *"identifies and replaces broken external links"* and "monitors every Wikimedia wiki for new outgoing links and actively makes fixes" (https://meta.wikimedia.org/wiki/InternetArchiveBot); its dead-link criterion is *"the site failed to validate as alive 3 times in a row, during 3 separately spaced out checks"* (https://meta.wikimedia.org/wiki/InternetArchiveBot/FAQ). It is reachable via the Meta talk page, the IRC/Telegram channels listed there, and the named maintainers. **Its published interest covers links in general and is silent on video — which is what makes it a receiver rather than a duplicate.**

**2. The English Wikipedia dead-link maintenance community — WikiProject External links.** Active (last edit 7 July 2026), with a stated goal to *"recover or remove dead external links"* (https://en.wikipedia.org/wiki/Wikipedia:WikiProject_External_links), and a live, publicly countable backlog of *"approximately 364,370"* articles (https://en.wikipedia.org/wiki/Category:All_articles_with_dead_external_links). It has an existing tooling/archiving apparatus (https://en.wikipedia.org/wiki/Wikipedia:Archiving_a_source, https://en.wikipedia.org/wiki/Wikipedia:List_of_web_archives_on_Wikipedia) in which Ghostarchive is already named as the sole YouTube-capable archive — a concrete hook for a video-specific finding.

**3. AI Forensics (with Democracy Reporting International).** Not a Wikipedia body, but the only named organisation that has already published a measurement of *exactly this quantity* on a short-form video platform and built an instrument for it. Published evidence: *"the API fails to provide metadata for one in eight videos… including official TikTok videos, advertisements, and content from specific accounts, without an apparent reason"* and *"we publish a dashboard with a daily check of the availability of 10 videos that were not retrievable in the last month"* (https://arxiv.org/abs/2506.09746). Their dashboard has been dead since 14 January 2026 — which makes them a plausible receiver for a working replacement rather than a competitor.

*Honourable mention, weaker:* Pew Research Center has published the closest thing to a baseline (11% of Wikipedia references unreachable, 54% of pages affected, https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/) and explicitly did **not** break out video — but Pew is a publisher, not an ongoing receiver.

*Explicitly weak, despite being the obvious guess:* **the Wikimedia Foundation Research team.** Its programme page invokes verifiability and provenance (https://research.wikimedia.org/knowledge-integrity.html), but its most recent published output, Research Report Nº 13 of 18 December 2025 (https://research.wikimedia.org/report_13.html), contains no occurrence of "citation," "reference," "external link," "link rot," "archive," or "verifiability"; and its Knowledge Integrity Risk Observatory left the sources indicator as "TBD" and was closed in July 2024. **Its published interest in external-source retrievability is not currently demonstrable.**

# (B) IS THERE ALREADY A RUNNING PUBLIC INSTRUMENT THAT TESTS A VERY LARGE VIDEO PLATFORM'S PUBLIC-CONTENT COVERAGE CLAIMS FROM OUTSIDE, CREDENTIAL-FREE?

## **NO.**

Evidence, in order of how directly it forecloses a yes:

1. **The one purpose-built dashboard exists and is dead.** AI Forensics' TikTok Research API Availability Dashboard (https://playground.tiktok-audit.com/api-na/) serves HTTP 200 but its own generated stamp reads **"generated on: 2026-01-14 21:53:41"** — no update in ~7½ months — and all 11 tracked videos currently report **"Videos with Errors"**, which the page itself attributes to "problems on our end, not TikTok." Its root path returns 403. It is a frozen artefact, not a running instrument.

2. **Even when it ran, it was not credential-free.** It queried TikTok's Research API, which requires an approved researcher account. Both published audits share this dependency: AI Forensics (https://arxiv.org/abs/2506.09746) and Bekavac & Mayer (https://arxiv.org/abs/2601.12390) both operate *inside* the credentialed API and compare it against separately-gathered observations — and Bekavac & Mayer's baseline required **sockpuppet accounts**, i.e. also credentialed.

3. **The only currently-maintained public tracker measures something else.** The DSA 40 Collaboratory Issue Tracker and Tracker Insights (https://dsa40collaboratory.eu/issue-tracker/, https://dsa40collaboratory.eu/tracker-insights/, last updated 16 March 2026) track *application outcomes and outages* — 46 applications, 20 accepted, 14 rejected; two logged incidents total, one of which is "TikTok Researcher API returned no data for 13-20 January 2025." It does not test content coverage.

4. **The published audits are one-shot studies, not instruments.** AI Forensics (June 2025), DRI/AI Forensics (June 2025), Cybersafety Research Center (November 2024), Bekavac & Mayer (January 2026) — four discrete publications, none of which reports a continuously running public measurement.

5. **The regulator found the gap but did not fill it with an instrument.** The Commission's 24 October 2025 preliminary findings (IP/25/2503) state that researchers are "often… le[ft] with partial or unreliable data" on **public** data access — an enforcement finding, not a monitor. And per the Commission's own FAQ (https://algorithmic-transparency.ec.europa.eu/news/faqs-dsa-data-access-researchers-2025-07-03_en), Delegated Regulation (EU) 2025/2050 specifies procedures for **Article 40(4)** only; **Article 40(12) public-data access has an obligation but no delegated procedure and no verification mechanism.**

## What I could not reach
- **EUR-Lex** (`eli/reg_del/2025/2050/oj/eng`, `CELEX:32025R2050`, `CELEX:32022R2065`) — HTTP 202 bot challenge on every attempt. I did not read the Delegated Regulation or the DSA legal text at source; Article 40(4)/(12) is quoted from a text mirror, and the regulation number is from the Commission's own library page.
- **web.archive.org** — blocked for me at both the fetch tool and the network layer (connection reset). I could not retrieve archived snapshots.
- **ACM Digital Library** — 403 to automated fetch; the IMC 2022 paper is confirmed via the conference's accepted-papers list, not the DL record itself.
- **IABot performance metrics** (`iabot.wmcloud.org/index.php?page=performancemetrics`) — HTTP 401. No public IABot statistics page exists that I could find.
- **WMF Knowledge Integrity Risk Observatory v1 dashboard** — behind `wmf`/`nda` LDAP.
- **Wikimania 2026 talk "Reference Risk: A Research-Based Approach to Source Reliability in Wikipedia"** (https://wikimedia.eventyay.com/wm/wikimania2026/talk/NSXGJU/) — login-gated; I could not retrieve the abstract or speakers.
- **The Internet Archive's "28 million Wikipedia links fixed" figure** — I found it only in the spoken transcript of the 22 October 2025 event video, not in any written Internet Archive publication.
- **A Phabricator task, RfC, or village-pump thread specifically about short-form-video or social-media citations being unretrievable** — searched four ways; **none found.**
