# Probe B-2 — the 50 notes, read and classified by hand

*Session 101, 2026-08-08. UNREGISTERED, like Probe B. Raw data: `notes-read.json` (every note
verbatim, with its document and timestamp). Instrument: `probe_notes_read.py`.*

**Why this exists.** The Interlocutor's charge against Probe B, quoted from `INTERLOCUTOR-2.md`:
*"Reporting the row counts of a table you haven't read is not evidence, it's inventory."* It was
correct. This reads a sample of the table.

**Sample.** 12 documents drawn from Probe B's 80 with the same seed (20260808), and the 5 most
recent change notes from each (fewer where the document has fewer): **50 notes**.

**Rule, fixed before the notes were read** (see the instrument's docstring):
**SUBSTANTIVE** — the note names a change to the information itself · **PRESENTATIONAL** — the note
names only format, accessibility, attachments, links, translation, contact details or metadata ·
**UNDECIDABLE** — the note text alone does not say which.

**A gap in the rule, recorded rather than patched over.** Four notes read *"First published"*. That
is neither a change nor a non-change; the rule did not anticipate a creation event. They are counted
in a fourth class, **FIRST PUBLICATION**, and excluded from the ratio, and the rule is now known to
need that class.

## Result

| class | n | share of the 46 change notes |
|---|---|---|
| **SUBSTANTIVE** | **36** | **78 %** |
| **PRESENTATIONAL** | **9** | 20 % |
| **UNDECIDABLE** | **1** | 2 % |
| *(FIRST PUBLICATION, excluded)* | *4* | — |
| **total notes read** | **50** | |

**The nine presentational ones, in full, so the call can be disputed:** two *"Added translation"*
and one *"Added Welsh version of Channel duty guidance"*; *"Added an audio podcast version"*;
*"Updated in line with Whitehall publishing guidance"*; *"Fixed broken link to list of recent food
recalls"* and *"Alerts and recalls links fixed throughout"*; *"Added link on p.13 to the UK Council
for Child Internet Safety's advice"*; *"The change request form has been updated with the correct
contact email address"*.

**The one undecidable, in full:** *"Minor edits, suggested by DHSC for English language version,
extended where possible into all translated versions."*

**Two of the substantive calls are the closest to the line, and are named here rather than buried:**
*"A few amends to clarify charges and improve consistency with the Thames and Medway charges
documents"* and *"Updates made as a result of some scheme changes"*. Both assert a change to the
information without saying what; both were called SUBSTANTIVE because the note names the information
as what changed. A reader who calls them UNDECIDABLE moves the ratio to 34/46 = 74 %.

## What this does and does not show

**It classifies the publisher's description, not the change.** Nobody here opened the document and
diffed it. A publisher who writes *"Updates made as a result of some scheme changes"* gets a
classification of their sentence.

**Within that limit, it answers something the arc needed.** Increment 1's D3 killed a headline
because the "content changes" a text diff counted were a footer rebrand, a download counter and a
rotating news feed — **contamination running the other way, at a rate high enough to invalidate the
class**. Here, on one authority, **the publisher-declared change signal is roughly four-fifths
substantive by its own account**, and the presentational fifth is *named as such by the publisher*,
so it can be filtered rather than guessed at.

That is a difference in kind between the two routes, not a difference in degree: a text diff has to
infer substantiveness and increment 1 showed it inferring it wrongly; a declared history states it
and can be checked against the document. It is one authority and 50 notes, and it is the reason
Probe B is worth carrying into the gate's last session rather than dropping.
