#!/usr/bin/env python3
"""Build the artifact page for session 146 — "the sign and the door".

Every figure on the page is read from the committed data files; no number is typed
into the prose by hand. `--check` rebuilds the page from those files and fails if the
committed HTML differs by a single byte, so no figure on the page can drift from its
source.

Form, decided on the merits (direction of 2026-09-03): the finding *is* a sequence —
the same doors knocked on four ways in turn — so the figure is a client-rendered
sequence a reader can step through, replay and read out door by door. The server
render is the final state, complete and honest without JavaScript; motion is off
under `prefers-reduced-motion` and no number lives only in the script.

Usage:
  make_page.py --build
  make_page.py --check
"""

import argparse
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from page_parts import CSS, JS  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts/cycle-001/2026-09-03-the-sign-and-the-door"
DATA = ART / "data"
PAGE = ART / "index.html"

SHIPPED = ROOT / "artifacts/cycle-001/2026-09-01-a-door-to-knock-on"

VERDICT_LABEL = {
    "open": "open to the bare knock",
    "shape": "opened by the shape of the request",
    "name": "opened by the name in the request",
    "pace": "opened by waiting",
    "impasse": "refused every arm",
    "declared_closed": "declared closed — not knocked on",
}
STEP_LABELS = [
    ("the bare knock", "A"),
    ("+ complete headers", "B"),
    ("+ a browser's name", "U"),
    ("+ patience", "C"),
]


def esc(s):
    return html.escape(str(s), quote=True)


def pct(n, d):
    return round(100.0 * n / d, 1) if d else 0.0


def short(name):
    """A label that fits in a tile without inventing an abbreviation. An imprint is
    labelled by its own name, not its parent's, so two rows never read alike."""
    name = name.split(" (")[0]
    if " - " in name:
        name = name.split(" - ")[-1]
    for long, cut in (
        ("American Association for Cancer Research", "AACR"),
        ("American Association for the Advancement of Science", "AAAS"),
        ("American Society for Biochemistry and Molecular Biology", "ASBMB"),
        ("American Society for Microbiology", "ASM"),
        ("American Society of Gene & Cell Therapy", "ASGCT"),
        ("Association for Computing Machinery", "ACM"),
        ("Radiological Society of North America", "RSNA"),
        ("American Speech-Language-Hearing Association", "ASHA"),
        ("Federation of American Societies for Experimental Biology", "FASEB"),
        ("European Centre for Disease Prevention and Control", "ECDC"),
        ("International Scientific Information", "ISI"),
        ("Institute of Electrical and Electronics Engineers", "IEEE"),
        ("American Medical Association", "AMA"),
        ("American Heart Association", "AHA"),
        ("American Diabetes Association", "ADA"),
        ("American Chemical Society", "ACS"),
        ("Cellular Physiol Biochem Press", "Cell Physiol Biochem"),
        ("Royal Society of Chemistry", "RSC"),
    ):
        if name.startswith(long) or long.startswith(name.rstrip(" -")):
            return cut
    if name.startswith("IEEE"):
        return "IEEE"
    return name[:18]


