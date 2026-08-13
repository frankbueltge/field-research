# Interlocutor 6 — against Increment 4, on state `75987b8`

*Session 114, 2026-08-12/13. Convened on the exact committed state named above, for both
obligations in one pass. Published unedited, including the parts that are unflattering to this
practice and the parts that praise it. The verdict is good only for the state it was run on; the
document it attacks was edited afterwards to discharge these conditions, and those edits are
recorded in `CONDITIONS-DISCHARGED-114.md`.*

---

## (a) REFUTATION

**STANDS WITH CONDITIONS.**

The core statistical claim survives every attack I could mount, including several harsher than the ones the increment set for itself. The conditions below are eight specific defects, one of which (C1) is a factual error the document's own table refutes, and one of which (C5) is a live alternative explanation that the increment never tested and that changes what §7 licenses.

Everything below was rederived by me from `ledger/run-2026-08-12T0341Z.json` and `ledger/run-2026-08-11T1124Z.json` with my own code, importing nothing from the session's modules except where I say so explicitly.

---

### What I could not break

**Population arithmetic — exact.** 3,869 − 249 (`B-truncated`) − 38 (INDETERMINATE) − 7 (non-19-digit) = 3,575 units, 2,744 handles, 432 absent, 12.0839 %, 2,366 singletons, largest handle 36. Every figure in §2 reproduces to the digit shown.

**Concordance and all-gone — exact, and understated.** 2,869 within-handle pairs, 67 both-absent, 41.89 expected at the pooled rate; 64/98 = 65.31 % in all-gone handles; 26 such handles at sizes {2:18, 3:6, 4:1, 6:1} → 36+18+4+6 = 64 ✓. The §2 expectation of 41.9 is generous to the null: the pairs live inside the multi-handle subpopulation whose own rate is 8.106 %, and 2,869 × 0.08106² = **18.85**, so the real excess is 3.6× and not 1.6×. The increment picked the weaker of the two available statements.

**The cluster bootstrap is implemented correctly, and resampling K handles against N units is the right comparison.** It is the standard nonparametric cluster bootstrap of a ratio estimator. I verified it against the closed-form linearised clustered variance, which the session never computed:

```python
V = K/(K-1) * sum((a_h - p*n_h)**2) / N**2      # a_h, n_h per handle
DEFF = V / (p*(1-p)/N)
# -> 1.4289
```
My own bootstrap (200,000 draws, `numpy`) gives a variance ratio of **1.4303** and a squared-width ratio of **1.4419**. So "the ratio of the squared widths *is* the design effect" (`cluster_bootstrap.py` docstring) is loose — the two differ by ~1 % because the cluster distribution is mildly skewed — but not wrong at two digits.

**The exclusions do not manufacture or destroy anything.** I re-ran with every combination put back:

| population | N | rate | DEFF |
|---|---|---|---|
| as published | 3,575 | 12.08 % | 1.429 |
| + `B-truncated` + non-19-digit | 3,829 | 17.84 % | 1.458 |
| + non-19-digit only | 3,582 | 12.20 % | 1.427 |
| INDETERMINATE counted absent | 3,613 | 13.01 % | 1.406 |
| INDETERMINATE counted present | 3,613 | 11.96 % | 1.427 |
| everything in, INDETERMINATE absent | 3,869 | 18.69 % | 1.444 |

The design effect is 1.41–1.46 under every policy. The point estimate moves a great deal (as it must — `B-truncated` is 246/249 absent), but the increment never claims otherwise and never uses that population for a rate.

**The failed key does not manufacture it either — and §0's directional claim is verifiable, which the increment did not bother to do.** §0 asserts a renamed account "splits into two groups … so the key *dilutes* clustering. It cannot manufacture it." The merge direction is the one that could manufacture it, and I tested it: **zero** cited handles in the population cover more than one platform `author_unique_id`. Further: canonicalising (key 2) *raises* DEFF from 1.429 to 1.437; dropping all 177 handles touched by a disagreement raises it to 1.456. The key failure costs the result nothing in the direction that matters.

**The age confound is dead, and by a harsher test than the pre-registered one.** Null 2 conditions on 1-year age bands — coarse enough that an account's videos, usually posted within weeks, share a band by construction, so "the shared era of an account's videos is already priced in" (§2) was an overstatement of what a 1-year control buys. I therefore re-ran it at 90-day and 30-day resolution, and as an exact within-cell permutation:

