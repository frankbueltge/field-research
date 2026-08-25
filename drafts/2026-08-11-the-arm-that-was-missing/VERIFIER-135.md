# Verifier 135 — published unedited

*Session 135, 2026-08-25. Convened on `INCREMENT-23.md` and its two JSON artifacts at commit
`0c5004c`, per `PREREGISTRATION-135.md` §5, with the reason stated in advance: Q1 is arithmetic
carried by hand over dates read out of four documents, and this practice has had a hand-carried
figure found wrong against a machine-written artifact beside it in three consecutive sessions.*

**Verdict: PASS WITH FINDINGS — 6 blocking.** Four accepted in full, one accepted with its count
corrected, **and one REFUTED** — finding 10, where reproducing the charge found a different and real
defect running the opposite way (`ERRATA-135.md` E54). Dispositions: `CONDITIONS-135.md`.

**The verdict is good only for `0c5004c`, which no longer exists.** Nothing below is edited.

---

# Verifier Report — INCREMENT-23.md (commit `0c5004c`)

*Checked against sources only, independent of the increment's own reasoning. State reviewed: the five pinned files at commit `0c5004c`. Confirmed via `git diff 0c5004c HEAD -- PROTOCOL.md CONDITIONS-128.md chronicle.json PREREGISTRATION-135.md stop-clock-135.json stop-licence-135.json stop_clock.py stop_licence.py deliveries/2026-07-31-enai/packet.json` (empty — these are unchanged since 0c5004c) and `git show 0c5004c:.../INCREMENT-23.md` (211 lines, matches what was reviewed below) that the working tree has since moved past this commit (HEAD is now `976341d`); everything below is checked against the pinned `0c5004c` text, not the current file.*

## Q1 — the clock

**1. Q1 arithmetic reproduces exactly** — NON-BLOCKING (PASS)
Recomputed by hand from the inputs table: reading 2026‑09‑05 − 7 = 2026‑08‑29 (D_guaranteed); D_possible = 2026‑09‑05; earliest stop-permitted date = 2026‑09‑05 (exclusive "before"); gap = 7 days; today 2026‑08‑25 → D_guaranteed is 4 days away; today → reading is 11 days. All match `stop-clock-135.json`'s `derived` block digit for digit.

**2. Q1 input quotes are verbatim** — NON-BLOCKING (PASS)
Checked `PROTOCOL.md` §"The reading of 2026-09-05" ("The architect reads the four-week review and the first investigation together on **2026-09-05**"), §"Leaving the house" ("sent or withheld with a dated reason within seven days" and "`status` is yours as far as `prepared` or `withheld`; `sent` is the architect's alone"), and `CONDITIONS-128.md` §"Binding on the next session" ("No repair pass, no tenth gauntlet, no packet from this arc before 2026-09-05"). All quotes in `stop_clock.py`/`PREREGISTRATION-135.md`/`INCREMENT-23.md` reproduce these exactly (only markdown bold vs. plain, and em-dash vs. hyphen, stripped). Also confirmed item 1 of `CONDITIONS-131.md` through `-134.md` all leave "before 2026-09-05" unchanged.

## Q2 — the licence

**3. Population is exactly {129–134}** — NON-BLOCKING (PASS)
`python3` over `chronicle.json`: sessions 127–134 have dates 08‑19, 08‑20, 08‑21, 08‑21, 08‑22, 08‑22, 08‑23, 08‑24 — no gaps, population strictly between 128 and 135 is exactly six entries.

**4. `move_quoted` fields are verbatim, not paraphrase** — NON-BLOCKING (PASS)
Printed `e["move"]` for sessions 129–134 directly from `chronicle.json` and diffed against `stop-licence-135.json`'s `move_quoted` — byte-for-byte identical for all six rows.

**5. Table and artifact counts match** — NON-BLOCKING (PASS)
OUTWARD 1 / INWARD 4 / INSTRUMENT 1 in `INCREMENT-23.md` §2 matches `stop-licence-135.json`'s `counts`.

**6. Session-129 quote in §2, and the `CONDITIONS-128.md` item-2 quote** — NON-BLOCKING (PASS)
Both are verbatim substrings of chronicle.json / CONDITIONS-128.md (the §2 quote is a truncated-but-unaltered prefix ending cleanly at "to its last line.").

## Novelty claim

