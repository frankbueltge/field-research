"""Study 64, step 1: reduce each fetched page to text and locate every claim's number.
Usage: python3 -I extract64.py <pages-dir>   (pages-dir holds urls.txt and p<i>.bin from the fetch)
Writes snippets64.json beside this script: for every claim, the page status and up to three passages
(at most 240 characters each) around a matched token. Page texts stay outside the repository."""
import json, re, subprocess, sys, html
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
pages = Path(sys.argv[1])
urls = [u.strip() for u in (pages / 'urls.txt').read_text().splitlines() if u.strip()]
claims = json.loads((HERE / 'claims64.json').read_text())['claims']

class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0
    def handle_starttag(self, t, a):
        if t in ('script', 'style', 'noscript', 'svg'): self.skip += 1
        if t in ('p', 'br', 'li', 'div', 'h1', 'h2', 'h3', 'h4', 'tr', 'td'): self.out.append('\n')
    def handle_endtag(self, t):
        if t in ('script', 'style', 'noscript', 'svg') and self.skip: self.skip -= 1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)

def text_of(i):
    raw = (pages / f'p{i}.bin').read_bytes()
    if raw[:4] == b'%PDF':
        return subprocess.run(['pdftotext', '-layout', str(pages / f'p{i}.bin'), '-'], capture_output=True, text=True).stdout
    p = Text(); p.feed(raw.decode('utf-8', 'replace')); t = html.unescape(''.join(p.out))
    return t

texts, status = {}, {}
for i, u in enumerate(urls, 1):
    alt = pages / f'p{i}.alt.txt'          # second route, if the first was refused
    t = text_of(i)
    if len(t.strip()) < 2000 and alt.exists():
        texts[u] = alt.read_text(); status[u] = 'second route'
    elif len(t.strip()) < 2000:
        texts[u] = ''; status[u] = 'refused'
    else:
        texts[u] = t; status[u] = 'plain client'

def norm(s):
    s = s.replace(' ', ' ').replace(' ', ' ').replace(' ', ' ')
    return re.sub(r'[ \t]+', ' ', s)

out = []
for c in claims:
    t = norm(texts[c['url']]); snips = []
    for tok in c['tokens']:
        for m in re.finditer(re.escape(tok), t):
            a, b = max(0, m.start() - 110), min(len(t), m.end() + 110)
            s = re.sub(r'\s+', ' ', t[a:b]).strip()
            if s not in snips: snips.append(s)
            if len(snips) >= 6: break
    out.append({'id': c['id'], 'cand': c['cand'], 'url': c['url'], 'route': status[c['url']],
                'says': c['says'], 'hits': len(snips), 'snippets': snips[:6]})
(HERE / 'snippets64.json').write_text(json.dumps(out, indent=1, ensure_ascii=False))
print({u.split('/')[2]: (status[u], len(texts[u])) for u in urls})
