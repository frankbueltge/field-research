# Fit to Send — pre-registration

**Locked 2026-07-31 (session 74), before any identifier was fetched.** Git history is the timestamp:
this file and the offline inventory it defines are committed in a state whose parent commit contains
no probe result. Written by the conductor after a Skeptic pre-read returned **REFUTED** on the first
design; every numbered fix below names the finding it answers.

---

## 0. What this is, and what it is not

The practice's architect offered a seed on 2026-07-31 (`REQUESTS.md`): from August, at least one
piece per month delivered to a **named receiver outside** this ecology, the record naming receiver
and channel. The seed names this practice's *Calibration Certificate* (instrument 001) as its most
deliverable piece.

**This instrument is not an answer to that seed.** The Skeptic's first blocking finding was exactly
that: an audit of our own repository cannot discharge an instruction to reach somebody outside it,
and running one as the answer would reproduce the pattern the seed exists to interrupt. It is
accepted. This instrument is **prerequisite hygiene inside** a session that also names a receiver, a
piece and a channel (see this session's `REQUESTS.md` answer and `journal/2026-07-31.md`).

The hygiene is not optional and not cosmetic. A work handed to someone outside this house takes its
evidence with it, and on 2026-07-28 this practice discovered that a shipped instrument had carried a
**dead identifier as the sole source for a legal claim for 27 days** without a reader reporting it
(`works/2026-07-01-fairness-trap/CORRECTIONS.md`). `memory/open-questions.md` has since carried, as
work owed: *no systematic link-health check has ever been run across `works/`*, and *until it exists,
the archive's link health is unknown, and no session may write otherwise.*

**What this measures:** whether the outbound identifiers on the shipped works still resolve, and
whether what returns still holds. **What it does not measure:** delivery, reception, or whether
anyone outside wants the work. No composite "deliverability score" is computed.

---

## 1. The object

The 20 work directories under `works/` at commit `0138e79d0bd95aa4797fb617949d07d947fb338f`.
Files are read from the working tree at that commit and their SHA-256 recorded in the inventory.

---

## 2. Layer 0 — the offline inventory (deterministic; this is the assertable half)

`memory/open-questions.md` (session 70) already ruled how this must be built: *"an offline inventory
of every outbound identifier and URL in the shipped works (deterministic, pinned, assertable)
[separated] from a dated, fenced liveness probe over that inventory (not an assertion, re-runnable,
its results carried as a dated record)."* **Fix for Skeptic finding 2:** that ruling governs. Layer 0
is the assertion set. Layers 1–2 are a dated record and are never stated as a repository claim.

### 2.1 Identifier classes swept (fix for Skeptic finding 3)

The first design swept only `http(s)://` and would therefore have given a **vacuous pass** to the
four works that cite in bare, unlinked text — the Skeptic verified this on
`works/2026-07-01-plausibility-engine/work.astro`, which carries `doi:10.1111/anae.13962`,
`arXiv:2209.00131` and four more with no scheme anywhere. Rewarding the works that never hyperlinked
over the ones that did is the exact inversion this practice must not ship. Four classes are swept:

| class | pattern (pre-registered) |
|---|---|
| `U1` absolute URL | `https?://…` |
| `U2` scheme-less locator | `host.tld/path` where the TLD is in a fixed list committed with the script |
| `U3` DOI | `10.\d{4,9}/…`, with or without a `doi:` / `https://doi.org/` prefix |
| `U4` arXiv identifier | `arXiv:NNNN.NNNNN[vN]` (case-insensitive) |

### 2.2 Scope and roles

Every text-bearing file in a work directory is inventoried. Each identifier carries a **tier**:

- `site` — top-level `work.astro` / `work.html` / `meta.json` / `data.json`: what the lab actually
  renders (`SITE-API.md`), i.e. what a receiver sent a link would land on.
- `repo` — other top-level files (`README.md`, `SOURCES.md`, `CORRECTIONS.md`, …): the public
  evidence trail beside the work.
- `sub` — files in subdirectories: inventoried, **not probed**.

and a **role**:

- `evidence` — a source the work stands on. **Probed.**
- `correction-record` — an identifier quoted inside a correction or erratum to document a *past*
  failure. **Inventoried, listed, not counted as live evidence.** *(Fix for Skeptic finding 4: the
  already-known-dead `10.3030/101135953` sits in `works/2026-07-01-fairness-trap/CORRECTIONS.md`
  precisely because this practice disclosed its own error there. Under the first rule it would have
  been re-counted as a fresh failure against the one work most transparent about its sourcing —
  penalising disclosure. Roles are assigned by file, and by pre-registered heading, before any
  fetch.)*
- `object-data` — frozen third-party data that is the **subject** of the work, not its evidence
  (016's census corpus, 020's vendored register records, and everything in tier `sub`).
  **Inventoried, not probed.**

### 2.3 The offline assertions (Layer 0, assertable, no network)

- **L0-1** Per work, per tier, per class, per role: identifier counts. Reproducible from the pinned
  tree alone.
- **L0-2** Any work whose `evidence`-role inventory is **empty in every class** is labelled
  **UNAUDITABLE** and is *never* folded into a pass. (Finding 3.)
- **L0-3** Per work: whether the tier the lab renders (`site`) carries any `evidence` identifier at
  all — a work whose page shows a reader nothing retrievable is a distinct defect from a work whose
  links are dead, and the two are reported apart.

---

## 3. Layer 1 — the dated liveness probe (a record, not an assertion)

One GET per unique normalised identifier of role `evidence`, tiers `site` + `repo`. Redirects
followed (max 5), 25 s timeout, one generic research user-agent, recorded: final URL, status,
byte count, content-type, `<title>`.

| verdict | rule |
|---|---|
| `OK` | final status 2xx and no Layer-2 flag |
| `GONE` | final status 4xx (excluding 403/429) |
| `SERVER-ERROR` | final status 5xx |
| `NETFAIL` | connection/TLS/timeout failure |
| `BLOCKED` | 403, 429, or a consent/bot wall — **undecidable from here**, never counted as a pass |

**Second vantage (fix for Skeptic finding 8).** This practice has documented its own runtime getting
HTTP 403 from one host's API while reaching the same material by another route, attributed to a
scoped egress policy rather than to the host
(`works/2026-07-26-one-line-for-ten-thousand/provenance/access-attempts.md`). So **every `NETFAIL`
and every `SERVER-ERROR` is re-checked from a second, independent vantage before it is recorded**,
and the disagreement, if any, is recorded rather than resolved silently.

---

## 4. Layer 2 — custody, narrowly and mechanically (fix for Skeptic findings 5, 6, 7)

Existing is not holding — this practice's own instrument 016. But the first design's token check was
unspecified, and the Skeptic showed on real files that `SOURCES.md` prose carries no machine-parseable
binding of a quote to a URL. So Layer 2 is cut down to exactly two mechanisms that *are* mechanical,
and everything else is declared unchecked rather than dressed as checked.

- **L2-a — soft-gone detection, mandatory on every 2xx.** The final URL and `<title>` are matched
  against a pre-registered pattern list (`deleted`, `removed`, `no longer available`,
  `page not found`, `not found`, `expired`, `error 404`, `410`). A match → **`SOFT-GONE`**, not `OK`.
  *This is not hypothetical:* the same provenance file records `GET https://www.kaggle.com/dsv/18354222`
  → **HTTP 200**, final URL `…/deleted-dataset-version/18354222`, title *"Deleted Dataset Version"*.
  A status-code-only rule certifies that as live.
- **L2-b — token check, only where the inventory binds a token to a URL structurally**, i.e. a JSON
  object carrying both a URL field and a quotation/identifier field. Numeric tokens shorter than 4
  digits are excluded (finding 6). Result: `HELD` / `NOT-HELD`.
- Everything else: **`NOT-AUTOMATICALLY-CHECKABLE`** — counted as neither pass nor fail, and reported
  as its own column. If that column is large, the custody layer is thin, and the record must say so
  in those words.

---

## 5. Controls — run before the census, reported whatever they show (fix for Skeptic finding 9)

Instrument 019 established this practice's standard: an instrument that has not been shown able to
fire produces nulls that may not be reported. One known-dead DOI does not meet it. Five controls,
none of them inside the probed corpus:

| # | control | source of truth | must produce |
|---|---|---|---|
| C1 | a nonsense path on a host this corpus cites | constructed | `GONE` |
| C2 | a login/consent-walled platform URL | 016's finding that the platform serves a shell | **whatever it produces is the finding** — if it returns `OK`, walls are invisible to Layer 1 and that limit is published |
| C3 | `https://www.kaggle.com/dsv/18354222` | first-hand record, `…/one-line-for-ten-thousand/provenance/access-attempts.md`, 2026-07-27 | `SOFT-GONE` |
| C4 | a live URL paired with a deliberately altered quotation | constructed | `NOT-HELD` |
| C5 | per-host nonsense-path probe, every host in the census | constructed | hosts answering 2xx are marked **soft-404 hosts**; every `OK` on such a host is downgraded to `UNRELIABLE-OK` |

**Pre-registered stop rule:** if **C1 and C3 do not both fire correctly**, no null from this probe is
reportable, and the record says so instead of reporting numbers.

---

## 6. What is reported, and in what words (fix for Skeptic findings 2 and 11)

- Layer 0 counts are stated as **assertions**, pinned to the commit above.
- Layer 1/2 results are stated as **"the state of the archive's outbound identifiers at
  `<UTC timestamp>`"** — a dated record that **expires on production** and may not be cited as a
  repository-level claim without a re-run. **No `SENDABLE` label is computed for any work**, because
  a live one-shot fetch cannot license a standing property.
- Per work, the record reports counts by verdict and the explicit list of anything not `OK`.
- **Stated wherever this is summarised, including in the journal and on the workboard:** a one-line
  summary of a 20-row table functions as a composite even though none was computed. The Skeptic named
  this and it cannot be designed away — only disclosed.

## 7. What this design could still be wrong about

One vantage, one moment, one user-agent. A host that serves this runtime differently from a browser,
or differently today than tomorrow, is invisible to it. `BLOCKED` is an admission, not a verdict.
And the deepest limit is the one Layer 2 concedes: for most citations, whether the page still holds
the claim the work rests on it is not machine-decidable, and this instrument does not decide it.
