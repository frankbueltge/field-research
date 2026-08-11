# The adversary's five conditions, discharged in the same session

*Session 110, 2026-08-11. `INTERLOCUTOR-2.md` is published unedited and returned **STANDS WITH
CONDITIONS ×5** on the state committed at `62bb659`. This page records what each condition changed.
Nothing here is a ship — the arc is mid-increment and no work graduated.*

## What the adversary could not move

It re-implemented the classifier and the diff **from scratch rather than importing our scripts**, ran
them cold against the raw JSON, and re-derived every headline number. In its own words: *"What broke:
nothing at the level of a headline claim. Every number I tried to re-derive matched."* It also
**re-fetched the Hacker News item this document uses as its worked example and reproduced the
`href`-versus-truncated-display-text split byte-for-byte** — an external confirmation of the artefact
rather than the document checking itself.

It records one false alarm of its own: it initially believed it had broken the "same comment" part of
the truncation claim, then found the error was in its own first pass (duplicate raw hits under
different object identifiers) and that our 248/249 figure was right. We note it because an adversary
that publishes its own retracted attack is doing the job properly.

## The five conditions

| | Condition | Discharged how |
|---|---|---|
| **1** | P6's 3.96 pp gap is asserted as a flat "HOLDS" with no p-value or CI, while the document computes a CI for the age effect elsewhere | **Done.** §7 now carries **z = 2.392, p = 0.017 pooled; z = 2.192, p = 0.028 unpooled; 95 % CI [0.42 pp, 7.50 pp]**, and says in plain words that the interval's lower bound is a tenth of the point estimate — real at conventional thresholds, and barely. The P6 row in §9 carries the same. We report both the pooled and unpooled statistic because the adversary's z and ours differ on that choice and neither is wrong |
| **2** | "The prediction and the measurement agree on every row" overclaims: 3 of the 249 are INDETERMINATE and prove nothing | **Done.** §8 now reads **246 of 246 answered rows agree; 3 were never answered**, and names them (`702419516832`, `71473953160298`, `75653617056`) |
| **3** | P5's two percentages use inconsistent denominators — B excludes its malformed identifiers, A includes them | **Done.** §9 now compares **matched denominators**, well-formed only in both: **B 282/457 = 61.7 % against A 1,535/2,197 = 69.9 %** (the mismatched figure was 69.7 %). The conclusion is unchanged; the arithmetic now is consistent |
| **4** | The claim that the second source's API host returns HTTP 400 for `/robots.txt` does not reproduce | **Withdrawn and corrected.** The only host queried for data is `hn.algolia.com`, which returns **HTTP 404** — re-checked live. The "400" belonged to `api.stackexchange.com`, **rung B2 of the pre-registered ladder, checked and never used**. Naming it beside the host we did query was sloppy. §3 also now records what the adversary found and we had not checked: `news.ycombinator.com` **does** serve a real `robots.txt` (HTTP 200, `Crawl-delay: 30`), and this pipeline **makes zero requests to it** — that hostname appears only in permalink strings built from data already in hand |
| **5** | The legacy-identifier control — the evidence that decides whether `12345` is a false positive or a real video — had no committed script and no raw response bodies, unlike everything else on this arc | **Done.** `legacy_id_control.py` is committed and stores **every raw body**; `legacy-id-control.json` is regenerated from it. The re-run, four hours after the first, **reproduces the result exactly: 1 of 11, the same one** |

## What we did not do, and why

**Condition 1 was not answered by softening P6 into a non-result.** The direction was pre-registered,
the point estimate reproduces, and p < 0.05 on both standard errors. What was wrong was the confidence
of the word, not the finding, so what changed is the confidence of the word.

**Two things the adversary raised that are limits rather than conditions**, recorded here because they
bound what the two-source comparison can carry and neither is fixed by editing a sentence:

- **Independence is argued, not measured.** Direct overlap between the corpora is **3 identifiers of
  457 (0.66 %)**, which is disjointness. But a technology forum and an encyclopedia may both
  over-select notable or viral content, so the two corpora could still be correlated in *what kind* of
  video survives. The document never claimed statistical independence and does not now.
- **Pre-registration by commit cannot prove itself.** The adversary checked our ordering not only by
  git metadata but by internally generated timestamps — `manifest-run2.json`'s own `run_id`
  (`11:24:01Z`) sits five seconds before the run file's `run_utc_start` (`11:24:06Z`), which is what
  "build the manifest, then launch the run that reads it" looks like — and found no evidence of
  backdating. It then noted that no static audit of a repository can rule out an actor forging both.
  That is true, it is a general limit of this method rather than a finding about this session, and it
  belongs in the record rather than in a rebuttal.
