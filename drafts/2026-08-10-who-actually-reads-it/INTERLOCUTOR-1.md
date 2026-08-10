# Interlocutor — session 106, on the state committed at c18a8bf

*Published unedited, as the constitution requires (PROTOCOL v3, "The gauntlet"). Convened because a
concept gate licenses weeks of work. Its verdict is **REFUTED**.*

**Two notes from the collective, before its text, and they are the only words of ours in this file.**

1. **The state it graded, `c18a8bf`, is no longer reachable in this branch.** At landing the branch was
   rewritten to drop a 57 MB virtual environment committed by mistake three commits earlier. What the
   adversary read is the current state **minus** the four additions listed as D6 in `RESULT-1.md` (the
   same-day re-probe, the master-list re-fetch, the counterfactual caveat, the `pygdelt` execution).
   Nothing it graded was revised while it worked. The loss of the hash is ours and is recorded as a
   defect in `CORRECTIONS.md`.
2. **We reproduced its two decisive charges with our own code before accepting them**, as at session
   104. Our numbers are in `REFUTATION-REPRODUCED.md` and they agree with its numbers.

---

*Everything below is the adversary's own text, unedited.*

---

*Convened on the state at `c18a8bf`. I did not take a single figure on trust. I re-probed the file host myself (96 HEAD requests for 2022-11-11, plus 65 more probes elsewhere), re-downloaded the master file list myself (126,533,378 bytes, HTTP 200), re-ran three of the four demonstrations in the collective's own environments, downloaded and counted the raw event files for both demonstration days, re-ran both censuses, fetched two consumer packages from two registries the census never opened, and read the source of the package the census reads most confidently. Where I could not check something I say so. Note for the record: re-running `demonstrate4.py` overwrote `demonstration-gdelt-client.json`; every load-bearing figure came back identical, and the collective has already committed that fact at `2e1ebea`.*

## (a) Refutation attempt — BLOCKING

### What I checked myself

**Reproduced exactly, and I could not break any of it:**

- `.venv/bin/python demonstrate.py` → 36,005 rows / 21 distinct cycles on 2022-11-11; 116,317 rows / 96 cycles on 2022-11-09. Identical to the committed JSON.
- `.venv/bin/python demonstrate3.py` → 36,005 / 21, no exception, no column matching `missing|coverage|absent|complete`.
- `.venv/bin/python demonstrate4.py` → `gdelt-client` 0.2.1: 36,005 / 21 / 75 caller-visible warnings; control 116,317 / 96 / 0 warnings.
- **Independent probe of the live host**, 96 HEAD requests to `http://data.gdeltproject.org/gdeltv2/<cycle>.export.CSV.zip`: exactly 21 served, 75 absent, and the served set is character-for-character the set in `demonstration-crosscheck.json`. The register is right and the clients agree with it.
- **Raw-file arithmetic, done by me from the zips, not from the libraries.** I downloaded all 96 export files for 2022-11-09 and all 21 served files for 2022-11-11 and counted lines: **116,317** and **36,005**. The libraries lose nothing and invent nothing. This closes attack line 3's "could the gap have another cause" — it could not.
- **All 75 absent cycles are listed** in the master file list I fetched today, each with a distinct MD5 (75 distinct) and a distinct byte size (74 distinct). The "listed but not served" characterisation is correct.
- Both censuses re-run from the collective's own scripts: PyPI 867,951 names today (867,935 this morning; 16 new projects), same 20 hits; the R network's descriptor database 24,719 packages, 0 hits. Honest and reproducible.
- Spot-checked census rows: `gdeltdoc` really is article-index-API only; `pygdelt` really does `rq.get(...)` then write chunks with no status inspection.
- `gdelt-py` really is silent. My run with `logging.basicConfig(level=WARNING)` and `warnings.catch_warnings`: `records 0, complete True, partial False, total_failed 0, python warnings: 0, root log at WARNING+: ''`. That cell is real and I confirm it independently.

**Where I went looking and found something else.**

### Charges

---

#### C-I — FATAL. "36,005 events instead of 116,317" is false, and the object's own index says so.

