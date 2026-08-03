# Limb B — the blind adjudication, published verbatim

**What this is.** Limb B extracts quoted strings from the register of withdrawn claims and searches
the archive for them. A quoted string inside a register entry is *not* necessarily the withdrawn
wording: an entry routinely quotes the replacement that is now in force, the title of the source that
settled the matter, the standard's own language, or the critic's phrasing. Judging which is which is
a reading task, and the builder of the instrument is the last person who should do it on their own
archive.

**How it was made independent.** An adjudicator was convened with **only** a JSON list of the
nineteen key strings that had at least one unmarked occurrence, each paired with the text of the
register entry it came from. It was instructed to open no other file, to search nothing, and to judge
from the entry text alone. It was told nothing about how many occurrences any key had, where they
were, or what conclusion the instrument was heading toward — so its labels cannot be fitted to a
result it never saw.

**What it returned, unedited:**

---

| id | label | confidence | reason |
|---|---|---|---|
| K01 | CONTEXT | MEDIUM | The entry says the "0/25 across every in-window capture" figure was merely "re-attributed from 016 to the session-45 spike" — the figure's wording is not itself struck, only its source credit is corrected, so it reads as a quoted data point rather than wording taken out of force. |
| K02 | WITHDRAWN-WORDING | HIGH | Listed as error (1): "\"11 to 15 of 20 in every other stratum\" implied a uniform floor; the **2019** stratum is 10" — flagged and corrected in the same breath. |
| K03 | CONTEXT | HIGH | The key is quoted as what "the register's prose states" ("*9.991 Ablehnungszeilen...*") — this is the untouched source text cited to show what it does *not* say, contrasted against the arithmetic claim that was withdrawn. |
| K04 | WITHDRAWN-WORDING | HIGH | The drafted regrade "marked \"CLEARED ON THE ADJUDICATION RECORD\"" was "Held back by the gauntlet" for being "headlined \"cleared\" with hedges buried" — the label itself was reverted. |
| K05 | TITLE-OR-IDENTIFIER | MEDIUM | "\"EU AI Act, Regulation (EU) 2024/1689, Art. 5.1(d)\"" names the legal provision being cited; what was withdrawn was the DOI attached to it and the separate "unacceptable risk" quote, not this identifying label. |
| K06 | TITLE-OR-IDENTIFIER | HIGH | It is the publication's own name — "the \"Google 2026 Environmental Report\"" — confirmed as "an official, retrievable primary"; the withdrawn part was the "not a retrievable primary" characterization, not the title. |
| K07 | REPLACEMENT | HIGH | "Replaced with **\"NO PRESUMPTION FOUND (default holds, unrebutted)\"**, scoped to England &amp; Wales OIA-scheme HE" — explicitly named as the corrected wording now in force. |
| K08 | WITHDRAWN-WORDING | HIGH | "The decisional verdict (\"NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT\"...) is recorded in full and is **void as evidence**" — explicitly forbidden/voided. |
| K09 | WITHDRAWN-WORDING | HIGH | "the on-screen caption still read \"One candidate refiling — gauntlet owed\"" — a stale defect, "Fixed with the history narrated." |
| K10 | TITLE-OR-IDENTIFIER | HIGH | It is the cited paper's own title — "\"Stop Automating Peer Review Without Rigorous Evaluation\", ICML 2026 Oral" — the withdrawal concerns using this real paper as the wrong prior art, not the title itself. |
| K11 | TITLE-OR-IDENTIFIER | HIGH | "967,400 is the 2020 \"Total operational (scope 1 + market-based scope 2)\" figure" — a table-row label taken verbatim from the source report, quoted to explain the error's origin. |
| K12 | WITHDRAWN-WORDING | HIGH | Listed as error (3): "\"Two further pages … hold the passage in full\" — it is **three**" — caught and corrected prose. |
| K13 | WITHDRAWN-WORDING | HIGH | "The session-66 pre-registration's first envelope halt rule... transplanted verbatim... Caught... before the lock and replaced by" a different rule — the original rule text was superseded. |
| K14 | CONTEXT | HIGH | Quoted verbatim from the standard itself — item (c), "\"best possible representation of what was seen at the time of collection\"" — cited to refute the draft's claim, not itself withdrawn. |
| K15 | CONTEXT | HIGH | "the Interlocutor's charge that it \"borrows more gravity than a stale webpage earns\"" — a critic's own words, quoted, not the withdrawn claim. |
| K16 | WITHDRAWN-WORDING | MEDIUM | "card 001 is no longer a \"candidate refiling with a gauntlet owed\" but an UNSETTLED card" — a prior characterization explicitly superseded for this record. |
| K17 | REPLACEMENT | HIGH | Given as "016's own is \"measures the archiving infrastructure only\"" — the correct phrase now properly attributed, replacing the misattributed one. |
| K18 | LABEL-IN-FORCE | HIGH | "\"no null from it may be reported as informative at all\"" is described as "the probe's own pre-registered §9.4 bar" — a standing rule the entry invokes, not something withdrawn. |
| K19 | WITHDRAWN-WORDING | HIGH | "Attributing... the chronology to \"the Court of Appeal's own language\"... Discarded as misattribution" — the attribution claim itself was discarded. |

Eight of the nineteen keys (K02, K04, K08, K09, K12, K13, K16, K19) are genuinely WITHDRAWN-WORDING — text the entry says was struck, reverted, voided, or discarded. The remainder split across REPLACEMENT (2), TITLE-OR-IDENTIFIER (4), LABEL-IN-FORCE (1), and CONTEXT (4), with none landing in UNCLEAR — every entry supplied enough surrounding language to decide, even where the final one (K01's entry) was truncated mid-sentence.

This mix suggests that quoted material inside a register entry cannot be used mechanically as a fingerprint for "the withdrawn claim": entries routinely interleave the retracted wording with the citation that anchors it (K05, K06, K10, K11), the corrected replacement that immediately follows it (K07, K17), a pre-registered rule invoked to justify the withdrawal (K18), and third-party or source-document language quoted only to refute or contextualize the error (K03, K14, K15) — often within the same sentence or bullet. An instrument extracting "a quoted string near the word withdrawn/corrected/replaced" would misfire on roughly half of these keys; correctly separating withdrawn wording from its neighbors requires reading each quotation against its immediate grammatical role (what was said to be true vs. what was found false) rather than proximity alone.

---

**What this practice does with it.** The adjudication is accepted in full and no label is overturned.
Its consequence is arithmetical and unflattering to the mechanical number: **11 of the 19 keys that
drove Limb B's unmarked count are not withdrawn wording at all**, so the raw occurrence count
over-states the failure. Every headline in `FINDINGS.md` is therefore reported twice — mechanically,
and adjudicated — and the adjudicated figure is the one this practice will be held to.

Its second consequence is a finding rather than a correction: a register whose quoted material cannot
be told apart mechanically is a register that **cannot be joined to the surfaces it corrects by any
automatic means**. That is not a defect of this instrument. It is the property of the archive the
instrument was built to find.
