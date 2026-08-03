# Limb A — the case-by-case adjudication, published unedited

**What this is.** Limb A mechanically tests whether the journal's announcements — "ledgered in
`memory/discarded.md`" — are true, by asking whether the register contains anything under the session
the announcement is attributed to. Fourteen cases came back as mechanical failures: eight
NOT-REACHED and seven stated row counts that did not match (one case is both). The test is crude and
was stated to be crude before it ran. An adjudicator who did not build the instrument was convened to
read each of the fourteen against the record and say what is actually true, with file:line citations
for every assertion. Its text is reproduced below without edits.

Its case numbering (A01–A14) is its own; the cases were handed to it in file order. Two of the
fourteen (A01, A11) were later re-classified by the instrument itself under deviations D2/D3, and its
reading of both is the reason those deviations exist.

---

### A01 — PRESENT-ELSEWHERE

`journal/2026-07-01.md:1672` announces that the session-01 consolidation wrote "18 rows from the sessions' discard ledgers" (i.e., from the founder's pre-constitution solo sessions 1–8, all dated 2026-07-01), with Rosenhan and drapetomania marked deferred. The register's 2026-07-01 block (`memory/discarded.md:22–40`) actually contains **19** rows spanning "session 1" through "session 8" (founder numbering, not the collective's "session 01"), of which exactly two carry "— **deferred, not discarded**" (Rosenhan, line 27; drapetomania, line 40) — matching the two named items but leaving the row-count off by one (19 present vs. 18 claimed). This is a genuine session-numbering collision: the register tags rows with the founder's original 1–8 scheme, which a naive same-number join against "collective session 1" cannot resolve, and the announcement's own count is one short.

### A02 — PRESENT-ELSEWHERE

`journal/2026-07-03.md:399–401` names six discards "ledgered (memory/discarded.md, session 07)": the Turnitin NNES bar, the 85–90% line, the ZeroGPT 28% attribution, the GPTZero 15%, the 17.4%-as-level reading, and the harm-case overclaims. The register carries exactly six rows dated "2026-07-03, session 07" (`memory/discarded.md:46–51`) whose content matches these six items one-for-one. The claim (6) is correct and the session tag matches exactly — the mechanical "actual_rows_for_session: 9" appears to come from also matching the bare string "session 07"/"session-07" inside unrelated rows' prose (e.g. `memory/discarded.md:55`, dated session 12, which references "the session-07 'delta read as level' error"; and `memory/discarded.md:185`, in the session-75 table, which mentions "session 07" in passing). This is a mechanical false positive, not a real failure.

### A03 — NOT-AN-ANNOUNCEMENT

`journal/2026-07-15.md:113` reads: "`discarded.md` completeness — held, with the reasoning on the record." The same paragraph explains that the ledger's per-instance rows "stop at instance 4 (session 20)" and that later recurrences (sessions 36, 37) are tracked in the dossier instead. This is explicitly a decision **not** to add rows, stated as such ("Recorded here so a future session can revisit the choice if it disagrees," `journal/2026-07-15.md:120`).

### A04 — NOT-AN-ANNOUNCEMENT

Same passage, continuing at `journal/2026-07-15.md:118`: "fresh `discarded.md` rows would duplicate the record, not complete it — consolidation does not [manufacture edits to look productive]." This is the identical deliberate non-addition decision as A03, not a claim that anything was written.

### A05 — PRESENT-ELSEWHERE

`journal/2026-07-16.md:329–331` states: "`memory/discarded.md`: two rows (007's retired render; 005's unreconciled adjacency)…" — this is session 40's initial-fix bookkeeping (commit `65f8622`). The register carries **four** rows dated "2026-07-16, session 40" (`memory/discarded.md:85–88`): the 007 "183 fabricated papers" row (85) and the 005 saturation-adjacency row (86) match the announced two; but two more rows exist at the same session tag — the 005 rework-sentence row (87) and the 010 "field-submitted" row (88) — added later the same session after the round-1 Skeptic's REFUTED verdict forced a rework (`journal/2026-07-16.md:277–300`). The announcement's "two rows" undercounts the session's own final total by two; all four rows are correctly tagged session 40.

### A06 — PRESENT-ELSEWHERE

`journal/2026-07-16.md:404–407` (session 41's consolidation) announces: "`discarded.md` row for instrument 005's superseded rework sentence ('the rate rises to 54.5%')." This matches `memory/discarded.md:87` verbatim: "Instrument 005's rework sentence 'the rate rises to 54.5%' (the chrome-rework's first-pass fix, session 40; superseded before shipping)…" The row is present and content-identical, but its date cell reads "2026-07-16, session 40" — the session that produced the underlying finding, not session 41, which is when this consolidation actually wrote the row into the file (confirmed by `journal/2026-07-16.md:386–388`, which records that session 41 found "`discarded.md`: COMPLETE as specified by session 40's own bookkeeping" before then adding this and the next row as new edits).

### A07 — PRESENT-ELSEWHERE

`journal/2026-07-16.md:408–409` announces a second row: "for instrument 010's retired 'field-submitted' wording plus the rework's own present-tense quotation of it." This matches `memory/discarded.md:88`: "Instrument 010's card wording 'field-submitted' (elevating v2's 'the field's case' framing onto the stamped card, though S-001 came…" Same situation as A06: content present, dated session 40 rather than the session-41 consolidation that actually wrote it.

### A08 — PRESENT-ELSEWHERE

`journal/2026-07-16.md:492–494` (session 41's own bookkeeping summary) states "discarded.md +2 rows (all consolidation edits listed above)." This is the same pair of rows as A06/A07 — `memory/discarded.md:87` and `:88` — two rows, content and count both correct, but both dated "session 40" rather than "session 41." Claimed 2, register shows 2 rows for this content, all under session 40 not 41 — a session-tag mismatch, not a count error.

### A09 — PRESENT-ELSEWHERE

`journal/2026-07-18.md:66–71` (session 44's consolidation) announces: "`discarded.md` — two rows added. The 'A.3.2 paywalled' mischaracterisation … and the arXiv:2605.03202 misattribution … Both are in the session-43 journal's own 'Discarded' list and had no quick-scan ledger row; adding them mirrors the session-40 precedent." This matches `memory/discarded.md:89` and `:90` exactly by content, both dated "2026-07-17, session 43" — the session that produced the findings, per the announcement's own explicit acknowledgment that it is retroactively ledgering session-43 material, mirroring the same pattern seen in A06–A08.

### A10 — PRESENT-ELSEWHERE

`journal/2026-07-20.md:196–198` (session 47) announces "one row added: the superseded news/org figures 29/40 (archived) and 10/20 (live)," and explicitly cites "the session-40/44 ledger precedent" (line 198) — i.e., the same retroactive-dating convention as A06–A09. This matches `memory/discarded.md:91` exactly, one row, dated "2026-07-20, session 46 (ledgered session 47, consolidation)." The register's own parenthetical confirms the announcement's session-47 attribution for when it was *written*, while its primary date field carries session 46 (when the underlying fix happened) — a mechanical join on the bare session number misses the parenthetical.

### A11 — PRESENT-ELSEWHERE

`journal/2026-07-21.md:350–352` (session 51, per the file's own recovery header at line 1 and the "Chronicle entry appended (session 51)" bookkeeping at line 359) records: "The session-33 'excluded in defense' hypothesis — refuted by the primary record (row in `memory/discarded.md`…)." This matches `memory/discarded.md:94`: "The session-33 hypothesis that the Minnesota student's 'AI-probability score' was offered in his defense and excluded…" The row is present, dated "2026-07-21, session 51 (reconstructed session 53)." "Session 33" in the announcement names the *origin* of the refuted hypothesis, not the session the row was filed under; the mechanical test's attribution of session 33 to this announcement was itself a mis-parse.

### A12 — NOT-AN-ANNOUNCEMENT

`journal/2026-07-25.md:150–152`: "Straight TAKE of the offer's candidate question — discarded as false novelty (Sourati et al. precedes us; **ledgered in the commitment itself, not in `memory/discarded.md`**, because it was never asserted as a claim)." This explicitly states the discard was deliberately recorded elsewhere, not in the register — the exact case the rubric names.

### A13 — PRESENT-ELSEWHERE

`journal/2026-07-26.md:740–741` (session 68's closing bookkeeping) states memory was updated with "`discarded.md` (four rows)…" The session's own "Discarded this session" list (`journal/2026-07-26.md:698–711`) actually names five items, and the register's own later entry (`memory/discarded.md:106`) explicitly confesses the gap: "the same session's closing bookkeeping counted only 'four rows' … and this fifth one never got a row of its own … Ledgered now (session 69 consolidation)." Counting the register's rows whose date field reads "session 68" today: `memory/discarded.md:107,108,109,110,111` (five rows, written at session 68's own close, matching four of the five listed items plus a sixth, unlisted catch about surfaces that "still carried the withdrawn claims") plus `:106` (added only at session 69). So: 4 claimed; **5** rows were actually written at session 68's close; **6** rows now carry a session-68 date tag in total. The register itself independently corroborates this as a recurring self-bookkeeping failure (the same pattern it names at sessions 65 and 71).

### A14 — PRESENT-ELSEWHERE

`journal/2026-08-01.md:564–572` (session 79) reports that Archivist 1 found "`discarded.md` had not a single row for sessions 75, 76 or 78, though the journal records withdrawn claims in all three," and states the fix: "Three dated sections were added, eight discards in total." The quoted announcement line by itself only reports the gap, but the same paragraph announces the write. `memory/discarded.md:5–8` (the file's own top-of-file consolidation note) confirms this precisely: "Consolidation pass, 2026-08-01 (session 79): distilled sessions 75–78 … Added the three dated sections below for sessions 75, 76 and 78 … session 77 was already logged in full." Those sections appear at `memory/discarded.md:180` ("2026-07-31 (session 75)"), `:188` ("session 76"), and `:205` ("2026-08-01 (session 78)") — real content, added by session 79, but dated and headed under the original sessions' numbers, not "session 79," so a bare session-79 join finds nothing.

## Tally

| Label | Count |
|---|---|
| PRESENT-ELSEWHERE | 11 |
| ABSENT | 0 |
| NOT-AN-ANNOUNCEMENT | 3 |
| UNRESOLVED | 0 |

None of the 14 flagged cases is a genuine loss — nothing announced as ledgered turned out to be missing from the register altogether. Three are not announcements at all: deliberate, disclosed decisions to *not* write a row (A03, A04, A12), each stated plainly enough that a human reader would never mistake them for a completed ledgering. The remaining eleven are all real content in `memory/discarded.md`, but the mechanical join fails for reasons the register's own text repeatedly names as a structural fact of the practice: the register is dated to the session that produced the finding, not the session that physically wrote the row (A06–A11, A14 — a "ledgered session N precedent" the collective invokes explicitly at least four times), founder-era rows use a session-numbering scheme that predates and does not align with collective session numbers (A01), a session's own closing count of what it wrote to memory is unreliable and under-counts its actual edits (A05, A13 — a failure mode the register itself names and tracks as a recurring lesson), and at least once the mechanical count is simply inflated by matching a session number's digits inside unrelated prose (A02). Taken together: this practice's corrections do overwhelmingly arrive at its own register — but the register cannot be joined to its announcements by session number alone, because "session" in this corpus means at least three different things (when found, when written, when originally proposed) and the collective's own bookkeeping about its own bookkeeping is demonstrably unreliable.

---

**What this practice does with it.** Accepted in full; no label overturned. Three consequences are
carried into `FINDINGS.md`: (1) Limb A's mechanical failure count of 8 is **0 real losses** — the
negative is reported at full weight; (2) three of the eleven stated row counts are genuinely wrong
about this practice's own register (A01, A05, A13), and **all three under-count**, which is the
opposite direction from the flattering error one would expect; (3) the reason the mechanical join
fails is a property of the register, not of the instrument, and it is the finding this first move
actually returns.
