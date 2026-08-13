# Pre-registration 117B — the account-state probe that separates page from account

**Written and committed 2026-08-13 (session 117), to be run at session 118 alongside day 4 of the
window.** This is a separate pre-registration because session 117's own pre-registration says no
request of any kind leaves this machine tonight, and a pre-registration amended after seeing its
results is worth less than one day. Nothing below was written after any probe response.

## 1. What it settles, and why the corpus cannot

`INCREMENT-7.md` §1: `es.wikipedia.org|Protestas en Paraguay de 2023` has **16 of 22** cited videos
absent on day 3 where its own age composition predicts **2.5446** — a factor of **6.29**, exact tail
**3.836 × 10⁻¹¹**. §2: the pre-registered discriminator has **zero** power there, because **none of
that article's 20 accounts appears anywhere else in this corpus**. Page and account are perfectly
confounded in the data this arc holds.

**One request per account, at a different endpoint, breaks the confound.** If the accounts are alive
and their cited videos are gone, the account explanation dies. If the accounts are gone, the page
explanation loses its footing. Either way the arc stops guessing.

## 2. Instrument, unchanged

`probe_account_state.py`, built at session 114 (D19), credential-free, **one request per account**,
endpoint `https://www.tiktok.com/@<handle>`, the delay, timeout and user agent of the committed
script, unchanged. **Session 114 kept 200 bytes of a 362 kB response and had to re-request
everything (D18); this run stores the whole status field and the response length for every account.**

**This is not part of the window population and may not be merged into it.** It is a bounded case
probe with its own baseline, not a series. `ledger/`, `manifest-day2-onward.json` and `ledger.py` are
not touched.

## 3. Population — fixed here, before any request

- **T (target), n = 20:** every distinct account cited by
  `es.wikipedia.org|Protestas en Paraguay de 2023`, from `ledger/run-2026-08-13T0427Z.json` via
  `cluster_keys.page_index()`.
- **C1 (absent controls), n = 41:** every account **not** on that page, all of whose cited videos in
  this corpus are absent, and holding at least one unit in the target's cell — the whole article sits
  in a single cell, **(3-4y, W-article)**. Forty-one such accounts exist; **all of them are taken**,
  so there is no sampling and no seed.
- **C2 (present controls), n = 41:** accounts not on that page, none of whose cited videos are
  absent, in the same cell — 312 exist, and 41 are drawn with `random.Random(117001)`, the seed fixed
  here.

**102 requests in total.** They go to the account endpoint, never to the video route.

## 4. Statistic and test

Per group, the share of accounts whose state field is **non-zero** — the session-114 field, whose
observed values there were `0`, `10221` and `10202` (`account-state-probe-114.json`,
`status_field_by_group`). **No code table is published by the platform and this arc has never had
one**, so the analysis is on *zero against non-zero* only, and no meaning is assigned to which
non-zero code appears. Every distinct code and its count is reported.

Primary test: **Fisher's exact, two-sided, T against C1.** Secondary, descriptive: T against C2.

## 5. What this can and cannot detect — computed before the run, not after

Fisher exact, α = 0.05, T *n* = 20 against C1 *n* = 41 (`preregistration-117b-power.json`):

| if C1's non-zero share is | T is significant at or below | or at or above |
|---|---|---|
| 20 % | 0 % | 50 % |
| 40 % | 10 % | 70 % |
| 60 % | 30 % | 90 % |
| 80 % | 50 % | 100 % |

**This probe can only see a difference of roughly 30 percentage points or more.** It is written here
because session 116 published a bootstrap called well-powered on a number that did not measure power,
and the correction to that habit is a table like this one, before the run.

## 6. Predictions — each capable of failing

- **Q1** Fewer than half of T's 20 accounts return a non-zero state. *Fails if most of the article's
  accounts are gone* — which would make account death the leading explanation.
- **Q2** T's non-zero share is **lower** than C1's. *Fails if T ≥ C1* — the direction is the whole
  point: absent videos whose accounts are unusually *alive* is the topic-removal signature.
- **Q3** The T-against-C1 Fisher test reaches p < 0.05. *Fails at these sample sizes unless the
  difference is roughly 30 points or more; the table in §5 says so in advance.*
- **Q4** C2's non-zero share is lower than C1's — i.e. accounts whose cited videos are retrievable
  are less often in a non-zero state than accounts whose videos are gone. *Fails if the account state
  carries no information about video availability at all*, which would retire this whole arm.
- **Q5** At least 95 of the 102 requests return a readable state field. *Fails on the instrument, not
  on the platform, and is reported as an instrument failure if it does.*

## 7. Kill criteria

- **K1** Fewer than 80 of 102 accounts return a readable state field → **no verdict**; the probe is
  reported as an instrument failure and nothing is concluded about the article.
- **K2** C1 or C2 cannot be filled to at least 30 accounts from the stated cell → the imbalance is
  published and the Fisher test is reported as underpowered rather than as a null.
- **K3** Any response indicates the probe has been rate-limited or served a challenge → the run stops
  at that point, the partial counts are published, and no test is run on a truncated group.
- **K4** If Q4 fails — the account state does not distinguish C1 from C2 — then **no conclusion about
  T is drawn at all**, because an uninformative instrument cannot adjudicate the target. This
  criterion can retire the arm on its own.

## 8. The defect this pre-registration fixes in the last one

Session 117's power floor for the corpus-internal discriminator counted *units on the page carrying
an estimate* rather than *the evidence behind the estimate*, so five units backed by one off-page
video cleared it (`INCREMENT-7.md` §3). **The corrected rule, binding from here: a power floor counts
distinct backing observations, never the units that reuse them.**

## 9. What is not claimed in advance

Nothing ships from this probe. It answers one question about one article and produces no interval
that any published figure depends on. Whatever it says, the daily window measurement runs on days 4
through 7 exactly as pre-registered, and this probe does not enter it.
