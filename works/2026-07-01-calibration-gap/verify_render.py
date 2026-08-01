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
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
CENSUS_DIR = os.path.join(REPO, 'drafts', '2026-07-31-served-not-shown')
SLUG = '2026-07-01-calibration-gap'

sys.path.insert(0, CENSUS_DIR)
from census import WORK_URL, browser, directive, dump_dom, fetch, meta_csp, screenshot, serve  # noqa: E402

# Geometry constants are PARSED OUT OF work.astro rather than restated here. An earlier
# state of this pair drifted -- the component moved its track to x=100 and its value text
# to x=410 while this file still said 42 and 352, so the specimen would have verified a
# layout the work no longer had. A transcription that can silently disagree with its
# original is not a verification.
def astro_const(src, name):
    m = re.search(r'const\s+%s\s*=\s*([0-9.]+)' % name, src)
    if not m:
        raise SystemExit('verify_render: constant %s not found in work.astro' % name)
    v = float(m.group(1))
    return int(v) if v.is_integer() else v


_ASTRO = open(os.path.join(HERE, 'work.astro'), encoding='utf-8').read()
TRACK = astro_const(_ASTRO, 'TRACK')
HAIRLINE = TRACK * 0.0015
ROW_PITCH = astro_const(_ASTRO, 'ROW_PITCH')
VIEWBOX_W = astro_const(_ASTRO, 'BAR_VIEWBOX_W')


def bar_len(v, cap):
    if v is None or v == 0:
        return HAIRLINE
    return min((v / cap) * TRACK, TRACK)


def fmt(v, suffix='%'):
    return f'{v}{suffix}' if v is not None else 'n/d'


def short_url(url):
    if not url:
        return ''
    return re.sub(r'/$', '', re.sub(r'^https?://', '', url))


def link_html(url):
    if not url:
        return ''
    return '<a class="cc-link" href="%s">%s</a>' % (url, short_url(url))


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
        ('spec', tool['claim_fpr'], 'cc-chart-bar--spec', 'cc-val--spec'),
        ('measured', tool['independent_fpr'], 'cc-chart-bar--meas', 'cc-val--meas'),
    ]
    if tool['nnes_fpr'] is not None:
        rows.append(('NNES*', tool['nnes_fpr'], 'cc-chart-bar--nnes', 'cc-val--nnes'))
    laid = [{'label': lbl, 'bar_cls': bc, 'val_cls': vc,
             'width': bar_len(v, cap), 'formatted': fmt(v)}
            for lbl, v, bc, vc in rows]
    aria = ('%s: vendor specification %s, independent measurement %s'
            % (tool['name'], fmt(tool['claim_fpr']), fmt(tool['independent_fpr'])))
    if tool['nnes_fpr'] is not None:
        aria += ', NNES %s' % fmt(tool['nnes_fpr'])
    aria += ', false positive rate, scale 0 to %s percent' % cap
    return laid, aria


