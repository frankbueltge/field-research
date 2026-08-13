# Pre-registration — session 116, 2026-08-13 (second session of the date)

*Committed before any analysis of this session was run. No new requests leave this machine tonight:
the window population, its manifest and its probe are untouched, and the account-state arm stays
outside the window. This is a re-analysis of runs already collected.*

## Why this exists

Session 115 published a conditional permutation test claiming the citing page adds nothing beyond
the account, and withdrew it the same night: only 113 of 3,575 units could move under that null, and
**zero of them lie inside the article that carries the entire page effect**
(`CONDITIONS-DISCHARGED-115.md`). The test could not have detected what it was looking for. Until a
test with power exists, the arc's ×1.20 interval correction stands as a **lower bound** on that
ground.

The arc has two design effects measured **separately** and never together:

| key | DEFF | source |
|---|---|---|
| account handle | **1.4289** | `cluster-keys-114.json`, closed form, no seed |
| citing page / thread | **1.8854** | same file, same units |

Neither is the right number. The account key ignores that two accounts' videos can sit on one page;
the page key ignores that one account's videos sit on many pages. **Tonight builds the model that
carries both at once.**

## Population

`ledger/run-2026-08-13T0427Z.json` — the day-3 run, the completed one (the killed attempt wrote
nothing; D20). Same exclusions as `cluster_model.load`, unchanged: arm `B-truncated` dropped,
`INDETERMINATE` dropped, 19-digit identifiers only. Then restricted to units the corpus files
attribute to a citing page or thread (`cluster_keys.page_index`) — the **crossed subset**, the only
population on which both keys exist. Every comparison against the account-only key is recomputed on
this same subset, never against the published full-population figure.

`ledger/run-2026-08-12T0341Z.json` (day 2) is run identically as a stability check.

## The model

For unit *i* with account *A(i)* and citing page *P(i)*, let *y_i* = 1 if NOT-RETRIEVABLE:

    y_i = mu + a_{A(i)} + b_{P(i)} + (ab)_{A(i)P(i)} + e_i

with all four terms independent, mean zero, variances `sigma2_A`, `sigma2_P`, `sigma2_AP`,
`sigma2_E`. This is a **crossed** — not nested — random-effects model, because an account appears on
many pages and a page cites many accounts.

**Route 1 — moments, closed form, no seed.** For *i ≠ j*:

| pair class | Cov(y_i, y_j) |
|---|---|
| same account, different page | `sigma2_A` |
| same page, different account | `sigma2_P` |
| same account **and** same page | `sigma2_A + sigma2_P + sigma2_AP` |
| neither shared | 0 |

Each variance is estimated as the mean of `(y_i - p)(y_j - p)` over its pair class, with `p` the
pooled absence rate on the subset. Then, with `M_A` the number of ordered same-account pairs
(`sum_a n_a^2 - N`), `M_P` likewise for pages and `M_AP` for account×page cells:

    DEFF_crossed = 1 + [ sigma2_A*M_A + sigma2_P*M_P + sigma2_AP*M_AP ] / ( N * p(1-p) )

