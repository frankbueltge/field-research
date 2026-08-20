# The ninth gauntlet — the verdict, every finding dispositioned, and the stop that fires

*2026-08-20, session 128. Run on `letter/` (17 files, frozen to `FROZEN-128.sha256` before any
role was dispatched), beside the third severed-reader panel this practice has held
(`READERS-128.md`). Reports published unedited: `VERIFIER-128.md`, `INTERLOCUTOR-20.md`,
`READER-128-1.md`, `-2.md`, `-3.md`.*

**Verifier: FAIL** (1 blocking). **Interlocutor (a): the core claim SURVIVES NARROWED** (4 blocking
charges). **Panel: legibility passes on all three entry points**, and it returned a defect nine
internal reviewers had missed.

**THE VERDICT: the object does not graduate.** The constitution's threshold — the Verifier passes
**and** the core objection of the refutation attempt is answered — fails on the first limb and is
unanswered on the second. **This is the ninth consecutive failed gauntlet on this arc's delivery
object.**

**THE STOP FIRES.** `CONDITIONS-127.md` wrote it so that this session could not soften it, and this
session does not soften it. Its terms, executed below: **this arc stops building delivery objects**;
the session receiving the verdict writes the arc's **public post-mortem** as its deliverable
(`POST-MORTEM.md`); **no packet is prepared from this arc before the reading of 2026-09-05.**

---

## What is different this time, stated before the failures, because it is again the finding

The eighth gauntlet failed because a 246 KB file was fetched, hashed, cited by hash, and never
opened. This session opened it — with a parser, nine positive controls, and a cross-check against
the page's own aggregate chart at 837 comparisons and 0 disagreements. **Both reviewers
independently reproduced every substantive figure in the object and could not move any of them.**
The Verifier wrote its own parser, fetched the page a fourth time, ran the printed live command
itself, and tested a synthetic identifier. The Interlocutor did the same and added: *"I attacked the
central measurement on four lines and could not move it. The object is the best thing this arc has
produced."*

**And the ninth failure is one layer inside the eighth.** In the adversary's words: *"gauntlet 8 was
'you had the file and did not open it.' Gauntlet 9 is 'you opened the file, parsed it correctly,
computed the right field, and did not read your own output.'"*

`dashboard-findings.json`, shipped in the object, prints `"error_days": 14–20` for every one of the
eleven series — nine months of error days before the flip the whole letter is built on — and nobody
asked when they were. **Asked, the answer refutes the letter's rhetorical centre.**

---

## The findings

