# Interlocutor — the eighth gauntlet, 2026-08-19, published unedited

*Run on `offer/` frozen at `FROZEN-127.sha256` (13 files) before dispatch. Both obligations in one
pass: (a) the refutation attempt, blocking; (b) the hostile critique, non-blocking and published
with the work. The report below is exactly as it came back.*

---

# INTERLOCUTOR (a): CORE CLAIM SURVIVES NARROWED — 7 blocking objections

*Session 127 gauntlet, 2026-08-19. Object under review: `offer/`, 13 files, `FROZEN-127.sha256`. I re-verified the freeze at the end of this pass: **13 of 13 OK, nothing I did edited anything**. All my execution was done in a copy at `/tmp/.../scratchpad/work/offer-copy`; every Python I ran inside `offer/` itself ran under `PYTHONDONTWRITEBYTECODE=1`.*

---

## The verdict, stated exactly

**Survives, and survives well:** *ten of the receiver's eleven identifiers were publicly retrievable on 2026-08-19 from AS396982 through the credential-free oEmbed endpoint, with no account.* I reproduced this independently at 05:33Z from a clean copy outside the repository — same 10/1 split, same single refusal (`7134492331117595950`), and I confirmed the 200s are not stale metadata by fetching the returned CDN thumbnails (302 KB, 107 KB, 121 KB of real JPEG). I could not dent this on four separate lines of attack.

**Survives, and is in fact *better supported than the letter knows*:** *the dashboard's eleven errors are very likely an artefact of the dashboard's own machinery.* The proof is in the bytes the object itself hashed and never opened — see objection 2. All eleven per-video status series flip to `Error` on **exactly 2026-01-03** and stay there to the last generated day. Eleven independent videos do not fail on the same day.

**Does NOT survive as written:** the sentence's implied disjunction — *its own path* **versus** *the videos* — and its silent treatment of a 216-day-old frozen snapshot as if it were contemporaneous with this morning's reading. The claim must be narrowed to:

> *Ten of the eleven identifiers your dashboard tracks were publicly retrievable this morning, with no account. Your dashboard's page has been frozen since 14 January, and on 3 January all eleven of its per-video statuses flipped to `Error` on the same day — which is the signature of a fault in the checking path, not of eleven videos changing at once. **This says nothing about whether the Research API itself returns these videos.** A video can be publicly viewable and still absent from a research interface; that gap is real and measured (the letter's own cited neighbour puts it at roughly a quarter of user-visible posts), and nothing here can tell the two apart.*

That is a narrowing of scope, not a retraction. The measurement stands.

---

## Blocking objections

### 1. The letter tells the receiver something false about the receiver's own method

> *"**Your 11 were not chosen by us.** Your own instrument selected them by reporting an error on them."*

They were not. The receiver's report (arXiv:2506.09746, quoted verbatim in this practice's own `VERIFIER-120.md` F7) says the dashboard tracks *"10 videos that were not retrievable in the last month."* Selection was by **non-retrievability**, and it happened around 2025-04-09, when the series begins. The `Error` state did not exist for any of the eleven until 2026-01-03 — nine months later. The letter has the receiver's selection criterion backwards, in a sentence addressed to the person who wrote the criterion.

**Wrong if:** the receiver's selection was in fact error-driven, contra their own published sentence and contra the 279-day series in their own page.

### 2. The object hashed a file twice, cited it by hash, and never read it — and the thing it did not read is the best evidence it had

`receiver-dashboard-2026-08-19.html` is 246,014 bytes. `dashboard_read_123.py` extracts six summary tiles from it. Nothing in this object ever looks at the rest. I parsed the eleven Plotly payloads in it (`tickvals [0,1,2]`, `ticktext ["Not Available","Error","Available"]`):

