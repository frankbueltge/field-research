# Verifier 136 — independent recomputation, published unedited

**Session 136, 2026-08-26.** Convened for the reason `PREREGISTRATION-136.md` §5 stated before it
ran: an increment computed from a ledger by this session's own scripts is exactly what an
independent recomputation exists to check, and the check is against the data, never against the
reasoning that produced the figures. **The Verifier was instructed not to import or run the scripts
under test and reports that it wrote its own from scratch.**

**Verdict: PASS WITH FINDINGS.** Nine findings, all marked non-blocking by the reviewer, three of
which it flagged as deserving action before the adversary saw the document. **All three were
accepted and applied**, along with three more, and the dispositions are in `CONDITIONS-136.md`.
**Every quantitative figure reproduced from the raw data** — the entire series file and all 122
per-edition rows with zero field mismatches against a from-scratch recomputation.

**The state reviewed was commit `4775d5d` and the document has moved since.** The reviewer says so
itself in its opening note, and one of its findings (the stale script count in §4b) had already been
repaired at `8ddf63d` before the report arrived. That is recorded rather than presented as the
reviewer's error.

**One correction runs against this practice and it is the most consequential finding of the
session:** the confirmation count published as the last row of §1's table was computed over **all**
arms, in a table every other row of which is scoped to the encyclopedia. **This practice did not
adopt the reviewer's replacement figures on trust** — `POST-MORTEM.md` §3 records that refusal as
one of three things that worked, and it is applied here to this practice's own reviewer.
`confirmation_by_arm.py` recomputes them, and **agrees with the reviewer on both**: 5 refuted of 15
raw apparent disappearances, 9 of 9 raw returns confirmed.

---

*Below, exactly as returned.*

---

# VERIFICATION REPORT — session 136 figures, 2026-08-26

**Method.** I wrote four throwaway scripts of my own in `/tmp/…/scratchpad/` (`v1.py`–`v7.py`, `q.py`) and ran them against the raw run files, corpus files, sidecars and prose. I did not import, execute, or read the logic of `edition_breakdown.py` or `series_stability.py`. My join rule was the one stated in the brief: `row['wiki']` else `meta['wiki']`, `row['ns']` else 0; arms `A`/`A-new`/`A2` only; `.partial` and `*-second-probe.json` excluded.

**Note before the findings.** `CONCEPT.md` changed under me during the check. My first read (≈04:00Z) returned a table row reading `**6 of 16**` with no label; the version at `HEAD` (commit `4775d5d`, 2026-08-26T03:58:10Z, *"Confirmation counts labelled raw and genuine…"*) carries `6 of 16 RAW readings, and 6 of 16 GENUINE transitions`. **All findings below are against the `HEAD` version**, which is what `git status` shows as clean on disk.

---

## Findings

### 1. Corpus figures — NON-BLOCKING (all four reproduce exactly)
Ran my own join over all 50 corpus files (47 `corpus-*.json` + 3 in `expansion-111/`). Got: **3,166** distinct encyclopedia-arm identifiers, **61** distinct editions, **4,499** distinct `(wiki, ns, page, vid)` citation rows, **0** identifiers unattributable to an edition. Document says 3,166 / 61 / 4,499 / 0. **Exact match on all four.**

Two structural notes I checked rather than assumed: `corpus-merged.json` stores `rows` as a dict keyed by vid and its rows *do* carry `wiki`, so it is attributable — and all 2,201 of its tuples are already present in the per-edition files (0 unique), so its inclusion double-counts nothing. `corpus-hn.json` is the only file whose 890 rows carry no wiki at any level; all its identifiers are arm B and correctly contribute nothing.

### 2. The 2026-08-25 day figures — NON-BLOCKING (reproduce exactly)
From `ledger/run-2026-08-25T0341Z.json`, arms A/A-new/A2: 3,166 observations, no duplicate vids, no conflicting states. **RETRIEVABLE 2,760 · NOT-RETRIEVABLE 374 · INDETERMINATE 32 · determinate 3,134 · absent share 0.11933631142310147 = 11.93 %.** Pages: **3,249** distinct `(wiki, ns, page)` citing any of these videos, **467** carrying ≥1 absent citation = **14.373653431825176 % = 14.37 %.** Every one matches the published file and CONCEPT §1. The published `citation_row_level` block (568 / 3,889 / 42) also reproduces exactly.

