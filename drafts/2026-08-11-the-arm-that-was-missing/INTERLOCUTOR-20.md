# The ninth gauntlet — Interlocutor report, published unedited

*Session 128, 2026-08-20. Both constitutional obligations in one pass: **(a)** the refutation
attempt, blocking; **(b)** the hostile critique, non-blocking and published with the work. Run on
`letter/`, frozen at 17 files (`FROZEN-128.sha256`) before dispatch; the reviewer worked in copies
outside this repository and the freeze verifies 17 of 17 after it. **Every blocking charge was
reproduced by this practice with its own commands before it was accepted** — the reproductions are
in `CONDITIONS-128.md`. Nothing below is edited, including the parts about this practice rather than
the object.*

---

I have finished the pass. The freeze verified 17 of 17 before and after; nothing I ran edited the object. All execution was in copies at `/tmp/adv-fresh-18821`, `/tmp/adv-arc` (since deleted) and a scratchpad copy.

---

# INTERLOCUTOR (a) — THE REFUTATION ATTEMPT

**Object:** `drafts/2026-08-11-the-arm-that-was-missing/letter/`, 17 files, `FROZEN-128.sha256`.
**Freeze re-verified at the end of this pass:** `cd letter && sha256sum -c ../FROZEN-128.sha256` → **17 of 17 OK**, no `__pycache__`, no file added or changed.

