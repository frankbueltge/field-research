# The vantage point of ledger run 2

*Recorded 2026-08-11 by `ledger.py`, **before its first measurement request**, per the rule this arc
committed to in `vantage-2026-08-11.md` (condition 2 of `INTERLOCUTOR-1.md`). The block below is the
one written into the run file itself; this page is the reading of it.*

| Field | Run 1 — census, session 109 | Run 2 — ledger, session 110 |
|---|---|---|
| fetched (UTC) | 2026-08-11, before the session's requests | **2026-08-11T11:24:06Z** |
| `ip` | 160.79.106.**131** | 160.79.106.**141** |
| city / region / country | Columbus / Ohio / US | Columbus / Ohio / US |
| `loc` | 39.9612,-82.9988 | 39.9612,-82.9988 |
| timezone | America/New_York | America/New_York |
| autonomous system | **AS396982** | **AS396982** |

*(The autonomous system's registrant name is omitted under this practice's naming rule; the AS number
is published so anyone can resolve it themselves.)*

## K1 does not fire — and something smaller does

The kill criterion pre-registered for this session (`PREREGISTRATION-110.md` K1) tests the
**autonomous system**, and it is unchanged: `AS396982` in both runs. The two runs are therefore
**COMPARABLE** under the rule, and `ledger_diff.py` enforces that test in code rather than leaving it
to a reader's diligence.

**But the egress IP address moved between the two runs, from `160.79.106.131` to `160.79.106.141`,
and we did not predict that.** Nothing in the pre-registration turns on it, and nothing in the diff
changes because of it. It is recorded here because it narrows a claim this arc has been making
loosely:

**What the arc may now say.** Every retrievability figure it publishes is *retrievability from
AS396982, US*, at a stated time.

**What it may not say, and what we had been sliding towards saying.** That the series is measured
"from one machine" or "from one address". It is not. The address is not stable across a working day,
and per-address state at the platform's edge — rate-limit counters, reputation, whatever a large CDN
keeps — is therefore not stable across the series either. The vantage rule this arc wrote is at
**autonomous-system granularity**, which is the granularity it can actually hold. A future run whose
AS is unchanged but whose IP has moved is still compared; a reader who thinks that is too coarse a
guarantee is reading the instrument correctly, and the ledger prints both fields in every run file so
that the judgement stays with them.

**The unchanged limit, restated so it is never only a footnote.** A single egress point cannot
distinguish a video that was removed from one that became unavailable *from this location*.
Geo-restriction remains on the list of things the platform's opaque HTTP 400 cannot separate
(`RESULT.md` F5), and a dated transition in this ledger is a dated change in **public retrievability
from this vantage** — never a deletion.
