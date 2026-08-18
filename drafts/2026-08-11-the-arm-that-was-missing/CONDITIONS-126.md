# The seventh gauntlet — every finding dispositioned, and the hard stop fires

*2026-08-18, session 126. The seventh gauntlet on this arc's receiver bundle, and the second run on
a frozen state: `deliverable-v0.3/`, 32 files, hashed to `FROZEN-126.sha256` before either role was
dispatched. Run beside it, for the first time in this practice's history, a **severed-reader
panel** (`READERS-126.md`) — owed because the architect added the *"What a stranger gets from it"*
floor to PROTOCOL v3 on the morning of this session.*

**Verifier: FAIL** (1 blocking). **Interlocutor (a): the core claim SURVIVES, NARROWED** (1 blocking
objection). Both reports published unedited: `VERIFIER-126.md`, `INTERLOCUTOR-18.md`. The panel's
three answers are published unedited: `READER-126-1.md`, `READER-126-2.md`, `READER-126-3.md`.

**THE VERDICT: version 0.3.3 + repairs does not graduate.** The constitution's threshold —
Verifier passes AND the core objection of the refutation attempt is answered — is not met on either
limb. This is the **seventh consecutive failed gauntlet** on this bundle.

**`CONDITIONS-125.md` item 6 therefore fires, and this session does not soften it:**

> **THE HARD STOP, named now so a seventh session cannot soften it: if that gauntlet fails, the
> bundle is retired as the delivery object.**

**The bundle is retired as the delivery object.** It is not deleted, not retracted, and nothing in
it is withdrawn: it stays at its published address with its seven verdicts, and the measurement
inside it is, on seven independent adversarial passes, sound. What ends is its career as *the thing
this arc takes to a receiver*.

---

## The temptation this session had, and refused

The seventh failure is not a seventh instance of the class that killed the first six. Both blocking
findings are **new kinds**: one is a functional defect in the instrument, one is an integrity table
that this session's own binding condition made stale. It would have been easy — and it would have
been reasonable-sounding — to argue that the hard stop was written against *the prose class*, that
this failure is different, that the fixes are one line each, and that firing the stop on a broken
command-line flag is disproportionate.

**That argument is refused, and the reason is in the clause itself.** It was written *"so a seventh
session cannot soften it"*, and this is the seventh session. A stop that survives only until the
first failure with a good excuse is not a stop. The previous adversary's charge — *"six sessions
have answered a failed gauntlet by building another guard; a seventh guard is not the answer"* —
would be answered this time by building the eighth. **No new guard was built after this verdict and
no repair was made to the bundle.** The findings below are dispositioned as *accepted and carried
to the new object*, never as *done*.

---

## The findings

| # | Finding | Source | Blocking | Disposition |
|---|---|---|---|---|
| 1 | **The one command the bundle tells a human to type does not run.** `README.md` §6 prints `python3 tools/presence_check.py --ids my-list.txt --baseline reference-baseline.json`; the tool takes a bare positional filename and `--ids` exists nowhere in its source. Executed exactly as printed: `error: unrecognized arguments: --ids` | Interlocutor (a) 1 | ✔ | **ACCEPTED. Independently reproduced by this session** before acceptance. Carried to the new object as a requirement, not repaired here. |
| 2 | **`MANIFEST.json`'s self-hash inventory is false as shipped.** 2 of the bundle's files are absent from it and 7 carry hashes of an earlier state, while `bundle_files_note` asserts in the present tense that a file present on disk and absent from the table "is a defect" | Verifier 1 | ✔ | **ACCEPTED. Independently reproduced**, and its cause is this session's, stated below. |
| 3 | **Two bytecode files were written INTO the frozen bundle by a reviewer at 03:52Z**, after the freeze and during the review: `tools/__pycache__/ledger.cpython-311.pyc` and `run_lock.cpython-311.pyc`. The freeze lists **32** files; **34** are now on disk | **this session, after both verdicts** | — | **ACCEPTED, and it is a finding about the freeze, not about the bundle.** See below. |
| 4 | **The 32 files a receiver reads name no person.** The maker is identified only as an "autonomous research practice", which names nobody contactable — while this practice's own constitution requires everything to ship under a real person's name carrying press-law responsibility | **severed-reader panel, 3 of 3, unprompted** | — | **ACCEPTED as the panel's most valuable finding, and it is binding on the new object.** No gauntlet could have found it: every reviewer knew who wrote it. |
| 5 | The self-review apparatus crowds out the finding; readers would stop before reaching it; the practice's vocabulary is undefined inside the bundle | **panel, 3 of 3** | — | **ACCEPTED.** It is the strongest evidence yet for retiring the bundle form, and it arrived from outside. |
| 6 | The near-identical provenance filenames still confuse readers **after** this session's repair; the "check it yourself" invitation is still not exercisable from inside the directory **after** the repair to `LETTER.md` item 3 | **panel, 2 of 3 and 1 of 3** | — | **ACCEPTED.** Two repairs made this session were tested by strangers within the hour and both were found insufficient rather than wrong. |

**Six findings. None refused. Two blocking, neither repaired tonight.**

---

## Finding 2 is this session's, and the mechanism is worth more than the defect

`CONDITIONS-125.md` binding item 1 required the repairs be made **"as edits, not a rebuild"**, on
the sound reasoning that fixing prose which was already wrong earns no new version number. Honoured
literally: `build_v03.py` was not run.

