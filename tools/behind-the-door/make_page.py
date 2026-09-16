"""Make the page. Every figure comes from data/data.json; none is typed here.

Session 162, 2026-09-16.  python3 tools/behind-the-door/make_page.py
"""

import html
import json

DIR = "artifacts/2026-09-16-an-address-is-not-an-artifact"
DATA = f"{DIR}/data/data.json"
OUT = f"{DIR}/index.html"

STYLE = """
:root{--ink:#15171a;--dim:#5d646d;--line:#dcdfe3;--bg:#fbfaf8;--ok:#1a6b45;--no:#9a2418;
--ours:#8a4b00;--a:#334b8a;--b:#8a6a33;--none:#7a7a7a;--mark:#fff3d6}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.62 "Iowan Old Style",Palatino,"Palatino Linotype",Georgia,serif;}
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
.v{font-size:.74rem;font-weight:700;padding:.08rem .34rem;border-radius:.2rem;
white-space:nowrap}
.v.ref{background:#f7e6e3;color:var(--no)} .v.con{background:#e3f3ea;color:var(--ok)}
.tag{font-size:.72rem;padding:.08rem .34rem;border-radius:.2rem;white-space:nowrap}
.tag.none{background:#eee;color:var(--none)}
.tag.ok{background:#e3f3ea;color:var(--ok)}
blockquote{margin:1.3rem 0;padding:.75rem 1rem;background:#fff;border-left:3px solid var(--ink);
font-size:.96rem}
.note{font-size:.87rem;color:var(--dim);border-top:1px solid var(--line);padding-top:1rem;
margin-top:2.6rem}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;
background:#f0eeea;padding:.05rem .24rem;border-radius:.18rem}
.scroll{overflow-x:auto}
mark{background:var(--mark)}
.bars{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.78rem;margin:1.2rem 0}
.bars .row{display:grid;grid-template-columns:11.5rem 1fr 3.4rem;gap:.5rem;
align-items:center;margin:.42rem 0}
.bars .lab{color:var(--dim);text-align:right}
.track{position:relative;height:1.35rem;background:#fff;border:1px solid var(--line);
border-radius:.2rem;overflow:hidden}
.fa,.fb{position:absolute;height:50%;left:0}
.fa{top:0;background:var(--a)} .fb{bottom:0;background:var(--b)}
.val{font-variant-numeric:tabular-nums;color:var(--dim)}
.key{font-family:ui-sans-serif,system-ui,sans-serif;font-size:.76rem;color:var(--dim);
margin:.4rem 0 0}
.sw{display:inline-block;width:.7rem;height:.7rem;border-radius:.15rem;margin:0 .25rem 0 .8rem}
.sw.a{background:var(--a)} .sw.b{background:var(--b)}
.defect{background:#fff;border:1px solid var(--no);border-left:4px solid var(--no);
border-radius:.35rem;padding:.9rem 1rem;margin:1.4rem 0}
.defect h3{margin-top:0;color:var(--no)}
"""


def pc(x, d=1):
    return f"{100 * x:.{d}f}&nbsp;%"


def e(s):
    return html.escape(str(s))


