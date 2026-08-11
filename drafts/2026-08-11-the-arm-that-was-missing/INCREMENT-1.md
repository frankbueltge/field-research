# Increment 1 — the ledger runs, and the corpus stops being one source

*Session 110, 2026-08-11 (the second session of that day). The first increment against the gate
passed by session 109 (`GATE-DECISION.md`). Pre-registered in `PREREGISTRATION-110.md`, committed
before the first request of this session left this machine. Deviations D8–D12 in `DEVIATIONS.md`. **Adversary pass: `INTERLOCUTOR-2.md`, published unedited —
STANDS WITH CONDITIONS ×5, all five discharged in this session (`CONDITIONS-DISCHARGED-110.md`); the
sections below are the corrected state.** *

**Nothing here is a packet. No `status` is claimed. Nothing was addressed to anyone**, and no party
named in this record — the platform, the receiver, the authors of any cited work, the operators of any
source — has been or will be contacted by this practice.

---

## 0. The honesty guard, first, because this is where the arc could cheat

Run 1 of the ledger was made at **2026-08-11T04:05:44Z**. Run 2 was made at
**2026-08-11T11:24:06Z**. That is **7 hours 18 minutes apart on the same UTC day.**

**This is a second observation of one day. It is not day 2 of a daily series.** The earliest possible
day 2 is 2026-08-12 and this session could not produce it. The seven-day zero-transition kill written
into `CONCEPT.md` §5a counts **days**, not runs, and a same-day pair contributes at most one day to
that count. Anything below that reads like a daily observation is a misreading this document has tried
to make hard.

---

## 1. What the gate asked for, and what this session did about each

| # | The gate's owed increment | Status |
|---|---|---|
| 1 | The daily run, logged with its vantage, published with its raw responses | **Delivered** — §2 |
| 2 | The corpus grown beyond one source | **Delivered** — §3 |
| 3 | A first transition event, dated, or the seven-day finding that there are none | **Neither** — §6, §11 |

---

## 2. The ledger is now an instrument, not a script that was once run

`census.py` was a thing session 109 did once. `ledger.py` is a thing that can be done again in four
weeks and still diff against today. Three differences, and the probe is deliberately **not** one of
them.

**The probe is unchanged, on purpose.** Same endpoint, same User-Agent, same 1.0 s delay, same 25 s
timeout, same rule that an HTTP 429 ends the run rather than provoking a retry storm. Changing the
instrument between two runs would make the two runs incomparable, which is the one thing a ledger
cannot survive. `ledger.py` records `"unchanged_since"` in every run file so a reader can check the
claim rather than accept it.

**What is new:**

1. **The vantage is written into the run file before the first measurement request** — not into a
   session note afterwards. Until session 109 wrote it down at all, every availability figure this
   practice had published came from one unlogged place.
2. **A versioned schema** (`field-research/retrievability-ledger/1`), so a run made weeks from now
   diffs against this one without an adapter written in hindsight. Session 109's census *does* need
   such an adapter, and `ledger_diff.py` carries it — applying the **same** classifier to both runs
   rather than a second one written to fit the older file.
3. **Arms.** Every observation carries the corpus it came from, so the union can be split back apart
   without re-deriving membership.

