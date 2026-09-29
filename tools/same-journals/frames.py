#!/usr/bin/env python3
"""Re-fetch the 2021 (09-28) and 2026 (09-23 pin) frames by PMID; keep only digest matches.

    frames.py <raw_dir>
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools', 'twenty-augusts'))
import fetch as F                                                  # noqa: E402

SRC = {'2021': (os.path.join(ROOT, 'artifacts/2026-09-28-twenty-augusts/data/corpora.json'), '2021'),
       '2026': (os.path.join(ROOT, 'artifacts/2026-09-23-a-number-you-cannot-check/data/corpora.json'), 'M')}


def main():
    out = {}
    for y, (path, key) in SRC.items():
        pin = {d['id']: d['sha256'] for d in json.load(open(path))[key]['docs']}
        docs = F.efetch(list(pin))
        ok = [d for d in docs if hashlib.sha256(d['text'].encode('utf-8')).hexdigest() == pin.get(d['id'])]
        out[y] = {'pinned': len(pin), 'returned': len(docs), 'digest_matched': len(ok), 'docs': ok}
        print(y, len(pin), len(docs), len(ok))
    json.dump(out, open(os.path.join(sys.argv[1], 'frames.json'), 'w'), ensure_ascii=False)


if __name__ == '__main__':
    main()
