# Appendix — every Research-Tools entry in the platform's public changelog

*Session 108, added after `572a6a9`. Gathered because the adversary's brief asked whether other
changelog entries bear on the gap and were ignored. Source:
`https://developers.tiktok.com/doc/changelog` (HTTP 200, 751,085 bytes, fetched 2026-08-10);
62 dated blocks on the page, of which the following mention Research Tools or the Research API.*

```
May 21, 2026 :: Product Research Tools : Updated existing APIs to enrich and return additional parameters: Query Videos, Query User Liked Videos, Query User Pinned Videos, and Query User Reposted Videos now return favorites_count Query Video Comments returns display_name for comments and replies
February 26, 2026 :: Product Research Tools : Updated data pipeline logic to ensure comprehensive coverage of all public video content, including videos not eligible for recommendation to the For You feed.
December 23, 2025 :: Product Research Tools : Added a data access application for vetted researchers. Mini Games : Released integration workflow and APIs for TikTok Mini Games. Website enhancement Organizations : Updated the user interface for organization management on the Developer Portal.
October 18, 2025 :: Product Research Tools : Published a webpage for vetted researchers , explaining the types of data vetted researchers can access.
May 16, 2025 :: Product Research Tools : Launched Batch Compliance APIs that allow you to retrieve the compliance status of user IDs in batches.
April 26, 2025 :: Product Research Tools : Introduced data filtering to the Test Stage of the Virtual Compute Environment, limiting data access to users that have at least 25,000 followers.
April 17, 2025 :: Product Research Tools : Updated existing APIs to enrich and return additional parameters: Query Videos, Query User Liked Videos, Query User Pinned Videos, and Query User Reposted Videos now include the following: video_mention_list, hashtag_info_list, sticker_info_list, video_label, video_tag Query User Info now includes author_profile_URL Query Video Comments now includes display_name
December 9, 2024 :: Product Research API : Launched TikTok Shop related APIs for EU based shops.
November 4, 2024 :: Product Research API : Added hashtag_info , user bio_url , video_mention_list and video_label .
July 09, 2024 :: Product Research API : Launched Playlist Info endpoint for Research API and added additional fields to existing APIs. Learn more about the Playlist Info endpoint .
February 07, 2024 :: Product Research API : Launched five additional APIs that allows querying liked videos, reposted videos, pinned videos and the followers and following lists of a user.
August 10, 2023 :: Product Research API : Expanded Research API to Europe-based non-profit academic institutions. Learn more here .
February 21, 2023 :: Product Research API : Launched Research API to US non-profit academic institutions. Learn more here . Was this document helpful? On this page
February 21, 2023 :: On this page Products Share Kit Login Kit Content Posting API Research API Display API Embed Videos Data Portability API Green Screen Kit Commercial Content API Other platforms TikTok Embeds TikTok for Business Advertise on TikTok TikTok Creative Center TikTok.com Policy Center Company About TikTok Newsroom Contact Careers ByteDance Transparency Center © 2026 TikTok Terms of Service Privacy Policy
TOTAL Research Tools/API entries: 14
```

**What the enumeration shows.** Thirteen entries in three and a half years touch the research interface.
Twelve are launches, endpoint additions, field enrichments, portal and compliance changes. **Exactly one
speaks to coverage or completeness** — the entry of **February 26, 2026** quoted in `RESULT.md` F4.

So the framing in F4 is not a matter of picking one sentence out of many candidates: on the platform's
own changelog it is the only sentence of its kind. What the enumeration does **not** settle is whether
that sentence is a targeted remediation or a routine pipeline note that happens to use the word
"comprehensive" — it names no gap, no report, no advertisements and no account exclusions, and this
practice makes no claim about its intent. Two adjacent entries are worth reading beside it, without
inference: **October 18, 2025**, "Published a webpage for vetted researchers, explaining the types of
data vetted researchers can access", and **December 23, 2025**, "Added a data access application for
vetted researchers" — both in the window between the report and the claim.
