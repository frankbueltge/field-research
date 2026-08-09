# Pre-registration — increment 2: opening the collapse arm at scale

**Written and committed 2026-08-09 (session 104) before any file was downloaded and before the
manifest was re-fetched.** Nothing below is revised after a number exists. Predictions that fail are
reported as failed, in this table, with the number that failed them.

## Why this increment, and what it decides

`CONCEPT.md` names increment 2 exactly: *open collapsed cycles at scale and convert the byte-size
screen into a measured record-count series.* `INTERLOCUTOR-1.md` §(a).5 voided the concept's named
receiver, and the response accepted the condition: the rebuild must rest on **what a
manifest-reading consumer does not get for free.**

That phrase is the whole difficulty, and it is why this increment is designed the way it is.
GDELT's published manifest gives every consumer three things per file: the URL, the byte size, and
an MD5. Therefore **the outage arm is derivable from the manifest** — anyone can subtract the file
list from the 15-minute grid. **And so is the collapse screen**, because the screen is a function of
the byte sizes the manifest publishes. If everything this arc measures is a view of one public text
file, the register is a convenience, not a counter-measurement, and the concept should die.

So the load-bearing question of this increment is not *"is the screen right?"* — it is:

> **Does the byte size a consumer can read in the manifest tell them what is inside the file?**

Four things could be true and none of them is readable from the manifest: a file's contents may not
match its size; a file's MD5 may not match what is published for it; a listed file may not exist; a
normal-sized file may republish the previous cycle rather than report a new one. Each has a
prediction below, and one of them (Q4) has no expected direction at all.

## The kill criterion, written so it can fire against us

**If Q1 holds and Q4, Q6 and Q7 all fail and Q5 holds at 100 %, then everything this arm measures
was already computable from the published manifest.** In that case the phrase *"an absence that
answers HTTP 200"* describes something a consumer can see for free, the collapse arm cannot carry
the receiver, and gate session 3 either rebuilds the receiver on the verification arm alone or
discards the concept with a one-page finding. This outcome is on the table and is not a failure of
the session.

## The sampling design, fixed here

Random draws use Python's `random.Random(20260809)`, seeded once, drawing the samples in the order
A, C, D below, so the draw is reproducible from this file alone.

The flag sets come from increment 1 and are not recomputed: `collapses.json` (3,137 cycles, the
pre-registered trailing-median screen) and `rescreen-english.json` (3,136 cycles, the independent
same-minute-of-day screen). **"Flagged" means flagged by either screen; "unflagged" means flagged by
neither.** All samples are on the English GKG series only.

- **Sample A — collapsed, 80 cycles.** Drawn from the **intersection** of the two screens (the 3,125
  cycles both methods flag), stratified by calendar year: every year present in the intersection
  contributes at least 4 cycles or all it has, whichever is smaller; the remainder is drawn
  proportionally.
- **Sample B — matched controls, up to 80.** For each cycle in A, the **nearest preceding unflagged
  cycle present in the manifest, within 7 days**. If none exists, the pair is reported as unmatched,
  never substituted from elsewhere.
- **Sample C — random unflagged, 80 cycles.** Drawn uniformly at random from all unflagged cycles
  present in the manifest across the whole series. This is the sample Q4 is scored on.
- **Sample D — consecutive unflagged pairs, 30 pairs (60 cycles).** A cycle t is drawn uniformly at
  random such that t and t+15 min are both present and both unflagged.

**Truncation rule, committed in advance.** If measured throughput or a host limit makes the full
draw impossible inside this session, each sample is truncated **in its pre-registered draw order**,
the number actually measured and the number lost are both reported, and nothing is imputed. This is
the rule increment 2 of the previous arc ran under when a third-party host cut it off; it is
restated here before it is needed.

**What is measured per downloaded file.** HTTP status · bytes received · MD5 of the bytes received ·
whether the zip opens · the byte length of the inner CSV · the number of records (lines) in the
inner CSV · for sample D only, the set of values in the GKG `DocumentIdentifier` column. Files are
counted in memory and never kept.

## Predictions

| | prediction | why it is worth writing down |
|---|---|---|
| **Q1** | **Screen validity.** ≥ 90 % of sample A cycles that download successfully hold **< 20 %** of the record count of their own matched control (sample B). | If the byte screen does not predict the record count, increment 1's third pattern was an artifact and must be withdrawn. |
| **Q2** | **The zero class.** ≥ 5 % of sample A are valid archives whose inner CSV holds **0 records**. | Increment 1 found two by hand out of six. Whether that rate survives at scale is unknown. |
| **Q3** | **The calibration does not travel.** Median **records per megabyte** among unflagged cycles differs by a factor **≥ 2** between the earliest and the latest year measured. | If true, no fixed byte threshold identifies a degraded file across the series, and the screen a consumer could build for themselves is era-specific. |
| **Q4** | **The converse — no expected direction.** At least one of the 80 randomly drawn **unflagged** cycles holds a record count below **20 %** of what its own byte size predicts (its year's median records-per-megabyte × its megabytes). | This is the receiver's whole case: a file whose size looks ordinary and whose contents do not is invisible to every manifest reader. We do not know whether such a file exists. |
| **Q5** | **Integrity.** ≥ 99 % of all successfully downloaded files match **both** the manifest's byte size and its published MD5. Every mismatch is reported individually. | The manifest's MD5 is a promise nobody checks at scale. |
| **Q6** | **Duplication.** In ≥ 1 of the 30 consecutive unflagged pairs, ≥ 50 % of the later cycle's `DocumentIdentifier` values already appear in the earlier one. | A cycle that republishes its predecessor has a normal size, a normal record count, and no new information. Nothing in the manifest could show it. |
| **Q7** | **Listed but absent.** ≥ 1 file listed in the manifest fails to download (HTTP error or truncated body). | Increment 1 probed 40 entries and found 40 present. At 300 entries this may simply not fire. |
| **Q8** | **The published past is stable.** The manifest re-fetched today reports byte sizes **identical** to yesterday's for **all 3,137** cycles flagged by the pre-registered screen. | If the manifest's account of the past changes between two days, every measurement anyone has ever taken from it is dated, including ours. |

## What this increment cannot decide

1. **Record count is not record quality.** A cycle with a normal record count may still hold a
   degraded or duplicated sample; only Q6 looks past the count, and only on 30 pairs.
2. **One series.** English GKG only. Nothing here speaks for the Translingual stream, the events
   files, or GDELT's other series.
3. **Now, not then.** Every file is fetched today. A file that was absent or corrupt in 2017 and was
   repaired since reads as healthy here, and this instrument cannot see the difference.
4. **The receiver is not decided by a number.** Even if Q4 and Q6 fire, whether a real named party
   outside this house can use the result is a separate question, answered by search and judgement,
   not by this table.
