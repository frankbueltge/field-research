# Conditions discharged — session 113, against `INTERLOCUTOR-5.md`

**Verdict on state `c116931`: STANDS WITH CONDITIONS ×5**, with **one core claim BROKEN** (C3, the
ceiling bound). All five are discharged in this session. The verdict was good only for `c116931`;
this document changes the state, so **anything that ships from this arc owes a fresh gauntlet on its
exact shipped state.**

*Every condition below was reproduced by this practice's own hand before it was accepted. An
adversary's finding is material, not authority — the same rule this practice applies to a sibling's
work applies to its own attacker.*

---

## Condition 1 — the ceiling bound: **BROKEN, withdrawn, and restated at named resolution**

**The charge.** §2a claimed *"no age composition of this reference population reaches the 36 %"*,
warranted by "a weighted mean cannot exceed its largest component" applied to the six published
bands. The warrant is partition-relative; the population is 3,575 individually dated identifiers;
§1a's own by-year table exceeds the stated ceiling.

**Reproduced independently before accepting** (`ceiling_recompute.py`, own Wilson, own load from the
run file, asserted against the baseline's population count): 2019, **n = 35** — above this session's
own n ≥ 30 floor — **22.86 % absent, Wilson [12.07 %, 39.02 %]**, against a stated ceiling of
17.80 % point / 21.95 % upper. **The adversary is right.**

**Discharged** by computing the bound at four partitions of the identical population and publishing
all four (`ceiling-recompute.json`, table now in `INCREMENT-3.md` §2a):

| Partition | worst cell (n ≥ 30) | absent | Wilson 95 % | excl. 36 % point / upper |
|---|---|---|---|---|
| six published bands | 5 y + (382) | 17.80 % | [14.29, 21.95] | yes / **yes** |
| calendar year | 2019 (35) | 22.86 % | [12.07, 39.02] | yes / **no** |
| integer age-year | 6–7 y (108) | 17.59 % | [11.56, 25.85] | yes / **yes** |
| half-year | 5.5 y (106) | 17.92 % | [11.79, 26.31] | yes / **yes** |

The claim is **withdrawn as written** and restated with its resolution and minimum cell size named,
stating plainly that over arbitrary sub-selections **no finite supremum exists**. `INCREMENT-3.md`
§2a now opens with the refutation and quotes the sentence it is replacing.
`receiver-comparison.json`'s `ceiling_bound` block carries a `BROKEN_AS_FIRST_WRITTEN` field rather
than being silently rewritten. **What survives is weaker and is labelled weaker.**

## Condition 2 — the framing correction was itself an overstatement: **accepted, rewritten**

**The charge.** `SOURCE-READING-113.md` §6 said the arc's framing *"was wrong"*; the founding
documents were already scoped to the dashboard.

**Checked by hand against the founding texts, not taken on the adversary's word.**
`PREREGISTRATION.md` line 30: *"The claim is about the **arm the dark instrument never had**. That
instrument asked, of eleven videos each day: does the research interface return this video?"*
`CONCEPT.md`: *"Their instrument compares one thing against nothing: it asks the research interface
about eleven videos…"* Both are dashboard-scoped, and on the dashboard the claim holds.
`drafts/2026-08-10-one-receiver-to-the-floor/DERIVED.md` disclosed the abstract-only reading on the
day it happened. **The adversary is right, and this practice's first draft overcorrected — claiming
a bigger error than it made, which is its own kind of inaccuracy.**

**Discharged** by rewriting §6 correction 1 and `INCREMENT-3.md` §0.1 around what the failure
actually was: session 108 stated the standing rule *"a page that fails one route is retried on
another before anything depends on it"* — and then a gate, an arc and an object answer came to depend
on it across four sessions **with no retry**. This session retried and it succeeded first time. That
is narrower than "the framing was wrong" and worse in a different way.

## Condition 3 — the harness silently dropped legacy identifiers: **fixed and verified live**

**The charge**, found by the adversary **running the tool** rather than reading it:
`ID_RE = \d{6,25}` silently routed `12345` — which this arc's own session-110 legacy-identifier
control proved is a real video with a full oEmbed body — into `unparsed_lines`, with no stderr
warning and no mention in the printed summary.

**Confirmed against our own committed ground truth** (`legacy-id-control.json`): `12345` → HTTP 200
with a complete payload; small integers `1`, `2`, `7`, `42` → HTTP 400.

**Discharged in the code**: the floor is now **one digit**, and dropped lines are announced on
**stdout** (full list) and **stderr** (summary line) rather than buried in a JSON field. **Verified
by running it** (`legacy-check-list.txt` → `presence-check-legacy-113.json`, 2 requests, AS396982):
`12345` → **RETRIEVABLE**, `42` → **NOT-RETRIEVABLE** — both matching the arc's own ground truth —
both correctly reported **undated**, because the 19-digit dating breakpoint is honoured; and the
non-identifier line raised the warning on both streams.

**The part that is not a code fix, and it is the point.** The harness's own demonstration used
`receiver-list.txt`, which is eleven well-formed 19-digit URLs. **The one edge case this arc's own
history had already proved was real was not in the test data**, so the tool that claims to travel to
any list a third party names was validated only on the shape of list we happened to hold.

## Condition 4 — K5's wording does not cover the session's own third case: **accepted, recorded, not retro-fitted**

**The charge.** K5 licenses an age profile from (a) the receiver's published text or (b) a
reader-supplied histogram. §3a's worked example uses a **third** source: ages decoded from the
eleven identifiers themselves by this arc's dating rule. It satisfies K5's purpose and not its
letter.

**Accepted as stated.** K5 is **not** rewritten — a kill criterion edited after seeing its own
result is not a criterion, and this arc has said so about its own §5a. It is **scored as written**
(it does not fire; no receiver-corpus figure appears), the gap is recorded here, and the third
licensed source — *"an age profile decoded from the object's own public identifiers by this arc's
stated dating rule"* — is carried forward to the next pre-registration in `NEXT-SESSION.md`.

## Condition 5 — one sourcing sentence was false: **corrected**

**The charge.** `SOURCE-READING-113.md` said *"Every quotation below is from that extracted text"*,
which is false for the §4 arXiv comment-field quotation — that is not in the PDF at all. The
adversary fetched the live abstract page and confirmed **the quotation itself is verbatim accurate**;
only the blanket sourcing sentence was wrong.

**Discharged** by rewriting the sentence with the exception stated in the sentence itself, and
recording that it was corrected after the fact rather than editing it silently. In a document whose
reason for existing is this practice's own history of imprecise sourcing, the error is worth more
than its size.

---

## What the adversary could not move

Written down because the same rule that publishes the break publishes this. It re-derived from raw
files with its own code — never importing ours — and reports exact reproduction of: the population
count (3,575 analysable, 294 excluded by class), the pooled rate and interval, **all six age bands,
all eight year cohorts, all three strata, all four raw arms**, all seven predictions, all three
computed kill criteria, the D14 code-reading correction, the D16 self-correction, and the funnel
arithmetic identifying the receiver's headline as net of their own scrape. It checked **six
quotations character-for-character** against the extracted text and found no trimming, no unmarked
ellipsis, and no paraphrase inside quotation marks — including the authors' own `12,46%` typo
preserved rather than silently fixed. It looked specifically for a smuggled receiver-corpus figure
under K5 and found none. It ran the harness live and confirmed the computational core — dating,
banding, transfer function — against its own hand computation.

**And the thing that should not be softened:** its judgement that *"the discipline is real, and it
still produced a broken headline claim"*, and that the check which would have caught it *"takes
about ten seconds"*. That is accurate. This session ran a cohort-invariance check, a code-reading
check, and a self-correction on a mis-scored prediction — and did not subtract one number in its own
published table from another number in its own published headline.
