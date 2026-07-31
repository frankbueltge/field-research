#!/usr/bin/env python3
"""
Build and verify the face specimen: the same four measurements drawn twice on one page, under
the site's own policy — once by the sanctioned mechanism, once by inline style attributes.

Why a specimen and not the Astro file. `work.astro` cannot be rendered here: this runtime has no
site build, and a static stand-in cannot evaluate its template expressions — an earlier attempt
did exactly that and measured its own artifact rather than the policy. So the object that is
actually verified is `evidence/face-specimen.html`, generated below from `data.json` with every
value already expanded. `work.astro` is a transcription of this specimen into the site's
component form (the precedent for that transform is instrument 017). The transcription itself is
NOT verified here and is not shipped.

The policy under which the specimen is rendered is the site's own `style-src`, fetched live, plus
one addition: the sha256 of the specimen's own <style> block. That addition is not a loosening —
it is precisely what the site's build does with a component <style>, and it is what the twelve
works that render correctly already rely on. Nothing else in the policy is changed.

Run: python3 verify_face.py
"""

import base64
import hashlib
import json
import os
import re
import shutil
import tempfile

from census import (WORK_URL, browser, directive, dump_dom, fetch, meta_csp, screenshot, serve)

HERE = os.path.dirname(os.path.abspath(__file__))
REFERENCE_PAGE = '2026-07-01-calibration-gap'
TRACK = 300

READBACK = """
(function () {
  function read(el, prop) {
    if (!el) return null;
    var cs = getComputedStyle(el);
    return { fill: cs.fill, backgroundColor: cs.backgroundColor,
             width: cs.width, height: cs.height };
  }
  document.getElementById('out').textContent = JSON.stringify({
    frame:     read(document.querySelector('.sns')),
    left_bar:  read(document.querySelector('#left-specimen rect.meas')),
    right_bar: read(document.querySelector('#right-specimen .measured-bar'))
  });
})();
"""


def fmt(v):
    return ('%g%%' % v) if v is not None else 'n/d'


def bar_len(v, cap):
    return 1 if (v is None or v == 0) else min((v / cap) * TRACK, TRACK)


def pct(v, cap):
    return '0.15%' if (v is None or v == 0) else '%.2f%%' % min((v / cap) * 100, 100)


def build_specimen(data, style):
    cap = data['fpr_scale_cap']
    left, right = [], []
    for r in data['rows']:
        left.append(
            '<div class="row"><div class="name">%s</div>'
            '<svg class="chart" viewBox="0 0 420 34" role="img" aria-label="%s: vendor '
            'specification %s, independent measurement %s, false positive rate, scale 0 to %d '
            'percent">'
            '<text x="0" y="11" class="lbl">spec</text>'
            '<rect x="42" y="4" width="%d" height="7" class="track"/>'
            '<rect x="42" y="4" width="%.2f" height="7" class="spec"/>'
            '<text x="352" y="11" class="val">%s</text>'
            '<text x="0" y="28" class="lbl">measured</text>'
            '<rect x="42" y="21" width="%d" height="7" class="track"/>'
            '<rect x="42" y="21" width="%.2f" height="7" class="meas"/>'
            '<text x="352" y="28" class="val meas-t">%s</text>'
            '</svg></div>' % (r['name'], r['name'], fmt(r['claim_fpr']),
                              fmt(r['independent_fpr']), cap, TRACK,
                              bar_len(r['claim_fpr'], cap), fmt(r['claim_fpr']), TRACK,
                              bar_len(r['independent_fpr'], cap), fmt(r['independent_fpr'])))
        right.append(
            '<div>'
            '<div style="display: flex; justify-content: space-between; margin-bottom: 0.45rem;">'
            '<span style="font-weight: 700; color: #e8e8e8; font-size: 0.8rem;">%s</span></div>'
            '<div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.22rem;">'
            '<span style="width: 5.5rem; text-align: right; font-size: 0.6rem; color: #5a5a5a; flex-shrink: 0;">spec</span>'
            '<div style="flex: 1; background: #1e1e1e; height: 7px; position: relative;">'
            '<div style="position: absolute; top: 0; left: 0; height: 100%%; background: #555; width: %s;"></div>'
            '</div><span style="width: 3.5rem; font-size: 0.6rem; color: #7a7a7a;">%s</span></div>'
            '<div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.22rem;">'
            '<span style="width: 5.5rem; text-align: right; font-size: 0.6rem; color: #5a5a5a; flex-shrink: 0;">measured</span>'
            '<div style="flex: 1; background: #1e1e1e; height: 7px; position: relative;">'
            '<div class="measured-bar" style="position: absolute; top: 0; left: 0; height: 100%%; background: #c0392b; width: %s;"></div>'
            '</div><span style="width: 3.5rem; font-size: 0.6rem; color: #c0392b;">%s</span></div>'
            '</div>' % (r['name'], pct(r['claim_fpr'], cap), fmt(r['claim_fpr']),
                        pct(r['independent_fpr'], cap), fmt(r['independent_fpr'])))

    return (
        '<div class="sns"><div class="wrap">'
        '<p class="kicker">Meridian &middot; render census &middot; 2026-07-31 &middot; specimen, not shipped</p>'
        '<h1>Two Columns, One Policy</h1>'
        '<p class="lede">The same four measurements, drawn twice, on one page, under one '
        'Content-Security-Policy &mdash; this site\'s own. Left: the mechanism this practice\'s '
        'constitution requires. Right: the markup of a work it published on 2026-07-01 and '
        'committed for delivery to an outside reader on 2026-07-31, verbatim.</p>'
        '<div class="cols">'
        '<section class="col" id="left-specimen"><h2>As declared '
        '<span class="tag ok">component &lt;style&gt; + SVG attributes</span></h2>%s'
        '<p class="foot">Scale 0&ndash;%d&#160;%% false-positive rate. Figures copied unchanged '
        'from the shipped work; their sources, and the six known defects in them, are that '
        'work\'s own.</p></section>'
        '<section class="col" id="right-specimen"><h2>As served '
        '<span class="tag bad">inline style="" attributes</span></h2>%s</section>'
        '</div>'
        '<p class="note"><strong>If the two columns look the same to you</strong>, the page you '
        'are reading is not being served under the policy this piece is about. Under that policy '
        'an inline <code>style=""</code> attribute has no effect: <code>style-src</code> carries '
        'hash-sources, which make <code>\'unsafe-inline\'</code> inoperative, and no '
        '<code>\'unsafe-hashes\'</code>. Eight of this practice\'s twenty published works serve '
        'inline style attributes &mdash; 594 of them, all inert. In two, including this one, '
        'nothing draws the measurement without them.</p>'
        '</div></div>' % (''.join(left), cap, ''.join(right)))


