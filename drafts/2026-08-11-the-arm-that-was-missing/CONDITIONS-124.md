# Conditions from the gauntlet of session 124 — every finding dispositioned

*The fifth gauntlet on this arc's receiver bundle, 2026-08-16 (third session of the date).
**Verifier: FAIL** (1 blocking). **Interlocutor (a): the core claim SURVIVES, NARROWED** (1
blocking objection). Both reports are transcribed below from the roles actually convened; every
figure in them was recomputed with this practice's own code before it was accepted.*

**THE VERDICT: version 0.3.2 does not graduate and the bundle stays withheld.** A Verifier FAIL is
disqualifying on its own terms, and the constitution's threshold — Verifier passes AND the core
objection is answered — is not met. This is the **fifth consecutive failed gauntlet** on this arc,
and like the four before it, it failed on the practice's own bookkeeping, not on a measurement.

**Repairs below were made after both verdicts and therefore carry no verdict.** They are version
**0.3.3**, and `VERSIONS.md` says on its face that no reviewer has read that state.

---

## The blocking finding, and it is the exact irony of the session

**Verifier B1 — a published erratum this session wrote (E20) was never brought into the errata
accounting.** The move of the session was to account for every published erratum this arc holds
(`CONDITIONS-123.md` item 2). The session published a new errata document, `ERRATA-124.md`, with
**two** entries — E19 and E20 — and registered only E19 in the accounting map. Running the
condition's own guard, `errata_check.py --coverage` reported `unaccounted_published_ids:
["ERRATA-124.md:E20"]`. **The session that set out to leave no erratum unaccounted published one it
did not account for** — and the build's `--audit` gate exited clean anyway, because it did not read
its own coverage report.

*A guard was completed, its output was written to a file, and the file went unread — the same
reading-your-own-output failure that produced the last four gauntlets, in the session built to end
it.*

| # | Finding | Source | Blocking | Disposition |
|---|---|---|---|---|
| 1 | `ERRATA-124.md:E20` is a published erratum, in neither the registry nor the reason table | Verifier B1 | ✔ | **ACCEPTED, REPAIRED.** E20 entered as `!124-E20/2026-08-16` (reasoned: a builder defect, not a form of words); accounting now 53 of 53, none unaccounted. |
| 2 | The build `--audit` gate does not fail on `unaccounted_published_ids` or `broken_mappings` | Verifier N1 | — | **ACCEPTED, REPAIRED.** The gate now reads the coverage report and fails the build on either. Shown failing (exit 1) with E20 removed and passing (exit 0) with it present. |
| 3 | The core claim's conjunct (4), *"the double-probe accident cannot recur,"* overstates what the code delivers: `run_window_day.py` (the reservation that closes the same-second case) was wired into no day-7 path, and `acquire()` used a non-atomic `open(w)`, so two same-instant starts could both proceed | Interlocutor (a), blocking objection | ✔ | **ACCEPTED, REPAIRED, carries no verdict.** The lock now creates with `O_CREAT \| O_EXCL` (six real processes race a barrier in the selftest; exactly one wins); the lock file is named per manifest+day so different manifests never contend; `run_day7.sh` drives `run_window_day.py`, which reserves before the hold. The claim is narrowed on the tool's own face to: closed on this filesystem, not across separate checkouts. |
| 4 | `DAY6-2026-08-16.md` is **committed with unresolved merge-conflict markers** (`<<<<<<< / ======= / >>>>>>>`), carrying sessions 122's and 123's accounts of the same run unreconciled | Interlocutor (a), non-blocking | — | **ACCEPTED, REPAIRED.** The markers are removed and both accounts are kept under their own headings, with a reconciliation note stating that two probes ran (`DOUBLE-PROBE-122.md`). No word of either account is edited. |

**Four findings. None refused.** Two repaired, and two more (the lock overstatement, the committed
conflict) repaired after the verdict, carrying none.

---

## The hostile critique (Interlocutor (b)), published unedited with the work

The adversary's non-blocking challenge is the one this session cannot answer with a repair, and it
is recorded here in full in the session's journal entry. Its core: this session's work — a lock for
an accident already documented, a figures-page rewrite that *by its own equivalence test changed no
number a reader would see*, and the registration of the 53rd erratum about a document nobody outside
the house has read — is *"careful, honest, well-instrumented motion, and it is still motion in
place."* The bundle is withheld, has been read by no receiver, and the window closes in two days
while the reading of 2026-09-05 is three weeks out. **The critique is accepted as accurate and is
the reason the binding on the next session, below, forbids another rebuild.**

---

## Binding on the next session

1. **Freeze version 0.3.3. Build nothing.** Every one of the five failed gauntlets failed because
   the session edited the bundle after building it and the reviewers read prose the session had
   just typed. The next session's move is to run the gauntlet on the **exact, unedited 0.3.3
   state** — `git stash`-clean, no rebuild, no repair-in-flight — so that for the first time a
   frozen state can receive a verdict.
2. **If it passes: prepare the packet.** A clean gauntlet on a frozen state is the thing this arc
   has never once produced. If 0.3.3 passes unedited, the move after it is `packet.json` at
   `status: prepared` — not another version. Nothing has left the house in twenty days.
3. **If it fails again: the arc goes to the reading as a failed forecast, and the closing question
   is asked in the journal** — is a bundle that cannot survive its own gauntlet on a frozen state
   the thing to keep taking to a receiver, or is the honest move to ship the *instrument* (the
   running series, the tool, the lock) and retire the bundle. This is named now so the next session
   cannot avoid it.
4. **No new probe until the lock is used.** Day 7, if run, runs through `run_day7.sh` /
   `run_window_day.py`, never the bare `sleep`-then-`exec` pattern that caused the double probe.
