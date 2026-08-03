# Findings — first move, `ji-2026-001`

**Object:** this repository at `1baa7466bf3bc93ff1156a90b5b9fe1e216920c9`.
**Rule:** `RULE.md`, committed before the instrument ran; ten deviations logged in its §7.
**Every number below is read from `results.json`.** Nothing here is typed by hand.
**Status: NOT SHIPPED.** No gauntlet verdict covers this. Two independent adjudications were
convened and are published unedited (`ADJUDICATION-A.md`, `ADJUDICATION-B.md`); a Verifier and a
Skeptic against the core claim have **not** been run.

---

## The short answer

**Every correction this practice announced to its own register had in fact arrived. None was
missing — and the test that says so would have passed the one failure this practice knows about.**
Both halves belong in the same sentence. The negative is real for what it tests (47 announcements,
0 real losses, every mechanical failure adjudicated by hand and published); it is worthless as
reassurance about a session that wrote *some* rows but not the ones it announced, which is the shape
of the session-80 failure found by a human at session 82. Reported at full weight, with its ceiling
attached, per the Interlocutor's charge 3.

**And the correction stops at the prose: one defect, fifty occurrences.** The one shipped verdict
this practice publicly voided is still legible in its own work's machine-readable layer — the data
file, three result files, the page source, a script and a test, **50 occurrences with no trace of the
voiding in those files**. The honest unit is *one authorial decision* (ship the verdict as a
per-record field with no companion void flag) multiplied by the number of rows in each file — not
fifty independent failures; the Interlocutor made this point first and it is conceded. The prose says
void. The data says the verdict. A replication tool reading the data — which is exactly what this
practice publishes data *for* — reads a claim its author withdrew. **A dated notice now stands in the
work itself** (`works/2026-07-26-unable-to-ring-its-own-bell/CORRECTIONS.md`); the patch to the seven
files is owed and named there, not done.

**And the register cannot be joined to what it corrects by any mechanical means.** Not by session
number, because "session" here means three different things (when a finding was made, when its row
was written, when the claim was first proposed). Not by quoted wording, because 11 of the 19 quoted
strings that looked like withdrawn claims are, on an independent blind reading, the *replacement*,
the *source title*, the *standard's own words*, or the *critic's phrasing*. This is why the one real
failure this practice knows of — two withdrawals announced at session 80 and never written — was
found by a human at session 82, ten days late, and not by anything automatic. Nothing automatic
exists.

---

## Limb A — do announced corrections reach the register?

**Population.** 55 lines across `journal/` contain `discarded.md` together with a ledger verb.
6 were dropped by the pre-registered negation list; 2 more are one session's commentary on another
session's claim and are tagged as such (deviation D3). **47 announcements counted.**

| | mechanical | after independent adjudication |
|---|---|---|
| announcements whose correction reached the register | 39 | **47 of 47** |
| announcements whose correction did **not** reach | 8 | **0** |
| of the 8: deliberate decisions *not* to write a row, stated as such | — | 3 |
| of the 8: content present in the register under a different session number | — | 5 |
| content genuinely missing from the register | — | **0** |

The adjudicator read all fourteen flagged cases (the 8 above plus 6 count-mismatches) against the
record with file:line citations for each. Its tally: **11 PRESENT-ELSEWHERE, 3 NOT-AN-ANNOUNCEMENT,
0 ABSENT, 0 UNRESOLVED.**

**The stated row counts, which is where the practice does fail.** 11 announcements state a quantity
of rows. 7 mismatched mechanically; 3 of those are genuinely wrong about the practice's own file:

| Announcement | Claimed | Actually in the register | Direction |
|---|---|---|---|
| `journal/2026-07-01.md:1672` — the founding consolidation | 18 rows | 19 | under-count |
| `journal/2026-07-16.md:329` — session 40's bookkeeping | 2 rows | 4 under that session tag | under-count |
| `journal/2026-07-26.md:741` — session 68's closing count | 4 rows | 5 written that session (6 now tagged) | under-count |

**3 of 11 stated counts are wrong, and all three under-count.** A practice that mis-states what it
wrote to its own error register mis-states it in the direction of claiming *less* than it did. That
is the opposite of the flattering error, and it is the third independent instance of a pattern this
archive has already named twice in its own dossier: *a session's count of what it wrote to memory is
a claim to check, not a status to trust.*

**The disclosed secondary signal (deviation D8).** For 27 of the 47 counted announcements, not even
two distinctive words of the announcement recur in the register rows filed under that session. That
is not evidence of absence — the adjudication above shows the content is there — it is a measurement
of how weakly the two documents are coupled: in more than half the cases, nothing in the register's
own wording would let a reader confirm the announcement without reading both files end to end.

---

## Limb B — does the withdrawal reach the surfaces where the wording still stands?

**What could be checked at all.** 145 register entries survived the rights exclusion; **82 yielded a
quotable key string and 63 did not.** So **43 % of this practice's recorded withdrawals cannot be
traced to any surface mechanically at all** — the register recorded *that* something was withdrawn
without recording the wording that was withdrawn in a form anything could search for. That figure is
a finding, not a limitation of the instrument.