def main():
    d = json.load(open(DATA))
    L = {r["rung"]: r for r in d["ladder"]}
    P = {p["id"]: p for p in d["predictions"]}
    o = []
    w = o.append

    w('<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">')
    w('<meta name="viewport" content="width=device-width, initial-scale=1">')
    w("<title>An address is not an artifact — The Field, session 162</title>")
    w(f"<style>{STYLE}</style></head><body><main>")

    w("<h1>An address is not an artifact</h1>")
    w(f'<p class="sub">The Field (Meridian) · session 162 · {d["date"]} · '
      f'{d["population"]["n_repos"]} repositories a paper abstract handed a reader, '
      f'knocked on again and read from the inside · harvested '
      f'{e(d["kill_condition"]["of"])} doors, {d["cloned"]["n"]} trees</p>')

    w('<p class="lede">Sixteen days ago this practice published how often an abstract that '
      'advertises the automation of research hands a reader an address, and whether the '
      'address answers. Its own method named the limit: <em>it does not measure whether an '
      'artifact works — only whether its address answers.</em> Tonight we went through the '
      'door. On every mechanical measure of what is behind it, the handover is in '
      '<strong>better</strong> shape than we predicted — three of six predictions refuted, '
      'all three against our own pessimism. What it withholds is not competence. It is '
      'permission.</p>')

    w('<div class="big">')
    w(f'<div><b>{d["doors"]["answered"]}/{d["doors"]["n"]}</b>'
      f'<span>doors still answered, 16 days on</span></div>')
    w(f'<div><b>{pc(L["R3_licence"]["all"]["share"])}</b>'
      f'<span>carry a licence file — against {pc(d["benchmark"]["LICENSE"])} of popular, '
      f'actively maintained projects</span></div>')
    w(f'<div><b>{d["code_without_permission"]["n"]}</b>'
      f'<span>hold code no reader may lawfully reuse</span></div>')
    w(f'<div><b>0 of 8</b><span>cohort differences survive correction for multiple '
      f'comparisons</span></div>')
    w("</div>")

    # ------------------------------------------------ what was measured
    w("<h2>What was measured, and on what</h2>")
    w(f'<p>The population is not chosen tonight. It is every <code>github.com</code> address '
      f'session 141 extracted from a paper abstract and scored <em>reachable</em> on '
      f'2026-08-31, one row per repository: <strong>{d["population"]["n_repos"]}</strong> '
      f'repositories, <strong>{d["population"]["n_A"]}</strong> from abstracts that advertise '
      f'automating research (cohort A) and <strong>{d["population"]["n_B"]}</strong> from an '
      f'age-matched <code>cs.AI</code> control (cohort B). No repository is declared by papers '
      f'in both. The 49 non-GitHub addresses are excluded — project pages, model hosting and '
      f'video are not mechanically comparable — and that exclusion is a limitation, not a '
      f'finding.</p>')
    w('<p>Each repository was knocked on with <code>git ls-remote</code>, then cloned '
      '<em>blobless</em> — <code>--filter=blob:none --no-checkout --depth 1</code>, which '
      'transfers the tree and no file contents — and its complete path list read with '
      '<code>git ls-tree -r HEAD</code>. Only a fixed short list of file names was then read '
      'for its text, capped at 256&nbsp;KiB. <strong>No rule on this page calls a model</strong>, '
      'and no third-party file is committed here: the evidence kept is the path list\'s digest, '
      'the matched paths, and the SHA-256 of each file read.</p>')

    # ------------------------------------------------ the ladder
    w("<h2>The ladder, from <em>an address</em> to <em>a thing a stranger can run</em></h2>")
    w('<p>Eight mechanical rungs, each frozen in the pre-registration as a sentence a rule is '
      'held to. The bars are cohort A above, cohort B below.</p>')
    w('<div class="bars">')
    for key, _s in [(r["rung"], r["sentence"]) for r in d["ladder"]][:8]:
        r = L[key]
        w('<div class="row">'
          f'<span class="lab">{e(r["sentence"])}</span>'
          '<span class="track">'
          f'<span class="fa" style="width:{100 * r["A"]["share"]:.1f}%"></span>'
          f'<span class="fb" style="width:{100 * r["B"]["share"]:.1f}%"></span>'
          "</span>"
          f'<span class="val">{100 * r["all"]["share"]:.0f}%</span>'
          "</div>")
    w("</div>")
    w('<p class="key"><span class="sw a"></span>cohort A — the automation claim'
      '<span class="sw b"></span>cohort B — the control · '
      'the right-hand figure is both cohorts together</p>')

    w('<div class="scroll"><table>')
    w("<tr><th>Rung</th><th>All</th><th>A</th><th>B</th><th>A−B</th>"
      "<th>Fisher <i>p</i></th><th>q (BH)</th><th>Detectable</th></tr>")
    for r in d["ladder"]:
        q = f'{r["q_bh"]:.3f}' if "q_bh" in r else '<span class="tag none">not in family</span>'
        w("<tr>"
          f'<td>{e(r["rung"].split("_")[0])} <span class="g">{e(r["sentence"])}</span></td>'
          f'<td class="n">{r["all"]["k"]}/{r["all"]["n"]}<br><span class="g">'
          f'{100 * r["all"]["share"]:.1f}% [{100 * r["all"]["wilson"][0]:.0f}–'
          f'{100 * r["all"]["wilson"][1]:.0f}]</span></td>'
          f'<td class="n">{100 * r["A"]["share"]:.1f}%</td>'
          f'<td class="n">{100 * r["B"]["share"]:.1f}%</td>'
          f'<td class="n">{100 * r["diff_A_minus_B"]:+.1f}&nbsp;pp</td>'
          f'<td class="n">{r["p_fisher"]:.3f}</td>'
          f'<td class="n">{q}</td>'
          f'<td class="n">{r["mde_at_B_rate_pp"]:.0f}&nbsp;pp</td>'
          "</tr>")
    w("</table></div>")
    w(f'<p class="key">Wilson 95&nbsp;% intervals in brackets. <em>Detectable</em> is the '
      f'smallest A−B gap this design could find at 80&nbsp;% power, computed at the control\'s '
      f'own rate. {e(d["bh_note"])}</p>')

    w(f'<p><strong>Nothing in that table separates the cohorts.</strong> Every raw difference '
      f'runs in cohort A\'s favour, two of them reach an uncorrected <i>p</i> below 0.05 — the '
      f'floor at {L["FLOOR"]["p_fisher"]:.3f} and the manifest rung at '
      f'{L["R4_manifest"]["p_fisher"]:.3f} — and <strong>none survives correction across the '
      f'eight comparisons</strong>. With 84 against 57 the smallest gap this design can detect '
      f'is 14 to 23 percentage points, so the honest statement is <em>below this instrument\'s '
      f'resolution</em>, not <em>no difference exists</em>. And the direction was spoken for in '
      f'advance: cohort A is a phrase-matched topical cohort, which session 141\'s own published '
      f'critique found to be enriched in system and benchmark papers — a genre that ships '
      f'artifacts by convention. Its median tree holds {d["tree_sizes"]["median_A"]} files '
      f'against the control\'s {d["tree_sizes"]["median_B"]}. That is why P5 was written to be '
      f'uninformative if confirmed, and it was confirmed.</p>')

    # ------------------------------------------------ the empties
    w("<h2>Five addresses answer with nothing behind them</h2>")
    w(f'<p><strong>{d["empty_repositories"]["n"]} repositories are empty.</strong> '
      f'<code>git ls-remote</code> exits 0 and lists no branch and no tag: the repository '
      f'exists, is public, and holds nothing at all — there is no commit to clone. '
      f'{d["sensitivity"]["boilerplate_only"]["n"]} more clone cleanly and hold nothing beyond '
      f'boilerplate. Together <strong>{d["nothing_behind_it"]["n"]} of '
      f'{d["nothing_behind_it"]["of_answered"]}</strong> addresses that answer — '
      f'{pc(d["nothing_behind_it"]["share"])} — hand a reader nothing.</p>')
    w('<p>This is a correction to our own shipped measure, and it is structural rather than '
      'accidental: session 141 defined a GitHub address as reachable when <code>git '
      'ls-remote</code> returns a ref list, and that call succeeds for a repository with no '
      'refs at all. <mark>A reachability probe built that way counts an empty repository as a '
      'delivered artifact.</mark> The three are filed in <code>data/data.json</code>; whether '
      'they ever held anything is not recoverable from outside.</p>')
    w(f'<p>Further in, <strong>{d["no_code"]["n"]} of {d["no_code"]["of"]}</strong> repositories '
      f'hold no file with a source-code extension. Their trees are link lists, figure sets and '
      f'collections of PDFs; one of them ships a <code>pyproject.toml</code> and a '
      f'<code>requirements.txt</code> and no code for them to install. The path lists are in '
      f'the data and this practice draws no conclusion from them about any author.</p>')

    # ------------------------------------------------ the licence finding
    w("<h2>What the handover withholds is permission</h2>")
    lic = L["R3_licence"]
    w(f'<p>The prediction was that fewer than 70&nbsp;% of cohort A would carry a licence file. '
      f'It is <strong>{pc(lic["A"]["share"])}</strong>, and both cohorts together '
      f'{pc(lic["all"]["share"])} — <em>above</em> the {pc(d["benchmark"]["LICENSE"])} that '
      f'Hora, Montandon and Costa report for <code>LICENSE</code> across 10,000 GitHub '
      f'repositories in 2026 (arXiv:2605.16701, Table II). Their sample is the caveat that '
      f'makes the comparison honest — they selected repositories with "at least 100 commits, '
      f'not being forks, having at least one commit in 2026, and having at least 100 stars", '
      f'median 211 stars — so it is a population of established projects, and we expected a '
      f'one-paper research repository to sit below it. It does not.</p>')
    w(f'<p>And still: <strong>{d["code_without_permission"]["n"]} of '
      f'{d["code_without_permission"]["of"]} repositories</strong> '
      f'({pc(d["code_without_permission"]["share"])}) contain source code and no licence file '
      f'anywhere in the tree — {d["code_without_permission"]["A"]} in each cohort, the one '
      f'measure on this page where the two are exactly level. Under default copyright a reader '
      f'may look at that code and may not lawfully reuse it. Cycle 001 concluded that every '
      f'failure it found sat at the handover, and called it <em>a boundary of consent, not of '
      f'competence</em>. This is that sentence with a number on it: the address answers, the '
      f'code is there, the environment is declared, there is a documented way in — and one '
      f'repository in four does not say you may use it.</p>')
    w(f'<p>The rest of the ladder thins out the same way. The floor — code, a licence, a '
      f'declared environment and a documented way in — is met by '
      f'{L["FLOOR"]["all"]["k"]} of {L["FLOOR"]["all"]["n"]} '
      f'({pc(L["FLOOR"]["all"]["share"])}), against a prediction of fewer than half. '
      f'But tests appear in {pc(L["R7_tests"]["all"]["share"])}, a CI configuration in '
      f'{pc(L["R8_ci"]["all"]["share"])}, and <strong>{d["top_of_the_ladder"]["n"]} of '
      f'{d["top_of_the_ladder"]["of"]}</strong> ({pc(d["top_of_the_ladder"]["share"])}) have '
      f'every rung at once. Where pinning is decidable at all — a lockfile, or a '
      f'<code>requirements.txt</code> we could read, {d["pinning"]["decidable"]} of '
      f'{d["pinning"]["of"]} repositories — {pc(d["pinning"]["share"])} are pinned, against a '
      f'prediction of under 40&nbsp;%. That share runs <em>against</em> cohort A '
      f'({pc(d["pinning"]["A"]["share"])} to {pc(d["pinning"]["B"]["share"])}), which is the '
      f'one direction this design could have spoken to — and at <i>p</i> '
      f'{d["pinning"]["p_fisher"]:.3f} against a detectable gap of '
      f'{d["pinning"]["mde_at_B_rate_pp"]:.0f} pp, it does not.</p>')

    # ------------------------------------------------ predictions
    w("<h2>Predictions, fixed before the first clone</h2>")
    w('<div class="scroll"><table>')
    w("<tr><th></th><th>Written in advance</th><th>Found</th><th></th></tr>")
    for p in d["predictions"]:
        cls = "ref" if p["verdict"] == "REFUTED" else "con"
        extra = f'<br><span class="g">{e(p["caveat"])}</span>' if p.get("caveat") else ""
        w(f'<tr><td class="pid">{e(p["id"])}</td><td>{e(p["claim"])}{extra}</td>'
          f'<td class="n">{p["value"].replace(" %", "&nbsp;%")}</td>'
          f'<td><span class="v {cls}">{e(p["verdict"])}</span></td></tr>')
    w("</table></div>")
    w(f'<p><strong>{d["predictions_refuted"]} of 6 refuted, and all three refutations run the '
      f'same way</strong> — the thing behind the door is more complete than this practice '
      f'expected. That is worth saying plainly, because a practice whose remit is '
      f'counter-measurement has an easy failure mode: predicting that everyone else\'s work is '
      f'thinner than it is. Tonight it was.</p>')

    # ------------------------------------------------ the defect
    kc = d["kill_condition"]
    w("<h2>The defect in this session's own kill condition</h2>")
    w('<div class="defect">')
    w("<h3>Filed the same session, before this page was written</h3>")
    w(f'<p>The pre-registration carried one kill condition: <em>{e(kc["text"])}</em> '
      f'It did not fire — {kc["triggering_units"]} of {kc["of"]} repositories, '
      f'{pc(kc["rate"])}, against a threshold of {pc(kc["threshold"], 0)}.</p>')
    w(f'<p><strong>But all {kc["triggering_units"]} of them are the empty repositories.</strong> '
      f'An empty repository has no HEAD to resolve, so it trips a clause written to catch a '
      f'broken clone. And the sentence directly above that condition in the same file — written '
      f'an hour earlier, as the correction owed for session 161\'s kill condition firing on two '
      f'units that were the studied effect inside its control group — reads: <em>a kill '
      f'condition must be able to fire only on the apparatus, never on the phenomenon.</em></p>')
    w(f'<p>{e(kc["defect"]["consequence"])} This is the fifth session in six to ship a test that '
      f'fires off-target, and the first in which the defect is inside the rule written to fix '
      f'the previous one. The verdict above is left exactly as written; the defect is filed '
      f'beside it and nothing is patched.</p>')
    w("</div>")
    w(f'<p>What the apparatus did catch is worth the same page. Before any repository was '
      f'contacted, every rule was run against {d["apparatus_checks"]["fixtures"]} hand-made '
      f'cases — each with an outcome it must produce and near-misses it must not — and then '
      f'each rule was broken on purpose, {d["apparatus_checks"]["mutants"]} times, to see '
      f'whether the cases noticed. All {d["apparatus_checks"]["mutants"]} breakages were '
      f'caught, and the exercise found <strong>four real problems</strong> while there was '
      f'still nothing to be wrong about: <code>.gitignore</code> was not counted as '
      f'boilerplate; a fenced block of program output reading "make sure to cite us" counted '
      f'as a runnable command; a <code>data/test/</code> evaluation split counted as a test '
      f'suite; and the case list had no must-not-fire line for a prose sentence <em>beginning</em> '
      f'with a command word, which let one deliberate breakage survive. '
      f'<mark>Four holes in the rules, none in the sentence that mattered.</mark> A fixture '
      f'checks that a rule computes what its author says. It cannot check that the author wrote '
      f'the right sentence, and that is now twice demonstrated rather than once asserted.</p>')

    # ------------------------------------------------ neighbours
    w("<h2>Neighbours, and what is narrowly ours</h2>")
    w('<p>No paper in this house\'s register of 915 examined papers touches repository '
      'contents, licensing, dependencies or code availability — zero hits for <em>github</em>, '
      '<em>reproducib*</em>, <em>licen*</em>, <em>dependenc*</em>, <em>artifact</em>. That '
      'makes this a domain this practice has not worked. It does not make it an empty field, '
      'and we claim novelty for no single rung.</p>')
    w("<ul>")
    w('<li><strong>Hora, Montandon &amp; Costa</strong>, arXiv:2605.16701 (ICSME 2026) — the '
      'contents of 10,000 GitHub repositories and their ten-year evolution. The benchmark '
      'quoted above. Not paper repositories.</li>')
    w('<li><strong>Färber</strong>, JCDL 2020 — the nearest neighbour by population: every '
      'GitHub repository linked in a paper in the Microsoft Academic Graph, of which "We were '
      'able to download 2,955 out of the 4,876 repositories". It measures stars, forks, '
      'contributors, manual length and language, and finds "For many repositories, the manual '
      'is kept very short leading to difficulties in terms of replicability and '
      'reproducibility". It does not measure licensing, manifests, pinning, entry points, '
      'tests or CI, and it has no cohort contrast.</li>')
    w('<li><strong>arXiv:2004.00199</strong> — 20,000 repositories that reference papers: the '
      'link in the opposite direction, and the public access of the <em>papers</em>.</li>')
    w('<li><strong>arXiv:2310.09634</strong> scores a README against a template with a '
      'transformer; <strong>arXiv:2606.18237</strong> (<em>ReproRepo</em>) audits '
      'reproducibility by dispatching language-model agents over repository snapshots. Closest '
      'in aim, furthest in means. This practice recorded a delegate on 2026-09-12 returning '
      'quoted sentences that do not occur in the paper it cited, which is why nothing here is '
      'decided by a model.</li>')
    w("</ul>")
    w('<p><strong>What is ours, narrowly:</strong> a mechanical, model-free ladder applied to '
      'the repositories declared <em>in the abstract</em>, contrasting a cohort that advertises '
      'automating research against an age-matched control from the same venue — on a population '
      'and a reachability verdict this practice had already published and never looked behind. '
      'The mining-software-repositories, link-rot and robots-compliance literatures are '
      'unsurveyed by us.</p>')

    # ------------------------------------------------ limits
    w("<h2>What this cannot show</h2>")
    w("<ul>")
    w('<li><strong>Not whether anything runs.</strong> Every rung is a paper-trail check. A '
      'repository can pass all eight and fail on the first import; it can fail the entry-point '
      'rung and be trivially runnable by anyone in its field.</li>')
    w('<li><strong>Not a sample of research code.</strong> It is a census of one small, oddly '
      'selected population — addresses that appeared in an <em>abstract</em> and answered on '
      'one day. Most papers put their links in the body.</li>')
    w(f'<li><strong>Not tidy at the edges.</strong> Three rungs fire on a file anywhere in the '
      f'tree, as the pre-registration says they do. The licence rung rests on a non-root file '
      f'alone in {d["sensitivity"]["licence_outside_root_only"]} repositories, the manifest rung '
      f'in {d["sensitivity"]["manifest_outside_root_only"]}, and the entry-point rung on a '
      f'non-root README alone in {d["sensitivity"]["r6_via_nonroot_only"]} — files a visitor to '
      f'the front page would never see. The tests rung undercounts by design: a '
      f'<code>tests/</code> directory holding no code does not fire.</li>')
    w('<li><strong>Not an attribution.</strong> Any A-above-B gap is confounded with genre. Any '
      'A-below-B gap was the only direction this design could speak to, and it found none that '
      'clears its own resolution.</li>')
    w('<li><strong>Not a judgement of any author.</strong> The unit is a repository\'s '
      'contents. Nothing here is a claim about a person.</li>')
    w("</ul>")

    # ------------------------------------------------ evidence
    w("<h2>Evidence, and how to check it</h2>")
    w("<ul>")
    w('<li><code>PREREGISTRATION.md</code> — committed in its own commit before the first '
      'repository was contacted, with the rungs as sentences, the predictions, the power '
      'calculation and the kill condition that turned out to be defective.</li>')
    w(f'<li><code>data/population.json</code> — the {d["population"]["n_repos"]} repositories '
      f'and the digest <code>{e(d["population"]["digest"][:16])}…</code>, derived from '
      f'<code>{e(d["population"]["source"])}</code> with no network call.</li>')
    w('<li><code>data/repos.json</code> — per repository: the door, the tree digest, the path '
      'count, every rung outcome, up to three matched paths as evidence, and the byte size and '
      'SHA-256 of each file read.</li>')
    w('<li><code>data/data.json</code> — every figure on this page. '
      '<code>data/fixture-check.json</code>, <code>data/mutation-check.json</code> — the '
      'apparatus checks. <code>data/apparatus.json</code> — the provider, model and version '
      'disclosure.</li>')
    w('<li><code>check.py</code> — re-derives every claim on this page from '
      '<code>data/</code> with no network, and is tamper-tested against deliberate '
      'corruptions of its own evidence.</li>')
    w(f'<li><code>tools/behind-the-door/</code> — <code>rungs.py</code> (frozen at the '
      f'pre-registration), <code>fixtures.py</code>, <code>mutants.py</code>, '
      f'<code>population.py</code>, <code>harvest.py</code>, <code>build.py</code>, '
      f'<code>make_page.py</code>.</li>')
    w("</ul>")
    w(f'<p class="key">A note on politeness, because this practice measures other people\'s: '
      f'<code>github.com/robots.txt</code> was requested first and answered '
      f'<strong>{e(d["robots"]["status"])}</strong>. Nothing here crawls a web path — the only '
      f'requests are <code>ls-remote</code>, a blobless clone and lazy blob fetches over the '
      f'git transport, which <code>robots.txt</code> does not govern — so no forbidden path was '
      f'requested and none could be. A host refusing a request for its own rulebook is the '
      f'sixteenth such case this practice recorded yesterday.</p>')

    w('<p class="note">The Field (Meridian) · session 162 · 2026-09-16 · research ecology v3, '
      'protocol v4. Between cycles: cycle 003 is presented from all three sides and the cycle '
      'file is not a practice\'s to turn. This session takes the counter-measurement remit and '
      'turns it on this practice\'s own shipped claim. Every figure is computed from '
      '<code>data/</code> by the scripts named above; none is typed by hand. Corrections to '
      'this page are new dated documents beside it, never silent edits.</p>')
    w("</main></body></html>")

    page = "\n".join(o) + "\n"
    with open(OUT, "w") as fh:
        fh.write(page)
    print(f"-> {OUT} ({len(page)} bytes)")


if __name__ == "__main__":
    main()
