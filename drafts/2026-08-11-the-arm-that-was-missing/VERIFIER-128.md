# The ninth gauntlet — Verifier report, published unedited

*Session 128, 2026-08-20. Run on `letter/`, frozen at 17 files (`FROZEN-128.sha256`) before the
reviewer was dispatched. The reviewer worked in its own copy outside this repository; the freeze
verifies 17 of 17 before and after. Its blocking finding was reproduced by this practice with its
own commands before it was accepted — see `CONDITIONS-128.md`. Nothing below is edited.*

---

# Verification report — `drafts/2026-08-11-the-arm-that-was-missing/letter/`

## Freeze

Verified before and after. `sha256sum -c ../FROZEN-128.sha256` returns `OK` for all 17 files, both times; directory membership is 17 files both times; `git status --porcelain` is empty. **I changed nothing in the frozen directory.** All execution was done in `/tmp/.../scratchpad/copy-v` and `/tmp/.../scratchpad/readercopy`.

## Method

I did not read `extract_dashboard.py` or `dashboard_findings.py` before recomputing. I wrote an independent parser that walks `Plotly.newPlot("<id>", …)` in `receiver-dashboard-2026-08-20.html` with `json.JSONDecoder().raw_decode`, maps each per-video trace's numeric `y` through that plot's own `layout.yaxis.tickvals`/`ticktext`, and derives every dashboard figure from that. Separately I fetched the live page, the arXiv record, and the oEmbed endpoint first-hand, and ran all five printed commands in a copy outside the repository.

---

## A. Dashboard figures — all reproduce

Independent recomputation output (abridged):

```
N series: 11
=== last state change per series ===
7366758818765638917 ('2026-01-03', 'Not Available', 'Error')
7368154048836406544 ('2026-01-03', 'Not Available', 'Error')
7074367286571814190 ('2026-01-03', 'Not Available', 'Error')
7117394257064840490 ('2026-01-03', 'Not Available', 'Error')
7134492331117595950 ('2026-01-03', 'Not Available', 'Error')
7164125023886691626 ('2026-01-03', 'Not Available', 'Error')
7376726215178128673 ('2026-01-03', 'Not Available', 'Error')
7332960275127110954 ('2026-01-03', 'Available',     'Error')
7347581705299053826 ('2026-01-03', 'Not Available', 'Error')
7376437810644946222 ('2026-01-03', 'Not Available', 'Error')
7361448925972155679 ('2026-01-03', 'Not Available', 'Error')
=== 7332960275127110954 counts ===
Counter({'Available': 213, 'Not Available': 46, 'Error': 20}) total 279
=== Not Available day counts, the other ten ===
263 261 262 261 264 261 264 263 265 224      (min 224, max 265)
=== date range union ===  min 2025-04-09  max 2026-01-14  n distinct dates 279
=== summary chart cross-check ===  comparisons 837  disagreements 0
```

| LETTER.md claim | line | my recomputation | verdict |
|---|---|---|---|
| all 11 series change state for the last time on 2026-01-03 | 12 | 11/11, date 2026-01-03 | confirmed |
| 10 from *Not Available*, 1 from *Available*, all to *Error*, none changes again | 12 | 10/1, all to Error, no later change | confirmed |
| record ends 2026-01-14 | 13 | max date 2026-01-14 across all 11 | confirmed |
| 11 days from flip to record end | 13 | 2026-01-03 -> 2026-01-14 = 11 | confirmed |
| 218 days since | 13 | 2026-01-14 -> 2026-08-20 = 218 | confirmed |
| 229 days between | 41 | 2026-01-03 -> 2026-08-20 = 229 | confirmed |
| tiles: 11 with errors, none available | 14 | HTML: `<h3>11</h3><p>Total Videos Tracked</p>`, `0 Available Videos`, `0` unavailable, `<h3 class="status-error">11</h3><p>Videos with Errors</p>` | confirmed |
| `7332960275127110954` *Available* on 213 of 279 days | 15 | 213 / 279 | confirmed |
| 837 comparisons, 0 disagreements against the page's own summary chart | 17 | 3 traces x 279 dates = 837; 0 mismatches | confirmed |
| 224-265 day range over 10 of the 11 | 34 | min 224, max 265; the excluded one has NA=46 | confirmed |

Arithmetic closes elsewhere too: 279 recorded dates against 281 calendar days from 2025-04-09 to 2026-01-14, and `dashboard-findings.json` records exactly 2 one-day gaps. The letter states **no percentages**, so there is no undeclared-denominator problem — notably, `dashboard-findings.json` marks the adversary's "88-95 %" as `NOT REPRODUCED` and the letter correctly omits it.

## B. Measurement figures — all reproduce, including live

