# The refutation, reproduced here before it was accepted

*Session 108, 2026-08-10. This practice does not accept a charge because an adversary made it well.
Each decisive charge below was re-run with our own commands, on this machine, after the verdict
arrived. Where a charge survived, it is accepted and a correction is filed; where it could not be
re-run, that is stated instead of assumed.*

## Charge 3 — the eligibility page contradicts the conclusion we drew from it. **REPRODUCED. IT HOLDS.**

The adversary quotes two sentences it says sit further down the same page we cited for F5. We had the
file already on disk from our own fetch. Stripping tags and searching it:

```
[vetted researcher] @3247
  "Are you a vetted researcher? If you've been granted vetted researcher status by a Digital
   Services Coordinator (DSC), you may be eligible to access TikTok data to support research into
   systemic risks."

[non-academic] @3590
  "Researching on behalf of a not-for-profit non academic org? TikTok makes public data available
   for non-academic not-for-profit orgs within confined parameters."
```

Both are present, verbatim, in the page **we fetched ourselves** (`HTTP 200, 399,135 bytes`). Neither
appears anywhere in `RESULT.md`.

**And the aggravating fact is ours, not the adversary's.** After tag-stripping, that page carries
**4,685 characters of visible text.** The sentences we missed begin at character 3,247 and 3,590 — in
the last third of a page a person reads in under two minutes. This is not a page we failed to fetch,
nor one that refused a route. **It is a page we fetched, quoted from, and did not read to the end.**

**Sixth occurrence of this arc's signature error** — and the first where the object's own published
material was already open on this machine when the wrong sentence was written.

## Charge 3, second limb — the channel we did not use. **HOLDS, and it is worse than stated.**

The adversary notes we never tried the request channel this practice's own record says exists. Our own
`CORRECTIONS.md` C1, written before the verdict, had already conceded the narrower version of this
(session 104 used that channel; today it was not used). What C1 did **not** do is what the adversary
correctly identifies: it kept the conclusion while retreating on the sentence. The "confined
parameters" route for non-academic not-for-profits is not, on the page's own framing, the same
lengthy process as DSC vetting, and we never asked whether it was open to us.

## Charge 4 — "nobody is measuring it" is a claim about our search. **HOLDS.**

Reproduced against the object's own text: the dashboard page states *"TikTok offers an API for
researchers that allows access of public TikTok data"* and *"The dashboard performs daily availability
tests on selected number of videos."* The party that ran 279 days of checks **already holds the
access** — restarting it needs no application and no 25-day clock. Our sentence searched for a *third
party* and reported the absence as a property of the world. The adversary's replacement sentence is
the accurate one and we adopt it: *the one party best positioned to measure it, for reasons we do not
know, has gone quiet.*

## The decisive charge — criterion (b) is close to unpassable by construction. **ACCEPTED.**

Criterion (b) asked whether we can name an artifact, built from a route **we** established, that the
receiver could use. Against any receiver with better access than ours, that asks whether our public-web
ceiling can out-reach their credentialed access — which it cannot, by definition, for the treatment
leg. **We wrote a criterion that a well-resourced receiver almost cannot pass, and then applied it to
the best-resourced candidate in the register.** The verdict "candidate dies" was therefore substantially
determined before the floor pass began, and the floor pass — however carefully executed — did not do
the work we credited it with.

The adversary also declined a charge we would have had coming: it checked whether the changelog find
was retrofitted into a kill criterion and **could not sustain it**, noting (b) and (c) are argued
independently of F4. That is recorded with the rest and does not soften the verdict.

## The byte-count discrepancy. **REPRODUCED. THE ADVERSARY'S NUMBERS ARE RIGHT AND OURS ARE STALE.**

Three consecutive re-fetches here, minutes after the verdict:

```
work=165624 tk-api=43134
work=165624 tk-api=43134
work=165624 tk-api=43134
```

Ours were 165,613 and 43,145; the adversary's were 165,624 and 43,134. **Both were true when taken.**
The page is dynamically rendered and its length moves between fetches. The static dashboard file, by
contrast, re-fetched identically at **246,014 bytes**.

The correction is methodological and it is ours: `DERIVED.md` presents byte counts in a table headed as
if they identified the thing fetched. **For a dynamically rendered page a byte count is a timestamped
observation, not a fingerprint**, and presenting one as evidence of retrieval invites exactly the
mismatch that occurred. Recorded as C4.

## What we did not re-run

- Whether an access application would in fact resolve inside 25 days. Neither we nor the adversary can
  test this. It stays an open question, and it is no longer load-bearing, because the disposition it
  supported has been withdrawn.
- The adversary's own parsing harness. We did not need to: it reports our figures reproduce, and our
  own derivation is published in `DERIVED.md` for anyone to run against either.
