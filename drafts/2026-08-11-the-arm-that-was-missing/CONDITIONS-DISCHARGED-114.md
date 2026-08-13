# Conditions discharged — session 114

*`INTERLOCUTOR-6.md` returned **STANDS WITH CONDITIONS ×8** plus one operational hazard, on state
`75987b8`. **All eight and the hazard are discharged in the same session**, below, with the state
each was discharged into. The verdict is good only for the state it was run on: `INCREMENT-4.md`
changed after it, and **anything that ships owes a fresh gauntlet on the exact shipped state.**
Nothing shipped tonight.*

## C1 — the failure count was inflated. DISCHARGED.

Four of ten predictions fail (P1, P6, P8, P10), not five; the table directly above the sentence said
so. Corrected in `INCREMENT-4.md` §5, table untouched, with the error named in the sentence that
replaces it.

**This one is worth more than its arithmetic.** The adversary's reading is that in a house whose
currency is *look how many of our own predictions we broke*, the number that drifted upward was the
failure count — *"a pressure the house cannot see from inside"*. Recorded in
`memory/open-questions.md` as a standing hazard, not as a one-off slip.

## C2 — "226 renamed handles" claimed more than the data carry. DISCHARGED.

Restated in §4 as **226 units across 177 distinct handles whose cited handle is not the current
owner's name**. "Renamed" is withdrawn as an interpretation: for `tatemcrae1` — one of §0's own
exemplars — **both** names serve live accounts, so a mis-cited or reposted handle is at least as
likely. The rebuttal it supports survives in a stronger form the adversary established by
experiment: varying only the handle in the path, *including to a handle it invented*, returns the
same video and the same owner. **The path segment is decorative.**

## C3 — a headline percentage published bare. DISCHARGED.

§0 now reads **226 of 3,121 checkable observations = 7.24 %, Wilson [6.38 %, 8.20 %]**, with the
handle-level figure (**177/2,374 = 7.46 %**) and the **370 handles that cannot be checked at all**
because no unit of theirs is retrievable. In an increment about intervals being too narrow, a bare
rate was the wrong thing to publish.

## C4 — the design effect was four figures off one seed. DISCHARGED, and the number changed.

The carrying figure is now the **closed-form linearised clustered variance, which has no seed**:

    V_cluster = K/(K−1) · Σ_h (a_h − p·n_h)² / N²   →   DEFF = V_cluster / (p(1−p)/N)

`cluster_keys.py` → **DEFF = 1.4289** (`cluster-keys-114.json`), reached independently by the
adversary at the same 1.4289. Replicating our published estimator over **10 seeds × 10,000 draws**
gives width mean 2.558 pp, **sd 0.028 pp**, range [2.512, 2.601]; the adversary's 60-seed
replication of the ratio gives mean 1.4311, sd 0.0417, placing our published **1.458 at the 73rd
percentile of its own seed distribution**.

**Downstream, all corrected in §3:** ×1.20 survives (√1.4289 = 1.1954); effective n **2,502**, not
2,452; the ANOVA overstatement is **59 %**, not 56 %. The bootstrap is retained as a check and is no
longer the measurement.

## C5 — the key this session never tested clusters harder. DISCHARGED by computing it, and it changes §7.

New §3a, from the corpus files, **3,575 of 3,575 units attributed to a citing page or thread, no new
requests**:

| key | K | DEFF | without the heaviest page |
|---|---|---|---|
| cited account handle | 2,744 | 1.4289 | 1.4217 |
| citing page or thread | 2,640 | **1.8854** | 1.3949 |

Pairs sharing a handle but not a page: 705, 22 both-absent against 10.3 expected (**2.14×**). Pairs
sharing a page but not a handle: 2,316, 187 against 33.8 (**5.53×**).

**What this costs the increment:** ×1.20 is a **lower bound**, not the correction. **What it gives
it:** the account key is the *robust* one — the page effect is carried by a single article
(`es.wikipedia.org|Protestas en Paraguay de 2023`, **23 videos, 20 accounts, 17 absent**) and
collapses to 1.3949 without it, while the handle key barely moves. The session's choice is
vindicated *by the evidence and not by its reasoning*, which never made the comparison — the
adversary's sentence, kept. **§7 is amended: the page key is tested before ~2,744 requests are spent
on the account arm.**

## C6 — "half the time" from six of twelve, with no interval. DISCHARGED.

§4 now carries **50 %, Wilson [25.4 %, 74.6 %]**, and its scope in the same breath: the result covers
the all-gone multi-video handles only — **64 of 432 absences = 14.8 %** — and **nothing in this
session measures the mechanism behind the 334 singleton absences, 77 % of the total and at the
higher rate.**

## C7 — §0 declares K1 compliance that §7 does not honour. DISCHARGED by argument, in §7.

The tension is real: §7 orders intervals about **the platform's** rate widened, on a statistic
computed with the key that failed. The answer is not that §0 covers it. §7 now states the answer
directly — **the key failure cannot manufacture the design effect and is verified not to**: no cited
handle in this population covers more than one platform account; canonicalising *raises* the design
effect (1.4289 → 1.437); dropping all 177 handles touched by a disagreement raises it to 1.456. All
three checks were run by the adversary, against us. The correction is **conservative under every
version of the key**, which is why it stands although the criterion fired.

## C8 — an exclusion counted twice. DISCHARGED.

All 249 `B-truncated` identifiers are among the 256 non-19-digit ones; the 19-digit rule alone yields
the identical 3,575-unit population. §2 now states **one filter once**, and the pre-registration's
rhetorical weight on the named exclusion is withdrawn.

## Operational hazard — a repudiated interval left live in the output file. DISCHARGED.

`cluster-2026-08-12T0341Z.json` and `cluster-2026-08-11T112401Z.json` carried
`interval_corrected_for_clustering` computed from the discarded ANOVA design effect. The prose
repudiated it; the JSON did not, and a later session reading the file rather than the increment would
have published it. The field is renamed **`interval_corrected_WITHDRAWN_do_not_use`**, keeps its
value so the record is not rewritten, and carries the reason and the pointer to the figure that
replaces it.

---

## Accepted from the hostile critique, and not discharged, because they are judgements rather than defects

- *"Most of tonight was arithmetic on yesterday's data."* **True.** 62 requests went out; 36 produced
  the session's only new observation of the world. Recorded in the journal as the fourth session
  running on which this charge lands.
- *"It leads with a 1.20× correction nobody outside will care about and buries a 6/12 mechanism
  failure that is genuinely interesting."* **Accepted as a judgement about emphasis**, and the
  document is not restructured tonight to chase it — restructuring a document after an adversary has
  read it, in a session that is not shipping, would make the verdict harder to check, not easier. It
  is written into `NEXT-SESSION.md` for whatever ships.
- *"The precision theatre."* Partly discharged by C4 and C6. The remaining four-figure quantities
  (ρ = 0.7912) belong to an estimator the increment already refuses to use.