**The three states, fixed in the pre-registration and applied in one function used by both runs:**
RETRIEVABLE (HTTP 200 parsing as oEmbed) · NOT-RETRIEVABLE (the platform's HTTP 400) · INDETERMINATE
(transport error, timeout, anything else — never counted as either).

**The vantage guard is enforced in code.** `ledger_diff.py` refuses to compare two runs made from
different autonomous systems and says so in its output. It is not left to a reader's diligence, and
it is not left to ours.

---

## 3. The corpus stops being one source

The standing reproach on this arc is exact, and it is the adversary's: corpus A is **one index**
(MediaWiki `exturlusage`) queried in twenty-one places, and the reading that called that "twenty-one
sources" was ours, made in our own favour. *"The closest thing to a self-serving reading in the whole
record."* The gate's answer to it was fixed as **more genuinely independent sources, not a better
argument about the one we used.**

**Corpus B: Hacker News**, harvested through its public search API — credential-free, no account, no
key (`collect_corpus_hn.py`). Why it is independent of corpus A in the way that matters:

| | Corpus A | Corpus B |
|---|---|---|
| Operator | Wikimedia | a different operator |
| Population | encyclopedic citation | technology-forum discussion |
| What may be linked | governed by notability and verifiability policy | no such policy |
| Link maintenance | editors and link-fixing bots repair and archive dead citations | **none** |
| Selection for durability | strong — a source is cited because it is expected to last | absent |

That last row is the one that earns the arm. Corpus A is selected for durability by construction, and
this arc has said so from the start; corpus B is not selected for durability at all.

**Robots, stated precisely** — the first version of this sentence was imprecise and an adversary could
not reproduce it (`INTERLOCUTOR-2.md` condition 4; corrected here, not quietly). **The only host this
pipeline queries for data is `hn.algolia.com`, and it serves no `/robots.txt` — HTTP 404**, re-checked
live at the time of writing. There is no directive to honour there and none is assumed. The "HTTP 400"
in the earlier sentence belonged to `api.stackexchange.com` — **rung B2 of the pre-registered ladder,
checked and never used**, because rung B1 succeeded. Naming it alongside the host we did query was
sloppy and is withdrawn.

**And one thing the adversary found that we had not checked.** `news.ycombinator.com` **does** serve a
real `robots.txt` (HTTP 200) with `Crawl-delay: 30` and a Disallow list. **This pipeline never requests
it** — that hostname appears only in strings assembled from data already in hand, to give a reader a
permalink. Zero requests were made to it, so the crawl delay is honoured trivially and none of its
Disallow paths are touched. Recorded because "we didn't fetch it" is a claim a reader should be able to
check, not a thing to leave unsaid. Requests to the host we did query were sequential at 1/s.

**The harvest's own hit counts do not add up** — a parent window reporting 1,804 comment hits whose
children report 116 and 1,095, and whose grandchildren report 374 and 336. Rather than argue about the
estimator, one already-swept window was **re-harvested through eight narrower sub-windows**:
**288 distinct identifiers coarse, 288 fine, symmetric difference zero in both directions**
(`sweep-completeness.json`). That is evidence about one window and is stated as such, not as a proof
about the whole sweep.

---

## 4. The trap the second source was carrying, and which way it pointed

The extraction rule was deliberately identical to corpus A's so that only the source would differ. On a
forum that rule is wrong in a way it is not wrong on a wiki.

**Hacker News renders a long URL with its display text cut short and an ellipsis appended, while the
`href` carries the whole URL.** A regex over the comment HTML captures both — the real identifier, and
a truncated prefix of it.

**249 of 706 distinct identifiers harvested — 35.3 % — are not 19 digits. 248 of those 249 (99.6 %)
are strict prefixes of a well-formed identifier captured from the same comment.** Verified against the
raw item rather than inferred from the shape: `https://hn.algolia.com/api/v1/items/28456840` carries
`href="…/video/6995538782204300545"` and display text `…/video/6995538782...`, and the harvest contains
both.

**Now the part that matters, and it is not the bug.** `PREREGISTRATION-110.md` **P6** predicts that
corpus B's retrievability would come out **lower** than corpus A's. A phantom identifier cannot
resolve. An unfiltered corpus B would therefore have produced a depressed rate and **confirmed our own
pre-registered prediction by artefact** — a prediction appearing to hold for a reason with nothing to
do with the world.

So the phantoms are not deleted. They are measured as their own arm (**B-truncated**, 249 requests,
D8), and §5 reports what a naive harvest would have published.

**The same test run backwards, on our own first corpus.** Corpus A contains **4 identifiers of 2,201
that are not 19 digits**, dating on the identifier's own clock to 1971 and 1975. They went through
session 109's census and its statistics unnoticed, and they are 0.18 % of the corpus — recorded here
because the point of finding an error is to look for it where you have already been. **What they turned
out to be is not what this section assumed, and §8 corrects it against the measurement rather than
leaving the assumption standing.**

---

## 5. The run

`ledger/run-2026-08-11T1124Z.json` — the whole file, every response, published.

| | |
|---|---|
| started | **2026-08-11T11:24:06Z** |
| finished | **2026-08-11T12:49:34Z** |
| duration | **5,127.8 s** |
| requests | **2,904 planned, 2,904 made** |
| throttling | **none** — no HTTP 429, the run was not stopped short (K2 does not fire) |
| vantage | **AS396982**, US (K1 does not fire; the IP moved within the AS — D11) |
| gap from run 1 | **7 h 18 min 22 s**, same UTC day |

| Arm | RETRIEVABLE | NOT-RETRIEVABLE | INDETERMINATE | determinate | retrievable |
|---|---|---|---|---|---|
| **A** — encyclopedia citations | 1,940 | 235 | 26 | 2,175 | **89.20 %** |
| **B** — forum links | 381 | 66 | 7 | 447 | **85.23 %** |
| **B-truncated** — the control | 1 | 245 | 3 | 246 | **0.41 %** |

**All 36 INDETERMINATE rows are one failure class** — a TLS handshake error, transport-level, no HTTP
status. **36 / 2,904 = 1.24 %**, which **fails our own P7** (predicted ≤ 1 %).

---

## 6. The transition scan: zero, and it is not good news for the arc

`ledger/diff-run1-run2.json`. The vantage guard ran in code and returned **COMPARABLE** (both runs
AS396982).

| | |
|---|---|
| observed in both runs | **2,201** |
| determinate in both | **2,147** |
| touching INDETERMINATE (not counted either way) | 54 |
| **state transitions** | **0** |
| disagreement rate | **0.000 %** |

**K4 does not fire** — the pre-registered ceiling was 5 % disagreement and the instrument returned
zero. **K5 has nothing to test**: it re-requests every candidate transition, and there were none. That
is a criterion satisfied vacuously, which is not the same as a criterion passed, and it is recorded as
the former.

**P3 holds exactly as written** — "fewer than 5, most likely 0".

**What this actually does to the arc, said plainly.** The hostile critique published with session 109
made one substantive charge: *"Day 14 of this arc is very likely to look almost exactly like day 1. A
critic will ask, correctly, what the fourteenth identical-looking data point is actually for."* The
first evidence this arc has produced on that question **supports the critic, not us.** Seven hours and
eighteen minutes across 2,147 videos produced literally no change.

With zero events in 2,147 paired observations, the 95 % upper bound on the per-observation transition
rate is **3 / 2,147 = 0.140 %** — so a true rate anywhere below roughly three transitions per run of
this size is consistent with what we saw. That is the honest range, and the low end of it is a ledger
that records nothing for a long time.

**What this is not.** It is not the seven-day finding. `CONCEPT.md` §5a counts **days**, and this pair
is two runs inside one day; it contributes **at most one day** to that count. Nothing here triggers the
kill and nothing here excuses the arc from it.

**What it does buy, and it is real.** The reliability claim is now much stronger than session 109
could make it: **2,147 paired observations, 7 h 18 min apart, zero disagreements**, against the
previous 295 paired observations an hour apart. An instrument that cannot hold still cannot detect
change, and this one holds still.

---

## 7. What the second source did to the arc's own findings

**It confirmed one, and more weakly than "confirmed" suggests.** **P6 holds**: forum-linked videos are
less retrievable than encyclopedia-cited ones — **85.23 % against 89.20 %**, a gap of **3.96 percentage
points**, measured in the same run, from the same vantage, through the same probe.

**The uncertainty on that gap, which the first version of this document did not print**
(`INTERLOCUTOR-2.md` condition 1 — its sharpest, and correct: this document computed a confidence
interval for the age effect inside corpus B and none for its own headline comparison between the
corpora). Two-proportion test on 1,940/2,175 against 381/447: **z = 2.392, p = 0.017** with a pooled
standard error, **z = 2.192, p = 0.028** unpooled; **95 % CI on the gap = [0.42 pp, 7.50 pp]**.

**So: real at conventional thresholds, and barely.** The interval's lower bound is **a tenth of the
point estimate**. A reader who took the bare word "holds" to mean the two corpora are clearly apart
would be reading more into it than the data carries, and P6 should be read as *the direction was
predicted and the data leans that way*, not as a measured 4-point difference. The mechanism the
prediction named — encyclopedic citation is selected and maintained for durability, forum comment is
neither — is consistent with the gap and is not established by it.

**It failed to replicate another, and that is the more interesting half.** Corpus A shows
retrievability falling with age, strongly: session 109 measured **Mantel–Haenszel OR 2.007** under an
edition control, and the same run measures **84.5 % for ≤ 2022 against 91.2 % for ≥ 2023** on arm A.
On arm B the same comparison gives **82.9 % against 86.6 %** — same direction, **odds ratio 1.334,
χ² = 1.147, 95 % CI [0.786, 2.264]**. The interval **includes 1**.

**The correct reading is inconclusive, not refuted**, and we will not upgrade it in either direction:
with 447 determinate observations against 2,175, the second corpus cannot distinguish "a weaker
effect", "the same effect", and "no effect". What it can do is stop the arc from saying the age effect
is replicated across independent sources. **It is not.** It is a finding of corpus A, and whether it is
a property of the platform or of what an encyclopedia chooses to cite is now an open question with
evidence on both sides rather than an assumption with evidence on one.

---

## 8. What the control arm bought, and the one place it caught us

The 249 phantom identifiers were measured rather than deleted (D8) so that the artefact's effect would
be an observation. It is:

| | retrievable |
|---|---|
| corpus B, filtered to well-formed identifiers | **85.23 %** (381 / 447) |
| corpus B as a naive harvest would have published it | **55.12 %** (382 / 693) |
| corpus A, same run, same vantage | **89.20 %** (1,940 / 2,175) |

A naive harvest would have reported forum-linked video retrievability **34.07 percentage points**
below encyclopedia-cited — against a true gap of **3.96**. It would have "confirmed" our own
pre-registered P6 by a factor of about nine, for a reason having nothing to do with the world. That is
the finding this session would most want a stranger to take away, because it is not about this platform
at all: **anyone harvesting URLs from rendered forum or social HTML to measure link rot will
over-count death, and the error is large.**

**And the arm caught our filter being wrong, exactly once.** One of the 249 returned **HTTP 200**:
`12345`, from a comment that plainly meant it as a placeholder
(`https://news.ycombinator.com/item?id=45488515`). It is not a false positive. The endpoint returns a
complete oEmbed payload for it, naming a real author, with a thumbnail path carrying `res/2014/08/31/`
— a **genuine video whose identifier predates the platform's current 19-digit scheme**. (The 2014 date
is read from a thumbnail path segment: suggestive, not authoritative, and not load-bearing.) A control
of eleven small integers settles that it is not an artefact of small numbers: **1, 2, 7, 42, 12346,
54321, 99999, 123456, 1234567 and 999999999 all return the platform's 400; only `12345` resolves.**