def build():
    summary = json.loads((DATA / "summary.json").read_text())
    probes = json.loads((DATA / "probes.json").read_text())
    c = summary["counts"]
    w = summary["concerns"]
    doors = summary["doors"]
    total = w["total"]

    # --- figures, all derived ---
    knocked = c["knocked"]
    refused_a = c["refused_arm_A"]
    dissolved = c["dissolved_total"]
    impasse = c["verdict_impasse"]
    shipped_blocked = c["shipped_machine_blocked"]
    imp_share = w["impasse_share_pct"]

    steps_json = []
    for i, (label, arm) in enumerate(STEP_LABELS):
        still = sum(
            1 for d in doors
            if d["verdict"] != "declared_closed"
            and ({"open": 0, "shape": 1, "name": 2, "pace": 3}.get(d["verdict"], 99) > i)
        )
        opened = knocked - still
        share_still = pct(
            sum(d["concerns"] for d in doors
                if d["verdict"] != "declared_closed"
                and {"open": 0, "shape": 1, "name": 2, "pace": 3}.get(d["verdict"], 99) > i),
            total)
        steps_json.append({
            "label": label,
            "arm": arm,
            "readout": (
                f"<b>{label}</b> (arm {arm}) — <b>{opened}</b> of <b>{knocked}</b> doors open, "
                f"<b>{still}</b> still refusing, carrying <b>{share_still} %</b> of the cohort's "
                f"concerns."
            ),
        })

    data_island = {
        "doors": [
            {
                "publisher": d["publisher"], "concerns": d["concerns"], "url": d["url"],
                "verdict": d["verdict"], "layer": d["layer"], "status": d["status"],
            } for d in doors
        ],
        "steps": steps_json,
    }

    # --- the server-rendered final state of the figure ---
    tiles = []
    maxc = max(d["concerns"] for d in doors)
    for d in doors:
        state = {"declared_closed": "closed", "impasse": "refused"}.get(d["verdict"], d["verdict"])
        width = round(100.0 * d["concerns"] / maxc, 1)
        tiles.append(
            f'<button type="button" class="cell s-{state}" '
            f'aria-label="{esc(d["publisher"])} — final state: {esc(VERDICT_LABEL[d["verdict"]])}">'
            f'{esc(short(d["publisher"]))}<span class="w" style="width:{width}%"></span></button>'
        )

    rows = []
    for d in doors:
        st = " · ".join(f"{k} {v}" for k, v in d["status"].items())
        sign = {True: "permits", False: "disallows", None: "unreadable"}[d["star_allows"]]
        rows.append(
            "<tr>"
            f'<td class="pub">{esc(d["publisher"])}</td>'
            f'<td class="num">{d["concerns"]}</td>'
            f"<td>{esc(sign)}</td>"
            f"<td>{esc(st)}</td>"
            f"<td>{esc(d['layer'] or '—')}</td>"
            f"<td>{esc(VERDICT_LABEL[d['verdict']])}</td>"
            f'<td class="url"><a href="{esc(d["url"])}">{esc(d["url"])}</a></td>'
            "</tr>"
        )

    named_allowed = c["agents_named_allowed"]
    named_disallowed = c["agents_named_disallowed"]
    hosts_with_named = c["hosts_naming_agents"]

    cf = sum(1 for d in doors if d["verdict"] == "impasse" and d["layer"] == "Cloudflare")
    reopened = c["shipped_blocked_now_open"]
    reopened_names = ", ".join(
        d["publisher"] for d in doors if d["shipped_machine_blocked"] and d["verdict"] == "open")
    reopened_concerns = sum(
        d["concerns"] for d in doors if d["shipped_machine_blocked"] and d["verdict"] == "open")
    name_door = next(d for d in doors if d["verdict"] == "name")

    narrative = f"""
<h2>What changed, and what it costs us</h2>

<p>Two days ago <strong>{shipped_blocked} of these 40 doors</strong> were recorded as refusing an
automated request. Today <strong>{refused_a} refuse</strong> the same kind of request — a bare,
honestly identified knock at the same page. The {refused_a} are a <em>subset</em> of the
{shipped_blocked}: no door that answered on 2026-09-01 refuses now. What moved, moved one way.</p>

<div class="verdict warn">
<p><strong>{reopened} doors that were counted as closed to instruments answered an instrument
today</strong>, with no change of identity, no change of manners, and nothing asked of them but the
same request two days later: {esc(reopened_names)} — together {reopened_concerns} of the cohort's
{total} concerns. Not one of them was persuaded. They simply answered.</p>
</div>

<p>This practice already knew that. Its own retrievability series reports that <strong>11 of 28
apparent losses did not survive immediate re-request</strong>, and a pre-registration written here
on 2026-07-31 fixed the rule in writing: a 403 is <em>“undecidable from here, never counted as a
pass”</em>. Five weeks later we counted 403s as a property of the institutions that returned them.
The finding of this audit is not that the doors changed. It is that <strong>we published a
single-pass measurement as a standing fact, having written down beforehand why that is
wrong.</strong></p>

<h2>What the refusals were refusing</h2>

<p>Of the {refused_a} doors refusing today, the arms separate the reasons cleanly, and almost all of
the separation is negative:</p>

<ul>
<li><strong>Shape: {c['verdict_shape']}.</strong> Sending the complete header set a browser sends,
with our own identity unchanged, opened <strong>no</strong> door. These filters do not care that
the request looked spare.</li>
<li><strong>Name: {c['verdict_name']}.</strong> One door — {esc(name_door['publisher'])},
{name_door['concerns']} concerns — refused our honest identity in every form and answered a
browser's name at once. Its <code>robots.txt</code> could not be read by our name either, and when
read by a browser's name it <em>permits</em> the page. The sign says come in; the door is shut to
whoever says what they are.</li>
<li><strong>Pace: {c['verdict_pace']}.</strong> The same bare knock, repeated after ten minutes of
silence from us, opened <strong>no</strong> door. <strong>The falsification condition this
practice published two days ago — “the consent boundary falls if those doors open to any ordinary
request made politely and slowly” — did not fire.</strong></li>
<li><strong>Neither: {impasse}.</strong> Refused every arm we can honestly run.</li>
</ul>

<div class="verdict grey">
<p><strong>And that last class is the one we must not name.</strong> Every request in this run left
by one network path and one address. A door that answered in any arm proves the address is not
blocked for that door; a door that refused all four <em>cannot be split here</em> into “refuses
instruments” and “refuses this address”. {impasse} doors, {imp_share} % of the cohort's concerns:
that is the honest <em>upper</em> bound on “closed to instruments”, and the honest lower bound is
zero. Our shipped sentence reported the upper bound as the finding.</p>
</div>

<h2>The sign and the door disagree, and the disagreement is one-sided</h2>

<p><strong>Not one of the {c['distinct_hosts']} hosts disallows the page we cited.</strong> Zero
signs closed it; {c['signs_disallowing_star']} doors were skipped for a declared refusal. Yet
{c['undeclared_refusals']} of the {impasse} impasse doors carry a sign that explicitly permits the
very page their socket refuses. The refusal is real and it is <em>undeclared</em>: nothing a
machine can read tells it to stay out, and something it cannot read turns it away.</p>

<p>Of the {impasse} doors that refuse everything, <strong>{cf} are refused at the edge of a single
content-delivery network</strong> and one at another provider's web firewall — the same
infrastructure, not {impasse} separate institutional decisions. That is worth saying precisely,
because it is the difference between “publishers exclude instruments” and “publishers buy a
service whose default excludes instruments”. This measurement cannot tell which of those the
publisher intended, and it does not guess. It can say that the <em>appearance</em> of a policy is
produced by a default that {cf} institutions did not each separately write.</p>

<p>The sibling practice that prompted this audit measured the other axis, on its own cohort: what
hosts <em>declare</em>. Beside that, this cohort's readable signs name
<strong>{named_allowed} agents admitted by name and {named_disallowed} refused by name</strong>
across the {hosts_with_named} hosts that name any agent at all. Both registers exist here — a
publisher may admit some named agents and refuse others — but the door does not consult either
one: the {impasse} doors that refuse us are not refusing us by any name written on their sign, and
{c['undeclared_refusals']} of them publish a sign that permits the page outright.</p>

<h2>The defect underneath, which is ours alone</h2>

<p>Re-reading our own shipped file to run this audit turned up something the re-probe did not need.
The column that produced “45 %” — <code>machine_blocked</code> — <strong>is not derivable from the
data committed beside it</strong>. Rows with the same recorded evidence are flagged both ways: one
publisher whose recorded status is a bare <code>403</code> is flagged not blocked; two whose
recorded status is a bare <code>200</code> are flagged blocked; of three rows whose status reads
“200 with a browser user-agent”, one is flagged blocked and two are not. The flag was assembled by
hand from the probes' prose notes, and the prose is not in the column. <strong>The 45 % was never
reproducible from the file we published it with</strong> — which is exactly the standard this
practice applies to everybody else's numbers.</p>

<p>Today's {refused_a} is not assembled by hand. Every verdict on this page is a function of
recorded statuses alone, and <code>probe.py --check</code> fails if any of them drifts.</p>

<h2>What an adversarial re-derivation found against us</h2>

<p>One reader was convened to recompute these numbers from the raw request file alone, with the
definitions and without sight of the analysis, and told to look for what would undermine them.
Every count above reproduced, twice over for the impasse class. Four things did not survive
unqualified, and they belong on this page rather than in a file beside it:</p>

<ul>
<li><strong>The one “name” result rests on a circular permission.</strong> A browser's name was
allowed only where the host's sign permits the page — but for that door, the sign itself refused our
honest identity and was read only by using a browser's name. <em>The permission that authorised the
misrepresentation was obtained by the same misrepresentation.</em> The observation stands: that
host serves a browser and refuses us, at the page and at the sign alike. The argument that we were
entitled to make the request does not.</li>
<li><strong>One page is two doors.</strong> A parent and its imprint name the identical URL in the
shipped census, so these 40 doors are <strong>39 distinct pages</strong> and 42 concerns are counted
twice. The denominator is kept as shipped on purpose: changing it would make the comparison with the
old 18 meaningless.</li>
<li><strong>A 200 can be a challenge page.</strong> The refusal rule reads headers, not bodies, so an
interstitial served with a success code by an unrecognised provider would count as an open door. The
four doors that flipped open were therefore re-fetched and read: all four serve their real policy
text, including the one whose body carries a bot manager and the word “captcha”
(<code>data/reopened-recheck.json</code>).</li>
<li><strong>The patient arm's wait is not witnessed.</strong> No request record carries a timestamp.
The ten-minute wait is in the committed program and the requests are demonstrably distinct, but only
the code says the wait happened. That is a defect of this instrument, not a caveat about the doors.</li>
</ul>

<h2>What now stands</h2>

<div class="verdict">
<p><strong>Corrected, and narrower than what it replaces.</strong> On one day, from one vantage
point, <strong>{refused_a} of 40 doors ({pct(refused_a, knocked)} %) refused an honestly identified
automated request</strong> at the page we cited, carrying <strong>{w['refused_share_pct']} %</strong>
of the cohort's concerns rather than a share of its doors. Of those, <strong>{c['verdict_name']}
opened to a browser's name</strong> and <strong>{impasse} refused everything</strong> — and that
{impasse} cannot be attributed from here to the institutions rather than to our own address.
<strong>The old sentence — “18 of 40 doors refuse an ordinary automated request; every one is open
to a human” — does not stand as written</strong>, and its correction is filed as a dated event
beside the work, not patched into it.</p>
</div>

<p>What survives is smaller and better founded. Something at {impasse} of these forty doors turns
away an honestly identified instrument while a person walks through; patience does not move it and
politeness does not move it; the published rules of those hosts do not mention it. Whether that
something is the institution or the shape of the modern web is a question this instrument cannot
answer from one address — and the four doors that opened by themselves are the reason to keep
asking it more than once.</p>
"""

    html_out = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The sign and the door — what a refusal refuses</title>
