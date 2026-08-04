# Echo index: published rule vs near-duplicate rule

Generated: 2026-08-04T23:02:18Z

## Input files

| beat file | beat | raw records | after url dedup | sha256 |
|---|---|---|---|---|
| gdelt-politics.json | politics | 250 | 250 | `9a254eed4f62bc18...` |

Pool size after URL dedup: **250**  
Distinct domains: **203**

## Rule A (published rule, reconstructed)

Echo index A: **23.60%** (59 / 250 titles)  
Titles with fewer than 6 tokens (cannot produce a shingle): **17**  
Distinct echo phrases found: 55  
Headline (most-replicated echo phrase): "what ex son in law is" (13 domains)

## Rule B sweep (near-duplicate clustering)

| t | echo index B | clusters | largest cluster size | largest cluster domains | gap vs A (pp) | caught by B not A |
|---|---|---|---|---|---|---|
| 0.9 | 22.00% | 191 | 13 | 13 | -1.60 | 0 |
| 0.8 | 22.00% | 190 | 13 | 13 | -1.60 | 0 |
| 0.7 | 22.80% | 188 | 13 | 13 | -0.80 | 1 |
| 0.6 | 24.40% | 186 | 13 | 13 | +0.80 | 2 |
| 0.5 | 24.80% | 183 | 13 | 13 | +1.20 | 3 |

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
