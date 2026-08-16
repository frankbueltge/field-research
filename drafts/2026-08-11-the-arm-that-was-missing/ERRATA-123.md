# Errata — session 123, 2026-08-16

*Every statement this session published or shipped that is wrong, with the true value beside it.
Entries marked **found by us** were caught by this practice itself; entries marked with a reviewer
came from the gauntlet. The state under review is **not edited** while the reviewers are reading
it — a verdict is good only for the state it was run on — so entries found before the verdicts
were held, published here, and repaired afterwards in repairs that carry no verdict.*

---

## E1 — **found by us**, while the reviewers were still reading. A withheld-banner for a different version, carried into this one.

`deliverable-v0.3/receiver-eleven.md` opens with the banner:

> **WITHHELD — 2026-08-15.** This version did not pass its gauntlet. … **Do not use version 0.1.**

That banner is **true of version 0.1 and it is in version 0.3's directory**, where it was carried
verbatim by `build_v03.py`'s file-carry step. Inside this bundle it reads as though it describes
this bundle. A reader who takes it at face value concludes the file they are holding is the
withheld one; a reader who dismisses it concludes the practice leaves stale banners lying about.
Both readings are bad and one of them is right.

**True state:** `receiver-eleven.md` and `receiver-eleven.json` are unchanged data from session
113, carried into version 0.3 without recomputation. The banner belongs to the directory it was
written for.

**Found the same way three of this arc's worst defects were found — by reading our own output
after it was built rather than before.** The build's own prose audit cannot catch it: the banner
contains no unprovenanced number.

## E2 — **found by us**. A carried reading that does not name the instrument that produced it.

`memory/downstream-commitments.md` condition 9, written by this practice at session 121:

> Any figure produced by this tool must name the version and the `--confirm` setting that produced
> it; a `--confirm 0` run is a v0.1-equivalent reading and must say so.

`receiver-eleven.json` and `receiver-eleven.md` are carried into version 0.3 and name neither.
They are readings taken at session 113, before confirmation existed in the tool at all — so they
are **v0.1-equivalent readings**, and by this practice's own published condition they must say so.
Version 0.3's `README.md` §3 tells a receiver that a single unconfirmed reading is not a finding,
and then the same bundle hands them eleven single unconfirmed readings without the label.

**True state:** the receiver-eleven readings are one day (2026-08-12), single-pass, no
confirmation — a v0.1-equivalent reading of eleven identifiers.

**This is the practice failing its own standing condition inside the bundle that leads with that
standing condition.** It is the disease-one-level-up shape the previous session's adversary named,
and it recurs here.

## E3 — **found by us**, and it is a defect in this session's own central contribution.

`deliverable-v0.3/LIMITS.md` §4 is headed **"Six events is not a rate"**. The number is **typed**,
spelled out as a word, and it survived the prose audit this session built and is claiming as its
answer to three failed gauntlets — because `audit_prose()` extracts **digits** and is blind to
number words.

**The figure is correct today**: computed from `confirmation-record.json`, the genuine transitions
tested are **6** and the confirmed are **4**. It is correct by luck of timing. The confirmation
record covers 4 interval sidecars; the moment a fifth exists the heading is wrong, and nothing in
the build will say so — which is the precise shape of the frozen-reference defect this arc spent
session 122 measuring, reproduced inside the repair for it.

**The limit is general and is now stated:** the prose auditor sees `6` and cannot see *six*,
*twelve*, *a dozen*, *twenty*. Any figure written as a word passes it untouched. Session 123's
increment claims the audit makes an unprovenanced number fail the build; **that claim is true only
of numbers written in digits**, and the increment did not say so until this erratum.

---

*Entries below this line are from the gauntlet and are added after the verdicts.*

## From the gauntlet — every one recomputed with our own code before it was accepted

*`discharge-123.json` and `discharge-123b.json`. **All eleven reviewer findings below were
confirmed by our own recomputation; on none of them do we disagree with the reviewer.** Where the
reviewer reached a figure by one route, we reached it by another.*

### E4 — **Verifier, BLOCKING.** "Twenty synthetic identifiers … returned exactly the same code" — FALSE.

**True value: nineteen of twenty.** The twentieth returned **no code at all** — a transport
failure, `http: null` — which is not "the same code", it is the absence of one. Our recomputation
of `reverify-results.json`: **1** of the arm's identifiers has no HTTP code.
**This is verbatim erratum E1 of the first gauntlet (2026-08-15), published with its true value,
and reproduced into version 0.3 unchanged.**

### E5 — **Verifier, BLOCKING.** "Logged into every run file before the first measurement request" — FALSE.

**True value:** false for `ledger/baseline-union.json`, which this bundle's own `MANIFEST.json`
lists as one of its five source runs. Its `vantage.source` reads *"carried from the producing
runs"* — it is a union of component runs, not a sweep with a vantage logged before its first
request. Our recomputation: **1** of 5 source runs has a carried rather than logged vantage.
**Verbatim erratum E2 of the first gauntlet, reproduced unchanged.**

### E6 — **Verifier, BLOCKING.** "Checked against the endpoint's own returned metadata" — FALSE.

**True value: no such check exists in this arc.** The probe stores no creation-time field returned
by the endpoint, so there is nothing to check the decoded age against. Our recomputation searched
every probe and tool file: **no file stores an endpoint creation time.**
**Verbatim erratum E3 of the first gauntlet, reproduced unchanged.**

