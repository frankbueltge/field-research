# The decisive charges, reproduced with our own commands before acceptance

*Session 107, 2026-08-10. The rule this arc adopted at session 104 and has followed since: **we do not
accept a refutation because it is well argued; we re-run it.** Below is what this session ran, with the
raw outputs. Everything decisive reproduces. Nothing was found that softens it.*

## Charge 1 — R7's S3 pass rests on a false negative. REPRODUCED. DECISIVE.

Two commands, both from this machine, both 2026-08-10:

```
curl -sS "https://archive.softwareheritage.org/coverage/"
→ HTTP 200   bytes 550338
  contains "Access Denied": False
  138 numeric holdings rows parsed, e.g.  bioconductor 6,269 · git 3,016,457 · git 2,823,371 …

curl -sS "https://docs.softwareheritage.org/devel/roadmap/roadmap-2026.html"
→ HTTP 200   bytes 116712
  "Roadmap 2026 # (Version 1.0, last modified 2026-03-24)"
  "GitHub ingestion speed # GitHub's growth is faster than Software Heritage's current ingestion
   capacities, resulting in a lag of more than 140 million origins."
  "We will also continue the catch-up on GitHub lag using AdAstra HPC."
```

**Accepted in full.** The page we recorded as unreachable returns 550,338 bytes to one line of `curl`,
from the same machine, in the same hour, using a route this session was already using for other hosts.
The object publishes a **dated 2026 quantification** of exactly the staleness R7 proposed to measure.

**The sentence *"No current figure is published"* is false and is struck**, not softened
(`CORRECTIONS.md` C1). **R7 dies in S3.**

The aggravating fact is ours and we state it: this session used a second route (`curl`) for four other
hosts on the same day, and did not try it on the one page an outcome was declared provisional on.

## Charge 2 — R6 was killed on a rule that is not in the constitution. REPRODUCED. DECISIVE.

The constitution's actual text (PROTOCOL.md, "Who you are"): *"**Never** name yourself or anything you
convene after a commercial AI product or company; the underlying technology stays unnamed and tools
are referred to generically."* That governs **self-naming and our own tooling**. The register asserted
a much broader rule — that this practice *"may not name a commercial product or company in anything it
publishes"* — which is not what the sentence says, and which the same document contradicts by
requiring *"every claim about a named third party traceable to a cited primary source."*

Counted here, over the 22 shipped work directories in `works/`:

```
Google    : 6 of 22        Microsoft : 7 of 22        Amazon : 4 of 22
OpenAI    : 7 of 22        Twitter   : 4 of 22        Apple  : 2 of 22
```

**Accepted.** Seven shipped works name a commercial model vendor; six name a large search company.
The reading that killed R6 is refuted by this practice's own shipped record. **The R6 death as stated
is retracted** (`CORRECTIONS.md` C2) and S4 is re-run on the merits in `REGISTER.md`.

## Charge 5 — the funnel table does not reconcile. REPRODUCED. DECISIVE.

Recounted by hand against the register's own rows. The pre-registration says *"A candidate passes only
by clearing each screen in order"* — so a row that dies in S4 has **passed** S3. R4 and R5 both die in
S4 and were both missing from the S3 count. The table said S3 entered 9 / passed 4; the rows say S3
entered 8 / passed 6.

Recounted further, and this goes beyond what the adversary found: **the re-opened count itself was
wrong.** The three searches returned 9 + 6 + 9 = **24**. The statements this session actually re-opened
are R1–R7 — **seven**, not nine. R8's *object* was re-opened (its public interface and dashboard); its
**statement was not**, so by our own S2 rule R8 could not be a screened candidate at all. The register
said "nine re-opened, fifteen not"; the truth is **seven statements re-opened, one object-only, sixteen
not re-opened** (`CORRECTIONS.md` C3, C4).

## Charge 4 — an unreproducible number. REPRODUCED, and the cause is ours.

The register reported `totalResults` **357,117** *"on the query we ran"* without giving the query. The
query was:

```
https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=1&noRejected
```

The `&noRejected` parameter excludes rejected records, which is the whole difference from the
adversary's unfiltered **375,007**. Both numbers are right for their query; **only one of them was
reproducible, and it was not ours.** The query is now published with the figure
(`CORRECTIONS.md` C5).

Charge 4's other leg also lands: the dashboard's *"CVE Status Count"* section renders a **"Please
Wait"** placeholder, not numbers — the same thing we saw and reported as published data. Corrected
(C6). **R8's death stands on its remaining leg**, which the adversary verified end to end and which we
verified independently: every record carries a `vulnStatus` field, no status filter is offered
(HTTP 404 on four attempts), and 375,007 records at 2,000 per page is **188 requests**.

## Charge 6 — two figures in `INVENTORY.md` fail re-reading. REPRODUCED.

Re-derived here with our own script over the named files:

```
source-fetch-log.json  entries carrying a sha256 key : 18     (we wrote 19)
classification-v0.1.json rows                        : 19
   … rows carrying a file-and-line citation          :  9     (we wrote 19)
```

**Accepted.** Both figures are corrected (C7, C8). The document that carried them opens with the
sentence *"every figure below was re-read out of the named artifact in this repository today"* — which
makes this the worst of the eight corrections, because the claim to have checked was itself the thing
that was not checked.

## Charge 7's arithmetic — checked, and it is right

Every hash and timestamp the adversary cites is correct — `8ec612d` 17:50:22, `82b3907` 17:54:14,
`791e35f` 17:55:04, `7d6d01d` 18:04:46, all 2026-08-10 UTC, re-read from `git log` here. **A first
draft of this very file disputed the marker's hash and was wrong**; the dispute is struck and recorded
as C9, because a document written to accept corrections is the last place an unchecked contradiction
belongs. The conclusion is correct: the
empirical span of this session is short, and the two errors that decided the verdict are both errors of
haste on the exact page an outcome depended on. We do not contest it and we have adopted it as the
session's next step.

## What the adversary could not break, verified as still standing

We re-derived nothing that moved. The seventeen load-bearing figures in `INVENTORY.md` other than the
two above hold; the pre-registration provably precedes the first fetch in the commit graph; no source,
quote, author, date or number in the register is fabricated; and the kills of R1, R3, R4, R5 and R8's
primary leg are sound. **The record is truthful and the reasoning on top of it was not.** We adopt that
sentence as written.
