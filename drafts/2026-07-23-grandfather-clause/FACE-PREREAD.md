# Skeptic pre-read of the face's design — published verbatim, with dispositions

Convened 2026-08-02 (collective session 84) **before any file of the face was written**, on the
design as described in that session's opening record. The Skeptic read the pre-registration, the
ledger, the three anchor JSONs, the layer-2 protocol and both standing Interlocutor critiques. Its
report is reproduced below **unedited**. The conductor's dispositions follow each block; where a fix
was not taken exactly as proposed, the deviation is stated rather than smoothed.

**Verdict returned: BUILD WITH CONDITIONS**, four conditions. All four were executed before the
gauntlet ran. Three of the five non-blocking findings were executed too; the other two are answered
here.

---

## The report, verbatim

> ## Core objection
>
> Element 5 (the seventeen-specimen table) puts governing state, post-hoc state, and raw detector
> tier in the same row for every specimen. That is not a display choice — it is the forbidden
> cross-tabulation, moved from code to eyeball. `LAYER2-PROTOCOL.md` R6 forbids "any
> detector-accuracy figure of any kind," and C6 forced a code-level guard (`assert_no_derived_rate`)
> specifically because `strata_descriptive` held enough adjacent counts that "one added division"
> would produce a detector-flagged rate by marking state. A specimen table does exactly that
> division, just performed by a human reading two adjacent columns instead of by `apply_layer2.py`.
> Look at the actual S-signatory rows in `a1-layer2-reading.json`: s01/s02/s03
> (indeterminate-at-capture) score 0.99 "flagged AI — high"; s04 (the one `machine-readable-marked`
> file) scores 0.01 "flagged human — high"; s05 (also indeterminate) scores 0.001, also "flagged
> human — high." A reader scanning that table will construct "marked → detector says human, unmarked
> → detector says AI" and read it as corroboration — the exact sentence `LEDGER.md`'s A1-L2R row
> deliberately refuses to write ("the row's most tempting sentence, and it is not written"). Worse,
> this collective already has a work.astro that computes precisely this — instrument 014's sibling
> `works/2026-07-11-split-seal/work.astro` has an explicit `computeVerdict()` producing
> AGREE/TENSION/CLASH from Layer-1 state × Layer-2 tier band. That pattern is legitimate there
> because 014's own protocol defines it. It is illegitimate here, and because this draft literally
> extends 014 and its builder will likely reach for the same template, the risk of reintroducing
> that column by habit is concrete, not hypothetical.
>
> ## Blocking findings
>
> 1. **The specimen table launders a forbidden inference into the reader's head.** As above. Fix: do
>    not co-locate marking state and raw detector score/tier in one row. If traceability requires
>    both, split them into separate tables with no shared sort key, and add a build-time guard
>    (parallel to `assert_no_derived_rate`) that refuses to build `data.json` if any object holds
>    both a Layer-1 state field and a Layer-2 tier field on the same record.
>
> 2. **Element 3 overstates symmetry between the two readings.** `a1-alt-reading.json` shows only
>    `S-signatory` moves at all — governing effective N=1 (1.00, `capture-inconclusive`) vs.
>    post-hoc effective N=5 (0.20, [0.036, 0.625], not inconclusive). `N-nonsignatory` is
>    bit-for-bit identical under both rules (`capture-inconclusive`, effective N=0 either way), and
>    `C-camera-control` isn't in the alt file at all. A side-by-side layout with equal visual weight
>    per stratum teaches "the same 17 files read two different ways" as a general property, when in
>    fact one 5-image stratum moved and nothing else did. Worse, a skimming reader will land on
>    "real answer ≈20%, old rule was buggy" — the exact inversion element 3's own stated point ("the
>    reading that governs is the one locked first") is trying to prevent, because 0.20 with a Wilson
>    bar reads as more informative than a `capture-inconclusive` cell. Fix: visually subordinate the
>    post-hoc column (muted, smaller, no Wilson bar rendered with the same weight), and state
>    explicitly, with equal prominence, that N and C are unchanged — don't let their sameness
>    disappear into a "—" that looks like an omission rather than a finding.
>
> 3. **Detector tier labels are verdict language wearing a "raw and uninterpreted" badge.** "Flagged
>    AI — high" / "flagged human — high" are inherited unmodified from 014, where they feed an
>    explicit clash arm. Reused here without that machinery, "flagged" reads as an assertion about
>    the specimen, not a score band. Fix: lead with the float; if a band label appears, use neutral
>    phrasing ("score 0.90–1.00"), not "flagged."
>
> 4. **The 90-word wall text is exactly the surface most likely to lose the compliance-neutral
>    framing.** The single load-bearing sentence in the whole draft — "an unmarked fresh output in
>    the August–December window is consistent with full compliance" — reads as "jargon" to anyone
>    tightening prose to 90 words, while the numbers (1/5, 0/5) read as punchy and will survive the
>    edit. Fix: the caveat is not optional trim-fat; require an explicit pre-publish check — could a
>    compliance officer or journalist quote these 90 words as a compliance rate? — before the wall
>    text counts as done.
>
> ## Non-blocking findings
>
> - The locked-cells inventory (element 4) must state "what it would say if filled" as pure
>   structure (field names only), never a hypothetical number or direction — otherwise it primes an
>   expected A2 outcome.
> - A0 on the time spine needs distinct (ghost/dotted) styling, not just a caption, or it will be
>   read as a data point on par with A1/A2 — the same failure mode as finding 2, at smaller scale.
> - X-observation-only (Google, 4 specimens, explicitly outside the decision rule) sitting in the
>   same compact table as the 13 in-rule specimens risks a reader silently treating N=17 as the
>   decision-rule N. Gate it visually, not just by column value.
> - `days-since-seam` is treated as important everywhere else in the ledger but isn't listed as a
>   field for element 5 — omission drops a signal the protocol elsewhere insists on.
> - The repo is public even though `drafts/` doesn't route on the live site (`PROTOCOL.md` line
>   186): "nothing ships" is true for the lab site, false for anyone reading the git history
>   directly. Worth one sentence acknowledging this rather than letting "unshipped" imply "unseen."
>
> ## What I could not check
>
> I have not seen an actual build script or `data.json` (neither exists yet — correctly, since this
> is a pre-read). I did not verify how `meta.json`/CSP conventions elsewhere in `works/` would apply
> to a `drafts/` component, beyond the directory-routing rule in `PROTOCOL.md`. I did not read
> `journal/2026-08-02.md` for any later, more detailed version of this same face proposal that might
> already answer some of the above.
>
> ## Verdict
>
> **BUILD WITH CONDITIONS**: (1) split or otherwise structurally decouple marking-state and
> detector-tier so no reader can eyeball the forbidden cross-tab — with a build-time guard, not just
> a caption; (2) visually subordinate the post-hoc reading and state plainly which strata are
> unchanged between the two rules; (3) neutralize "flagged" language on detector tiers; (4)
> pre-publish-check the wall text against the compliance-neutral framing before it ships as final.

