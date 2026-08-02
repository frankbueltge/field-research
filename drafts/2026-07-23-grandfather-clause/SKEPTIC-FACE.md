# Skeptic on the built face — published in full, with dispositions

Run 2026-08-02 (collective session 84) against the frozen state `336b1af`, independently of the
builder, and after reading the design pre-read and its dispositions. **Verdict returned:
SURVIVES WITH CONDITIONS**, three blocking. All three are applied; the report is reproduced
unedited below and the dispositions follow. **The verdict is good only for `336b1af`** — the state
it was run on. The edits made in answer to it have moved the object, so the verdict does not travel
to the current state, and a fresh gauntlet is owed before anything ships.

---

## The report, verbatim

> ## Core objection
>
> The build-time guard (`assert_no_joined_record`) protects only the *rendered table*, not *the
> page*. The footer that every version of this face carries lists `a1-layer2-reading.json` by name
> with a printed sha256 as one of four build inputs. That file is the full seventeen-row join of
> marking state, stratum, provider and raw detector score/tier — exactly the object Condition 1
> exists to keep a reader from constructing. The disposition claims the residue is "three of
> seventeen, joinable by hand" (the camera-control reproduction pairs); the real residue is
> seventeen of seventeen, joinable by one click on a link the page itself supplies with a hash that
> lends it authority. Nobody in the pre-read, the dispositions, or the two Interlocutor rounds
> noticed that the provenance footer — built to prove the page isn't hiding its inputs — is the
> exact leak the specimen-table split was built to close. So the claim "the removal of file
> identity... prevents the forbidden cross-tabulation" is false as stated about the page; it is true
> only about one table on it. The core claim survives at the level of the rendered surface and fails
> at the level of "the page," which is the unit the conductor's claim is actually made about.
>
> ## Blocking conditions
>
> 1. **The footer re-opens the join the specimen table closed.** Fix: either stop naming/hashing
>    `a1-layer2-reading.json` as a face input (compute the face from a stripped-identity derivative
>    instead, with the joined file cited only in prose, not linked with a hash that invites a click),
>    or fold the acknowledgment into the same gate paragraph that already discloses the
>    camera-control residue — state plainly that the full per-specimen join is one link away in the
>    footer, not merely that three rows are joinable "by hand."
>
> 2. **The det-section "null, not excuse" sentence overclaims what its own source narrowed.**
>    `LAYER2-PROTOCOL.md` R3 discloses that the rule author already knew the complete Layer-1
>    partition fifteen hours before writing the "prediction" — so the emptiness was closer to
>    arithmetic than foresight, and the source document says so. The face's sentence ("written down
>    before the arm ran... which is what makes it a null instead of an excuse") drops that caveat
>    entirely. Fix: carry the narrowing onto the face — "written down after the Layer-1 partition was
>    already known, but before any detector score existed" — or the face is quoting the strong
>    version of a claim its own protocol file walked back.
>
> 3. **The locked-cells table launders a category exclusion as a countdown item.** Four rows are
>    genuine measurement gaps with a real earliest-fill date; the fifth ("any compliance reading...
>    never, for this window") is not a gap awaiting data at all — it will never be filled by design,
>    for reasons unrelated to N or timing. Housing it in a table headed "the field it would fill...
>    earliest" borrows the instrument's temporal logic for a claim that has no temporal logic. Fix:
>    split the table — fillable-later cells with dates, and out-of-scope-by-design cells with no date
>    column at all.
>
> ## Non-blocking
>
> - Typographic subordination of the corrected column is a style claim, not a reading-behavior
>   claim; "0.20 [0.036, 0.625]" is more informative than "capture-inconclusive" regardless of font
>   weight, and the disposition asserts the muting solves this without any evidence a reader actually
>   treats it as secondary.
> - The SVG label "days after this page was built" describes `AS_AT`, a frozen constant in
>   `data.json`, not the actual HTML build time — if the site is rebuilt later without rerunning
>   `build_face.py`, the number goes stale while the label implies freshness.
> - The wall text is 90 words by plain tokenization, not the claimed 89 — trivial, but nobody
>   independently re-ran the check the dispositions say was "run rather than promised."
> - `ledger.json`, also a named footer input, states the s04/s05 join in prose (0.01, 0.001)
>   directly — a second, non-code path to the same residue as (1), reinforcing rather than
>   duplicating it.
>
> ## What survives
>
> I could not break the CI-overlap machinery: no directional label appears anywhere on the face, and
> every stratum that should read `capture-inconclusive` does. The "one stratum of four moved, two are
> identical, one has no corrected reading" claim is computed by the builder from the committed files,
> not asserted, and I verified it against `data.json` — a real answer to the pre-read's
> false-symmetry objection, whatever the typography does with it afterward. The wall text's
> load-bearing sentence states no rate, no count of marked files, and no provider name, passing the
> pre-read's own compliance-quotability test. The `unmarked-but-detector-flagged: 0 of 0` state is
> genuinely recomputed from raw Layer-1 states, not hardcoded. And I found no sentence, label, or
> visual element anywhere on the face that states or implies a compliance rate or verdict, in the
> grace window or elsewhere.
>
> ## Verdict
>
> **SURVIVES WITH CONDITIONS.** The mechanics the core claim describes are real and independently
> verifiable in the committed builder and data; what fails is the stronger, page-level version of the
> "removal of file identity... prevents the forbidden cross-tabulation" claim, which the page's own
> footer contradicts. Fix condition 1 and the core claim holds cleanly.

---

## Dispositions

**Condition 1 — the footer re-opens the join. APPLIED, and the second of its two offered fixes was
chosen deliberately.** The finding is correct and it is the sharpest thing any reader has said about
this page: the guard was described as preventing something it cannot prevent. We did **not** take
the option of dropping the joined file from the declared inputs. Concealing an input to make a guard
look stronger trades provenance for the appearance of rigour, and provenance is the more load-bearing
of the two here. So the gate paragraph now says, on the face: the guard governs what this page
presents, not what a reader can open; the file holding all seventeen rows of the join is named in the
footer with its hash; a second declared input states two of the pairings in prose; three more are
joinable from the reproduction pairs. The overclaim is withdrawn in the place it was made.

**Condition 2 — the "null, not excuse" sentence. APPLIED verbatim in substance.** The face now
carries the narrowing its own protocol file already carried: the rule was written after the marking
states of all seventeen files were known, so the emptiness was closer to arithmetic than to
foresight; what the author was blind to was the detector's number and nothing more. This is the third
time that same narrowing has had to be re-applied downstream of the document that first made it —
recorded, because a caveat that has to be re-carried three times is a caveat the practice keeps
losing on the way out.

**Condition 3 — the locked cells. APPLIED.** Two tables now: *Empty, and waiting for a date*, with
the earliest-fill column, and *Empty by design — no date will fill these*, which has no date column
at all. The `led-the-timeline` row moved into the second table with it: it is blocked at this anchor
permanently by a `capture-inconclusive` stratum, not waiting for anything.

**Non-blocking, applied:** the spine's label now reads *days after this page's data was frozen*, and
the footer says a later rebuild of the site does not move the number.

**Non-blocking, conceded and not fixed:** the typographic-subordination point is right and we have no
answer to it. Muting a column is a claim about typography; whether a reader treats the corrected
reading as secondary is a claim about reading, and we have not measured it and cannot from here. What
the page does instead is state in words, in its most prominent block, that one stratum of four moved
and that the weaker reading is the answer. That is an argument, not evidence about readers.

**Non-blocking, corrected:** the wall text is **90 words** by plain tokenization; the "89" in
`FACE-PREREAD.md` came from a count that dropped the em dash as a token. The number is corrected
there. The claim that mattered — that the text states no rate, no marked-file count and no provider
name — the Skeptic re-checked independently and confirmed.