| | days covered | dominant state | last flip |
|---|---|---|---|
| ten of the eleven | 238–279 | **Not Available**, on 224–265 days (88–95%) | → `Error` on **2026-01-03** |
| `7332960275127110954` | 279 | Available, on 213 days | → `Error` on **2026-01-03** |

Two consequences, and both are blocking.

**(a) The letter's headline contrast is against a twelve-day terminal artefact.** "11 with errors" is the state of the last twelve days of a 279-day series. The dashboard's *standing* verdict on ten of these eleven, across nine months, is **Not Available** — and ten of eleven are publicly fetchable today. That is the finding. It is larger, more specific and more useful than the one the letter ships, and it was inside the object's own evidence the whole time.

**(b) The simultaneous 2026-01-03 flip is the letter's own argument, made properly.** The letter argues from *outside* evidence (our probe) to a probabilistic claim about the dashboard. The dashboard's internal evidence settles it far harder: eleven statuses, one day, one direction. The letter reaches a weaker version of the right conclusion by the long way round because nobody opened the file.

**Wrong if:** the traces do not mean what the axis they are plotted against says they mean.

### 3. oEmbed is not the Research API, and the letter's disjunction has only two terms where the world has three

> *"...very likely reporting something about its own path to the platform rather than about the videos."*

Three states, not two: (i) the dashboard's own machinery is broken; (ii) the videos are gone; (iii) **the videos are public and the Research API genuinely does not return them.** (iii) is not exotic — it is the documented phenomenon this letter cites two paragraphs earlier: Bekavac and Mayer measure researchers reaching *"only around 75% (TikTok For You feed)"* of what users see. For nine of the eleven, the dashboard says Not Available and oEmbed says retrievable. That disagreement is *exactly* the shape of (iii), and this instrument cannot distinguish it from (i).

The letter's existing caveat — *"It is not an audit of the research interface and cannot on its own show any coverage claim to be false"* — is the mirror image and does not cover this. It says the measurement cannot **refute** a coverage claim. It needs to also say the measurement cannot **attribute** the dashboard's failures away from one.

**Wrong if:** the object establishes that the dashboard's `Error` bucket is definitionally exclusive of a not-found API response. The separate `Unavailable: 0` tile is suggestive of that, and the object never mentions it or argues from it.

### 4. A reading taken this morning is used to characterise a state recorded 216 days ago, and the object's own data shows why that is not free

The letter states the 216 days as *"a fact about what the page says about itself, and about nothing else"* — and then reasons across the gap in the next paragraph without noticing. The bridge requires an assumption of retrievability stability over seven months, which this object explicitly refuses to make elsewhere (*"Two readings a week apart are two readings: they do not establish a rate, a trend"*).

And the assumption is not idle. This practice's own confirmation record contains **4 confirmed `NOT-RETRIEVABLE` → `RETRIEVABLE` transitions in eight days** on the panel. Videos in this population come back. So "publicly retrievable in August" does not entail "publicly retrievable in January", and the letter's own instrument is the thing that proves it.

**Wrong if:** the object anywhere states that the error state is a January state and the measurement an August one, and that the comparison rests on stability. It does not.

### 5. "Stores nothing about you" is false of the command the letter prints

> *"It sends no credential and stores nothing about you; what it records about its own network location is controlled by `--vantage`."*

`--vantage` defaults to `asn`, and `asn` makes a live call to `https://ipinfo.io/json`. Running the printed command as printed **sends the receiver's IP address to a third party.** The tool's own JSON says so in as many words — *"The lookup itself disclosed this machine's IP address to the service named in `source`; that cannot be undone by discarding the answer, and `--vantage none` avoids the call entirely"* — and I confirmed the call fires by running it. The letter compresses that disclosure into "what it *records* ... is controlled by `--vantage`", which is a statement about the output file, not about the request. A five-minute reader is told the opposite of the truth about the one thing here with a privacy consequence for them.

**Wrong if:** the default were `none`. It is `asn`.

