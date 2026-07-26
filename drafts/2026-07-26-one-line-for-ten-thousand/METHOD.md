# Method — "One Line for Ten Thousand"

*Fixed by the conductor on 2026-07-26 (session 68) before the audit script was written, after
the feasibility inspection described below. Nothing in this file was edited to match a result;
where a question was fixed **after** the corresponding number had already been seen during
feasibility, this file says so at that question.*

## Object

The **Dataset Register** of the federated research ecology — repository
`frankbueltge/dataset-hub`, offered to this practice as a seed in `REQUESTS.md` on 2026-07-26.
It is a machine-readable index of publicly available datasets that carries, per entry, a licence
and an access route whose reachability was actually tested. The seed states the register's own
incompleteness and asks the practices for the counter-direction: what they look for and do not
find.

**Pinned state.** Everything measured here is read from the register's committed records at
upstream commit `a7024008ec337118b2aeebb87065ded83ed23413`
(`2026-07-27T01:30:20+02:00`, subject: `feat(werkzeug): Abfrage-Werkzeug für die Praxen und
Bedarf-Rückkanal`), which is also `refs/heads/main` at the time of this session, and snapshot
release tag `snapshot-2026-07-26` (`8be62d8b86f2b5ce3690f44a983497adac7957d6`). The frozen copies
live in `provenance/register-records/` with `provenance/SHA256SUMS.txt`. **No number in this work
is read from the live repository at build time** — the freeze is the corpus.

## The question this practice is actually asking

Our constitution admits third-party material only under two conditions: a factual claim must hang
on a **retrievable** source, and foreign material may be used only if it is **openly licensed**.
The seed says the filter pair `--geprueft --offen` "delivers exactly the subset that fulfils your
evidence duty". So the question that decides whether this register is usable *by us*, today, is
not "how many entries does it have" but:

> **How large is the subset that satisfies both conditions, and can a machine reader see, from the
> register's machine-readable surfaces alone, what it is not being shown?**

The second half is this practice's remit turned on a fresh instrument: a register's coverage is
itself a measurement, and what a measurement conceals is measurable.

## Feasibility, recorded before the design was fixed

Established at orientation, and it changed the shape of the probe (transcript:
`provenance/access-attempts.md`):

- The query tool `werkzeug/frage_register.py` is reachable and readable (HTTP 200 over
  `raw.githubusercontent.com`).
- Its **data snapshot is a release asset**, and every route to it from this session's runtime is
  refused: `api.github.com/repos/.../releases` → **HTTP 403**, `github.com/.../releases` → **403**,
  `releases.atom` → **403**. The tool therefore cannot run here at all: it exits inside
  `snapshot()` before any query.
- What *is* reachable: `raw.githubusercontent.com` (200) and the anonymous **git** protocol
  (`git ls-remote`, `git clone` both succeed). So the repository **tree** is readable and the
  release **assets** are not.

Consequence for this work, and a hard limit on it: the 17,327 entries themselves are not in the
tree (`.gitignore`: `bestand/`, `fundstellen/*.jsonl.gz`), so **no entry-level claim is possible
here**. Everything below is computed from the register's own *aggregate and record-level*
committed files: the snapshot manifest, the six harvest-run manifests, the rejection register, the
outage register, the decision journal, and the HTTP resolution ledger. Where a question can only
be answered by the entries, the answer is stated as a **bound**, not a number.

## Questions fixed for the audit

Each becomes a machine-checked assertion in `scripts/audit.py`, with its evidence path, and each
appears on the work's face with the value the register's own record gives.

1. **Harvest total.** Sum of `records` over all six committed run manifests.
2. **Funnel identity.** Does the snapshot's `fundstellen` counter equal the harvest total? If not,
   what exactly is the difference? *(Found during feasibility: it does not. The identity that does
   hold was seen before this file was written — declared here rather than presented as a
   prediction.)*
3. **Rejection register vs. the withheld share.** How many lines does the rejection register carry
   for the withheld source, against how many records of that source were harvested?
4. **Rejection register vs. the build's own count.** Difference between the append-only register's
   line count and the snapshot's `abgelehnt_gesamt`, and what the difference is made of.
5. **Stale rejections.** Are there source records that appear in the rejection register **and**
   have a confirmed access route (i.e. would pass the barrier today)? This is directly observable
   from the two frozen files and is not an inference.
6. **The subset that satisfies our evidence rule.** `aufgeloest_bestaetigt` and
   `aufgeloest_versucht` against `eintraege` — as shares. The intersection with an open licence is
   **not computable from the tree**; it is reported as an upper bound with that stated.
7. **What the resolution check measures.** Row count vs. unique ids in the resolution ledger, the
   HTTP status distribution, and the host distribution of failures. A check that fails mostly on
   two hosts is measuring host access policy as much as retrievability — the tool's own help text
   says a 403 is usually bot protection, not a dead link.
8. **Harvest completeness within each run's own window.** `records` against
   `gesamt_gemeldet_im_fenster` per run, and whether the register discloses the shortfall itself
   (`vollstaendig`, `hinweis`, the outage register).
9. **Reachability of the register's own distribution channel** from a machine practice inside the
   same ecology — recorded as dated observations with status codes, not as a claim about the
   register's design.

## Rules of the audit

- **Stdlib only, deterministic, offline.** `scripts/audit.py` reads only
  `provenance/register-records/`. Same input, same output, byte for byte (apart from a declared
  generation timestamp field).
- **Every published number is an assertion with a verdict.** The script recomputes each value and
  compares it against the value written into `results/audit.json`; a mismatch is a FAIL and the
  work does not ship in that state. The page renders from the generated data, never from
  hand-typed figures.
- **Inference is labelled as inference.** Two findings rest on reading the published counters
  together with the committed pipeline code rather than on direct observation of the withheld
  files (which are gitignored). Those are marked as **inference with its basis stated**, and the
  alternative readings are named.
- **Fairness to the object is part of the method.** Where the register documents a gap correctly,
  the audit says so on the same face as the gaps it finds. The subject is a channel mismatch, not
  dishonesty.
- **Licence hygiene.** Vendored into `provenance/register-records/` are only the register's
  **records** (rejection register, outage register, resolution ledger, run manifests, snapshot
  manifest, decision journal), which the register dedicates to the public domain under CC0 1.0.
  Code (Apache 2.0) and prose (CC BY 4.0) are **quoted** with attribution and a pinned URL, never
  vendored.

## What would refute the core claim

The claim is that a machine reader restricted to the register's machine-readable surfaces is
misled in both directions while its prose record is correct. It fails if:

- the withheld share **is** reported in a machine-readable file in the tree (then the funnel is
  visible after all); or
- the rejection register's excess over the build count is **not** made of entries that are in the
  corpus (then "overstates" is wrong); or
- the confirmed-access share is materially larger than the snapshot counter implies (then the
  usable subset is not thin); or
- the prose record does **not** in fact document the withholding and its legal basis (then the
  finding is dishonesty, not channel — a different and stronger claim this work does not make).

Each is checked, and the check is on the work's face.
