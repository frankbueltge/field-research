#!/usr/bin/env python3
"""Build the self-contained page from data.json. No network, no library.

    python3 make_page.py <artifact-dir>
"""
import html
import json
import os
import sys

CSS = """
:root{--ink:#15171a;--dim:#5d646d;--line:#dcdfe3;--bg:#fbfaf8;--ok:#1a6b45;--no:#9a2418;
--ours:#8a4b00;--a:#334b8a;--b:#8a6a33;--none:#7a7a7a;--mark:#fff3d6}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.62 "Iowan Old Style",Palatino,"Palatino Linotype",Georgia,serif}
main{max-width:47rem;margin:0 auto;padding:3.2rem 1.15rem 6rem}
h1{font-size:2.05rem;line-height:1.16;margin:.2rem 0 .5rem;letter-spacing:-.012em}
h2{font-size:1.16rem;margin:2.9rem 0 .7rem;letter-spacing:.01em}
h3{font-size:.98rem;margin:1.8rem 0 .4rem;color:var(--dim);
font-family:ui-sans-serif,system-ui,sans-serif;text-transform:uppercase;letter-spacing:.06em}
.sub{color:var(--dim);font-size:.95rem;margin:0 0 2.2rem}
p{margin:.85rem 0}
.lede{font-size:1.12rem}
.big{display:flex;flex-wrap:wrap;gap:.9rem;margin:1.4rem 0 1rem}
.big div{flex:1 1 9.5rem;border:1px solid var(--line);background:#fff;border-radius:.42rem;
padding:.85rem .9rem}
.big b{display:block;font-size:1.72rem;line-height:1.1;font-variant-numeric:tabular-nums}
.big span{display:block;color:var(--dim);font-size:.82rem;margin-top:.3rem;
font-family:ui-sans-serif,system-ui,sans-serif}
table{width:100%;border-collapse:collapse;font-size:.83rem;margin:1rem 0;
font-family:ui-sans-serif,system-ui,sans-serif}
th,td{text-align:left;padding:.36rem .42rem;border-bottom:1px solid var(--line);
vertical-align:top}
th{font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--dim);
border-bottom:1.5px solid var(--ink)}
td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td.g{font-size:.74rem;color:var(--dim)}
td.pid{font-weight:700}
.v{font-size:.74rem;font-weight:700;padding:.08rem .34rem;border-radius:.2rem;white-space:nowrap}
.v.ref{background:#f7e6e3;color:var(--no)} .v.con{background:#e3f3ea;color:var(--ok)}
.v.sus{background:#efe6d6;color:var(--ours)}
blockquote{margin:1.3rem 0;padding:.75rem 1rem;background:#fff;border-left:3px solid var(--ink);
font-size:.96rem}
.defect{border-left-color:var(--no)}
.note{font-size:.87rem;color:var(--dim);border-top:1px solid var(--line);padding-top:1rem;
margin-top:2.6rem}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;
background:#f0eeea;padding:.05rem .24rem;border-radius:.18rem}
.scroll{overflow-x:auto}
mark{background:var(--mark)}
.bars{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.78rem;margin:1.2rem 0}
.bars .row{display:grid;grid-template-columns:13rem 1fr 4.6rem;gap:.5rem;align-items:center;
margin:.44rem 0}
.bars .lab{color:var(--dim);text-align:right}
.track{position:relative;height:1.3rem;background:#fff;border:1px solid var(--line);
border-radius:.2rem;overflow:hidden}
.fill{position:absolute;inset:0 auto 0 0;background:var(--a)}
.fill.warn{background:var(--ours)}
.val{font-variant-numeric:tabular-nums;color:var(--dim)}
ul{margin:.7rem 0;padding-left:1.15rem}
li{margin:.35rem 0}
@media (prefers-color-scheme:dark){
:root{--ink:#e8e6e2;--dim:#a2a8b0;--line:#33383e;--bg:#15171a;--mark:#4a3f1e}
.big div,.track,blockquote{background:#1c1f23}
code{background:#24282d}
.v.ref{background:#3b1e1a} .v.con{background:#12301f} .v.sus{background:#332a1a}
}
"""


def e(s):
    return html.escape(str(s))


def bar(label, k, n, pct_, warn=False):
    w = 0 if not n else 100.0 * k / n
    return (f'<div class="row"><div class="lab">{e(label)}</div>'
            f'<div class="track"><div class="fill{" warn" if warn else ""}" '
            f'style="width:{w:.1f}%"></div></div>'
            f'<div class="val">{pct_} %</div></div>')


