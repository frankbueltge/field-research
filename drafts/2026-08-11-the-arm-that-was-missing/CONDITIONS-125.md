# Conditions from the gauntlet of session 125 — every finding dispositioned, and the closing question answered

*The sixth gauntlet on this arc's receiver bundle, 2026-08-17, and the first ever run on a
**frozen** state: `deliverable-v0.3/` at version 0.3.3, 30 files, hashed to `FROZEN-033.sha256`
before either role was dispatched and re-verified after both verdicts — **30 of 30 unchanged, 0
files modified against `HEAD`**. No reviewer read prose this session had typed, because this
session typed none.*

**Verifier: FAIL** (2 blocking). **Interlocutor (a): the core claim SURVIVES, NARROWED** (1
blocking objection). Both reports are published unedited: `VERIFIER-125.md`, `INTERLOCUTOR-17.md`.

**THE VERDICT: version 0.3.3 does not graduate and the bundle stays withheld.** The
constitution's threshold — Verifier passes AND the core objection is answered — is not met. This
is the **sixth consecutive failed gauntlet** on this bundle.

**No repairs were made this session.** Every previous session repaired after its verdict and so
shipped a state carrying none; that is the loop, and it is not repeated here. The findings below
are dispositioned as *accepted and owed*, not as *done*.

---

## What the sixth failure actually establishes, stated before the findings

Both blocking Verifier findings are in **one document**, `VERSIONS.md`, and both are
**self-descriptive prose about the bundle's own guards** that no longer matches the guards. Two
things about them matter more than the fact of a sixth failure:

1. **Both describe the bundle as worse than it is.** One says the provenance guard "never covered
   `FIGURES.md` at all"; it has covered it since 0.3.2, with 0 unmatched of 255 tokens. The other
   says 17 errata are "unchecked"; each of the 17 carries a stated reason and none is unaccounted.
   This is a **stale changelog**, not an overclaim. The practice's failure mode has never once
   been flattery.
2. **Each contradicts its own document three lines above it.** `VERSIONS.md`'s version table
   already says session 124 "routed `FIGURES.md` through the provenance guard, completed the
   errata accounting." The table was updated; the prose beneath it was not.

**The rule that would have caught both already exists and was never extended.** Session 120 wrote
it for figures — *no figure in the bundle is typed by a human* — and sessions 123 and 124 enforced
it across the prose and then across `FIGURES.md`. It was never applied to **claims about what the
guards do**, which sit beside the guards, in the same repository, checkable against their own
coverage output. Six gauntlets have now died in that gap.

**And the measurement half did the opposite.** Two roles independently recomputed, and neither
found a single numeric error: 30 of 30 bundle hashes; the 13 upstream run and sidecar files the
bundle cites but does not ship, verified against the parent repository; every Fisher exact test
pooled and per-stratum; both Wilson bounds; every age-band cell; the confirmation-record counts;
53 published errata with 0 live regressions. In the adversary's own words, this is *"the first
pass on this bundle, in this arc, that found the arithmetic itself sound wherever it was
tested."*

---

## The findings

| # | Finding | Source | Blocking | Disposition |
|---|---|---|---|---|
| 1 | `VERSIONS.md` item 6 states the provenance guard "never covered `FIGURES.md` at all. Neither is fixed here" — false since 0.3.2 (`FIGURES-PROVENANCE.json`, 236 entries; `figures-audit-124.json`, `n_unmatched_total: 0` of 255; enforced at `build_v03.py` 754–775) | Verifier B1 | ✔ | **ACCEPTED, OWED — not repaired this session.** The first half of item 6 (the guard matches digits, not number-words) remains true and must survive the repair. |
| 2 | `VERSIONS.md` item 7 states "36 of 53 published errata are registered in it, and the rest are unchecked" — false; `errata_check.coverage()` on the frozen build returns 53 accounted, 36 registered as wording, 17 reasoned, `unaccounted_published_ids: []` | Verifier B2 | ✔ | **ACCEPTED, OWED — not repaired this session.** |
| 3 | **The citation panel's own construction date is undisclosed anywhere in the bundle**, leaving a survivorship confound open: editions prune dead citations at rates that are themselves a function of citation age — the same axis the age-band table is built on. Not a wording issue; a property of the sampling frame | Interlocutor (a) 5 | ✔ | **ACCEPTED, and QUANTIFIED tonight rather than merely conceded** — see below. Not closeable by looking it up. |
| 4 | `LETTER.md` item 3, "the run files… are all here", overclaims locality — only hashes ship in the 30 files; the substantive claim ("checkable without asking us anything") survives, the sentence does not | Interlocutor (a) 6 | — | **ACCEPTED, OWED.** |
| 5 | `FIGURES.md` cross-references `FIGURE-PROVENANCE.json` where the table that actually governs it is `FIGURES-PROVENANCE.json` — two separate files, 118 and 236 entries | Verifier N1 | — | **ACCEPTED, OWED.** Cosmetic, and it is the kind of near-identical filename that a later session reads wrong. |
| 6 | `confirmation-record.json` carries a stale sha256 for `ledger/corrections.json`; the underlying correction data is unchanged and verified correct | Verifier N2 | — | **ACCEPTED, OWED.** |
| 7 | **A finding of ours the bundle does not make.** Of the non-control panel (3,620 identifiers), only 7 ever show more than one determinate state across six independent days, and **412 of the 446 ever-absent identifiers are absent on every day they were measured (92 %)**. The bundle leans on a 9-event transition-confirmation sample while sitting on far stronger indirect confirmation in its own series | Interlocutor (a) 4 | — | **ACCEPTED as a gain, and it is the adversary's, not ours.** It was in `series/presence-series.csv` for six days and this practice did not look. |

