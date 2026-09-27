#!/usr/bin/env python3
"""Render the page in a real browser, scripting on and off, at three widths; then operate
the radio controls with scripting OFF and check the readout shows exactly the row the data
says. Session 172, 2026-09-27."""
import glob, json, os, sys
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.abspath(os.path.join(HERE, '..', '..', 'artifacts/2026-09-27-the-range-of-the-method'))
L = json.load(open(os.path.join(ART, 'data/lattice.json')))
url = 'file://' + os.path.join(ART, 'index.html')
exe = sorted(glob.glob('/opt/pw-browsers/chromium*/chrome-linux/chrome'))[-1]
out = {'note': 'Rendered from the filesystem. The page carries no JavaScript; its controls are '
               'radio buttons read by CSS, so they are operated here with scripting off.',
       'widths': [], 'operated': []}
VIS = "Array.from(document.querySelectorAll('tbody.row')).filter(e=>getComputedStyle(e).display!=='none')"
TRIALS = [
    {'w-all': 1, 'c-full': 1, 's-newline': 1, 'p-many': 1, 't-fetched': 1, 'm-round-or-trunc': 1},
    {'w-40': 1, 'c-words-only': 1, 's-semi': 1, 'p-greedy': 1, 't-fetched': 1, 'm-half-point': 1},
    {'w-10': 1, 'c-slash-only': 1, 's-nosemi': 1, 'p-many': 1, 't-decoded': 1, 'm-last-digit': 1},
]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe)
    for js in (True, False):
        for w in (390, 768, 1280):
            ctx = b.new_context(viewport={'width': w, 'height': 900}, java_script_enabled=js)
            pg = ctx.new_page()
            errs, reqs = [], []
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            pg.on('request', lambda r: reqs.append(r.url) if not r.url.startswith('file:') else None)
            pg.goto(url, wait_until='load')
            sw, iw = pg.evaluate('[document.documentElement.scrollWidth, window.innerWidth]')
            out['widths'].append({'width': w, 'javascript': js, 'horizontal_overflow': sw > iw,
                                  'console_errors': len(errs), 'network_requests': len(reqs),
                                  'script_elements': pg.evaluate("document.scripts.length")})
            ctx.close()
    ctx = b.new_context(viewport={'width': 390, 'height': 900}, java_script_enabled=False)
    pg = ctx.new_page()
    pg.goto(url, wait_until='load')
    n0 = len(pg.query_selector_all('tbody.row'))
    shown = pg.eval_on_selector_all('tbody.row', 'es=>es.filter(e=>getComputedStyle(e).display!=="none").map(e=>e.className)')
    out['operated'].append({'state': 'initial', 'row_groups': n0, 'visible': shown})
    for t in TRIALS:
        for i in t:
            pg.check(f'input[id="{i}"]')
        vis = pg.eval_on_selector_all('tbody.row', 'es=>es.filter(e=>getComputedStyle(e).display!=="none").map(e=>e.querySelector("td").textContent)')
        cls = pg.eval_on_selector_all('tbody.row', 'es=>es.filter(e=>getComputedStyle(e).display!=="none").map(e=>e.className)')
        red = pg.eval_on_selector_all('circle.dot', 'es=>es.filter(e=>getComputedStyle(e).opacity>0.8).length')
        out['operated'].append({'state': sorted(t), 'visible_rows': len(vis), 'M_rate_shown': vis,
                                'classes': cls, 'full_opacity_dots': red})
    b.close()
json.dump(out, open(os.path.join(ART, 'data/render-check.json'), 'w'), indent=1)
print(json.dumps(out, indent=1)[:3000])