**Route 2 — two-way cluster-robust, model-free.** Cameron, Gelbach & Miller: *"we obtain three
different cluster-robust 'variance' matrices … by one-way clustering in, respectively, the first
dimension, the second dimension, and by the intersection … Then we add the first two variance
matrices and subtract the third"*
(https://cameron.econ.ucdavis.edu/research/JBESpaper2009version.pdf, version of 2009-05-15; published
as *Robust Inference With Multiway Clustering*, JBES 29(2), NBER Technical Working Paper 327,
https://www.nber.org/papers/t0327). Here that is `V_2way = V_A + V_P - V_AxP`, each component the
one-way linearised ratio-estimator variance this arc already uses (`cluster_keys.deff_analytic`).
The same authors record that the estimator **can come out non-positive-definite** in finite samples;
that is K2 below, not a surprise.

The two routes are algebraically the same object up to the finite-cluster factors, so the code
computes a **third form directly** — the double sum `(1/N^2) * sum_{i,j} u_i u_j * 1[same account or
same page]`, `u_i = y_i - p` — and asserts it equals `V_A + V_P - V_AxP` computed **without** the
`K/(K-1)` factors. If that identity fails, the implementation is wrong and nothing is published.

**Route 3 — the components envelope.** Accounts and pages form a bipartite graph; any dependence
this model can express lies **inside a connected component**. Components are therefore a legitimate
one-way key carrying both effects, and `DEFF_component` from the same closed form is an upper
envelope. Uncertainty on `sigma2_P` comes from a bootstrap resampling **components** with
replacement, 10,000 draws, seed fixed in the script, percentile interval.

## Predictions, written before the numbers

- **P1** `DEFF_crossed` > the account-only DEFF **on the same crossed subset** — the page adds.
- **P2** `sigma2_P` > 0 with a component-bootstrap 95 % interval excluding 0.
- **P3** Dropping the single heaviest page (`es.wikipedia.org|Protestas en Paraguay de 2023`, 17 of
  23 cited videos absent, session 115), `sigma2_P` stays positive but its interval **includes** 0 —
  the page effect is real in the corpus as a whole and **not established** without that one article.
- **P4** `DEFF_crossed` < 1.8854, the page-only figure — the page key over-states because it absorbs
  account structure.
- **P5** Route 1 and route 2 agree within **0.20** absolute DEFF.
- **P6** The bipartite graph has a giant component holding **> 50 %** of attributed units — which
  would make the component bootstrap weak, and is the outcome that costs us, not the tidy one.
- **P7** Day 3 and day 2 `DEFF_crossed` differ by **< 0.15** absolute.

## Kill criteria — each written with the outcome that would pass it

- **K1** `sigma2_A <= 0` on the crossed subset → the account effect does **not** survive controlling
  for the page, and this arc's whole ×1.4289 correction is page-driven and must be restated as such.
  (Passes if `sigma2_A` is clearly positive, which is the outcome three sessions of account-key work
  predict.)
- **K2** `V_2way <= 0` or `DEFF_2way < 1` → the model-free route yields nothing usable; it is
  reported as failed and **not** presented as corroboration of route 1. (Passes if `V_2way` is
  positive, which the authors' own caveat says is the common case away from fixed effects.)
- **K3** attributed share < **90 %** of the day-3 analysis population → the crossed analysis is on a
  subset that is not the arc's population; its composition is published and every claim is
  restricted to it. (Passes above 90 %.)
- **K4** `DEFF_crossed <= DEFF_account` on the same subset → the sentence "×1.20 is a lower bound on
  the page ground" is **refuted**, and it is struck from `NEXT-SESSION.md` and from
  `RESTATEMENT-2026-08-13.md` in a dated line, not silently.
- **K5** routes 1 and 2 differ by **> 0.50** absolute DEFF → they are not measuring the same thing;
  both are published and **neither** becomes the arc's number until the discrepancy is explained.

## The consequence, committed before the number is known

If `DEFF_crossed > 1.4289 + 0.05`, then the 36 intervals restated this morning are **still too
narrow**, and they are recomputed at the crossed design effect **tonight**, as a dated addendum to
`RESTATEMENT-2026-08-13.md` — never a silent edit of it. If `DEFF_crossed` lands at or below 1.4289,
the published restatement stands unchanged and this session says so plainly.

## The standing check becomes a script

Three consecutive sessions published a number their own machine-written file refutes (113: a bound;
114: "five of ten" over a table showing four; 115: a per-cell maximum of 1.7052 over a table topping
out at 1.6739). Session 115's handover asked whether a discipline that has failed three times should
be a script. Tonight it becomes one: `prose_vs_json.py` reads every number in a prose file and
checks each against the JSON files of this draft, reporting what it could not match. It is run on
this session's own increment before that increment is committed, and **its failures are published
whether or not they are flattering.**
