# Pre-registration — a number you cannot check

**Session 168, 2026-09-23.** Committed **before any corpus was fetched** and **before the rule
was written**. What was done first, and is not a result: three candidate corpus routes were
probed for reachability only (§5), and the prior-art search of §3 was run. No abstract, no
summary and no percentage had been read through any instrument when this file was committed.

---

## 1. The question

An automated research pipeline that verifies claims can only verify a claim whose evidence is in
the text it holds. A sentence that says *"the method succeeded in 62 % of cases"* cannot be
checked by any machine, or by any reader, without going somewhere else. A sentence that says
*"succeeded in 31 of 50 cases (62 %)"* can be checked by arithmetic alone, in the reader's head,
with nothing fetched.

> **Of the percentages printed in scientific abstracts, what share hand over the integers that
> would let any reader recompute them — and of those that do, what share are wrong?**

Two measurements, one instrument:

1. **The hand-over rate.** Of all percentage tokens in a document, the share that are
   *recomputable*: an integer pair `(k, n)` stands in the same sentence in an explicit linking
   construction, so that `100·k/n` can be formed without leaving the sentence.
2. **The consistency rate.** Of the recomputable percentages, the share whose printed value
   agrees with `100·k/n` under a stated tolerance.

This is the same failure this practice has now met four times from four directions and named
*the handover*: cycle 001 found **81.7 %** of 613 automation-advertising abstracts hand over no
address; 09-18 found consent to be binary — the failure is not a sloppy grant but an absent one.
Here the object is the number itself.

## 2. Why this session, and what it is not

The licensing arc closed on 09-22 after seven consecutive sessions on one instrument, with the
record's own note that the next session starts elsewhere. This one does: new corpora, new rule,
new subject, no licence file touched. It runs under the **counter-measurement remit**, which
returned with cycle 003 by the terms of the decision of 2026-09-03, and under the default theme
of protocol §5 — *what quality do automated steps deliver* — because claim verification is one of
the steps the end-to-end systems say they automate, and its ceiling is set by the text, not by the
verifier.

It is **not** cycle 003's outside session (§5.2.3); 09-19 was. It is the first session since
09-15 whose corpus is not a repository.

## 3. Prior art, searched outward before the rule was written

Established, and no novelty of method is claimed:

- **statcheck** (Nuijten et al.) recomputes a p-value from its test statistic and degrees of
  freedom and reports inconsistency prevalence in psychology.
- **The GRIM test** (Brown & Heathers) tests whether a reported mean is attainable at the
  reported sample size, and reports that only a minority of sampled articles were *amenable to
  testing* at all — the closest published relative of this session's first measurement, in a
  different field and at the article level rather than the claim level.
- **Abstract-versus-full-text inconsistency** is a measured literature in biomedicine.
- **Numerical claim verification** (fact-checking a number against external evidence) is an
  active NLP literature; it is the opposite direction of travel from this session, which asks
  only whether the number can be checked **without** external evidence.

Every source above that any finding rests on is read first-hand and quoted from the passage in
`data/sources.json` before this artifact ships. Nothing is cited from memory. **What would make
this session's claim of subject-novelty false:** a published claim-level hand-over rate for
percentages in abstracts of any field. If one is found, it is cited and this session's numbers
are reported against it, not as a first.

## 4. The rule, fixed here before it is written

**R-1 Sentence split.** Normalise whitespace; strip Markdown emphasis, link syntax and heading
markers; split on `.`/`;`/`!`/`?` followed by whitespace, and on newlines; treat a Markdown table
row as one sentence per cell.

**R-2 Percentage tokens.** A percentage token is a number (integer or decimal, optional thousands
separators) followed by optional whitespace and `%` or `percent`. Its **decimals** `d` is the
count of digits printed after the decimal point. **No percentage token is excluded for any
reason** — not differences, not thresholds, not hyperparameters. Exclusion by meaning is a
judgement, and a judgement inside the denominator is the defect this practice keeps finding in
other people's instruments. The consequence — that irrecomputable-by-nature tokens inflate the
un-checkable share — is handled by the hand-read decomposition of §6, not by the rule.

**R-3 Linking constructions.** Within one sentence, an integer pair `(k, n)` is *linked* when it
appears as `k of n`, `k out of n`, `k of the n`, `k among n`, `k in n`, or `k/n`, with
`0 ≤ k ≤ n` and `n ≥ 2`. Thousands separators are read; a pair either side of which stands a
`%` sign is still a pair.

**R-4 Recomputable.** A percentage token is *recomputable* when at least one linked pair stands
in its sentence. It is paired with the linked pair at the smallest character distance; ties go to
the pair on the left.

**R-5 Consistent.** A recomputable token with printed value `p` at `d` decimals and pair `(k, n)`
is **consistent** when `p` equals `100·k/n` rounded to `d` decimals, **or** equals it truncated to
`d` decimals. It is **complement-consistent** when it satisfies the same test against
`100·(n−k)/n`. Otherwise it is **inconsistent**. Complement-consistent tokens are counted and
reported separately and are **not** counted as inconsistent.

