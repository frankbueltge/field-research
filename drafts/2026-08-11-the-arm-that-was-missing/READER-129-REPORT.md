# Independent reader 129-B — the report, read to its last line

*Published unedited. Nothing has been corrected, softened or removed.*

**Severing conditions.** Dispatched 2026-08-21 at ~03:38Z, before this session had formed any
reading. Given **one file and only that file** — `receiver-report-2506.09746v2-extracted.txt`, the
29 KB report this arc has held since 2026-08-11 and, until the ninth gauntlet, had opened only to
search for a single string. No context about this practice, no statement of what answer would be
welcome, an instruction to bring in no outside knowledge, and an explicit instruction that *"the
document does not say"* is a good and expected answer. Told, in those words, that reading the file
completely was the entire point of the task.

**This session re-verified every quotation below directly against the file** before using any of it
(`INCREMENT-19.md` §4). All of them are present. Two of this session's own verification searches
initially returned a false ABSENT, from ligature and markup, and are recorded as this session's
defect in `INCREMENT-19.md` §6.

---

**1. Coverage statement**

I read the entire file, lines 1–4634 (the tool's line count; the file's final content line is 4634, with a trailing blank line 4635 shown by the reader). `wc -l` independently confirmed 4634 lines. This is the complete document, not a partial or keyword-searched read.

**2. A — What the document is**

It is a report titled "TIKTOK'S RESEARCH API: PROBLEMS WITHOUT EXPLANATIONS" (running header, e.g. line 5). It studies the completeness and reliability of TikTok's Research API, which TikTok "augmented... within Europe in July 2023" following the Digital Services Act (lines 87–107). Authorship (lines 21–26): "Authors: Carlos Entrena-Serrano¹, Martin Degeling, Salvatore Romano, Raziye Buse Çetin." Line 26: "The contribution from AI Forensics is funded by core grants from Open Society Foundations, Luminate, and Limelight Foundation. All other content (c) AI Forensics 2025 Email: info@aiforensics.org." Footnote 1 (lines 27–47): the first author is affiliated with the "Centre for Digitalisation, Democracy and Innovation (Brussels School of Governance, Vrije Universiteit Brussel)"; "All other authors are affiliated with AI Forensics."

Its own stated limits (lines 507–582): "The objective of this project is to test the TikTok official API by querying a set of videos we encountered with different methodologies. The report does not draw any legal conclusions from this analysis, and is not intended to make any accusations against the platform, but rather test the API in a real case scenario." Two experiments are run: Experiment 1 (data donation, comparing ~260,000 donated video URLs against API retrieval, lines 1026–3073) and Experiment 2 (scraping the German FYP, lines 3074–3518). Key headline claim (lines 176–213): "the API fails to provide metadata for one in eight videos provided through data donations... without an apparent reason."

**3. B — Dashboard / monitoring instrument (exhaustive)**

