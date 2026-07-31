#!/usr/bin/env python3
"""
Verify that the repaired works/2026-07-01-calibration-gap/work.astro draws under the
site's live Content-Security-Policy, now that its bars are inline SVG geometry plus a
component <style> block instead of inline style="" attributes.

Why a specimen and not the .astro file. work.astro cannot be rendered here: this runtime
has no Astro/site build, and a static stand-in cannot itself evaluate the file's template
expressions. So the object actually verified below is evidence/specimen.html -- a static
expansion generated from data.json with every value already evaluated in Python, using
the exact same class names, markup shape and bar-geometry formula as work.astro's
frontmatter (TRACK, HAIRLINE, barLen/toolChart). It is a faithful transcription, not a
build of the .astro file; whether the .astro file itself compiles under the real Astro
toolchain is NOT checked here and is called out below rather than assumed.

Policy under test. The site's own live style-src for this work's published page, fetched
fresh, plus the sha256 of the specimen's own <style> block -- the same block work.astro
declares, copied out of the .astro source verbatim (see EXTRACTION GUARD), not rewritten
by hand. That addition is not a loosening: it is exactly what the site build does with a
component <style> block, and what twelve of the collective's other works already rely on.

EXTRACTION GUARD. A prior harness in this collective matched the literal text "<style>"
wherever it occurred -- including inside a comment -- and hashed a blob of prose as if it
were CSS, which silently dropped the real stylesheet and made a known-good control
"fail". This script guards against repeating that in three ways:
  1. It strips HTML comments (<!-- ... -->) and JS/TS comments (// line comments and
     /* block comments */) from a scratch copy of work.astro before searching, so a
     mention of the word "style" or the tag name inside a comment cannot be matched.
  2. It requires there to be EXACTLY ONE <style>...</style> block left after stripping,
     and raises loudly (does not guess, does not silently pick the first or last) if
     there are zero or more than one.
  3. It sanity-checks the extracted text actually looks like CSS (contains "{", "}" and
     ":", and contains no HTML tags such as "<div" or "<svg") before hashing it, and
     raises rather than hashing text that fails that check.

Run: python3 verify_render.py
"""

import base64
import hashlib
import html
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
CENSUS_DIR = os.path.join(REPO, 'drafts', '2026-07-31-served-not-shown')
SLUG = '2026-07-01-calibration-gap'

sys.path.insert(0, CENSUS_DIR)
from census import WORK_URL, browser, directive, dump_dom, fetch, meta_csp, screenshot, serve  # noqa: E402

# Geometry constants -- must mirror work.astro's frontmatter exactly (TRACK, HAIRLINE,
# ROW_PITCH, TRACK_X, VALUE_X, and the barLen/toolChart formulas) since this script is a
# from-scratch transcription of the template, not an execution of it.
TRACK = 300
HAIRLINE = TRACK * 0.0015
TRACK_X = 42
VALUE_X = 352
ROW_PITCH = 17


def bar_len(v, cap):
    if v is None or v == 0:
        return HAIRLINE
    return min((v / cap) * TRACK, TRACK)


def fmt(v, suffix='%'):
    return f'{v}{suffix}' if v is not None else 'n/d'


def esc(s):
    return html.escape(str(s), quote=False)


def extract_style_block(astro_source):
    """Return the CSS text of work.astro's single component <style> block.

    See the module docstring's EXTRACTION GUARD section for why this is not simply
    astro_source.index('<style>') / .rindex('<style>').
    """
    scratch = astro_source
    scratch = re.sub(r'<!--.*?-->', '', scratch, flags=re.S)      # HTML comments
    scratch = re.sub(r'/\*.*?\*/', '', scratch, flags=re.S)       # JS/TS block comments
    scratch = re.sub(r'(?m)^\s*//.*$', '', scratch)               # JS/TS line comments

    matches = re.findall(r'<style(?:\s[^>]*)?>([\s\S]*?)</style>', scratch)
    if len(matches) != 1:
        raise SystemExit(
            'EXTRACTION GUARD FAILED: expected exactly one <style> block in work.astro '
            'after stripping comments, found %d. Refusing to guess which one is real.'
            % len(matches))
    css = matches[0]
    looks_like_css = ('{' in css and '}' in css and ':' in css)
    looks_like_markup = bool(re.search(r'<(div|p|span|section|svg|text|rect|g)\b', css))
    if not looks_like_css or looks_like_markup:
        raise SystemExit(
            'EXTRACTION GUARD FAILED: the extracted <style> content does not look like '
            'CSS (or looks like markup/prose). Refusing to hash it. First 200 chars:\n'
            + css[:200])
    return css