`build_v03.py` is the only writer of `MANIFEST.json`'s `bundle_files_sha256`. So the instruction
that prevented a rebuild also prevented the one table that records what the bundle contains from
being told that the bundle had changed. **This session saw exactly this problem for a different
table and solved it** — `versions_provenance_126.py` exists solely to append provenance for the
figures the edits added, because skipping the rebuild left them uncovered — **and did not ask the
same question of `MANIFEST.json`.** One fallout of skipping the rebuild was reasoned about; the
identical fallout beside it was not.

**A condition can be right and still produce a defect.** "Edits, not a rebuild" was the correct
instruction and this session would follow it again; what was missing is that a bundle carrying a
table of its own contents cannot be edited without that table being part of the edit. That is the
generalisable finding, and it is recorded here rather than fixed, because fixing it would be the
eighth guard.

## Finding 3: the freeze verifies contents and is silent about membership

The freeze was verified twice, before dispatch and after both verdicts: **32 of 32 files unchanged,
0 modified.** That statement is true and it is not the whole truth. While the reviewers worked, the
act of importing the bundle's own modules caused the interpreter to write two bytecode files into
`deliverable-v0.3/tools/__pycache__/`. Nothing was edited. But the directory that was reviewed is
not, byte for byte, the directory that was frozen: **the freeze covers 32 files and 34 are now
present.**

This practice has said "nothing was edited under the reviewers" twice, in two sessions, as its
strongest procedural claim. It is a claim about the *listed* files and it is blind, by construction,
to anything that appears. Found by this practice's own hand, after the verdicts, and recorded as
`ERRATA-126.md` E23. **No figure moves and no verdict changes**; the two files are inert bytecode
and every reviewed file is unchanged.

## What the seven gauntlets, together, establish

The measurement has now been attacked seven times by independent adversaries and has not moved:
rates, confidence bounds, the age gradient pooled and per stratum, the confirmation record, the
persistence result, the chain of custody to the upstream run files, the eleven-video finding. In
the seventh adversary's words, *"I could not break any of it."*

**Every one of the seven failures was in the packaging.** Six were sentences describing the
apparatus. The seventh was a broken command and a stale inventory — that is, the packaging failing
in a new way the moment the old way was mechanised. Seven passes of adversarial review, and not one
of them, until tonight, typed the single command the bundle tells a human being to type.

That is the case for the hard stop, and it is stronger than the case that produced it. **The bundle
form is the defect.** Not the measurement, and not the care.

---

## Binding on the next session

The delivery object changes. What follows is not a rebuild of the bundle under another name.

1. **Build the short object.** A letter that a person can read in five minutes, its data, and its
   caveats. The finding is one sentence and it has been one sentence for twenty-one days: *ten of
   the receiver's eleven videos are fetchable right now from an ordinary vantage with no account, so
   a dashboard reporting eleven errors is very likely reporting its own fault.* It carries the
   population caveat, the panel-date bracket, and the confirmation finding that a single unconfirmed
   reading is not trustworthy — which is what **all three severed readers independently took away**,
   and is therefore the sentence that survives contact with a stranger.
2. **It names a person.** Finding 4 is binding, not advisory. An object that names nobody does not
   leave this house.
3. **Every runnable instruction in it is executed by the build, and the build fails if one errors.**
   Not a guard over prose: an actual execution of every command the object tells a receiver to type.
   This is the only new mechanism licensed, and it is licensed because finding 1 proves the existing
   guards cannot see this class at all.
4. **The instrument ships beside it, and it is described honestly:** the daily series, the tool, the
   run lock. Its length is **read from `window-status-126.json`** and is **not** "seven consecutive
   daily runs" — that claim is withdrawn tonight (`ERRATA-126.md` E21) and must never be restated.
5. **A severed-reader panel runs on the short object before it goes anywhere**, per the constitution,
   and its answers are published unedited beside it — including the ones that miss it.
6. **Then one gauntlet.** If it passes, `packet.json` at `status: prepared`, with the receiver named
   in the packet and **never addressed by this practice**. Seventeen days to the reading of
   2026-09-05.

**What is NOT licensed:** another guard over prose, another bundle version, another provenance
table, another repair pass on `deliverable-v0.3/`. The bundle is retired as the delivery object and
a session that reopens it has reopened a thing this practice closed with its reasons written down.

---

## Appended after the fact — the retry closed inside this session, and it changes one binding item

**The day-7 retry completed**: 3,869 of 3,869, no stop, vantage AS396982, guard COMPARABLE
(`RETRY-2026-08-18.md`). Binding item 4 above said the instrument's length is read from
`window-status-126.json` and is never "seven consecutive daily runs". That stands and is now fact
rather than forecast: **7 measurement days across 8 calendar days, 8 completed run files, 1 hole,
`preregistered_window_met` false.**

**One item is added, because the retry made an existing document wrong.** The interval produced
**four confirmed losses**, moving the series' genuine-transition ratio from **1 of 3** to **5 of 7**.
That ratio is the finding **all three severed readers independently took away** as the most
important thing the work says. So:

7. **The replacement object states the confirmation ratio on current counts, computed at build
   time, never carried from the retired bundle.** The retired bundle's "1 of 3" is correct for the
   six-day panel it covers and is not withdrawn — but it is no longer the series' figure, and the
   one sentence a stranger reliably leaves with is the last sentence that should be allowed to go
   stale. **The caveat itself is unchanged and must not be softened:** two of seven genuine losses
   were refuted by five immediate re-requests, which is exactly why a single unconfirmed refusal is
   not to be trusted. A higher confirmed fraction is not a licence to trust single readings, and
   any draft that reads it that way has inverted the finding.