def main():
    chrome = browser()
    if not chrome:
        print('NOT RUN — no browser found')
        return

    data = json.load(open(os.path.join(HERE, 'data.json')))
    astro = open(os.path.join(HERE, 'work.astro'), encoding='utf-8').read()
    # Take the LAST <style> in the file: the frontmatter comment may mention the tag,
    # and an earlier attempt matched that mention and hashed a blob of JavaScript
    # comment as if it were CSS. The parser then dropped the first real rule and the
    # run reported a policy failure that was the harness's own defect.
    style = astro[astro.rindex('<style>') + len('<style>'):astro.rindex('</style>')]

    _, page = fetch(WORK_URL.format(slug=REFERENCE_PAGE))
    style_src = directive(meta_csp(page), 'style-src')
    digest = base64.b64encode(hashlib.sha256(style.encode('utf-8')).digest()).decode()
    policy = "default-src 'self'; script-src 'self'; %s 'sha256-%s'" % (style_src, digest)

    body = build_specimen(data, style)
    html = ('<!doctype html><html><head><meta charset="utf-8">'
            '<meta http-equiv="content-security-policy" content="%s">'
            '<style>%s</style></head><body>%s<pre id="out">not-run</pre>'
            '<script src="./readback.js"></script></body></html>' % (policy, style, body))

    os.makedirs(os.path.join(HERE, 'evidence'), exist_ok=True)
    open(os.path.join(HERE, 'evidence', 'face-specimen.html'), 'w').write(html)

    tmp = tempfile.mkdtemp(prefix='face-verify-')
    open(os.path.join(tmp, 'readback.js'), 'w').write(READBACK)
    open(os.path.join(tmp, 'index.html'), 'w').write(html)
    httpd, base = serve(tmp)
    try:
        dom = dump_dom(chrome, base + '/index.html')
        m = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
        measured = json.loads(m.group(1)) if m and m.group(1) != 'not-run' else None
        screenshot(chrome, base + '/index.html', os.path.join(HERE, 'evidence',
                                                              'face-under-policy.png'),
                   size='1200,760')
    finally:
        httpd.shutdown()
        shutil.rmtree(tmp, ignore_errors=True)

    left = (measured or {}).get('left_bar') or {}
    right = (measured or {}).get('right_bar') or {}
    frame = (measured or {}).get('frame') or {}
    result = {
        'verified_object': 'evidence/face-specimen.html',
        'not_verified': 'work.astro — the Astro transcription; no site build is available here',
        'policy': 'the site\'s live style-src, plus the sha256 of this specimen\'s own <style>',
        'measured': measured,
        'hashed_stylesheet_applies': frame.get('backgroundColor') == 'rgb(13, 13, 13)',
        'left_column_bar_drawn': left.get('fill') == 'rgb(192, 57, 43)',
        'right_column_bar_drawn': right.get('backgroundColor') == 'rgb(192, 57, 43)',
        'screenshot': 'evidence/face-under-policy.png',
    }
    json.dump(result, open(os.path.join(HERE, 'face-verification.json'), 'w'), indent=2)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
