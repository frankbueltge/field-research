# Amendments to the pre-registration — session 100, 2026-08-08

Each amendment states when it was made relative to the data. The commit order in git is the
check: this file is committed **before** `scored.json` exists, and `analyse.py` had been written
but **not run** — no P1, P2, P3 or P4 number had been computed or seen by anyone when A1–A3 were
written.

## A1 — a minimum-N floor for P1, stated before any P1 number exists

**Cause:** Interlocutor condition 3. The pre-registration lets P1 be satisfied "on at least one
authority" with no floor on how many scored pairs that authority contributes. With 2 URLs in the
IE arm, a HELD verdict could rest on one or two pairs.

**Amendment:** an authority's P1 result counts as **HELD** only if it contributes **≥ 10 scored
SUBSTANTIVE pairs that are scorable for V**. Below that it is reported as **INCONCLUSIVE (n
below floor)** with its count printed, never as a verdict. The count is printed beside the share
for every authority regardless.

*(The floor of 10 is chosen by the same reasoning as the sibling line's own floor of 15 in
`drafts/2026-08-06-as-of-today/RECORD.md`, lowered because this population is 11 URLs rather than
177 and a floor of 15 would make every authority inconclusive by construction. It is a judgement
made blind to the data, not a threshold fitted to it.)*

## A2 — EC and non-EC are reported separately, and the reason is this house's own finding

**Cause:** Interlocutor condition 1, and it is the strongest attack the gate received.

This house's own blind-reader adjudication (`drafts/2026-08-06-as-of-today/RECORD.md` §14) found
that of 60 usable visible-date hits, **every row a blind reader confirmed as referring to the page
itself was EC** — and the three-class labelling that produced those classes was itself **KILLED**
by that test. **8 of the 11 URLs in this increment (all NIST, GOV.UK and IE) come from authorities
where no extracted V has ever been confirmed to be a statement about the page it sits on.**

**Amendment:** P1 and P3 are reported **split, EC versus non-EC**, never as one headline number.
Any non-EC V result carries, at every place it is stated, the warning that **V's referent is
unconfirmed on that authority** and that a non-moving or moving V there may be tracking a date
belonging to some other document on the page. No non-EC V number may be quoted alone.

**And the kill condition the concept was missing** is added to `CONCEPT.md` §6 as **(d)**: if the
referent of V cannot be established outside EC, this investigation cannot make a per-authority
claim about V beyond EC at all, and the artifact must say so on its face rather than in a caveat.

## A3 — the SUBSTANTIVE class is hand-checked before it is trusted

**Cause:** Interlocutor condition 2. `norm_text()` runs on the whole page — navigation,
breadcrumbs, related-content rails and promoted items included — and the sibling record's defect
**D8** already found whole-document handling admitting navigation as corpus on 40/40 NIST links.

**Amendment:** before any SUBSTANTIVE-based number is stated, the session hand-inspects a sample
of pairs classified SUBSTANTIVE and reports what the difference actually consisted of. If the
sampled differences are dominated by chrome rather than document content, the SUBSTANTIVE class is
reported as **contaminated** and the P1 number is withdrawn rather than published with a caveat.
The hand-check and its verdict are written into `RESULT.md`.

## A4 — two conditions this session records as open rather than discharging

**Cause:** Interlocutor conditions 4 and 5. Recorded here so a later session cannot mistake them
for settled.

- **The secondary receiver is dropped, not caveated.** The direct route to the code host of the
  monitoring project named as a secondary receiver returned **HTTP 403** to this session; its
  current liveness is reported by a search pass and unconfirmed by us. An unconfirmed-live project
  is not a receiver. It is **removed from `CONCEPT.md` §2 as a named receiver** and kept only as a
  described *class* of user. The primary receiver stands.
- **`x-archive-orig-last-modified` is treated as an open technical question, not ground truth.**
  Whether the archive's capture pipeline can preserve a header derived from a conditional request,
  a cached intermediary, or an earlier fetch has **not** been tested by this session. Every H
  result in `RESULT.md` is stated as *what the archive preserved as the origin's claim*, never as
  *what the origin's disk said*. A test is owed at increment 2 and named in `RESULT.md`.