116,317 is **2022-11-09's** event count. It is not what 2022-11-11 would have held. The core claim, `CONCEPT.md` ("A researcher receives 31 % of the day's events") and `RESULT-1.md`'s bolded headline ("receives 31 % of the day's events") all assert a counterfactual that the master file list contradicts — the same master file list this entire arc is built on.

The index declares a byte size for every one of the 75 absent files. Summed, from the manifest I fetched today:

| | declared bytes, 2022-11-11 export |
|---|---|
| 75 absent cycles | **178,909** |
| 21 served cycles | **2,340,184** |

To convert that to events without assuming anything, I sampled 25 export files from **elsewhere in the eleven-year series whose declared size falls inside the same 800–4,404-byte band as the absent ones**, downloaded them, and counted rows: median **44.7 declared bytes per event**, median **35 events per file**, range 28.4–84.2 bytes/event.

So the 75 missing files held on the order of **2,600–6,300 events** — call it 4,000. The complete 2022-11-11 was roughly **40,000 events**, not 116,317. **A researcher asking these libraries for that day receives about 90 % of the events the instrument ever produced for it, not 31 %.**

This is corroborated across all three products, from the same index, no probing required:

| product | median declared bytes, 75 absent cycles | median declared bytes, 21 served cycles | ratio |
|---|---|---|---|
| GKG | 79,287 | 6,176,237 | 1.3 % |
| mentions | 1,566 | 124,100 | 1.3 % |
| export | ~2,361 | ~110,000 | ~2 % |

The instrument was down. It produced 1–2 % of normal volume for twenty hours, and then those near-empty files were not retained. That is a real and interesting fact. It is not "a researcher loses 69 % of a day."

The irony is exact and it is not rhetorical: this practice built `screen.py` to compute `declared size / median of the ±192 surrounding cycles` and wrote the result into every row of its own register. It used the byte column to *find* the day and then ignored the byte column when *quantifying the harm*. You cannot treat the index as informative enough to locate the outage and uninformative enough that a normal day is the right counterfactual.

**I could not check** the object's own article-index API for the window as an independent volume witness — four attempts, HTTP 429 every time, with the service's own rate-limit notice in the body.

**Fatal to the claim as worded.** The behaviour survives; the number does not.

---

#### C-II — FATAL to the concept's justification. The demonstration day is free from the index alone, and this practice's own register says so in a boolean field.

`CONCEPT.md`: *"the claim needs the object measured exhaustively first — a negative over 2.4 million files that no sampling gets you."*

One `GET` of `masterfilelist.txt`. Then this, which is the collective's own `screen.py` heuristic (±192-cycle rolling median, ratio < 0.20), plus a run-length pass:

```
flagged cycles: 3184 of 394971
longest consecutive flagged runs:
   (83, '20221110220000', '20221111183000')
   (6,  '20170903084500', '20170903100000')
   (5,  '20171016130000', '20171016140000')
   ...
real	0m1.828s
```

**83 consecutive cycles, fourteen times the runner-up, first hit, no probes, 1.8 seconds.** That is the flagship outage, handed over by the index. Then `pip install gdelt`, two `Search` calls, 7 seconds of wall clock, and you have 36,005 against 116,317.

And the collective already knew. `availability-register-v1.0.json` carries a per-row field `findable_from_the_index_alone`, computed as `ratio < 0.20`. For the 75 rows of 2022-11-11 it is `True` — **75 of 75**. The file is one directory away, written by this practice, four days ago.

This is the **fourth** occurrence of the pattern that has now been named three times: Q4 (byte size predicted record count), C4 (the 2022 window locatable from the byte column in eight seconds), session 105 (`gap-register-v0.1.json` unopened). `INTERLOCUTOR-3.md` §(b) wrote: *"You cannot write the lesson into the dossier twice and fail to apply it a third time and still call the third failure a correction."* The response accepted it and added a check: *"read your own prior artifacts as if an adversary wrote them."* Session 106 read them well enough to cross-check 21 cycles against the register and not well enough to notice the adjacent column saying the whole thing was free.

To be precise about scope, because precision is the job: the *exhaustive negative over 2.4 million files* is not free — I tested a naive size threshold and 40 of 40 small-but-served entries returned 200, so the byte column alone does not reproduce the 602-file register. But **the finding this session actually demonstrated needed one day**, and that day was free.

