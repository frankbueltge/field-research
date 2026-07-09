# Verification — The Floor

The record of the session-17 shipping gauntlet (2026-07-09), so the work's factual base can be
re-audited by anyone. Method differs from instrument 012's hash-anchored record for an honest
reason: this environment has no direct egress to the primary hosts (raw PDF download fails at the
proxy), so the primaries were read via server-side full-text extraction instead, and no file
hashes are recorded — recording hashes we could not compute ourselves would be fabrication.

## Method (reproducible)

1. The conductor fetched every load-bearing source first-hand via web research (server-side
   full-text extraction of the PDFs/pages listed in `SOURCES.md`), before any role was briefed —
   quote-level queries against each document, verbatim passages captured.
2. An independent Verifier (not the Builder) re-checked every quote and figure against that
   material, re-fetched what it could reach live itself, and recomputed all arithmetic with an
   independent implementation. It reported explicitly which items it verified live vs. against
   supplied excerpts.
3. An independent Skeptic recomputed the arithmetic again and attacked the core claim (round 1)
   and the reworked state (round 2, fresh convening).
4. Two closing micro-checks ran on the exact committed states after each round of fixes.

Anyone can repeat this: fetch the URLs in `SOURCES.md`, search for the quoted passages, and
recompute the derivations below by hand.

## Result

- **Verbatim quotes: all confirmed against the primaries** — the Figure-4 framing sentence, the
  27%/17% growth sentence (elision marked), the market-based Scope 2 sentence, the 84%/1.56
  industry comparison, the bridge-graphic totals paragraph (11.5M/+51%, 3.1M/+241%, 8.4M/+25%),
  the full six-year GHG inventory table (digit-for-digit), the 2024 report's fleet-PUE table
  (1.10 × five years) and per-site rows, the PUE definition/floor texts, the "PUE Abuse" prior
  art, The Green Grid's management-tool language, REHVA's near-floor passage, the leased-scope
  note, and the postscript's two 2026-report sentences (37% growth; PUE 1.09 / 83%).
- **Derived values: recompute exactly** (independently by Verifier, Skeptic, and conductor):
  headroom (1.09−1.00)/1.09 = 8.26%; verdict ratio 8.26/27 = 0.306; breakeven 1.10/1.27 = 0.866 ≈
  0.87; floor crossing at exactly 10% for base 1.10 (9% for base 1.09 — disclosed as
  base-dependent); implied-IT-growth route 28.2% → 0.858 ≈ 0.86; robustness 1.10/1.17 = 0.94;
  postscript 1.09/1.37 = 0.796 ≈ 0.80; emissions growth +120.5%; industry headroom
  (1.56−1)/1.56 = 35.9%.
- **Two blocking findings were caught by the gauntlet and fixed before shipping** (the record is
  the point): a paraphrase dressed as a verbatim quotation in `SOURCES.md` (the "12%" highlight),
  replaced with the verified wording; and a 120% / 121% rounding inconsistency between prose and
  the rendered figure, unified at 120.5%. Both are ledgered in `memory/discarded.md` (session 17),
  with two further corrections (an inferred "TPU v2" label; an uncited "≥12 months" detail).

## Scope and limits

- This check verifies **factual accuracy** — transcription against the primaries and the
  arithmetic on top of them. It does not, and cannot, adjudicate the work's **framing** (whether
  putting a near-floor ratio's foregrounding "on trial" is fair comment); the work carries that
  question itself: the concession beside the exhibit states Google's literal claim is true and
  marks the offset reading as the collective's own interpretation, and the Interlocutor's hostile
  critique — which attacks exactly this — is published verbatim in `journal/2026-07-09.md`
  (session 17).
- The GHG inventory table and per-site PUE table were extraction-verified and internally
  cross-checked (the +241% operations claim recomputes exactly from the table), but not re-pulled
  byte-for-byte from the raw PDFs in this environment (no direct egress) — stated here rather
  than papered over.
