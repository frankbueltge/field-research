#!/usr/bin/env python3
"""
Falsification spike (conductor's-hand verify-before-build, session 42, 2026-07-17).

Question: an end-to-end AI-research-automation paper (arXiv:2606.15497; Nature 651,
914-919, 2026) reports that its "Automated Reviewer" (an ensemble of five reviews +
an Area-Chair meta-review, reading the paper text) reaches a balanced accuracy of
0.69 against ICLR accept/reject decisions from the public OpenReview dataset, which it
frames as "comparable to humans (69% vs 66%)" -- where 66% is the NeurIPS-2021
inter-COMMITTEE consistency figure (Beygelzimer et al., arXiv:2306.03262).

Spike: how much of the ICLR accept/reject label is recoverable by a TRIVIAL,
single-parameter predictor -- a threshold on the MEAN human review score -- on the
same public data source the paper cites? This is the gate the Proposer and Skeptic
both demanded before any framing. Nothing here ships; it is an internal probe.

Dataset (pinned, NOT committed -- retrievable + hash-checkable):
  berenslab/iclr-dataset, file data/iclr24v2.parquet
  raw: https://raw.githubusercontent.com/berenslab/iclr-dataset/main/data/iclr24v2.parquet
  sha256: f486c7a0f58c71005ab8f86e6128038ca523a9efe7feb4ab353b37f789d47fb0
  24,445 ICLR submissions 2017-2024; columns incl. `decision` (str), `scores` (int array).
  Described in Gonzalez-Marquez & Kobak, arXiv:2404.08403 (DMLR workshop @ ICLR 2024).

Determinism: no randomness. The threshold is swept over midpoints of the observed
mean-score values and the balanced-accuracy-maximizing cut is reported.

Load-bearing caveats (must appear on any work built from this -- see README):
  1. INPUT ASYMMETRY. This baseline uses the mean HUMAN review score, information the
     paper's from-text Automated Reviewer does not receive. So this is NOT "a trivial
     reviewer beats the LLM reviewer." It measures how far the accept/reject LABEL is a
     threshold on the scores -- i.e. what "balanced accuracy against the decision"
     actually rewards.
  2. NOT A MATCHED-SUBSET REPLICATION. The paper's 0.69 is computed on 1,000 ICLR papers
     (2017-2024) -- the sample SIZE is stated openly in the preprint's main text; only the
     exact sampling of which 1,000 papers is not given. This spike computes on ALL 19,685
     clearly-decided scored papers
     of the same years. So this is a same-corpus stress test on the same public source, not
     a re-run of the paper's pipeline on a matched subset; the SIZE of the 0.88-vs-0.69 gap
     is not established, only that the comparison as stated omits the score axis.
"""
import sys
import numpy as np
import pandas as pd

PARQUET = sys.argv[1] if len(sys.argv) > 1 else "iclr24v2.parquet"


def is_accept(d: str) -> bool:
    return d.strip().lower().startswith("accept")


def is_reject(d: str) -> bool:
    return d in ("Reject", "Desk rejected")


def balanced_accuracy(y, pred) -> float:
    y = np.asarray(y); pred = np.asarray(pred)
    tpr = pred[y == 1].mean() if (y == 1).any() else 0.0
    tnr = (1 - pred[y == 0]).mean() if (y == 0).any() else 0.0
    return 0.5 * (tpr + tnr)


def best_threshold(y, s):
    uniq = np.unique(s)
    cands = np.concatenate([[uniq[0] - 1], (uniq[:-1] + uniq[1:]) / 2, [uniq[-1] + 1]])
    best_ba, best_t = -1.0, None
    for t in cands:                       # deterministic sweep
        ba = balanced_accuracy(y, (s >= t).astype(int))
        if ba > best_ba:
            best_ba, best_t = ba, t
    return best_ba, best_t


def report(sub, name):
    sub = sub.dropna(subset=["mean_score"])
    sub = sub[sub["y"] >= 0]
    y = sub["y"].values; s = sub["mean_score"].values
    ba_const = balanced_accuracy(y, np.ones(len(sub)))
    ba_best, t_best = best_threshold(y, s)
    print(f"[{name}] n={len(sub)}  accept_rate={y.mean():.3f}  "
          f"BA(constant)={ba_const:.3f}  "
          f"BA(best mean-score threshold)={ba_best:.4f} at mean>= {t_best:.2f}")
    return ba_best


def main():
    df = pd.read_parquet(PARQUET).copy()
    df["mean_score"] = df["scores"].apply(
        lambda a: float(np.mean(a)) if a is not None and len(a) > 0 else np.nan)
    # primary label: Accept* = 1; Reject/Desk-reject = 0; Withdrawn/Invite-to-Workshop = -1 (excluded)
    df["y"] = df["decision"].apply(lambda d: 1 if is_accept(d) else (0 if is_reject(d) else -1))

    print("PRIMARY: clearly-decided (Accept* vs Reject/Desk-reject), scored papers, 2017-2024")
    report(df, "ALL 2017-2024")
    print("\nPer year (robustness):")
    for yr in sorted(df["year"].unique()):
        report(df[df["year"] == yr], f"  {yr}")

    print("\nSENSITIVITY: Withdrawn + Invite-to-Workshop counted as REJECT")
    d2 = df.copy()
    d2["y"] = d2["decision"].apply(lambda d: 1 if is_accept(d) else 0)
    report(d2, "ALL 2017-2024 (withdrawn=reject)")


if __name__ == "__main__":
    main()