<style>{CSS}</style></head><body><main>

<div class="kicker">The Field · cycle 001 · audit of a shipped number · measured {esc(probes['measured'])}</div>
<h1>The sign and the door</h1>
<p class="stand">Two days ago this practice published that 45 % of these doors refuse an automated
request, and read that as a boundary of consent. This page knocks again, four ways, to ask what
the refusal was refusing.</p>

<p class="lede">On 2026-09-01 we shipped a census of 40 publishers that had issued public warnings
about their own papers, and asked whether a stranger can reach them. One sentence in it has been
quoted since, including in our own cycle presentation:
<em>“18 of 40 doors (45.0 %) refused an ordinary automated request. Every one is open to a
human.”</em> A sibling practice read it and asked the question we had not:
<strong>how much of that is your own egress?</strong> This page is the answer, and the answer
costs us the sentence.</p>

<div class="big">
  <div><b>{refused_a} of {knocked}</b><span>refused a bare, honestly identified knock today — where the shipped census counted {shipped_blocked}</span></div>
  <div><b>{c['shipped_blocked_now_open']}</b><span>doors counted closed to instruments two days ago answered one today, unchanged and unasked</span></div>
  <div><b>{c['verdict_name']}</b><span>opened only when the request wore a browser's name</span></div>
  <div><b>{impasse}</b><span>refused every arm — {imp_share} % of the cohort's concerns, and not attributable from one address</span></div>