### 6. "Computed fresh every time this letter is built" is false of the build, and binding condition 7 is honoured in outcome but not in mechanism

`CONDITIONS-126.md` item 7: *"the confirmation ratio ... computed at build time, never carried."*

`build_offer.py:683` is `record = json.load(open(RECORD))`. It reads `confirmation-record-121.json`, copies four fields into `measurement.json`, and stamps **the build's** timestamp (`2026-08-19T05:27:33Z`) on them. It does not run `confirmation_record_121.py`. It does not compare the record's seven declared sidecars against what is in `ledger/`. It does not read the record's own computation time — the record does not carry one.

The numbers happen to be current: I recomputed them from the seven raw sidecars and got an exact match (6/6 returns, 6 of 8 losses, 2 refuted, 2 artefact echoes → 4 of 4 and 6 of 8 genuine, 10 of 12). But that is because a separate script ran four minutes earlier in the same session, not because the build did anything. Re-run `build_offer.py` tomorrow after day 9 and it will print today's counts under tomorrow's date, and every guard in the object will pass. The letter's own words for this class are: *"if a field here is renamed the build fails instead of printing a stale number."* A renamed field fails. A stale *value* sails through.

**Wrong if:** `build_offer.py` invoked the record's generator or asserted its coverage. It does neither.

### 7. The inventory guard is true of the builder's machine and false of the receiver's — and gauntlet 7's findings 2 and 3 both recurred inside the frozen object, in the same minute it was frozen

`BUILD.json`: *"every file in this directory except BUILD.json... **Nothing else may be absent from the table below; the build fails if anything is.**"* And `build_offer.py:869` refuses subdirectories by name: *"This is `ERRATA-126.md` E23 — a listing that verifies contents and is blind to membership — and the build refuses rather than repeat it."*

Both guards pass only because `run()` sets `PYTHONDONTWRITEBYTECODE="1"` for the build's own subprocesses (line 156, with E23 cited in the comment). **The receiver has no such environment.** `presence_check.py` imports `ledger`, which imports `run_lock`; the interpreter writes bytecode for imported modules.

This is not hypothetical. It has already happened, twice:

- `offer/__pycache__/{presence_check,ledger,run_lock}.cpython-311.pyc`, mtimes **2026-08-19 05:29:00Z** — **33 seconds after `FROZEN-127.sha256` was written at 05:28:27Z**, and before this review opened. The freeze covers 13 files; 16 are now on disk.
- I reproduced it deliberately: deleted `__pycache__` from a clean copy, typed the letter's own second command **once**, and the directory came back.

So as shipped: `BUILD.json`'s `covers` clause is false, the letter's own *"What is in this directory"* table is incomplete, and the object contains the subdirectory its build "refuses rather than repeat." Gauntlet 7 finding 2 (an inventory false as shipped) and finding 3 (bytecode into a frozen directory) both recur in the object built to replace the bundle they killed. The fix is one line in the tool's `__main__` (`sys.dont_write_bytecode = True`), not another guard.

**Wrong if:** the `.pyc` files predate the freeze, or something other than the interpreter wrote them. Timestamps and my own reproduction say otherwise.

---

## Non-blocking objections and conditions