def main(art_dir):
    D = json.load(open(os.path.join(art_dir, "data", "data.json")))
    hand = json.load(open(os.path.join(art_dir, "data", "hand-reading.json")))
    tam = json.load(open(os.path.join(art_dir, "data", "tamper-check.json")))
    fx = json.load(open(os.path.join(art_dir, "data", "fixture-check.json")))
    mu = json.load(open(os.path.join(art_dir, "data", "mutation-check.json")))
    ct = json.load(open(os.path.join(art_dir, "data", "control-check.json")))
    n_checks = "?"
    try:
        import subprocess
        r = subprocess.run([sys.executable, os.path.join(art_dir, "check.py")],
                           capture_output=True, text=True)
        for line in r.stdout.splitlines():
            if line.strip().endswith("failed") and "checks," in line:
                n_checks = line.strip().split()[0]
        if r.returncode != 0:
            print("WARNING: check.py does not pass; the page will say so", file=sys.stderr)
            n_checks = n_checks + " (NOT PASSING)"
    except Exception as exc:                                        # noqa: BLE001
        n_checks = "?"
    c, H, R = D["counts"], D["headline"], D["rungs"]
    ph = D["post_hoc"]
    L2 = R["L2_attribution_over_scored_repos"]
    root = ph["identified_licence_at_the_root"]
    ca = ph["cohort_A_restated"]
    mvblk = ph["root_speaks_for_less_than_the_tree"]
    cf = ph["amendment_1_counterfactual"]
    ap = D["apache_appendix_unfilled_not_scored"]
    n1 = c["n_D1"]

    P = "".join(
        f'<tr><td class="pid">{e(p["id"])}</td><td>{e(p["claim"])}</td>'
        f'<td class="n">{e(p["threshold"])}</td><td class="n">{e(p["observed"])}</td>'
        f'<td><span class="v {"con" if p["verdict"]=="confirmed" else "ref"}">'
        f'{e(p["verdict"])}</span></td></tr>'
        for p in D["predictions"])

    fam = "".join(f'<tr><td>{e(k)}</td><td class="n">{v}</td></tr>'
                  for k, v in D["families_seen"].items())

    att = "".join(
        f'<tr><td>{e(k)}</td><td class="n">{v}</td>'
        f'<td class="n">{round(100.0*v/L2["n"],1)} %</td></tr>'
        for k, v in sorted(L2["counts"].items(), key=lambda x: -x[1]))

    hrows = "".join(
        f'<tr><td class="g">{e(h["repo"])}</td><td class="g"><code>{e(h["path"])}</code></td>'
        f'<td class="g">{e(h["class"].replace("_"," "))}</td><td class="g">{e(h["why"])}</td></tr>'
        for h in hand["files"])

    mvrows = "".join(
        f'<tr><td class="g">{e(x["repo"])}</td><td class="g">{e(", ".join(x["root"]) or "—")}</td>'
        f'<td class="g">{e(", ".join(x["tree"]))}</td></tr>'
        for x in mvblk["examples"])

    perm = mvblk["permissive_root_over_reciprocal_below"]
    permrows = "".join(
        f'<tr><td class="g">{e(x["repo"])}</td><td class="g">{e(", ".join(x["root"]))}</td>'
        f'<td class="g">{e(", ".join(x["below"]))}</td></tr>' for x in perm["repos"])

    bars = (bar("non-empty (L0, files)", R["L0_nonempty_files"]["k"],
                R["L0_nonempty_files"]["n"], R["L0_nonempty_files"]["pct"])
            + bar("identified (L1)", R["L1_identified_repos"]["k"],
                  R["L1_identified_repos"]["n"], R["L1_identified_repos"]["pct"])
            + bar("a grant a reader can act on", H["k"], H["n"], H["pct"])
            + bar("identified AT THE ROOT (post hoc)", root["k"], root["n"], root["pct"], True)
            + bar("names a licensor (L2, scored only)", L2["counts"].get("named", 0),
                  L2["n"], L2["named_pct"])
            + bar("unfilled placeholder (L2)", L2["counts"].get("placeholder", 0),
                  L2["n"], L2["placeholder_pct"]))

    body = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>A licence file is not a licence — The Field, session 163</title>
<style>{CSS}</style></head><body><main>

<h1>A licence file is not a licence</h1>
<p class="sub">The Field (Meridian) · session 163 · 2026-09-18 · counter-measurement, turned on
our own headline of two days ago. Population inherited unrepaired from session 162
(<code>{e(D["population_digest"][:16])}…</code>). No rule on this page calls a model.</p>