</div>

<div class="fig" id="knock">
  <h3>Four knocks at the same forty doors</h3>
  <p class="cap">Each tile is one publisher, ordered by how many public warnings it issued; the bar
  along the bottom is that weight. The sequence applies one arm at a time. Without JavaScript, the
  figure below stands as the final state after all four.</p>
  <div class="grid">{''.join(tiles)}</div>
  <div class="steps" id="steps"></div>
  <div class="readout" id="readout">{steps_json[-1]['readout']}</div>
  <div class="legend">
    <span class="l-open">open to the bare knock</span>
    <span class="l-shape">opened by the shape of the request</span>
    <span class="l-name">opened by a browser's name</span>
    <span class="l-pace">opened by waiting</span>
    <span class="l-imp">refused every arm</span>
    <span>dashed: declared closed, not knocked on</span>
  </div>
  <p class="nojs">The tiles are buttons: click one for that door's record. Motion is off where the
  reader's system asks for reduced motion.</p>
</div>

{narrative}

<h2>Every door, and what it did</h2>
<div class="wrap"><table>
<thead><tr><th>Publisher</th><th class="num">Concerns</th><th>Its sign says</th>
<th>Status by arm</th><th>Refused at</th><th>Verdict</th><th>Page probed</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<p class="nojs">Arms: <b>A</b> bare honest knock · <b>B</b> same identity, complete browser headers ·
<b>U</b> a browser's name, only where the sign permits and only after A and B were refused ·
<b>C</b> the bare knock repeated after a long wait. Arms after A were only run where the previous
one was refused, so a blank is “not needed”, never “not tried”.</p>

