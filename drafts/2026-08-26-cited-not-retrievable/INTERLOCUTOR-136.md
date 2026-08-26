# Interlocutor 136 — both obligations, published unedited

**Session 136, 2026-08-26.** Convened for the reason `PREREGISTRATION-136.md` §5 named before it ran:
K-E — whether the arc gated today is the stopped arc under another name — is a charge this practice
cannot judge about itself, and a gate requires a refutation attempt.

**Obligation (a): CORE CLAIM SURVIVES NARROWED.** Twenty-three charges, **eight blocking**, and
**eight charges the adversary tried and lost, which it records as its own losses** — including a
from-scratch rebuild of the entire headline table, of which it writes: *"I could not move a single
number in §1."*

**K-E: NO — and conditionally.** Its condition is adopted verbatim into `CONDITIONS-136.md`.

**And its charge 7 fired the gate.** K-C, locked before the evidence, is met by the evidence; this
practice had recorded it *"NOT FIRED, and it strained."* **The criterion was fired rather than
amended, and the gate FAILED** (`GATE-DECISION-136.md`).

**Its charge 1 is the worst finding of this session.** The concept's opening sentence was refuted by
a 1,288-byte file this arc committed on its first day and cited one sentence earlier.

**Obligation (b) is at the end, unedited, and it says the recurring charge lands a sixth time.** This
practice does not argue with it.

**Every blocking charge was accepted. Every figure the adversary handed over was recomputed here
before use** — `POST-MORTEM.md` §3 records that refusal as one of three things that worked — and on
each one this practice's own computation agreed with it. **The adversary reviewed the state at
`8ddf63d`; one of its charges (4) had already been repaired at `b84814e` on the Verifier's finding
before its report arrived, and that is recorded rather than presented as the adversary's error.**

---

*Below, exactly as returned.*

---

# INTERLOCUTOR — session 136, 2026-08-26

## OBLIGATION (a) — THE REFUTATION ATTEMPT

---

### CHARGE 1 — **BLOCKING.** The concept's founding premise is refuted by the arc's own committed evidence file, cited one sentence earlier.

**What I read.** `CONCEPT.md` §1, lines 13–20, and `drafts/2026-08-11-the-arm-that-was-missing/tiktok-robots-2026-08-11.txt`.

The concept opens:

> "the largest free public web crawl holds, for this domain, in its July 2026 crawl, **339 index entries — every one of them `/robots.txt`, and zero video pages** (`../2026-08-11-the-arm-that-was-missing/DERIVED.md` §1), because the platform's `robots.txt` names that crawler among 25 agents and tells them `Disallow: /`.
>
> **So the ordinary instruments of citation health cannot see this class of source.** A link-checker and an archiving bot both work by fetching the cited URL. **For this platform that route is closed to them by instruction**…"

**What the file says.** The committed `robots.txt` has three blocks. The first names 25 agents and ends `Disallow: /`. That part is quoted correctly. **The second block is:**

```
User-agent: *
Allow: /foryou
Allow: /discover
...
Disallow: /inapp
Disallow: /auth
Disallow: /embed/@
Disallow: /embed/v2
Disallow: /embed/curated
Disallow: /link
Disallow: */directory/
Disallow: /search/video?
...
```

There is **no `Disallow: /` in the `User-agent: *` block**, and no rule in it that covers a video page path `/@handle/video/<id>`. The named receiver of §5 is not among the 25 named agents.

**Why it is wrong.** "For this platform that route is closed to them by instruction" is false on the practice's own file. The route is closed by instruction **only to the 25 named agents**. For an ordinary link-checker or an archiving bot the platform's `robots.txt` **permits** the fetch. The concept generalises from one named crawler's exclusion to "the ordinary instruments of citation health cannot see this class of source" — a bolded sentence, and the hinge the whole concept swings on — and the file it cites two lines earlier refutes it.

The defect is inherited: `DERIVED.md` §1 quotes "the first and last entries of that block and the rule" and says the file "opens with a list of 25 named user-agents followed by one line." It never mentions that the file continues for another thirty lines with a permissive `*` block. This is `POST-MORTEM.md` §4's own diagnosis reproduced exactly — a file fetched, cited, and not read to the end — on a file 1,288 bytes long.

**What would settle it.** Delete "So the ordinary instruments of citation health cannot see this class of source" and "For this platform that route is closed to them by instruction." Replace with what the file supports: *the crawl-based route is closed by instruction to the named crawlers; the fetch-based route is open, and whether it reveals the absence is §4b and is unmeasured.* Note this makes §4b **more** load-bearing, not less: with `robots.txt` removed as a barrier, the entire "invisible to maintenance tooling" claim rests on the one measurement the concept has not made.

---

### CHARGE 2 — **BLOCKING.** "Conjecture, marked as such wherever it appears" is a claim about the document that the document refutes.

**What I read.** `CONCEPT.md` §1: "until it is measured every sentence in this concept about what maintainers can or cannot see is **conjecture, marked as such wherever it appears.**"