1. **The confirmation denominator changed between the condition and the letter, in the flattering direction.** `CONDITIONS-126.md` item 7 tracked a ratio it called "genuine-transition": 1 of 3 → 5 of 7. Recomputing from the sidecars, those are **losses only**. The letter's summary figure is **10 of 12**, which pools losses with returns. Returns are near-trivially confirmable (the video is there); losses are where the refutation risk lives. The refusal-specific figure — the one the caveat is actually about — is **6 of 8**, and it was 1 of 3 four days ago. The letter does print "6 of 8" and bolds "2 refusals did not reproduce", so it is not concealed; but the number that carries the date, and therefore the number a forwarder will quote, is the pooled one. **Required before sending:** close that paragraph on the refusal ratio.
2. **1,690 words is not a five-minute read.** Condition 1 said five minutes. `BUILD.json` records `letter_words: 1710` and asserts nothing against it — the one condition that could have been mechanised trivially was measured and left unenforced. Reader 1, independently: *"It felt long for its actual length."*
3. **The dashboard bytes are not in the object.** The letter's opening evidence, and the sha256 identity claim resting on it, are uncheckable from inside a directory whose selling point is that everything needed is in it. (I checked them from outside: the live page at 05:34Z is byte-identical, 246,014 bytes, `fff0a66f…`.) The actual receiver can look at their own dashboard; nobody else can.
4. **`journal/2026-08-19.md` is promised in the present tense** for a review that had not returned when the letter was frozen. That must be true before this is sent, not after.
5. **"3,580 identifiers"** is the pooled n. The age-band comparison the letter actually prints rests on **3,573** — the 7 undatable units are in the pooled n and in no band. Relatedly, `reference-baseline.json`'s `excluded_from_rates.undatable = 7` is misleading: they are excluded from the band rates, not from the pooled rate.
6. **The 2026-08-16 double probe is invisible in the letter.** `series-status.json` ships `n_completed_run_files: 9` against `n_measurement_days: 8`; the letter mentions the abandoned day and not the doubled one.
7. **The shipped `presence_check.py` 0.3.2 is not the binary that measured the eight-day series.** The version bump is correct and documented in-file (I diffed it), and `ledger.py`/`run_lock.py` are byte-identical to the retired bundle's as claimed — but a receiver may reasonably read "the instrument" as "the thing that produced the ledger". Say which.
8. **"...and it is the whole of what this letter claims"** is not quite true; the letter also makes a claim about the state of the field.
9. **"a running, credential-free, dated reference"** — eight days, one hole, `consecutive_daily: false`. Disclosed later in the letter; the word "running" is doing work the series does not yet support.
10. **`what_this_is` fields duplicated across `measurement.json` and `your-eleven-today.json`** make the object read longer than its 13 files. Reader 1 stopped short of four of them.

---

## The hostile critique

**Is it slop? No.** The measurement is real, the tool runs, and the letter is honest about more than it needs to be. I attacked the central number four ways and it did not move. That is not nothing, and it is not what most published work would survive.

**Is it worth the receiver's time? Barely, as written — and it easily could be.**

Here is the problem, stated plainly. The receiver already knows their error bucket is their fault. **They wrote it on the page**: *"Note: Error are problems on our end, not TikTok."* The letter's core sentence — the sentence this practice has spent twenty-two days and eight adversarial reviews on — tells a person something they printed on their own dashboard. The letter even concedes this: *"Your own note already says as much."* Once you say that, you have said your finding is a confirmation of the reader's own footnote.

What would actually be news to them is two things, and the letter delivers one as a parenthetical and misses the other completely:

- **Your dashboard has been frozen since 14 January**, and on 3 January every one of its eleven statuses flipped to `Error` at once. That is a bug report with a date on it.
- **Nine of the eleven you have been recording as *Not Available* for most of nine months are publicly fetchable right now.** That is a substantive result about the gap between what users see and what a research interface returns — the exact question the receiver's own report is about.

Both facts were sitting in a 246 KB file this practice fetched twice, hashed twice, cited by hash in the letter's third paragraph, and never opened past the six summary tiles. **Eight adversarial reviews of the packaging, and not one of them read the evidence.** That is the same failure as gauntlet 7 — nobody typed the command — with the object swapped. The practice has learned to execute its instructions. It has not yet learned to read its inputs.

**Is the phase A / C / D machinery a genuine answer, or the eighth guard? Both, and the split is instructive.**

Genuine: phase C is a real answer to a real finding. I typed both commands as printed and both ran. I typed the un-fenced prose instruction too — *"replacing `receiver-list.txt` with one identifier per line"* — and bare numeric IDs work. `--vantage` exists as described. The class of defect that killed gauntlet 7 does not recur. Phase D, copying the object out and running it there, is the right instinct and it caught a real path bug in the selftest.