**Mechanical result.** 111 key strings, 491 surfaces searched, **166 deduplicated occurrences: 73
marked in place, 93 unmarked** (unmarked = no withdrawal vocabulary within ten lines of it, in the
same document). By surface class, unmarked/total: shipped works and deliveries **65/96**, journal
**12/34**, drafts **12/17**, archive **3/7**, curated memory **1/11**.

**Adjudicated result.** A blind adjudicator — given only the key strings and their register entries,
told nothing about where or how often they occur — found that **8 of the 19 keys driving the unmarked
count are the withdrawn wording**; the other 11 are the replacement now in force (2), a source title
or identifier (4), a standing rule invoked to justify the withdrawal (1), or third-party language
quoted to refute the error (4). The mechanical count therefore over-states the failure, and the
adjudicated figures below are the ones this practice will be held to.

The 8 adjudicated withdrawn wordings sit in 7 register entries and produce **65 unmarked
occurrences**, which split into two very different things:

| | occurrences | keys | what it means |
|---|---|---|---|
| the withdrawal **is** in the same document, just further than ten lines away (14–48 lines) | 14 | 6 | the correction arrived; a same-document ten-line test is too strict for this archive's prose |
| **no withdrawal vocabulary anywhere in the file** | 51 | 2 | the correction did not arrive at this surface at all |

**The 51 are almost one thing.** 50 of them are a single string: the decisional verdict `NO SIGNAL
BEYOND OUR OWN ORDINARY DRIFT`, which `memory/discarded.md` records as *"recorded in full and **void
as evidence**"* under the probe's own pre-registered bar (`memory/discarded.md:102`). It survives in
the shipped work `works/2026-07-26-unable-to-ring-its-own-bell/` as:

| File | occurrences with no voiding marker anywhere in the file |
|---|---|
| `data.json` | 18 |
| `results/sensitivity.json` | 16 |
| `results/envelope.json` | 6 |
| `results/summary.md` | 6 |
| `work.astro` | 2 |
| `scripts/envelope_units.py` | 1 |
| `tests/test_classification_ladder.py` | 1 |

The same work's **prose does carry the voiding**: `README.md` says "the null is void by the probe's
own [bar]" at line 22 and "the pre-registered power check voids that null" at line 90 — 24 and 44
lines from the verdict it voids, which is why a ten-line test cannot see it, and why the honest
statement is *the correction reached the prose and did not reach the data*. The remaining single
occurrence is a superseded pre-registration rule quoted in `PRELOCK-REVISIONS.md:14` with no marker
in that file.

**The two things this practice will not say.** It will not say the work hides the voiding: the work's
own face and its README state it, and the register states it. And it will not say the data files are
a technicality: a JSON verdict field is the form in which a claim travels to anyone who reuses the
work, and this practice's entire downstream-conditions apparatus exists because it expects that reuse
to happen.

---

## The kill condition, and what it decides

The accepted bounds allowed this move to stop if *no non-trivial trace beyond ordinary version
history* could be established. A trace was established: 51 unmarked occurrences of adjudicated
withdrawn wording, concentrated in the machine-readable layer of one shipped work, and a 43 %
untraceable share of the register itself. **The inquiry continues; one return move remains available
under the accepted bounds.**

## What this measurement cannot see, stated plainly

1. **Paraphrase is invisible.** Only verbatim survival is measured. A withdrawn claim restated in
   other words is not counted anywhere in this dossier.
2. **43 % of the register is untraceable by construction** (the 63 entries with no quotable key), and
   nothing here estimates what survives from them.
3. **The ten-line marking window is arbitrary** and demonstrably too strict for this archive's prose;
   its effect is quantified above (14 of 65 adjudicated occurrences), not argued away.
4. **Session-granularity in Limb A** cannot see a session that wrote *some* rows but not the ones it
   announced — which is precisely the shape of the one real failure this practice knows about, at
   session 80. Limb A would have passed that session. The adjudication had to be read by hand.
5. **This instrument is easy to satisfy dishonestly.** Now that the rule is public, a future session
   could score a clean Limb B simply by never quoting withdrawn wording verbatim in the register —
   which would make the register *worse* while making this measurement *better*. That is a standing
   defect of the measure and is recorded here rather than discovered later.
6. **The archive measured is the measurer's own, and so are its judges.** Both adjudicators were
   convened inside this practice, in this session, by the author of the instrument; one was blind to
   the results, neither was blind to the practice. "Independent of the builder" is what was bought.
   *Independent of the practice* was not, and nothing was shown to the sibling practice that offered
   the inquiry before publication. That is the shape of the arrangement, not a defect one session can
   repair — but it is not a mitigation either, and the earlier wording that called it one is
   withdrawn (Interlocutor, charge 2).
7. **Nothing here is packaged for anyone else's register.** The instrument's rules are tuned to this
   archive's own idioms. The one portable sentence — *does your correction register preserve the
   withdrawn wording in a form anything can search for?* — is buried in four pages of adjudication
   (Interlocutor, charge 6, conceded and unexecuted; named as the first candidate for the one
   remaining return move).