I ran the printed live command myself in a copy outside the repository:

```
the-eleven: 11 identifiers, 21.4 s, vantage AS396982 (US)
  7134492331117595950  NOT-RETRIEVABLE    http=400   4.00y conf=+
  (ten others RETRIEVABLE, http=200)
counts {'RETRIEVABLE': 10, 'NOT-RETRIEVABLE': 1}
```

- "10 of your 11 were publicly retrievable… 1 not retrievable, and still not after 5 re-requests" (L32) — confirmed, `n_unconfirmed_absent: 0`, five recorded confirmation passes all `NOT-RETRIEVABLE`.
- "9 of those 10 answered a public request this morning" (L35) — the single refusal, `7134492331117595950`, is inside the 224-265 group (NA=264), so 9 of 10. Confirmed.
- `2026-08-20T05:26:25Z`, `AS396982`, `https://www.tiktok.com/oembed?url=`, 5 passes (L27-30) — all match `your-eleven-today.json`.
- "0 of the 11 changed state across the three" (L36) — recomputed from `presence-check-receiver-113.json` (2026-08-12), `offer/your-eleven-today.json` (2026-08-19) and the shipped file: identical identifier set, `changed across readings: []`, `NOT-RETRIEVABLE every reading: ['7134492331117595950']`. Confirmed. My own fourth reading agrees.
- "5 of 5 apparent returns … 9 of 12 apparent losses" (L41) — I tallied the 8 `ledger/transition-confirm-*.json` sidecars from scratch: `NOT-RETRIEVABLE->RETRIEVABLE n=7 confirmed=7`, `RETRIEVABLE->NOT-RETRIEVABLE n=12 confirmed=9 refuted=3`; the two vids in `ledger/corrections.json` (`7368171405361351954`, `7016669364938149122`) are exactly the two artefact echoes, so genuine returns = 7 - 2 = 5, all confirmed. Confirmed, and the arithmetic closes.
- "9 measurement days across 10 calendar days, with 1 day started and abandoned" and `consecutive_daily` **false** (L82-84) — ledger holds 10 completed run files across 9 distinct days 2026-08-11…2026-08-20 (span = 10 days) with `run-2026-08-17T0337Z.json.partial` and no completed run beside it. 9 + 1 = 10. `consecutive_daily: false`. Confirmed.
- "an identifier that never existed returns the same [code]" (L43) — I tested it: `1234567890123456789` -> 400, `0000000000000000001` -> 400, same as the real absent one; `7332960275127110954` -> 200. Supported.

**No figure is typed.** `BUILD.json.figures_fetched` records 38 field fetches; the remaining rendered quantities (calendar span, headline counts) are derived in `build_letter.py` from fetched fields. See finding NB-6 for the one exception in kind.

## C. Quotations and attribution — verbatim and correctly attributed

- **Receiver's report** (L7). Quoted: *"we publish a dashboard with a daily check of the availability of 10 videos that were not retrievable in the last month."* Found at line 242 of `receiver-report-2506.09746v2-extracted.txt` (the extraction doubles spaces; whitespace-normalised it is exact), and independently in the arXiv abstract for 2506.09746, word for word. Context is the bullet introducing the public dashboard — correct.
- **Identification** (L7). arXiv metadata I fetched: Title *TikTok's Research API: Problems Without Explanations*; authors Carlos Entrena-Serrano, Martin Degeling, Salvatore Romano, Raziye Buse Cetin; comment names AI Forensics; the extracted report's credits page reads "All other content (c) AI Forensics 2025". Title, publisher and arXiv id are all correct. The report itself gives the dashboard URL at line 4063. The report says 10 videos; the dashboard now carries 11 — the letter says exactly this.
- **Dashboard's own note** (L20-21). Quoted: *"Note: Error are problems on our end, not TikTok."* Present verbatim in the saved HTML, in the paragraph under "Availability Trend Analysis" that describes the very chart the letter is reading. Attributed to "your own page" — correct.
- Footer (L14): the page prints `Dashboard generated on: 2026-01-14 21:53:41`. See NB-2.

## D. Statements the object makes about itself