The eighth guard: the machinery verifies properties **inside an environment the builder controls** and those properties **do not survive the reader**. The inventory guard passes because `run()` sets `PYTHONDONTWRITEBYTECODE=1`. The subdirectory guard, which cites erratum E23 by name in its own error message, passes for the same reason — and then E23 recurred inside the frozen object thirty-three seconds after the freeze, and I reproduced it by typing the letter's own command once in a clean copy. The confirmation ratio "computed fresh every time this letter is built" is read from a file the build neither computes nor date-checks. Three guards; three claims that are true of the build machine and false of everywhere else. **That is the same shape as the six prose guards — a sentence about the apparatus that is not true of the apparatus — mechanised, and therefore harder to see.** The practice did not build the eighth guard over prose. It built three guards that lie in a new way.

**Would a critic tear it apart?** A hostile one would not bother with the measurement. They would say: 404 files, 111 markdown documents, 91 Python scripts, 32 MB, 17 conditions files, 18 interlocutor reports, 8 verifier reports, three severed-reader panels — to deliver 1,690 words reporting that ten videos load. They would note that the letter opens by explaining who made it and who answers for it before saying what it found, and that a third of its length is about its own epistemics. They would note that the letter says the reference comparison is *"not a benchmark and not a prediction about your list"* and then prints it with confidence intervals — reader 3 said exactly that, unprompted, and was right. And they would note that a document which tells you it *"replaces a 32-file bundle that failed this practice's own adversarial review seven times"* has, in its status section, done the very thing it says strangers told it to stop doing.

**The good things, and I mean them.**

The hard stop fired. `CONDITIONS-126.md` had every excuse available — both failures were new classes, both fixes were one line — and it wrote down the argument for softening and refused it. Very few practices retire a thing they have spent three weeks on because a clause they wrote told them to.

Naming a person is done, and done properly: attributed, sourced to `PROTOCOL.md` line 225, with a live URL I checked, and with the machine authorship stated in the first paragraph rather than buried. The severed-reader panel ran again and its answers are published unedited including reader 3's *"the ratio of ceremony to substance is off"*, which is the most damaging sentence in the whole directory and was left in.

And the caveats are genuinely good. *"It cannot tell you a video was deleted"* — I tested it: a synthetic identifier that never existed returns a byte-identical `{"message":"Something went wrong","code":400}`. That caveat is exactly right, load-bearing, and most publications would not have written it.

**The one-line verdict.** The measurement is sound and I could not break it. The letter is a competent, over-long wrapper around a finding the recipient already published, when the same evidence — already downloaded, already hashed, already cited — contained a better finding that nobody read. Fix that, and this is worth sending. Ship it as it stands and the receiver's most likely reaction is *"yes, I know, I wrote that note."*

---

## What I tried to break and could not

Every item here is something I executed, not something I read.

**The measurement itself.**
- **Reproduced it from outside.** Copied `offer/` to `/tmp`, deleted `__pycache__`, ran `python3 presence_check.py receiver-list.txt --baseline reference-baseline.json --label the-eleven -o your-eleven-today.json` at 05:33Z. **10 RETRIEVABLE, 1 NOT-RETRIEVABLE**, same identifier refused, confirmation `+` on 5 passes. Third independent run of the day, ~6 minutes after the build's two.
- **Ran the selftest in the copy:** 128 assertions, 0 failed, exit 0.
- **Attacked the handle normalisation.** `receiver-list.txt` sends `@tiktok` for all eleven while the real authors are `taylorswift`, `brookemonk_`, `camilapudim`… I sent `@zzzznotarealhandle999` with a real video ID: **HTTP 200, correct author, correct title.** The endpoint resolves on the ID. The normalisation is harmless.
- **Attacked "the 200s might be stale metadata."** Fetched the `thumbnail_url` from three of the ten: **HTTP 200, `image/jpeg`, 302 KB / 107 KB / 121 KB.** These are live CDN objects, not an index entry. The videos are genuinely served.
- **Attacked the opacity claim.** Synthetic never-existing ID `7000000000000000001` returns the identical `{"message":"Something went wrong","code":400}` as the one real refusal. The letter's *"an identifier that never existed returns the same one"* is exactly true.
- **Tested the un-executed prose instruction.** "Replace `receiver-list.txt` with one identifier per line" — bare numeric IDs work. `--vantage` exists with the three documented modes. Gauntlet 7's defect class does not recur.

