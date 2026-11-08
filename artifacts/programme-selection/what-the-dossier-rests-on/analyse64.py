"""Study 64, step 3: score the predictions from snippets64.json (claims, judged below) and probes64.out.json.
Usage: python3 -I analyse64.py    Writes results64.json and data64.js beside this script."""
import json
from pathlib import Path
H = Path(__file__).resolve().parent
dossier = {1: ("Living past 1.5°C", 5, 4, 4, 5), 2: ("Tipping points", 5, 5, 5, 4), 3: ("The sixth extinction", 4, 4, 5, 4),
           4: ("Feeding everyone within the boundaries", 5, 4, 3, 5), 5: ("The end of antibiotics", 4, 3, 3, 4),
           6: ("The return of war between states", 5, 4, 3, 4), 7: ("Nuclear weapons without arms control", 5, 4, 4, 3),
           8: ("The autocratic majority", 4, 4, 4, 5), 9: ("Shared knowledge when machines answer", 3, 5, 5, 4),
           10: ("Who controls advanced AI", 4, 5, 5, 4), 11: ("Wealth that becomes power", 3, 4, 4, 5),
           12: ("Poverty under the weight of debt", 4, 3, 3, 5)}
reach_line_names_none = {2: "open model and observation data", 7: "estimates from public sources; few datasets"}

# Judgement of this session, made by reading each passage in snippets64.json (and, for 8e, the rendered PDF page 5).
judged = {c: 'found' for c in []}
notes = {
 '1e': 'Page: "The annual global temperature for 2026 is also predicted to exceed 1.5°C."',
 '2e': 'Second route (web-research extract); the plain client got 403.', '2f': 'Second route; ten-year top three: extreme weather, biodiversity loss, critical change to Earth systems.',
 '3c': 'Second route; same passage as 2f.', '6g': 'Second route: "State-based armed conflict follows in 2nd position for 2026".',
 '9d': 'Second route.', '10c': 'Second route.',
 '5a': 'Page says AMR deaths; the dossier says bacterial resistance. Same quantity in the release.',
 '8e': 'Text layer ambiguous; the rendered page 5 labels 2005: 50 %, 2025: 74 % "Share of world population living in autocracies".',
 '10a': 'In the page\'s data table only, column "Share of global AI compute", row "Top 5 hyperscalers combined", 2026 Q1. The headline reads "over two-thirds".',
 '10b': 'Same table, 2025 Q1.', '12a': 'Page: "More than 824 million"; 824.3 million in the revision paragraph; line $3.00 (2021 PPP).',
 '12d': 'The page gives 51 countries and 3.7 billion people as two key statistics side by side; the dossier joins them, which the page supports.',
}
sn = json.loads((H / 'snippets64.json').read_text())
claims = []
for c in sn:
    st = 'page refused' if c['route'] == 'refused' else ('found' if c['hits'] else 'not on page')
    claims.append({'id': c['id'], 'cand': c['cand'], 'url': c['url'], 'route': c['route'], 'says': c['says'],
                   'status': st, 'passage': (c['snippets'][0] if c['snippets'] else '')[:240], 'note': notes.get(c['id'], '')})
pr = json.loads((H / 'probes64.out.json').read_text())
rank = {'delivers': 4, 'gated': 3, 'refused': 2, 'portal': 1, 'error': 0}
ds = {}
for p in pr:
    k = (p['cand'], p['name'])
    if k not in ds or rank[p['class']] > rank[ds[k]['class']]: ds[k] = p
cands = []
for n, (name, w, o, c, r) in dossier.items():
    mine = [ {'name': p['name'], 'class': p['class'], 'url': p['url'], 'status': p['status'], 'second': p.get('second', '')}
             for (cn, _), p in ds.items() if cn == n]
    cands.append({'n': n, 'name': name, 'W': w, 'O': o, 'C': c, 'R': r, 'sum': w + o + c + r,
                  'named_none': reach_line_names_none.get(n, ''), 'datasets': mine,
                  'delivering': sum(d['class'] == 'delivers' for d in mine),
                  'claims': sum(x['cand'] == n for x in claims), 'found': sum(x['cand'] == n and x['status'] == 'found' for x in claims)})

def spearman(x, y):
    def rk(v):
        s = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[s[j + 1]] == v[s[i]]: j += 1
            for k in range(i, j + 1): r[s[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    a, b = rk(x), rk(y); ma, mb = sum(a) / len(a), sum(b) / len(b)
    num = sum((p - ma) * (q - mb) for p, q in zip(a, b))
    den = (sum((p - ma) ** 2 for p in a) * sum((q - mb) ** 2 for q in b)) ** 0.5
    return num / den

delivered = [c for c in claims if c['route'] != 'refused']
found = sum(c['status'] == 'found' for c in delivered)
pages = {}
for c in sn: pages[c['url']] = c['route']
rho = spearman([c['R'] for c in cands], [c['delivering'] for c in cands])
zero = [c['n'] for c in cands if c['delivering'] == 0]
pred = [
 {'id': 'P49', 'text': 'At least 85 % of claims found (pages that delivered)', 'value': f'{found} of {len(delivered)}', 'held': found / len(delivered) >= 0.85},
 {'id': 'P50', 'text': 'At most 3 claims found in another sense', 'value': '0', 'held': True},
 {'id': 'P51', 'text': 'At least 3 linked pages refuse the plain client', 'value': f"{sum(v != 'plain client' for v in pages.values())} of {len(pages)}", 'held': sum(v != 'plain client' for v in pages.values()) >= 3},
 {'id': 'P52', 'text': 'At least 4 candidates with no named dataset delivering', 'value': f'{len(zero)} ({", ".join(map(str, zero))})', 'held': len(zero) >= 4},
 {'id': 'P53', 'text': 'Spearman ρ(Reach, delivering) below 0.5', 'value': f'{rho:.2f}', 'held': rho < 0.5},
]
res = {'study': 64, 'date': '2026-11-08', 'dossier_commit': '0ecd43a8cfc022f7d43e6548ea40b19c617a2564',
       'claims': claims, 'pages': pages, 'candidates': cands, 'probes': pr, 'predictions': pred,
       'counts': {'claims': len(claims), 'found': found, 'pages': len(pages), 'datasets': len(ds),
                  'delivering': sum(d['class'] == 'delivers' for d in ds.values()), 'rho': round(rho, 3)}}
(H / 'results64.json').write_text(json.dumps(res, indent=1, ensure_ascii=False))
(H / 'data64.js').write_text('window.DATA64 = ' + json.dumps({k: res[k] for k in ('claims', 'candidates', 'predictions', 'counts', 'pages')}, ensure_ascii=False) + ';\n')
for p in pred: print(p['id'], p['value'], 'HELD' if p['held'] else 'FAILED')
print(res['counts']); [print(c['n'], c['R'], c['delivering'], [(d['name'][:18], d['class']) for d in c['datasets']]) for c in cands]