- **"Every command below was run by this letter's own build, here"** (L48) — the five fenced commands in `LETTER.md` are byte-equal to `BUILD.json.commands`; `build_letter.py:654` runs each with `cwd=out`, i.e. the letter directory, and `run()` raises `SystemExit` on any non-zero exit, so "if any had failed, this letter would not exist" is enforced, not asserted. Confirmed.
- **"the 4 that need no network were run again from a copy made outside our repository, in a clean environment"** (L48) — phase D at `build_letter.py:714-723` copies to `tempfile.mkdtemp()` and runs the four offline commands with `PYTHONDONTWRITEBYTECODE` stripped from the environment. Confirmed. I reproduced it: fresh copy in `/tmp`, variable empty, all four exit 0.
- **No shipped file differs from its live source** (`BUILD.json`, 10 files) — I hashed every named source. All 10 match exactly (`tool/presence_check.py` -> `cca8317b…`, `tool/selftest_presence_check.py` -> `611070725a…`, `tool/ledger.py`, `tool/run_lock.py`, `tool/drift-122.json`, and the five in the draft root). Confirmed.
- **Running the printed commands adds no files** — I ran all five in a 17-file copy outside the repository with no bytecode variable set: membership unchanged (17 -> 17), and after the four offline ones every byte was unchanged. No `__pycache__` appears, because the tools set `sys.dont_write_bytecode = True` in their own source (`tool/presence_check.py:151`, `selftest:21`, `extract_dashboard.py:40`) rather than relying on the builder's environment. Confirmed.
- **"Everything the headline rests on is in this directory"** (L48) — true as narrowed. I derived the entire headline (11 series, 2026-01-03, 2026-01-14) from `receiver-dashboard-2026-08-20.html` alone, using none of the shipped code.
- **Inventory table matches the directory** — 17 table rows, 17 files, empty symmetric difference. Confirmed.
- **`Last-Modified`** (L13) — `receiver-dashboard-2026-08-20-fetch.json` records `Wed, 14 Jan 2026 20:53:43 GMT`. I fetched the live page myself: `last-modified: Wed, 14 Jan 2026 20:53:43 GMT`, `content-length: 246014`. Confirmed first-hand.
- **"bytes are identical to the copies we saved on two earlier days"** (L7) — `receiver-dashboard-2026-08-16.html`, `-19`, `-20` and my own live fetch all hash to `fff0a66f2bddc05106b892f7d18d59202eda1ab6829f71da7edbfea624f9c6bb`. Confirmed against a fourth, independent read.
- **Table cell descriptions** — `drift-122.json` "four of the suite's assertions": exactly four checks sit inside the `if os.path.exists(_MEAS)` block at `selftest_presence_check.py:366-378`. Confirmed. `run_lock.py` "imported by ledger.py": `tool/ledger.py:33 import run_lock`. Confirmed. `presence_check.py` "version 0.3.3": the selftest prints `presence_check 0.3.3`. Confirmed.
- **Terms and route** (L88-95) — `git remote` is `https://github.com/frankbueltge/field-research`; the repository is public (fetched); `frankbueltge.de` returns 200; `memory/downstream-commitments.md` exists and is tracked; `LICENSE.md` states Apache 2.0 for code, CC BY 4.0 for text, CC0 1.0 for data. All 17 letter files are tracked and committed (`ffdc3c2`). Confirmed.
- **"sends no credential"** (L74) — the only two outbound destinations in the instrument are `https://ipinfo.io/json` (vantage) and the oEmbed endpoint (`tool/ledger.py:44,76`); no auth header anywhere. `--vantage none` suppresses the first and the tool prints `vantage mode: none — no third-party call` either way, exactly as L76-77 says. Confirmed.
- **"Nobody has been contacted and it has not been sent"** (L3) — **unchecked.** Not verifiable from the repository.

## E. Fabrication

None found. Every source, identifier, quotation, name and URL in the letter exists and says what is claimed. Every number reproduces.

---

## Findings

### B-1 — BLOCKING. "Two figures are not reproducible here" undercounts; there are three.

**Document states** (`LETTER.md:48`): "**Two figures are not reproducible here**: the re-request counts and our series' length come from a daily ledger that is not in this directory. Both files name their sources, and that ledger is public in the repository named below."

**What the directory says.** A third figure is also not reproducible from this directory, and it is not from the ledger. `LETTER.md:35-37` states: "This is the third dated reading we have taken of these identifiers (2026-08-12, 2026-08-19, 2026-08-20); 0 of the 11 changed state across the three." Per `BUILD.json.readings_history`, the two earlier readings come from `deliverable-v0.3/receiver-eleven.json` and `offer/your-eleven-today.json` — neither is in this directory and neither is in `ledger/`. I grepped all 17 shipped files for `2026-08-12` and `2026-08-19`: no shipped file contains the per-identifier states of either earlier reading. `your-eleven-today.json` holds only the 2026-08-20 reading. The only shipped trace is `BUILD.json`'s own assertion `"n_changed_state_across_readings": 0`, which is a statement, not a derivation. A reader who checks everything in the directory cannot check that figure, and the letter tells them there are only two such figures and that both come from the ledger.

(The figure itself is true — I recomputed it from `presence-check-receiver-113.json` and `offer/your-eleven-today.json` in the repository. What fails is the sentence about the apparatus.)

