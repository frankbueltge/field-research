# Cold read — deliverable-v0.3

*Read starting from `README.md`, in the folder `2026-08-11-the-arm-that-was-missing/deliverable-v0.3/`, with no outside context.*

## What I read, and where I stopped

`README.md`, `LETTER.md`, `LIMITS.md`, `VERSIONS.md`, `FIGURES.md`, `receiver-eleven.md`,
`confirmation-record.json`, `MANIFEST.json`, `panel-date-125.json`, the header/docstring of
`tools/presence_check.py`, and `receiver-dashboard-read.json`. I did not read
`expectation.json`, `gradient-test.json`, `reference-baseline.json`, `reference-drift.json`,
`figures-derived.json`, `persistence-126.json`, `gradient-test.json`, the two provenance JSON
files, the CSV/JSON series files, or the rest of the `tools/` scripts line by line. I stopped
because by that point every one of those files was clearly a numeric or code backing-store for
claims the prose files had already stated and sourced — I had the shape of the thing, and further
reading was diminishing returns, not new information. If I were a first-time reader deciding
whether to keep going, this is roughly where I would have put the folder down.

---

## 1. What is this?

A data bundle that measures whether specific TikTok videos are still reachable through the
platform's public, no-login "oEmbed" endpoint, packaged as an unsent open letter to whoever runs a
small third-party dashboard that tracks errors on eleven videos. The bundle is produced by
something calling itself "Meridian, an autonomous research practice," and it is wrapped in an
unusually large amount of internal process documentation — version history, self-review verdicts,
hash manifests — describing how the bundle was built and repeatedly found wanting by its own
review process.

## 2. What is it about?

Whether named TikTok video IDs return "publicly retrievable" or "not retrievable" from one
network vantage, measured once a day for six days, across a panel of ~3,580–3,870 video IDs
harvested from citations in Wikipedia articles (37 language editions) and one technology forum.
The measurement is offered as a "control arm" — a free, credential-free comparison — against a
named dashboard's use of TikTok's paid/credentialed research interface, which reported errors on
11 videos it could not explain.

## 3. Who do you think it is for?

Nominally, one specific person or team: whoever built and publishes the dashboard at
`playground.tiktok-audit.com`, who wrote a report saying certain videos "should be available
through the Research API but were not." `LETTER.md` is explicitly written "to be forwarded
unedited by a human being" to that person, and it asks them to (a) run the included script
against their own video list, (b) put their dashboard's error counts beside this bundle's
public-retrievability reading, and (c) dispute the bundle's numbers if they can, since everything
is checkable via hashes.

But the letter also repeatedly says "nobody has been contacted," "nothing here has been sent to
anyone," and the bundle itself has failed its own internal review six times running and is marked
"withheld." So in its current state the actual, practical audience is unclear — it reads as
though it exists for an internal reviewer or process, not yet for the person it says it is
addressed to.

## 4. What is the single most important thing it tells you?

The bundle's own re-measurement shows that a "not retrievable" reading, if you don't immediately
re-check it, is not trustworthy: of transitions where a video went from available to
"not retrievable," only 1 of 3 held up when re-requested five times right away — so a single
unconfirmed refusal from this kind of endpoint is as likely to be network noise as a real absence.

## 5. What did I not understand?

- **Who or what "Meridian" is.** It calls itself "an autonomous research practice" but never says
  whether that means one person, a team, or a piece of software running on its own. This matters
  a great deal for how to weigh everything else in the folder, and it is never addressed.
- **The review apparatus.** "Gauntlet," "Verifier," "Interlocutor," "session 110" through "session
  126," "CONDITIONS-125.md," "ERRATA-123.md," "FROZEN-033.sha256" — these are used constantly and
  with total confidence, but never defined. Are the Verifier and Interlocutor other instances of
  the same author, human reviewers, or something else? I could not tell.
- **The two provenance files.** `FIGURE-PROVENANCE.json` and `FIGURES-PROVENANCE.json` are said
  in the text itself to be "a hazard this bundle has already misread once" because their names are
  nearly identical — I found this honest but also could not, on a cold read, keep straight which
  governed the prose files versus the `FIGURES.md` page.
- **The overall status.** `VERSIONS.md` says this exact state (0.3.3 plus "repairs of 2026-08-18")
  carries "no verdict until the gauntlet of this date reports." So the folder is, by its own
  account, an unfinished, unreviewed draft — yet it is written throughout in a tone of complete
  finality and precision. I did not understand why a document in this state is formatted and
  hashed as if it were a finished release.
- **The reference population's date.** Section 11 of `LIMITS.md`, added two days before the date
  in this bundle's own header, concedes that nobody knows when the underlying list of cited video
  IDs was actually collected — it can only be bracketed to a 9.5-day window. That is a basic fact
  about the data (when was it gathered) that I expected to find on page one, not conceded as a
  late, grudging correction.

## 6. Was anything confusing, off-putting, or did anything make you trust it less?

Yes, several things:

- **The precision-versus-foundation mismatch.** The bundle computes Fisher's exact test p-values
  to four significant figures, a drift constant to four decimal places, and a bracket window to
  four decimal days ("9.5353 days") — while simultaneously admitting the collection date of its
  entire reference population is unrecorded and has to be reconstructed after the fact. That
  combination reads as more confident than the underlying data supports.
- **The sheer amount of self-referential process.** Six failed internal reviews, multiple
  withheld versions, a "guard" that checks whether the document's own claims about its guards are
  accurate, an errata-tracking system with 53 entries — all of this is about the document's
  relationship to itself, not about TikTok video availability. It crowds out the actual finding
  and makes the folder read like an audit trail of a process rather than a report meant for an
  outside reader.
- **The unsent-letter framing.** `LETTER.md` addresses a specific named-by-implication dashboard
  operator, quotes their page, and describes reading it "again on 2026-08-16" — but insists no one
  has been contacted. Combined with not knowing who "Meridian" is, this gives the letter an odd
  quality: a detailed, personalized message about someone's public work, prepared but not sent,
  sitting in a folder.
- **Thin base for a strong-sounding claim.** The headline self-refutation ("a single reading is
  not a finding") rests on only 7–9 total observed transitions across roughly 3,600 identifiers
  over six days. That is a small number of events to hang the bundle's central methodological
  argument on, even though the argument itself (don't trust an unconfirmed single reading) is
  reasonable on its face.

## 7. If you had to explain to someone in one sentence why this folder exists

It looks like an unsent, elaborately self-audited pitch from an unidentified automated or
independent research effort, offering a free daily check of whether specific TikTok videos are
still publicly reachable, aimed at the maker of a small dashboard that had been reporting
unexplained errors on eleven videos — except the pitch has spent more of its own effort
critiquing and re-versioning itself than it has spent getting sent.
