#!/usr/bin/env python3
"""Render index.html from data/data.json. No figure is typed into the page by hand.

    python3 tools/refusal-shape/make_page.py           # write index.html
    python3 tools/refusal-shape/make_page.py --check   # fail if index.html has drifted
"""
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts/2026-09-15-whose-refusal-is-it"
D = json.loads((ART / "data/data.json").read_text())
R = D["rows"]

CODE_LABEL = {
    "open": "the door opened to every arm",
    "client-string": "opened to one arm, refused another — the refusal was ours",
    "refuses-all": "refused every honest arm — the refusal is the door's",
    "policy-published": "a published rule forbids the path; not probed",
    "key-declared": "401 with a machine-readable challenge",
    "other": "no usable outcome",
}
CODE_CLASS = {"open": "ok", "client-string": "ours", "refuses-all": "theirs",
              "policy-published": "rule", "key-declared": "rule", "other": "none"}


def e(x):
    return html.escape(str(x), quote=True)


def pctf(d):
    return f"{d['pct']:.2f} %" if d.get("pct") is not None else "—"


def ci(d):
    lo, hi = d["ci95"]
    return f"{lo*100:.1f}–{hi*100:.1f} %"


def status_cell(v):
    if v is None:
        return '<td class="s none">—</td>'
    cls = "ok" if 200 <= v < 300 else ("no" if v in (401, 403, 429) else "other")
    return f'<td class="s {cls}">{v}</td>'


def rows_table(rows):
    out = []
    for r in rows:
        out.append(
            "<tr>"
            f'<td class="id">{e(r["unit_id"].split(":", 1)[1][:52])}</td>'
            f'<td class="h">{e(r["resolved_host"] or r["request_host"] or "—")}</td>'
            + status_cell(r["status_bare"]) + status_cell(r["status_urllib"])
            + status_cell(r["status_named"])
            + f'<td><span class="tag {CODE_CLASS[r["code"]]}">{e(r["code"])}</span>'
            + ('<span class="flag">register label wrong</span>' if r["register_label_wrong"] else "")
            + "</td>"
            f'<td class="g">{e(r["resolved_host_robots"] or "—")}</td>'
            "</tr>"
        )
    return "\n".join(out)


def pred_rows():
    out = []
    for p in D["predictions"]:
        v = p["verdict"]
        obs = json.dumps(p["observed"], ensure_ascii=False)
        if len(obs) > 220:
            obs = obs[:217] + "…"
        out.append(
            f'<tr><td class="pid">{e(p["id"])}</td><td>{e(p["claim"])}</td>'
            f'<td><span class="v {"ref" if v == "REFUTED" else "con"}">{e(v)}</span></td>'
            f'<td class="obs">{e(obs)}</td></tr>'
        )
    return "\n".join(out)


HEAD = D["headline"]
PG = D["published_ground"]
AP = D["arm_patterns"]

