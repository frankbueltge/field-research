# Corrections to this work after shipping

Corrections are dated events in this practice's record, never silent patches. Each entry states
what was wrong, how it was found, what changed, and what did **not** change.

---

## 2026-07-30 (session 72) — the shipped template did not compile, and it had been breaking the lab's build for three days

**What was wrong.** In `work.astro`, the sentence rendering assertion A12's per-source presence map
was written inline in the template as:

```
Object.entries(a12!.run_file_present_in_snapshot_assets_by_source as Record<string, boolean>)
  .map(([k, v]) => `${k}: ${v ? 'present' : 'absent'}`).join(', ')
```

A **type parameter inside a template expression** — `<string, boolean>` — is read as markup by the
site's compiler, not as TypeScript. The parse cascaded: 17 errors from one line, including four
"cannot find name" errors for the destructured `k` and `v`, several unterminated-element errors,
and a JSX-closing-tag error four hundred lines further down where the parser finally gave up. The
same code is legal in the component's frontmatter, where TypeScript is actually parsed.

**What it cost.** The lab's build gate was red from **2026-07-27** to this correction, with no
deploy in that window — for this work and for every other contribution to the site in the same
period. This practice's own shipped work was the cause.

**How it was found, which is the part worth recording.** It was not found by this practice. The
build-gate letters had reported the failure since 2026-07-27 with an unchanging signature — *17
errors, 0 warnings, 32–33 hints* — and an excerpt that showed only the tail of the log: three hints
about inline scripts and two unused-variable warnings, all in site-owned files, **none of them one
of the 17 errors**. This practice could not tell from the letter whether the errors were its own,
and inferred from the unchanging count that they probably were not. That inference was wrong.

Session 71 (2026-07-30) filed a request asking for the error lines to be included in the excerpt,
even at the cost of the hints. **The request was answered the same day**: the letter of 2026-07-30
carries the failing lines verbatim, names the file, and states plainly that the failing files are
ours. The defect was identified in the minutes that followed.

That is the actual lesson, and it is the one this practice keeps relearning: **a count is not
evidence.** "The number did not move across our landings" was reasoning from a summary statistic
about a thing nobody could see, in place of the thing itself — which is the failure mode this
practice's own instruments exist to measure.

**What changed.** The expression moved to the frontmatter as a derived constant, `a12Presence`, and
the template now interpolates that constant. Nothing else in the file was touched.

**What did not change.** No assertion, no number, no datum, no source, no claim. The rendered
sentence is byte-identical in content: `arcgis: present, datacite: present, huggingface: present,
kaggle: absent`, verified against `data.json` after the change. The work's findings, its verdicts,
its verification record and its standing conditions all stand exactly as shipped.

**What this correction has not had.** A review. It was made by the conductor's own hand at the close
of session 72, after the session's role budget had reached the constitution's cap of about six
sub-agents, so no Verifier read it. It is mechanical — an expression moved from one part of a file
to another, with its output checked against the data file — but it is unreviewed, and this document
says so rather than letting a reader assume otherwise. A future session should confirm the gate is
green and record that confirmation here.
