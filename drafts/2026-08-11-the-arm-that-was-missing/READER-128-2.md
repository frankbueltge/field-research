# Severed reader 2 — full answer, unedited

*Session 128, 2026-08-20. Entry point: the bare directory listing, with an instruction to choose
its own first file and to assume nothing was the entry point. Severing conditions: `READERS-128.md`.
Nothing below is edited, reordered or cut.*

---

# Reading of `/copy-2`

## 1. The single most important thing this directory tells you
A public dashboard that is supposed to daily-check the availability of a fixed set of TikTok videos stopped updating on 2026-01-14 and has shown all 11 tracked videos as "Error" since a state change on 2026-01-03, yet an independent check this morning found 10 of those 11 videos still publicly fetchable.

## 2. What is it about?
It's an open letter (`LETTER.md`) addressed to the operator of a specific public page (`playground.tiktok-audit.com/api-na/`, tied to a cited AI Forensics arXiv paper about TikTok's research API), arguing from the page's own saved data that its displayed "all errored" tiles describe a frozen January snapshot rather than the present. The rest of the directory is the entire supporting apparatus for that claim: the saved dashboard HTML, the code that extracts and cross-checks its per-video series, the independent retrievability probe and its output, and a build log tying every claimed number to a command that was actually run.

## 3. Who is it for, and who is it from?
It's addressed to whoever runs that dashboard ("your dashboard," "your record," "your own server"). It's attributed to "Meridian," described in the letter as "an autonomous research practice" that did the measuring and writing, with a named human, Frank Bültge, stated as the one who "publishes it and carries responsibility for it" and who decides whether it is ever sent. The letter says explicitly: "Nobody has been contacted and it has not been sent."

## 4. What would you not trust, or want to check yourself?
- Two figures the letter leans on (re-request counts, the daily series' length) are stated to come from a ledger not included in this directory — only in an external GitHub repo named in the letter. I can't verify those from the directory alone.
- The independent measurement is one machine, one morning, three dated reads — the letter itself says this "is not a sample of anything" and cannot distinguish a broken checking pipeline from a genuinely broken research interface.
- The measuring tool's own file (`presence_check.py`) documents a rough history: an earlier version was "withheld" at an internal review ("gauntlet"), a later one "failed its own gauntlet," and a bookkeeping defect ("frozen-reference drift") had to be measured and separately repaired. That doesn't make the current numbers wrong, but it means this instrument has a track record of needing correction, by its own account.
- The 5x-reconfirmation rule used to validate "not retrievable" readings is explicitly flagged by the tool's own documentation as unvalidated: "not claimed to be the right test, only the pre-registered one."
- I did not re-run any of the code myself, so everything here is a claim the directory makes about itself, not something I independently reproduced.

## 5. Where, if anywhere, did you stop reading or want to stop?
I stopped short of reading the full 246KB dashboard HTML and the full-length JSON series/code files line by line — once the extraction, the cross-check against the page's own aggregate chart (837/837 comparisons agreeing), and the independent probe output were internally consistent with the letter's numbers, further line-by-line reading of the same data seemed to add confirmation rather than new understanding. The place I most wanted to stop and go elsewhere was the letter's own pointer to the external ledger/GitHub repository — that's where two of its cited figures actually live, and this directory can't settle them on its own.

## 6. Anything you noticed that nobody asked you about
The directory has an unusually heavy internal-accounting culture for what is, on its face, a short letter: a strict prose word cap (1097/1100 words), a build log that reruns every cited command twice (once to produce figures, once "from scratch" as a reproduction check) and hashes every shipped file, and references throughout to numbered "sessions," a "gauntlet" review process, an "erratum," and pre-registration documents. It reads like output from a disciplined, self-auditing research pipeline rather than a one-off note. Separately, the letter and the tool both flag, unprompted, that running the probe yourself discloses your machine's IP address to a third-party lookup service unless you pass a flag to suppress it — that's disclosed plainly rather than buried.
