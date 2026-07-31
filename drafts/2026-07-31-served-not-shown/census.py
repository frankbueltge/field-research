#!/usr/bin/env python3
"""
Served, Not Shown — a render census of a published corpus.

The question: for each work this practice has shipped, does the published page apply the
styling the work's own source declares — or is the work served as markup whose visual
argument the browser never draws?

The instrument has three layers and each one is separately falsifiable:

  Layer 0 — POLICY PROBE. A controlled two-cell experiment in a real browser. One cell
            carries the site's exact served style-src policy, the other carries no policy.
            Both contain the same element with an inline style="" attribute. The computed
            style is read back by a same-origin script (allowed under the policy, unlike an
            inline one) and printed. Decides, without argument from the specification text,
            whether inline style attributes take effect under this site's policy.

  Layer 1 — CORPUS CENSUS. Fetches every published work page and counts the inline style
            attributes actually served in it, then cross-references the work's source in
            works/<slug>/work.astro: static attributes, template-interpolated ones (the
            data-bearing kind — bar widths and the like), and whether the work uses a
            component <style> block, which the site hashes and the policy admits.

  Layer 2 — SPECIMENS. Renders named pages in the same browser from a same-origin local
            mirror, so that what is lost can be looked at rather than inferred.

Boundary, declared before any number was produced: this measures whether declared styling is
APPLIED. It does not measure whether a reader understands the page, whether the work is any
good, or whether an unstyled page is worthless. A work that loses only spacing loses little;
a work whose bars encode its measurements loses its argument. The census reports the counts
and names the difference; it computes no composite score.

Re-run:  python3 census.py            (full: probe + census + specimens)
         python3 census.py --no-net   (Layer 0 + source-side counts only)

No third-party packages. Requires a Chromium-family browser for Layers 0 and 2; pass its
path in CENSUS_BROWSER, or the script looks in a few usual places and, failing that, records
the layer as NOT RUN rather than guessing its result.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
WORKS = os.path.join(REPO, 'works')
SITE = 'https://frankbueltge.de'
WORK_URL = SITE + '/field/werke/{slug}/'
UA = 'field-research render census (contact: frankbueltge.de/post/)'

BROWSER_CANDIDATES = [
    os.environ.get('CENSUS_BROWSER', ''),
    '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    shutil.which('chromium') or '',
    shutil.which('chromium-browser') or '',
    shutil.which('google-chrome') or '',
]

# The probe element. Every declaration is one a browser would visibly apply, so that a
# failure to apply cannot hide in a value that happens to match the default.
PROBE_STYLE = ('background: #0d0d0d; color: #c0392b; width: 420px; height: 160px; '
               'font-size: 40px; font-family: monospace')
PROBE_BODY = ('<div id="probe" style="' + PROBE_STYLE + '">INLINE STYLE APPLIED</div>'
              '<pre id="out">not-run</pre>')


def browser():
    for c in BROWSER_CANDIDATES:
        if c and os.path.exists(c):
            return c
    return None


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.read().decode('utf-8', 'replace')


def meta_csp(html):
    m = re.search(r'<meta http-equiv="content-security-policy" content="(.*?)">',
                  html, re.S | re.I)
    return m.group(1) if m else ''


def directive(csp, name):
    for part in csp.split(';'):
        part = part.strip()
        if part.startswith(name + ' ') or part == name:
            return part
    return ''


def count_inline_style_attrs(html):
    return len(re.findall(r'\sstyle="', html))


def serve(root):
    """Serve a directory on 127.0.0.1 so that 'self' in the policy means this mirror."""
    class H(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=root, **kw)

        def log_message(self, *a):
            pass

    httpd = HTTPServer(('127.0.0.1', 0), H)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd, 'http://127.0.0.1:%d' % httpd.server_address[1]


def dump_dom(chrome, url):
    out = subprocess.run(
        [chrome, '--headless=new', '--no-sandbox', '--disable-gpu', '--dump-dom', url],
        capture_output=True, text=True, timeout=120)
    return out.stdout


def screenshot(chrome, url, path, size='1000,1400'):
    subprocess.run(
        [chrome, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars',
         '--window-size=' + size, '--screenshot=' + path, url],
        capture_output=True, text=True, timeout=180)
    return os.path.exists(path)


def layer0(chrome, style_src):
    """Controlled experiment: same element, with and without the site's style-src."""
    if not chrome:
        return {'status': 'NOT RUN — no browser found'}
    tmp = tempfile.mkdtemp(prefix='census-probe-')
    shutil.copy(os.path.join(HERE, 'probe', 'probe.js'), os.path.join(tmp, 'probe.js'))
    pages = {
        # Only style-src is transplanted. script-src is set to 'self' so that probe.js may
        # run in BOTH cells: the two cells must differ in exactly one thing.
        'under_policy': "%s; script-src 'self'" % style_src,
        'control': None,
    }
    for name, csp in pages.items():
        meta = ('<meta http-equiv="content-security-policy" content="%s">' % csp) if csp else ''
        html = ('<!doctype html><html><head><meta charset="utf-8">%s</head>'
                '<body>%s<script src="./probe.js"></script></body></html>' % (meta, PROBE_BODY))
        open(os.path.join(tmp, name + '.html'), 'w').write(html)
    httpd, base = serve(tmp)
    try:
        res = {}
        for name in pages:
            dom = dump_dom(chrome, '%s/%s.html' % (base, name))
            m = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
            res[name] = json.loads(m.group(1)) if m and m.group(1) != 'not-run' else None
    finally:
        httpd.shutdown()
    applied = (res.get('under_policy') or {}).get('backgroundColor')
    ctrl = (res.get('control') or {}).get('backgroundColor')
    return {
        'status': 'RUN',
        'style_src_under_test': style_src,
        'measured': res,
        'control_applies_inline_style': ctrl == 'rgb(13, 13, 13)',
        'policy_applies_inline_style': applied == 'rgb(13, 13, 13)',
    }