def tool_chart(tool, cap):
    rows = [
        ('spec', tool['claim_fpr'], 'cc-bar--spec', 'cc-val--spec'),
        ('measured', tool['independent_fpr'], 'cc-bar--meas', 'cc-val--meas'),
    ]
    if tool['nnes_fpr'] is not None:
        rows.append(('NNES*', tool['nnes_fpr'], 'cc-bar--nnes', 'cc-val--nnes'))
    laid = []
    for i, (label, value, bar_cls, val_cls) in enumerate(rows):
        laid.append({
            'label': label, 'bar_cls': bar_cls, 'val_cls': val_cls,
            'y': 4 + i * ROW_PITCH, 'label_y': 11 + i * ROW_PITCH,
            'width': bar_len(value, cap), 'formatted': fmt(value),
        })
    height = 34 + (len(rows) - 2) * ROW_PITCH
    aria = ('%s: vendor specification %s, independent measurement %s'
            % (tool['name'], fmt(tool['claim_fpr']), fmt(tool['independent_fpr'])))
    if tool['nnes_fpr'] is not None:
        aria += ', NNES %s' % fmt(tool['nnes_fpr'])
    aria += ', false positive rate, scale 0 to %s percent' % cap
    return laid, height, aria


def build_body(data):
    cap = data['fpr_scale_cap']

    tools_html = []
    for tool in data['tools']:
        rows, height, aria = tool_chart(tool, cap)
        rows_svg = []
        for r in rows:
            rows_svg.append(
                '<g><text x="0" y="%s" class="cc-chart-lbl">%s</text>'
                '<rect x="%s" y="%s" width="%s" height="7" class="cc-chart-track"/>'
                '<rect x="%s" y="%s" width="%.4f" height="7" class="cc-chart-bar %s"/>'
                '<text x="%s" y="%s" class="cc-chart-val %s">%s</text></g>'
                % (r['label_y'], esc(r['label']), TRACK_X, r['y'], TRACK,
                   TRACK_X, r['y'], r['width'], r['bar_cls'],
                   VALUE_X, r['label_y'], r['val_cls'], esc(r['formatted'])))
        tools_html.append(
            '<div class="cc-tool">'
            '<div class="cc-tool-head"><span class="cc-tool-name">%s</span>'
            '<span class="cc-tool-stats">spec: %s &middot; measured: %s</span></div>'
            '<svg class="cc-chart" viewBox="0 0 420 %s" role="img" aria-label="%s">%s</svg>'
            '<div class="cc-finding">%s</div>'
            '</div>'
            % (esc(tool['name']), esc(fmt(tool['claim_fpr'])), esc(fmt(tool['independent_fpr'])),
               height, esc(aria), ''.join(rows_svg), esc(tool['key_finding'])))

    cases_html = []
    for c in data['harm_cases']:
        if c['scale'] == 'institutional' and c['allegations'] is not None:
            sub = '{:,} allegations'.format(c['allegations'])
            if c['dismissed_pct'] is not None:
                sub += ' &middot; %s%% dismissed' % c['dismissed_pct']
        else:
            sub = esc(c['detector'])
        caveat_html = ''
        if 'caveat' in c:
            caveat_html = '<div class="cc-case-caveat">%s</div>' % esc(c['caveat'])
        cases_html.append(
            '<div class="cc-case">'
            '<div class="cc-case-head">%s &middot; %s</div>'
            '<div class="cc-case-sub">%s</div>'
            '<div class="cc-case-outcome">%s</div>'
            '%s'
            '<div class="cc-case-source">%s</div>'
            '</div>'
            % (esc(c['institution']), c['year'], sub, esc(c['outcome']), caveat_html, esc(c['source'])))

    sources_html = []
    for s in data['benchmark_sources']:
        sources_html.append(
            '<div class="cc-source-row"><span class="cc-source-name">%s</span>'
            '<span class="cc-source-finding">%s</span></div>' % (esc(s['name']), esc(s['finding'])))

    # The three correction/revision paragraphs and the closing note are copied verbatim
    # from work.astro (they are not derived from data.json), so they are transcribed
    # literally here rather than templated.
    correction = (
        'CORRECTION (2026-07-03): the Originality.ai row previously displayed a vendor claim of 0.2% FPR '
        'against an independent measurement of 37% FPR (“a 185x gap”). Neither figure is retrievable in the '
        'cited RAID paper or in vendor marketing; the row now shows what the sources actually state — the '
        'vendor’s own “under 3%” FPR claim holds on RAID’s clean corpus (0.07–0.47%), while claimed accuracy '
        'collapses out-of-domain (8.5% on code, 55.8% on unseen domains, at 5% FPR). Additionally, the GPTZero '
        'row previously displayed 61% as a GPTZero-specific NNES false-positive rate — that figure is Liang '
        'et al.’s seven-detector average (61.22%), now correctly framed in the sources list; and the same '
        'source line previously said “one detector flagged 98%” where the paper’s 97.8% is the fraction of '
        'essays flagged by at least one of seven detectors. The discarded figures are ledgered in the '
        'research archive (memory/discarded.md, session 06).')
    reverify = (
        'RE-VERIFICATION COMPLETED (2026-07-03, session 07): every remaining pre-constitution figure was '
        're-checked against live primary sources. Changes: GPTZero’s measured bar corrected 15% → 18% and '
        're-pinned to its actual primary source (Ibrahim et al., Scientific Reports 2023 — the previously '
        'cited commercial aggregator itself states 18%, citing that study); Turnitin’s measured bar corrected '
        '5% → 4% (the vendor’s own sentence-level admission — a sentence-level figure, disclosed as such '
        'beside document-level bars); Turnitin’s NNES 30% bar removed (no retrievable study supports a '
        'Turnitin-specific NNES rate — the foundational cross-detector study excluded Turnitin, and the '
        'vendor’s own research reports no statistically significant ELL bias at 300+ words); an unattributed '
        '“real-world accuracy 85–90%” line removed as unsourced; ZeroGPT’s measured bar corrected 28% → '
        '16.67% (the previous attribution was unretrievable; now Pratama 2025, PeerJ CS); the Perkins et al. '
        '17.4% restated as a 17.4-percentage-point mean drop (39.5% → 22.2%), not a resulting accuracy — the '
        'same error is corrected in the research archive’s claims ledger; a “no better than random guessing” '
        'paraphrase-in-quotation-marks restricted to the tool the paper applies it to (DetectGPT); the two '
        'individual harm cases narrowed to what court records and local reporting state. The FPR scale was '
        're-capped 65% → 20% after the removals. Verified figures that stood: both vendors’ spec claims, the '
        'Perkins 46.1% and Weber-Wulff 59% accuracy figures, all source-list lines, and the core facts of all '
        'three harm cases. Discards ledgered in memory/discarded.md (session 07).')
    revision = (
        'REVISION (2026-07-12, session 33): two changes to the harm register, on a binding team steer and a '
        'downstream correction report (the lab’s production wing, via REQUESTS.md). First, the register no '
        'longer carries personal names of the individuals in its own voice — the two individual cases now read '
        'as role + institution + consequence, with the official case captions moved into the source lines as '
        'citations (named-individuals policy, team, 2026-07-12; the underlying reporting is unchanged and '
        'linked). Second, the Minnesota row now carries the appellate record’s load-bearing caveat at display '
        'prominence: the disciplinary panel did not rely on AI-detection evidence — the case documents a '
        'detector figuring in an accusation, not a consequence the courts attributed to a detector. The '
        'collective’s own field sweep had already recorded this framing (“grader judgment, explicitly not '
        'detector output alone”, FIELD.md); the register row had never been updated to match. Gauntlet re-run '
        'on the revised state per the standing rule; record in journal/2026-07-12.md, session 33.')
    footer_note = (
        'This certificate is itself a measurement instrument — it documents the gap between specification '
        'and performance in tools now deployed to judge the authenticity of human writing. '
        'Method and data are open: frankbueltge.de/field / github.com/frankbueltge/field-research')

    body = (
        '<div class="cc">'
        '<div class="cc-header">'
        '<div class="cc-eyebrow">THE MEASURING FIELD / MERIDIAN / INSTRUMENT 001</div>'
        '<h1 class="cc-title">CALIBRATION CERTIFICATE</h1>'
        '<p class="cc-subtitle">AI Text Detection — Independent Audit Against Vendor Specifications</p>'
        '<p class="cc-refdate">Reference date: %s &middot; Scale: 0–%s%% FPR</p>'
        '<div class="cc-stamp">OUT OF SPEC</div>'
        '</div>'
        '<div class="cc-matrix">'
        '<div class="cc-matrix-title">FALSE POSITIVE RATE — CLAIM vs. INDEPENDENT MEASUREMENT</div>'
        '<div class="cc-legend">'
        '<span><span class="cc-swatch cc-swatch--spec"></span>vendor specification</span>'
        '<span><span class="cc-swatch cc-swatch--meas"></span>independent (general)</span>'
        '</div>'
        '%s'
        '<div class="cc-matrix-footnote">NNES = Non-Native English Speakers. No per-tool NNES false-positive '
        'rate survived the 2026-07-03 re-verification; the cross-detector NNES evidence (61.22% seven-detector '
        'average, Liang et al., Cell Patterns 2023) is in the measurement sources below. Confidence ratings '
        'vary — see data.json for per-tool methodology notes.</div>'
        '</div>'
        '<div class="cc-harm">'
        '<div class="cc-harm-title">FIELD OBSERVATIONS — DOCUMENTED HARM REGISTER</div>'
        '%s'
        '</div>'
        '<div class="cc-sources">'
        '<div class="cc-sources-title">MEASUREMENT SOURCES</div>'
        '%s'
        '<div class="cc-correction">%s</div>'
        '<div class="cc-note">%s</div>'
        '<div class="cc-note">%s</div>'
        '<div class="cc-footer-note">%s</div>'
        '</div>'
        '</div>'
        % (data['generated'], cap, ''.join(tools_html), ''.join(cases_html), ''.join(sources_html),
           correction, reverify, revision, footer_note))
    return body


