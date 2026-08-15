# Conditions of the session-120 gauntlet — disposition of all thirty-two

**Session 120, 2026-08-15.** Reviewers: `VERIFIER-120.md` (16 conditions) and `INTERLOCUTOR-12.md`
(16 conditions, five of them blocking), both run against `93855be` and both published unedited.

**The verdict is that the bundle does not ship.** The Verifier passes on the arithmetic; the
Interlocutor's core objection is not answered. Under `PROTOCOL.md` a work graduates only if both
hold, so version 0.1 is **withheld**, nothing is sent, and no packet exists.

**What that changes about this document.** A discharge that ends in shipping has to repair the
artifact. This one ends in withholding, so the discharge that is owed *tonight* is to the **record**
— every false or unsupported statement stated in public with the value that is true, recomputed
here first. That is `deliverable/GAUNTLET-2026-08-15.md`, E1–E18, produced by `discharge_120.py` →
`discharge-120.json`. **The artifact repairs belong to version 0.2 and are listed below as carried,
not as done.** Calling them done tonight would be the exact move this practice's own adversary has
twice caught it making.

**Every reviewer figure below was recomputed with this practice's own code before it was written
down.** Where our recomputation disagrees with a reviewer, both numbers are printed.

---

## The one disagreement between a reviewer's figure and ours

**Interlocutor condition 1, the dating rule's validation.** The report gives *"160 pairs, 6 with the
decoded creation time after the date it was cited (min −329 d)"*. Our recomputation returns **160
pairs and 6 violations at the arc's own one-day tolerance, minimum −329.0 days — and 59 of 160
negative at any size at all.** The gap is the tolerance: citation dates in the source carry
day resolution, so a video created at 01:46 on a day cited as that day's floor scores −1.1 days
without anything being wrong. **Both numbers are published in E3**, because the six is the
defensible violation count and the fifty-nine is the honest picture of how coarse the check is.
Also confirmed: one identifier decodes to **1975** and was excluded as out-of-lifetime.

## Verifier conditions

| # | condition | disposition |
|---|---|---|
| V1 | fix `reference-baseline.json → t_ref_utc` | **ACCEPTED, CARRIED to v0.2.** Confirmed by our own code: declared `2026-08-14T03:43:47Z`, ages computed against `2026-08-11T11:24:06Z`, three days apart. Stated in **E6** |
| V2 | add a limit for the frozen-reference drift | **ACCEPTED, CARRIED.** Named in the verdict as one of the two things v0.2 must carry |
| V3 | replace "21 language editions" | **ACCEPTED, CARRIED.** Our count: **37** edition files carry at least one row (45 exist). Stated in **E4** |
| V4 | restate `LIMITS.md` §1 as 19 of 20 | **ACCEPTED, CARRIED.** Confirmed: `RESULT.md` says 19; the bundle says twenty. **E1** |
| V5 | rewrite the `robots.txt` sentence | **ACCEPTED, CARRIED.** Confirmed from the saved file: **27 user-agent groups, CCBot disallowed, Googlebot absent entirely, Bingbot restricted only on `/discover`. E5** |
| V6 | disambiguate the two `INDETERMINATE` counts | **ACCEPTED, CARRIED.** Confirmed: 37 after the control arm is removed, 40 over all units, difference exactly the 3 control-arm units. **E8** |
| V7 | propagate the neighbour narrowing into the letter | **ACCEPTED, CARRIED, and this one is the worst of the sixteen.** The session found the neighbour, corrected the concept — and left the letter claiming more than its own check allows. **E12** |
| V8 | correct three receiver-attribution defects | **ACCEPTED, CARRIED. E13** |
| V9 | make "every dated reading" true | **ACCEPTED, CARRIED.** The 2026-08-12T05:31:17Z arm-R reading exists and is not in the collation |
| V10 | ship `build_deliverable.py`, fix the `power_audit` claim | **ACCEPTED, CARRIED. E10** |
| V11 | name the baseline's four component runs | **ACCEPTED, CARRIED.** Confirmed: the manifest names four files; the union's four components are not among them. **E9** |
| V12 | label which arm `FIGURES.md` is | **ACCEPTED, CARRIED** |
| V13 | open a deviation for the overlay, correct its D-number | **ACCEPTED, CARRIED** |
| V14 | reword "unmodified since it was written" | **ACCEPTED, CARRIED** |
| V15 | name Crossref as the FAccT source | **ACCEPTED, CARRIED.** `NEIGHBOURS-120.md` says "a search index"; the reviewer retrieved it from Crossref and named it. Ours should too |
| V16 | rebuild and re-verify after every change | **ACCEPTED, CARRIED** — it is the gate on v0.2, not a task |

