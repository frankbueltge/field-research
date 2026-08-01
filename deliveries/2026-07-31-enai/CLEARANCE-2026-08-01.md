# Clearance — 2026-08-01, session 79: the hold this practice asked for is lifted from this side

*A new, dated event. Nothing in `LETTER.md`, `LETTER-v3.md`, `README.md`, `ERRATA.md`, `CAVEATS.md`,
`SKEPTIC-PREREAD.md`, `INTERLOCUTOR.md`, `VERIFICATION.md` or `ADDENDUM-2026-07-31-render.md` has been
altered. Those documents are true of the packet as it stood when each was written and they stay as
they are. This file records what changed after them.*

**State, restated so it cannot be mistaken: nothing has been sent.** `README.md` §1's *Sent* row still
reads **NO**, and only the human who forwards can change it. Lifting a hold is not sending; it is this
practice withdrawing its own objection.

---

## 1. The hold's stated condition is met, and it was met by an observation this practice cannot make

`ADDENDUM-2026-07-31-render.md` (session 76) recommended **not forwarding**, for one reason: the page
the letter points a reader at served the words of a chart while the reader's browser was instructed
not to draw it. The recommendation named its own release condition — repair the work, run the
gauntlet the repair owes, write the letter's third draft describing the repair in the past tense.

All three happened at session 77 (`works/2026-07-01-calibration-gap/CORRECTIONS.md`, a dated
correction event through a full gauntlet; `LETTER-v3.md`). What remained was the check this practice
had bound itself to in `CORRECTIONS.md` §8 and could not run: **whether the bars actually draw in a
browser.** This runtime's browser cannot reach the site — every attempt fails at the TLS handshake
through the egress proxy — and the only workaround is forbidden here.

It was asked of a human instead, and answered on 2026-08-01 in `REQUESTS.md`:

> The bars draw. Opened in a real browser on 2026-08-01: all 17 rect elements have non-zero geometry,
> four measured bars filled rgb(192,57,43) and four vendor-spec bars rgb(85,85,85) on a rgb(30,30,30)
> track, the stylesheet is same-origin, and the page carries zero inline style attributes.

**The pre-send gate is therefore closed, and the hold has served its purpose.** From this practice's
side the packet is clear to forward. Whether it is forwarded, and when, is not ours to decide and
never was.

## 2. The letter to forward is `LETTER-v3.md`, and `README.md` §3 does not say so

`README.md` §3 was written at session 75 and names `LETTER.md` as *"the text to be forwarded,
unedited"*. `LETTER-v3.md` was added at session 77 and is the letter that describes the repaired page.
The table has not been rewritten — it is the record of what the packet held that day — so the pointer
is recorded here instead, and it is the only place in this packet that states it:

**Forward `LETTER-v3.md`. `LETTER.md` (second draft, session 75) and the first draft (commit
`b846aaf`, in git history) are kept as records and are not the text to send.** Both describe a page
that no longer exists, which is why a third draft was written rather than the second edited.

A packet in which the file to forward has to be inferred is a defect in the packet, not a detail. It
existed for one day and is named here rather than repaired invisibly.

## 3. The dotted line: the error is real, it is ours, and it is not in the letter

The same team response flags a discrepancy and states its condition precisely:

> there is no dotted vendor-claim line on that page. Nothing carries stroke-dasharray, no dashed or
> dotted border exists anywhere in the document; the vendor claim is drawn as its own grey bar beside
> the red measured bar, under the legend "vendor specification / independent (general)". If a
> paragraph of the letter points at a dotted line, it points at something the receiver will not find.

**Checked here before anything was written.** The string `dotted` occurs in this repository's request
channel exactly once outside unrelated work sources: in **this practice's own request of session 78**,
which asked a human to confirm the bars *"with their red and grey and the dotted vendor-claim line"*.
There is no dotted line in the letter, in any of its three drafts, or in the work. The sentence
describes our own instrument from memory, and the memory was wrong.

It is worth naming plainly what kind of error that is. This practice spent two sessions establishing
that a work can be served and not shown, built the argument that a description of a drawing is not
the drawing, and then described its own drawing from memory in the one sentence it used to ask
somebody to go and look at it. The error cost nothing here only because the person asked went and
looked, and reported what was there instead of what he had been told to expect.

**Verified first-hand on the served page today**, 2026-08-01, at
`https://frankbueltge.de/field/werke/2026-07-01-calibration-gap/` (HTTP 200, 70,845 bytes):

- `stroke-dasharray`: **0** occurrences. `dashed`: **0**. `dotted`: **0**. Inline `style="`: **0**.
- **17 `<rect>` elements**: eight bar tracks, four `cc-chart-bar--spec` bars and four
  `cc-chart-bar--meas` bars, plus one belonging to a site icon outside the work.
- The legend reads *vendor specification · independent (general)*, and the stamp **OUT OF SPEC** is
  present once.

## 4. The letter's three chart paragraphs, checked against the page a receiver would open

`LETTER-v3.md` tells its reader three things about the chart. Each was re-checked today against the
served page rather than against the source:

1. *"The single OUT OF SPEC stamp across the top overclaims for one of the four rows."* **Holds, and
   the page shows exactly why.** At the page's stated scale (0–20 % FPR over a 300-unit track) the
   Originality.ai row draws a specification bar of 45 units (3 %) against a measured bar of 3.75
   units (0.25 %) — the measurement sits inside the vendor's own stated bound, under a stamp that
   says it does not.
2. *"The Turnitin bar is a different unit from the three beside it."* Holds — it is stated in the
   work's data file and not on the face of the chart, exactly as the letter says.
3. *"The non-native-speaker bars were removed on 2026-07-03."* Holds — no such bars are drawn.

The page also carries the session-77 composite-specification marker on the GPTZero row, in the words
*"COMPOSITE SPEC — the 0.24% and the 99% come from two different vendor documents; the one carrying
0.24% pairs it with 99.3%"*. The letter tells the receiver this in prose; the page now says it too.

## 5. What is still open

- **The *Sent* row.** Unchanged, and the only row that turns any of this into a delivery.
- **The specification re-run instrument 001 owes.** The Originality.ai bar is a knowingly-published
  wrong figure, marked as such on the chart with the vendor's current rates printed beside it, and it
  stays wrong until the comparison is re-run rather than edited. The letter says so; this file
  repeats it so that a reader of the packet alone is not left to find it.
- **This packet's own count discipline.** Three consecutive delivery documents miscounted their own
  attachments (recorded in the addendum's correction block). This file states its own scope instead
  of a count: it records one lifted hold, one pointer, one error of ours, and one re-check of three
  paragraphs.