SPECIMENS = [
    # (slug, why it is here)
    ('2026-07-01-calibration-gap', 'the piece committed for outbound delivery on 2026-07-31'),
    ('2026-07-01-the-edition', 'the largest count in the corpus'),
    ('2026-07-09-the-floor', 'CONTROL — a work that uses a component <style> block'),
]


def layer2(chrome, pages, outdir):
    """Render specimens from a same-origin local mirror, so 'self' resolves and the page's
    own policy still governs. Only same-origin CSS the page itself references is mirrored;
    fonts and analytics are not, so the site chrome may differ from production. The work's
    own body is unaffected by that, which is what is under examination."""
    if not chrome:
        return {'status': 'NOT RUN — no browser found'}
    if not pages:
        return {'status': 'NOT RUN — no network'}
    os.makedirs(outdir, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix='census-mirror-')
    wanted = set()
    for slug, _ in SPECIMENS:
        html = pages[slug][1]
        os.makedirs(os.path.join(tmp, slug), exist_ok=True)
        open(os.path.join(tmp, slug, 'index.html'), 'w').write(html)
        wanted.update(re.findall(r'href="(/_astro/[^"]+\.css)"', html))
    for path in sorted(wanted):
        dest = os.path.join(tmp, path.lstrip('/'))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            open(dest, 'w').write(fetch(SITE + path)[1])
        except Exception:
            pass
    httpd, base = serve(tmp)
    shots = {}
    try:
        for slug, why in SPECIMENS:
            dest = os.path.join(outdir, 'render-%s.png' % slug)
            ok = screenshot(chrome, '%s/%s/index.html' % (base, slug), dest)
            shots[slug] = {'why': why, 'screenshot': os.path.basename(dest) if ok else None}
    finally:
        httpd.shutdown()
    return {'status': 'RUN', 'mirrored_stylesheets': sorted(wanted), 'specimens': shots}


def source_facts(slug):
    p = os.path.join(WORKS, slug, 'work.astro')
    if not os.path.exists(p):
        return {'work_astro': False}
    s = open(p, encoding='utf-8').read()
    return {
        'work_astro': True,
        'static_style_attrs': len(re.findall(r'\sstyle="', s)),
        'interpolated_style_attrs': len(re.findall(r'\sstyle=\{', s)),
        'component_style_blocks': len(re.findall(r'<style', s)),
    }


def main():
    net = '--no-net' not in sys.argv
    chrome = browser()
    slugs = sorted(d for d in os.listdir(WORKS)
                   if os.path.isdir(os.path.join(WORKS, d)))
    out = {
        'instrument': 'Served, Not Shown — render census',
        'site': SITE,
        'browser': chrome or None,
        'network': net,
        'works_examined': len(slugs),
        'layer1': [],
    }

    pages = {}
    style_src = ''
    if net:
        for slug in slugs:
            status, html = fetch(WORK_URL.format(slug=slug))
            pages[slug] = (status, html)
            if not style_src:
                style_src = directive(meta_csp(html), 'style-src')

    out['policy'] = {
        'style_src': style_src,
        'has_hash_source': "'sha256-" in style_src,
        'has_unsafe_inline': "'unsafe-inline'" in style_src,
        'has_unsafe_hashes': "'unsafe-hashes'" in style_src,
    }
    out['layer0'] = layer0(chrome, style_src) if style_src else {'status': 'NOT RUN — no policy fetched'}

    for slug in slugs:
        row = {'slug': slug}
        row.update(source_facts(slug))
        if net:
            status, html = pages[slug]
            row['http'] = status
            row['served_inline_style_attrs'] = count_inline_style_attrs(html)
        out['layer1'].append(row)

    out['layer2'] = layer2(chrome, pages, os.path.join(HERE, 'evidence'))

    served = [r for r in out['layer1'] if r.get('served_inline_style_attrs')]
    out['summary'] = {
        'works_with_served_inline_style_attrs': len(served),
        'total_served_inline_style_attrs': sum(r['served_inline_style_attrs'] for r in served),
        'works_with_zero': len([r for r in out['layer1']
                                if r.get('served_inline_style_attrs') == 0]),
    }

    json.dump(out, open(os.path.join(HERE, 'results.json'), 'w'), indent=2)
    print(json.dumps(out['policy'], indent=2))
    print(json.dumps(out['layer0'], indent=2))
    print(json.dumps(out['summary'], indent=2))
    for r in out['layer1']:
        print('%-42s served=%-4s src_static=%-4s src_interp=%-3s style_blocks=%s' % (
            r['slug'], r.get('served_inline_style_attrs', '-'),
            r.get('static_style_attrs', '-'), r.get('interpolated_style_attrs', '-'),
            r.get('component_style_blocks', '-')))


if __name__ == '__main__':
    main()