| null (2,000 draws each, on DEFF) | mean | p95 | **max** | observed |
|---|---|---|---|---|
| 1-year band × arm (as pre-registered) | 1.040 | 1.101 | 1.174 | **1.429** |
| 90-day bin × arm (119 cells) | 1.058 | 1.114 | 1.180 | **1.429** |
| 30-day bin × arm (321 cells) | 1.084 | 1.142 | **1.215** | **1.429** |
| permutation within 1-year band × arm | 1.037 | 1.093 | 1.153 | **1.429** |

Not one draw in 8,000 comes near. The overstatement in §2 is harmless because the stronger claim is also true.

**The significance claims are honest.** Both Monte Carlo p-values report `n_ge_observed: 0` in `cluster-2026-08-12T0341Z.json`, and the increment says in terms that 0.0001 is the floor and means "not once in 10,000 draws". Null 2's rates being estimated from the same data does not rig it: the cells are coarse (≤24 cells over 3,575 units), the estimation absorbs structure *into* the null (null-2 mean ρ = 0.0553 against null-1's −0.0000, exactly as it should), and the direction of any residual bias is against the finding, not for it. The ANOVA ICC is calibrated honestly by the Monte Carlo — under both nulls the singleton pathology is present in the simulated data too, which is why null-1 mean ρ ≈ 0 despite 2/3 singletons. The ICC's *magnitude* is uninterpretable (I get 0.0824 from the pooled pairwise estimator and 0.2253 from the multi-handle pairwise estimator against the ANOVA's 0.7912), and D17 says so and refuses to use it. That is the right call.

**The probe's `statusCode` reading is sound.** Across all 36 handles, `statusCode == 0` ⟺ `userInfo`, `uniqueId`, `secUid`, `followerCount` all present; no exceptions. I fetched two account pages myself and confirmed the recorded `uniqueId` sits inside the `userInfo` object (offset 349,884 vs 349,944), not in a URL echo. Byte separation is clean: served pages 364,064–365,676; unserved 362,007–362,978.

**"Largest first" does not drive the 6/12 — it runs the other way.** The all-gone group is the 26 all-gone multi-handles sorted by size: the sample takes all handles with k ≥ 3 plus four of the eighteen k = 2. That enriches for large all-gone clusters, which is precisely where account-death should be most likely. It still failed: the two largest (k = 6, k = 4) are both unserved, but 4 of the 6 k = 3 handles are *served*. The four k = 2 handles split 2/2, the same as the whole. A random sample would not plausibly reverse the direction.

**Every quotation checks character-for-character.** I fetched `https://arxiv.org/html/1709.09186` (HTTP 200, 236,800 bytes), stripped tags, and string-matched:

