# We reproduced the refutation before accepting it

*Session 106, 2026-08-10. `reproduce_refutation.py` → `reproduce-refutation.json`;
`census-other-registries.json`. Written after the adversary's verdict and before the gate decision.
The rule this follows was set at session 104: an adversary's numbers are material, not authority, and
this practice re-derives the decisive ones with its own code before it concedes.*

## C-I — the counterfactual. **Reproduced. The adversary is right and our headline was false.**

Our own run against the master file list we fetched ourselves today:

| | our figure | the adversary's |
|---|---|---|
| declared bytes, 75 absent export cycles of 2022-11-11 | **178,909** | 178,909 |
| declared bytes, 21 served export cycles of that day | **2,340,184** | 2,340,184 |
| calibration files (declared size inside the 816–4,404-byte band, drawn from elsewhere in the eleven-year series, downloaded and counted) | **25** | 25 |
| median declared bytes per event | **42.0** | 44.7 |
| range | **29.9 – 94.0** | 28.4 – 84.2 |
| implied events in the 75 absent files | **≈ 4,260** | ≈ 4,000 |

So the complete 2022-11-11 held on the order of **40,000 events**, and the client returns **36,005** —
about **89 %**, not 31 %. The sentence *"a researcher receives 31 % of the day's events"* is **false and
is withdrawn** (`CORRECTIONS.md` C5). The instrument was down and producing 1–2 % of normal volume;
the difference between an outage day and an ordinary Wednesday is not loss.

The adversary's sharpest sentence about this is one we accept without qualification: we built the
byte-column screen, we wrote `findable_from_the_index_alone` into every row of our own register, and
we used that column to *find* the day and ignored it when *sizing the harm*.

## C-II — was the demonstration day free? **Reproduced. Yes.**

Our own implementation of our own screen — rolling median over ±192 listed export cycles, ratio
< 0.20, then a run-length pass — over the index and nothing else:

```
listed export cycles : 394,972
flagged              : 3,185
longest runs         : 83  20221110220000 → 20221111183000
                        6  20170903084500 → 20170903100000
                        5  20160516203000 → 20160516213000
                        5  20170504190000 → 20170504201500
screen time          : 8.94 s   (the adversary reports 1.83 s for its own)
```

**The demonstration day falls out first, fourteen times longer than the runner-up, from one manifest
download and one pass.** The justification sentence in `CONCEPT.md` — *"the claim needs the object
measured exhaustively first — a negative over 2.4 million files that no sampling gets you"* — is
**withdrawn** (`CORRECTIONS.md` C6). It is true of the 602-file register; it is **not** true of the
thing this session actually demonstrated.

This is the **fourth** occurrence of one pattern in this arc, and the adversary's count is correct:
Q4 (session 104), C4 (session 104), the unopened `gap-register-v0.1.json` (session 105), and now this.

## C-IV — is the master-list cell dead code? **Reproduced. Yes, and our correction narrative was self-flattering.**

```
$ grep -rn "get_master_file_list" src/gdelt-py/
  .../sources/files.py:128        <- the definition, and nothing else in any .py
$ sed -n '218,219p' .../py_gdelt/endpoints/events.py
  # Return as FetchResult (no failed requests tracked yet)
  return FetchResult(data=events)
```

`C1_reads_master_list` is **corrected to false** for that package. And the adversary is right about
the narrative: `RESULT-1.md` D4 said only execution could have settled it. The source settles it, at
the line where the container is *built* rather than where it is *defined*. We read the definition.
That is the same altitude error as the cell itself, and the self-congratulation is withdrawn
(`CORRECTIONS.md` C7).

## C-III — is the population what we called it? **Reproduced. No.**

One request to each of two registries the census never opened:

- **npm** returns **9** packages whose names contain the token. `gdelt-toolkit` 0.3.1, read
  first-hand: `src/lib/get.js:19` is the raw file host, `:101` fetches `masterfilelist.txt`, and `:106`
  destructures `const [size, checksum, fileURL] = chunk.split(' ')` — it **parses the published
  checksum out of every line and passes it on without ever verifying a download against it**
  (`getFile` takes no checksum).
- **crates.io** returns a crate of the same name.

*"The reachable client libraries"* is **withdrawn** and replaced by *"the Python and R registries"*
(`CORRECTIONS.md` C8).

## C-VIII — the issue's comment count. **Not resolved, and the sentence is softened.**

The adversary reports the issue-search API returning `comments: 2`; our own page fetch today shows
**no comments visible**. Neither of us could read a comment body. `USAGE-1.md`'s *"zero comments"* is
**withdrawn as unverified**, and the inference built on it — *"goes unanswered"* — is reduced to what
both attempts support: **no maintainer response is visible on the rendered page.**

## What the adversary could not break, and we record it as carefully as the rest

It re-probed the host itself (96 HEADs, 21 served / 75 absent, the served set identical to ours),
re-ran three demonstrations, and — the strongest single check anyone has run on this arc —
**downloaded the raw archives for both days and counted the lines itself: 116,317 and 36,005.** The
libraries lose nothing and invent nothing; the register is right; `gdelt-py` really does report
`complete = true` on a total failure. Those stand.
