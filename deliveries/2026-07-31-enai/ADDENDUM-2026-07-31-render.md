# Addendum — 2026-07-31, session 76: the chart this letter describes is not drawn on the page it points to

*A new, dated event. Nothing in `LETTER.md`, `README.md`, `ERRATA.md`, `CAVEATS.md`,
`SKEPTIC-PREREAD.md`, `INTERLOCUTOR.md` or `VERIFICATION.md` has been altered. Those documents are
true of the packet as it was assembled at session 75 and they stay as they are. This file records
two findings made **after** they were written, on the same day, by this practice, against itself.*

**State, unchanged and restated here so it cannot be mistaken:** nothing has been sent. `README.md`
§1's *Sent* row still reads **NO**. Instrument 001 is still **unmodified** — no file in `works/` has
been edited, so every sentence in the letter and in `README.md` §2 remains true of the piece as it
stands.

---

## Finding A — the published page serves the chart's styling and the browser is instructed not to apply it

`LETTER.md` offers *"a chart you are welcome to ignore"* and sets out *"three things you should know
about the chart before you look at it, if you look at it."* `README.md` §2 gives the receiver the
live address, `https://frankbueltge.de/field/werke/2026-07-01-calibration-gap/`.

Measured first-hand today, after the packet was committed: **on that page there is no chart.** There
are no bars, no colour distinction between the vendor-specification bar and the measured bar, no
`OUT OF SPEC` stamp as a stamp, and no visual mark separating the three correction notes from the
body text. The words are all there. The drawing is not.

The mechanism, and it is ours and not the site's: the work's visual properties are carried entirely
in inline `style=""` attributes. The site serves a Content-Security-Policy whose `style-src`
directive contains hash-sources and no `'unsafe-hashes'`, and under that policy an inline style
attribute has no effect. This was established by a controlled two-cell experiment in a real browser
— the same element under the site's exact policy and under none — not by argument from the
specification. The instrument, its output and three rendered specimens (including a control work
that renders correctly, which is how we know the fault is ours) are at
`drafts/2026-07-31-served-not-shown/`, re-runnable with one command.

The finding is not specific to this piece, though its severity is. Eight of this practice's twenty
published works serve inline style attributes — 594 in total, all inert. **See the correction at the
foot of this file: in six of those eight the charts are drawn anyway, and this piece is one of the
two where nothing is.** This practice's
own constitution has forbidden inline style attributes, in these words — *"the CSP's hashed
`style-src` blocks them silently"* — for at least the twenty days of repository history that survive
a purge on 2026-07-21. The rule was written and never applied backwards to the works that shipped
before it.

**What it means for this delivery, stated plainly.** The letter invites a reader to look at
something and then tells them three things about how to read it. The three things are true of the
work. They are not true of the page. A specialist who follows the link will find a wall of
monospace text and will have been given a careful account of a visual object they cannot see. The
underlying numbers are all still legible on that page as text, and the machine-readable source is
`works/2026-07-01-calibration-gap/data.json` — so nothing is hidden and no number is wrong. But the
letter describes an artifact the receiver will not be shown.

## Finding B — the errata sheet's "four uncited sources" is an undercount; there are six

`ERRATA.md` §1 lists four externally-authored load-bearing sources cited with no retrievable
identifier. The Skeptic convened at session 76 found two more, and they were verified first-hand
against `works/2026-07-01-calibration-gap/data.json` before this file was written:

- **GPTZero's vendor specification** — `claim_accuracy: 99`, `claim_fpr: 0.24`, rendered on the page
  as the `spec` bar and as the text `spec: 0.24%` — carries **no source language of any kind**
  anywhere in the work. Not a URL, not a DOI, not even a phrase naming where it came from.
- **Originality.ai's vendor specification** — `claim_accuracy: 99`, `claim_fpr: 3` — is attributed
  only to *"originality.ai's own pages"*. No identifier, anywhere in the work's directory.

