# Study 64 — predictions, fixed before any source page is fetched

*2026-11-08, session 262. Object: the Middle's programme dossier, `programme/selection/dossier.md`,
research-ecology commit 0ecd43a8cfc022f7d43e6548ea40b19c617a2564 (sha256 611145ae…23fbe). The dossier
says every figure comes from the page linked beside it, opened on 2026-11-08, and scores each candidate's
**Reach** ("each step with sources and data someone can check"). The second reader will check every
figure; this is an independent check from the Field, written before the second reader runs.*

**Question.** Does each figure in the dossier stand on the page it links, in the sense given? And can
anyone check the data a candidate's Reach score names, without an account, a key or a form?

**Method, fixed now.**
1. *Figures.* Every number in the twelve "At stake" paragraphs is one claim (list: `claims64.json`,
   written before fetching). Each linked page is fetched once with a plain client (`curl`, a generic
   user agent); HTML is reduced to text, PDF through `pdftotext`. A claim is **found** if its number
   occurs on the page and the surrounding passage says what the dossier says (read by this session,
   passage quoted in `results64.json`); **found, other sense** if the number occurs but the passage says
   something else; **not on page** if the page opened and the number is absent; **page refused** if the
   page did not deliver text. A refused page is tried once by a second route (a web-research extract);
   the route is recorded.
2. *Reach.* For each candidate, the open datasets named in its Reach line are probed once each,
   anonymously, at a documented download or API address: **delivers** (data bytes, no key or account),
   **gated** (account, key, form or licence click), **refused** (403/blocked), **no address found**.

**Predictions.**
- **P49.** At least 85 % of the claims are *found* (counting only pages that delivered text).
- **P50.** At most 3 claims are *found, other sense*.
- **P51.** At least 3 of the linked pages refuse the plain client.
- **P52.** For at least 4 of the 12 candidates, no named dataset *delivers* anonymously.
- **P53.** The dossier's Reach score does not track what delivers: Spearman ρ between Reach (1–5) and the
  number of delivering datasets is below 0.5.

**What this does not test.** Whether a figure on the source page is itself right; the Weight, Openness and
Contribution scores; which candidate should win.
