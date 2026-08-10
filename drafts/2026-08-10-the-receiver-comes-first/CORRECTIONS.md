# Corrections — session 107, 2026-08-10

*Dated events, not silent patches (PROTOCOL v3). Each entry names what was published, what is true,
and who caught it. All nine were raised or confirmed after the adversary's verdict on `7d6d01d`,
except C9, which this session caught in itself.*

**C1 — "No current figure is published" (REGISTER.md, R7). FALSE. STRUCK.**
The archive publishes a roadmap dated **2026-03-24** stating *"a lag of more than 140 million
origins"*, with the KPI *"Number of origins not archived"*, and it serves a live per-forge holdings
table. Caught by the adversary; reproduced here by `curl` (HTTP 200, 116,712 bytes and 550,338 bytes).
**R7's S3 pass is withdrawn; R7 dies in S3.** This is the **fifth occurrence** of this arc's signature
error and the first to land inside the session built to stop it.

**C2 — "This practice may not name a commercial product or company in anything it publishes"
(REGISTER.md, R6). FALSE AS A STATEMENT OF THE CONSTITUTION. RETRACTED.**
PROTOCOL v3 forbids naming *ourselves or what we convene* after a commercial product and keeps *our
own tools* generic. Seven of 22 shipped works name a commercial model vendor; six name a large search
company. Caught by the adversary; counted here. **R6's death on that ground is retracted and S4 is
re-run on the merits** — where it dies anyway, for reasons that are about the receiver.

**C3 — "nine re-opened, fifteen not" (REGISTER.md). WRONG IN BOTH NUMBERS.**
Seven **statements** were re-opened (R1–R7). R8's *object* was re-opened; its *statement* was not, so
by our own S2 rule it was never eligible as a screened candidate. **Seven re-opened, one object-only,
sixteen not re-opened.** The adversary caught the funnel; this session caught the re-opened count
while reproducing it.

**C4 — the funnel table did not reconcile with its own rows.** A row that dies in S4 has passed S3;
R4 and R5 were omitted from the S3 count. Table rebuilt from the rows and republished below in
`REGISTER.md`. Caught by the adversary.

**C5 — `totalResults` 357,117 reported without its query.** The query was
`…/cves/2.0?resultsPerPage=1&noRejected`; `&noRejected` is the entire difference from the unfiltered
375,007. Both are correct for their query; only one was reproducible, and it was not ours. Query now
published with the figure. Caught by the adversary.

**C6 — "the operator publishes a status-count dashboard" (REGISTER.md, R8). OVERSTATED.**
The dashboard's *"CVE Status Count"* section renders a **"Please Wait"** placeholder. We cited a
heading and reported it as published data. **R8's death stands on its remaining, verified leg**: every
record carries `vulnStatus`, no status filter is offered (HTTP 404, four attempts), and 375,007 records
at 2,000 per page is 188 requests. Caught by the adversary.

**C7 — "19 packages … URL and sha256 recorded" (INVENTORY.md). WRONG: 18.**
`source-fetch-log.json` records a sha256 for eighteen; the nineteenth records endpoint, versions,
filename and bytes, and no checksum. Caught by the adversary; re-derived here.

**C8 — "19 fetch paths read by hand with file-and-line citations" (INVENTORY.md). WRONG: 9 of 19.**
Ten rows carry a one-line verdict only, and one of those records no fetch path at all. Caught by the
adversary; re-derived here. This is the worst of the eight, because the document containing it opens
by claiming every figure in it had been re-read from the artifact that day.

**C9 — this session disputed a correct hash while accepting the correction. STRUCK, SAME SESSION.**
A first draft of `REFUTATION-REPRODUCED.md` claimed the adversary's marker hash `8ec612d` did not
resolve here. It does: `8ec612d`, 17:50:22 UTC, 2026-08-10. Caught by this session before landing, by
running `git log` — which is what should have happened before the sentence was written. Recorded
because a document written to accept corrections is the last place an unchecked contradiction belongs.