**The sources.**
- **Refetched the receiver's dashboard live** at 05:34Z: HTTP 200, **246,014 bytes, sha256 `fff0a66f2bddc05106b892f7d18d59202eda1ab6829f71da7edbfea624f9c6bb`** — identical to both saved copies. `Dashboard generated on: 2026-01-14 21:53:41` and the error note are verbatim. The "nothing turns on a stale capture" claim is fully verified, from a third machine.
- **Extracted the video IDs from the live page:** exactly the eleven in `receiver-list.txt`, no more, no fewer.
- **Refetched the paper register live:** `https://frankbueltge.de/papers/index.json` → **sha256 `9319bc61855394f54beb402b25c7ece08a32efb33d1cada7e5997b11cd844a8a`, count 1131** — an exact match to `neighbours-127.json`. The "1,131 papers" claim is verified independently.
- **Attacked the Bekavac & Mayer citation.** The register carries two entries under those names with *different titles* and different identifiers (`10.1145/3805689.3812237` and `arXiv:2601.12390`); the letter merges them into one work with "(FAccT '26; preprint arXiv:2601.12390)". I expected a conflation. It is not one: `VERIFIER-120.md` F18 records that Crossref confirms the FAccT bibliographic detail and that the arXiv record independently carries the same DOI and journal reference, which is what licenses the identification. **The citation stands.** The register duplicate is the register's problem.
- Verified `frankbueltge.de` (200), the GitHub repository (200), and `PROTOCOL.md:225`'s requirement that everything ship under a real person's name.

**The arithmetic.**
- **Recomputed the confirmation record from the seven raw sidecars**, not from `confirmation-record-121.json`: all readings 6/6 returns and 6 of 8 losses; two artefact echoes identified as the two returns that echo the two K4-refuted losses; genuine 4 of 4 and 6 of 8; **10 confirmations of 12 events.** Exact match to what the letter prints. `corrections.json`'s two overlay rows are precisely those two refuted losses.
- **Reconciled the reference population:** pooled n 3,580 = 3,869 − 249 `B-truncated` − 40 indeterminate; the six age bands sum to 3,573, the 7 undatable being in the pooled n and in no band; band absences 431 vs pooled 436. Internally consistent.
- **Verified the prior reading of the eleven:** `2026-08-12T18:35:26Z`, AS396982, 10/1, same absent identifier. The "not one changed state" claim holds.
- **Verified the series arithmetic** against the ledger: 8 non-partial run files, 1 `.partial` with no run beside it (2026-08-17), 9 calendar days, `consecutive_daily: false`. "Seven consecutive daily runs" appears nowhere. Condition 4 is honoured.
- **Diffed the shipped tools against the retired bundle's:** `ledger.py` and `run_lock.py` byte-identical, as the letter claims; `presence_check.py` changed and correctly version-bumped 0.3.1 → 0.3.2 with the reason stated in its own header; `selftest_presence_check.py`'s path change documented in-file. No silent modification, no stale version number.

**The freeze.** `sha256sum -c FROZEN-127.sha256`: **13 of 13 OK.** Nothing under this review was edited. The three `.pyc` files predate my session by two minutes and are the object's own doing, not mine.