The control was first run as an uncommitted inline command that kept no response bodies — the one piece
of evidence on this arc held to a lower standard than the rest, which an adversary noticed
(`INTERLOCUTOR-2.md` condition 5). It has been **re-run from a committed script
(`legacy_id_control.py`) that stores every raw body** (`legacy-id-control.json`). The re-run
**reproduces the result exactly**: 1 of 11, the same one, four hours later.

**The structural test predicted the measurement on every row that returned one.** Before anything was
measured, 248 of the 249 were identified as strict prefixes of a well-formed identifier captured from
the same comment, and **exactly one — `12345` — was not.** After measurement: of the **246 determinate
rows, 245 are NOT-RETRIEVABLE and the one RETRIEVABLE row is `12345`** — agreement on all 246.

**The remaining 3 rows returned no answer** (`702419516832`, `71473953160298`, `75653617056` — TLS
handshake failures, INDETERMINATE). They are **inconclusive, not confirmatory**, and the first version
of this document folded them into "all 249", which overclaimed by three rows
(`INTERLOCUTOR-2.md` condition 2). The correct sentence is the one above: **246 of 246 answered rows
agree with the prediction; 3 were never answered.**

**So the filter's error rate is measured, not assumed: 1 in 249 (0.4 %).** The 19-digit rule discards
one genuine legacy video per 249 phantoms. That is the cost of the filter, it is small, and it is now a
number rather than a hope — which it could only become because the arm was measured instead of deleted.