**7. `grep -rn "2026-08-29" .` before `df54cc0` returns nothing** — NON-BLOCKING (PASS)
`git grep -n "2026-08-29" 03d10c6` → no matches (exit 1). Also swept the full history (`git rev-list --all`) — the string first appears at `df54cc0`. Claim is true, and true even more broadly than stated.

**8. Substance not stated elsewhere in other words** — NON-BLOCKING (PASS)
Searched "seven days", "prepared", "post office" in `POST-MORTEM.md`, `REQUESTS.md`, `WORKBOARD.md`, `journal/2026-08-2*.md`. Found only generic restatements of the stop ("no packet is prepared… before the reading of 2026-09-05") and day-counts to the reading ("Fourteen days to the reading… nothing has left"). No prior text derives a 7‑days‑before‑the‑reading deadline. Novelty claim holds.

## Post office

**9. ENAI and Atelier quotes are verbatim** — NON-BLOCKING (PASS)
Fetched `https://frankbueltge.de/post/` (WebFetch got 403; fell back to web research per `PROTOCOL.md`'s tool-fallback rule, which succeeded). Live page: `field · lies open for collection · as of 2026-08-01` … `"Not sent: that row stays NO until a date can be entered."` and `atelier · in preparation · as of 2026-08-03` — both verbatim. `deliveries/2026-07-31-enai/packet.json` confirms `"status": "prepared"`, `"as_of": "2026-08-01"`.

**10. "Two of the Studio's (as of 2026-08-15 and 2026-07-31)" is wrong** — BLOCKING
The live ledger's "Outgoing" section has exactly **one** `studio` entry: *NO PART*, `lies open for collection · as of 2026-07-31`. The second entry the increment attributes to the Studio is actually labelled `plenum` (a cross-practice decision involving the Studio, the Field and the Atelier jointly — "The plenum's answer to the world-contact seed"), and it is dated `as of 2026-08-05`, not 2026-08-15. No `studio … as of 2026-08-15` entry exists anywhere on the page. This is a misattribution of source (plenum → "Studio") **and** a date error (08‑05 → 08‑15), and it propagated verbatim into the actual request filed at `REQUESTS.md` ("2026-08-25 — Request…", which repeats "two of the Studio's (2026-08-15, 2026-07-31)").

**11. "24 days" and the 2026-08-08 bind-date, no-retroactivity claim** — NON-BLOCKING (PASS)
2026‑08‑01 → 2026‑08‑25 = 24 days, correct. `PROTOCOL.md` header: "Decided and drafted by the architect… 2026-08-08" — a week after the packet's `as_of`. §"Leaving the house" contains no language about packets already open when the bind landed. Claim holds.

## Day 13 / Day 14

**12. Ledger state for 2026-08-24** — NON-BLOCKING (PASS)
`ls -la ledger/` at `0c5004c`: only `run-2026-08-24T0341Z.json.partial`, **212,692 bytes** exactly, no completed `run-2026-08-24T0341Z.json`. Matches.

**13. Comparison day / interval** — NON-BLOCKING (PASS)
Last completed run is `run-2026-08-23T0341Z.json`; 2026‑08‑23 → 2026‑08‑25 = 2.0000 days. Matches.

**14. "The six-in-a-row streak of one-day intervals ends here" is wrong — it is five** — BLOCKING
`DAY12-2026-08-23.md` (the day-12 close, dated before this session and generated from `interval-metrics-133.json`): *"Interval 1.0000 days from day 11's start second — the **fifth** one-day interval in a row."* The streak visible in the completed ledger runs at the time this increment was written is five, not six. (The working tree has since self-corrected this in place at commit `ae935ce`/`ERRATA-135.md` E50, which independently confirms this finding and traces the "six" to an uncompleted script's forecast comment — but at `0c5004c`, the reviewed state, the claim was wrong.)

**15. "Day 14 fired at 03:40:59Z" — mislabelled; it is Day 13** — BLOCKING
`interval-metrics-133.json`: `"n_measurement_days": 12`, under the stated rule "a `.partial` is never a run; a day counts only if a non-partial run file exists." Since 2026‑08‑24 produced no completed run, the ledger still stands at 12 measurement days going into this session — today's run, once complete, would be measurement day 13 (a second attempt), not day 14. The numeric facts themselves are correct — `day14-stderr.txt` at `0c5004c` does show `start 2026-08-25T03:40:59Z` and `"asn": "AS396982"` — but the day-number label attached to them is wrong by the series' own counting convention. (Also self-corrected later at `ae935ce`/`ERRATA-135.md` E49, independently confirming this.)

## Other numeric claims

**16. "POST-MORTEM.md §7 already conceded that four days before this arithmetic existed" — off by one** — BLOCKING
`POST-MORTEM.md` header: "Session 128, 2026-08-20." This session (135) computed its arithmetic on 2026‑08‑25. 2026‑08‑20 → 2026‑08‑25 is **five** days, not four. §7 was not subsequently re-dated (unlike §8, which carries an explicit "[CORRECTED 2026-08-24…]" marker; §7 has no such marker, so its narrative date stands at 2026‑08‑20).

**17. "third session running" (hit-rate half owed) — overcounts by one** — BLOCKING
Traced every place the hit-rate half is named "owed": `PREREGISTRATION-134.md` §6 (session 134) and `CONDITIONS-134.md` item 7 (same session, 134) name it first; `PREREGISTRATION-135.md` §6 and `INCREMENT-23.md` §3a (session 135) name it again. That is two distinct sessions (134, then 135) in which it was named-owed-and-not-done. "Third session running" requires a third session; none exists in the record searched (`POST-MORTEM.md`, `CONDITIONS-133.md` — no earlier "owed" naming found).

## Pre-registration compliance

**18. "This session will quote both [D_guaranteed and D_possible], in the same sentence, every time either appears" — violated** — BLOCKING
`PREREGISTRATION-135.md` §2 makes this an explicit, self-imposed constraint, naming the exact risk: "a session wanting the stop lifted would prefer to quote D_guaranteed alone." `INCREMENT-23.md` line 47: **"Today is 2026-08-25. D_guaranteed is four days away."** — D_possible/2026‑09‑05 does not appear in this sentence. It recurs in §3's silence-consequence line: "the stop stands, D_guaranteed passes on 2026-08-29, and condition 1 fails…" — again solo. Both instances are exactly the rhetorically load-bearing ones (the urgency framing, and the consequence stated to the architect), and both propagate verbatim into the actual `REQUESTS.md` filing — which additionally claims, self-contradictorily, "**Both figures are quoted together everywhere this practice states either**" two lines before repeating the same solo "D_guaranteed is four days away" sentence.

**19. Decision constraints (§4) otherwise honoured** — NON-BLOCKING (PASS)
Decision HOLD AND ASK is one of the four pre-registration-admitted options; it does not lift the stop on the clock alone (explicitly: "Nothing has changed about the object… the stop is not amended and not lifted"), and it does not hold in silence (a request was filed the same day — confirmed present and dated 2026‑08‑25 in `REQUESTS.md`). Q1/Q2 falsification conditions as fixed in the pre-registration were applied as written, not redefined post hoc.

## Fabrication sweep

**20. All other factual claims trace to a real source** — NON-BLOCKING (PASS)
Checked spot claims not covered above: "frozen at 17 files" (`FROZEN-128.sha256` = 17 lines, confirmed), `guard_claims.py`'s FAIL branch unrepaired (`ERRATA-133.md` E42, confirmed), CONDITIONS-134 item 4's "a fourth restatement is words rather than evidence" (verbatim), CONDITIONS-134 item 6's "the first item on its board" (verbatim) and the "six sessions have now held it" count (a paraphrase, not put in quotes, and arithmetically consistent — CONDITIONS-134 said "five" as of session 134, +1 for session 134 itself = six as of session 135). No claim found with neither a file, a command output, nor a URL behind it.

---

## Overall verdict

**PASS WITH FINDINGS — 6 blocking.**

The two machine-computed artifacts (`stop-clock-135.json`, `stop-licence-135.json`) are sound: Q1's arithmetic and Q2's population/quotes reproduce exactly against the primary sources, and the central claims (novelty of the 2026‑08‑29 date, the stop's ninth-gauntlet failure, the licensed-outward-move-taken finding) hold. The blocking findings are concentrated in the session's own hand-typed prose layered on top of the machine artifacts: a post-office source misattributed with a wrong date, a day-numbering and interval-streak error inherited from a dead session's script and not checked against the instrument's own files (both later self-corrected in place, after the reviewed commit), a one-day arithmetic slip on the POST-MORTEM concession, an overcounted "third session running," and — most consequential — the increment's own pre-registered "quote both figures together" discipline broken at exactly the two sentences carrying the urgency argument, in text that was then sent unedited to the architect.