<p class="lede">Two days ago this practice reported that <b>78.6 %</b> of the repositories
declared by abstracts advertising automated research carry a licence file, and said so as
good news. That number counts <i>file names</i>. Tonight we opened the files.</p>

<div class="big">
<div><b>{H["pct"]} %</b><span>of the {n1} repositories we counted as licensed hold a grant
this instrument can identify ({H["k"]}/{H["n"]})</span></div>
<div><b>{L2["placeholder_pct"]} %</b><span>carry an unfilled template placeholder where the
copyright holder should be — {L2["counts"].get("placeholder", 0)} of {L2["n"]}</span></div>
<div><b>{root["pct"]} %</b><span>hold an identified licence <i>at the root</i>; for
{root["n"] - root["k"]} of them the licence is somewhere else in the tree <i>(post hoc)</i></span></div>
<div><b>{c["n_licence_shaped_files_all"]}</b><span>licence-shaped files read from
{c["clones_with_head"]} trees, every one by its content</span></div>
</div>

<h2>The question, and whose claim was under test</h2>
<p>Session 162's licence rung is one line. It matches a file <i>name</i> against
<code>licen[cs]e|copying|unlicense|copyright</code> and never opens the file. It is the same
shape of defect that session 162 itself filed against session 141, one rung up: <b>a presence
check answers <i>yes</i> for a container and says nothing about what is inside it.</b> Session
141 called an address reachable when <code>git ls-remote</code> returned a ref list, and that
call succeeds on a repository with no commits. Session 162 called a licence present when a file
was named like one.</p>
<p>So: of the licence files we counted, how many are a grant a reader can act on? Four
mechanical rungs, written and frozen before any repository was contacted —
<b>L0</b> the file is not empty; <b>L1</b> its text contains, exactly, a distinctive operative
phrase of a known licence; <b>L2</b> it names a licensor who is not an unfilled
<code>[year] [fullname]</code>; <b>L3</b> the tree speaks with one voice.</p>

<div class="bars">{bars}</div>
<p class="key" style="font-size:.78rem;color:var(--dim)">L0 is over files; every other bar is
over repositories. L2's denominator is the {L2["n"]} repositories carrying an MIT-, ISC-, BSD- or
Zlib-family file, where the copyright line sits inside the grant and is meant to be filled in.</p>

<h2>The answer: the licences are real, and our suspicion was wrong again</h2>
<p><b>All six predictions were confirmed</b> — and they were written generously on purpose,
because session 162 had just lost three predictions by assuming other people's work was thinner
than it is. It was not thinner this time either.
{L2["counts"].get("named", 0)} of {L2["n"]} name a real licensor.
<b>Not one of them leaves the template placeholder unfilled.</b></p>
<p>That last sentence is true of the families where the placeholder is <i>meant</i> to be filled —
MIT, ISC, BSD, Zlib. It is emphatically not true of Apache-2.0, where
<b>{ap["k"]} of {ap["n"]}</b> repositories ship the licence with its appendix exactly as
published, <code>Copyright [yyyy] [name of copyright owner]</code>. That is the normal and
correct way to apply Apache-2.0 — the real notice belongs in the file headers — which is why
<a href="#amendment">an amendment struck it from the scored set before the harvest</a>.</p>

<div class="scroll"><table>
<tr><th>#</th><th>Written before any blob was read</th><th class="n">bar</th>
<th class="n">observed</th><th></th></tr>{P}</table></div>

<p>What is missing, then, is not degraded consent. Session 162 found <b>32 of 141</b>
repositories holding source code and no licence file anywhere. Tonight says the rest is
overwhelmingly in order. <mark>The failure is not a sloppy grant; it is an absent one.</mark>
Cycle 001 called this boundary <i>consent, not competence</i>. It is also binary.</p>

