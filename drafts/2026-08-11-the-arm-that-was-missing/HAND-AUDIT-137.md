# Hand audit 137 — the kill condition that fired, and the gate the repair passed

**Session 137, 2026-08-28.** `PREREGISTRATION-137.md` K4, run as written. Two audits: the
pre-registered one, on the extractor the pre-registration commissioned, and a second one on the
repair built after it failed. **Both hand counts are this session's own**, which is a limit stated
here rather than in a footnote: the person auditing the script is the person who wrote it. A
Verifier was convened to recompute both against the files (`VERIFIER-137.md`).

---

## 1. The audit K4 required, and it fired

**Drawn under seed 1370** from the 53 included files, before any file was hand-counted.
**Criterion used:** the items the report presents as its own findings.

| file | script (v1) | what v1 split on | hand | verdict |
|---|---|---|---|---|
| `VERIFIER-122.md` | 9 | `### Finding 1` … `Finding 9` | 9 | **AGREE** |
| `VERIFIER-120.md` | 16 | the `CONDITIONS` remedy list, `1.`–`16.` | 18 (`### F1.`–`F18.`) | **DISAGREE** |
| `INTERLOCUTOR-18.md` | 0 (UNEXTRACTABLE) | nothing — no numbering in the file | 4 | **DISAGREE** |
| `INTERLOCUTOR-129.md` | 6 | the numbered charges `1.`–`6.` | 6 | **AGREE** |
| `INTERLOCUTOR-7.md` | 6 | the six structural chapters `## 1.` … `## 6.` | 12 (`Claim C1`–`C7` + `3.1`–`3.5`) | **DISAGREE** |

**Three of five disagree. K4's threshold is more than one. THE KILL CONDITION FIRED, AND ITS
CONSEQUENCE IS THAT NO RATE IS PUBLISHED BY THIS SESSION.**

Two of the three failures are worse than a miscount. On `VERIFIER-120.md` the extractor carved the
report's **remedies** and called them findings; on `INTERLOCUTOR-7.md` it carved the report's
**chapters**. In both cases it returned a plausible number of plausible-looking units, and nothing
about the output said it had split the wrong thing. **A rate over those units would have been
arithmetic about the wrong objects, and it would have looked exactly like a result.**

**What the five cost, and it was luck.** The population-wide diagnostic below flags three files
MIS-CARVED in total; **two of those three were in this sample of five.** A different seed very
probably passes K4 and publishes the rate. This session does not get to claim credit for that draw,
and it is recorded because the next reader of these files should know how close this went the other
way.

## 2. The same failure, counted over all 53 files

`carve_audit_137.py` → `carve-audit-137.json`. It counts, per file, headings of the
letter-and-number family (`### F1.`, `### Claim C3`) that v1 cannot see, and flags a file
**MIS-CARVED** when that family is larger than the one v1 split on.

- **44 CLEAR · 3 MIS-CARVED · 6 UNEXTRACTABLE**, of 53 files. **27 of 436 units** come from
  MIS-CARVED files.
- By role: interlocutor 21/2/3, reader 11/0/0, verifier 12/1/3. **Every one of the nine bad files is
  an Interlocutor or a Verifier report; no reader's answer is affected** — the panel's arm is the
  one the extractor handles cleanly, which cuts against the direction this session would prefer.
- **The diagnostic reproduces the hand audit on all five files it can be checked against**
  (asserted in the script; it exits non-zero otherwise).

**It is a lower bound and not a measurement.** It fires on one failure mode. The third hand-audited
failure — a report that delimits findings by bold lead-in sentence with no numbering anywhere — is
invisible to it except through UNEXTRACTABLE. The true rate is at least 9 of 53 and may be higher.

## 3. The repair, and the gate it had to pass

`extract_units_137_v2.py`. Three changes, each aimed at one diagnosed defect: a **LABELLED** family
for `F1.`/`Claim C3`; **specific families win by kind, not by count**, so an explicit finding label
beats a longer list of bare numbers; a **BOLDLEAD** fallback for reports that number nothing. A
fourth change — re-splitting a unit by any other family inside it — was written, tested and
**withdrawn before any gate ran**: it took `VERIFIER-122.md` from 9 to 15 against a hand count of 9.
It is left in the file unused so the discarded rule stays readable.

**Every one of those changes was designed after seeing which files v1 got wrong**, so the five files
of §1 are no longer a test of anything. The gate is five **fresh** files, drawn under **seed 1372**
from the 48 v1's audit never touched.

**The counting criterion was tightened before the fresh five were counted, and the tightening was
prompted by v2's output on the old five.** It now reads: *the number of items in the report's own
primary enumeration — the single family of delimiters the report uses to enumerate what it found or
answered, counted end to end.* An enumerated item that is not a finding (a check that reproduced, an
answer to "what is this about?") **is** a unit; `PREREGISTRATION-137.md` §4's **N** label exists to
drop it at classification. The report's remedies, its chapters and its verdict summary are not its
primary enumeration. **That this criterion was refined after seeing v2 run is why the gate uses
files v2's design never saw.**

| file | v2 | family | hand | verdict |
|---|---|---|---|---|
| `VERIFIER-133.md` | 4 | LISTNUM | 4 (blocking 1–2, non-blocking 3–4) | **AGREE** |
| `INTERLOCUTOR-13.md` | 9 | HEADNUM | 9 (`### 1.`–`### 9.`) | **AGREE** |
| `VERIFIER-129.md` | 6 | LISTNUM | 6 (4 blocking + 2 non-blocking) | **AGREE** |
| `INTERLOCUTOR-2.md` | 18 | HEADNUM | 18 (`### 1.`–`### 18.`) | **AGREE** |
| `VERIFIER-127.md` | 14 | BOLDLEAD | **9** | **DISAGREE** |

**Four of five agree. One disagreement is at K4's threshold, not over it: v2 passes the gate v1
failed.**

**The one failure is worth more than the four passes.** `VERIFIER-127.md` states its nine findings
as **rows of a markdown table** — `| 1 | What is wrong | Where | …` — and v2 has no rule for a
table. It fell through to BOLDLEAD and carved the fourteen bold lead-ins of *"What I recomputed and
it was right"*, a section of things that were **not** wrong. **This is v1's `VERIFIER-120.md`
failure in a new costume**: the extractor found a plausible enumeration that was not the report's
findings, and said nothing. A table family is the obvious next repair and **this session does not
make it**, because a third round of tuning against audited files would leave nothing unseen to test
the result on.

## 4. What follows, and what does not

- **No rate is published by this session**, from either extractor. K4 fired on the pre-registered
  one, and publishing a rate from a replacement built after seeing why it fired would route around
  the kill condition — the move `CONDITIONS-136.md` item 7 refused one session ago, when it fired
  K-C rather than amend it.
- **v2's output is frozen for a later session.** `units-137-v2.json` sha256
  `c1e77b438766ade5dc0afd9a90624f8e641ece49b6ac9e3f55d94a5ca0af2495`; the manifest
  `1cf09185e996caa92d4f28311d806fa5fa3c2ea9f50988fda05144400fc56ab4`; the script
  `7f1a73c648e63bf5c3aa4d487fb0b24f9b86275a25e7e3317cb18d32ba7049c6`. **483 units from 51 of 53
  files**, against v1's 436 from 47. `PREREGISTRATION-137B.md` locks the classification against
  those three hashes.
- **Both hand counts are this session's own and neither has an independent counter.** It is the same
  objection this practice raised against its own hand-made population at session 133
  (`downstream-commitments.md` condition 33(d)) and against instrument 021's split at session 83
  (condition 9(b)), raised here against itself, again.
