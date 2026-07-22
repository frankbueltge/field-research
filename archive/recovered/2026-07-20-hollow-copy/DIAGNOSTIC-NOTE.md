# Pre-run diagnostic (conductor's hand, 2026-07-20) — disclosed, not the measurement run

Run to settle two questions the Skeptic (C1.1) and the Proposer (control arm) raised *before*
freezing the classifier. Structural-only; no content substance recorded (description **hashes and
lengths** only, per containment). These are design-fixing diagnostics, distinct from the
pre-registered census; disclosed here in full so the classifier's design choices are auditable.

## Q1 (Skeptic C1.1) — is archived Telegram `og:description` post-specific, or channel boilerplate?

For two channels with ≥2 posts in the sample, archived captures gave **distinct** `og:description`
hashes and lengths per post (e.g. one channel: len 113/101/104, hashes 52984f/10734a/ae4860;
another: 363/226/1028). `og:title` is constant per channel (the channel name), as expected.
**Verdict: post-specific.** The interstitial carries the specific cited post's text in
`og:description`. Consequence for the classifier: `content_present` on Telegram (desc ≥ 20) is a
valid content-preservation signal. The Skeptic's proposed post-ID *gate* (C1.2 — require the
numeric message ID in `og:url`/canonical, or `tgme_widget_message` markup) is **NOT adopted as a
hard gate**: the diagnostic shows genuinely post-specific pages carry **neither** (`og:url` is the
channel URL, no `tgme` markup), so the gate would over-reject valid preserved content. The residual
false-positive (a *deleted* post redirecting to the channel bio) is instead bounded by a
**within-channel description-hash-duplication** guard + a reported **distinct-channel count**
(C2.1): a repeated channel bio shows as identical same-channel hashes.

## Q2 (Proposer control arm) — do the same URLs serve content when fetched LIVE today?

Same unauthenticated, no-JS fetch, live (2026-07-20):

- **Live X (4 distinct tweets):** content-bearing and **post-specific** — `og:description` len
  117/235/72/4, **distinct** hashes; no login-wall marker; 80–125 KB pages. (The len-4 case is an
  edge/media-only or restricted tweet.) X serves per-tweet content to bots **today**.
- **Live Telegram (4 posts):** content-bearing, post-specific; hashes **match the archived
  captures** (52984f/10734a/ae4860 recur) — the archive preserved exactly what the source still
  serves.

**This reverses the Proposer's hypothesised control outcome** (that live X would also be hollow →
archive not implicated). Live X is **not** hollow. Therefore the archived X hollowness is **not**
"the platform never served content to a crawler"; it is a **capture-time archive×platform
failure** — at capture time (2023–24) the crawler received X's JS/login app-shell and the archive
faithfully stored the shell. The content is demonstrably servable to a bot (live proof), so the
loss is not an inevitability of the medium; it is what "coverage" conceals.

**Honest limit on the causal claim (kept as a standing caveat):** the live arm proves the content
is bot-servable *in 2026*; it does not prove X served `og:description` to the Wayback crawler
*at capture time* in 2023–24 (X may have changed bot-serving behaviour since). Either way the load-
bearing point stands: the archive's X captures are hollow shells of content that is **not
intrinsically bot-inaccessible**, and "coverage" certifies them as present.

## Design consequences carried into the frozen classifier

1. **X precedence fix (Skeptic C3.1):** tweet-article markup ⇒ `content_present` first,
   before the login-wall rule (a public tweet shown with a login nag is content, not a shell).
2. **Telegram guard:** `content_present` = desc ≥ 20; report distinct-channel count and
   within-channel duplicate descriptions as the deleted-post→bio bound (not a hard post-ID gate).
3. **Two arms:** archived census + live-control sample, identical classifier, per stratum.
4. **Third stratum:** news/org static pages as a positive-control ceiling (Proposer §3).
5. **Containment (Skeptic C4):** results committed **aggregate-only** — no per-item URL, handle,
   or capture-timestamp→bucket join (a per-item timestamp is joinable to the URL via the public
   session-41 CDX census); description hashes used only at runtime for the distinct-fraction and
   never published as raw values; capture-date histograms month-binned. `sample.json` lists the
   citation URLs (already public — from the public report and our own session-41 census) for
   reproducibility; the results carry no URL→outcome mapping.
