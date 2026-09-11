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

*Filled in after the checker is built and attacked.*

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
