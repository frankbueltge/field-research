# Codebook — reading 89, after the presentation (session 287, 2026-11-21)

*Fixed before any diff or blame was run for this reading and before the Atelier's per-pair codes were opened (see
`PREDICTIONS89.md`). Decidable by script from Git alone; no reader codes anything.*

**Units.** The 77 deeds of `credit88.json` with a recorded mending (`repair_found`), each with its deed commits and its
mending (`repair_hash`, `repair_repo`), exactly as reading 88 recorded them.

**Where.** Full bare clones of the seven repositories reading 88 used, as GitHub serves their default branches on
2026-11-21. The site's clone omits blobs over 2 MB, which git fetches on demand. A deed's commits are the commits
reading 88 lists for it; where one of them is a merge, the commits it brought in (`D^1..D`) count as the deed's too.

**Lines a mending takes out.** The lines its diff against its first parent removes or rewrites (`git diff -U0`, every
`-` line), per path. A removed line belongs to the deed when `git blame` at the mending's first parent attributes it to
one of the deed's commits.

**Codes, per pair, in this order of precedence (the first that applies is the pair's class).**

| code | rule | class for P144 |
|---|---|---|
| `same_commit` | the mending is one of the deed's commits | joined by Git |
| `lines` | the mending takes out at least one line that belongs to the deed | joined by Git |
| `name` | reading 88's `names_deed` is true (hash prefix or pull-request number) | joined by Git |
| `file` | the mending changes a path that one of the deed's commits changed, in the same repository | a file only |
| `log_only` | none of the above | the log alone |

Every pair is also coded on each rule apart, so a pair joined by lines and by name is reported under both.

**From the deed alone (`git_points`, for P145).** For a pair coded `lines`: the commits that lie after the deed and
before the mending (`git rev-list` from the deed's latest commit to the mending's first parent, merges excluded) and
change a path the deed changed. Each is a candidate *earlier heir*: it counts when at least one line it takes out
belongs to the deed, by the same blame rule at its own first parent. A first pass keeps only candidates that remove a
line whose text equals a line one of the deed's commits added; only those are blamed. `git_points` is true when no
earlier heir is found: an outsider who follows the deed's lines forward meets the mending first. `heirs_before` counts
the earlier heirs.

**Agreement (P144).** Only after every pair is coded, the Atelier's `data/sort.json` at ulysses `aa8a96e` is opened and
each pair's class compared by deed and mending. Agreement is reported as a count of 77 and as Cohen's κ over the three
classes; every disagreement is listed with both codes and read for its cause.

**Reported.** Counts, not estimates: the 77 are the pairs the log holds, not a sample. Each prediction also without the
five mendings read before reading 88's predictions (`SEEN_BEFORE` in `credit88.py`).

**Addendum during the run (2026-11-21, written before any pair's code was seen).** Three rules of the procedure changed
after two runs were stopped for speed, each before the script had printed a single pair: (1) blobs the site's clone
lacks (over 2 MB) are never fetched, so a path whose diff or blame needs one is *unread* for that pair and listed in
`unread_paths`; (2) the earlier heirs are searched oldest first and the search stops at the first, so `heirs_before` is
0 or 1 and P145 is decided by it unchanged; (3) in that search the text pre-filter keeps only lines with at least one
letter or digit, so an earlier commit that took out only blank or bracket lines of the deed is not counted as an heir.
The class codes and P144 are untouched.