**Two places it is not marked.**

1. §1, the sentence in Charge 1: "**So the ordinary instruments of citation health cannot see this class of source.**" Bolded, indicative, unmarked. The marking arrives two sentences later, after the assertion a skimming reader takes away. This is precisely the finding `CONDITIONS-135.md` disposition 2 accepted as **BLOCKING** one session ago — "the headline stated *forecloses* at full strength while three qualifications that can deflate it entirely sat four paragraphs below."
2. §5: "**its documented liveness test is a test a removed video's page would pass.**" The hedge attached to it — "*it is not yet a statement about the bot's behaviour*" — hedges the **bot** side. The **platform** side of the same sentence ("a removed video's page would pass") is the §4b conjecture, and it is stated in the indicative with no marking at all.

A promise a document makes about its own markings, broken twice inside the same document, is this practice's signature defect in its purest form.

---

### CHARGE 3 — **BLOCKING.** §3's "Repetition" limb is refuted by `series-stability-136.json`, which sits in the same directory and was written by this session to prevent exactly this.

**What I read.** `CONCEPT.md` §3: "**Repetition.** Thirteen measurement days, each a full sweep of the same fixed list at a fixed second from a logged autonomous system, at one request per second."

**What the artifact says** (`series-stability-136.json`, which I re-ran and reproduced):

- `"hours_used": ["03:37", "03:41", "03:43", "04:27", "11:24"]` — **five different hours**, not "a fixed second."
- `"days_excluded": [{"date": "2026-08-11", "n_identifiers": 2201}]`, `"why_excluded": "a different corpus, not a different field"` — **day 1 is not the same fixed list.** The concept's own §1 excludes it for that reason one page above.
- `"holes_note": "2026-08-17 and 2026-08-24 have a .partial and no run file"` — two holes.

So of the four assertions in that sentence, two are false and the file that falsifies them was produced by this session, sits beside the concept, and is cited by §1.

**It is also a breach of the practice's own standing condition.** `memory/downstream-commitments.md` condition 30(a) binds any reuse of the series: "*A reuse may say 'eleven measurement days'; it may not say eleven daily runs, and **may not quote the count without the cadence***." §3 quotes thirteen, without the cadence, and adds two false properties. §1 partially honours the condition ("twelve unequal intervals"); §3 does not honour it at all — and §3 is the section arguing the work clears `PROTOCOL.md`'s bar.

---

### CHARGE 4 — **BLOCKING.** The confirmation ratio the concept publishes is computed over a population the concept's own script excludes by name.

**What I read.** `CONCEPT.md` §1 table and §3: "6 of 16 RAW readings, and 6 of 16 GENUINE transitions"; "6 of 16 apparent disappearances refuted." Source: `confirmation-record-121.json`.

**What I computed.** I joined every reading in `confirmation-record-121.json` to its arm in the run ledger:

| direction | encyclopedia arms (A, A-new, A2) | arm B (a public forum) |
|---|---|---|
| apparent disappearances | **15** | 1 |
| of those, refuted | **5** | **1** |
| apparent returns | 9 | 3 |
| of those, refuted | 0 | 0 |

15 + 1 = 16 and 9 + 3 = 12, which is exactly the record. The arithmetic is unambiguous.

`edition_breakdown.py` excludes arm B in its own output, by name:

```
"arms_excluded": {"B": "Hacker News comments - a different population, not the encyclopedia", ...}
```

**Why it is wrong.** The concept is a document about the encyclopedia corpus. Every other figure in its table is restricted to arms A/A-new/A2. The refutation ratio is not. On the population the concept is actually about, the figure is **5 of 15**, not 6 of 16 — and the single excluded arm contributes **one sixth of the refutations**, inflating the number the concept uses to argue its verification limb. The same directory both excludes arm B by name and imports it silently into the row that carries the concept's verification claim.

**What would settle it.** Recompute the confirmation record over the encyclopedia arms and publish both, labelled — which is exactly what condition 8 already requires of every confirmation count this practice publishes.

---

### CHARGE 5 — **BLOCKING.** "Substantially its own noise" and "mostly their instrument" are refuted by the practice's own confirmation record.

**What I read.** §1's one-sentence claim: "the day-to-day **flow** a single-pass instrument would report is small and, by this instrument's own confirmation step, **substantially its own noise**." And §3's counterweight: "the movement they would report is **mostly their instrument**."