READBACK = """
(function () {
  function readEl(sel) {
    var el = document.querySelector(sel);
    if (!el) return null;
    var cs = getComputedStyle(el);
    return {
      backgroundColor: cs.backgroundColor,
      fill: cs.fill,
      width: cs.width,
      height: cs.height,
      borderTopWidth: cs.borderTopWidth,
      borderTopStyle: cs.borderTopStyle,
      borderTopColor: cs.borderTopColor
    };
  }
  document.getElementById('out').textContent = JSON.stringify({
    container: readEl('.cc'),
    measured_bar: readEl('.cc-chart-bar--meas'),
    stamp: readEl('.cc-stamp')
  });
})();
"""


def main():
    result = {
        'verified_object': 'evidence/specimen.html',
        'not_verified': (
            'works/2026-07-01-calibration-gap/work.astro itself was NOT rendered or '
            'compiled by this script -- this runtime has no Astro/site build. '
            'evidence/specimen.html is a hand-built static expansion of the same markup '
            'shape, class names and bar-geometry formula, generated from data.json; it '
            'demonstrates that the mechanism (component <style> + SVG attributes) draws '
            'under the live policy, not that the .astro file compiles.'
        ),
    }

    chrome = browser()
    if not chrome:
        result['status'] = 'NOT RUN'
        result['reason'] = 'no Chromium-family browser binary found by census.browser()'
        print(json.dumps(result, indent=2))
        return

    astro_path = os.path.join(HERE, 'work.astro')
    astro_source = open(astro_path, encoding='utf-8').read()

    # Zero style="" attributes in the source, asserted here too (not just by the
    # session's grep check), so the harness fails loudly if that regresses.
    style_attrs_in_source = len(re.findall(r'\sstyle=', astro_source))

    style_css = extract_style_block(astro_source)

    data = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8'))

    _, page = fetch(WORK_URL.format(slug=SLUG))
    style_src = directive(meta_csp(page), 'style-src')
    digest = base64.b64encode(hashlib.sha256(style_css.encode('utf-8')).digest()).decode()
    policy = "default-src 'self'; script-src 'self'; %s 'sha256-%s'" % (style_src, digest)

    body = build_body(data)
    specimen_html = (
        '<!doctype html><html><head><meta charset="utf-8">'
        '<meta http-equiv="content-security-policy" content="%s">'
        '<style>%s</style></head><body>%s<pre id="out">not-run</pre>'
        '<script src="./readback.js"></script></body></html>'
        % (policy, style_css, body))

    evidence_dir = os.path.join(HERE, 'evidence')
    os.makedirs(evidence_dir, exist_ok=True)
    specimen_path = os.path.join(evidence_dir, 'specimen.html')
    open(specimen_path, 'w', encoding='utf-8').write(specimen_html)

    style_attrs_in_specimen = len(re.findall(r'\sstyle=', specimen_html))

    tmp = tempfile.mkdtemp(prefix='cc-verify-')
    try:
        open(os.path.join(tmp, 'readback.js'), 'w').write(READBACK)
        open(os.path.join(tmp, 'index.html'), 'w', encoding='utf-8').write(specimen_html)
        httpd, base = serve(tmp)
        try:
            dom = dump_dom(chrome, base + '/index.html')
            m = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
            measured = json.loads(m.group(1)) if m and m.group(1) != 'not-run' else None
            screenshot(chrome, base + '/index.html',
                       os.path.join(evidence_dir, 'render.png'), size='900,1600')
        finally:
            httpd.shutdown()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    container = (measured or {}).get('container') or {}
    bar = (measured or {}).get('measured_bar') or {}
    stamp = (measured or {}).get('stamp') or {}

    checks = {
        'zero_style_attrs_in_source': style_attrs_in_source == 0,
        'zero_style_attrs_in_specimen': style_attrs_in_specimen == 0,
        'style_block_extracted_and_looks_like_css': True,  # extract_style_block raises otherwise
        'dark_ground_applied': container.get('backgroundColor') == 'rgb(13, 13, 13)',
        'measured_bar_nonzero_width': bool(bar.get('width')) and bar.get('width') not in (None, '0px', 'auto'),
        'measured_bar_correct_fill': bar.get('fill') == 'rgb(192, 57, 43)',
        'stamp_border_visible': (
            stamp.get('borderTopStyle') == 'solid'
            and stamp.get('borderTopWidth') == '3px'
            and stamp.get('borderTopColor') == 'rgb(192, 57, 43)'
        ),
    }
    overall = all(checks.values())

    result.update({
        'status': 'RUN',
        'policy_tested': policy,
        'style_src_source': "site's live style-src for %s, fetched fresh" % SLUG,
        'style_block_extraction_guard': (
            'stripped HTML/JS comments, required exactly one <style> match, and '
            'sanity-checked the extracted text looks like CSS and not markup/prose'
        ),
        'style_attrs_in_source': style_attrs_in_source,
        'style_attrs_in_specimen': style_attrs_in_specimen,
        'measured': measured,
        'checks': checks,
        'overall_pass': overall,
        'specimen': 'evidence/specimen.html',
        'screenshot': 'evidence/render.png',
    })

    out_path = os.path.join(HERE, 'render-verification.json')
    json.dump(result, open(out_path, 'w'), indent=2)
    print(json.dumps(result, indent=2))
    print()
    print('=== %s ===' % ('PASS' if overall else 'FAIL'))
    for k, v in checks.items():
        print('  [%s] %s' % ('x' if v else ' ', k))


if __name__ == '__main__':
    main()
