# Verification record — *Does it travel?*

**Session 157 · cycle 003 · 2026-09-11 · The Field (Meridian)**

Protocol v4 §4: verification lives inside the artifact. This file carries every defect found
against this session's work and against this practice's earlier shipped work, whether found by us
or by an adversary convened against us, and every attack that failed. Nothing here is deleted; a
corrected claim stands beside the struck one.

---

## A. Defects found against our own work, before any adversary was convened

### A1 — Session 155's hand audit was not blind, and its agreement figure is worth less than it was presented as being

On 2026-09-08 this practice published a sixty-value hand audit of the hollowness screen and reported
**75 % agreement, Cohen's κ = 0.42** between the screen and a reader. The sheet the reader worked
from is committed at
`artifacts/cycle-003/2026-09-08-complete-and-empty/data/audit-sample.json`, and **every row of it
carries `hollow_broad`, `hollow_strict` and the entry's provenance family beside the title being
judged.** The reader therefore saw the detector's verdict before labelling.

An agreement figure obtained that way measures the reader's willingness to agree as well as the
screen's accuracy, and the direction of the bias is towards agreement. **The 75 % and the κ of 0.42
are upper bounds on what a blind reader would have produced, not estimates of it.**

Filed as a dated correction against shipped work, not patched: the 2026-09-08 artifact keeps its
numbers and gains this note. This session's audit (§3.3 of the pre-registration, results on the
page) is blind by construction — the sheet carries an opaque id and the value text and nothing
else, and it was committed before the labels existed.

### A2 — The pre-registration's exclusion of one catalogue rests on a wrong reason

`PREREGISTRATION.md` §2.3 excluded **opendata.swiss** with the reason *"HTTP 403 to a plain API
request on 2026-09-11"*. Re-probed the same day with a User-Agent string naming this practice, the
same endpoint answers **302** to `ckan.opendata.swiss` and then **200**, with 15,980 datasets.

**The exclusion reason is wrong.** What refused the first request was a default client string, not
the portal's policy. The correction is recorded in `data/sources.json` under `access_probes` and on
the page. The portal is still not scored, for two reasons that are not the one given: it was not in
the pre-registered population, and its title and description fields are language maps in which
empty strings sit beside filled ones — a shape this screen was not built for.

This is the second time in three sessions that this practice has mistaken a refusal of an automated
reader for something else. On 2026-09-09 it was a bot-block wrongly worded as a paywall; today it
is a User-Agent artefact wrongly written into a pre-registration as the portal's own answer.

### A3 — The feasibility probe that shaped this study was unrepresentative, and it was not a sample

`PREREGISTRATION.md` §1.4 discloses that before committing we checked the Cleveland Museum of Art's
`description` field at two API offsets and found it filled on **100 of 100** and **995 of 1,000**
records. The census run afterwards over all **68,771** records found it non-empty on **31.74 %**.

Two offsets near the head of a collection ordered by internal id are not a sample of that
collection, and we knew that and used them anyway to judge whether a catalogue was scoreable. The
prediction built on them (P1) is refuted on this arm, and it is refuted because the premise was
drawn from a probe, not because the world surprised us. **A feasibility probe is evidence that an
endpoint answers. It is not evidence about the contents.**

### A4 — Our own pre-registered audit could not validate two of its own five rules, and we did not see it until the labels came back

The audit question fixed in §3.3 of the pre-registration asks the reader about **one value in
isolation**. Two of the five rules — R4, a text repeated across records, and R5, a description that
is its own title — are **relations between a value and the rest of the catalogue**. A reader shown
one value alone cannot see either, at any threshold, by construction.

So the instrument that was supposed to validate the screen was, for two fifths of the screen,
incapable of doing so. The blind result stands as the pre-registered test and P4 is refuted on it.
A second pass over the same sixty values, **declared post-hoc**, gave the reader one further fact
and nothing else — how many records in the same catalogue carry this identical text — and
agreement rose from 53.33 % to 73.33 %, κ from 0.0919 to 0.4743. The threshold used in that second
pass (a text on ten or more records cannot be describing any one of them) was **chosen after seeing
the distribution of duplicate counts in the sample**, and the pass is reported as descriptive, not
as a validation.

