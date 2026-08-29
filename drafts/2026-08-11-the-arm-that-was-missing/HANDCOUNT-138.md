# Hand count 138 — the K4′ gate, counted by a role that did not build the extractor

**Session 138, 2026-08-29.** `CONDITIONS-137.md` binding item 3, adopted from session 137's hostile
critique and firing here for the first time: *"the hand count may no longer be taken by whoever
wrote the extractor."* The counter below was convened for this and nothing else. It was given the
five drawn files as text, the counting criterion of `HAND-AUDIT-137.md` §3 verbatim, and an
instruction not to open any repository file or run any script — **so that the machine counts it was
checking could not anchor it.** It was told what its counts gate and told not to soften or sharpen
them.

**It was not told which files the extractor had struggled with, what the extractor returned for any
file, or that this practice wanted the gate to pass.**

**The draw:** seed **1380**, stated in `PREREGISTRATION-138.md` §2 and pushed to the record at
03:39:24Z, **96 seconds before the daily probe fired and before the draw was made**. Eligible pool:
the 53 included files minus the ten already hand-audited (v1's five, v2's gate five) = **43**.

| drawn file | shown to the counter as | v2 units | v2 family | hand count | verdict |
|---|---|---|---|---|---|
| `INTERLOCUTOR-11.md` | FILE-1 | 6 | LISTNUM | **5** | **DISAGREE** |
| `INTERLOCUTOR-15.md` | FILE-2 | 4 | CHARGE | 4 | AGREE |
| `READER-128-3.md` | FILE-3 | 6 | HEADNUM | 6 | AGREE |
| `VERIFIER-125.md` | FILE-4 | 5 | CHARGE | 5 | AGREE |
| `VERIFIER-134.md` | FILE-5 | 7 | HEADNUM | **6** | **DISAGREE** |

## **K4′ FIRES. TWO OF FIVE DISAGREE. NO RATE IS PUBLISHED.**

The gate reads: *"If more than one of the five disagrees with the manifest, no rate is published and
the extractor is reported as unfit — again."* Two is more than one. This is the **second consecutive
session** in which the pre-registered extractor gate has fired, under the **second** extractor, on
**fresh files the extractor's design never saw**.

## Both disagreements were recomputed here before being adopted, against the files themselves

Neither is a matter of judgement, and both are **the exact two defects v2 was built to repair**,
named in `extract_units_137_v2.py`'s own docstring:

**`INTERLOCUTOR-11.md` — defect 1, "a remedy is not a finding."** The report's primary enumeration
is five bold lead-ins, `**Claim 1 — …**` through `**Claim 5 — …**` (lines 17, 36, 48, 55, 75), each
carrying its own verdict (BROKEN / QUALIFIED / SURVIVES). v2 split instead on the six numbered items
of its `# CONDITIONS` section (lines 82–87) — *"Fix or explicitly disclose…", "Add…", "Remove or
disclose…"* — which are remedies. v2's repair does not reach this case because rule (2), *specific
families win by kind*, privileges only CHARGE and LABELLED; a report that delimits its findings by
bold lead-in loses to any six-item numbered list, because BOLDLEAD fires only when **every** other
family is below MIN_UNITS.

**`VERIFIER-134.md` — defect 2, "it preferred a report's chapters to its findings."** v2 split on
the seven `## N.` chapter headings (`## 1. Recomputed numbers (check (a))` … `## 7. What I could not
check and why`). The report's own primary enumeration is its `## Summary of findings` list, six
items, each tagged BLOCKING or NON-BLOCKING.

**The counter reached both by reading, without seeing either count.** On `VERIFIER-125.md` it
returned AGREE at MEDIUM confidence and named the competing reading itself — 5 `### Finding N`
items against a 26-item *"What I RECOMPUTED and found CORRECT"* list — which is the same
under-determination in the counting criterion that `carve_audit_138.py`'s validation failure
located independently on `VERIFIER-133.md`. **That the criterion does not uniquely determine a
primary enumeration for a verification report carrying both a checklist and a findings list is a
defect in the study's own rule, not in the extractor, and it is recorded as owed.**

---

## The counter's report, published unedited