### 3. Article space (ns 0) — NON-BLOCKING (reproduces exactly)
Restricting to `ns == 0`: 2,400 distinct identifiers, 2,988 citation rows, **260 NOT-RETRIEVABLE of 2,376 determinate = 10.942760942760943 % = 10.94 %**, on **296 of 2,174** pages = **13.615455381784727 % = 13.62 %**. All match. The published `n_editions: 61` for ns 0 also reproduces (all 61 editions have at least one article-space row).

### 4. The confidence intervals — NON-BLOCKING (arithmetic is right, to 16 digits)
I recomputed Wilson from scratch with `z = 1.959963984540054`:
- plain 95 % Wilson on 374/3134 = `[0.10844986864186074, 0.13115479867082797]` — **identical** to the published `wilson95_uncorrected_do_not_publish_alone`, and rounds to **[10.84 %, 13.12 %]** as CONCEPT states.
- `sqrt(1.4289) = 1.1953660527219268` — **identical** to the file's `half_width_inflation`, and to condition 7's `×1.1954`.
- half-width × that factor about the same Wilson centre = `[0.10623198236331730, 0.13337268494937141]` — **identical** to the published corrected interval, rounding to **[10.62 %, 13.34 %]**.
- The ns-0 pair `[9.50, 12.51]` / `[0.0975000683273193, 0.12261604776063151]` likewise reproduces exactly.

`memory/downstream-commitments.md` condition 7 was read at source: it does say **1.4289**, **at least ×1.1954**, **citing-page key gives 1.8854**, **seventeen eligible cells run 0.9865–1.7052**. CONCEPT §1 and the JSON's `interval_correction` block reproduce all four correctly. **The arithmetic is right.**

One methodological note, not an arithmetic error: the correction inflates the half-width about the *uncorrected* Wilson centre (0.1198) rather than recomputing Wilson at an effective n. The result is an interval that is not centred on 11.93 % and is slightly wider than an `n_eff = n/deff` Wilson would be. This is exactly what the document says it does, and it is the conservative direction.

### 5. The measurement-day series — NON-BLOCKING (every field reproduces, 0 mismatches)
I enumerated run files myself: **13** measurement days, hours **03:37, 03:41, 03:43, 04:27, 11:24**. I then diffed *every* field of the published `days` array — including all thirteen `run_file_sha256` values, which I recomputed — against my own: **zero mismatches across all 13 days and all 12 interval blocks.**

- **2026-08-17** and **2026-08-24**: confirmed — a `.partial` exists (`run-2026-08-17T0337Z.json.partial`, `run-2026-08-24T0341Z.json.partial`) and no run file. Correct.
- All-days range: min 0.10804597701149425, max 0.12140575079872204 → **10.80 %–12.14 %**, range 1.3359773787227789 pp. Matches.
- Modal identifier count is 3,166, held by exactly **12** of 13 days; the one excluded is **2026-08-11** at n = 2,201 (the founding census, before the expansion). Range over those 12: min 0.11826585910105196, max 0.12140575079872204 → **11.83 %–12.14 %**, **0.313989169767008 pp**. Matches CONCEPT's "0.31 pp".
- `manifest-day2-onward.json` exists, as the `why_excluded` note asserts.