def build_body(data):
    cap = data['fpr_scale_cap']

    tools_html = []
    for tool in data['tools']:
        rows, aria = tool_chart(tool, cap)
        rows_html = []
        for r in rows:
            rows_html.append(
                '<div class="cc-row"><span class="cc-row-lbl">%s</span>'
                '<svg class="cc-row-bar" viewBox="0 0 %s %s" preserveAspectRatio="none" '
                'aria-hidden="true" focusable="false">'
                '<rect x="0" y="0" width="%s" height="%s" class="cc-chart-track"/>'
                '<rect x="0" y="0" width="%.4f" height="%s" class="cc-chart-bar %s"/>'
                '</svg><span class="cc-row-val %s">%s</span></div>'
                % (esc(r['label']), VIEWBOX_W, ROW_PITCH, VIEWBOX_W, ROW_PITCH,
                   r['width'], ROW_PITCH, r['bar_cls'], r['val_cls'], esc(r['formatted'])))
        extras = ''
        if tool.get('spec_flag'):
            extras += '<div class="cc-specflag">%s</div>' % esc(tool['spec_flag'])
        extras += ('<div class="cc-finding">%s</div>' % esc(tool['key_finding']))
        extras += ('<details class="cc-method"><summary class="cc-method-tag">method, sources '
                   'and what was corrected on this row</summary>'
                   '<div class="cc-method-body">%s</div>' % esc(tool['confidence_note']))
        if tool.get('claim_accuracy_status'):
            extras += ('<div class="cc-method-body">%s</div>'
                       % esc(tool['claim_accuracy_status']))
        extras += '</details>' 
        tools_html.append(
            '<div class="cc-tool">'
            '<div class="cc-tool-head"><span class="cc-tool-name">%s</span>'
            '<span class="cc-tool-stats">spec: %s &middot; measured: %s</span></div>'
            '<div class="cc-rows" role="group" aria-label="%s">%s</div>'
            '%s</div>'
            % (esc(tool['name']), esc(fmt(tool['claim_fpr'])), esc(fmt(tool['independent_fpr'])),
               esc(aria), ''.join(rows_html), extras))

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
            '<div class="cc-case-source">%s</div>'
            '%s'
            '</div>'
            % (esc(c['institution']), c['year'], sub, esc(c['outcome']), caveat_html, esc(c['source']),
               link_html(c.get('source_url')) + (
                   ' &middot; ' + link_html(c['source_url_secondary'])
                   if c.get('source_url_secondary') else ''),
               ('<div class="cc-case-access">%s</div>' % esc(c['access_note'])
                if c.get('access_note') else '')))

    sources_html = []
    for s in data['benchmark_sources']:
        sources_html.append(
            '<div class="cc-source-row"><span class="cc-source-name">%s</span>'
            '<span class="cc-source-finding">%s%s</span></div>'
            % (esc(s['name']), esc(s['finding']),
               (' &middot; ' + link_html(s['url'])) if s.get('url') else ''))

    # Specification sources — added 2026-08-01 with the repair. The spec side of this
    # certificate carried no source of any kind until that date.
    specs_html = []
    for sp in data.get('specification_sources', []):
        specs_html.append(
            '<div class="cc-spec">'
            '<div class="cc-spec-head"><span class="cc-spec-tool">%s</span>'
            '<span class="cc-spec-claim">%s</span></div>'
            '%s%s'
            '<div class="cc-spec-caveat">%s</div>'
            '</div>'
            % (esc(sp['tool']), esc(sp['claim_shown']),
               ('<div class="cc-spec-quote">&ldquo;%s&rdquo;</div>' % esc(sp['verbatim']))
               if sp.get('verbatim') else '',
               ('<div class="cc-spec-url">%s</div>' % link_html(sp['url'])) if sp.get('url') else '',
               esc(sp['caveat'])))

    # The static prose blocks (the dated correction/revision/repair notes, the
    # specification lede and the closing note) are NOT derived from data.json. An earlier
    # version of this harness transcribed them by hand, which lets the specimen and the
    # work drift apart silently. They are now EXTRACTED from work.astro itself, so the
    # specimen provably carries the same text the component does.
    astro = open(os.path.join(HERE, 'work.astro'), encoding='utf-8').read()

    def block(cls, nth=0):
        found = re.findall(r'<div class="%s">(.*?)</div>' % cls, astro, re.S)
        if len(found) <= nth:
            raise SystemExit('verify_render: could not extract .%s #%d from work.astro' % (cls, nth))
        return re.sub(r'\s+', ' ', found[nth]).strip()

    correction = block('cc-correction')
    reverify = block('cc-note', 0)
    revision = block('cc-note', 1)
    repair = block('cc-note', 2)
    spec_lede = block('cc-spec-lede')
    footer_note = block('cc-footer-note')

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
        'rate survived the 2026-07-03 re-verification; the cross-detector NNES evidence (61.22%% seven-detector '
        'average, Liang et al., Cell Patterns 2023) is in the measurement sources below. Confidence ratings '
        'vary — see data.json for per-tool methodology notes.</div>'
        '</div>'
        '<div class="cc-harm">'
        '<div class="cc-harm-title">FIELD OBSERVATIONS — DOCUMENTED HARM REGISTER</div>'
        '%s'
        '</div>'
        '<div class="cc-sources">'
        '<div class="cc-sources-title">SPECIFICATION SOURCES — WHERE THE CLAIM BARS COME FROM</div>'
        '<div class="cc-spec-lede">%s</div>'
        '%s'
        '</div>'
        '<div class="cc-sources">'
        '<div class="cc-sources-title">MEASUREMENT SOURCES</div>'
        '%s'
        '<div class="cc-correction">%s</div>'
        '<div class="cc-note">%s</div>'
        '<div class="cc-note">%s</div>'
        '<div class="cc-note">%s</div>'
        '<div class="cc-footer-note">%s</div>'
        '</div>'
        '</div>'
        % (data['generated'], cap, ''.join(tools_html), ''.join(cases_html),
           spec_lede, ''.join(specs_html), ''.join(sources_html),
           correction, reverify, revision, repair, footer_note))
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
      borderTopColor: cs.borderTopColor,
      fontSize: cs.fontSize,
      boxWidth: el.getBoundingClientRect().width,
      boxHeight: el.getBoundingClientRect().height
    };
  }
  document.getElementById('out').textContent = JSON.stringify({
    viewport: window.innerWidth,
    container: readEl('.cc'),
    measured_bar: readEl('.cc-chart-bar--meas'),
    row_label: readEl('.cc-row-lbl'),
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

            # NARROW-WIDTH CHECK. Row labels and values are HTML, not SVG text, precisely so
            # that they do not shrink with the container. This measures that: the same page,
            # rendered at three widths, must report the SAME computed font-size and the SAME
            # label box height, while the bar's width changes and its height does not.
            #
            # HONEST LIMIT, tested rather than assumed: this runtime's headless browser
            # clamps its layout viewport at 500px. Asking for 390 yields innerWidth 500, and
            # a screenshot at 390 crops rather than reflows -- a control page whose media
            # query flips the background colour below 480px stayed unflipped at both. So no
            # measurement here reaches a true phone width, and none is claimed to. What is
            # established is that text size is INDEPENDENT of width across the range that can
            # be reached, which is the property that makes the phone width safe.
            narrow = {}
            for w in (1200, 900, 500):
                d = subprocess.run(
                    [chrome, '--headless=new', '--no-sandbox', '--disable-gpu',
                     '--window-size=%d,900' % w, '--dump-dom', base + '/index.html'],
                    capture_output=True, text=True, timeout=180).stdout
                mm = re.search(r'<pre id="out">(.*?)</pre>', d, re.S)
                if mm and mm.group(1) != 'not-run':
                    r = json.loads(mm.group(1))
                    narrow[str(w)] = {
                        'viewport': r.get('viewport'),
                        'label_font_size': (r.get('row_label') or {}).get('fontSize'),
                        'label_box_height': (r.get('row_label') or {}).get('boxHeight'),
                        'bar_box_width': (r.get('measured_bar') or {}).get('boxWidth'),
                        'bar_box_height': (r.get('measured_bar') or {}).get('boxHeight'),
                    }
            fonts = {v['label_font_size'] for v in narrow.values()}
            heights = {v['bar_box_height'] for v in narrow.values()}
            widths = {v['bar_box_width'] for v in narrow.values()}
            text_size_independent_of_width = len(fonts) == 1 and len(narrow) == 3
            bar_height_constant = len(heights) == 1
            bar_width_responsive = len(widths) == 3

            screenshot(chrome, base + '/index.html',
                       os.path.join(HERE, 'evidence', 'render.png'), size='1000,4400')
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
        'row_text_size_independent_of_width': text_size_independent_of_width,
        'bar_height_constant_across_widths': bar_height_constant,
        'bar_width_responsive_across_widths': bar_width_responsive,
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
        'narrow_width': narrow,
        'narrow_width_limit': (
            "this runtime's headless browser clamps its layout viewport at 500px; a request "
            "for 390 reports innerWidth 500 and a screenshot at 390 crops rather than "
            "reflows (verified with a control page whose media query flips a colour below "
            "480px, which stayed unflipped at both). No measurement here reaches a true "
            "phone width, and none is claimed to."
        ),
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