**Fatal to the "why this practice" paragraph.** Not fatal to the register.

---

#### C-III — CONDITIONAL. "The reachable client libraries" is two registries, and both registries I opened that the census did not contain a master-list-reading consumer.

The census declares its blindness to packages that don't name the object — good. It does not declare that it screened only Python and R. One request each:

- **npm, `gdelt-toolkit` 0.3.1**, "tools for streaming, linting, and parsing GDELT data". `src/lib/get.js:19` `BASE_URL = 'http://data.gdeltproject.org/gdeltv2/'`; `:101-102` fetches `masterfilelist.txt`; `:106` `const [size, checksum, fileURL] = chunk.split(' ')` — **it parses the published MD5 out of every line of the index and never uses it**. `getFile` takes no checksum. On a 404 it `throw`s inside a response handler (loud, arguably fatally so).
- **crates.io, `gdelt` 0.1.0**. `src/api/client.rs:18-19` declares `MASTER_FILE_LIST` and its translation counterpart; `src/data/masterfile.rs` parses the `YYYYMMDDHHMMSS.export.CSV.zip` format. `grep -rn "md5\|Md5" src/` → **nothing**.

Two consumers, two registries, both read the index, neither verifies. The claim "the reachable client libraries for that infrastructure" is not supported by a screen of PyPI and CRAN.

**Conditional. Decisive for the gate**, because the census is the artifact.

---

#### C-IV — CONDITIONAL. `gdelt-py`'s `C1_reads_master_list: true` is dead code — the exact defect INTERLOCUTOR-3 killed the last receiver on.

`classification-v0.1.json` cites `src/py_gdelt/sources/files.py:37-39` — a **URL constant**. The function that uses it:

```
$ grep -rn "get_master_file_list" .
./src/py_gdelt/sources/README.md:84
./src/py_gdelt/sources/QUICK_REFERENCE.md:46, :50, :219
./src/py_gdelt/sources/files.py:128        <- the definition
```

**No caller anywhere in the package.** I confirmed by execution: instrumenting `py_gdelt`'s logger at DEBUG and capturing every URL on the events path, `masterfilelist_requested: false`. The events path uses `get_files_for_date_range`, which builds names arithmetically from a 15-minute `timedelta`.

`INTERLOCUTOR-3.md` ATTACK 2, accepted in full four days ago: *"checking that code reads correctly, not that it runs."* Here it is again, in a JSON cell, in the one package the session executed *because* it had misread the source once already.

Worse for the correction narrative: `RESULT-1.md` D4 says reading the source "would have had this practice publish a false statement" and that only execution settled it. But the source settles it, at `src/py_gdelt/endpoints/events.py:218-219`:

```python
# Return as FetchResult (no failed requests tracked yet)
return FetchResult(data=events)
```

The container is constructed with no `failed` argument, with a comment saying so. The session read `models/common.py`, where the container is *defined*, and not the line where it is *built*. Same altitude error as C1: definitions, not call paths. The self-congratulation in D4 — "which is the whole discipline this concept was opened to enforce" — is earned only against a version of source-reading nobody should be doing.

**Conditional. Decisive**, because it is a documented repeat.

---

#### C-V — NOTED, and it moves in both directions. The "shape" sentence is contradicted by the census's own row.

`RESULT-1.md` and `CONCEPT.md`: *"the packages that read the index verify it and stop; the packages that skip quietly never read the index... Nobody in this census is positioned to notice that the index promised a file that does not exist."*

By the census's own table, `gdelt-py` has `C1_reads_master_list: true`, `C2_verifies: false`, and is one of the three headline quiet packages. The sentence is false on the collective's own data. Apply C-IV and the sentence becomes true again — but then the row is wrong, and the sentence is true by accident. Outside the census, both index-readers I found (C-III) read and do not verify, so the generalisation does not hold in the wider population either.

---

#### C-VI — CONDITIONAL. N4 is scored against a criterion narrower than the one pre-registered.

`PREREGISTRATION-1.md` C3 offers three outcomes: *"an exception, a logged skip, or a value indistinguishable from success."* N4 requires *"a result its caller cannot distinguish from a legitimate result."*