- Line 19 (TOC): "Monitoring APIs: a Public Dashboard 15" — section title, listed as page 15.
- Lines 242–256 (Executive Summary): "To monitor the functionality of the API and eventual fixes implemented by TikTok, we publish a dashboard with a daily check of the availability of 10 videos that were not retrievable in the last month. The video list includes very well-known accounts, notably that of Taylor Swift." — states purpose (monitor API function/fixes), cadence (daily), sample size (10 videos), and selection criterion (videos not retrievable "in the last month").
- Line 3520: section header "Monitoring APIs: a Public Dashboard."
- Lines 3521–3579: "TikTok frequently modifies its infrastructure, including its API. These changes have historically resulted in API downtimes, data reporting inaccuracies, or glitches; however, we are not aware of any record of the changes and the issues they addressed on the API." — framing the rationale.
- Lines 3580–3618: "This often leaves the research community in the position of needing to test the tool before it can be used."
- Lines 3620–3654: "We decided to create a public dashboard to ensure that the problems we identified are consistent over time."
- Lines 3656–3701: "We set up a script to regularly check a set of videos that should be available through the Research API but were not."
- Lines 3702–3735 (selection method): "We went through the lists of videos that were not available, ordered by the number of views."
- Lines 3736–3782: "We selected videos with millions of views that matched the categories described above, as well as other videos that were not available, e.g., by creators like Brook Monk (35M followers) or Taylor Swift (32.5M followers)."
- Lines 3784–3829: "We monitored the availability of 10 selected videos over one month and found that the majority of the videos were consistently not available."
- Line 3832 (Figure 8 caption): "Figure 8: Availability of 10 tested videos in the Public Dashboard. You can check the updated data here." — present-tense, implies a live/updating resource.
- Lines 3833–3878: "We developed the dashboard to enable transparency about TikTok's Research API. We intend to keep the dashboard online to also help researchers understand whether problems they are encountering are affecting only their own account." — future intent stated ("intend to keep... online"), stated audience (researchers), stated function (distinguish systemic vs. individual-account problems).
- Lines 3880–3911: "Our records indicate that certain functionalities have been unavailable since a test conducted in December 2024." — a specific reliability/continuity claim about tracked functionality, tied to their own "records."
- Lines 3913–4007: describes plans to meet TikTok's API team, and hope: "We hope to be able to say that all the documentation is updated and complete and that all the data that should be accessible on the official API will actually be available." (future-oriented, not yet achieved).
- Lines 4009–4060 (Conclusion, dashboard-adjacent): "In conclusion, our ongoing monitoring efforts are crucial, and we remain committed to working with the relevant teams to rectify the identified issues. We plan to release timely updates regarding any improvements or fixes that have been implemented." — commits to continuing the monitoring effort and to releasing "timely updates," but is nonspecific about mechanism/cadence beyond what's already described.
- Line 4063: "A dashboard of the videos queried daily is available at: https://playground.tiktok-audit.com/api-na/" — gives the URL, present tense ("is available"), reaffirms "queried daily."

On errors/failures/reliability of their own checking specifically for the dashboard: the document does not report any errors, downtime, or failure of the dashboard itself anywhere. The only reliability caveat tied to the dashboard is the December 2024 "functionalities... unavailable" note above, which is about TikTok's API, not about the dashboard failing to run. Separately (not the dashboard, but relevant to their checking generally), lines 1600–1657 note that during Experiment 1 some 100-item API batches became "corrupted" (their term) — a reliability issue in their querying method, not the dashboard.

Tense: The dashboard is spoken of throughout as something that exists now and is running ("we publish a dashboard," "is available at," Figure 8 "you can check the updated data here"), plus explicit forward intent ("we intend to keep the dashboard online," "we plan to release timely updates"). There is no passage describing the dashboard as merely planned/not-yet-built, nor any passage describing it in the past tense as something that existed then but no longer does.

**4. C — Ordinary user vs. research interface**

The document repeatedly contrasts what is visible/public on the platform with what the Research API (the "research interface") returns:
- Lines 664–677: "some video metadata could not be retrieved from the API, even when it was still publicly accessible on the platform."
- Lines 1454–1480: "The other 62.7% were all publicly available on the platform, but not retrievable through the API."
- Lines 2326–2330 (excluded accounts): "None of their videos could be retrieved although the majority is publicly available."
- Lines 2582–2611 (an ad video): "Although the video (Figure 4) exists on the platform, it has a unique identifier and is publicly accessible, the research API does not return any content for that ID when queried."
- Lines 3499–3518: about @thesun and @barstoolsports — "no video could be retrieved... which we think should be accessible as they are prominent public profiles."

The document does not use the phrase "ordinary user" itself, nor does it describe a specific separate "research interface" distinct from "the Research API" — the contrast it draws throughout is between public/platform-visible availability and API-retrievable availability, using those terms.

**5. D — Effect of a hypothetical January 2026 dashboard outage**

