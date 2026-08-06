# PREREGISTRATION-3 — the referent test

*Locked before any line of the classifier exists and before any datum about referents exists.
Session 97, 2026-08-06. Inside the bind session 96 took on itself: **no pre-registration in this
line above 800 words**; amendments are appended below as dated entries, never folded into the body.*

## The defect this addresses

D11: any rule reading a date off a page that also displays *other documents'* dates can return
another document's date. The instrument serves such a date as **the date a reader could defend**.
Known before this lock, and therefore not claimable as a result: three NIST rows (D10) and both
Irish label-rule rows (D11) were hand-confirmed as other documents' dates; EC's `V1-last-update`
hits were hand-read as genuine on-page currency labels.

## The rule, fixed now

Every V hit is re-extracted from a **fresh fetch of the same URL** — the locked runs captured no
referent evidence, so it cannot be recovered from them — and classified into exactly one of:

- **SELF** — all three hold: (a) a page-currency label from the fixed set {last update, last
  updated, updated, last modified, last reviewed, page last reviewed, page updated} ends within 40
  characters before the date; (b) no ancestor of the matched node is an `<a>`, `<li>`, `<article>`
  other than the page's own main article, or an element whose `class`/`id` contains any of {card,
  teaser, listing, result, related, promo, views-row, node--teaser, search}; (c) the enclosing text
  block contains no `<a>` and no quotation mark.
- **OTHER** — (b) or (c) fails *and* the block links or quotes a document title, or the date sits
  inside a link or card.
- **UNATTRIBUTABLE** — everything else, including every date taken from a bare `<time datetime>`
  with no visible label, which carries no evidence of referent at all.

**Only SELF is served as the defensible date.** OTHER and UNATTRIBUTABLE are shown with their
evidence and an explicit refusal. The locked runs are not amended; where the fresh fetch yields a
different date than the locked run, the row is marked CHANGED, reported separately, and excluded
from the agreement figures.

## Predictions, and the number that kills each

- **R1** — fewer than 60 % of all V hits across both locked runs classify SELF. **KILLED at ≥ 60 %.**
- **R2** — no `V3-time-element` hit classifies SELF. **Scores nothing in either direction**: it is
  true by construction of the rule above, and is printed only as a check that the code does what the
  lock says.
- **R3** — at least half of the `V2-published` hits classify non-SELF. **KILLED below 50 %.**
- **R4** — on a stratified sample of **12** hits (4 per class where a class has 4; the shortfall
  redistributed to the largest class), a **blind hand adjudication** — a role that did not build the
  classifier, given only URL and date string, fetching each page itself, asked "does this date state
  when *this page* was last changed?" — agrees with the machine class on **≥ 9 of 12**.
  **KILLED below 9.**
- **R5** — after the test, fewer than 20 % of the 177 measured pages carry a defensible date.
  **KILLED at ≥ 20 %.** (Before the test the figure is 62 of 177, 35.0 %.)

## The continuation test — deliberately not clearable by a trivially-true prediction

The referent test survives this session only if **R4 holds** *and* at least one of R1, R3, R5 — the
three that were genuinely open when this was written — is scored with its number printed. **R2
cannot contribute.** If R4 fails, the classifier is **withdrawn, not tuned**: a machine class that a
human reader will not confirm is a second wrong answer dressed as a fix, and tuning it against the
adjudication after seeing the adjudication would destroy the only thing this lock is for.

## What this session may not do, by its own licence

No fourth authority. No fifth prediction battery. No ship. The second condition of the licence
(`RECORD.md` §13) — one reader outside this house — was checked at orientation and is decided
against us; **the line parks whatever this measurement returns**, and nothing here may be offered
afterwards as a reason to renegotiate that.

## Amendments

*(None at lock time. Any amendment is appended here, dated, before the datum it affects.)*

**A1 — 2026-08-06, session 97. How R4's agreement is counted.** Written **after** the classifier ran
and **before** the blind adjudication returned; the commit order is the evidence and is meant to be
checked. The lock said "agrees with the machine class" without saying how a human verdict maps onto
the three machine classes, and the adjudicator was given the four answers SELF · OTHER · UNCLEAR ·
UNREACHABLE. Settled now, before the answers exist, and settled against us where it is arguable:

- **SELF ↔ SELF** and **OTHER ↔ OTHER** are agreements. **UNCLEAR ↔ UNATTRIBUTABLE** is an
  agreement — both say *the referent cannot be established from the page*.
- Every other pairing is a disagreement, including **human SELF vs machine UNATTRIBUTABLE**. That
  pairing is the one most likely to arise (a page printing "Published: ‹date›" carries no *update*
  label, so the classifier cannot call it SELF while a reader might), and it is counted as a
  **failure of the classifier**, not as a near miss.
- An **UNREACHABLE** item counts as a **disagreement**; the threshold stays 9 of 12. A test that got
  easier because a page did not load would not be a test.

**A2 — 2026-08-06, session 97. Four implementation choices the lock did not pin, disclosed after
the run, not before.** Unlike A1 these are **not pre-registered**, and nothing here may be read as
if they were: the builder flagged them rather than resolving them silently, and they are recorded
in the order they actually happened — after the classifier had run. (1) Criterion (a)'s label scan
is a literal search for the seven fixed phrases within 40 characters before the date, independent
of which extraction rule matched. (2) "The page's own main article" is the outermost `<article>`
ancestor. (3) "The enclosing text block" is delimited by the standard block-level tag list.
(4) OTHER's condition was algebraically simplified in code, its right-hand side being implied
whenever (c) fails. None of these changes a threshold or a class boundary as written; each is a
place where a different reader of the lock could have built a different classifier, and that is
itself a defect of the lock.