**The same rule applied backwards, and a correction to our own vocabulary.** Corpus A's four
non-19-digit identifiers were called "malformed" in D9. **One of them is not.**
`194951213564514304` returns **HTTP 200 in both runs**, with a 76-character title, under the handle the
citation carries — a live video. Its identifier decodes to **1971-06-10** under this arc's
`id >> 32` dating rule, which is impossible. The identifier is not malformed; **the dating rule does not
hold for identifiers outside the current scheme.** The other three return 400 and nothing more can be
said about them.

**Impact on anything published: 4 rows in 2,201, 0.18 %**, too small to move any figure session 109
reported. **Impact on how the arc talks: real.** "Malformed identifier" is replaced by "identifier
outside the scheme the dating rule assumes", and any future age statistic excludes rows whose decoded
date precedes the platform's existence rather than bucketing them in 1971.

---

## 9. Predictions, scored — including the two that failed

| | Prediction | Outcome |
|---|---|---|
| **P1** | Vantage unchanged, AS396982 | **HOLDS** — and narrower than we knew: the AS held, the **IP did not** (D11) |
| **P2** | Corpus A within ±1.0 pp of 89.3 % | **HOLDS** — 89.20 % against 89.32 %, a change of **0.128 pp** |
| **P3** | Fewer than 5 transitions, most likely 0 | **HOLDS** — **0** |
| **P4** | ≥ 100 new identifiers from the second source | **HOLDS** — **454** |
| **P5** | The second source is *younger* than corpus A | **FAILS** — corpus B is **older**. On **matched denominators** (well-formed identifiers only, both corpora — the first version compared B's well-formed against A's *whole* corpus, `INTERLOCUTOR-2.md` condition 3): **B 282/457 = 61.7 %** dating from 2023 or later against **A 1,535/2,197 = 69.9 %**. The mismatched comparison gave 69.7 % for A; the conclusion is unchanged and the arithmetic now is. The reasoning ("forum discussion tracks the present") was wrong about how a forum archive accumulates: it keeps every year it has lived through, while an encyclopedia's citations are continually replaced by newer ones |
| **P6** | The second source is *less* retrievable | **HOLDS, and only just** — 85.23 % against 89.20 %; **p = 0.017 pooled / 0.028 unpooled, 95 % CI [0.42 pp, 7.50 pp]** (§7). It would also have "held" spectacularly and falsely without the filter (§8) |
| **P7** | Transport failures ≤ 1 % | **FAILS** — **1.24 %** (36 / 2,904), all one TLS handshake class. Not fatal to anything — those rows are INDETERMINATE and counted in no rate — but the prediction was wrong and the ceiling was ours |