**R-6 Before any corpus.** The rule is fixture-tested on hand-written cases written before the
rule's code, then mutation-tested: each mutation of the rule must be caught by at least one
fixture, and every mutation that survives is reported as a hole in the fixtures, not hidden.

## 5. The corpora, and how they are pinned

Three, each pinned by an identifier list and a SHA-256 over its normalised texts, both committed:

- **Corpus M — medicine, where a reporting standard applies.** PubMed, article type
  *randomized controlled trial*, publication date 2026-08-01 to 2026-08-31, abstract present;
  the first 1,000 PMIDs in the API's own order.
- **Corpus A — the AI literature, where none does.** Semantic Scholar bulk search,
  `query="large language model"`, `year=2026`; the first 1,000 records carrying a non-empty
  abstract, in the API's own order.
- **Corpus F — this practice's own public record.** Every `SUMMARY.md` under `artifacts/` and
  `presentations/` (the five-minute summary protocol §2 requires), and every version of
  `BULLETIN.md` in this repository's history. Genre-matched to an abstract: a short public
  account of one piece of research, written to be read on its own.

**Reachability, probed before this file was written and reported as a result of its own.** The
arXiv API refused this session from every route tried — `429 Rate exceeded` direct over HTTPS,
`406` through a dispatched client, `301` on the OAI-PMH endpoint — and OpenAlex answered `429`
with the message that the free daily budget shared by this network's address was spent. Neither
is a statement about arXiv's or OpenAlex's policy; both are statements about this session's
network, and they go to open question 46. **Corpus A is a Semantic Scholar corpus because arXiv
was shut, and the record says so rather than presenting a second choice as a first.**

## 6. What is read by hand, and why both directions

The rule's errors run both ways, and a session that reads only its own flags measures only one.

- **Every** inconsistent and complement-consistent token is read by hand, in its sentence, and
  adjudicated: *real arithmetic error* / *rule error* / *undecidable from the sentence*.
- **A random sample of 60 recomputable tokens** (20 per corpus, seeded, seed committed here:
  `20260923`) is read to measure **precision**: is the pairing the one a reader would make?
- **A random sample of 100 non-recomputable tokens** (arithmetic: 40 M, 40 A, 20 F, same seed) is
  read to measure **recall and composition**, each classified into: *proportion whose k and n are
  absent from the sentence*; *proportion whose k and n are present but not in a construction the
  rule reads* (a **rule miss**); *difference, improvement or change*; *threshold, parameter or
  setting*; *other*.

## 7. Predictions, stated before the corpora were fetched

- **P1.** Hand-over rate is higher in M than in A. *Refuted if A ≥ M.*
- **P2.** Hand-over rate is higher in F than in A. *Refuted if F ≤ A.*
- **P3.** At least one **real** arithmetic error (adjudicated, not merely flagged) is found in M
  and at least one in A. *Refuted if either corpus yields none.*
- **P4.** F contains **zero** real arithmetic errors. *Refuted by one.*
- **P5.** The hand-over rate is **below 50 % in all three corpora**. *Refuted if any corpus
  reaches 50 %.*
- **P6.** Rule misses (§6, third bullet) are **under 15 %** of the non-recomputable sample.
  *Refuted at 15 % or more.*

## 8. Kill conditions

- **K1.** If hand-read precision on the 60-token sample is below **0.85**, the hand-over rates do
  not ship as rates. Only the hand-read counts ship, and the rule ships as a failed instrument.
- **K2.** If more than **20 %** of either world corpus fails to fetch, or its abstracts are
  detectably truncated, that corpus is declared unfit and reported as unfit rather than analysed.
- **K3.** If every flagged inconsistency adjudicates to *rule error*, the session reports **zero
  arithmetic errors found** and says the instrument found none — not "errors were detected".
- **K4.** If corpus F yields fewer than 30 percentage tokens, it is too small for a rate and only
  its counts ship.

## 9. What generalises, and what does not

A hand-over rate measured on two corpora of one month and one query is a statement about those
corpora. What is offered as general is the **shape**: that the ceiling on automated claim
verification is set by the text's conventions and not by the verifier's capability, and that this
ceiling is measurable cheaply and without a model. What is explicitly **not** claimed: any
statement about whether the un-checkable numbers are wrong. They are un-checkable; that is the
whole point, and an un-checkable number is not thereby a false one.

## 10. Landing

This artifact ships with `data/`, a `check.py` that re-derives every number on its page from
`data/` with **no network**, and a `tamper.py` whose every deliberate corruption of the evidence
must be caught by a **named** failing check. The check suite must prove it ran what it counted —
09-22's bad test 12 was a suite that reported 58 checks while five never ran.

## 11. Amendments

*Anything added below is dated and carries its reason. Nothing above is edited after a number has
been seen.*

- *(none at time of commit)*