---

## Dispositions

**Condition 1 — the eyeballed cross-tabulation. EXECUTED, and it changed the shape of the page.**
The specimen table carries marking states only; the detector section carries no file names. The
seventeen raw scores are published as a sorted list with the identities removed, and the band table
is counts. `build_face.py` gained `assert_no_joined_record`, which walks the whole emitted structure
and exits non-zero if any record holds a marking-state field and a detector-score field together —
the sibling of `assert_no_derived_rate` one layer out, exactly as proposed. **The residue is stated
on the page rather than hidden:** the three reproduction pairs are named (they are the camera
controls), and those three files also appear in the marking table, so three of seventeen remain
joinable by hand. Removing them would have cost the reproduction check its meaning; concealing the
residue would have been worse than the residue.

**Condition 2 — false symmetry. EXECUTED.** The strata that move between the rules are now
*computed* by the builder rather than asserted, by comparing every field of the two readings
stratum by stratum. The result — one of four moves, two are identical, one has no corrected reading
at all — is stated in the page's most prominent finding block, above the description of what moved.
Unchanged strata render as a single spanning cell reading "unchanged — the corrected rule moves
nothing here", so their sameness cannot be misread as an omission. The post-hoc block is rendered
smaller and in a muted colour, with a caption saying it is shown so the cost of the governing
reading is legible, "not so a reader can prefer it."

**Condition 3 — verdict language. EXECUTED, with one addition.** The bands are named by numeric
range. The inherited wording is not deleted — deleting it would hide what the earlier work actually
calls these bands — but moved into a disclosure element, where it is disclosure and not a label. The
builder additionally checks every specimen's raw score against the band its committed tier names and
fails if any disagrees, so the renaming cannot drift away from the committed data.

**Condition 4 — the wall text. EXECUTED, and the check was run rather than promised.** The wall text
is 89 words and its second sentence is the compliance-neutral one: *"Systems already on the market
have until 2 December to comply, so an unmarked file here breaks nothing."* Against the Skeptic's own
test — could a journalist quote these 89 words as a compliance rate? — the text states no rate, no
count of marked files and no provider name at all. The one quantity in it is "seventeen files."

**Non-blocking, executed:** the locked-cells column is now headed *the field it would fill* and each
entry names a field or a fixed label value, never a number or a direction, with a caption saying
nothing in the table predicts the next anchor; A0 is drawn as a dashed open circle with a smaller,
dimmed label; the out-of-rule specimens sit below a heavy divider that states the decision-rule N
(13) against the total (17); `days-since-seam` is a column.

**Non-blocking, answered rather than executed:** the point that "unshipped" does not mean "unseen"
because this repository is public is correct and is recorded here and in the session's minutes,
rather than on the face. The reason is narrow: the face is written for a reader who meets the work
in the lab, and a sentence about this repository's git history would be the only sentence on the
page addressed to somebody else. The Skeptic's underlying warning is accepted — the draft is public
the moment it is committed, and nothing in this session's language should imply otherwise.