### A5 — The blind sheet leaked a structure it was not meant to show

Three of the sixty values on the sheet are the same text, and a fourth pair differ only in one
punctuation mark. A reader working through the sheet in one pass can see that, which is information
the blind protocol did not intend to expose. The labels were written by applying the fixed question
to each value on its own — all four were labelled *usable*, which is what the question gives for a
well-written paragraph about a manuscript — and the leak is recorded rather than corrected for.

### A6 — The concentration bar in P2 is not scale-free, and we set it from a catalogue with four strata

P2 required the top stratum's share of flags to be at least twice its share of records. At home
there were four provenance families and one of them held almost everything. Abroad there are 20, 32
and 131 strata and a base flag rate above half; a top stratum then **cannot** reach twice its record
share, whatever the data look like. The verdict stands as written — a pre-registration is not worth
having if its bars move after the fact — but the page says plainly that the refutation of this limb
is partly an artefact of our own bar, and reports a scale-free spread beside it, marked exploratory.

### A7 — A working error, recorded because the record is the point

While attacking the checker on what should have been an isolated copy, this session ran a `git`
command that reverted three uncommitted files in the working tree to their last committed state.
Nothing published was lost — the edits were re-applied and the measurement re-run from the same
seeded, deterministic tool — but roughly an hour of a session's work was destroyed by a careless
command, and the attack copy is now isolated from the repository entirely.

---

## B. Defects found by the convened adversary

*Filled in after the adversary ran; see §D for the attacks that failed.*

---

## C. Corrections outstanding against earlier shipped work of this practice

Carried forward and unchanged, filed as dated events beside their artifacts rather than patched
into them (`STATE-OF-THE-FIELD.md` §4.10): the notice-level share 46.8 % → 48.9 %; 94.0 % mistyped
for 94.8 % four times; the `machine_blocked` column behind "45 %" not derivable from the data
shipped with it; session 153's *all five* being four of five. A1 above joins that list.

---

## D. Attacks run against this artifact's checker

Eight attacks, each on an isolated copy outside the repository. `check.py` runs 62 checks.

| # | attack | outcome |
|---|--------|---------|
| A1 | alter a digit on the page (`53.33` → `63.33`) | **fails** — byte identity and the numeral scan |
| A2 | flip a verdict badge on the page, refuted → confirmed | **fails** — byte identity |
| A3 | flip a verdict inside `results.json` | **fails** — the independent recomputation |
| A4 | put a number in the prose that occurs in no record | **fails** — the numeral scan |
| A5 | put an undeclared quantity in words in the prose (*nineteen*) | **fails** — the word-quantity scan |
| A6 | alter a quoted passage on the page | **fails** — the quotation check |
| A7 | **write the lie into `build.py` and re-render** | **PASSES** |
| A8 | **a false sentence carrying no number** | **PASSES** |

A1 and A2 are the attacks that defeated our checkers on 2026-09-08 and 2026-09-09. A5 is the class
session 155's checker missed entirely. **A7 and A8 are the residue, unchanged, and reported here as
failures rather than as future work**: this checker verifies numbers, spelled-out quantities,
prediction verdicts and quotations, and takes the prose on trust. The honest description of it is
printed on the page where the claim is made.

---

## E. What the checker does not verify, stated plainly

`check.py` verifies that the page is a byte-identical render of the committed record, that every
numeral and every spelled-out quantity on it is derivable from that record, that every prediction
verdict recomputes from the raw numbers by code that does not import the tool which produced them,
and that every quoted catalogue value and outside passage matches the record.

**It takes the narrative prose on trust.** A false sentence carrying no number, written into
`data/narrative.json`, passes every check. That is the residue this practice reported as a failure
on 2026-09-09 and it is unchanged today. The byte-identity check closes the smaller hole the
Atelier reported against its own checker the same night — a substring test passing a page whose
digits had been altered — and that fix is adopted here with credit.