- *"The exception is the percentage of unique users found in the recollected datasets, which is 80.0%. This indicates that many of the tweets likely disappeared because of the removal of the user accounts"* — **exact match**, and the increment correctly truncates before the trailing clause.
- The pre-registration's *"119,752,714 tweets (81.4% of the whole) were still available"* — **exact match**.
- "147 M items" ✓ (the paper's Table 1 total is 147,055,035). "JASIST" ✓ (the abstract page carries "Accepted for publication in JASIST"). "Arkaitz Zubiaga" ✓.
- **"It does not measure clustering" — confirmed.** Occurrences in the full text: `cluster` 0, `intraclass` 0, `intra-class` 0, `design effect` 0, `confidence interval` 0, `standard error` 0, `bootstrap` 0, `correlat` 0. The single hit for `variance` is inside a reference title (Welch 1947). The increment *undersells* its own daylight: the paper does run inferential statistics — Welch's t-test across 22 features — and those tests treat items as independent. That is a much sharper instance of "computes as if items were independent" than the descriptive percentages, and it is not used.
- `https://dl.acm.org/doi/10.1145/3517745.3561451` → **HTTP 403** ✓ (verified by `curl -L`).
- `https://github.com/davidteather/TikTok-Api/issues/403` exists and is open, titled *"List of TikTok responses' status codes anywhere?"*, asking exactly what §4 says it asks. I could not independently verify "stands unanswered" — no comment count was exposed to my fetch. Mark that half of the sentence as unverified rather than verified.

**§0's "citation drift that leaves no broken link behind" is real, and I proved it rather than accepting it.** Three oEmbed requests against one cited video id, varying only the handle in the path:

```
tatemcrae1                 -> (200, 'tatemcrae', 'tate mcrae')
tatemcrae                  -> (200, 'tatemcrae', 'tate mcrae')
zzz_not_a_real_handle_9187 -> (200, 'tatemcrae', 'tate mcrae')
```
The handle in the path is decorative to the point of being ignorable. §0's point 1 stands.

---

### Conditions

**C1 — `INCREMENT-4.md` §5: "Five of ten fail." The table above it shows four.** P1, P6, P8, P10 are FAIL; P2, P3, P4, P5, P7, P9 are hold. `sed -n '183,195p' INCREMENT-4.md | grep -c FAIL` → **4**. The document overstates its own failure rate by 25 %, in the direction that flatters the house's stated virtue. This is the same error class as the bound refuted by its own table, and it took the same ten seconds. Fix the sentence, do not fix the table.

**C2 — §4: "This corpus contains 226 renamed handles whose videos still return HTTP 200 with a *different* author name."** It contains 226 disagreeing **observations** across **177 distinct handles**. §0 gets this right ("the 226 disagreements"); §4 converts observations into handles. Worse, "renamed" is an interpretation the data do not carry. `@tatemcrae1` is one of the four exemplars in §0's own table, and tonight's own probe returned `statusCode 0, uniqueId "tatemcrae1"` for it; I re-fetched and confirmed a full live user object (`secUid`, `followerCount`, `nickname`) under that name while all nine of its cited videos report owner `tatemcrae`. Both names are live accounts. That is not a rename — given C-above, it is at least as likely a mis-cited or reposted handle. The rename-rebuttal's *logic* survives (a name change demonstrably does not remove a video from the endpoint, so it cannot explain the six unserved handles), but its premise must be restated as "226 units whose cited handle is not the current owner's name", not "226 renamed handles".

**C3 — §0: "7.24 % of the account handles cited in this corpus no longer name the account that holds the video."** 7.24 % is 226/3,121 **observations**. The handle-level figure is 177/2,374 = **7.46 %**, and only 2,374 of the 2,744 handles are checkable at all — 370 have no retrievable unit and cannot be tested in either direction. The sentence generalises a per-observation rate measured on a checkable subset to "the account handles cited in this corpus", with no interval (Wilson on 226/3,121 is [6.38 %, 8.20 %]). In an increment whose subject is intervals being too narrow, a headline percentage published bare is not a small thing.

**C4 — §3: "Measured design effect: 1.458" is over-precise by two digits, and 1.20× is right by luck.** Their estimator is a percentile-width ratio from 10,000 draws. I replicated *that exact estimator* 60 times with independent seeds:

```
mean 1.4311   sd 0.0417   range [1.3402, 1.5325]
published 1.4575 sits at the 73rd percentile of its own seed distribution
analytic clustered/binomial DEFF = 1.4289
```
The stable value is **1.429**, not 1.458. Downstream: √1.4289 = **1.1954** (still "1.20×", so the headline survives); effective n = 2,502 not 2,452; and "the ANOVA route overstates it by 56 %" should be **59 %** (2.2699/1.4289 = 1.589). Either raise the draws by 10× or publish the analytic figure with the bootstrap as its check. Four significant figures off a 10,000-draw percentile width is not a measurement, it is a seed.

**C5 — the account is not established as the unit of clustering, and the strongest competitor was never tested.** I joined each unit back to its **citing page or thread** (`corpus-merged.json` `wiki|page`, `corpus-hn.json` `hn_object_id`, the expansion corpora); 3,507 of 3,575 units carry one. On the identical subset:

| grouping key | K | DEFF | age-arm null max (1,000 draws) |
|---|---|---|---|
| cited handle | 2,687 | **1.436** | 1.175 |
| **citing page / thread** | 2,585 | **1.895** | 1.484 |

On arm A alone: handle 1.492, page **2.328**. Pair decomposition:

```
same HANDLE, DIFFERENT page   pairs=  660  both= 24  exp=  9.6  ratio=2.49
same PAGE,   DIFFERENT handle pairs= 2302  both=187  exp= 33.6  ratio=5.56
```
One article does most of it — `es.wikipedia.org|Protestas en Paraguay de 2023`, **23 cited videos across 20 distinct accounts, 17 of them absent**. Drop that single page and the page-key DEFF collapses to 1.395 while the handle-key DEFF barely moves (1.436 → 1.428), and the pair ratios invert to 2.66 (handle) against 1.93 (page). So: the *account* key is the robust one and the *page* key is the fragile one — I will say that plainly, it is a point in the increment's favour. But three things follow that the increment does not say. (i) On the data as they stand, the largest measured design effect in this corpus is **1.895**, not 1.458, so §7's "the intervals widen by 1.20×" is a **lower bound**, not the correction. (ii) A single Wikipedia article co-losing 17 videos from 20 different accounts is a mechanism — event-level or topic-level removal — that the account frame cannot express and that §4's probe cannot detect. (iii) §7's "cheap new arm … ~2,744 accounts" is licensed on an attribution the data do not uniquely support; the cheaper and more discriminating arm is the one that costs zero requests, namely the page key, which was sitting in the repository all along. Test the page key before spending 2,744 requests on the account key.

**C6 — §4: "It is the account half the time" is 6 of 12 with no interval.** Wilson 95 % on 6/12 is **[25.4 %, 74.6 %]**. The sentence is compatible with "a quarter of the time" and with "three quarters of the time". It also covers only the all-gone multi-handle subpopulation: 64 of 432 absences, **14.8 %** of the losses. Nothing in §4 measures the mechanism behind the 334 singleton absences, which are 77 % of the total and which have the *higher* absence rate (14.12 % against 8.11 %). §4's negative result is the most interesting thing in the increment; it deserves its own uncertainty stated, and its scope stated in the same sentence.

**C7 — K1 in §0 versus the restatement in §7.** `PREREGISTRATION-114.md` §4 K1: on P1 failure, "tonight's result is **not** published as a finding about the platform; it is published as a finding about the key." §0 declares compliance and withholds the sentence "the unit of loss is the account" — genuinely, and to the session's credit. But §7 then orders a dated correction to `RESULT.md`, `OBJECT-ANSWER.md` and the power audit, widening published intervals about **the platform's** retrievability rate by 1.20×, on the strength of a statistic computed with the key that failed. That is not a finding about the key. Asked bluntly whether the increment is wording its way around K1: **partly, yes** — §0's compliance declaration is written as though it covers the whole document, and it does not cover §7. What saves it from being a break rather than a condition is that the underlying inference is sound and I verified it independently (see the key-sensitivity results above): the key failure demonstrably cannot manufacture the design effect, so the correction is conservative regardless. Say that in §7, in one sentence, instead of letting §0 carry it.

**C8 — the `B-truncated` exclusion is entirely subsumed by the 19-digit filter, and §2's arithmetic hides it.** All 249 `B-truncated` identifiers are non-19-digit (lengths 5–18); there are 256 non-19-digit ids in the run and 249 of them are that arm. Filtering on 19 digits alone yields the identical 3,575-unit population. So the pre-registration's emphasis — "*This exclusion is registered before the statistic is computed*" — buys nothing that a mechanical decodability rule did not already buy, and §2's "minus the 249 … minus 7 identifiers that are not 19 digits" reads as two independent filters when it is one filter counted twice. Not an error; a piece of rhetorical weight resting on nothing.

**Operational hazard, not a condition.** `cluster-2026-08-12T0341Z.json` still carries `interval_corrected_for_clustering: [10.57 %, 13.79 %]`, computed from the discarded DEFF 2.270 with `n_eff = 1574`. The prose repudiates it; the JSON does not. A later session reading the output file rather than the increment will publish the wrong interval. Rename the field or write the bootstrap interval into it.

---

## (b) THE HOSTILE CRITIC

**Is this slop? No. Is it as important as it thinks it is? Also no.**

Let me start with what an outside critic would concede, because a critique that attacks everything is worth nothing. This session did something genuinely rare: it pre-registered a statistic, ran it, got a number it did not like, said so in public, threw the statistic away in a numbered deviation, replaced it with a better one, and reported the discarded number beside the kept one. Then it wrote three predictions into a file, committed them, ran the probe, and published two failures. Then it wrote down a dated falsifiable prediction about a single account — `grimhoundgaming` on 2026-08-13 — that will settle itself in twenty-four hours whether anyone likes the answer or not. I have attacked ten sessions' worth of published work in my time and this is the top decile of that behaviour. The P8 failure in particular is the good kind of result: the session set out to write "the unit of loss is the account", measured it, found it true half the time, and published the smaller sentence. That is what measuring the world looks like.

Now the hard part.

**Most of tonight was arithmetic on yesterday's data.** §2 and §3 — the parts that carry the headline — sent zero requests. They took a run already in hand and computed a variance a different way. That is a legitimate and necessary thing to do, but it is bookkeeping, not fieldwork, and the increment's own framing ("the arc owes a restatement") is the tell: the deliverable is a correction to the arc's previous arithmetic. Sixty-two requests went out, thirty-six of which produced the paper's only genuinely new observation about the world. Thirty-six. An outside critic looking at the ratio of prose to new observation — fifteen thousand characters of increment against thirty-six data points and one recomputed variance — would call this a house that has begun to talk about itself.

**The headline correction is small and the document knows it.** 1.20×. A lower bound of 11.06 % becomes 10.85 %. The increment says "Small, real, and in the direction that costs us", which is exactly the right register, and then spends seven sections on it. Nobody outside this house will change a conclusion because a link-rot interval on 3,575 videos widened by two tenths of a percentage point. The *methodological* point — that everyone in this literature, the nearest neighbour included, computes item-independent intervals on item-clustered corpora — is the durable contribution, and it is buried under §3's table of four nearly identical confidence intervals.

**The framing is probably wrong, and it is wrong in the direction of the arc's own prior commitment.** This arc is called "the arm that was missing" and it has spent sessions building toward the account as an object. So when the losses turned out to be clustered, the session reached for the account. It never asked whether the citing page clusters harder — and on the data as they sit, it does (1.895 against 1.436). One Spanish Wikipedia article about the 2023 Paraguayan protests carries 23 cited videos from 20 different accounts and 17 of them are gone. That is an event, or a moderation sweep, or a class of content — and it is invisible to every instrument this session built. The honest reading is that the page key is fragile (drop that one article and it collapses) and the account key is robust, which vindicates the choice on the evidence but not on the reasoning: the session picked the account because the account is what it was already looking for, and got lucky. §7 then proposes spending 2,744 requests on the account arm. A critic outside this house would say: you had a stronger competing key sitting in your own repository at zero request cost, and you did not test it, and you are now proposing to buy the answer you already assumed.

**The precision theatre.** "1.458", "56 %", "2,452 of 3,575", "ρ = 0.7912", four significant figures throughout. The 1.458 has a seed-to-seed standard deviation of 0.042. A session whose entire thesis is *you have been publishing intervals that are too narrow* published its own central estimate as a point with no interval, from an estimator it could have solved in closed form in four lines. That is not a small irony; it is the same error one level up. Likewise "half the time" from 6 of 12, in the same document.

**"Five of ten fail."** Four of ten fail. In a document whose rhetorical currency is *look how many of our own predictions we broke*, the one number that got inflated is the failure count. I do not think it was deliberate. I think it is what happens when a house has found that publishing failures is rewarded: the count drifts upward without anyone checking. That is worth more attention than the arithmetic slip, because it is a pressure the house cannot see from inside.

**The neighbour reading is real and correctly done, and undersold.** The Zubiaga check is exemplary — quotation exact, absence of clustering analysis verified by search and not by assumption, the closed ACM route recorded as closed rather than as absent. But the daylight is stated weakly. The paper does not merely report percentages as if items were independent; it runs Welch's t-tests across 22 features on 147 million items and reads significance off them. *That* is the sentence: the nearest neighbour in this method family performs formal hypothesis tests on a corpus it has itself just told you is user-clustered. Say that and the contribution is obvious to any statistician. Say "its reported figures treat items as independent" and it sounds like a quibble.

**Verdict on the "so what".** This is not slop and it is not a session that only re-measured its own arithmetic — §4 measured something new about the world, and what it measured contradicted the session's own hypothesis, which is the most valuable thing here. But the increment inverts its own emphasis: it leads with a 1.20× correction that nobody outside will care about and buries a 6/12 mechanism failure that is genuinely interesting, then licenses a 2,744-request arm on the reading the data least support. The strongest thing in this document is the sentence the session did not want to write. Lead with it next time, put an interval on it, and test the page key before you spend the requests.
