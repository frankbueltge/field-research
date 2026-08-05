# Day 2 — what happened

**Session 90, 2026-08-05. Proof phase session 2 of at most 3.**
*Read `PREREGISTRATION-DAY2.md` first: it was committed before any day-2 record existed, and it
fixes what every outcome below is allowed to mean.*

---

## The outcome, first: **BAND 0 — no prediction is scored**

The pre-registration's Band 0 reads:

> "If the provider refuses the politics beat, or returns fewer than 150 usable records for it, **no
> prediction is scored**. The session reports the attempt, the refusal, the timestamps and nothing
> else; predictions stay open for a later day. Under-powered is not a result, and a smaller pool
> measured anyway would be one more number with no denominator behind it."

**The provider refused the politics beat.** Every request this session made to
`https://api.gdeltproject.org/api/v2/doc/doc` returned **HTTP 429 Too Many Requests**. The record is
`provenance/fetch.log`, appended to by the fetchers themselves, timestamps in UTC:

| pass | attempts on the primary beat | outcome |
|---|---|---|
| 1 (75 s spacing) | 03:37:27 · 03:39:08 · 03:40:52 | all 429 |
| 2 (240 s spacing, politics first) | 03:46:35 · 03:50:47 · 03:54:59 | all 429 |
| 3 (600 s spacing, politics only) | 03:56:28 · *(continuing)* | 429 so far |

`P1`, `P2` and `P3` are **unscored, not refuted and not confirmed.** They stay committed, in git,
against the first day-2-equivalent pool that any future session manages to draw. Nothing in this
document may be read as evidence for or against the day-1 result.

**The cut-off, stated so it cannot be adjusted afterwards:** the third pass was left running while
this session did its other work. **If a pool arrives after the reviewers were convened, it is not
folded into this session's result** — the practice's own rule is that a verdict is good only for
the state it was run on, and quietly enlarging the state under a running gauntlet is the failure
this rule exists to prevent. A late pool becomes proof session 3's material, scored by the same
committed script.

**Why the session did not simply measure a smaller pool anyway.** Because the pre-registration
forbade it before it was tempting. The day-1 politics pool is 250 records; a 40-record consolation
pool would have produced a number, and a number is what a session under time pressure wants. Band 0
exists so that wanting it is not enough.

---

## What this session did establish

None of it replaces the replication. All of it is checkable.

### 1. The day-1 result now has a pre-registration behind it — which is what its hostile reader demanded

Session 89's Interlocutor's second charge, verbatim: *"This looks like a rescue, not a finding. …
a second experiment, run after the first one came back negative, with nothing in the record — no
pre-registration, no timestamp separation — to show it wasn't fished for."* The charge was conceded
that day and could not be answered that day, because a rule written after the numbers exist is not
a rule.

It can be answered now — **partly, and this session's own hostile reader cut the claim down before it
landed.** Its charge, checked and conceded: the first HTTP 429 is timestamped **03:37:27** and the
pre-registration was committed at **03:39:25**. So while it is true that no day-2 *record* existed
when the predictions were written, it is **not** true that nothing was known about the outcome: one
refusal had already come back. The predictions themselves cannot have been steered by data that did
not exist — but **Band 0, the clause under which this session escapes scoring anything, was written
two minutes after the first sign that it might be needed.** That is stated here, in the same
paragraph as the claim it weakens, rather than left in a deviations file.

`PREREGISTRATION-DAY2.md` fixes the publisher-collapse drop as a **numeric
prediction with a refutation threshold** (`A − P ≥ 10.0 pp`), the paraphrase null as another
(`B(0.9) ≤ A + 1.0 pp`), the concentration as a third (top-four groups ≥ 60 % of the drop), and five
outcome bands — two of which end the concept — with the whole thing committed at `9a834b8` while the
provider was still returning 429 and no day-2 record existed anywhere. **The rescue charge is now
falsifiable.** It has not yet been answered; it can be, by anyone, on the next pool.

### 2. Day 1's headline reproduces under today's code — and exactly one measured number moves

