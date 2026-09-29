#!/usr/bin/env python3
"""Same journals, two years — session 174, 2026-09-29. Build and fetch the journal panel.

    fetch.py <raw_dir>

Extraction and HTTP are imported from 09-28's tools/twenty-augusts/fetch.py, unedited.
Raw texts stay outside the repository.
"""
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import urllib.parse
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'twenty-augusts'))
import fetch as F                                                  # noqa: E402

FRAME21 = os.path.join(ROOT, 'artifacts/2026-09-28-twenty-augusts/data/corpora.json')
FRAME26 = os.path.join(ROOT, 'artifacts/2026-09-23-a-number-you-cannot-check/data/corpora.json')
TERM = '{jid}[jid] AND randomized controlled trial[pt] AND hasabstract AND {y}/01/01:{y}/06/30[dp]'
PER, MIN = 25, 10


def journals(pmids):
    out = {}
    for i in range(0, len(pmids), 200):
        q = urllib.parse.urlencode({'db': 'pubmed', 'id': ','.join(pmids[i:i + 200]), 'retmode': 'json'})
        r = json.loads(F.get(F.EUTILS + 'esummary.fcgi?' + q))['result']
        for p in pmids[i:i + 200]:
            if p in r:
                out[p] = {'jid': r[p].get('nlmuniqueid'), 'source': r[p].get('source')}
        time.sleep(0.4)
    return out


def sample(jid, y):
    q = urllib.parse.urlencode({'db': 'pubmed', 'term': TERM.format(jid=jid, y=y), 'retmax': PER,
                                'retmode': 'json', 'sort': 'pub_date'})
    res = json.loads(F.get(F.EUTILS + 'esearch.fcgi?' + q))['esearchresult']
    time.sleep(0.4)
    docs = F.efetch(res['idlist']) if res['idlist'] else []
    return {'count': int(res['count']), 'docs': docs}


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    f21 = [d['id'] for d in json.load(open(FRAME21))['2021']['docs']]
    f26 = [d['id'] for d in json.load(open(FRAME26))['M']['docs']]
    meta = {'2021': journals(f21), '2026': journals(f26)}
    json.dump(meta, open(os.path.join(out, 'frame_journals.json'), 'w'))
    c21 = Counter(v['jid'] for v in meta['2021'].values())
    c26 = Counter(v['jid'] for v in meta['2026'].values())
    cand = sorted({j for j, n in c21.items() if n >= 2} | {j for j, n in c26.items() if n >= 2})
    print('frame journal lookups', len(meta['2021']), len(meta['2026']), 'candidates', len(cand))
    cache = os.path.join(out, 'cache')
    os.makedirs(cache, exist_ok=True)

    def one(jid):
        path = os.path.join(cache, jid + '.json')
        if os.path.exists(path):
            return jid, json.load(open(path, encoding='utf-8'))
        rec = {str(y): sample(jid, y) for y in (2021, 2026)}
        ok = all(len(rec[str(y)]['docs']) >= MIN for y in (2021, 2026))
        if ok:
            rec['2025'] = sample(jid, 2025)
        rec['qualifies'] = ok
        json.dump(rec, open(path, 'w'), ensure_ascii=False)
        print(jid, [len(rec[str(y)]['docs']) for y in (2021, 2026)], ok, flush=True)
        return jid, rec

    with ThreadPoolExecutor(3) as ex:                 # three workers, each sleeping between calls
        panel = dict(ex.map(one, cand))
    json.dump({'fetched_at_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
               'term': TERM, 'per': PER, 'min': MIN, 'panel': panel},
              open(os.path.join(out, 'panel.json'), 'w'), ensure_ascii=False)


if __name__ == '__main__':
    main()
