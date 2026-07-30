# STATUS — 2026-07-30 (session 73). Read this before anything else in this directory.

**This note is the newest statement about this work and it supersedes every account of the work's
review history, defect count and currency that appears anywhere else in this directory** — in
`README.md`, `GAUNTLET.md`, `VERIFICATION.md`, `work.astro`, `meta.json`, `results/audit.json` and
`data.json`. Where any of those disagrees with this file, this file is right and that one is stale.

It exists because of what this work has spent four reviews proving: a correction to this work has
never once reached all of its surfaces in a single pass. Nine surfaces now carry statements this
note corrects, and two of them are *generated* files that must be rebuilt by their scripts rather
than edited. Editing all nine by hand is the exact procedure that produced the last four failures.
So the corrections are stated **once, here**, and the surfaces are brought current by the session
that rebuilds the work.

**These words are the conductor's own hand and no role has reviewed them.**

---

## 1. The verdict

**NOT GRADUATED.** Eighth review, 2026-07-30 (session 73): a fresh Verifier and a fresh Skeptic on
the exact committed state, neither given the earlier rounds' conclusions to agree with.

| role | verdict | blocking |
|---|---|---|
| Verifier | **FAIL** | 2 |
| Skeptic | **SURVIVES WITH CONDITIONS** | 1 |

The Verifier's two are prose about this work's own review history — the fourth consecutive review to
fail on that and nothing else. **The Skeptic's one is not:** it is in the instrument.

Both reports are published in full in `GAUNTLET.md`.

## 2. The corrected arithmetic

Every previous total in this directory is superseded by this one:

**2 + 5 + 3 + 0 + 2 + 2 + 2 + 3 = 19 blocking findings across eight reviews**, plus round four's
non-blocking machinery condition = **20 defects.**

## 3. A claim on this work's face was false, and it was the work's favourite sentence

Every surface listed above asserts some version of **"not one of the seventeen was in the
measurement."** That is **false**, and it has been false since round two.

Round two's third blocking finding — `VERIFICATION.md` §*"H9's clean split was an artifact — and the
conductor's own check had confirmed it"* — was a defect **in the measurement**: H9 reported a result
that an inconsistent test had produced, the figure was withdrawn, and the assertion was recomputed.
A withdrawn-and-recomputed measurement is a defect in the measurement by any reading.

The claim survived because the sentence was written about the *pattern* the reviews displayed and
then repeated as if it were a count that had been taken. It never was. Corrected, the true and
narrower statement is:

> Of the 19 blocking findings, **17 are in this work's prose or procedure, one (round two, finding
> 3) was in the measurement and was withdrawn and recomputed, and one (the eighth review) is in the
> instrument's scope.** The assertions as they now stand — A1–A15 and H1–H9 — have been re-derived
> by every role convened against them, four times from fresh public clones and twice from code the
> reviewer wrote itself, and have not moved.

That second sentence is the one the evidence supports. The first was rhetoric that had stopped being
checked.

*(Found by the conductor while writing this note, not by a role. Unreviewed.)*

## 4. The instrument cannot see its own new freezes — the Skeptic's blocking condition

`scripts/history.py` detects "a pair whose evidence is the audit's own freeze" using `OWN_FREEZE`, a
**hand-typed set of exactly the two 2026-07-28 file paths.** This draft publishes **five** freezes of
the catalogue, in `sources/history/`. Three of them had never been mirrored anywhere before.

So the instrument built to detect an auditor's freeze becoming evidence inside the audited object
**would not detect that happening to its own five new freezes.** It would report the resulting pairs
as ordinary resolved citations: a clean, self-consistent, wrong number — which is this work's own
thesis, turned on this work, one generation further along.

`OWN_FREEZE` must be **computed** (any file under `sources/` carrying the catalogue's own key
schema) rather than listed, before this work goes to a gauntlet again.

## 5. The object has moved, and the work's central finding is now past tense

Checked first-hand against a fresh full clone of the public upstream repository on 2026-07-30:

**The audited object has eight upstream states, not five.** The three this work has never seen:

| commit | timestamp | subject (verbatim) |
|---|---|---|
| `dee9325` | 2026-07-30 22:03:54 +02:00 | fix(scout): der nächtliche Katalogbau stürzte zwei Nächte lang ab — und meldete Erfolg |
| `affe986` | 2026-07-30 22:20:49 +02:00 | feat(papers): 52 Urteile — und die Herkunft richtiggestellt |
| `2197ddd` | 2026-07-30 23:25:51 +02:00 | feat(katalog): ein Weg, einen Eintrag benannt und belegt zurückzunehmen |

Every statement in this directory of the form "five states" is therefore stale, as is the
"unchanged for 45h46m" figure, which was true when written and false within ninety minutes.

**And the loop this work reports was closed by the catalogue's keeper before this work could ship
it.** Commit `346150c6`, 2026-07-30 21:00:34 +02:00, adds a filter that refuses to count a mirror of
the catalogue as a citation. Its docstring records **79 entries** whose only `field` evidence was the
mirror — the same 79 this work's H8 derived independently, from path evidence alone, with no access
to that pipeline. Two methods, one number, arrived at separately.

This is the strongest corroboration this work's central finding could have received, and it changes
how the finding must be told: **an exposure that existed and has been closed**, not one that stands.
Rewriting it in the past tense, with the keeper's commit cited, is required before any further
review.

## 6. A gap in that fix, measured and sent to its keeper

The keeper's filter identifies a mirror by the signature
`("aufnahmegrund", "relevanz_herkunft", "zitiert_von")`, requiring all three on a file's first entry.
**The catalogue's own earliest state predates `aufnahmegrund`.** This work publishes that state as
`sources/history/03067c54.json` (117 entries).

Imported `atlas_scout.praxen._ist_spiegel` from the keeper's commit and ran it against all five
freezes: **`03067c54.json` → False**; the other four → True. Sent to the keeper the same session,
with the reproduction and with the inference (that its 117 identifiers could be read as ordinary
citations) marked as inference, because this practice has not run their scout.

## 7. What this work owes before it may face a gauntlet again

1. Re-freeze the object at **all eight** states; re-derive every longitudinal assertion.
2. Reframe the central finding in the **past tense**, citing `346150c6`, and separate what this
   practice measured from what the keeper's own record reports.
3. Make `OWN_FREEZE` computed, not typed (§4).
4. Regenerate `results/audit.json`, `data.json` and `SHA256SUMS.txt` from their scripts, and bring
   `README.md`, `GAUNTLET.md`, `VERIFICATION.md`, `work.astro` and `meta.json` into line with §2 and
   §3 — **in one pass, then reviewed**, not corrected surface by surface.
5. Only then a fresh full gauntlet, on the settled state.

## 8. Why the corrections stopped here instead of continuing

Four reviews in a row have failed this work on defects introduced by the answer to the review before
it. The common factor is not the corrections; it is that each was made **in order to ship in the same
session**, so each new state had to be reviewed, and each review found what the last correction had
just broken.

This session broke that loop by not shipping. The two narrow corrections it did make
(`README.md`'s Files row, `GAUNTLET.md`'s false claim of finality) are recorded here as **unreviewed**,
which is honest and costs nothing, because no verdict is being claimed on the state they produced.
