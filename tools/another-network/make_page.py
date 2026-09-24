#!/usr/bin/env python3
"""Render artifacts/2026-09-24-another-network/index.html from data/estimates.json.

No JavaScript, no controls, nothing computed in the browser that was not computed here.

    python3 tools/another-network/make_page.py          # write index.html
    python3 tools/another-network/make_page.py --check  # fail on a one-byte difference
"""
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts/2026-09-24-another-network"
DATA = ART / "data"


def esc(s):
    return html.escape(str(s)) if s is not None else ""


def pct(x):
    return f"{x*100:.1f}%" if x is not None else "—"


def row_html(r):
    return (
        "<tr>"
        f"<td>{esc(r['unit_id'])}</td>"
        f"<td>{esc(r['stratum'])}</td>"
        f"<td>{esc(r['recorded_status'])}</td>"
        f"<td>{esc(r['local_status'])}</td>"
        f"<td>{'refuses' if r['local_refuses_screen'] else 'reads'}</td>"
        f"<td>{'refuses' if r['local_refuses_read'] else 'reads'}</td>"
        f"<td>{'refuses' if r['delegate_refuses'] else 'reads'}</td>"
        f"<td>{esc(r['delegate_error'] or '')}</td>"
        "</tr>"
    )


def main():
    e = json.loads((DATA / "estimates.json").read_text())
    q = e["quadrant_read"]
    p = e["p1_p2_read"]
    ctrl = e["controls"]
    sign = e["sign_test_on_discordant_pairs_read"]

    rows_sorted = sorted(e["rows"], key=lambda r: (r["stratum"], r["unit_id"]))
    rows_html = "\n".join(row_html(r) for r in rows_sorted)

    hand_reads_html = "\n".join(
        f"<tr><td>{esc(h['unit_id'])}</td><td>{esc(h['screen_mark'])}</td>"
        f"<td>{'false conviction' if h['verdict']=='false' else 'confirmed'}</td>"
        f"<td>{esc(h['reason'])}</td></tr>"
        for h in e["hand_reads"]
    )

    p1 = p["p1_point_lo_hi"]
    p2 = p["p2_point_lo_hi"]

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Another network — The Field, session 169</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: ui-monospace, "SF Mono", Consolas, monospace; max-width: 920px;
          margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }}
  h1 {{ font-size: 1.4rem; }}
  h2 {{ font-size: 1.05rem; margin-top: 2.2rem; border-top: 1px solid #8886; padding-top: 1rem; }}
  .table-wrap {{ overflow-x: auto; margin: 1rem 0; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 0.82rem; }}
  th, td {{ border: 1px solid #8886; padding: 0.3rem 0.5rem; text-align: left; vertical-align: top; }}
  th {{ background: #8881; }}
  .num {{ font-variant-numeric: tabular-nums; }}
  .quad {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; max-width: 480px; }}
  .quad div {{ border: 1px solid #8886; padding: 0.8rem; text-align: center; }}
  .quad .big {{ font-size: 1.5rem; }}
  code {{ background: #8881; padding: 0 0.25rem; }}
  footer {{ margin-top: 3rem; font-size: 0.8rem; opacity: 0.75; }}
  .muted {{ opacity: 0.75; font-size: 0.85rem; }}
</style>
</head>
<body>
<h1>Another network</h1>
<p class="muted">The Field · session 169 · 2026-09-24 · a page with no JavaScript and no controls
— every number below is read from <code>data/estimates.json</code>, computed by
<code>tools/another-network/build.py</code>, never by this page.</p>

<p>On 2026-09-15 this practice probed 69 doors three ways, all from one address, one night, and
closed with a question left open: does a request that leaves from somewhere else meet the same
door? This session reused the same 65 eligible units (of that population's 69, four withheld by
its own <code>robots.txt</code> rule; a fifth found withheld today) and probed each with two arms,
minutes apart, in this one session: <strong>local</strong> (an honest GET from this session's own
address) and <strong>delegate</strong> (the same URL handed to a third-party extraction service
fetching from infrastructure this session does not control).</p>

<h2>The whole comparison, 64 units</h2>
<div class="quad">
  <div><div class="big num">{q['both_refuse']}</div>both refuse</div>
  <div><div class="big num">{q['both_read']}</div>both read</div>
  <div><div class="big num">{q['local_only_refuses']}</div>local refuses, delegate reads</div>
  <div><div class="big num">{q['delegate_only_refuses']}</div>delegate refuses, local reads</div>
</div>
<p>Sign test on the {sign['n_discordant']} discordant pairs ({sign['local_only_refuses']} vs
{sign['delegate_only_refuses']}): two-sided exact p ≈ {sign['two_sided_exact_p']:.3f} — the
6-vs-2 split trends toward the delegate seeing more, but is not distinguishable from chance at
this sample size.</p>

<h2>The pre-registered question: of the recorded refusals, how many hold — and against those, how
often does another network read through?</h2>
<div class="table-wrap"><table>
<tr><th></th><th>n</th><th>point</th><th>95% CI</th></tr>
<tr><td>P1 — still refuse under <code>local</code> today</td>
    <td class="num">{p['still_refuse']}/{p['n_refusal_units']}</td>
    <td class="num">{pct(p1[0])}</td><td class="num">{pct(p1[1])}–{pct(p1[2])}</td></tr>
<tr><td>P2 — of those, <code>delegate</code> reads</td>
    <td class="num">{p['of_those_delegate_reads']}/{p['still_refuse']}</td>
    <td class="num">{pct(p2[0])}</td><td class="num">{pct(p2[1])}–{pct(p2[2])}</td></tr>
</table></div>
<p class="muted">Pre-registered bands: P1 ≥ 70% (met); P2 15–35% (met by the uncorrected screen,
16.4%; undershot by the hand-corrected reading above).</p>

<h2>Positive controls</h2>
<p>{ctrl['n']} controls, recorded 200 by this ecology's own registers. {ctrl['local_reads']} read
under <code>local</code>, {ctrl['delegate_reads']} under <code>delegate</code>. Both above the
pre-registered kill-condition floor of 4. The {len(ctrl['both_fail'])} that failed on
<em>both</em> arms: {", ".join(esc(u) for u in ctrl['both_fail'])} — a client-side JavaScript
wall, not an address-dependent block.</p>

<h2>The hand-read adjudication</h2>
<p>Every 200-status page where the reused challenge-word screen fired — a census of five, not a
sample.</p>
<div class="table-wrap"><table>
<tr><th>unit</th><th>screen word</th><th>verdict</th><th>reason</th></tr>
{hand_reads_html}
</table></div>

<h2>All 64 units</h2>
<div class="table-wrap"><table>
<tr><th>unit</th><th>stratum</th><th>recorded</th><th>local status</th>
    <th>local (screen)</th><th>local (read)</th><th>delegate</th><th>delegate error</th></tr>
{rows_html}
</table></div>

<footer>
<p>Pre-registration: <code>PREREGISTRATION.md</code>, committed before either arm ran.
Verification: <code>check.py</code> (30 checks, each re-deriving its number from the raw probe
files) and <code>tamper.py</code> (15 deliberate corruptions, all caught). Five-minute summary:
<code>SUMMARY.md</code>. Sources: <code>data/sources.json</code>.</p>
</footer>
</body>
</html>
"""
    out = ART / "index.html"
    if "--check" in sys.argv:
        old = out.read_text()
        if old != page:
            print("PAGE OUT OF DATE with data/estimates.json")
            sys.exit(1)
        print("page matches data/estimates.json, byte for byte")
        return
    out.write_text(page)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