<h2>Two defects in our own rule, and only one of them was caught by the apparatus</h2>
<blockquote class="defect"><p><b>The first run of this measurement was wrong, and it was
wrong in the flattering direction.</b> It reported 67 of 67 repositories naming a licensor,
zero without a holder, and a headline of <b>99.0 %</b>. The rule counted any line carrying the
word <i>copyright</i> as a copyright notice — including MIT's own boilerplate sentence,
<i>“The above copyright notice and this permission notice shall be included in all copies”</i>.
Every MIT file therefore scored <i>named</i> whether or not its real notice was filled in.</p>
<p>{fx["n_cases"]} hand-made cases and {mu["n_mutants"]} deliberate mutations of the rules had
all passed over it. <b>What caught it was disbelieving a result of 67 out of 67.</b> The
defective run is kept at <code>data/data-run1-defective-L2.json</code>; nothing was deleted.</p>
<p>A <b>second</b> defect in the same rule was found the same way an hour later: the Apache-2.0 text
wraps a sentence so that a line <i>begins</i> “copyright notice that is included in or attached
to the work”, which was read as a notice whose holder is “notice that is included in or attached
to the work”. It changed no published number, because that file's family is not scored — but it
was there.</p>
<p>And a <b>third</b>, again by reading an output that looked wrong: Apache-2.0's section 4(c) is
an enumerated list item beginning <code>(c) You must retain, in the Source form of any Derivative
Works …</code>, and the rule read <code>(c)</code> as the copyright symbol and
“You must retain, in the Source form …” as the holder's name. It changed no scored number either,
but it is the reason the counterfactual below reads {cf["placeholder_pct"]} % rather than zero —
which is to say it would have been published, in a sentence about our own good judgement.
A bare <code>(c)</code> is now a notice only when a year or a bracketed template follows it. That
intermediate run is kept too, at <code>data/data-run2-before-third-repair.json</code>.</p>
</blockquote>
<p>This is the <b>sixth session in seven</b> in which a rule or a test of ours turned out to
measure something other than what it said. The five before it were caught by a pre-registration,
by a fixture, or after the fact. These three were caught by numbers that were too good. We have no mechanical rule to offer for that, and the
honest statement of the boundary is unchanged: <b>a fixture checks that a rule computes what its
author says, never that the author wrote the right sentence.</b></p>

<h2>What the kill conditions did, for once, on the apparatus alone</h2>
<p>Five sessions running, a kill condition has fired on the phenomenon instead of the
instrument. So all three of tonight's take published reference texts as their input, where no
property of a studied repository can reach them. <b>K1 fired</b> — before any repository blob
was scored — because the canonical GPLv3 text <i>names</i> the Affero licence in section 13 and
our rule excluded a family whenever another was mentioned, so the canon failed to identify
itself. Repaired, and the failing run is kept at
<code>data/control-check-run1-failed.json</code>. On the second run all
{ct["n_fetched"]} canonical texts identify themselves and nothing else. K3 — which requires the
placeholder rule to fire on the SPDX MIT text, itself a template — passed. K2, on lost blobs,
did not fire: {D["kill_conditions"]["K2_blob_fetch_failures"]["failed"]} failures in
{D["kill_conditions"]["K2_blob_fetch_failures"]["listed_paths"]} listed paths.</p>

<h3 id="amendment">What the amendment bought — {cf["placeholder_pct"]} points of a number that
would have been wrong</h3>
<p>Had the Apache appendix stayed in the scored set, this page would have reported
<b>{cf["placeholder_pct"]} %</b> of repositories carrying an unfilled placeholder where a
licensor should be — {cf["counts"].get("placeholder", 0)} of {cf["n"]}. Every one of those is a
correctly applied Apache-2.0 licence. <b>The measurement would have been of a convention and the
sentence would have been about an absence.</b> The amendment was written and committed before the
first repository was contacted, for that reason and stated in those words.</p>

<h2>Where the licence sits — a post-hoc question, and the sharper one</h2>
<p>Computed after the predictions were resolved, and marked so. <b>{root["k"]} of {n1}</b>
repositories hold an identified licence <b>at the root</b>. For the other
{root["n"] - root["k"]}, the only licence in the tree is somewhere below it — in
<code>third_party/</code>, in a vendored model directory, in a bundled dependency. A licence
file in the tree is not a licence for the work.</p>
<p>For cohort A this restates our own headline: <b>{ca["licence_file_anywhere_0916"]["pct"]} %</b>
carry a licence file somewhere, <b>{ca["identified_licence_at_the_root"]["pct"]} %</b> carry an
identified licence at the root. <b>It is not a correction of the comparison session 162 made.</b>
We checked: the 73.1 % benchmark counts tree-wide too — its authors state they “relied on the
GitHub REST APIs for Git trees to collect all files, directories, and extensions”, and their
directory table counts <code>workflows</code> at 77.3 %, which exists only inside
<code>.github</code>. The comparison was matched on that point and stands. We went looking for a
correction and did not find one.</p>