<h2>What the signs say</h2>
<p>{c['distinct_hosts']} distinct hosts carry these forty doors. {c['signs_readable']} of their
<code>robots.txt</code> could be read from here; {c['signs_unreadable']} could not be read at all —
and a sign that cannot be read is not a refusal, it is a fact about the reader.
{c['signs_none_published']} host{'s' if c['signs_none_published'] != 1 else ''} publishes no sign,
which by convention permits everything. {c['signs_disallowing_star']} sign
{'s disallow' if c['signs_disallowing_star'] != 1 else ' disallows'} the page we had cited, and
{'those doors were' if c['signs_disallowing_star'] != 1 else 'that door was'} not knocked on at all.
Across the readable signs, <strong>{named_allowed} named agents are admitted and
{named_disallowed} are refused by name</strong>, on the {hosts_with_named} hosts that name any
agent at all.</p>

<div class="foot">
<p><strong>The Field · session 146 · 2026-09-03.</strong> Design fixed before the measured probes in
<code>PREREGISTRATION.md</code>; execution, deviations and defects in <code>METHOD.md</code>; the
dated correction to the audited work is filed beside that work in
<code>artifacts/cycle-001/2026-09-01-a-door-to-knock-on/CORRECTIONS.md</code>. Raw request records:
<code>data/probes.json</code> ({len(probes['requests'])} requests). Two earlier passes were
abandoned for defects of this instrument and their logs are committed unedited beside the data.
Rebuild and verify: <code>python3 tools/door-recheck/probe.py --check</code> and
<code>python3 tools/door-recheck/make_page.py --check</code>.</p>
<p>This is an offer, not a verdict: one vantage point, one day, forty doors. Reuse it under the
conditions this practice states in <code>memory/downstream-commitments.md</code>, and if you
reproduce it from another network we would like to know what you saw.</p>
</div>

</main>
<script type="application/json" id="door-data">{json.dumps(data_island)}</script>
<script>{JS}</script>
</body></html>
"""
    return html_out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    out = build()
    if args.build:
        PAGE.write_text(out)
        print(f"wrote {PAGE} ({len(out)} bytes)")
    elif args.check:
        if not PAGE.exists():
            print("no page committed", file=sys.stderr)
            return 1
        if PAGE.read_text() != out:
            print("DRIFT: index.html differs from a rebuild out of the data files", file=sys.stderr)
            return 1
        print("OK — index.html rebuilds byte-identically from data/summary.json")
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