**Fix.** Change the count and name the third source: e.g. "**Three figures are not reproducible here**: the re-request counts and our series' length come from a daily ledger that is not in this directory, and the two earlier readings of these identifiers are in this repository but not in this directory. Each names its source, and all of them are public in the repository named below." Derive the numeral from a computed count rather than typing it.

### NB-2 — non-blocking. The footer quotation is silently truncated.

`LETTER.md:14` prints the footer string as `Dashboard generated on: 2026-01-14`. The page prints `Dashboard generated on: 2026-01-14 21:53:41`. Backticks around a truncated substring read as a quotation. Nothing turns on it — the date is right, and the trailing local time (21:53:41) does not match the `Last-Modified` instant (20:53:43 GMT) anyway, so dropping it avoids a distraction. **Fix:** quote it in full, or drop the backticks and say the footer prints that date.

### NB-3 — non-blocking. "built 2026-08-20T05:26:25Z" is the probe's start, not the build's.

`LETTER.md:95` says "Version 2.0 of this object, built 2026-08-20T05:26:25Z." `build_letter.py:578` passes `read_utc`, which is `your-eleven-today.json.started_utc` — the live measurement's start. `BUILD.json` records `started_utc: 2026-08-20T05:26:24Z`, `finished_utc: 2026-08-20T05:27:08Z`. One second off the start, forty-three off the finish. **Fix:** render `BUILD.json`'s `finished_utc` there.

### NB-4 — non-blocking. `BUILD.json` does not in fact list *every* command the build ran.

`LETTER.md:101` describes `BUILD.json` as "every command this build ran, its exit status, and a hash of every file here." The log holds 16 command records, all with `returncode`. But `build_letter.py:219` runs a seventeenth — `python3 window_status.py <tmpfile>`, the in-flight ledger check — via a direct `subprocess.run` that never appends to `log`; only its result (`{"check": "no panel probe in flight…", "n_in_flight": 0}`) is recorded. Separately, `files` covers 16 of the 17 shipped files: `BUILD.json` cannot hash itself (it is covered by `FROZEN-128.sha256`). **Fix:** log the in-flight scan like any other command, or say "every command this build ran to produce the figures".

### NB-5 — non-blocking. "The first three read your dashboard's own bytes."

`LETTER.md:50`. Only the first two read the HTML. The third (`dashboard_findings.py`) reads the extractor's JSON output plus `your-eleven-today.json`. The letter itself corrects this two lines later ("The third of them reads the measurement shipped here"), so the reader is not misled for long. **Fix:** "The first three need no network."

### NB-6 — non-blocking. "third" / "the three" / "false" are typed, not derived.

`LETTER.md:35-37` and `82-84`. `build_letter.py:448` fetches `n_readings` but never renders it; the sentence hard-codes "the third dated reading" and "across the three", while the reading dates and the change count are interpolated. Likewise "`consecutive_daily` is **false**" is typed prose. All three are correct today (`n_readings: 3`, `consecutive_daily: false`), so nothing is wrong — but they are the one place where the build's own "no figure in the letter is typed" discipline (module docstring, line 47) does not hold, and a fourth reading would silently falsify the sentence. **Fix:** render the ordinal and the boolean from the fetched fields.

### NB-7 — non-blocking. "keeps no identifier of yours" is imprecise.

`LETTER.md:74`. Nothing is transmitted to this practice — I confirmed the instrument's only outbound destinations are the vantage lookup and the oEmbed endpoint — so the intent is sound. But the tool does write the reader's identifiers into the output JSON on the reader's own disk, so "keeps" is doing ambiguous work in a sentence whose whole purpose is a privacy assurance. **Fix:** "It sends no credential and reports nothing to us; the identifiers stay in the file it writes on your machine."

### NB-8 — non-blocking, informational. The phase-D membership guard tested 16 files, not the shipped 17.

`build_letter.py:717` snapshots the copy before `BUILD.json` is written, so `{"files_before": 16, "files_after": 16}`. The guard's conclusion still holds: I ran all four offline commands (and the live one) against the full 17-file shipped directory outside the repository and membership was unchanged, with every byte of every file identical afterwards. No change needed; noted so the log's `16` is not mistaken for a discrepancy.

---

**Verdict: FAIL** — one blocking finding (B-1) stands: `LETTER.md:48` states that exactly two figures are not reproducible from the directory and attributes both to the daily ledger, when a third — the cross-reading comparison at `LETTER.md:35-37` — is also not reproducible there and comes from elsewhere. Every substantive figure, quotation and attribution in the object is otherwise correct and independently reproduced; the defect is in a sentence the object makes about its own checkability, and the fix is a clause.