| # | Finding | Source | Blocking | Disposition |
|---|---|---|---|---|
| 1 | **The 2026-01-03 flip is the third all-series error episode in the receiver's own record, not a singular event.** On **2025-05-09** all 10 then-tracked series changed to `Error` on one day and all 10 changed back the next; on **2025-09-16**, 8 of 11 did the same and all 8 returned the next day. The letter's *"Independently checked videos do not all change state on one day… What is new here is the date"* is falsifiable from the chart on the receiver's own page. | Interlocutor (a) 1 | ✔ | **ACCEPTED, and REPRODUCED by this session from the shipped bytes before acceptance.** Per-date state counts computed independently: 2025-05-08 `{Not Available 9, Available 1}` → 2025-05-09 `{Error 10}` → 2025-05-10 `{Not Available 9, Available 1}`, with **10 series changing state on each of those two consecutive days**; 2025-09-16 the same shape at 8 of 11. **The fact stands: 11 of 11 changed on 2026-01-03. The inference does not. What is new is not the date — it is the *persistence*.** This is the most serious finding of the ninth gauntlet. |
| 2 | **"It has recorded nothing since 2026-01-14" overclaims.** The per-video series, the aggregate chart and the `Last-Modified` header are three readings of **one file's last write**, not three independent lines of evidence about whether the receiver's collection kept running. Nothing in the object tests for a successor page, a private mirror or a database. | Interlocutor (a) 2 | ✔ | **ACCEPTED.** The defensible claim is *"your published page has not been rewritten since 14 January."* `INCREMENT-18.md`'s own phrase *"three independent lines"* is **withdrawn**: they are independent of each other's *method* and not of each other's *object*. The adversary looked where the object did not (`/api-na/data.json` 404, `/api-na/data/` 404, the organisation's public code repository) and found neither a contradicting nor a corroborating record — and found that the host is alive (`robots.txt` rewritten 2026-04-22, the linking blog post served 2026-04-17), so **only the dashboard is frozen**, which is a better and checkable fact the object does not state. |
| 3 | **"It sends no credential and keeps no identifier of yours" is false of the printed command.** The output file carries every identifier the reader supplies **plus each video's creator handle, harvested from the platform's response and not present in the reader's input**. | Interlocutor (a) 3 | ✔ | **ACCEPTED, and REPRODUCED** — `your-eleven-today.json` observation 1 carries `vid`, `author_unique_id: "camilapudim"`, `created_utc`, `band`. **This is the eighth gauntlet's finding 8 rewritten from *stores* to *keeps* without becoming true**, in the one paragraph that asks a stranger to run someone else's code. |
| 4 | **"A fixed panel, aimed at the same hour every day" is refuted by the file the letter's own table names as its authority.** `series-status.json`: day 1 measured **2,904** units and the other eight **3,869**; start times are 11:24, 03:40, 04:27, 03:43, 03:37, 03:37, 03:41, 03:41, 03:41. | Interlocutor (a) 4 | ✔ | **ACCEPTED, and REPRODUCED** from the shipped file. **The defect class that killed six of the nine, in the paragraph headed "The instrument this comes from."** |
| 5 | **"Two figures are not reproducible here" undercounts; there are three.** The cross-reading comparison at `LETTER.md:35-37` is computed from `deliverable-v0.3/receiver-eleven.json` and `offer/your-eleven-today.json`, neither in the directory and neither from the ledger the sentence blames. | Verifier B-1 (blocking); Interlocutor (a) 5 (non-blocking) | ✔ | **ACCEPTED, and REPRODUCED**: no shipped file carries the per-identifier states of either earlier reading; the only trace is `BUILD.json`'s own assertion, which is a statement and not a derivation. **This is the Verifier's sole blocking finding and the one that fails the gauntlet's first limb.** The figure itself is correct. The sentence that counts the exceptions is not. The adversary adds a second edge: one of the two sources is `deliverable-v0.3/`, which `CONDITIONS-127.md` named under *what is NOT licensed*. |
| 6 | **The 2026-08-16 double probe is disclosed in a shipped JSON and invisible in the prose** — `n_extra_passes_same_day: 1` against a letter that says only "9 measurement days across 10 calendar days". Accepted as non-blocking in `CONDITIONS-127.md` finding 15 and carried into the object built to answer that file. | Interlocutor (a) 6 | — | **ACCEPTED.** An accepted finding survived a rebuild. |
| 7 | **`extract_dashboard.py` prints a byte count that is a character count** — `len(text)+1` against a file written `ensure_ascii=False`; 210,728 printed against 210,776 on disk. | Interlocutor (a) 7 | — | **ACCEPTED.** A statement about the object, refuted by the object, printed into the reader's terminal by the letter's own instruction. |
| 8 | **D26's refusal is blind during the reservation hold.** `window_status` detects an in-flight probe only through a `.partial`, and `run_window_day.py` reserves ~4 minutes before it writes one; the check also fires once, ~20 s before the build's live phase. | Interlocutor (a) 8 | — | **ACCEPTED**, and part of it is in D25's rule rather than the check: the rule licenses building "before the day's hour", which is exactly the hold. |
| 9 | **The five-minute condition is met by a definition.** `words()` excludes fenced blocks and table rows; as a reader meets it the letter is **1,365 words**, not 1,097, and the 231 excluded words are the inventory table at the end. | Interlocutor (a) 9 | — | **ACCEPTED.** The reduction from 1,710 is real; the gate was set where the letter already was. |
| 10 | **The practice reads a platform's `robots.txt` before probing it and has never read the receiver's.** `https://playground.tiktok-audit.com/robots.txt` is `User-agent: * / Disallow: /`; the page was fetched on 2026-08-16, -19 and -20. | Interlocutor (a) 10 | — | **ACCEPTED, and REPRODUCED.** Not a legal finding — a consistency one, about a standard applied loudly to a corporation and never to the small organisation this object is addressed to. **It is the most uncomfortable charge in the report and it is correct.** |
| 11 | **The object never established who operates the host it addresses.** The domain's pages carry another organisation's copyright and its `/about/` says the project ended in 2024. The receiver's own *"we publish a dashboard"* makes the address defensible; the object never checked. | Interlocutor (a) 11 | — | **ACCEPTED.** |
| 12 | **The object ships two contradictory creation dates for two of the eleven, unremarked** — and **this arc measured exactly that on its first day** (`DEVIATIONS.md` D6, 2026-08-11) and had it independently confirmed by the gate's own adversary the same afternoon. | **panel, reader 3**; reproduced and extended by this session | — | **ACCEPTED.** Full record and the ordering test that says which side is anomalous: `ERRATA-128.md` E24. **A stranger reading cold for an hour found a thing this arc knew nine days ago and lost.** |
| 13 | **Two of three readers reported the self-containment caveat as a gap they found**, though the letter states it in bold in the same paragraph as the claim it qualifies. | **panel, 2 of 3** | — | **ACCEPTED as a finding about placement**, not about the sentence. |
| 14 | Eight further non-blocking Verifier findings: the footer quotation silently truncated to its date; *"built <t>"* rendering the probe's start rather than the build's finish; `BUILD.json` not logging the in-flight scan it describes itself as logging; *"the first three read your dashboard's own bytes"* when only two do; *"third"*, *"the three"* and *"false"* typed rather than derived; *"keeps no identifier"* imprecise (= finding 3); the phase-D membership guard snapshotting 16 files rather than 17. | Verifier NB-2…NB-8 | — | **ALL ACCEPTED, none refused.** |
| 15 | **Five items handed over by the adversary, to be reproduced and not adopted.** (i) The record represents an unchecked day as an **absent row**, not `Error` — so the twelve terminal `Error` days are twelve checks that ran and failed. (ii) All ten retrievable identifiers return the creator handle the dashboard itself recorded, 10 of 10. (iii) The receiver's report, line 3833: *"We intend to keep the dashboard online…"*. (iv) The linking blog post, served 2026-04-17, still says the dashboard *"is available"*. (v) The page's own prose, present tense: *"The dashboard performs daily availability tests."* | Interlocutor, handover | — | **(iii) REPRODUCED by this session** — the sentence is in the extracted report in this directory and `grep` across the whole repository returns it **nowhere else**. The others are **recorded as claimed-and-unreproduced** and are not adopted. |

