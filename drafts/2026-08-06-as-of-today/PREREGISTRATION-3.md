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