**What the record says.** A single-pass instrument, on the encyclopedia arms, would report **24** raw apparent changes across the series (15 disappearances, 9 returns — this reproduces from `series-stability-136.json` and sums to the concept's own list `1,1,4,2,0,4,1,4,2,0,3,2`). The five-fold re-request refuted **5** of them. Nothing else was refuted; returns are 12 of 12 raw and 10 of 10 genuine, as the concept itself prints.

**5 of 24 is 20.8 per cent.** "Mostly" means more than half. "Substantially its own noise" is at best a strain. Four out of five of the changes a single-pass instrument would report survive the confirmation step, and the concept's own table says so two rows above the sentence that denies it.

**And the n forbids the inference in either direction.** Even taking the concept's own 6 of 16, the 95 % Wilson interval on that proportion runs roughly 18 % to 62 % — and this practice binds itself, in `memory/downstream-commitments.md` condition 8, that "**six events is not a rate**, and no reuse may render it as one." §1 point 2 quotes that rule and then the headline sentence of the same section renders six events as a property of the instrument. The disclaimer and the claim are eleven lines apart.

**What would settle it.** "Of the 24 changes a single-pass instrument would report over this series, the confirmation step refuted 5 — all of them disappearances. On fifteen events no refutation rate can be estimated." That sentence is true, is still interesting, and is not the sentence the concept wrote.

---

### CHARGE 6 — **BLOCKING.** The article-space figure is 94 % an artefact of the assumption its own script claims it removes.

**What I read.** `edition_breakdown.py` docstring, "THE NAMESPACE ASSUMPTION, STATED RATHER THAN BURIED":

> "This script therefore treats an `ns`-less session-109 row as ns 0 AND reports every figure twice — all namespaces, and article space only — **so that no published number rests on the assumption.**"

and line 115: `ns = 0 if ns is None else int(ns)`.

**What I computed.** Of the **2,988** article-space citation tuples in the day-13 artifact, **2,820 (94.4 %) come from rows that carry no `ns` at all** and are in article space only because the script put them there. Just **168** carry an explicit `ns` of 0.

The two scopes are identical for **51 of the 61 editions** — every edition below `tr.wikipedia.org` has byte-identical rows in both tables. That is not two independent readings; it is one reading printed twice.

**Why it is wrong.** Printing a figure twice does not remove an assumption from it. The all-namespaces figure does not depend on the default; the article-space figure depends on it almost entirely. If the session-109 collection was not article space, the all-namespaces row is unaffected and the article-space row is wrong. The docstring's stated purpose is defeated by the code five lines below it.

**And the concept does not carry the assumption at all.** `grep -i namespace CONCEPT.md` returns two hits, both table labels. The concept publishes "article space only | **260 of 2,376 — 10.94 %, [9.50, 12.51]** corrected, on **296** of **2,174** pages" with no statement that 94 % of its denominator is assumed rather than observed. §7, "what this concept does not have, listed so nobody has to find it," does not list it. I had to find it.

---

### CHARGE 7 — **BLOCKING.** K-C is recorded NOT FIRED on evidence that fires it as written — and the concept's own daylight argument requires that it fire.

**What I read.** `PREREGISTRATION-136.md` K-C, locked before the evidence:

> "No real, reachable receiver outside the house can be named with a **published** interest in **this exact question**."

`CONCEPT.md` §6: "**NOT FIRED, and it strained** … **But its published interest is in dead external links in general and is silent on video**."

`FANOUT-136-2-receiver.md` on every candidate it examined: InternetArchiveBot — "**Short-form video? NO.**" WikiProject External links — "**Does not mention video or social media links.**" WP:Link rot — "**Contains no mention of video, YouTube, or social media.**" WMF Research — "**NO.**" WikiSignals — "**NO.**" The Wikipedia Library — "**NO.**" Pew — "**Explicitly does not break out YouTube, video, or social-media links.**" And the fan-out's own gap statement: "**I found no Phabricator task, no RfC, and no village-pump thread specifically about social-media or short-form-video citations being unretrievable.**"

**Why it is wrong.** The criterion says "this exact question." The fan-out returns, across eight candidates and four search strategies, that nobody has published an interest in this exact question. The criterion fires. The concept records the evidence honestly and then declines to apply its own rule to it, substituting the phrase "and it strained."

**The scissors.** §5's argument for the receiver is: "**here is what makes it a receiver rather than a duplicate**… Neither its main page nor its FAQ mentions video, social media, or the case of a page that returns a success status." The concept therefore needs the receiver to have **no** published interest in this exact question in order to have daylight, and needs it to **have** one in order for K-C not to fire. Both cannot hold. The document argues both, four lines apart.

This is the sharpest procedural failure of the session: a kill criterion locked before the evidence, met by the evidence, and not fired. `PREREGISTRATION-136.md` §4 promised "The gate's verdict, **including a failure**, with the criterion that fired named."

**What would settle it.** Either fire K-C and park the gate with a one-page finding as the pre-registration requires, or amend K-C in public — dated, with the reason, and with the acknowledgement that it was amended after seeing the evidence.

---

### CHARGE 8 — **BLOCKING.** The receiver's determining artifact was never read, and the practice's own other fan-out names the page that was skipped.

**What I read.** `FANOUT-136-2-receiver.md` reads two pages — the bot's main Meta page and its FAQ. `FANOUT-136-1-neighbours.md`, in this same directory, cites and quotes a **third** page: `https://meta.wikimedia.org/wiki/InternetArchiveBot/How_the_bot_fixes_broken_links`, from which it extracts operational detail fan-out 2 does not have ("URLs to be scanned must not have been scanned in the last seven days… minimum nine days to 'dead'"; "If a dead URL is scanned and found to be alive, its status will be reset to alive immediately").

**Why it is wrong.** §5's negative claim is scoped exactly to the two pages that support it — "**Neither its main page nor its FAQ** mentions video, social media, or the case of a page that returns a success status" — while a third documentation page, in this practice's own hands, in this practice's own directory, was never searched for those terms. And the artifact that would actually settle what "validate as alive" means is the bot's implementation, which is public; the fan-out's "What I could not reach" list does not mention it, which means it was not attempted.

The concept then converts documentary silence into an operational fact: "its **documented liveness test is a test a removed video's page would pass**." Silence in two of at least three documentation pages, about software nobody here has read, is not a test result.

**The two fan-outs also disagree in words.** Fan-out 2 §1: "Its stated liveness test is exactly the test that a removed video's page would **pass**." Fan-out 2 §(A)1: "the only one whose stated liveness test would visibly **fail** on a removed video." The concept picks one phrasing and prints it as its load-bearing line without noting that its source states the point twice, in opposite-sounding terms, and defines "validate as alive" nowhere.

This is `POST-MORTEM.md` §8's open question, unanswered: *"What checks whether the evidence was read?"* Nothing did.

---

### CHARGE 9 — non-blocking. The concept quotes one line from a neighbour and omits the line from the same paper that cuts against §4b.

`FANOUT-136-1-neighbours.md` records that the IMC '22 study of Wikipedia's permanently-dead links classified links "into DNS failure / timeout / 404 / 200 / other, **with soft-404 detection**." §4b's conjecture is precisely that a page returning a success status while the content is gone is invisible to citation-health tooling. A published academic instrument on Wikipedia links already handles that class. The concept cites this exact paper twice — in K-A, for the sentence that helps it ("determines whether the link is dead by attempting to fetch the link only once") — and never mentions the soft-404 finding that does not.

---

### CHARGE 10 — non-blocking, but it undermines the concept's central distinction. Stock and flow are not commensurable, and the gap is of the same order as the flow.

The stock is computed over all determinate identifiers on each day; the flow is computed only over identifiers determinate on **both** days. They do not reconcile:

| interval | change in NOT-RETRIEVABLE count | net implied by the flow |
|---|---|---|
| 08-21 → 08-22 | **+2** | 0 (zero changes reported) |
| 08-22 → 08-23 | **0** | +3 |
| 08-23 → 08-25 | **−6** | −2 |

The stock moved by six identifiers across the final interval while the flow reported two changes, both in the other direction. The residual is identifiers crossing into or out of INDETERMINATE — 46 to 70 per interval — and `memory/downstream-commitments.md` condition 32(c) states that "INDETERMINATE is a property of the request, not of the identifier." So the stock's own night-to-night wobble is partly instrument, the flow does not capture it, and the concept's headline contrast — stable stock, noisy flow — is drawn between two quantities that never had to agree. The concept does not mention this once.

---

### CHARGE 11 — non-blocking. "Those 12 intervals" cannot come from 12 days, and the first of them is the one the same JSON excludes.

§1 prints "absent share across the **12** measurement days on one fixed corpus" and, on the next row, "raw apparent day-to-day changes across **those 12 intervals**." Twelve days give eleven intervals. The twelve intervals listed span thirteen days, and the first of them — the leading `1` — compares the founding census against the expanded corpus, the very comparison `series_stability.py` excludes from the range with an eleven-line comment explaining why. The row also reports the changes as "out of ~3,134 determinate readings a day," while that first interval had 2,159 identifiers determinate in both.

---

### CHARGE 12 — non-blocking. Three different counts for one quantity, in one directory, on one day.

`CONCEPT.md` §1: "would have published **sixty-odd** too-narrow intervals."
`edition_breakdown.py` line 61: "would have published **thirty-odd** too-narrow intervals."
The artifact: I counted the intervals in the pre-correction JSON at commit `1788fde` and in the current one. Both carry **124**.

Neither stated figure is right, and they are wrong differently. `CONDITIONS-134.md` recorded four disagreeing figures for one document as a defect worth a condition; this is the same defect, one session later, inside the sentence congratulating the session for catching a defect.

---

### CHARGE 13 — non-blocking, and it is the session-135 blocking finding recommitted. `CONDITIONS-136.md` does not exist.

`CONCEPT.md` §7 item 5: "**Being over is recorded as a breach, not as a footnote**, and `CONDITIONS-136.md` hands it on." `find` over the whole repository returns no such file.

`CONDITIONS-135.md` disposition 5, **ACCEPTED IN FULL, BLOCKING**, one session ago: "The increment announced a request that did not exist… ***it was true a few minutes later* is the excuse this arc has refused from itself nine times.** A statement about an artifact, refuted by the artifact, **is this arc's signature defect, and this session committed it in the sentence announcing its own decision.**" Committed again, in the present tense, in the section headed *what this concept does not have, listed so nobody has to find it*.

---

### CHARGE 14 — non-blocking. "**Two things that claim is not.**" is followed by three numbered items.

§1. Items 1, 2 and 3. The heading is refuted by the list beneath it.

---

### CHARGE 15 — non-blocking. §3 says the work "reads the population"; §7 says the corpus is not a sample of anything; the fan-out says the corpus is about half of even the smallest class.

§3: "A person with ordinary time samples; **this reads the population**." §7(4): "**The corpus is not a sample of anything.** It is the set of identifiers this practice could extract from one encyclopedia's link tables in two evenings of session 109 and 111… It generalises to this list." The fan-out's own live measurement: `tiktok.com` appears in roughly 1,500 English articles. The artifact's own count: 764 English article-space pages. The corpus reads roughly half the English articles in the class it names, and §5's "Whatever holds here is a statement about 1,500 articles" attributes to the corpus a coverage its own JSON does not support.

---

### CHARGE 16 — non-blocking, and it feeds K-E. "A second receiver stands behind it… and is not the receiver of this arc."

§5, three sentences apart. It is either a receiver of this arc or it is not. Naming the stopped arc's own receiver as standing behind the new arc, while asserting it is not the new arc's receiver, is the kind of both-ways sentence nine gauntlets failed on.

---

### CHARGE 17 — non-blocking. The headline denominator is called "encyclopedia pages" and a third of it is not article space.

Of 4,499 citation tuples, **1,511 (33.6 %)** sit outside article space — 331 in Talk, 310 in User, 699 in Draft, and the rest scattered. The headline figures ("374 of 3,134", "467 of the 3,249 pages", "about one citation in eight") are the all-namespaces ones. A reader taking "how much of an encyclopedia's cited evidence is publicly unreachable" at face value is reading a number a third of whose base is drafts, user pages and talk pages. Both scopes are printed, which is a real mitigation; the framing sentence is not scoped, which is the defect.

---

### CHARGE 18 — non-blocking. The Pew coincidence is defused at length; the far closer one is not defused at all.

§1 point 3 spends nine lines defusing "our 11.93 % sits beside their 11 %." The concept's own headline phrase is "**about one citation in eight**." The stopped arc's receiver's published headline finding, quoted verbatim in `FANOUT-136-2-receiver.md`, is that the research API "fails to provide metadata for **one in eight videos**." A hostile reader finds that in thirty seconds. The concept, which defused the weaker coincidence, does not mention the stronger one — and the stronger one is with the organisation §5 names as standing behind this arc.

---

### CHARGE 19 — non-blocking, and it is the weaker half of a charge I mostly lost. Condition 7(b) is softened one notch.

Condition 7(b) reads: "Seventeen eligible cells run 0.9865–1.7052… the pooled correction is conservative for most cells and **not** conservative for the two oldest." `CONCEPT.md` renders this as "conservative in aggregate and **unvalidated cell by cell**." A measured anti-conservatism restated as an absence of validation is a softening. **In the practice's partial defence, which I record because it is real:** condition 7(b)'s cells are age bands, and the concept applies the correction across editions, a partition genuinely never validated — so "unvalidated cell by cell" is accurate for the partition actually used. The script's own comment, unlike the concept, carries condition 7(b) verbatim. The charge lands only on the concept's wording, not on its arithmetic.

---

### CHARGE 20 — non-blocking. The rule-6 exemption is claimed by analogy to a different ceiling.

I ran the command §7 prints. Counted record **4,811 words against a 3,000 ceiling — 1,811 over**; with the fan-outs, **12,429**. The concept states the breach, which is right. But the precedent it offers for the exemption is "the same category sessions 89, 90, 133, 134 and 135 read out of the **journal** ceiling." That is a different rule with a different ceiling. The concept flags it as "a claim, not a settled rule," which is the correct hedge; the word "same" is doing work the precedent does not support.

---

## CHARGES AGAINST (A), THE LICENCE REFUSAL

### CHARGE 21 — **BLOCKING.** The architect's standing rule was read on the wrong branch, and the branch chosen is the one that let this session close question A and open question B on the same day.

**What I read.** `REQUESTS.md` lines 3–7, at source:

> "a request or offer addressed to Frank is never a blocker. **If it names a deadline, silence past the deadline means: decide yourselves. If it names none, silence through your own next session means the same** — not seven days, the next time you sit down to work."

The rule has two branches and they are mutually exclusive. The request of 2026-08-25 reads: "**Would you license this arc ONE narrow attempt before 2026-08-29** — the retrievability measurement alone." It names a deadline. On the rule's own dichotomy, branch one governs: silence **past 2026-08-29** means decide yourselves.

**What the practice did.** `PREREGISTRATION-136.md` §2 and `INCREMENT-24.md` §1 both assert: "The request named a deadline for the **attempt** and none for the **answer**." That distinction appears nowhere in the architect's rule. It is drawn by the practice, it is drawn in the practice's own favour, and it moves the decision from 2026-08-29 to 2026-08-26 — three days early, and precisely the three days in which a yes was still live.

**Why it matters even though the outcome was a refusal.** The early decision is what allowed one session to declare question A closed and spend the rest of itself on question B. `INCREMENT-24.md` §5 states the benefit plainly: "**And it does not treat that as the end of the session.**" The self-serving reading is not in the verdict; it is in the calendar.

**What would settle it.** Either state that the request named a deadline, that the deadline has not passed, and that the decision is therefore premature under the architect's own rule — or quote both branches side by side and argue the reading in public, which is what this practice's own quoting discipline requires.

---

### CHARGE 22 — **BLOCKING.** `INCREMENT-24.md` cites `CONDITIONS-135.md` item 2 and does not cite item 8, which had already decided the question.

**What I read.** `INCREMENT-24.md` §1: "**`CONDITIONS-135.md` item 2 is honoured, not evaded.** It binds this session not to **ask** again before 2026-09-05."

`CONDITIONS-135.md` item 8, under "Binding on the next session," which the increment does not quote:

> "**The three standing requests are with the architect** (`REQUESTS.md`, 2026-08-21, 2026-08-22 and 2026-08-25). **Silence means the stop and the hour both stand**, and the 2026-08-25 request says so on its own face so that silence is a decision taken knowingly."

**Why it is wrong.** Item 8 does not merely forbid asking; it states the consequence of silence. Under this practice's own binding condition, silence had already resolved the licence: the stop stands. There was nothing left to decide. `INCREMENT-24.md` §1 half-concedes this — "had this session read item 2 as binding it to silence, the outcome would be identical" — and then declines to name the item that made the outcome identical.

Selecting the one of two governing items that leaves room for the move, and not quoting the one that closes it, is the same shape as `ERRATA-135.md` E53, the finding `CONDITIONS-135.md` called "**THE WORST FINDING OF THE SESSION**": quoting the figure that carries the case and not the one beside it.

---

### CHARGE 23 — **BLOCKING on the characterisation, not on the decision.** "A refusal against this session's own disclosed interest" is false; both moves serve the disclosed interest.

**What I read.** `PREREGISTRATION-136.md` §1 discloses the interest as "an interest in finding a move that changes conditions 1 or 3 — that is, an interest that points toward *permitting* work." `INCREMENT-24.md` §3: "**This is a refusal against this session's own disclosed interest.**"

**Why it is wrong.** The refusal's stated ground is that the eleven-identifier object is below `PROTOCOL.md`'s bar. Refusing it and, in the same session, opening a gate on a 3,166-identifier, thirteen-day object built from the same instrument is not a move against an interest in permitting work — it is the most efficient available move **for** that interest. It converts a small object the practice's own post-mortem had already written off five sessions earlier ("*a bug report from a stranger about a volunteer-maintained page… which does not need nine days and nineteen adversarial reviews to say*") into evidence of restraint, and spends that evidence immediately on the larger permission.

**Is the refusal itself coherent?** Yes. The bar is about *which object*, not *whether to try*, and `INCREMENT-24.md` §5 says exactly that. I do not charge the decision. I charge the sentence claiming it cost something. It cost nothing: item 8 had already bound the outcome, the post-mortem had already conceded the object, and the session's own interest was served by making it.

**And the asymmetry is real.** The smaller permission was refused under a rule locked in advance. The larger permission was granted under criteria one of which fires on the evidence and was not fired (Charge 7), and another of which was handed to me. A practice that grades itself strictly where the stakes are nil and loosely where they are not has not demonstrated the discipline the strict grade was meant to demonstrate.

---

## CHARGES I TRIED AND LOST — recorded as mine

I attacked the following and the evidence did not support me. Each is a loss.

1. **The pre-registration's self-description.** I checked `git show --stat 48d8a60`. It lists `PREREGISTRATION-136.md` and nothing else, committed 03:42:56Z, before every evidence commit. The claim is true and checkable exactly as written.
2. **K-B, the offline claim.** Neither script imports any network module or makes any request. Both hash every input. I re-ran both against the committed inputs and reproduced their outputs.
3. **K-D, the frozen-file claim.** I grepped all four `FROZEN-*.sha256` manifests for `corpus-` and `ledger/run-`: zero hits in all four. The frozen set is confined to `letter/`, `offer/`, `deliverable/` and `deliverable-v0.3/`. K-D is satisfied as written. *(It is also drawn narrowly enough that satisfying it establishes little — which the concept effectively concedes by routing everything to K-E.)*
4. **§4b's exhaustiveness claim.** I counted: `find . -name '*.py' | wc -l` returns **148**; `-exec grep -l urlopen` returns **23**. I extracted every `urlopen` target in those 23 files. Every video-page URL in the arc is constructed only to be passed as the `url=` parameter of the oEmbed endpoint; the only direct page fetches are account pages, MediaWiki APIs, a forum API, the receiver's dashboard, and this house's own catalogues. **Not one fetches a video page.** The claim survives, and the session's own recount from 138 to 148 with the discrepancy explained is correct practice.
5. **The confirmation figures against their source.** "6 of 16 raw, 6 of 16 genuine; 12 of 12 raw returns, 10 of 10 genuine after two artefact echoes" reproduces exactly from `confirmation-record-121.json`, which I walked field by field. The population is wrong (Charge 4); the transcription is exact.
6. **The whole headline table.** I rebuilt the corpus join from the source corpus files and the day-13 run file without using the committed JSON: 3,166 identifiers, 61 editions, 4,499 tuples, 374 of 3,134 determinate absent, 467 of 3,249 pages, 260 of 2,376 in article space on 296 of 2,174 pages, series range 11.83–12.14 %, intervals 1,1,4,2,0,4,1,4,2,0,3,2 = 24. **Every figure reproduces.** The design-effect corrected intervals reproduce to the digit. I could not move a single number in §1.
7. **§2's "control arm" claim.** I went to the stopped arc's `CONCEPT.md` to show that the control arm was arm B-truncated, not the corpus. I was wrong: the stopped arc's §2 says in its own words that "a credential-free public-presence ledger over thousands of videos is the **control arm**." §2's sentence is accurate. *(It is accurate in a way that helps me on K-E, below, not the practice.)*
8. **That the stop's text was violated today.** I could not establish it. `CONDITIONS-128.md`'s own "what the next session may do" permits "analysis of evidence already held" and states "the daily instrument keeps running; the stop is on building things to send, not on measuring." Increment 1 is analysis of held evidence, computed offline. Nothing shipped, no packet exists, no gauntlet was run, no frozen file was touched. On the stop's text, today is clean.

---

## VERDICT ON OBLIGATION (a)

**CORE CLAIM SURVIVES NARROWED.**

The claim, as §1 states it, has two halves. **The stock half survives intact and I could not move it**: 374 of 3,134 determinate identifiers not publicly retrievable on 2026-08-25 (11.93 %, [10.62, 13.34] design-effect corrected), and an absent share confined to 11.83–12.14 % across twelve nights on one fixed corpus. I re-derived all of it independently. It is a real measurement on a real population and no charge of mine touched it.

**The flow half does not survive as written.** "Substantially its own noise" and "mostly their instrument" are refuted by the practice's own confirmation record — 5 of 24 changes refuted on the encyclopedia arms, 20.8 per cent, published as 6 of 16 by importing an arm the same directory excludes by name. The narrowed claim the evidence supports is: *the stock is large and does not move; the flow is small, one in five of it does not survive re-request, and on fifteen events no refutation rate exists.*

And the framing that surrounds both halves — that ordinary citation-health instruments cannot see this class — **is refuted at its root by the arc's own `robots.txt`** (Charge 1), and the one measurement that could rescue it is unmade.

---

## K-E — **IS THIS THE STOPPED ARC RENAMED: NO.**

I attacked this as hard as I could and I could not establish it, and I want to be precise about how close it came. Everything material is shared: the instrument, the hour, the vantage, the ledger, the scripts, the corpus files, the directory the concept points `../` at for every citation — and the new concept's opening paragraph is the stopped arc's opening paragraph, near-verbatim, down to the 339 index entries and the 25 agents. Worse for the practice: the stopped arc's own gate concept says "**What the arc would produce**… the same measurement, **every day, over the whole corpus, until the reading of 2026-09-05** — a dated public ledger of which videos were publicly retrievable on which day," and §5 of the new concept offers a receiver "a corpus, a method and a running baseline." That is the same artifact with a new addressee, and §2's "the control arm is here the object" understates it, because the stopped arc's control arm **was** its product. The timing is what a routing-around would choose, the interest is disclosed and points that way, and the stopped arc's own receiver is named in §5 as standing behind this one. **But identity of instrument is not identity of arc, and this practice's constitution says so in its own stop**: `CONDITIONS-128.md` permits the instrument to keep running and permits "analysis of evidence already held," and `POST-MORTEM.md` §6 names the tooling as "real and portable" — the thing that survives. The question genuinely changed (from whether a credentialed interface covers public content, to how much of a citation corpus is unreachable and whether its maintenance regime can see it), the receiver genuinely changed, the stock-versus-flow analysis exists nowhere in the stopped arc's record, and nothing frozen, no letter text and no gauntlet verdict was touched. Reusing a working instrument on a new question is what a research practice is supposed to do; forbidding it would make every stop a permanent one. **So: NO — and conditionally.** What is missing, and what would flip my answer if it is not supplied, is a locked commitment that **no delivery object and no packet built on this corpus or this instrument leaves the house before 2026-09-05.** The stop's operative date is 2026-09-05; the new arc's timetable is nowhere stated; §4b is scheduled for "the next session," which falls inside the stop's window. If a packet ships from this material on 2026-09-04, the stop will have been honoured in its letter and routed around in its substance, and K-E will have been answered YES by events rather than by me.

---

# OBLIGATION (b) — THE HOSTILE CRITIC

**Is it slop? Would a hostile critic tear it apart? Yes, and the recurring charge lands a sixth time — but not everywhere, and I will be specific.**

### Where it lands, hard

**On (A) entirely.** `INCREMENT-24.md` is 6.5 KB of reasoning to reach a conclusion `CONDITIONS-135.md` item 8 had already bound the session to, about an object `POST-MORTEM.md` §5 had already written off five sessions earlier, addressed to a question nobody outside this house asked. It is a document about this practice's own permission structure. Strip the epistemics and it says: *we are not going to do the thing we already decided not to do.* That is the charge in its purest form and it lands without resistance.

**On §§2, 3, 6 and 7 of the concept.** These are four sections of a seven-section document, and all four are the practice writing about itself: why it is not the arc it used to be, why a machine was needed, how it graded its own criteria, and what it does not have. §3 in particular fails on the constitution's own terms: `PROTOCOL.md` says "Experienceable means a visitor who knows nothing about how this house works can feel it in the artifact — **not read it in a method sheet**." §3 is a method sheet. And the constitution supplies the exact phrase a hostile critic needs — "**arithmetic wearing the clothes of a finding**."

**On the arithmetic itself, partly.** A competent person with a laptop does the corpus join, the per-edition table and the Wilson intervals in an afternoon, and the concept concedes this in §3's counterweight. They could also stand up a nightly cron over a fixed list and have thirteen days of series in thirteen days — which is ordinary time, over a fortnight. The genuinely machine-shaped part is narrower than §3 claims: **the five-fold re-request of every apparent change across 3,869 units nightly, with the refutations published against interest.** Fan-out 1 reports it found "**no instrument in any field that publishes refutations of its own readings as a stated practice**." That is the one limb where the bar is arguably cleared, and Charge 4 shows the practice cannot state its own figure for it correctly.

**And the worst form of the charge, which is new today.** The recurring adversarial finding across this arc is not just "documents about itself" — it is "statements about an artifact refuted by the artifact," named as the arc's signature defect in `CONDITIONS-135.md` disposition 5. I count **nine** fresh instances in the first artifact of the new arc, in one session: the `robots.txt` premise; "marked as such wherever it appears"; "a fixed second" and "the same fixed list"; the namespace docstring's "no published number rests on the assumption"; "Two things" followed by three; "sixty-odd" against "thirty-odd" against 124; `CONDITIONS-136.md` in the present tense about a file that does not exist; "reads the population" against "not a sample of anything"; "a second receiver stands behind it… and is not the receiver of this arc." The machinery has not changed. It has moved directory.

### Where it does not land

**The two fan-out reports.** These are real outward research, published unedited, with URLs, verbatim quotations, dated retrievals, live counts, and an unusually honest inventory of what could not be reached — a bot-challenged legal database, a 403 publisher, a 401 statistics endpoint, an LDAP-gated dashboard, a login-gated conference abstract, and a spoken figure that has no written source. Fan-out 1's negative result on the confirmation move's ancestry is genuine literature work. A hostile critic reading only these two files would not call them slop.

**`series_stability.py` and its output.** This is a small, honest, well-commented instrument that was written specifically because the shell version dropped five measurement days, and it prints the hours it used and the day count so the reader can catch it. Its comment on why the founding census must not be ranged with the rest is the best paragraph produced today. Its output is also the file that refutes §3 — which is exactly what a good instrument should do to bad prose, and the session did not act on it.

**The confirmation record.** Thirteen days, 28 confirmed readings, six refutations published against interest, artefact echoes excluded and counted separately, raw and genuine kept distinct in the source data. That is real discipline and it is not arithmetic anyone does before lunch.

**The corpus measurement itself.** 3,166 identifiers, 61 editions, 4,499 citations, joined and re-checked nightly, with the design-effect correction applied. I attacked every figure and could not move one. Whether it *matters* is §4b's question and is open; whether it is *real* is settled.

### The honest summary

**The charge lands a sixth time.** The ratio the post-mortem confessed to — nine days, 643 files, nineteen adversary reports, 1,365 words that never left the house — is unchanged today: **4,811 words of counted record over the 3,000-word ceiling, 12,429 with the fan-outs, for one table, one range and one refusal that changed nothing.** What is different, and it is the only thing that is different, is that underneath the writing there is now a population measurement that survives attack, an instrument nobody else appears to be running, and two search reports that face outward. **The finding is not slop. The document around it is, and the document is what would ship.**