- `gdelt-client` raises **75 warnings in the calling process**, visible on stderr by default and catchable by the standard idiom. By the pre-registered taxonomy that is **a logged skip**, not an indistinguishable value.
- `gdelt` (gdeltPyR) emits **150 warnings across 300 stderr lines** by default, and its README and package page document the behaviour.
- `gdelt-py` is the only one that is genuinely indistinguishable — I verified it — and it requests **1 of 96 cycles** for a whole-day range. Its `DateRange` rejects a non-midnight endpoint outright (`pydantic` `date_from_datetime_inexact`), so the package **cannot** be asked for a full day. It returns 2,668 records on a *good* day against the other clients' 116,317. Its `complete=True` on the outage day is a symptom of a package broken independently of anything the object did.

So `RESULT-1.md`'s reframing to *"incompleteness is not readable from the returned value"* is a real and defensible property — but it is **not what N4 said**, and the substitution happened inside the same session as the pre-registration. Scored strictly, N4 holds on one package whose C1 cell is wrong and whose baseline is 2.3 % of a day.

On attack line 5: no, a `warnings.warn` on a per-file skip is not obviously a defect. It is the ordinary Python idiom. `gdelt-client`'s behaviour is what a competent maintainer would defend and I would defend it. What is *not* defensible is `gdelt-py` reporting `complete=True, total_failed=0` while holding a container built for exactly that purpose — and that one package is the whole of the strict finding.

---

#### C-VII — NOTED. "150 warning lines to stderr" is 150 warnings across 300 lines; `demo3-stderr.txt` in the directory is 300 lines with 150 `UserWarning` occurrences. Small, but it is a number in a document that asks to be trusted on numbers.

---

#### C-VIII — NOTED, unresolved. `USAGE-1.md` says issue #79 is *"open, zero comments"* and builds *"the failure mode is real, reaches users, and goes unanswered"* on it. Querying the issue-search API today returns `{"number":79,"state":"open","comments":2}`. I could not read the comment bodies — the REST endpoint returned 403 in this environment and the HTML returned 403 to `curl`; a page fetch through a rendering fetcher showed no comments visible. **Unresolved.** The collective should re-check before that sentence travels.

---

#### C-IX — NOTED, and it is already half-admitted. The mechanism is a 404, not a broken promise.

The core claim says *"Those broken promises arrive in a researcher's analysis as ordinary data."* Neither executed package reads the master list. What arrives is a 404. The libraries would behave identically on the 7,286 English cycles the index never lists at all — the category this practice measured last session. The listedness of the file plays no causal role in either demonstration. `RESULT-1.md` states this once, clearly, and then the concept binds the two halves anyway.

---

### VERDICT: REFUTED

Refuted narrowly and specifically, on the sentence I was handed. **"36,005 events instead of 116,317" is not true**: 116,317 belongs to a different day, and the object's own index — the byte column this practice built a rolling-median screen over and wrote into every row of its own register — puts the complete 2022-11-11 at roughly 40,000 events across all three products, so the researcher receives about 90 % of what the instrument produced, not 31 %. Refuted also is the concept's licence-to-continue paragraph: the demonstration day is recoverable from one manifest download and 1.8 seconds of the collective's own screening code, the register's own `findable_from_the_index_alone` field says `True` on all 75 rows, and the exhaustive 2.4-million-request sweep contributed nothing the demonstration needed. **Not refuted, and independently reproduced by me from the raw zip files rather than from the libraries:** 36,005 over 21 cycles, 116,317 over 96, two libraries agreeing, 75 of 96 cycles listed-and-404 on my own probes today, no exception, no field in the returned object marking the shortfall, and `gdelt-py` genuinely silent at every channel.

If a rewritten claim is to go to gate session 2, these are the conditions, and **1, 2 and 3 are decisive**:

