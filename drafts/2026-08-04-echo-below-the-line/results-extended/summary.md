# Echo index: published rule vs near-duplicate rule

Generated: 2026-08-04T23:18:12Z

## Input files

| beat file | beat | raw records | after url dedup | sha256 |
|---|---|---|---|---|
| gdelt-health.json | health | 250 | 250 | `a97b13b25ee81375...` |
| gdelt-politics.json | politics | 250 | 240 | `9a254eed4f62bc18...` |
| gdelt-technology.json | technology | 250 | 222 | `5afe92ebf39aa992...` |

Pool size after URL dedup: **712**  
Distinct domains: **442**

## Rule A (published rule, reconstructed)

Echo index A: **22.33%** (159 / 712 titles)  
Titles with fewer than 6 tokens (cannot produce a shingle): **26**  
Distinct echo phrases found: 164  
Headline (most-replicated echo phrase): "u s stock tuesday as war" (17 domains)

## Rule B sweep (near-duplicate clustering)

| t | echo index B | clusters | largest cluster size | largest cluster domains | gap vs A (pp) |
|---|---|---|---|---|---|
| 0.9 | 21.21% | 556 | 17 | 17 | -1.12 |
| 0.8 | 21.21% | 555 | 17 | 17 | -1.12 |
| 0.7 | 21.77% | 545 | 17 | 17 | -0.56 |
| 0.6 | 22.47% | 541 | 17 | 17 | +0.14 |
| 0.5 | 23.46% | 530 | 17 | 17 | +1.12 |

## A and B are not nested

Rule A can flag a title on the strength of a single shared 6-token phrase even when the rest of the title differs; Rule B requires the whole normalised title to be similar. These are different conditions, so neither rule's catch is a subset of the other's. Both directions, at every swept threshold:

| t | caught by A, not B | caught by B, not A | caught by both | echo index A | echo index B | which is larger |
|---|---|---|---|---|---|---|
| 0.9 | 8 | 0 | 151 | 22.33% | 21.21% | A > B |
| 0.8 | 8 | 0 | 151 | 22.33% | 21.21% | A > B |
| 0.7 | 5 | 1 | 154 | 22.33% | 21.77% | A > B |
| 0.6 | 1 | 2 | 158 | 22.33% | 22.47% | B > A |
| 0.5 | 0 | 8 | 159 | 22.33% | 23.46% | B > A |

No direction is softened here: where B(t) falls below A in this table, that is reported as measured, not adjusted.

## Rule C: is 'distinct domain' a sound unit?

URL paths seen in the pool that are served by >=2 distinct domains: **40**  
URL paths served by >=3 distinct domains: **24**  
Path served by the most distinct domains: `/news/279222614/record-breaking-day-for-u-s-stock-tuesday-as-war-jitters-subside` -- 17 domains  
Domain-group size distribution over paths with >=2 domains (size -> number of such paths): {2: 16, 3: 11, 4: 4, 5: 2, 6: 1, 8: 2, 10: 2, 13: 1, 17: 1}

Collapsing domains that share >=1 identical URL path (transitively) into publisher groups: **442 domains** collapse into **331 publisher groups**.  
Publisher-group size counts (group size -> number of groups): {1: 309, 2: 4, 3: 5, 4: 5, 6: 2, 8: 1, 11: 1, 12: 1, 13: 1, 14: 1, 20: 1}

Echo index A recomputed with '>=3 distinct domains' replaced by '>=3 distinct publisher groups': **5.06%** (original domain-based Echo index A: 22.33%, drop of **17.28 percentage points**).

*A shared URL path shows the same item was republished through a shared publishing system across those domains. It does not show, and this output does not claim, common ownership of those domains.*

## Judgement calls

- Normalisation is lossy: lowercase + collapse any non-alphanumeric run to a single space. Numbers, hyphens, punctuation, and diacritics are all flattened; 'Bio-tech' and 'Biotech 2026' can end up sharing tokens they would not share in a stricter scheme.
- The 6-token shingle length for Rule A is taken verbatim from the published method sheet; it was not tuned or chosen by us.
- Rule B's default similarity keeps stopwords in the token set, so two titles that mostly share function words ('a', 'the', 'of') can look more similar than they are topically. A stopword-removed variant is computed alongside for comparison, using a short hand-written list (STOPWORDS in the code), not a standard corpus list.
- Jaccard-over-token-sets ignores word order and duplicate tokens entirely; 'X beats Y' and 'Y beats X' can score identically to 'X beats X'.
- Single-linkage clustering chains by construction: A-B and B-C above threshold puts A and C in one cluster even if A-C similarity is 0. This is disclosed, not hidden, but it means Echo index B is an upper-bound-leaning estimate of near-duplicate coordination, not a tight one. The per-threshold largest-cluster diagnostics exist specifically so a reader can see how much chaining occurred.
- The >=3-distinct-domain rule is applied identically to Rule A echo phrases and Rule B clusters, as the method sheet's own bar for counting as 'echo' rather than coincidence. Any threshold is somewhat arbitrary; 3 is the published instrument's choice, not ours.
- Titles with fewer than SHINGLE_N=6 tokens cannot produce a Rule-A shingle at all and are excluded from Rule A's echo count by construction (not by evidence of non-echo); they are still eligible for Rule B clustering. This asymmetry is reported explicitly.
- Deduplication is by exact URL string match only. It does not catch tracking-parameter variants, http/https variants, or mirrored copies at different URLs; GDELT's own upstream deduplication behaviour (if any) is unknown to us and not corrected for.
- Threshold sweep (0.9 down to 0.5) is a fixed, pre-declared grid, not a search for the most dramatic gap; all five values are reported together, not cherry-picked.
- Domain is taken as GDELT's reported 'domain' field verbatim; no attempt is made to detect co-owned outlets or wire-service syndicates publishing under multiple domains, which would tend to inflate the apparent domain count of a real echo.
- Example pairs (Rule B catches, Rule A does not) are chosen deterministically by sorting on (similarity descending, then url pair ascending) and are illustrative, not a random or representative sample of the gap.
- Rule A and Rule B are NOT nested: Rule A can flag a title on the strength of a single shared 6-token phrase even if the rest of the title differs a lot (low whole-title Jaccard), while Rule B requires the whole normalised title to be similar. So a title can be caught by A and missed by B, and vice versa; both directions are reported at every threshold, and on at least one input B(0.9) was measured BELOW A -- the near-duplicate rule did not simply add cases on top of the exact-phrase rule.
- Rule C's URL-path grouping uses the exact path string with no normalisation (no trailing-slash collapsing, no case-folding, no stripping of tracking segments embedded in the path itself); two paths that are the same item but differ by one character will not be grouped, so the collapse is a lower bound on true shared-item republication, not an exact count.
- Rule C's publisher grouping is transitive and can chain exactly like Rule B's single-linkage clustering: two domains that never share a path directly can end up in the same publisher group via a third domain that shares a different path with each. This is disclosed, not hidden.
- A shared URL path is evidence of shared publishing infrastructure (the same item, byte-for-byte path, served from multiple domains); it is not evidence of common ownership and must not be read as one. No ownership claim is made anywhere in this output.