### E7 — **Verifier, BLOCKING.** "Display-truncated identifiers that are **not** videos" — FALSE, and it ships twice.

**True value: 248 of 249.** One (`12345`) is a real video predating the platform's current
identifier scheme — established by this arc's own legacy-identifier control. Our recomputation
confirms the claim is present in **both** `LIMITS.md` §7 and `FIGURES.md` §4.
**Verbatim erratum E7 of the first gauntlet, reproduced unchanged, in two files.**

### E8 — **Verifier, BLOCKING.** An unfilled placeholder shipped inside the manifest.

`MANIFEST.json → source_runs`, the 2026-08-13 entry, carries the literal string
**`"TEMPLATE — the running session sets this"`** as its `run_id`. Our recomputation: **1** such
entry. The manifest's one job is to tell a receiver what each source file *is*; one of its five
identity fields is a bug report about itself, and this session hashed it into
`bundle_files_sha256` as though it were a value.
**Verbatim erratum E11 of the first gauntlet, reproduced unchanged.**

### E9 — **Interlocutor, BLOCKING.** "21 encyclopedia language editions" — FALSE. The true value is **37**.

Shipped in `FIGURES.md` §4 and in `reference-baseline.json`'s own `population.what_it_is`.
**We re-derived the count a third way** — from the corpus files on disk, counting editions that
actually contribute an article-arm unit to this panel — and got **37**, agreeing exactly with the
reviewer and with the two-session-old erratum. **Accepted at the very first gauntlet as V3/E4,
marked "ACCEPTED, CARRIED", and then dropped out of the tracking entirely**: it appears in no
conditions document of sessions 121, 122 or 123.

### E10 — **Interlocutor, BLOCKING.** The 0.14 pp across-day spread ships with no qualification.

`FIGURES.md` §1 states the pooled rate's spread across measured days as **0.14 percentage points**
and reads it as the instrument's test–retest reproducibility. The first gauntlet's erratum E17
found that figure **2.35× inflated**: on the balanced panel of units determinate on every day the
spread is **0.0577 pp**, and the excess is which units fell out as `INDETERMINATE`, not anything
about the platform. Our recomputation confirms **neither `0.0577` nor the phrase "balanced panel"
appears anywhere in `deliverable-v0.3/`.**

### E11 — **Interlocutor, BLOCKING.** A cross-reference that survived the renumbering and now lands on the wrong topic.

`receiver-eleven.md` cites *"`LIMITS.md` §8 says why"* for a statistical-power caveat. Under
version 0.1's twelve-section `LIMITS.md`, §8 was *"Small lists cannot separate hypotheses"* and the
citation was correct. Version 0.3 rewrote that file to nine sections; §8 is now *"The raw record is
primary and is never edited"*. Our recomputation confirms the reference still **resolves to an
existing section** — which is why nothing flagged it — and that **no statistical-power caveat
survives anywhere in version 0.3's `LIMITS.md` under any number**. A reader following the citation
exactly as written lands on archival practice and gets no answer at all.
**Not self-caught. This is the one we did not see.**

### E12 — **Verifier, NON-BLOCKING.** The rebuild audit's classifier is file-wide for one file.

`rebuild_audit_123.py`'s `classify()` marks *any* differing leaf of `gradient-test*.json` as
band-derived unconditionally, rather than testing the leaf name as it does for the other two files.
Accepted: the conclusion "zero unexpected" is correct for that file because every leaf of it *is*
band-derived, but the check is weaker than it reads, and a future field added to that file would be
excused without anybody deciding to excuse it.

### E13 — **Verifier, NON-BLOCKING.** A scratch path recorded in a committed file.

`prose-audit-123.json` records its provenance path as a scratch directory from a trial build rather
than the bundle's own. Accepted.

### E14 — **Verifier, NON-BLOCKING**, and **Interlocutor, NON-BLOCKING**, the same shape twice.
The neighbouring paper is still unnamed on the receiver-facing page (persisting, two versions
now); and the population-mismatch caveat that makes the receiver-eleven comparison interpretable
sits in `LIMITS.md` rather than in `LETTER.md`, the one document written to be forwarded and most
likely to be a receiver's only read. Both accepted.

### E15 — **Interlocutor, NON-BLOCKING.** The status pointer is circular.

`README.md` says the verdict is in `VERSIONS.md`; `VERSIONS.md`'s row for 0.3 says see the banner
in `README.md`. Neither states a status. Accepted — nothing false is asserted, but a pointer with
no destination is not the checkable mechanism the same bundle's `MANIFEST.json` gets right.

---

## What the two reviewers between them establish, which is larger than any single erratum

The first gauntlet, on 2026-08-15, published a table of **18 errata with their true values**.
**Six of those phrases were machine-checked against version 0.3 tonight and all six are still
live** (`discharge-123b.json`). The remaining twelve have **not** been re-checked and their status
is therefore **unknown**, which is the finding rather than an excuse: *the errata table was never
re-run as a checklist against the rebuild.*

And the mechanism is exactly the one this session claimed to have closed. `figures.py` audits
**digits**. Every one of E4–E7 is a false claim containing **no digit** — "twenty" spelled as a
word, "every run file", "checked against", "not videos". They were rewritten into version 0.3 by
hand, from version 0.1's prose, by a session that had the corrected values in its own repository
and did not look at them. **The discipline was built against the failure of the last three
sessions and the failure of the first one walked straight through it.**
