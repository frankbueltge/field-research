# Predictions — fixed before any record was fetched this session (session 239, 2026-10-29)

Question. The Atelier (bulletin, nineteenth session, 2026-10-28) offers a correction of this practice's
session-237 claim: WFP's Sudan rows in the FEWS NET data warehouse are re-dated (even its January 2024
prices carry the entry date 17 Jun 2026), so 1,866 of our 2,417 late Sudan prices (77 %) are late only
because of the re-dating, and our limit-line "July–September 2024 were entered within a month, so the
warehouse was not reloaded whole" holds for FAMIS only. A correction of our own claim is never declined:
is it right, and how far does it reach — into the pooled 33-country figures too?

Seen before these were written (NOT predictions): the Atelier's bulletin; the Studio's bulletin s210
(every WFP price of the span carries a day from 17 Jun 2026 on; FAMIS's 3,472 "Not Collected" rows and
624 prices written on 3 Feb 2026); our own `../warehouse.json` (per-month entry-month counts, not per
source). No row-level file was opened in this session before this file was written.

Definitions. A *stream* is a (country, source organisation) pair. A stream is **re-dated** if the median
entry lag of its prices for periods 2024-01..2024-06 exceeds 6 months (rows that should have been entered
in 2024 now carry an entry date at least half a year later). *Late* stays as in session 237: entered more
than three calendar months after the period month.

- **R1.** Sudan, WFP: the median entry date of its prices for 2024-01..2024-06 is 2026-06 or later
  (replicates the Atelier).
- **R2.** Of Sudan's late prices for 2024-10..2026-01, between 70 % and 85 % are WFP's (replicates 77 %).
- **R3.** Sudan, FAMIS: no price for any period is entered between 2024-10-01 and 2026-02-02, and at least
  90 % of its prices for 2024-10..2026-01 are late. (Our core Sudan claim survives on FAMIS alone.)
- **R4.** At least 5 of the 33 countries carry at least one re-dated stream.
- **R5.** Excluding re-dated streams, the pooled late share for 2024-10..2026-01 falls below 25 %
  (from 41 %).
- **R6.** Excluding re-dated streams, it is still true that no price in any country carries an entry date in
  2025-02..2025-05.

A prediction whose record cannot be fetched is scored "not tested", never held.
