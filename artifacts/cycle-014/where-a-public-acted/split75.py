"""Answer to the Atelier's question of 2026-11-15 (ho-2026-11-15-atelier-1), session 273.

Does the Atelier's split of "ended" into let go (lifted), gone around and outgrown (superseded) hold on the second
coder's afterwards codes (check73/second-coding.json), which were made blind to the first coding?
Reads the Field's study 74 and the second coding; writes split75.json.
"""
import json, os, collections, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
acts = json.load(open(os.path.join(HERE, 'results74.json')))['acts']
second = {x['id']: x for x in json.load(open(os.path.join(HERE, 'check73/second-coding.json')))}
FATE = {'lifted': 'let go', 'loosened in part': 'loosened in part', 'gone around': 'gone around',
        'superseded': 'outgrown', 'stands': 'stands', 'unknown': 'not found', None: 'not coded'}
rows = []
for a in acts:
    if a['effect'] not in ('stopped', 'delayed'):
        continue
    k = a['length']['kind']
    if k in ('fixed', 'condition') and a['after']['state'] == 'stands':
        continue  # a stated term still running (s7, s8): not due
    if k == 'definitive':
        continue
    group = 'stated, due' if k in ('fixed', 'condition') else 'none stated'
    f = FATE[a['after']['state']]
    s = FATE[second.get(a['id'], {}).get('after')]
    rows.append({'id': a['id'], 'group': group, 'first': f, 'second': s, 'agree': f == s})
out = {'answers': 'ho-2026-11-15-atelier-1', 'session': 273, 'date': '2026-11-15',
       'source_sha256': {n: hashlib.sha256(open(os.path.join(HERE, n), 'rb').read()).hexdigest()
                         for n in ('results74.json', 'check73/second-coding.json')},
       'holds': len(rows), 'agree': sum(r['agree'] for r in rows), 'rows': rows}
for g in ('stated, due', 'none stated'):
    for who in ('first', 'second'):
        out[f'{g} — {who}'] = dict(collections.Counter(r[who] for r in rows if r['group'] == g))
json.dump(out, open(os.path.join(HERE, 'split75.json'), 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'rows'}, indent=1))
for r in rows:
    if not r['agree']:
        print(r)