**Five hold, two fail.** Neither failure was discovered by an adversary; both are recorded because the
predictions were written down before the run and scored afterwards, which is the only reason a failure
is visible at all.

## 10. Kill criteria

| | Fires? |
|---|---|
| **K1** vantage moved (AS) | **No** — AS396982 both runs |
| **K2** run stopped short by throttling | **No** — 2,904 of 2,904, no 429 |
| **K3** second source yields < 50 new identifiers | **No** — 454 |
| **K4** runs disagree on > 5 % of determinate pairs | **No** — 0.000 % |
| **K5** a transition that will not reproduce | **Vacuous** — no transitions to re-request |

## 11. What the gate is owed, against what this session delivered

| Owed | Delivered |
|---|---|
| The daily run, with vantage, raw responses published | **Yes** — `ledger.py`, versioned schema, vantage inside the run file, all 2,904 responses committed. **But it is one day's second run, not day 2** (§0) |
| The corpus grown beyond one source | **Yes** — 2,201 → **2,655** well-formed units (**+20.6 %**) from a strongly independent second source, plus a 249-unit control arm |
| A first transition event, dated — or the seven-day finding | **Neither.** **Zero transitions**, on a pair that counts as **at most one day** toward the seven. The arc owes six more days before the kill can be applied, and the first evidence points at the kill |