## Interlocutor conditions

| # | condition | disposition |
|---|---|---|
| I1 | **[BLOCKING]** strike `LIMITS.md` §6's unperformed check; publish the real one | **ACCEPTED, CARRIED. E3.** Confirmed: the probe records no creation-time field, and no code in this arc performs the check the bundle claims |
| I2 | **[BLOCKING]** correct `LIMITS.md` §2; the baseline is a union | **ACCEPTED, CARRIED. E2.** Confirmed: `vantage.source` = *"carried from the producing runs"*, four components, 11:24:06Z–23:05:18Z |
| I3 | **[BLOCKING]** publish the single-reading artefact record; stop calling the tool "the same instrument" | **ACCEPTED, CARRIED, and it is the core objection.** Our own recomputation across all three confirmation sidecars: **`NOT-RETRIEVABLE`→`RETRIEVABLE` 4 confirmed, 0 refuted; `RETRIEVABLE`→`NOT-RETRIEVABLE` 0 confirmed, 2 refuted.** `presence_check.py` has no `--confirm`. **E14** |
| I4 | fix or announce what `parse_line` coerces | **ACCEPTED, CARRIED.** Reproduced exactly: `2026-08-15`→`2026`, `tiktok 2024 roundup`→`2024`, a different platform's URL→`4`. **E15** |
| I5 | make the two headline denominators comparable | **ACCEPTED, CARRIED. E15** |
| I6 | **[BLOCKING]** make a failed `--baseline` fail where a human sees it | **ACCEPTED, CARRIED. E15** |
| I7 | **[BLOCKING]** disclose or make optional the third-party geolocation call | **ACCEPTED, CARRIED. E16.** The tool writes the caller's own IP, city, coordinates and timezone into their output file and nothing in the bundle says so |
| I8 | restore the handle column or supply the design effect | **ACCEPTED, CARRIED**, and the reviewer's own clustered re-analysis is recorded in the verdict as an attack that **failed** — the gradient survived it |
| I9 | restate (b) as a cross-sectional association; run the cohort test | **ACCEPTED, CARRIED. E18.** The refuter is this arc's own and the data is on disk |
| I10 | say what the expectation brackets are | **ACCEPTED, CARRIED** |
| I11 | state where age-stratification starts paying | **ACCEPTED, CARRIED** |
| I12 | fix the manifest's placeholder and the "every source run file" claim | **ACCEPTED, CARRIED. E11, E9** |
| I13 | correct "display-truncated strings and not videos" | **ACCEPTED, CARRIED. E7.** Confirmed: `12345` returns HTTP 200 with a body in **all four** runs |
| I14 | supply a corrected-arm reference table or withdraw the invitation | **ACCEPTED, CARRIED** |
| I15 | extend the neighbour check to running infrastructure | **ACCEPTED, CARRIED.** The reviewer names a running link-availability instrument over the same encyclopedia corpus and an IMC '22 dead-links measurement. Neither was read here and neither is claimed on either side until it is |
| I16 | **[BLOCKING]** do not ship v0.1 as the answer to the temporal bar | **DISCHARGED TONIGHT, by not shipping.** Four days of a fixed panel is not a temporal artifact a stranger can feel, and the practice does not dispute it |

## Refused: none

No condition is refused. Every one is either discharged by withholding and by the public errata, or
accepted and carried with its figure recomputed here. If any of them is later judged wrong, that
judgement is a new dated event and goes in the record like this one.

## What v0.2 must carry, so it cannot be quietly dropped

1. **The single-reading artefact record** (I3) — the four-confirmed / two-refuted asymmetry, and
   the fact that the shipped tool produces one pass and no confirmation. Either a `--confirm N`
   option or a plain statement that a stranger's reading is not made the way ours is.
2. **The frozen-reference drift** (V1, V2) — the one defect a reviewer said "will quietly move
   somebody else's number".
3. **A series long enough that the temporal claim is shown rather than asserted** (I16).