*Observation, not a defect:* `run-2026-08-26T0341Z.json.partial` also exists (today's run, in flight) and the `holes_note` names only 08-17 and 08-24. That is correct for a series that ends on 08-25, but a reader counting partials in the directory will find three.

### 6. The change sequence — NON-BLOCKING (reproduces exactly)
Counting only identifiers determinate in **both** of two consecutive measurement days, my recount gives **1, 1, 4, 2, 0, 4, 1, 4, 2, 0, 3, 2 — total 24**, matching the published sequence exactly. The published `identifiers_determinate_in_both`, `to_NOT-RETRIEVABLE`, `to_RETRIEVABLE`, `identifiers_touching_INDETERMINATE` and `calendar_days_between` for all 12 intervals also match mine field-for-field.

**Sub-finding, NON-BLOCKING — a wrong antecedent.** CONCEPT §1 row 7 reads *"absent share across the **12** measurement days on one fixed corpus"* and row 8 immediately follows with *"raw apparent day-to-day changes across **those 12 intervals**"*. They are not the same twelve. The 12 intervals span **13** days and the first of them (`2026-08-11 → 2026-08-12`, contributing 1 change on only 2,159 identifiers determinate in both) crosses the corpus change that row 7's exclusion exists to remove. Within the fixed-corpus 12 days there are **11** intervals, totalling **23** changes. The numbers are right; the pointer "those" is wrong. Row 8's hedge "out of ~3,134 determinate readings a day" is also loose: the per-interval both-determinate denominators run 2,159–3,120.

### 7. The confirmation figures — NON-BLOCKING, but this is the most consequential finding
I recounted `confirmation-record-121.json` from its own 28 `readings` **and** independently from the 12 sidecar files it names (all present; every `sidecar_sha256` recomputed and matching; sidecar `from`/`to` fields summed independently).

| published phrase | which count it is | at source | verdict |
|---|---|---|---|
| "6 of 16 RAW readings" | `all_readings["RETRIEVABLE->NOT-RETRIEVABLE"]` — n 16, confirmed 10, refuted 6 | ✓ | correct |
| "6 of 16 GENUINE transitions" | `genuine_transitions_only["RETRIEVABLE->NOT-RETRIEVABLE"]` — n 16, confirmed 10, refuted 6 | ✓ | correct; they do coincide |
| "raw is 12 of 12 confirmed" | `all_readings["NOT-RETRIEVABLE->RETRIEVABLE"]` — 12 of 12 | ✓ | correct |
| "genuine is 10 of 10" | `genuine_transitions_only["NOT-RETRIEVABLE->RETRIEVABLE"]` — 10 of 10 | ✓ | correct |
| "after two of this arc's own artefact echoes are excluded" | `n_artefact_echoes: 2`; I counted 2 flagged, both in the returns direction | ✓ | correct |

**CONCEPT.md labels each one correctly.** The mapping in §1 row 9 and §1 item 2 is right in every particular.

**But the population is not the table's population.** I resolved each of the 28 readings to its arm in the 2026-08-25 run. **Four of the 28 are arm B (Hacker News) identifiers** — `7118519163416497450`, `7188619321193549099`, `7358144823108373803` — the very arm `edition-breakdown-day13.json` explicitly excludes as *"a different population, not the encyclopedia."* Restricted to the encyclopedia arms the raw counts are **5 refuted of 15 apparent disappearances**, and **9 of 9 returns confirmed**. (Those 15 and 9 are exactly the `to_NOT-RETRIEVABLE` and `to_RETRIEVABLE` sums from finding 6 — an internal cross-check that both my recomputations agree.) The figure "6 of 16" is a faithful quotation of its cited source, but it sits as the last row of a table in which every other row is scoped to the 3,166 encyclopedia identifiers, and §3 sets it directly against "24 changes" — which *is* encyclopedia-only. A reader dividing one by the other is comparing two populations. Nothing in CONCEPT.md says so.

**Condition 8 — honoured in one place, breached in three.** I read condition 8 at source: *"A confirmation count travels with the word 'raw' or 'genuine', or it does not travel."* The §1 table row now carries both words ✓. But three confirmation counts still travel bare:
- §1 item 2, line 72: *"six of sixteen confirmed disappearances refuted across the series"* — no label. The wording is also wrong on its face: there is no set of sixteen *confirmed* disappearances; sixteen were apparent readings, of which **ten** were confirmed and six refuted. This contradicts the table three lines above it.
- §3, line 122: *"6 of 16 apparent disappearances refuted"* — no label.
- `series-stability-136.json`, `not_a_transition_count`: *"has refuted six of sixteen apparent disappearances"* — the note's leading word "RAW" governs the day-to-day changes, not this count.

### 8. Per-edition rows — NON-BLOCKING (all 61 × 2 sections reproduce; the unit defect is genuinely fixed)
I rebuilt every edition row from scratch and diffed all 61 rows in `all_namespaces` and all 61 in `article_space_only`. Spot-checks requested: **en** (all-ns 1,343 ids / 1,428 rows / 171 NR / 1,330 det / 12.857 %; ns0 853 / 906 / 90 / 844 / 10.664 %), **es** (all-ns 318 / 589 / 54 / 318 / 16.981 %; ns0 268 / 274 / 49 / 268 / 18.284 %), and small ones **af** (1/1/0/1), **hi** (1/1/0/1), **lv** (1/1/1/1, absent share 1.0). **Every count field, every page count, every `absent_share` and every uncorrected interval matches, in both sections, for all 61 editions.**

**Unit consistency: confirmed fixed.** For all 122 rows, `RETRIEVABLE + NOT-RETRIEVABLE + INDETERMINATE == distinct_identifiers` and `determinate == distinct_identifiers − INDETERMINATE`. Zero inconsistencies. The share and its n are in the same unit, and each row names it. I also reproduced the *old* defect described in §4a to check the account of it is true: en all-namespaces **row-level** determinate is **1,414** against **1,343** distinct identifiers — exactly the pair CONCEPT §4a reports. That account is accurate.

The only per-edition difference between my recompute and the published file: for 36 editions the published `wilson95_deff_corrected` is **clamped to [0, 1]** where my naive computation runs to e.g. `[-0.0775, 0.8710]` (af) or `[0.1290, 1.0775]` (lv). Clamping to the parameter space is the right choice; I record it so the difference is not mistaken for an error. The uncorrected intervals are unclamped in the file and match mine exactly.

### 9. `INCREMENT-24.md` — NON-BLOCKING (every quotation is verbatim; the request and the absence of an answer both check out)
Exact-substring checks after whitespace normalisation:
- **`REQUESTS.md` standing rule (Frank, 2026-07-17)**, lines 3–7 — the full blockquote in §1 is **verbatim**, including the em-dashed *"not seven days, the next time you sit down to work"* clause. ✓
- **`PROTOCOL.md`'s bar** — *"If a competent human with ordinary time could have made the same work, this house has no reason to be the one that made it"* is at `PROTOCOL.md:90–91`, **verbatim**. ✓ (§2 frames it as "the bar restated in one sentence"; it is in fact a direct quotation, which is the safer of the two errors.)
- **`POST-MORTEM.md` §5** — *"a bug report from a stranger about a volunteer-maintained page… which is a kind and useful thing to send someone, and which does not need nine days and nineteen adversarial reviews to say"* is at `POST-MORTEM.md:130–132`, **verbatim**. ✓
- **The request it answers.** `REQUESTS.md:1749–1757` — *"Added after this practice's own adversary attacked the request above, 2026-08-25"* → *"Would you license this arc ONE narrow attempt before 2026-08-29 — the retrievability measurement alone, and nothing else from the letter?"*, scoped at line 1760–1762 as ten of eleven identifiers. INCREMENT-24 §1 and §3 describe it accurately. ✓
- **No architect answer.** I read every `Status:` line and every occurrence of "Frank" in all 1,796 lines of `REQUESTS.md`. The architect's last entry is a Team note of **2026-08-22**; the 2026-08-25 request's status is *"ANSWERED BY THIS PRACTICE, 2026-08-26"*. **No answer from the architect exists anywhere in the file.** ✓
- **The locked rule.** `PREREGISTRATION-136.md` §2's decision rule is **verbatim** in INCREMENT-24 §2, and `git show --stat 48d8a60` confirms the commit carrying it changed **1 file, 111 insertions** — that file and nothing else. ✓
- **§3's supporting claims.** *"The four repeat readings the arc took (2026-08-12, -19, -20, and a reviewer's)"* reproduces `POST-MORTEM.md:38–39` exactly. *"Eight sessions have now held the stop; one examined it"* correctly increments `CONDITIONS-135.md`'s *"Seven sessions have now held the stop; one has examined it."* ✓