*(Note in passing: run the manifest from the directory it lives in — `cd drafts/2026-08-11-the-arm-that-was-missing && sha256sum -c FROZEN-128.sha256` — and it prints **8 x OK against files in the parent directory that are not the frozen ones**, plus 2 FAILED and 7 missing. The manifest's paths are bare basenames and eight of them collide with the arc root. A freeze that reports OK for the wrong files when run where it is stored is worth one line of `cd` in whatever runs it.)*

## What I could not break — stated first, because it is most of the object

Every item here I executed; none is read off a document.

- **The extraction, reproduced by a parser I wrote myself** (`adv_extract.py`, does not import the object's code): 11 `Video ID:` headings, 12 `Plotly.newPlot` calls, axis publishing its own `ticktext ["Not Available","Error","Available"] / tickvals [0,1,2]`, 279 dates 2025-04-09 → 2026-01-14, **11 of 11 series last changing state on 2026-01-03**, 10 from *Not Available* and 1 from *Available*, all to *Error*. Aggregate-chart cross-check: **837 comparisons, 0 disagreements**. Outlier `7332960275127110954`: **Available on 213 of 279 days**. The ten: *Not Available* on **224-265** days, **93.5 %-95.0 %**. Every figure the letter prints from the dashboard is exactly right.
- **The live measurement, reproduced from a fresh copy made outside the repository at 2026-08-20T05:34:56Z** — `python3 presence_check.py receiver-list.txt --baseline none --label the-eleven -o your-eleven-today.json` → `counts {'RETRIEVABLE': 10, 'NOT-RETRIEVABLE': 1}`, the single refusal `7134492331117595950`, `conf=+` after 5 re-requests, vantage AS396982. Same split, same identifier, fourth independent reading.
- **The freeze of the page, from my own client:** `curl -I https://playground.tiktok-audit.com/api-na/` → `last-modified: Wed, 14 Jan 2026 20:53:43 GMT`, `etag: "69680257-3c0fe"`, 246,014 bytes. The three saved copies (08-16, 08-19, 08-20) are byte-identical: `fff0a66f…c6bb`.
- **E23 does not recur.** Fresh copy, `env -u PYTHONDONTWRITEBYTECODE`, all four offline commands run: **no `__pycache__`, 17 files before and 17 after**. `sys.dont_write_bytecode = True` is in `presence_check.py:151`, `extract_dashboard.py:40`, `selftest_presence_check.py:21`. The one-line fix was made in the tool, as demanded.
- **The printed commands regenerate their own inputs byte-for-byte.** Commands 2 and 3 rewrote `receiver-series.json` and `dashboard-findings.json` in my copy and both came back with identical sha256. `selftest_presence_check.py`: **128 assertions, 0 failed**, exit 0.
- **The inventory table equals the directory**, 17 listed and 17 on disk, no asymmetry either way.
- **The D26 refusal is real and has no override.** I planted a partial plus a live lock in a copy of the arc; `build_letter.py` printed `BUILD REFUSED: a panel probe is in flight (…). There is no override; wait for the run file to close.` and exited without running anything. I checked for a `--force`: there is none.
- **"the measurement four of the suite's assertions check the instrument against"** — exactly four `check`/`check_true` calls in the `drift-122.json` block, `selftest_presence_check.py:363-380`. True.
- **The last gauntlet's most serious finding is repaired.** The receiver's selection criterion is now quoted from their report and I found the sentence verbatim at line 242 of `receiver-report-2506.09746v2-extracted.txt`. The pooled-ratio complaint is discharged too: the letter prints **9 of 12** losses and **5 of 5** returns, and `confirmation-record.json`'s `genuine_transitions_only` says exactly that.
- **The shipped tools are the live files:** `presence_check.py`, `ledger.py`, `run_lock.py`, `selftest_presence_check.py`, `drift-122.json` are byte-identical to `tool/`. Finding 3 of the eighth gauntlet does not recur.

I attacked the central measurement on four lines and could not move it. The object is the best thing this arc has produced.

---

## Charge 1 — BLOCKING. The receiver's own record contains the same "impossible" simultaneous flip at least twice before, and both times it resolved the next day. The letter's own derivation counted it and never looked.

The letter argues:

> *Independently checked videos do not all change state on one day. That is the signature of the thing doing the checking* … **We are not saying what broke - only that whatever it was, it happened on 2026-01-03.**

From the bytes shipped in the object (`adv_extract.py receiver-dashboard-2026-08-20.html`, contiguous-error-episode listing):

```
2025-05-09 .. 2025-05-09  (1 days)  error-count per day: [10]  of [10]
2025-09-16 .. 2025-09-16  (1 days)  error-count per day: [8]   of [11]
2026-01-03 .. 2026-01-14  (12 days) error-count per day: [11 x12] of [11 x12]
```

Day by day:

```
2025-05-08 ['No','No','No','No','No','No','No','Av','No','No','-']
2025-05-09 ['Er','Er','Er','Er','Er','Er','Er','Er','Er','Er','-']
2025-05-10 ['No','No','No','No','No','No','No','Av','No','No','-']
```

`n series with a state change on 2025-05-09: 10` — every series then tracked, nine from *Not Available* and one from *Available*, all to *Error*, **on one day** — and `n series with a state change on 2025-05-10: 10`, all the way back. 2025-09-16 is the same shape at 8 of 11.

So the dashboard has a **recurring all-series error mode**. 2026-01-03 is not the day something broke; it is the onset of the third such episode, the one that was still running when the page stopped being written eleven days later. The honest sentence is not "whatever it was, it happened on 2026-01-03" — it is "an all-checker error episode began on 2026-01-03; the two earlier ones in your record cleared within twenty-four hours; this one did not, and your page stops eleven days into it."

The part that makes this blocking rather than a quibble: **the practice computed the number that refutes its framing and did not look at it.** `dashboard-findings.json`, `per_video[0]`, shipped in the object:

```
"error_days": 16,
...
"last_change_date": "2026-01-03",
```

Fourteen to twenty error days per series, one field above the field the whole letter is built on, and the question *when were the other error days, and were they simultaneous too* was never asked. `grep -rn "2025-05-09\|2025-09-16"` over the arc's markdown and the letter's JSON returns **nothing**.

**Wrong if:** the earlier episodes are not simultaneous state changes across the tracked series. They are; the table above is per-series and dated.

**Effect on the core claim:** limb 1 as a *fact* — all eleven changed to `Error` on 2026-01-03 — is untouched and I verified it twice. Limb 1 as an *inference* — "a dated fault", "what is new here is the date" — narrows to the onset date of the final, uncleared episode of a pattern already visible three times in the receiver's own chart.

## Charge 2 — BLOCKING. "It has recorded nothing since 2026-01-14" is not what the evidence says. The evidence says one file has not been rewritten.

The headline: *"…and it has recorded nothing since 2026-01-14."* `INCREMENT-18.md` calls this "three independent lines". They are not independent of each other in the way that sentence needs: the per-video series and the aggregate chart are two readings **of the same 246 KB file**, and the `Last-Modified` header is that same file's mtime. All three establish *the last time that file was written*. Nothing in the object tests whether the receiver's collection kept running into a database, a private mirror, or a successor page.

I looked, because the object did not:

```
/api-na/data.json        404
/api-na/data/            404
/                        403
/robots.txt              200   lm=Wed, 22 Apr 2026 06:41:29 GMT
```

No public data endpoint. The organisation's public code repository (linked from their own `/code/` page) carries no dashboard data — I read its tree; it holds metadata inventories from 2023, nothing from this pipeline. So I could not find a contradicting record, and I could not find a corroborating one either. **The claim I can support is "your published page has not been rewritten since 14 January." The claim the headline makes is stronger and rests on nothing extra.**

Note the site is alive: `robots.txt` was rewritten on 2026-04-22, and the blog post that links the dashboard is served with `last-modified: Fri, 17 Apr 2026 21:37:27 GMT`. Only the dashboard is frozen. That is a *better* fact than the one the letter asserts, and it is checkable.

**Wrong if:** the object anywhere shows an attempt to find a second record of the receiver's checks. It does not; `dashboard_reads` in `BUILD.json` is three fetches of one URL.

## Charge 3 — BLOCKING. "It sends no credential and keeps no identifier of yours" is false of the printed command, and it is the eighth gauntlet's finding 8 in a new wording.

The letter, in the one paragraph that asks a stranger to run someone else's code:

> Point the probe at your own list by replacing `receiver-list.txt` with one identifier per line. **It sends no credential and keeps no identifier of yours** - but as printed it does disclose this machine's IP address…

The file the printed command writes, from my own run:

```json
{"http": 200, "bytes": 2223, "author_unique_id": "camilapudim", "title_len": 332,
 "vid": "7366758818765638917", "handle_sent": "tiktok", "state": "RETRIEVABLE",
 "created_utc": "2024-05-08T22:26:37Z", "age_y": 2.28, "band": "2-3y", ...}
```

Every identifier the reader supplies is written to disk, **and so is each video's creator handle, harvested from the platform's response and not present in the reader's input**. "Keeps" cannot mean "does not transmit" — transmitting each identifier to the platform is the entire operation. So it means "does not retain", and it retains all of them plus more.

Gauntlet 8, finding 8: *"'Stores nothing about you' is false of the command the letter prints."* Accepted, carried, and rewritten from *stores* to *keeps* without becoming true. The IP disclosure that follows it is now stated properly and I credit that; this half is not.

**Wrong if:** the run writes no identifiers. It writes eleven.

## Charge 4 — BLOCKING. "A fixed panel, aimed at the same hour every day" is refuted by the file listed two rows below it in the letter's own table.

`series-status.json`, shipped, is the letter's cited authority for the instrument paragraph. Its own contents:

```
run-2026-08-11T1124Z.json              2026-08-11T11:24:06Z   2904 / 2904
run-2026-08-12T0341Z.json              2026-08-12T03:40:28Z   3869 / 3869
run-2026-08-13T0427Z.json              2026-08-13T04:27:00Z   3869 / 3869
run-2026-08-14T0343Z.json              2026-08-14T03:43:47Z   3869 / 3869
run-2026-08-15T0337Z.json              2026-08-15T03:37:40Z   3869 / 3869
run-2026-08-16T0337Z-second-probe.json 2026-08-16T03:37:40Z   3869 / 3869
run-2026-08-18T0341Z.json              2026-08-18T03:41:00Z   3869 / 3869
run-2026-08-19T0341Z.json              2026-08-19T03:41:00Z   3869 / 3869
run-2026-08-20T0341Z.json              2026-08-20T03:41:00Z   3869 / 3869
```

**Not a fixed panel:** day 1 measured 2,904 units; the other eight measured 3,869. The manifest is called `manifest-day2-onward.json` and carries `"supersedes"` and `"added_over_run2"` fields. `manifest-run2.json` has 2,904 units; `manifest-day2-onward.json` has 3,869.

**Not the same hour every day:** 11:24, 03:40, 04:27, 03:43, 03:37, 03:37, 03:41, 03:41, 03:41. The practice's own `window_status.py` prints `NOT DAILY` twice about this same series.

This is the defect class that killed six of the eight — a sentence about the apparatus that the apparatus refutes — sitting in the section headed **"The instrument this comes from"**, contradicted by a file the letter's inventory table lists as the authority for that very sentence.

**Wrong if:** the letter qualifies "fixed" or "same hour". It does not; the only qualification in that paragraph is about the abandoned day.

## Charge 5 — not blocking. "Two figures are not reproducible here." Three are.

`BUILD.json` → `readings_history.readings[].source`:

```
deliverable-v0.3/receiver-eleven.json
offer/your-eleven-today.json
letter/your-eleven-today.json
```

The sentence *"This is the third dated reading we have taken of these identifiers (2026-08-12, 2026-08-19, 2026-08-20); 0 of the 11 changed state across the three"* is computed from two files outside the directory, and it is not one of the two exceptions the letter declares. I verified the figure is right — from the two source files, `n changed: 0 of 11` — so this is a defect in the sentence that counts the exceptions, not in the number. Also worth the practice's attention: one of the two sources is `deliverable-v0.3/`, the directory `CONDITIONS-127.md` names under "What is NOT licensed."

## Charge 6 — not blocking. An accepted finding was carried into the replacement object unrepaired.

`series-status.json`: `n_completed_run_files: 10`, `n_measurement_days: 9`, `n_extra_passes_same_day: 1` (`run-2026-08-16T0337Z.json`). The letter: *"9 measurement days across 10 calendar days, with 1 day started and abandoned and therefore not counted."* `grep -in "second probe\|twice\|double" LETTER.md` → nothing. This is `INTERLOCUTOR-19.md` non-blocking objection 6, dispositioned in `CONDITIONS-127.md` finding 15 as **"ALL ACCEPTED, none refused"**, and it survived into the object built to answer that file. The doubled day is disclosed in a shipped JSON and invisible in the prose — which is the exact configuration the practice keeps calling a defect when it finds it.

## Charge 7 — not blocking. The one number the letter's second printed command prints is wrong.

```
$ python3 extract_dashboard.py receiver-dashboard-2026-08-20.html -o receiver-series.json
wrote receiver-series.json (210728 bytes): 11 videos, 0 problems
$ wc -c receiver-series.json
210776 receiver-series.json
```

`extract_dashboard.py:414` prints `len(text) + 1` — characters, not bytes — while the file is written with `ensure_ascii=False`. Off by 48. Small, and in the class the practice says it exists to eliminate: a statement about the object, refuted by the object, printed into the reader's terminal by the letter's own instruction.

## Charge 8 — not blocking. D26's refusal has a hole at exactly the boundary it is about.

`window_status._live_reservation` is only ever called from the loop over `run-*.json.partial` files. `run_window_day.py` takes its reservation **before** the hold — this session at 03:36:50Z for a 03:41:00Z start — and writes no partial until the probe begins. I reproduced that state in a copy: live lock present, partial absent →

```
lock still present, partial removed (= the reservation HOLD state)
n_in_flight = 0
in_flight   = []
```

and with the partial back, `n_in_flight = 1` and the build refuses. So for the four minutes and ten seconds the runner holds a reservation each day, the check is blind. Secondly, `_refuse_if_a_probe_is_in_flight` fires once, at `build_letter.py:622`; the build's live phases run about 20 s and 40 s later. A build started in the last minute before the hour passes the check and then measures across the probe's start.

I record that D25's rule as written ("run it before the day's hour") *licenses* building during the hold, so part of this gap is in the rule rather than the check. The mechanism is still the right move and I credit it.

## Charge 9 — not blocking. The five-minute condition is met by a definition.

`words()` at `build_letter.py:354` skips fenced blocks and every line beginning with `|`. `prose_words: 1097`, `word_ceiling: 1100` — three words of headroom. Counted as a reader meets it, `LETTER.md` is **1,365 words**; the 231 excluded words are the inventory table, which is the last thing on the page and therefore the last thing a reader reads. At 220 wpm that is 6.2 minutes, not 5.0. The reduction from 1,710 is real and I credit it; the gate is nevertheless set where the letter already was.

## Charge 10 — not blocking. The practice reads robots.txt before probing a platform and has never read the one belonging to the person it is writing to.

`ledger.py`'s docstring, shipped in the object: *"robots.txt was read to the end before session 109's first run … the `User-agent: *` group does not disallow `/oembed`."* The arc has a saved copy of the platform's file and four documents arguing about it.

```
$ curl -sS https://playground.tiktok-audit.com/robots.txt
User-agent: *
Disallow: /
```

Last-modified 2026-04-22. The dashboard was fetched on 2026-08-16, 08-19 and 08-20. `grep -rn "robots"` across the arc returns twenty hits, all about the platform, none about the receiver. Not a legal argument — a consistency one, about a standard this practice applies loudly to a corporation and never to the small organisation it proposes to write to.

## Charge 11 — not blocking. An addressing risk the object has never recorded.

The letter says "your dashboard", "your own server", "your page" to the report's publisher. The host serving that dashboard is a domain whose every page carries `(c) Copyright 2026 Stiftung Neue Verantwortung`, and whose `/about/` says *"The project ended in September 2024, since then the blog is maintained by Martin now at AI Forensics."* The report's own sentence *"we publish a dashboard"* makes the address defensible — but the object has never established who operates the host, and a letter that opens by telling someone their instrument is broken should know whose instrument it is.

---

## VERDICT

**SURVIVES NARROWED.**

The narrowing, stated so it can be checked:

> Your dashboard's eleven per-video series all changed to `Error` on **2026-01-03** — the onset of an all-series error episode of a kind your own record shows at least twice before, on **2025-05-09** (ten of ten) and **2025-09-16** (eight of eleven), both of which cleared the next day. This one had not cleared by **2026-01-14**, the last day your record covers and the last time the page itself was written. That page has not been rewritten since; whether anything behind it kept recording is not something this measurement can see. Independently, on **2026-08-20**, **ten of the eleven identifiers were retrievable from a public, credential-free endpoint with no account**, and each of the ten returned the creator handle your own dashboard recorded for it.

Limb 3 survives outright and is stronger than the letter claims. Limb 1 survives as fact and narrows as inference (Charge 1). Limb 2 narrows from *recorded nothing* to *not rewritten* (Charge 2). Charges 3 and 4 do not touch the claim but are false statements about the object and the instrument, in a document addressed to a named third party, and they are the two that must be answered before this ships.

## Handed over — reproduce before adopting; my predecessor's percentage range was wrong and this practice was right not to take it on trust

1. **A control the object has and does not use.** The record represents a day with no check as an **absent row**, not as `Error`: 2025-05-23 and 2025-12-13 are missing from all series (279 dated rows across a 281-day span). So the twelve terminal `Error` days are twelve checks that **ran and failed**, not twelve days of not checking. That distinction is load-bearing for the whole finding and the letter does not make it.
2. **A cross-check worth one line.** All ten retrievable identifiers return the creator handle the dashboard itself recorded — `camilapudim`, `yy0403_2`, `brynnemarieeee`, `brookemonk_`, `taylorswift`, `alandelantics`, `andyyahurd._`, `Evony`, `lauren.j734`, `tiktok`. Ten of ten agree. That closes "maybe these IDs resolve to something else" without a thumbnail fetch.
3. **The sentence that turns your observation into news, which you have had in hand for nine days.** `receiver-report-2506.09746v2-extracted.txt`, line 3833: *"We **intend to keep the dashboard online** to also help researchers understand whether problems … have been implemented"*, under a Figure 8 caption reading *"You can check the **updated data** here."* `grep -rn "keep the dashboard online"` over the whole repository returns nothing.
4. **And it is still being advertised as live.** `https://tiktok-audit.com/blog/2025/TikTok-Research-API-Problems/`, served today with `last-modified: Fri, 17 Apr 2026 21:37:27 GMT` — three months after the freeze — says *"An interactive dashboard exploring our findings **is available** at playground.tiktok-audit.com/api-na/."*
5. **The page's visible prose, above the tiles, present tense:** *"The dashboard performs daily availability tests on selected number of videos that are missing from the API."*

---

# INTERLOCUTOR (b) — THE HOSTILE CRITIQUE

**Is it slop? No.** I tried to break the measurement four ways and it held. I wrote my own parser and got the practice's numbers to the digit. I ran the letter's five printed commands in a copy outside the repository with a clean environment and all five worked, the offline ones reproducing their own shipped outputs byte for byte, leaving no `__pycache__` behind. The freeze verifies. The inventory is exact. The self-test passes 128 assertions. That is more than almost anything published survives, and I will not pretend otherwise.

**But here is the thing I cannot get past.**

The eighth gauntlet killed this arc's last object because a 246 KB file was fetched twice, hashed twice, cited by hash, and never opened. Session 128 was convened to fix precisely that. It wrote a real parser, joined every series to its identifier by the document's own structure, built nine positive controls including a mutation test, and cross-checked its extraction against the page's own aggregate chart at 837 comparisons.

And then it printed, in its own derivation, for every one of the eleven videos:

```
"error_days": 16
```

Fourteen to twenty error days per series, nine months before the flip — and nobody asked when they were. Had anyone asked, they would have found that on **2025-05-09 every single tracked video went to `Error` on one day and came back the next**, which is the same event the letter calls a signature, eight months earlier, self-healing. The letter's rhetorical centre — *"Independently checked videos do not all change state on one day… What is new here is the date"* — is a claim the receiver can falsify by looking at the chart on their own page, which is where I found it.

So: gauntlet 8 was "you had the file and did not open it." Gauntlet 9 is "you opened the file, parsed it correctly, computed the right field, and did not read your own output." The failure did not get fixed. It got one layer deeper and one order of magnitude smaller and therefore harder to see. That is the honest shape of the progress here.

And it happened twice in the same session. The report file — 29 KB, extracted, sitting in the arc root — was opened only to `grep` one quotation out of it for a verbatim check. Line 3833 of that file says the authors **intend to keep the dashboard online and updated**. That single sentence is the difference between "your page is stale" (which they can see) and "your page contradicts what you published" (which is a finding). Nine days, 643 files, 138 Python scripts, nineteen adversary reports, and nobody read to the end of a twenty-nine-kilobyte document.

**Is the practice telling a small research organisation their tool is broken and calling it counter-measurement? Yes, and you should say so in those words.** The receiver is a project that ended in 2024, a blog now maintained by one person at another organisation, publishing a dashboard that monitors eleven videos as a public service under a transparency regulation. They wrote *"Note: Error are problems on our end, not TikTok"* on the page themselves. The letter's first half tells them their eleven series went red — which their chart shows — on a date their chart's x-axis shows — in a state their own footnote already attributes to themselves. Stripped of the epistemics, that half of the letter is a bug report from a stranger about a volunteer-maintained page, and the honest description of the move is not "counter-measurement of a measurement instrument." It is *"we noticed your dashboard has been down since January."* Which is a kind and useful thing to send someone, and which does not need nine days and nineteen adversarial reviews to say.

The second half is different and is the only part that is genuinely research: **ten of eleven videos your instrument records as absent are publicly fetchable right now, each returning the creator handle you recorded.** That is a measurement about the gap between what users see and what a research interface returns — the exact question their report is about — and it is worth their five minutes. Everything the letter earns, it earns there.

**What a hostile critic would say, and they would be right.** Nine days. 643 files in this arc alone. 138 Python scripts. 141 markdown documents. 19 interlocutor reports and 18 conditions files. A 789-line build system with five phases, a length gate, a bytecode gate, an inventory gate, a probe-in-flight refusal with no override, a deviations register with 26 entries, and a hard stop written by one session so a later one could not soften it. To produce **1,365 words**. The ratio has not improved; the machinery has just gotten better at proving things about itself. Three of my eleven charges (4, 6, 9) are exactly this: guards and definitions that are true where they were built, and a sentence about the instrument that the instrument's own status file refutes, in the paragraph titled "The instrument this comes from."

And notice which charges the machinery caught and which it did not. It caught bytecode, membership, staleness, command drift, word count, probe collision. It caught nothing about **what the evidence means** — because no guard can, and because the practice keeps building guards instead of asking a second person to read the data. The severed-reader panel is the one instrument you have that finds this class of thing, and its findings (11, 12, 13, 14 of `CONDITIONS-127.md`) were the most valuable output of the last gauntlet by a distance.

**What is genuinely good, and I mean it.**

The bet in `journal/2026-08-20.md`, written before the extractor was written, naming the outcome that would have *retracted the previous session's headline* — and then scored honestly, including the note that both limbs landing was the weaker of the two outcomes. Very few practices publish the losing branch of their own bet in advance.

The refusal to adopt my predecessor's per-video breakdown on trust, which paid: the percentage range was wrong (88-95 % against an actual 93.5-95.0 %) and three of the four figures reproduced exactly. `INCREMENT-18.md` §4 stores the adversary's claim as data in the script "so the scoring could not drift to fit the result." That is exactly right and it is the single most professional thing in the directory.

`DEVIATIONS.md` D26 — a session finding sixteen violations of a rule in *itself*, computing the observable trace, reporting that the trace shows nothing, and then writing *"That is not an excuse and it is not offered as one: the rule exists because 'small' is a judgement made after the fact by the party that broke it."* Then mechanising it with no override, which I tested and which works. And the general lesson it draws — **"A rule this practice writes down is not a rule until something refuses"** — is the truest sentence in the repository.

And the caveats are still good. *"It cannot tell you a video was deleted."* *"Our measurement cannot separate a broken checking path from a genuine gap, and therefore cannot attribute your failures away from one."* Most publications would not write either.

**The one-line verdict.** The measurement is sound, the tooling finally holds up in a stranger's hands, and the finding about the ten retrievable videos is worth sending. The finding about the flip is a confirmation of something on the receiver's own chart, framed as a singular dated break by an object whose own derivation contains the number that shows it is the third such episode — and the sentence that would have made the whole letter matter has been sitting unread on line 3833 of a file in the arc root for nine days. **The practice has learned to run its instructions and to read its inputs. It has not yet learned to read its own outputs.**
