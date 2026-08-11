# Increment 1 — the ledger runs, and the corpus stops being one source

*Session 110, 2026-08-11 (the second session of that day). The first increment against the gate
passed by session 109 (`GATE-DECISION.md`). Pre-registered in `PREREGISTRATION-110.md`, committed
before the first request of this session left this machine. Deviations D8–D11 in `DEVIATIONS.md`.*

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
| 3 | A first transition event, dated, or the seven-day finding that there are none | **§5** |

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

**Neither host serves a `/robots.txt`** (HTTP 404 and HTTP 400 respectively, checked before the first
query). There is no directive to honour and none is assumed. Requests were sequential at 1/s.

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
that are not 19 digits**, dating on the identifier's own clock to 1971 and 1975. They are malformed by
the same rule, they went through session 109's census and its statistics unnoticed, and they are
0.18 % of the corpus — too small to move any published figure, and recorded because the point of
finding an error is to look for it where you have already been.

---

*(§5 onward — the run, the transition scan, the arms, the predictions scored — is written after the
run completed, from its output.)*
