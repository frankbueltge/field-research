# Pilot counter A — published unedited

*Convened by session 138, 2026-08-29, under `PREREGISTRATION-138C.md`. Given the four drawn files as
text and the counting criterion of `HAND-AUDIT-137.md` §3 verbatim; forbidden to open the repository
or run anything; **not told that a second counter existed**, what the result gates, or what this
practice hoped for. Reproduced below exactly as returned.*

---

# Independent Count — Primary Enumerations

Method note: for each document I looked for the one repeated, self-consistent delimiter family the report itself uses to lay out what it found/answered, distinguishing it from (a) structural section headers, (b) remedy/condition lists, and (c) any disposition/verification material added by a second party checking the report, where the document's own framing marks that material as separate from "the report" proper (FILE-1 and FILE-4 both do this explicitly).

---

## FILE-1

**COUNT: 5**

**DELIMITER LINES:**

1. **The hour is not a loose habit — it is the just-written, specific binding term.** `CONDITIONS-129.md:71`: "**The daily instrument keeps running.** Day 10 closed this session; day 11 is due at 03:41:00Z." That sentence was written three hours before the current session opened, by a session that had just built `run_day10_close.sh`, which computes and records "the third one-day interval in a row" at `run_day10.sh:11-12` ("Launched at 03:41:00Z, exactly 1.0000 days after the last completed run's start second"). The people who wrote "day 11 is due at 03:41:00Z" knew exactly what they meant by it: not "sometime Friday," a specific second, chosen to preserve a 1.0000-day cadence that had just locked in for four runs running (`ledger/run-2026-08-18T0341Z.json` through `run-2026-08-21T0341Z.json`, all at `03:41:00Z`).
2. **This exact question — "does the stop's exception cover a session doing what's convenient for itself instead of what the license says" — was already litigated twice, against the conductor's position both times.** Session 129 refused to let the adversary draft an unshipped note "because a stop a later session may reinterpret when it sees a good enough reason is not a stop" (`journal/2026-08-21.md`, landing note). Session 130's adversary then applied the identical test to a public window and returned **VIOLATES**, for the identical structural reason: "**A stop under which a private draft is forbidden and a public web page is permitted is not a stop with a principle in it; it is a stop with a preference in it**" (`notes/2026-08-21-window-compliance/INTERLOCUTOR-130.md`, quoted at `journal/2026-08-21.md`). Re-anchor the hour because 03:41Z is inconvenient for this session, and you have manufactured exactly that asymmetry: "the instrument keeps running" is read as forbidding a hole but permitting a redesign, which is a preference (this session's schedule), not a principle.
3. **The house already has a documented, precedented answer for "the hour is not in this session's reach," and it is not to move the hour.** Session 130 opened at 14:30Z, three hours after 03:41Z had already passed, and wrote plainly: "Day 11 is due at 03:41:00Z, which is not in this session's reach" (`journal/2026-08-21.md`, session 130 opening record), and at landing: "Day 11 of the instrument is due at 03:41:00Z and no part of it is reserved by this session" (same file, landing note). That is the precedent on this exact fact pattern from the immediately preceding session: record non-reach, reserve nothing, leave it for whichever session can actually reach 03:41:00Z. The conductor is proposing to do the opposite of what the last session that faced this identical problem did.
4. **Steelmanning the FOR case and it still fails.** The strongest argument for the conductor is that a hole is unrecoverable. But this record already contains a hole — 2026-08-17 has no run file at all (`ledger/run-*.json` listing has no 08-17 entry) — and the practice's own tooling treats that calmly and honestly: "10 measurement days, one hole" and `consecutive_daily` **false** (`journal/2026-08-21.md`, "Day 10 closed" paragraph); `run_day10.sh:12`, "if this session ends before it closes, day 10 is a hole and this comment is not a substitute for the data." A hole is a contemplated, survivable, honestly-recordable state of this instrument — not a catastrophe that licenses redesign to avoid it. And the "no pre-registered test is scored" fact (`run_day10.sh:7-9`, `run_day10_close.sh:7-8`) cuts against the conductor too: if nothing is scored on day 11 either way, there is no measurement cost to letting a later session take it at the correct hour, and the only thing the re-anchor actually buys is convenience for this session — the exact motive session 129 and 130 both ruled out.
5. **On the "fixed hour was already refuted" point — it helps the conductor far less than it looks.** `CONDITIONS-128.md:52` (finding 4) does show start times of "11:24, 03:40, 04:27, 03:43, 03:37, 03:37, 03:41, 03:41, 03:41" and calls the "same hour every day" claim refuted. But read as a time series that refutation is early-series noise (day 1's 11:24, then a chaotic 03:40/04:27/03:43 band) that had, by the time of days 8-10, **converged and locked** to exactly 03:41:00Z for four consecutive runs — confirmed above. CONDITIONS-129 was written *after* that convergence and named the locked hour specifically. Citing the old chaos to justify reintroducing a new deviation gets the trajectory backwards: the record's own history is of an instrument that stabilized, and the conductor's move is the first hour-deviation since it did.

*(The counter returned each delimiter as the item's complete paragraph, copied
character-for-character from the source document. The five paragraphs above are reproduced in full,
verified line by line against `INTERLOCUTOR-131.md` lines 20, 22, 24, 26 and 28 — the counter's
report is not abridged anywhere in this file.)*

**REJECTED:** (a) The "Two errors of the report" list (2 items, same "N. **bold**" markdown syntax) — this lives in the *disposition* section, which the document's own frontmatter says is separate checking material added afterward ("does not touch the text above"), not part of "the report, verbatim." (b) The "Binding on this session" list (3 items) — explicitly a set of resulting rules/conditions, excluded by the criterion's own instruction. (c) Q2's answer, split into **(a)** and **(b)** (2 items) — a different delimiter family (bold parenthetical letters, not numerals), smaller, and answers a secondary question rather than the headline Q1 verdict.

**CONFIDENCE: MEDIUM.** The document contains three numbered/lettered lists inside "the report, verbatim" and its disposition, all using superficially similar syntax. I judged the 5-item Reasoning list primary because it is the largest, is explicitly what the verdict on the headline question (Q1) rests on, and sits inside the report proper rather than in the added disposition. Alternative count: 2 (if the primary enumeration is instead read as the two-part Q2 answer, (a)/(b)). What would settle it: an explicit statement in the document naming one list as "the findings" — none is given.

---

## FILE-2

**COUNT: 8**

**DELIMITER LINES:**

1. ### 1. Independent re-implementation — the headline arithmetic reproduces exactly
2. ### 2. The exclusions — I recomputed under four different rules; none moves the conclusion by more than a rounding error
3. ### 3. The dating rule — holds under an external check, but the window arithmetic it feeds is a genuine problem the document has already half-fixed
4. ### 4. Model dependence — I fit three more models from scratch; the power conclusion does not depend on the Weibull choice
5. ### 5. Arithmetic and framing — the LR/"decisive" language is a retrospective reframing, and it should be named as one
6. ### 6. Self-serving framing — checked, and partly substantiated, but the document is unusually forthright about its own temptation
7. ### 7. Hunt for the seventh instance of the arc's named signature error
8. ### 8. Quotation check, CONCEPT.md §5a and any INTERLOCUTOR-2.md material

**REJECTED:** (a) The 5 numbered "Numbered, concrete conditions" under "Verdict on §(a)" — explicitly a remedies/conditions list, excluded by the criterion. (b) The exclusion-sensitivity table (5 rows, §2) — a table nested inside item 2, not the document-level enumeration. (c) The three bolded rhetorical questions in §(b) ("So what?", "Is this slop?", "Would a serious critic tear it apart?") — not a consistent numbered/lettered delimiter family, and secondary ("hostile critique") rather than the primary investigative enumeration.

**CONFIDENCE: HIGH.** The `### N. Title` family is unambiguous, spans the whole investigative body of the report, and matches the criterion's own worked example almost exactly.

---

## FILE-3

**COUNT: 6**

**DELIMITER LINES:**

1. ## 1. The single most important thing this directory tells you
2. ## 2. What is it about?
3. ## 3. Who is it for, and who is it from?
4. ## 4. What would you not trust, or want to check yourself?
5. ## 5. Where, if anywhere, did you stop reading or want to stop?
6. ## 6. Anything you noticed that nobody asked you about

**REJECTED:** The bullet list under item 4 (5 sub-bullets) — nested inside one enumerated item, not a document-level family. No other numbered/lettered family competes; the document is structured entirely around these six numbered question-headings.

**CONFIDENCE: HIGH.** This is the cleanest case: six `## N. <question>` headings, each answered in the section beneath it, with no competing enumeration anywhere in the document. This matches the criterion's own clarification almost verbatim ("an answer to a question like 'what is this about?'").

---

## FILE-4

**COUNT: 14**

**DELIMITER LINES:**

1. **A1.** 11 completed run files (glob `run-*.json` minus `.partial`, in `.../drafts/2026-08-11-the-arm-that-was-missing/ledger/`):
2. **A2.** Runs with `requested`=3869: n=10. min=6221.5s, median=6528.5s (avg of 6518.1 and 6538.9), max=6827.3s.
3. **A3.** Consecutive start-to-start intervals, chronological:
4. **B1.** 97 session headings matching `# Session <n> — <date>` across 36 journal files (2026-08-22.md excluded, see note above).
5. **B2.** 7 sessions state their own opening time in their own block:
6. **B3.** 7 of 97.
7. **C1.** Dates with both a completed run and a session stating an opening time: 2026-08-16, 2026-08-18, 2026-08-19, 2026-08-20, 2026-08-21 (2026-08-17 has a stating session but no completed run — excluded).
8. **C2.** Lags (session-opening → run-start), one row per date, using the primary `run-2026-08-16T0337Z.json` for 08-16: 62s, 305s, 360s, 275s. → **min 62s, median 290s, max 360s. 0 of 4 exceed 600s.**
9. **C3.** Session-opening → run-end (floor on session lifetime), same 4 dates: 6732s, 6810s, 6699s, 6497s.
10. **D1.** 00:23:16Z → 03:41:00Z = **11,864 s = 3h 17m 44s**.
11. **D2.** 11,864 + 6528.5 (A2 median) = **18,392.5 s ≈ 5h 6m 32.5s**.
12. **D3.** 18,392.5 / 6810 (largest C3 value) = **≈ 2.7008**.
13. **E1. CONFIRMED.** `ledger/run-2026-08-17T0337Z.json.partial` exists (115,918 bytes, confirmed by direct directory listing). `RETRY-2026-08-18.md:13-15`: "It replaces the run session 125 launched on 2026-08-17 and did not finish. That run stopped at 600 of 3,869 and is not a measurement... it remains in the ledger as a `.partial` and `window_status.py` reports it as the window's one hole." `ERRATA-126.md:35-46`: "There is no `ledger/run-2026-08-17T0337Z.json`... `requested: 600`, `planned: 3869`... The run was started; it was never taken."
14. **E2. CONFIRMED.** `journal/2026-08-16.md:177-181`: "Session 122 scheduled day 6 of the window for 03:37:40Z and ended before it fired... This session [123] opened at 03:36:38Z. `run_day6.sh` was launched unchanged at 03:36:47Z... started at 03:37:40Z." Restated at `journal/2026-08-16.md:263`: "Session 122 scheduled it for 03:37:40Z and ended first. We opened at 03:36:38Z and started the unchanged probe at 03:37:40Z." Session 123 is explicitly headed "second session of the same date" (`journal/2026-08-16.md:168`).

**REJECTED:** (a) The `## A —` … `## F —` section headers (6) — structural chapters, explicitly excluded by the criterion. (b) The "Fragile / ambiguous points" list under `## F` (5 items, plain `1.` `2.` … syntax, not the bold letter-prefixed `**X#.**` family used by A–E) — a caveats list, and a different delimiter family from A1–E2. (c) The 5-row disposition table (`# | finding | reproduced | disposition`) — this is compelling as an alternative (its column is literally labeled "finding"), but it is generated by a second party ("this practice") checking the Verifier's report after the fact; the document's own frontmatter separates "the report, verbatim" from "the disposition follows the report and does not touch it," and the task asks for the report's *own* enumeration.

**CONFIDENCE: MEDIUM.** A1–E2 is a real, consistent 14-member delimiter family and is what the report itself computed and presented as its output. But the 5-row disposition table is a live alternative reading, since it is literally headed "finding" and is where the document's stated verification purpose cashes out. Alternative count: 5. What would settle it: whether "the report" in the task's sense is meant to include the disposition appendix or only the material the document itself calls "the report, verbatim" / "Verification Report" — the document's own labeling favors excluding the disposition, which is why I did.

---

## Summary Table

| | FILE-1 | FILE-2 | FILE-3 | FILE-4 |
|---|---|---|---|---|
| **COUNT** | 5 | 8 | 6 | 14 |
| **CONFIDENCE** | MEDIUM | HIGH | HIGH | MEDIUM |
| **Alternative** | 2 (Q2 a/b) | — | — | 5 (disposition table rows) |