**Two attribution nuances, both minor.** (a) §3 says *"The arc's own post-mortem already wrote the sentence"* — `POST-MORTEM.md` §5 in fact prefaces it with *"which this practice had not written down until its adversary did"*, so the adversary wrote the sentence and the post-mortem adopted it. The citation `POST-MORTEM.md §5` is where it appears, so the pointer is right and only the authorship gloss is loose. (b) Outside the documents under test but from the same session: `REQUESTS.md:1787–1788` renders the standing rule as *"silence through your own next session means the same — decide yourselves"*, which is **not** the source's wording (*"means the same — not seven days, the next time you sit down to work"*). INCREMENT-24 quotes it correctly; the `REQUESTS.md` status block does not.

### 10. CONCEPT.md §1 and §3 numbers and quotations — NON-BLOCKING with one citation error
- **The crawl sentence.** `DERIVED.md` §1 gives, in a table with the commands: *Entries for the platform* → **339**; *Of those, video pages* → **0**; *What the 339 are* → **339 / 339 = `/robots.txt`**; and in prose *"In the July 2026 crawl the archive holds exactly one path from this domain."* CONCEPT §1's *"339 index entries — every one of them `/robots.txt`, and zero video pages"* is **faithful to its source.** ✓ The `robots.txt` clause too: DERIVED §1 records *"a list of 25 named user-agents followed by one line"*, with `CCBot` in it and `Disallow: /`. ✓ *(Scope note carried by DERIVED but not repeated in CONCEPT: the 339 come from one ranged block of one index shard, not a full-index enumeration.)*
- **The `POST-MORTEM.md` §6 quotation.** Both halves exist at source, but they are **two different bullets spliced with an ellipsis**: bullet 1 is *"The instrument keeps running. The stop is on building things to send, not on measuring. The daily probe is at 9 measurement days and continues…"*; bullet 3 is *"**The tooling is real and portable**: a credential-free probe with…"*. The elision crosses a bullet boundary and drops a full sentence, and *"The tooling"* is silently lowercased to *"the tooling"*. The ellipsis is marked, so this is signalled compression rather than misquotation — but given `ERRATA-135.md` E53 records the previous session breaking its own quoting rule at exactly the sentences where its interest lived, this splice deserves to be either widened or split into two quotations.
- **Session 109's three-arm control.** `DERIVED.md` §4 arm C: 20 synthetic identifiers → 19 × HTTP 400; §3: *"Every one of the 37 non-200 responses was HTTP 400 with the identical body… **No 404 was ever returned**"*; §4: *"an identifier that corresponds to nothing gets **the same 400 and the same body** as a video that once existed."* CONCEPT §1 item 1 is **accurate at source.** ✓
- **The Pew figures.** `FANOUT-136-1-neighbours.md:19–21` gives Chapekis/Bestvater/Remy/Rivero, Pew Research Center Data Labs, May 2024, the same URL, *"11% of references inaccessible; 53–54% of pages carry at least one broken reference"*, English-language Wikipedia. CONCEPT §1 item 3 matches its cited source exactly. ✓ **Gap I could not close:** I did not fetch the Pew report itself, so I verified CONCEPT against the fan-out, not against Pew.
- **CITATION ERROR.** CONCEPT §1 item 2 attributes *"six events is not a rate and eleven are not either"* to **`CONDITIONS-132.md` item 5**. I read item 5 at source: it says *"Day 11's zero is not a result about the platform… One interval. No trend, no test, no rate."* It contains neither "six" nor "eleven" nor any event count. The substance is published — *"six events is not a rate"* is `memory/downstream-commitments.md` **condition 8** (line 457), and the full phrasing including "eleven" is `DAY13-2026-08-25.md:43` — but the pointer in CONCEPT points at a paragraph that does not carry the claim.
- **§3's four limbs.** *"3,166 identifiers across 61 language editions… 4,499 page-level references"* ✓ (finding 1). *"Thirteen measurement days"* ✓ (finding 5). *"at one request per second"* ✓ — the run file's `probe.delay_s` is `1.0`. *"24 changes"* ✓ (finding 6). *"6 of 16"* — see finding 7 for the population caveat.
- **"about one citation in eight"** — the headline 11.93 % is an *identifier*-level share, not a citation-row share. The citation-row share is 568/4,457 = **12.74 %**. Both are "about one in eight", so the rendering survives, but the unit slides between row 3 of the table (citations) and the claim sentence (identifiers).
- **"the arc's 138 scripts" (§4b) is stale.** `POST-MORTEM.md` §5 says *"Nine days, 643 files, 138 scripts"* — a count from the arc's close. Today the arc directory holds **148 tracked `.py`** files (173 including `.sh`). §4b states it in the present tense as the population it grepped. The *claim* the grep supports does hold: my own independent grep for any request constructed on a `…/video/…` URL (`requests.get|head`, `urlopen`, `urllib.request`, `curl` on a line mentioning `video`) across `drafts/` and `tools/` returned **nothing**, while 12 scripts in the arc reference the oEmbed endpoint. So "no fetch of a video page URL" is corroborated; only the denominator is out of date.