> # Hand-count results
>
> ## FILE-1
> **COUNT: 5**
>
> **DELIMITER FAMILY:** Bold lead-in headers `**Claim 1 — ...**` through `**Claim 5 — ...**`, each followed by a verdict (BROKEN / QUALIFIED / SURVIVES), in section "§a REFUTATION ATTEMPT." Verified by locating each header: Claim 1 (line 18), Claim 2 (37), Claim 3 (49), Claim 4 (56), Claim 5 (76). No Claim 6 exists.
>
> **REJECTED:** The `# CONDITIONS` numbered list, 1–6 (lines 83–88). This is explicitly a remedies list ("Fix or explicitly disclose...", "Add...", "Fix A8's directional blind spot...") — excluded by the criterion's own rule that a REMEDIES list is not the primary enumeration.
>
> **CONFIDENCE: HIGH.** The Claims are the document's only family that enumerates "what it found or answered" (each original claim is checked and given a verdict); the CONDITIONS list is categorically excluded, and §c has no enumeration at all (pure prose).
>
> ---
>
> ## FILE-2
> **COUNT: 4**
>
> **DELIMITER FAMILY:** `## Charge 1 [BLOCKING] — ...` through `## Charge 4 [NON-BLOCKING] — ...`. Verified: Charge 1 (line 135), Charge 2 (204), Charge 3 (265), Charge 4 (283). No Charge 5 exists.
>
> **REJECTED:** Two competing bulleted/numbered lists: (i) "What the refutation could not touch, and therefore what stands" — 9 unnumbered bold-lead bullets (lines 298–323); (ii) "What I tried that FAILED" — a numbered list, 1–5 (lines 332–349). Both are supporting evidence for/against the Charges, not the document's own primary "what did I find" enumeration — the document's own findings are structurally the numbered/tagged Charges, paralleling the "Finding N [BLOCKING/NON-BLOCKING]" pattern used in FILE-4.
>
> **CONFIDENCE: HIGH**, though I flag the 9-item "held" list as the strongest alternative reading if a machine extractor keys on bullet lists rather than headers — if so the alternative count would be 9.
>
> ---
>
> ## FILE-3
> **COUNT: 6**
>
> **DELIMITER FAMILY:** Numbered `## N.` headers 1 through 6 answering the fixed severed-reader questionnaire: "1. The single most important thing...", "2. What is it about?", "3. Who is it for...", "4. What would you not trust...", "5. Where...did you stop reading...", "6. Anything you noticed...". Verified all six present, no seventh.
>
> **REJECTED:** The 4 sub-bullets nested inside section 4 ("What would you not trust"). These are evidence supporting a single numbered item (item 4), not a separate delimiter family spanning the document.
>
> **CONFIDENCE: HIGH.** This matches the criterion's own clarification almost verbatim ("An answer to a question like 'what is this about?' ... counts as a unit").
>
> ---
>
> ## FILE-4
> **COUNT: 5**
>
> **DELIMITER FAMILY:** `### Finding 1 — BLOCKING.` through `### Finding 5 — NON-BLOCKING (informational).` under the `## Findings` header. Verified: Finding 1 (465), Finding 2 (503), Finding 3 (548), Finding 4 (566), Finding 5 (587). No Finding 6. The verdict line itself frames the report around this count ("Two blocking findings, both in the same document").
>
> **REJECTED:** The numbered list under "## What I RECOMPUTED and found CORRECT," items 1–26. This is a large, genuinely numbered family, but it is a differently-labeled, separately-headed list of confirmations, not called "Finding" and not the section the report's own verdict paragraph references.
>
> **CONFIDENCE: MEDIUM.** The 26-item recompute list is a serious competing candidate by sheer size and by the criterion's own instruction that "a check that reproduced correctly IS still a unit." What would settle it: whether the machine extractor keys specifically on a `### Finding N` heading pattern (→5) or on any top-level numbered list under a "found/recomputed" section (→26). I judge 5 more likely correct because the document's own self-description ("Two blocking findings") anchors on the Finding family specifically.
>
> ---
>
> ## FILE-5
> **COUNT: 6**
>
> **DELIMITER FAMILY:** The numbered list under "## Summary of findings," items 1–6, each tagged BLOCKING or NON-BLOCKING. Verified: item 1 (958), item 2 (962), item 3 (968), item 4 (971), item 5 (973), item 6 (975). No item 7.
>
> **REJECTED:** (i) The seven numbered `## N.` section headers (1–7, "Recomputed numbers" through "What I could not check and why") — these are structural chapters, not the findings themselves. (ii) The ~10-row confirmation table under section 1 — supporting detail for one section, not a document-spanning family. (iii) Inline "FINDING 1 — BLOCKING" / "FINDING 2 — BLOCKING" call-outs mid-document (lines 762, 800) are the same two items already present in the Summary list, not additional ones.
>
> **CONFIDENCE: HIGH.** The Summary of findings list is explicit, complete, and end-of-document, and (per the criterion's own clarification) includes non-fault items like item 6 ("Blinding is clean... with two generic words surviving masking"), consistent with "a check that reproduced correctly IS still a unit."
>
> ---
>
> ## Final table
>
> | FILE-1 | FILE-2 | FILE-3 | FILE-4 | FILE-5 |
> |---|---|---|---|---|
> | 5 | 4 | 6 | 5 | 6 |

*(The counter's line numbers are positions in the five-document bundle it was given, not in this
repository's files — FILE-1's "line 18" is line 17 of `INTERLOCUTOR-11.md`, and FILE-5's "line 958"
is line 240 of `VERIFIER-134.md`. **Every heading it names was checked here against the file itself
and every one is present at the stated position within its document.** The counts are the object of
this record; nothing in the quoted text is corrected, because it is published unedited.)*