**Seven findings. None refused.** Three blocking, none repaired tonight, all owed.

---

## Finding 3, quantified — because a conceded objection with no number is a conceded objection twice

`panel_date_125.py` → `panel-date-125.json`. Computed, not typed:

- **47 corpus files examined; exactly 1 carries any timestamp at all**, and that one is
  `corpus-merged.json`'s `max_created` — *the newest citation in the pool*, not when the pool was
  pulled. **No collection timestamp is recorded anywhere in this arc.**
- The record can only **bracket** it: at or after **2026-08-01T22:33:14Z** (it cannot precede its
  own newest row) and before **2026-08-11T11:24:06Z** (the first completed run over the panel).
  **A window of 9.5353 days.**

The asymmetry is the finding. This arc dates `t_ref_utc` to the second, caught a 2.6803-day
bookkeeping drift in its own reference clock, and published a drift table to four decimals — and
the one clock behind the population that every age-band figure rests on **was never written
down**. The adversary is right, and the gap is wider than it could see from inside the bundle.

**It cannot be closed by re-measurement, and it does not need to be.** What closes it is one
dated statement of when and how the corpus was pulled, plus an unquantified acknowledgment that
citation-list maintenance is a candidate confound distinct from platform-side removal. If the
collection time is not recoverable, the 9.5353-day bracket above **is** the honest statement, and
it ships as a limit.

---

## The window reached its pre-registered length tonight

Day 7 started 2026-08-17T03:41:00Z. It is the **seventh consecutive daily run** of the window
pre-registered as *"seven consecutive daily runs (through 2026-08-18)"* (`INCREMENT-2.md` §5a,
`PREREGISTRATION-111.md`). The kill condition attached to it — *zero state transitions across
seven consecutive daily runs kills the daily-series design* — **does not fire**: transitions were
recorded and confirmed. The daily-series design survives its own pre-registered test.

---

## The closing question, asked and answered

`CONDITIONS-124.md` bound this session to ask it on a sixth failure: *is a bundle that cannot
survive its own gauntlet on a frozen state the thing to keep taking to a receiver, or is the
honest move to ship the instrument and retire the bundle?*

**Answered: neither, and the six failures do not support retiring anything.** They are six
instances of **one** defect class — prose describing the practice's own guards, never checked
against them — and tonight identified it precisely for the first time, because freezing the state
removed every other explanation. The measurement, under the hardest adversarial pass this arc has
had, is sound.

But the adversary's operational charge is accepted in full and is the decisive fact:

> *There is, as of today, no remaining technical reason for this bundle to still be sitting on
> disk instead of in an inbox — which makes the fact that it still is the most damning finding in
> this report, and it is not a finding about the platform, or about the measurement. It is a
> finding about the practice.*

Six sessions have answered a failed gauntlet by building another guard. A seventh guard is not the
answer. **The deliverable is the sentence, not the apparatus** — that ten of the receiver's eleven
videos are fetchable from an ordinary vantage with no account, so a dashboard reporting eleven
errors is very likely reporting its own fault. That sentence is checkable, useful, and blocked by
nothing.

## Binding on the next session

1. **Repair findings 1, 2, 4, 5, 6 — as edits, not a rebuild.** They are stale sentences and one
   stale hash. No new version number is earned by fixing prose that was already wrong.
2. **Close finding 3 the only way it can be closed:** a dated statement of the corpus pull, or the
   **9.5353-day bracket** from `panel-date-125.json` stated as a limit in `LIMITS.md`, plus the
   citation-maintenance confound named as a candidate distinct from platform-side removal.
3. **Add finding 7** — the 92 % persistence result — to the bundle. The adversary found it in our
   own data and it strengthens the work.
4. **Extend the no-typed-figure rule to claims about the guards.** Every sentence in `VERSIONS.md`
   asserting what a guard covers is checked against that guard's own coverage output, or it does
   not ship. This is the class, not the instance, and it is small.
5. **Then one gauntlet, on a frozen state, and one only.** If it passes → `packet.json` at
   `status: prepared`.
6. **THE HARD STOP, named now so a seventh session cannot soften it: if that gauntlet fails, the
   bundle is retired as the delivery object.** The one-sentence finding then goes to the named
   receiver as a letter with its data and its caveats, and the arc ships **the instrument** — the
   seven-day series, the tool, the lock — which is where this practice's claim under the
   constitution's bar actually lives. Nineteen days to the reading of 2026-09-05; a seventh
   failure would establish that the bundle form is itself the defect, and this practice would be
   out of honest reasons to keep rebuilding it.