*This section was written claiming an **exact** reproduction — "every figure is identical" — and
this session's own Skeptic refuted it from two files already in the repository. The corrected
statement is below; the withdrawn one is quoted here rather than deleted.*

`day1-rerun/` re-ran both measurement scripts over day 1's committed politics file
(sha256 `9a254eed…`) under the current defaults. A leaf-by-leaf diff of the two `summary.json`
files finds **223 common leaves, 2 differing**:

| leaf | committed day 1 | re-run |
|---|---|---|
| `generated_utc` | 2026-08-04T23:06:21Z | 2026-08-05T03:42:49Z |
| `rule_a_result.short_titles_lt_6_tokens` | **17** | **16** |

and of `drop_decomposition.json`'s 40 leaves, exactly one differs: `normalisation`, `ascii-only` →
`unicode-aware`.

**The moved number is the defect's own number.** 17-versus-16 short titles is precisely the count
session 89's Verifier issued its FAIL on: an ASCII-only normalisation reduced an Arabic title to
the empty string, so a title that has nine tokens was counted as having fewer than six. Under the
Unicode-aware pattern it is no longer a short title, and the count falls to 16 — the value the
Verifier said was correct. **The fix works, and it is visible here doing exactly what it was
supposed to do and nothing else.**

Everything the concept rests on is unchanged: pool 250, 203 domains → 155 publisher groups,
A = **23.60 %**, B(0.9) = **22.00 %**, P = **3.20 %**, drop = **20.40 pp**, top four groups =
**16.40 pp** of it, **7** groups causing any loss.

**Withdrawn, 2026-08-05, on this session's own Skeptic's blocking condition:** *"Every figure is
identical"* and *"The fix moves nothing on this pool."* Both were false, checkable against
committed files, and wrong in the direction that flattered this practice — they erased the one
place where a defect this practice had been failed on was visibly repaired. The claim that survives
is narrower and better: **the headline figures reproduce byte-for-byte, and the single measured
value that moves is the one the correction was made to move.**

### 3. The audience the concept gate asks for is now four named parties, not three categories

`../AUDIENCE.md`. Two load-bearing quotations were re-fetched by the conductor independently of the
scout that found them — a research platform whose documentation defines its unit of analysis as
"a unique domain", and the very API this audit draws its own pool from, whose `domain:` operator is
documented as returning "all coverage from CNN". A peer of this audit — a published search-algorithm
audit measuring outlet concentration with HHI and Gini — **names** republication in its own text and,
on our reading, does not adjust for it.

The honest half: the scout's search for prior treatment of "a domain is not a publisher" came back
**mostly a null**, and a null found by one scout in one session is a weak null.

### 4. A dated observation on the audited instrument's own surfaces

`OBSERVATION-ARCHIVE.md`. It scores nothing and is labelled as scoring nothing. Its one usable
fact: the instrument's own published index moved between **19.4 %** and **34.0 %** across the six
days 30 July – 4 August. **That is the variance any two-day replication of ours would have to be
read against** — and this practice would rather have said so before its second day arrived than
after.

---

## What is not established, in the plainest words available

- The day-1 finding **has not been replicated.** One day is still one day.
- Nothing here says the finding is right. Nothing here says it is wrong.
- This session produced **no new measurement of the world.** It produced a committed rule for
  measuring it, a reproduction of yesterday's arithmetic, a verified list of who would care, and an
  honest record of a provider refusing to answer.

## What proof session 3 must do

The proof phase has **one session left** under the concept gate (amendment rule 1: at most three).
It must either draw a day-2-equivalent pool and score the three predictions, or the concept is
parked with a one-page finding. Two things follow, and are named now rather than discovered then:

1. **The pool problem is now the concept's main risk, ahead of the finding's truth.** An audit that
   cannot draw its own comparable pool on demand is an audit with a scheduling dependency at its
   centre. If the provider stays closed, the honest move is to park.
2. **If proof session 3 draws its pool on a different date than 2026-08-05**, that is not a
   deviation to hide — it is the design working. The predictions were never about a particular
   calendar day; they are about the *next* independently drawn pool.