The document commits its authors, in their own words, to:
- "We intend to keep the dashboard online" (lines 3833–3846) — a stated intention that a permanent stoppage would directly contradict.
- "our ongoing monitoring efforts are crucial, and we remain committed to working with the relevant teams to rectify the identified issues. We plan to release timely updates regarding any improvements or fixes that have been implemented." (lines 4009–4060) — commits to continuing monitoring and to releasing updates; a stopped dashboard with no such update would be in tension with this stated plan.
- Figure 8 caption: "You can check the updated data here" (line 3832) — asserts the linked data is (kept) updated; if it had frozen/errored, this claim would no longer hold as written.
- The dashboard's own stated purpose — "to also help researchers understand whether problems they are encountering are affecting only their own account" (lines 3856–3878) — would be undermined if the dashboard itself were stuck showing an error state, since it could no longer reliably distinguish "the researcher's own account problem" from "the dashboard's own malfunction."

The document does not state any specific uptime guarantee, does not describe any monitoring/alerting for the dashboard's own health, and does not anticipate or discuss the possibility of the dashboard itself failing or entering an error state. It gives no maintenance commitment beyond the general intentions quoted above, so a reader cannot find in the text any claim that is either confirmed or literally falsified by an error state — only the stated intentions above that such an outage would sit in tension with.

**6. E — Other notable content, especially last third / credits / footnotes**

- Footnote on Canada exclusion inconsistency (lines 1097–1131): "These limitations are listed in the https://developers.tiktok.com/doc/research-api-codebook in the codebook. Confusingly the 'Getting Started' page lists Canadian Videos as an example... (both accessed 20.05.2025)."
- Footnote 2 (lines 1134–1135): FAQ link "(accessed 20.05.2025)."
- Testing was interrupted (lines 1841–1885): "We interrupted the test on May 16, 2025, to begin writing this report, but we are continuing to recheck the posts left."
- TikTok contact (lines 1896–1978): "We contacted the TikTok API team and provided examples of content that could not be retrieved. Although we shared our report in advance and agreed to schedule a meeting to discuss the findings, a public explanation of the inconsistencies is still missing."
- Conclusion (lines 4068–4630) argues the API "can not serve as a source for research that requires up-to-date, complete, and consistent information" (4069–4086); quantifies unresolved gaps as "(1) videos of at least 1% of creators, (2) some TikTok company videos, and (3) almost 10,000 advertisements are not accessible through the API" (4180–4226); states "If TikTok has good reasons to exclude specific videos from the API escapes our assessment, since no justification is transparently disclosed in error messages or otherwise" (4228–4278).
- On scraping as policy recommendation (lines 4421–4537): "researchers should be allowed to use data scraping to access relevant metadata. Data scraping is a technique widely used in the industry, but discouraged in public interest research as it could sometimes be interpreted as a violation of platforms' terms of service. We believe it should be recognised for what it is: a vital tool for transparency."
- Closing line (lines 4611–4630): "Without the ability to independently verify the accuracy of API tools, the promise of data access risks remaining an illusion."
- A likely OCR/formatting artifact worth flagging: line 1822 reads "18961" where context ("we confirmed again that 18961 IDs are still not retrievable from the API") suggests a number (possibly "1,896" or similar) rendered without a separator — the raw text is ambiguous.
- Also of note, not previously highlighted: TikTok CEO Shou Zi Chew's video is described (lines 2131–2184) as posted "in response to the introduction of the TikTok ban bill in the US Congress with more than 30 million views," and is one of 32 "TikTok authorized videos" found unretrievable in the 70k dataset (lines 2187–2192).

**7. What the document does not say**

- It never states that the dashboard itself has failed, gone offline, stopped updating, or shown an error state at any point — no such incident is described or anticipated.
- It gives no specific uptime/maintenance schedule or health-monitoring mechanism for the dashboard beyond general stated intent to "keep the dashboard online."
- It does not use the term "ordinary user" verbatim, nor does it name a distinct "research interface" as a separate product from "the Research API" — the contrast it draws is consistently platform-public-availability vs. API-retrievability.
- It gives no publication date for the report itself (only that testing was interrupted May 16, 2025, to begin writing, and access dates of 20.05.2025 for API docs).
- It does not report the outcome of the planned meeting/call with TikTok's API team — only that one was agreed to and hoped for.
- It does not explain why the API's 1,000-daily-call limit or 48/72-hour delay exists, beyond calling the reasons "unclear."
