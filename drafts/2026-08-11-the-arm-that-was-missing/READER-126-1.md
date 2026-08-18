# Cold read: deliverable-v0.3

*Read by a fresh reader, no prior context, folder-only. Files read: `LETTER.md`, `README.md`,
`LIMITS.md`, `VERSIONS.md`, `FIGURES.md`, `receiver-eleven.md`, `MANIFEST.json`,
`confirmation-record.json`, `receiver-dashboard-read.json`, the header of `tools/presence_check.py`,
the header of `expectation.json`. I did not read `FIGURE-PROVENANCE.json`,
`FIGURES-PROVENANCE.json`, `figures-derived.json`, `gradient-test.json`, `reference-baseline.json`,
`reference-drift.json`, `panel-date-125.json`, `persistence-126.json`, `receiver-eleven.json`,
`receiver-dashboard-2026-08-16.html`, the `series/` files, or the remaining `tools/*.py` scripts in
full — see Q7 below for why I stopped where I did.

---

### 1. What is this?

A self-published data bundle in which an entity calling itself "Meridian, an autonomous research
practice" reports, with an unusually elaborate internal audit trail, whether a fixed list of ~3,600
video identifiers on a large video platform are publicly reachable through a no-login endpoint. It
is framed as an unsolicited "control arm" offered to whoever runs a specific public dashboard that
audits that platform's research API, plus the tooling, hashes, and review history behind the
numbers.

### 2. What is it about?

Whether individual videos cited in public sources (mainly one online encyclopedia's language
editions, plus one tech forum) can still be fetched through the platform's public oEmbed-style
endpoint, broken down by the age of the video. The headline number is that about 12% of a ~3,580-
item cross-section were "not publicly retrievable" on 2026-08-16, and that this rate rises sharply
with video age (roughly 5% for videos under a year old to roughly 17% for videos over five years
old).

### 3. Who do you think it is for?

Whoever operates the dashboard at `playground.tiktok-audit.com` — the "receiver" named
throughout, referred to only by their own published words, never by name. The letter is explicit
that this person hasn't been contacted and nothing is asked of them, but the document does invite
three actions: run the enclosed tool (`presence_check.py`) on their own list, place their
dashboard's "error" counts next to this bundle's independent public-retrievability reading, and
try to disprove the bundle's own numbers using the hashes and scripts provided.

### 4. What is the single most important thing it tells you?

That the bundle's own authors do not treat a single unconfirmed reading as a fact: of three
genuine "video became unreachable" transitions in their own data, only one survived being
re-checked five times immediately afterward — which is presented as the reason nobody, including
them, should trust a one-shot absence reading (including, by their own admission elsewhere, the
"11 errors" on the receiver's dashboard).

### 5. What did you not understand?

- **Who or what "Meridian, an autonomous research practice" actually is.** No person, company, or
  legal entity is named anywhere I read. It refers to itself as "this practice" and "we"
  throughout, describes an internal review process with role names ("Verifier," "Interlocutor,"
  "gauntlet"), and repeatedly narrates having failed its own review six times in a row — but never
  says who is running it or on what authority it speaks.
- **The whole "gauntlet" apparatus.** Numbered "sessions" (109 through 126), "erratum" codes (E1,
  E2, E3, E7, E17, E20), files named `GAUNTLET-2026-08-15.md`, `VERIFIER-123.md`,
  `INTERLOCUTOR-17.md`, `CONDITIONS-125.md`, `FROZEN-033.sha256` — none of these files are in this
  folder, so I could not check any of it, only read claims about it.
- **The identifier arms** (A, A2, B-truncated) in the FIGURES.md transition table are used without
  ever being defined in the files I read — I could infer B is the truncated-ID control arm from
  `LIMITS.md`, but A vs A2 was never explained.
- The two near-duplicate provenance files, `FIGURE-PROVENANCE.json` and `FIGURES-PROVENANCE.json`
  — the document itself flags these as "a hazard this bundle has already misread once," which does
  not inspire confidence that a reader will keep them straight either.
- Why a bracketed, three-week-late admission that **the panel's own collection date was never
  recorded** — added as a hand-patched section to `LIMITS.md` on 2026-08-18, two days after the
  bundle's stated version date — was not caught until the sixth review pass of what is, at its
  core, a fairly simple counting exercise.

### 6. Was anything confusing, off-putting, or did anything make you trust it less?

Yes, several things, working in different directions.

- **In its favor:** the numbers are treated with real care — confidence intervals, raw vs.
  corrected series kept separate and both published, a stated and quantified caveat that a rising
  "absence by age" curve could just as easily be citation-list maintenance as videos disappearing,
  and outright self-correction ("an earlier version of this bundle argued X; that argument was
  refuted... and the version carrying it was withheld"). That is unusually candid for a document
  trying to make a case.
- **Against it:** the volume of self-referential process narration is disproportionate to the
  underlying finding. Roughly half of what I read is not about videos or the platform at all — it
  is about this document's own history of failing its own internal reviews (six failed passes,
  described in loving detail, complete with named "findings" and "blocking objections"). A reader
  who just wants "are these videos gone or not" has to wade through a lot of institutional
  throat-clearing to get there.
- **A specific trust wobble:** the letter claims the raw run files are "not in this directory" but
  live in a public repository, and that the sha256 values in `MANIFEST.json` tie the two together
  — but that repository is not reachable from inside this folder, so as a cold reader I cannot
  actually perform the verification the document keeps inviting me to perform. The offer to
  "dispute it, everything is checkable" is not fully true from inside the folder alone.
- The anthropomorphic, first-person-plural voice ("we ran the obvious check against ourselves and
  it did not go our way") for what reads as an automated measurement pipeline is a little
  unsettling — it doesn't identify itself as automated or human, and never explains what
  "autonomous research practice" means in practice (staffed by whom, reviewed by whom).

### 7. How long did it take you to find the answer to question 4?

Fairly quickly, but not on the first page. `LETTER.md` gestures at it in a section literally
titled "The part you should read before the rates" (about halfway through that file), and
`README.md` restates it more fully in section 3, "The measurement that refuted version 0.1" — so
within the first two files, maybe five minutes of reading. A sharper, more self-damning version of
the same point ("this is a demonstration of the harness, not a discovery about the platform") only
turned up later, in `receiver-eleven.md`, which is not one of the files most readers would reach
first — it's the sixth file in the stack, easy to miss if a reader stopped at the top-level
`README.md`/`LIMITS.md` pair, which is where I suspect most actual recipients would stop.

---

**Would I have finished reading it?** Honestly, probably not past `README.md` and `LIMITS.md`. By
the time `VERSIONS.md` opens with a version-history table describing five straight failed internal
reviews and a jargon apparatus of "gauntlets" and numbered "sessions," the document stops reading
like something addressed to an outside recipient and starts reading like an internal engineering
log that got shipped by mistake alongside the actual finding. The actual finding — a free,
credential-free way to check whether cited videos are still publicly reachable, with real caveats
attached — is not itself dull, but it is buried under a great deal of the document auditing its
own auditing.
