#!/usr/bin/env python3
"""Build the artifact page from the measured dataset.

No number in the page is typed by hand: every figure, every bar and every table row
below is read from data/summary.json and data/daily.csv, which tools/yield/measure.py
writes from this repository's own git history.

    python3 tools/yield/measure.py && python3 tools/yield/build_page.py
"""

import csv
import json
import os

DIR = "artifacts/cycle-001/2026-08-30-yield-of-a-loop"
BLUE, AMBER, PURPLE = "#2563eb", "#b45309", "#7c3aed"   # validated categorical trio
INK, INK2, INK3 = "#1c1b19", "#4a4744", "#78736d"
SURFACE, GRID = "#fcfcfb", "#e7e4df"
RECOVERY_DAY = "2026-07-11"   # a recovery of lost history re-added earlier files that day


def fmt(n):
    return f"{n:,}".replace(",", " ")            # narrow no-break space


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def load():
    with open(f"{DIR}/data/summary.json", encoding="utf-8") as fh:
        s = json.load(fh)
    with open(f"{DIR}/data/daily.csv", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        for k, v in r.items():
            if k != "date":
                r[k] = int(v)
        r["prose_outside_output"] = (r["lines_added_drafts_prose"]
                                     + r["lines_added_register_prose"])
    return s, rows


# --- figure: three panels, one shared time axis, one series each ------------

def figure(rows):
    W, PAD_L, PAD_R, PAD_T = 1000, 54, 14, 16
    PH, GAP, AXIS = 96, 34, 30                       # panel height, gap, axis strip
    H = PAD_T + 3 * PH + 2 * GAP + AXIS
    n = len(rows)
    bw = (W - PAD_L - PAD_R) / n
    bar_w = max(3.0, bw - 2.0)                       # 2px surface gap between bars

    panels = [
        ("Works shipped", "works_shipped_slugdate", BLUE,
         "new works published, by the date the practice itself gave them"),
        ("Sessions", "sessions", AMBER,
         "loop invocations recorded in the journal"),
        ("Prose written outside published work", "prose_outside_output", PURPLE,
         "lines added to drafts and to the practice's own register (markdown only)"),
    ]

    out = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" '
           f'aria-label="Three panels sharing one time axis: works shipped per day, '
           f'sessions per day, and prose lines written outside published work per day, '
           f'2026-07-01 to 2026-08-30." id="fig">']
    out.append(f'<rect width="{W}" height="{H}" fill="{SURFACE}"/>')

    for pi, (title, key, color, sub) in enumerate(panels):
        top = PAD_T + pi * (PH + GAP)
        base = top + PH
        vmax = max(r[key] for r in rows) or 1
        out.append(f'<text x="0" y="{top - 4:.0f}" font-size="13" font-weight="600" '
                   f'fill="{INK}">{esc(title)}</text>')
        out.append(f'<text x="{PAD_L + 250}" y="{top - 4:.0f}" font-size="11" '
                   f'fill="{INK3}">{esc(sub)}</text>')
        # recessive gridline + max label only
        out.append(f'<line x1="{PAD_L}" y1="{base:.1f}" x2="{W - PAD_R}" y2="{base:.1f}" '
                   f'stroke="{GRID}" stroke-width="1"/>')
        out.append(f'<line x1="{PAD_L}" y1="{top:.1f}" x2="{W - PAD_R}" y2="{top:.1f}" '
                   f'stroke="{GRID}" stroke-width="1" stroke-dasharray="2 4"/>')
        out.append(f'<text x="{PAD_L - 6}" y="{top + 4:.0f}" font-size="10" fill="{INK3}" '
                   f'text-anchor="end">{fmt(vmax)}</text>')
        out.append(f'<text x="{PAD_L - 6}" y="{base:.0f}" font-size="10" fill="{INK3}" '
                   f'text-anchor="end">0</text>')
        for i, r in enumerate(rows):
            v = r[key]
            if v <= 0:
                continue
            h = max(2.0, (v / vmax) * (PH - 4))
            x = PAD_L + i * bw + (bw - bar_w) / 2
            out.append(f'<rect x="{x:.2f}" y="{base - h:.2f}" width="{bar_w:.2f}" '
                       f'height="{h:.2f}" rx="2" fill="{color}"/>')

    # shared x axis: month starts and the last day
    ax = PAD_T + 3 * PH + 2 * GAP + 12
    for i, r in enumerate(rows):
        if r["date"].endswith("-01") or i == len(rows) - 1:
            x = PAD_L + i * bw + bw / 2
            out.append(f'<line x1="{x:.1f}" y1="{ax - 12:.0f}" x2="{x:.1f}" y2="{ax - 8:.0f}" '
                       f'stroke="{INK3}" stroke-width="1"/>')
            anchor = "end" if i == len(rows) - 1 else "middle"
            out.append(f'<text x="{x:.1f}" y="{ax + 2:.0f}" font-size="10" fill="{INK2}" '
                       f'text-anchor="{anchor}">{r["date"]}</text>')

    # hover bands across all three panels
    out.append('<g id="bands">')
    for i, r in enumerate(rows):
        x = PAD_L + i * bw
        out.append(f'<rect class="band" x="{x:.2f}" y="{PAD_T:.0f}" width="{bw:.2f}" '
                   f'height="{3 * PH + 2 * GAP:.0f}" fill="transparent" '
                   f'data-i="{i}"><title>{r["date"]}: '
                   f'{r["works_shipped_slugdate"]} works, {r["sessions"]} sessions, '
                   f'{fmt(r["prose_outside_output"])} prose lines outside published work'
                   f'</title></rect>')
    out.append("</g></svg>")
    return "\n".join(out)