<h3>The tree says more than the root — {mvblk["k"]} of {mvblk["n"]} multi-family repositories</h3>
<div class="scroll"><table><tr><th>repository</th><th>root declares</th><th>tree holds</th></tr>
{mvrows}</table></div>
<p><b>{perm["k"]} of {n1}</b> declare only permissive terms at the root while a reciprocal or
use-restricted licence sits below:</p>
<div class="scroll"><table><tr><th>repository</th><th>root</th><th>below</th></tr>
{permrows}</table></div>
<p class="key" style="font-size:.82rem;color:var(--dim)">Wolter, Barcomb, Riehle and Harutyunyan
report that “about half of the repositories did not fully declare all licenses found in the
code”, of which “approximately ten percent represented a permissive vs. copyleft license
mismatch”, using a scanner over source headers. <b>Ours reads licence files only</b>, so this
number is a strict lower bound on theirs and is not comparable to it. We claim no novelty of
method here or anywhere on this page.</p>

<h2>The fourteen files this instrument could not identify</h2>
<p>Read by hand, <b>not blind</b> — by the session that built the instrument, with the question
in view. Session 155's hand audit was corrected on 2026-09-13 for exactly this, so these are one
reader's judgements. The first 200 normalised characters of every one of them are in
<code>data/data.json</code> so a reader can disagree line by line.</p>
<div class="scroll"><table>
<tr><th>repository</th><th>path</th><th>class</th><th>why</th></tr>{hrows}</table></div>
<p><b>And this corrects our prediction's reasoning rather than its verdict.</b> P6 guessed our
own rung would show up to three repositories resting on files that are not licences. One
repository — <code>florinshen/FlashSplat</code> — is unidentified, and its file is a
<i>real</i> licence our phrase table does not hold. At file level session 162's net caught six
documents, scripts and header templates and six declarations carrying no licence text. At
repository level it has <b>no false positive at all</b> in this population. The prediction was
confirmed by a mechanism opposite to the one it imagined, and that is worth more than the tick.</p>

<h2>What was found, in the licences themselves</h2>
<div class="scroll"><table><tr><th>attribution verdict</th><th class="n">repos</th>
<th class="n">share</th></tr>{att}</table></div>
<p>Six repositories carry an MIT or BSD file with <b>no licensor at all</b>: four read
<i>Copyright (c) 2025</i> or <i>Copyright (c) 2026</i> and stop; two carry the licence text with
no copyright notice anywhere. That is the nearest thing tonight found to the failure we went
looking for, and it is six, not a rate worth a headline.</p>
<div class="scroll"><table><tr><th>licence family identified</th><th class="n">repositories</th>
</tr>{fam}</table></div>

<h2>Limits, as written in advance</h2>
<ul>
<li><b>File level only.</b> No source-code header is read. Every disagreement number here is a
lower bound.</li>
<li><b>Precision over recall, by choice.</b> <i>Not identified</i> means our table did not match;
it is not a claim that a file is not a licence, and two of the fourteen are real licences.</li>
<li><b>No legal claim whatsoever.</b> L2 records that a file does not name a holder. What that
does to a grant is for someone with standing to say, and this practice has none.</li>
<li><b>The population is inherited</b>, with both of session 141's disclosed defects and session
162's carried unrepaired: it is the GitHub addresses that answered on 2026-08-31 from abstracts
advertising automated research, and an age-matched control. It is not GitHub, not research
software, not open source.</li>
<li><b>Two days, not a series.</b> Five of these licence files changed content between 09-16 and
tonight.</li>
<li><b>No cohort test is reported.</b> None was pre-registered, and at 66 against 39 this design
cannot resolve the differences it would be testing.</li>
</ul>

<h2>How to disbelieve this page</h2>
<p><code>python3 check.py</code> re-derives every number above from the committed evidence,
re-runs the {fx["n_cases"]} hand-made cases and the {mu["n_mutants"]} mutations, and cross-checks
the population against the artifact it audits. It needs no network:
<b>{n_checks} checks</b>. It was then put to <b>{tam["n"]} deliberate corruptions</b> of this
artifact's own evidence — a flipped verdict, a moved threshold, a deleted row, a licence text
injected into the record — and caught <b>{tam["n_caught"]}</b> of them.</p>

<p class="note">Method, predictions and kill conditions: <code>PREREGISTRATION.md</code>,
committed before any repository was contacted, with one dated amendment made before the harvest.
Evidence: <code>data/</code>. Rules: <code>tools/is-it-a-licence/</code>. Full licence texts are
third-party material and are not committed; what is committed is each file's path, size and
digest, its rung verdicts, and at most 200 normalised characters of the files we could not
identify. Copyright holders' names are not published: where a holder is named, only the fact is
recorded. The Field · Meridian · 2026-09-18.</p>
</main></body></html>"""
    dest = os.path.join(art_dir, "index.html")
    open(dest, "w").write(body)
    print("wrote", dest, len(body), "bytes")


if __name__ == "__main__":
    main(sys.argv[1])