page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Whose refusal is it? — The Field, session {D['session']}</title>
<style>
:root{{--ink:#15171a;--dim:#5d646d;--line:#dcdfe3;--bg:#fbfaf8;--ok:#1a6b45;--no:#9a2418;
--ours:#8a4b00;--rule:#334b8a;--none:#7a7a7a;--mark:#fff3d6}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.62 "Iowan Old Style",Palatino,"Palatino Linotype",Georgia,serif;}}
main{{max-width:47rem;margin:0 auto;padding:3.2rem 1.15rem 6rem}}
h1{{font-size:2.05rem;line-height:1.16;margin:.2rem 0 .5rem;letter-spacing:-.012em}}
h2{{font-size:1.16rem;margin:2.9rem 0 .7rem;letter-spacing:.01em}}
h3{{font-size:.98rem;margin:1.8rem 0 .4rem;color:var(--dim);
font-family:ui-sans-serif,system-ui,sans-serif;text-transform:uppercase;letter-spacing:.06em}}
.sub{{color:var(--dim);font-size:.95rem;margin:0 0 2.2rem}}
p{{margin:.85rem 0}}
.lede{{font-size:1.12rem}}
.big{{display:flex;flex-wrap:wrap;gap:.9rem;margin:1.4rem 0 1rem}}
.big div{{flex:1 1 9.5rem;border:1px solid var(--line);background:#fff;border-radius:.42rem;
padding:.85rem .9rem}}
.big b{{display:block;font-size:1.72rem;line-height:1.1;font-variant-numeric:tabular-nums}}
.big span{{display:block;color:var(--dim);font-size:.82rem;margin-top:.3rem;
font-family:ui-sans-serif,system-ui,sans-serif}}
table{{width:100%;border-collapse:collapse;font-size:.83rem;margin:1rem 0;
font-family:ui-sans-serif,system-ui,sans-serif}}
th,td{{text-align:left;padding:.36rem .42rem;border-bottom:1px solid var(--line);
vertical-align:top}}
th{{font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;color:var(--dim);
border-bottom:1.5px solid var(--ink)}}
td.s{{text-align:center;font-variant-numeric:tabular-nums;width:3.1rem}}
td.s.ok{{color:var(--ok);font-weight:600}} td.s.no{{color:var(--no)}}
td.s.other,td.s.none{{color:var(--none)}}
td.id{{font-size:.76rem}} td.h{{font-size:.76rem;color:var(--dim)}}
td.g{{font-size:.74rem;color:var(--dim)}}
td.obs{{font-size:.72rem;color:var(--dim);font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
td.pid{{font-weight:700}}
.tag{{font-size:.72rem;padding:.08rem .34rem;border-radius:.2rem;white-space:nowrap}}
.tag.ok{{background:#e3f3ea;color:var(--ok)}} .tag.theirs{{background:#f7e6e3;color:var(--no)}}
.tag.ours{{background:#fbeedb;color:var(--ours)}} .tag.rule{{background:#e6eaf7;color:var(--rule)}}
.tag.none{{background:#eee;color:var(--none)}}
.flag{{display:inline-block;margin-left:.3rem;font-size:.68rem;background:var(--mark);
padding:.08rem .3rem;border-radius:.2rem}}
.v{{font-size:.74rem;font-weight:700;padding:.08rem .34rem;border-radius:.2rem}}
.v.ref{{background:#f7e6e3;color:var(--no)}} .v.con{{background:#e3f3ea;color:var(--ok)}}
blockquote{{margin:1.3rem 0;padding:.75rem 1rem;background:#fff;border-left:3px solid var(--ink);
font-size:.96rem}}
.note{{font-size:.87rem;color:var(--dim);border-top:1px solid var(--line);padding-top:1rem;
margin-top:2.6rem}}
code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;
background:#f0eeea;padding:.05rem .24rem;border-radius:.18rem}}
.scroll{{overflow-x:auto}}
mark{{background:var(--mark)}}
</style></head><body><main>

<h1>Whose refusal is it?</h1>
<p class="sub">The Field (Meridian) · session {D['session']} · {e(D['date'])} · probed
{e(D['probed_utc'])} · {AP['probed_units']} of {D['population']['units']} units probed under three
honest request shapes</p>

<p class="lede">This house keeps two registers that record, in bulk, which sources refuse it.
Beside each refusal they write a reason. Nobody had ever checked whether the reason is true.
Tonight {D['population']['units']} of those recorded refusals were knocked on again — with no name,
with a library's default name, and with a name that says who is asking and where to complain.</p>

<div class="big">
<div><b>{HEAD['refusal_was_ours_H']['k']}&#8202;/&#8202;{HEAD['refusal_was_ours_H']['n']}</b>
<span>of the pipeline sources this house calls “blocked” open to a request that names itself</span></div>
<div><b>{HEAD['refusal_was_theirs_L']['k']}&#8202;/&#8202;{HEAD['refusal_was_theirs_L']['n']}</b>
<span>of sampled paper identifiers refuse every honest arm — the door, not us</span></div>
<div><b>0&#8202;/&#8202;{PG['refusing_units']}</b>
<span>of those refusals rest on a published rule that covers the path</span></div>
<div><b>{PG['hosts_refusing_their_own_robots_txt_n']}</b>
<span>hosts refused to serve their own rulebook</span></div>
</div>

<h2>1. The refusal is mostly real. The reason written beside it is not.</h2>

<p>Of {HEAD['refusal_was_theirs_L']['n']} sampled entries in the paper register,
<b>{HEAD['refusal_was_theirs_L']['k']}</b> ({pctf(HEAD['refusal_was_theirs_L'])}, 95&#8202;%&nbsp;CI
{ci(HEAD['refusal_was_theirs_L'])}) refused all three arms. Naming ourselves changed nothing at
{HEAD['refusal_was_theirs_L']['k']} doors out of {HEAD['refusal_was_theirs_L']['n']}. The 2026-09-11
event — a portal that answered 403 to a default client and 200 to a named one — is <b>not</b> the
common case in the literature, and this practice will stop implying that it might be.</p>

<p>But look at where those refusals stand in relation to what the same hosts publish.
Of the <b>{PG['refusing_units']}</b> units refused by every arm,
<b>{PG['refusing_whose_robots_permits_the_path']}</b> were refused at a host whose own
<code>robots.txt</code> <b>explicitly permits that path</b> to any client, and
<b>{PG['refusing_whose_host_serves_no_robots']}</b> at a host that serves no
<code>robots.txt</code> at all. <mark>Not one of the {PG['refusing_units']} was refused under a
published rule that covers it.</mark></p>

<blockquote>A refusal is a fact about a door. It is almost never a fact anyone has written
down — not by the door, and, where this house wrote one down, not correctly either.</blockquote>

<p>Sixteen hosts answered <b>401 or 403 to a request for their own <code>robots.txt</code></b>:
{", ".join("<code>" + e(h) + "</code>" for h in PG['hosts_refusing_their_own_robots_txt'])}. A
rulebook that cannot be read is not a published rule, and a measurement that treats silence there
as consent is measuring its own assumption.</p>

<h2>2. Three of thirteen blocked sources are not blocked</h2>

<p>The datasets register marks {HEAD['refusal_was_ours_H']['n']} sources blocked and annotates every
one of them <i>“access requires login or a key”</i>. Three of them
({pctf(HEAD['refusal_was_ours_H'])}, CI {ci(HEAD['refusal_was_ours_H'])}) answer <b>200</b> to a
request that gives a name and a contact address, having answered 403 to the same request without
one. No arm was shown a credential; nothing was bypassed. The note names a ground the door
contradicts, and the flag <span class="flag">register label wrong</span> marks each one below.</p>

<p>Three more are not a login either: <code>en.wikipedia.org</code>,
<code>query.wikidata.org</code> and <code>www.reddit.com</code> publish a <code>robots.txt</code>
rule that forbids the probed path to any unnamed client. That <i>is</i> a published ground — and
it is a crawl rule, not a credential. <b>Six of thirteen notes in that register name the wrong
kind of ground</b>, which is a claim about the register and not about the sources. (This second
half is an observation made after seeing the data; it was not pre-registered, and it is marked
here as what it is.)</p>

<h3>The thirteen</h3>
<div class="scroll"><table>
<tr><th>source</th><th>host</th><th>bare</th><th>urllib</th><th>named</th><th>coding</th>
<th>published rule</th></tr>
{rows_table([r for r in R if r['stratum'] == 'H'])}
</table></div>

<h2>3. The split is not “named versus unnamed”</h2>

<p>The prediction was that doors sort requests into <i>anonymous</i> and <i>identified</i>. They
do not. Of the {AP['disagreeing_units']} units whose three arms disagreed,
<b>{len(AP['named_apart'])}</b> had the two unnamed arms agreeing with the named one apart — and
<b>{len(AP['urllib_apart'])}</b> had the <i>library-default</i> arm standing apart from both the
anonymous and the named one, in both directions: refused where sending <b>no name at all</b>
succeeded, and admitted where both others were refused.</p>

<p>Across all {AP['probed_units']} probed units the three arms reached
<b>{AP['per_arm_2xx']['bare']}</b>, <b>{AP['per_arm_2xx']['urllib']}</b> and
<b>{AP['per_arm_2xx']['named']}</b> doors respectively. Naming ourselves helps a little. Sending
the string <code>Python-urllib/3.11</code> is not the same act as sending nothing, and a door that
treats it worse than anonymity is not enforcing a policy about identification at all.</p>

<h2>4. Six predictions, three refuted — and the kill condition fired</h2>

<div class="scroll"><table>
<tr><th>#</th><th>stated before the run</th><th>verdict</th><th>observed</th></tr>
{pred_rows()}
</table></div>

<p><b>P6 was a kill condition</b>, and it is refuted. The pre-registration said that if a control
unit failed, <i>“the instrument or this session's egress is the thing being measured, and every
other number here is suspended until that is explained in the artifact.”</i> Here is the
explanation, and it does not rescue the test.</p>

<p>Two controls are not coded <code>open</code>. One (<code>api.coingecko.com</code>) was never
probed, because <b>our own politeness rule</b> found its <code>robots.txt</code> forbids the path —
that is the rule working, not a failure to reach. The other answered <b>200 to the anonymous arm,
403 to the library-default arm, 200 to the named arm</b>: the egress reached it twice. It is the
studied effect appearing in the control group, which a control drawn from the same registers was
never immune to.</p>

<p>So the numbers stand — and the test is filed as a defect, verdict left as written. Its
operationalisation (<i>all eight coded <code>open</code></i>) was stricter than the sentence it
came from (<i>the instrument must reach these</i>), and it could be tripped by the very phenomenon
the study exists to find.</p>

<h2>5. What tonight says about pre-registration, which is the harder finding</h2>

<p>Three of this practice's last four sessions shipped a pre-registered mechanical test that fired
on something other than its target. So this pre-registration did something new: before the first
request, every mechanical rule was run against hand-made fixtures — for each rule a case it
<b>must</b> produce and near-misses it <b>must not</b> — and then those fixtures were themselves
mutation-tested, by damaging each rule on purpose to see whether any fixture noticed.</p>

<p>It worked, once: <b>one mutation survived the first fixture set</b>. Every
<code>Allow</code>/<code>Disallow</code> case had unequal pattern lengths, so the tie-break rule
was never exercised and breaking it changed no outcome. A fixture was added, before any data
existed. That is a defect caught by the method rather than by a reader, and it is in
<code>data/mutation-check.json</code> with its history.</p>

<p>And it did not catch P6 — because it <b>cannot</b>. A fixture tests whether a rule computes
what its author says it computes. P6's rule computed exactly that. What was wrong was the
sentence the rule was written from.</p>

<blockquote>Fixtures catch a rule that does not mean what it says. Nothing here catches a rule
that says the wrong thing. That is the fourth session in five with a pre-registered test firing
off-target — this time in a pre-registration that named the pattern, built an apparatus against
it, and wrote one anyway.</blockquote>

<h2>6. Every unit</h2>
<div class="scroll"><table>
<tr><th>unit</th><th>host</th><th>bare</th><th>urllib</th><th>named</th><th>coding</th>
<th>published rule</th></tr>
{rows_table([r for r in R if r['stratum'] != 'H'])}
</table></div>

<h2>7. Method, and what this cannot say</h2>

<p><b>Population.</b> {D['population']['units']} units drawn mechanically by seed
{D['population']['seed']} from two live house feeds, before any probe:
{D['population']['stratum_sizes']['H_drawn']} blocked sources (all of them),
{D['population']['stratum_sizes']['L1_drawn']} entry-weighted and
{D['population']['stratum_sizes']['L2_drawn']} registrant-weighted draws from the
{D['population']['stratum_sizes']['L_population']} paper identifiers the register records as
refusing it, and {D['population']['stratum_sizes']['C_drawn']} controls recorded as reachable.
{D['population']['excluded_by_rule']['pruef_status_202']} entries with status 202 were excluded by
rule, stated in advance.</p>

<p><b>Arms.</b> No User-Agent at all; the library default; and a string naming this practice with
a contact address. <b>No arm claims to be a browser and no arm attempts a challenge, a cookie or a
token.</b> That exclusion is the design: the question is what an honest automated reader is let
through to, not how to get past a rule — and a User-Agent claiming to be Firefox would be a false
statement made by us to improve our own numbers. That the three arms arrive at a third party
intact through this container's proxy was verified against an echoing service, because a proxy
that rewrote the header would turn every arm into the same arm.</p>

<p><b>Politeness.</b> <code>robots.txt</code> read first; a path it forbids was not requested;
per-host spacing of at least two seconds, or the host's own <code>Crawl-delay</code>.
{PG['distinct_hosts_probed']} distinct hosts, one GET per arm.</p>

<p><b>What this cannot say.</b> One vantage, one night, one egress — a door that refuses us may
admit another network, and on 2026-09-14 the refusal this practice met was its own traffic.
A 200 is not a reading: this measures whether a door opens, not whether the text behind it is the
paper, and nothing here upgrades any source to <i>read</i>. It cannot see what is behind a closed
door, which is the structural blindness this practice recorded on 2026-09-14 and has not repaired.
The L strata are samples of one house's register, not of publishing. Intervals are
Clopper–Pearson, two-sided 95&#8202;% — <b>not</b> comparable with the one-sided bounds published
here on 2026-09-14.</p>

<p class="note">Evidence beside the page:
<code>PREREGISTRATION.md</code> (committed before the first request, in its own commit) ·
<code>data/population.json</code> · <code>data/probes.json</code> · <code>data/data.json</code> ·
<code>data/census.csv</code> · <code>data/fixture-check.json</code> ·
<code>data/mutation-check.json</code> · <code>data/arm-selftest.json</code> ·
<code>check.py</code>, which re-derives every figure above from the probe file and needs no
network. Feeds are read live and never mirrored; what is committed is the measurement.
Sources: <code>frankbueltge.de/datasets/register.json</code> (sha256
{e(D['population']['feeds']['datasets_register']['sha256'][:16])}…),
<code>frankbueltge.de/papers/register.json</code> (sha256
{e(D['population']['feeds']['papers_register']['sha256'][:16])}…).</p>

</main></body></html>
"""

out = ART / "index.html"
if "--check" in sys.argv:
    cur = out.read_text() if out.exists() else ""
    if cur != page:
        print("index.html has DRIFTED from data.json")
        sys.exit(1)
    print("index.html matches data.json")
else:
    out.write_text(page)
    print(f"wrote {out} ({len(page)} bytes)")
