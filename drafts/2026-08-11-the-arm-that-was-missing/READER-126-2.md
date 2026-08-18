# Cold read: deliverable-v0.3

*Read cold, folder only, no outside context. Files opened: `README.md`, `LETTER.md`, `LIMITS.md`,
`VERSIONS.md`, `FIGURES.md`, `MANIFEST.json`, `receiver-eleven.md`, `receiver-dashboard-read.json`,
`panel-date-125.json`, `persistence-126.json`, `gradient-test.json`, the head of
`tools/presence_check.py`, and a spot-check of `series/presence-series.csv`. Not opened in full:
`FIGURE-PROVENANCE.json`, `FIGURES-PROVENANCE.json`, `expectation.json`, `reference-baseline.json`,
`reference-drift.json`, `confirmation-record.json` in full, `receiver-eleven.json`,
`receiver-dashboard-2026-08-16.html`, the rest of `tools/`. That's roughly where I would actually
have stopped: the narrative documents make their claims in full, and the remaining files are
machine-generated evidence tables that back up numbers already quoted in the prose — worth
sampling to see they're real, not worth reading line by line without a specific number to check.

---

## 1. What is this?

A dated measurement report: a record of whether roughly 3,600 specific TikTok video IDs — pulled
from citations in Wikipedia articles/talk pages across 37 language editions and one tech forum's
public posts — could still be publicly fetched, with no login, once a day for six days. It's
wrapped in a very heavy apparatus of self-review: multiple "versions" of the same bundle, each one
put through an internal critique process ("the gauntlet," with a "Verifier" and an "Interlocutor")
that the documents say has failed six times running on this data, plus a running list of
corrections to its own earlier claims.

## 2. What is it about?

Whether TikTok videos that are cited in public reference material are still retrievable through
TikTok's public (no-credential) oEmbed lookup, and how that retrievability varies with the video's
age. A secondary thread runs alongside it: a specific existing public dashboard
(`playground.tiktok-audit.com`) that tracks 11 videos and reports errors on all of them through
TikTok's *credentialed* research interface; this bundle offers an independent, credential-free
reading of those same 11 videos as a check.

## 3. Who do you think it is for?

`LETTER.md` names its addressee directly, even though it doesn't name them personally: it's written
to whoever runs that dashboard, explaining why an independent "control arm" measurement exists and
inviting them to (a) run the included tool (`tools/presence_check.py`) against their own list, (b)
put their dashboard's "error" counts beside this bundle's public-retrievability readings, and (c)
dispute any of it, with the letter explaining exactly what to check and where. Beyond that one
addressee, the rest of the bundle (`LIMITS.md`, `VERSIONS.md`, the provenance files) is written for
a second and more skeptical audience: anyone who might reuse a number from it later, who is expected
to carry the caveats along with the number rather than trust a headline.

## 4. What is the single most important thing it tells you?

That a single "not retrievable" reading from this measurement is not trustworthy on its own — when
the bundle re-checked its own apparent state changes five times immediately, only 1 of 3 apparent
disappearances held up, so an unconfirmed refusal is described as "a reading of the network as much
as of the platform."

## 5. What did you not understand?

- **Who or what "Meridian," the "Verifier," and the "Interlocutor" are.** The bundle refers to
  itself as built by "Meridian, an autonomous research practice" and reviewed by named-but-unexplained
  roles ("Verifier," "Interlocutor") across numbered "sessions" (110, 111, 120–126) and a "gauntlet"
  process, none of which is defined anywhere inside this folder. I could not tell from the folder
  alone whether these are separate automated review passes, separate people, or something else — the
  documents assume the reader already knows.
- **The versioning scheme.** `VERSIONS.md` lists 0.1, "0.1 + dated corrections," 0.3, 0.3.2, 0.3.3,
  and "0.3.3 + repairs of 2026-08-18" as distinct states, each with its own pass/fail verdict, and
  the rule for when a change earns a new version number versus an unversioned "repair" is stated but
  takes real effort to hold in your head (e.g., "fixing prose that was already wrong does not earn
  one"). I followed it, but only on a second pass.
- **`LIMITS.md` section 11**, the newest addition (dated 2026-08-18, added after everything else),
  concedes that the panel's own *collection date* was never recorded anywhere, and can only be
  bracketed to a 9.5-day window. This is presented as a serious, currently-unresolved problem for
  every age-banded number in the bundle — but the bundle still leads with those same age-banded
  numbers on its front page (`README.md` §4) without that caveat attached at the point of first
  use. I didn't understand why the fix was to add a late appendix rather than to soften the headline
  claim it undercuts.
- Exact meaning of `INDETERMINATE` vs `NOT-RETRIEVABLE` vs the `B-truncated` "control arm" took
  three different documents (`LIMITS.md` §1, §8, `FIGURES.md` §6) to piece together fully; no single
  place states all three together plainly.

## 6. Was anything confusing, off-putting, or did anything make you trust it less?

Yes, on balance more than it earned my trust. Two things stood out:

- **The volume of process relative to the size of the finding.** The empirical core is fairly
  modest — about 12% of a specific, non-random set of old cited videos return an opaque error from
  a public endpoint, rising with video age — but it arrives wrapped in six "failed gauntlets," a
  three-tier versioning scheme, a "provenance guard" that checks every number against a named JSON
  field, an "errata check" that tracks 53 previously-published corrections, and a document that
  discloses it once mixed up two similarly-named provenance files. Read cold, this reads less like a
  measurement and more like an elaborate machine for producing and re-litigating its own
  credibility, which made me more suspicious of the underlying numbers, not less — a document that
  has to keep telling you how carefully it checked itself is doing a different job than one that
  just shows its work plainly.
- **The letter's framing is unusual.** It's addressed to a real, identifiable dashboard operator who
  was, by the document's own repeated statement, never contacted and did not ask for this. The
  bundle is built and revised entirely by an unnamed, uncontactable "practice," with no human author
  or institution named anywhere in the folder. Combined with the letter's claim to be "written to be
  forwarded unedited by a human being," that gave the whole thing a slightly odd, one-sided quality
  — a document constructed to be handed to someone by someone else, about a third party, without
  any of the three ever having spoken.

I did not find anything that looked like fabricated or self-contradictory data on inspection — the
sample I checked (`series/presence-series.csv`, `gradient-test.json`) matched the numbers quoted in
the prose, and the reasoning about what "not retrievable" can and can't mean (§1 of `LIMITS.md`) is
genuinely careful. My hesitation is about the surrounding apparatus, not the arithmetic I could see.

## 7. Which file did you open first, and did that turn out to be the right place to start?

`README.md`. Yes — it's the first file alphabetically, it opens with a bold "STATUS — read this
first" banner, and it links out correctly to the letter, the limits file, and the version history.
It was the right entry point and I'd start there again.
