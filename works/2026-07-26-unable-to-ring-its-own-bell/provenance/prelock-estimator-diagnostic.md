# Pre-lock estimator diagnostic — bounded, and exhaustively listed here

Run by the conductor on 2026-07-26, **before** the pre-registration lock, after the Skeptic
pre-read was dispatched. Purpose: detect *degenerate estimators* — a metric that is
mathematically constant or undefined at this corpus's pool size would make the envelope
undefined (zero residual variance) and the whole probe empty.

**What was computed, exhaustively.** The four metric functions of instrument 018 on the
600-token prefix of **three named units only** — unit 5 (early), unit 44 (middle), unit 70
(late) — plus one earlier single-unit smoke test on the 2026-07-18 entry. No series, no
envelope, no z-value, no window mean, no verdict. Nothing that the pre-registration's decision
rule reads was computed.

```
unit  5: types=330 tail_ranks=230 tail_counts_gt1=1 zipf=-0.0193  mtld=131.67 hapax=0.6939 top50mass=0.4483
unit 44: types=296 tail_ranks=196 tail_counts_gt1=1 zipf=None     mtld=125.11 hapax=0.6588 top50mass=0.5050
unit 70: types=371 tail_ranks=271 tail_counts_gt1=0 zipf=0.0      mtld=157.26 hapax=0.7601 top50mass=0.4000
```

(earlier smoke test, 2026-07-18 entry, 600 tokens, 310 types: zipf slope exactly `0.0`,
mtld 108.69, hapax 0.7258, marker rate 33.33 per 1,000 over 20 marker tokens)

## The finding, and the design change it forced before the lock

**The Zipf-tail slope is degenerate on document-scale pools.** At 600 tokens a unit holds
roughly 300–370 types, and beyond rank 100 the frequency table is almost entirely hapax: the
counts above rank 100 that exceed 1 number **0 or 1** in every unit checked. A tail whose counts
are all 1 has `log10(count) = 0` at every rank, so the OLS slope over ranks 101…max is exactly
`0.0` (unit 70) or a near-zero artifact of the single non-hapax point (unit 5). One of the three
units (44) has 296 types and is **non-computable** under the parent instrument's own
`types < 300` gate.

An estimator that is identically 0 has zero residual variance in the envelope fit, which makes
`z` undefined by division by zero — not a weak metric, an empty one.

**Consequences, applied to the pre-registration before it was locked (§3, §4, §10, §12):**

1. Metric 3 is **substituted**: Zipf-tail slope → **top-50 frequency mass** (the share of the
   600-token pool's tokens accounted for by its 50 most frequent types), collapse direction
   **up**, entering the envelope with sign flipped. The diagnostic shows it live and varying
   (0.400 – 0.505 across the three units).
2. The Zipf-tail slope is **kept as a non-decisional reported diagnostic** — its degeneracy at
   this scale is itself a result about the parent instrument's transferability, which is the
   series' own subject matter.
3. The envelope-window halt rule is repaired (see §4): non-computable envelope units are
   excluded from the fit with the reduced df disclosed, instead of non-deciding the metric.

**Why this is a legitimate pre-lock change and not a degree of freedom.** The substitution is
driven by a *mathematical* property of the estimator at this pool size — demonstrable, and
demonstrated above, without any reference to whether the resulting series trends up or down. No
z-value, no envelope, no window mean and no verdict existed when it was made. It is recorded
here, in the pre-registration's §3/§12, and in the session's journal entry, so that a reader can
check the claim rather than take it.

**Residual risk, disclosed.** Top-50 frequency mass and hapax share are computed from the same
frequency table and are negatively related by construction, so they are not two independent
channels. The pre-registration's §7 carries a pre-committed downgrade for a finding that rests
on those two alone.