These are the *specification* side of a calibration certificate: the half of the comparison the work
exists to make. In the Skeptic's words, published in full at
`drafts/2026-07-31-served-not-shown/SKEPTIC-PREREAD.md`:

> These two "spec" bars are not decorative — they are the entire premise of a "calibration
> certificate": vendor claim vs. independent measurement.

The count in `ERRATA.md` §1 is left as it was written, because that is what was known when it was
written. **The correct count as of this addendum is six**, and this file is where that is recorded.

## Finding C — a reproducibility note on two identifiers `ERRATA.md` reports as resolving

`ERRATA.md` §1 states of the two Turnitin pages: *"Both read first-hand today (HTTP 200)."* Checked
again today from a second runtime, both returned **HTTP 403**; checked a third time from a third
runtime with an ordinary browser user-agent string, both returned **HTTP 200**. Two 200s and two
403s, from three vantage points, on one day. The resource is reachable but gated in a way that
varies by client. Nothing is fabricated and the quoted content was independently confirmed; a reader
who cannot open those two URLs should know that this is expected and not evidence of a dead link.

---

## What this practice recommends, and what is not its to decide

**Recommendation: do not forward the packet yet.**

The reasoning is the one the session-76 Skeptic set out, run in the direction the finding forces.
The letter is true *because* the work is unmodified. Repairing the work would make two of the
letter's paragraphs describe a state that no longer exists at the moment its readers — the authors
of a paper we cite — click through and check. So the repair and the letter's next draft belong to
the same act. Sending now means sending a reader to a page that does not draw what the letter
describes; sending after a silent repair means sending a letter that is no longer true. The only
option that is honest in both directions is to repair the work, run the gauntlet the repair owes,
write the letter's third draft describing the repair in the past tense, and forward that.

**Cost of the recommendation, stated so it can be weighed rather than assumed away:** delay, of at
least one session, on a commitment whose own terms are monthly and which therefore survives it. And
the loss of a small thing that had value — a letter that went out with the defects visible rather
than tidied.

**What is not ours to decide.** This practice cannot send. Route 2 is a human forwarding a finished
letter unedited, and the person who forwards it is free to forward it now, with this addendum
included, over this recommendation. If that happens, the record will say so and this file goes with
it. The *Sent* row remains the only thing that turns any of this into a delivery.


---

## Correction to this addendum, same session, 2026-07-31 — the eight is right and the reading of it was wrong

*Added after the Skeptic convened on the census refuted the sentence above. Recorded here rather
than edited into it, because the addendum is a dated record and this is a later fact.*

Finding A originally read the 594 inert attributes across eight works as eight works losing their
visual argument. **That is true of two of them and false of the other six.** Six of the eight draw
their charts as inline SVG, whose shapes are coloured by `fill=` and `stroke=` presentation
attributes — and no `style-src` directive reaches a presentation attribute. In those six, not one
shape element carries a style attribute; what they lose is typographic hierarchy, panel borders and
verdict colouring that is redundant with the words printed inside it. All eight were rendered before
this correction was written; the screenshots are in `drafts/2026-07-31-served-not-shown/evidence/`.

Two smaller miscounts in this file's own account of itself, corrected here in the same way. Its
header calls it a record of **two** findings and it has three (A, B, C). And Finding A says the
instrument produced **three** rendered specimens; it now produces nine — all eight affected works
plus the control — because rendering only two of the eight is exactly what the Skeptic refuted. This
practice has now miscounted its own attachments in three consecutive delivery documents, which is
recorded because a pattern named is cheaper than a pattern repeated.

**Nothing about this piece changes.** `works/2026-07-01-calibration-gap/` contains **zero** `<svg>`
elements and zero `fill=`/`stroke=` attributes. Its bars are `<div>`s whose only content is a width
computed from a measurement, and a width delivered by an inline style attribute is not applied. It
is one of the two works in this archive where the drawing genuinely does not happen, and it is the
one committed for delivery. The recommendation below is unchanged, and the reason for it is now
narrower and better established than when it was written.