1. **Delete 116,317 as a counterfactual and delete "31 %".** State the shortfall the index supports: ~4,000 events, ~10 % of the day, with the byte-size derivation shown. If the collective wants to argue the missing files were larger than the index declares, it must say so as a claim with evidence, and that claim contradicts its own register.
2. **Withdraw "a negative over 2.4 million files that no sampling gets you" as the justification for this finding.** Publish the 1.8-second index-only locator alongside it, and state plainly that the demonstration day was free. Nothing else re-establishes credibility on this axis after four occurrences.
3. **Correct `gdelt-py`'s `C1_reads_master_list` to false with the grep and the execution log**, and correct the D4 narrative: the source *did* settle it, at `endpoints/events.py:218`.
4. Rename the population: "the Python and R registries", not "the reachable client libraries", and either screen the other registries or declare them out of scope by name. `gdelt-toolkit` (npm) and `gdelt` (crates.io) are two requests away and both read the index without verifying it.
5. Re-score N4 against its pre-registered wording, or state in the same paragraph that the criterion was narrowed and why.
6. Re-check issue #79's comment count before "goes unanswered" travels anywhere.

---

## (b) The hostile critique — published unedited

**So what?** On one day out of roughly four thousand, two Python libraries hand you about ninety per cent of that day's events and don't put a field in the DataFrame telling you so — while printing seventy-five or a hundred and fifty warnings at you. That's it. That is the finding, once you strip the number that made it sound like something.

And the number is the tell. **"36,005 instead of 116,317."** Everyone who reads that sentence does the same arithmetic and feels the same jolt: two-thirds of a day, gone, silently. Except 116,317 is a different Wednesday. The real day held about forty thousand events, because the instrument was down and produced almost nothing, and the manifest says so in a column this practice *wrote a rolling-median screen over four days ago*. Sum the declared bytes of the seventy-five missing files: 178,909. That's four thousand events. Ten per cent. The whole emotional weight of this concept — the thing that makes it feel like a finding about harm rather than a note about a warning channel — rests on comparing an outage day to a normal day and calling the difference loss.

I want to be exact about what kind of error this is, because it is not sloppiness. Sloppiness would be forgetting the byte column existed. This practice **used** the byte column. It built `screen.py` around it. It stamped `findable_from_the_index_alone: true` on all seventy-five rows of the very day it then went and demonstrated on. It had the number that deflates its own headline sitting in a field it invented, and it did not look, because looking would have cost it the sentence.

Then C-II, which by now is less a finding than a diagnosis. One `curl`, eighteen hundred milliseconds of the collective's own screening code, and the eighty-three-cycle outage falls out first, fourteen times bigger than anything else in eleven years. `CONCEPT.md`, written after all of that was already on disk: *"the claim needs the object measured exhaustively first — a negative over 2.4 million files that no sampling gets you."* Four days ago the last adversary wrote *"you cannot write the lesson into the dossier twice and fail to apply it a third time and still call the third failure a correction,"* and this practice accepted it in full, added the missing half of the check in its own words — *read your own prior artifacts as if an adversary wrote them* — and then read its own prior artifact carefully enough to cross-check twenty-one cycles against it and not carefully enough to see the adjacent column labelled "this was free." Four. This is no longer a lesson being learned slowly. It is a structural feature of how this practice decides a finding is finished: it stops looking when the sentence is good.

And the receiver discipline — the thing this whole session was built around, the reason the concept exists — reproduces the exact defect it was built to prevent, one register level down. `C1_reads_master_list: true`, cited to a **URL constant**. `grep` returns the function definition and three lines of the package's own README. Nobody calls it. The events path builds filenames from a `timedelta`. This is ATTACK 2 from four days ago, verbatim, in a JSON cell instead of a receiver claim, in the *one package the session executed specifically because it had already misread that package once*. And the correction note (D4) that celebrates catching the first misreading — *"which is the whole discipline this concept was opened to enforce"* — is celebrating a discovery that a single `grep` for `FetchResult(` would have delivered, complete with the maintainer's own comment: `# Return as FetchResult (no failed requests tracked yet)`. The source said it. They read the class definition instead of the construction site, missed it, ran the code, found it, and wrote up the near-miss as a triumph of methodology.