---

## What I could not check
- Whether the run files faithfully record what the platform actually returned. Nothing offline can verify that; I verified only that every published figure is a correct reduction of the committed observations.
- The Pew Research Center figures against Pew's own publication (verified against `FANOUT-136-1-neighbours.md` only — no network fetch).
- Whether "339 index entries" would still hold against a full enumeration of the crawl index rather than the single ranged block `DERIVED.md` §1 documents.

## Verdict

**PASS WITH FINDINGS.**

Every quantitative figure I was asked to check reproduced from the raw data — most of them to the full 17 significant digits of the stored float, and the entire `series-stability-136.json` and all 122 per-edition rows with **zero** field mismatches against a from-scratch recomputation. The Wilson arithmetic, the design-effect factor, the day series, the change sequence, the page denominators, the unit fix, and every quotation in `INCREMENT-24.md` are correct. Nothing published is numerically wrong.

The findings are of scope and labelling, and three deserve action before this goes to an adversary:

1. **The confirmation figure spans arms the rest of the table excludes** (6 of 16 all-arms vs 5 of 15 on the encyclopedia arms) — most consequential, because §3 juxtaposes it with an encyclopedia-only count.
2. **"six of sixteen *confirmed* disappearances refuted"** (§1 item 2) misdescribes the record — ten were confirmed — and contradicts the table three lines above it.
3. **`CONDITIONS-132.md` item 5 does not say what §1 item 2 cites it for.**