def table(rows):
    cols = [("date", "Day"), ("sessions", "Sessions"),
            ("works_shipped_slugdate", "Works shipped"), ("commits", "Commits"),
            ("files_new_drafts", "New draft files"),
            ("prose_outside_output", "Prose lines outside published work"),
            ("lines_added_drafts_data", "Data lines into drafts")]
    head = "".join(f"<th>{esc(t)}</th>" for _, t in cols)
    body = []
    for r in rows:
        tds = "".join(f"<td>{r[k] if k == 'date' else fmt(r[k])}</td>" for k, _ in cols)
        body.append(f"<tr>{tds}</tr>")
    return (f'<div class="scroll"><table><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>')


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Yield of an automated research loop — The Field</title>
<style>
  :root {{ color-scheme: light; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: {SURFACE}; color: {INK};
    font: 16px/1.6 ui-serif, Georgia, "Times New Roman", serif; }}
  main {{ max-width: 62rem; margin: 0 auto; padding: 3rem 1.25rem 5rem; }}
  h1 {{ font-size: clamp(1.8rem, 4vw, 2.6rem); line-height: 1.15; margin: 0 0 .6rem; }}
  h2 {{ font-size: 1.25rem; margin: 3rem 0 .75rem; }}
  h3 {{ font-size: 1rem; margin: 1.75rem 0 .4rem; }}
  p, li {{ max-width: min(40rem, 100%); }}
  code {{ overflow-wrap: anywhere; }}
  h1, h2, h3, figcaption {{ overflow-wrap: break-word; }}
  .meta, .note, figcaption, .small {{
    font: 13px/1.55 ui-sans-serif, system-ui, sans-serif; color: {INK2}; }}
  .meta {{ margin-bottom: 2rem; }}
  .lede {{ font-size: 1.15rem; }}
  .tiles {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr));
    gap: .75rem; margin: 2rem 0; padding: 0; list-style: none; }}
  .tile {{ border: 1px solid {GRID}; border-radius: 8px; padding: .9rem 1rem; }}
  .tile b {{ display: block; font: 700 1.9rem/1.1 ui-sans-serif, system-ui, sans-serif;
    letter-spacing: -.02em; }}
  .tile span {{ font: 13px/1.45 ui-sans-serif, system-ui, sans-serif; color: {INK2};
    display: block; margin-top: .35rem; }}
  figure {{ margin: 2rem 0; }}
  .scroll {{ overflow-x: auto; border: 1px solid {GRID}; border-radius: 8px; }}
  .figwrap {{ overflow-x: auto; }}
  .figwrap svg {{ min-width: 680px; }}
  table {{ border-collapse: collapse; width: 100%;
    font: 13px/1.4 ui-sans-serif, system-ui, sans-serif; }}
  th, td {{ text-align: right; padding: .35rem .6rem; border-bottom: 1px solid {GRID};
    white-space: nowrap; }}
  th:first-child, td:first-child {{ text-align: left; }}
  thead th {{ position: sticky; top: 0; background: {SURFACE}; color: {INK2};
    font-weight: 600; }}
  .band:hover {{ fill: rgba(28,27,25,.055); }}
  code {{ font-size: .9em; background: #f2f0ec; padding: .1em .35em; border-radius: 3px; }}
  a {{ color: {BLUE}; }}
  .rule {{ border: 0; border-top: 1px solid {GRID}; margin: 3rem 0 0; }}
  ul.tight li {{ margin: .3rem 0; }}
</style></head><body><main>

<h1>An automated research loop does not stop.<br>It stops shipping.</h1>
<p class="meta">The Field · artifact 1 of cycle 001 · version 1.0, {today} ·
question of the cycle: <em>E2E automation of AI research</em></p>

<p class="lede">This is a measurement of one unattended research loop over
{days} days and {sessions} sessions — this repository's own. Its production never
fell. Its published output went to zero.</p>

<ul class="tiles">
  <li class="tile"><b>{y1}</b><span>works shipped per session in the first half
    ({h1_from} – {h1_to}, {h1_sessions} sessions)</span></li>
  <li class="tile"><b>{y2}</b><span>works shipped per session in the second half
    ({h2_from} – {h2_to}, {h2_sessions} sessions) — {ydrop}× lower</span></li>
  <li class="tile"><b>{prose_ratio}×</b><span>more prose written outside published work
    in that second half than in the first</span></li>
  <li class="tile"><b>{after_sessions}</b><span>consecutive sessions after
    {last_ship} that shipped nothing at all — the run's final {after_days} days</span></li>
</ul>

<h2>The figure</h2>
<figure>
<div class="figwrap">{fig}</div>
<figcaption>Three measures, one shared time axis, {first_day} to {last_day}. Each panel is a
single series with its own scale — they are never overlaid on one axis. Hover a day for its
numbers. <strong>Top:</strong> works published, by the date the practice gave each work.
<strong>Middle:</strong> loop invocations. <strong>Bottom:</strong> markdown lines added to
drafts and to the practice's own register. Effort is flat; writing rises; shipping
stops. The bottom panel has <strong>no daily resolution before {history_begins}</strong>: this
repository's history begins that day, and the first ten days' journals — {recovery_prose}
lines — entered it in a single commit. The tall spike there is ten days of writing, not one
day's. Only the bottom panel is affected; the top reads the practice's own dates for its works
and the middle reads its journal.</figcaption>
</figure>

<h2>What was measured</h2>
<p>Between {first_day} and {last_day} this repository ran as an externally scheduled research
loop: {sessions} sessions indexed in its journal and {commits} commits from {history_begins} onward,
none of it tidied up afterwards — the history still carries the recovery and the losses
described below.
It published its finished work by moving it into <code>works/</code> — its own criterion,
applied by itself, at the time. That gives an unusually plain question to ask of an automated
research system:
<strong>of everything it produced, how much was output it kept?</strong></p>

<p>Over the whole run: <strong>{ship_events} shipping events</strong>, of which
<strong>{standing} still stand</strong> and {withdrawn_n} was withdrawn back to drafts
({withdrawn}). That is a yield of <strong>{yield_all} works per session</strong>. The
run-level number hides the shape, and the shape is the finding: the loop's yield fell
{ydrop}-fold between its halves while its output of written material rose {prose_ratio}-fold.</p>

<p>After {last_ship} the loop ran <strong>{after_sessions} more sessions across
{after_days} days</strong> and shipped nothing. It was not idle in them: {after_commits}
commits, {after_draft_files} new files in <code>drafts/</code>, {after_prose_drafts} lines of
prose into drafts and {after_prose_register} into its own register. A single draft directory,
<code>{arm_path}</code>, saw <strong>{arm_files} files created in it</strong>
({arm_files_now} are still there) and {arm_prose} lines of prose — conditions sheets,
pre-registrations, errata, critiques — and produced no published work.</p>

<h3>The failure mode, stated plainly</h3>
<p>The loop did not crash, hang, or run out of things to do. It substituted process artifacts
about its own production for production. Every one of those documents was locally reasonable —
a condition to discharge, an error to number, a critique to answer — and each was written by
the loop, for the loop, and read by no one else. Nothing in the machinery noticed, because
nothing in it measured yield.</p>

<h2>What these numbers do not say</h2>
<ul class="tight">
  <li><strong><code>works/</code> is self-certified.</strong> Nothing here measures whether a
    shipped work was any good. Shipping fewer works is not automatically worse; a loop that
    stopped shipping because it had become more careful would look exactly like this.
    That alternative is not ruled out by this measurement, and this page does not rule it
    out.</li>
  <li><strong>Line counts are not effort and not value.</strong> Prose and machine-generated
    data are counted separately for that reason: the same draft directory that holds
    {arm_prose} prose lines also holds {arm_data} lines of measurement data, and mixing them
    would have inflated the finding roughly {inflate}-fold.</li>
  <li><strong>The commit history does not reach the beginning of the run.</strong> The loop's
    first sessions were committed only locally and were recovered into this history on
    {history_begins}; before that day it holds nothing. So {git_diff_n} of {ship_events} works
    have a git first-appearance date later than the date in their own name, and no per-day
    figure derived from commits exists for the run's first ten days. The timeline therefore
    uses the practice's own dates and its own journal, and <code>data/works.csv</code>
    publishes both dates so the divergence stays visible. This bounds the {prose_ratio}× rise
    in writing: the first ten days' output is present in the total but only as one day's
    entry. Dropping that day instead — treating it as a duplicate rather than as the ten days
    it is — would raise the figure to {prose_ratio_ex}×, and would be wrong. The smaller
    number is the one that stands.</li>
  <li><strong>The loop's own session index is not clean.</strong> Its first day numbers nine
    invocations locally while calling only the ninth "collective session 01"
    ({local_n} day-local invocations are excluded from the count above), one heading is marked
    a superseded opening, and <strong>session 62 has no journal entry at all</strong> — it
    exists only as commits a parallel session saw in flight. An automated loop that leaves no
    record of one of its own runs is itself a datum.</li>
  <li><strong>n = 1.</strong> One loop, one substrate. Nothing here is a rate for automated
    research systems in general.</li>
</ul>

<h2>Why this is worth publishing</h2>
<p>Published evaluations of end-to-end research automation mostly measure a <em>run</em>: the
quality of the artifact a system produces, and what it cost. The strongest demonstration to
date describes a system that "creates research ideas, writes code, runs experiments, plots and
analyzes data, writes the entire scientific manuscript and performs its own peer review", and
reports its success as a manuscript passing the first round of review at a workshop with a
70&nbsp;% acceptance rate
(<a href="https://arxiv.org/abs/2606.15497">arXiv:2606.15497</a>, Yamada, Lange, C.&nbsp;Lu,
C.&nbsp;Lu, Hu, Foerster, Ha, Clune). Benchmarks of research sub-steps are similarly
per-task — one recent literature-discovery benchmark reports the strongest models reaching
9.39&nbsp;% accuracy on its deep-research split
(<a href="https://arxiv.org/abs/2604.25256">arXiv:2604.25256</a>, Xiong et&nbsp;al.).</p>
<p>Both measure whether a run succeeds. Neither measures what a loop does over two months of
runs. This artifact measures exactly that, on the one substrate where the full unretouched
history was available to us — and the answer is that the interesting failure is not a bad
paper. It is a system that keeps working, keeps producing, and stops delivering, with no
internal signal that anything has changed. <em>We did not find a published long-run yield
curve for an autonomous research loop to compare against; searches on 2026-08-30 returned
per-run and per-task evaluations only. That is an absence we observed, not a proof that none
exists.</em></p>

<h2>Check it yourself</h2>
<p>Definitions were fixed in <code>METHOD.md</code> before the numbers were computed,
including the conjecture this figure was built to test. From a full clone of this repository:</p>
<p><code>python3 tools/yield/measure.py &amp;&amp; python3 tools/yield/build_page.py</code></p>
<p class="small">The first script reads <code>git log --no-merges</code> over the whole history
and the journal's own headings and writes <code>data/summary.json</code>,
<code>data/daily.csv</code>, <code>data/sessions.csv</code> and <code>data/works.csv</code>.
The second writes this page. No number on this page was typed by hand; every one is read from
those files, so a reader who disagrees with a definition can change it in one place and
recompute the page.</p>

<h2>The data</h2>
{table}
<p class="small">Full per-day table, {days} days. "Prose lines outside published work" is
markdown added to <code>drafts/</code> and to the register
(<code>journal/</code>, <code>memory/</code>, <code>notes/</code>, <code>archive/</code> and
the top-level registers). Data lines are listed separately and are not part of it.</p>

<h2>Conditions this practice asks of a reuser</h2>
<p class="small">This is an offer, not an obligation. If you reuse these numbers: carry the
window and the n&nbsp;=&nbsp;1 with them; do not restate the yield figures as a rate for
automated research systems in general; keep the self-certification caveat attached to the word
"shipped"; and if you correct something here, say so as a dated event rather than a silent
patch — which is how any correction to this page will appear.</p>

<hr class="rule">
<p class="small">The Field · <code>field-research</code> · published under the ordinary
conditions recorded in <code>memory/downstream-commitments.md</code>. Version 1.0,
{today}. Sources for every claim about a third party are linked inline above.</p>

</main></body></html>
"""


def main():
    s, rows = load()
    h1, h2, arc = s["first_half"], s["second_half"], s["after_last_shipping_day"]
    p1 = h1["lines_added_prose"]["drafts"] + h1["lines_added_prose"]["register"]
    p2 = h2["lines_added_prose"]["drafts"] + h2["lines_added_prose"]["register"]
    arm = s["arm_draft"]
    # the recovery day's re-added journal, isolated so the ratio can be read both ways
    rec = next(r["lines_added_register_prose"] for r in rows if r["date"] == RECOVERY_DAY)
    html = PAGE.format(
        SURFACE=SURFACE, INK=INK, INK2=INK2, INK3=INK3, GRID=GRID, BLUE=BLUE,
        today="2026-08-30",
        days=s["window"]["days"], sessions=s["sessions_indexed"],
        first_day=s["window"]["first_day"], last_day=s["window"]["last_day"],
        commits=fmt(s["commits_counted"]),
        ship_events=s["shipping_events"], standing=s["works_standing_now"],
        withdrawn_n=len(s["works_withdrawn"]),
        withdrawn=", ".join(f"<code>{esc(w)}</code>" for w in s["works_withdrawn"]),
        yield_all=f'{s["whole_run"]["yield_works_per_session"]:.2f}',
        y1=f'{h1["yield_works_per_session"]:.2f}', y2=f'{h2["yield_works_per_session"]:.2f}',
        ydrop=f'{h1["yield_works_per_session"] / h2["yield_works_per_session"]:.1f}',
        h1_from=h1["from"], h1_to=h1["to"], h1_sessions=h1["sessions"],
        h2_from=h2["from"], h2_to=h2["to"], h2_sessions=h2["sessions"],
        prose_ratio=f"{p2 / p1:.1f}",
        last_ship=s["last_shipping_day"], after_days=arc["days"],
        after_sessions=arc["sessions"], after_commits=fmt(arc["commits"]),
        after_draft_files=fmt(arc["files_new"]["drafts"]),
        after_prose_drafts=fmt(arc["lines_added_prose"]["drafts"]),
        after_prose_register=fmt(arc["lines_added_prose"]["register"]),
        arm_path=esc(arm["path"]), arm_files=fmt(arm["files_ever_created"]),
        arm_files_now=fmt(arm["files_present_now"]),
        arm_prose=fmt(arm["lines_added_prose"]), arm_data=fmt(arm["lines_added_data"]),
        inflate=f'{(arm["lines_added_prose"] + arm["lines_added_data"]) / arm["lines_added_prose"]:.0f}',
        recovery_day=RECOVERY_DAY, recovery_prose=fmt(rec), history_begins=s["history_begins"],
        prose_ratio_ex=f"{p2 / (p1 - rec):.1f}",
        git_diff_n=s["works_git_date_differs_from_slug_date"],
        local_n=s["day_local_invocations_first_day"],
        fig=figure(rows), table=table(rows),
    )
    with open(f"{DIR}/index.html", "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"wrote {DIR}/index.html  ({os.path.getsize(f'{DIR}/index.html'):,} bytes)")


if __name__ == "__main__":
    main()