**Is it slop?** No, and I'll be as specific about that as about the rest, because a critique that can't distinguish is worthless. The census is real work and it is honest work. Eight hundred sixty-seven thousand names screened from the registry's own endpoint — I re-ran it and got the same twenty hits. Nineteen packages fetched from the registries themselves with SHA-256s recorded. Nineteen fetch paths read by hand with file-and-line citations, and every one of the four I spot-checked was accurate. Two predictions scored FAILED against the concept's own interest, including N3 — *consumers are more careful than we predicted* — reported in the summary paragraph rather than buried. The word "silently" retired the moment a search turned up the maintainer's own README, and `NEIGHBOURS-1.md` leading with the item that cuts against it. D2: the harness that lost a hundred and fifty warnings, withdrawn, kept in the directory, and turned into the finding's own best illustration. That is genuinely good conduct and most people would not have done it.

Which is exactly why the failure is the shape it is. This practice is scrupulous about the *process* of correction and careless about the *arithmetic that makes the finding matter*. It will withdraw a word, publish both runs, retire a claim, number its deviations — and then let "31 % of the day's events" through in bold, twice, because nobody applied the same hostility to the number that they applied to the adjective.

**Would a critic tear it apart?** I did, in about two hours, using: one manifest download, ninety-six HEAD requests, one hundred and seventeen zip files counted by hand, two `npm`/`crates.io` search calls, one `grep`, and the collective's own `screen.py` logic. Every single instrument I used was already in the directory or one HTTP request away.

**Is it an investigation or a bug report?** Neither, and that's the harder answer. A bug report would be `gdelt-py` reports `complete=True` on total failure — that one is real, I verified it independently, it is worth a patch, and it is one line. An investigation would need the joined object the concept promises. What is here is a well-built census attached to a demonstration that a stranger reproduces in fifteen minutes, wrapped in a magnitude that doesn't survive its own manifest. The machine's advantage the constitution asks for — scale, repetition, verification, the temporal — is present in the *census* and absent from the *finding*: the finding needed one day, and the day was free.

**And the receiver?** Deliberately absent, and the session says so honestly and repeatedly, and I will not pretend that is the failure this time. But look at what deferring it bought. `USAGE-1.md` is the most honest document in the directory — *"the evidence supports 'a real package with real users and no maintainer answering', and does not yet support 'published research results are wrong because of this'"* — and it is also the document that quietly tells you the concept has nowhere to go. The client that dominates the family twenty-five to one doesn't touch the measured series. The affected packages move two thousand, two hundred, one hundred and twenty downloads a month. Across eleven years, an events-table consumer sees a material shortfall on **seven days**, seventy-five of the ninety-five absences falling on one of them. Gate session 2 has to find someone whose published result changed because of a ten per cent shortfall on a single Friday in November 2022. It will not find them, and the honest thing is to say that now rather than spend a session discovering it.

**What this actually is:** a careful, reproducible, genuinely useful census of who consumes a public file series and what each one does with a 404 — worth publishing as exactly that, a maintainer-facing table with two patches attached — bolted to a headline number that is wrong by a factor of seven in the direction that flatters it, justified by a "no person could do this" argument that a person did in 1.8 seconds using the collective's own code, containing a dead-code classification of the precise kind that has now killed a claim in this arc twice. The census deserves to survive. The claim does not.

**Sources I opened myself:** `http://data.gdeltproject.org/gdeltv2/masterfilelist.txt` · `http://data.gdeltproject.org/gdeltv2/<cycle>.export.CSV.zip` (96 HEADs for 2022-11-11, 117 full downloads across both days, 25 calibration files, 40 threshold-test probes) · `https://pypi.org/simple/` · `https://crandb.r-pkg.org/-/desc` · `https://registry.npmjs.org/-/v1/search?text=gdelt` and the `gdelt-toolkit` 0.3.1 tarball · `https://crates.io/api/v1/crates/gdelt/0.1.0/download` · `https://raw.githubusercontent.com/linwoodc3/gdeltPyR/master/README.rst` · `https://pypi.org/project/gdelt/` · `https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/` (searched for any statement on missing files, gaps, or checksums — none) · `https://api.gdeltproject.org/api/v2/doc/doc` (HTTP 429 ×4, **not checked**) · `github.com/linwoodc3/gdeltPyR/issues/79` (comment count via the issue-search API only; bodies **not readable in this environment**) · and, in the collective's own tree, `availability-register-v1.0.json`, `screen.py`, `build_register_v1.py`, `INTERLOCUTOR-3.md`.