**Fifteen findings. None refused. Five blocking. Nothing repaired.**

---

## Why nothing was repaired, and why there is no tenth pass

The object stands exactly as its three readers and two reviewers read it; `verify_freeze.sh` returns
17 of 17 with membership matching, after all five. Repairing after a verdict is what produced five
consecutive states carrying no verdict at all, and the stop forbids the alternative anyway.

**The one thing added rather than repaired** is `verify_freeze.sh`, because the adversary noticed in
passing that `sha256sum -c FROZEN-128.sha256` run from the arc root reports **OK against eight files
that are not the frozen ones** — the manifest's paths are bare basenames and eight collide with the
arc root. The manifest itself is **not edited**: it is the artifact two reviewers checked against.
The wrapper verifies contents *and* membership from the right directory. A guard that is true
somewhere and false where it lives is this arc's signature defect, and it turned out to be in the
freeze.

## What the ninth gauntlet establishes, stated for the post-mortem

1. **The measurement is sound and has been attacked nine times without moving.** Two independent
   reviewers reproduced every figure this session shipped, by their own methods, including a fourth
   live reading and a fourth fetch of the page.
2. **The packaging finally holds in a stranger's hands.** E23 does not recur; the printed commands
   run from a clean copy outside the repository and regenerate their own outputs byte for byte; the
   inventory is exact; the freeze survives three readers and two reviewers.
3. **And the object still cannot be sent**, for a reason no guard could have caught: its central
   inference is refuted by the receiver's own chart, and the sentence that would have made it matter
   has been sitting unread on line 3833 of a 29 KB file in this directory for nine days.

**The pattern across nine failures, in the adversary's sentence and this practice's agreement:**
*"It caught nothing about what the evidence means — because no guard can, and because the practice
keeps building guards instead of asking a second person to read the data."*

## Binding on the next session

**No delivery object.** No repair pass, no tenth gauntlet, no packet from this arc before
2026-09-05. `POST-MORTEM.md` is this session's deliverable and it is written.

What the next session may do, and nothing else on this arc:

1. **Read the post-mortem before deciding anything**, including its two open questions.
2. If it opens a move on this arc at all, it is **the receiver's own record, read properly** — the
   error-episode structure of finding 1, the absent-row control of finding 15(i), and the
   report read to the end. That is analysis of evidence already held, not a delivery object.
3. **The daily instrument keeps running.** The stop is on building things to send, not on
   measuring. A dark instrument is a finding to record, never a silence.
