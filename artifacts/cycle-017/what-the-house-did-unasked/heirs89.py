#!/usr/bin/env python3
"""Reading 89 (session 287): for each pair whose mending was not the first commit to take out a line of the deed
(join89.json, git_points false), when that earlier heir came and whose name Git gives it. Descriptive, not a prediction.

Usage: python3 heirs89.py <dir holding the bare clones named <repo>.git>
Writes heirs89.json (hashes, times and signer codes only; no commit message is copied).
"""
import json
import statistics
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent


def signer(an):
    if an.strip() == 'Frank Bültge':
        return "the architect's name"
    if an.strip().split(' ')[0] in ('Meridian', 'Ulysses', 'Assay', 'Ensemble'):
        return "a practice's persona"
    return 'a workflow or bot'


def main():
    clones = Path(sys.argv[1]).resolve()
    jn = json.loads((HERE / 'join89.json').read_text())['pairs']
    cr = {(d['row'], d['deed']): d for d in json.loads((HERE / 'credit88.json').read_text())['deeds']}
    rows = []
    for p in jn:
        if p['code'] != 'lines' or p.get('git_points') is not False:
            continue
        c, repo, h = cr[(p['row'], p['deed'])], p['repair_repo'], p['heirs_before_hashes'][0]
        out = subprocess.run(['git', '--git-dir', str(clones / f'{repo}.git'), 'show', '-s', '--format=%H%x00%an%x00%aI', h],
                             capture_output=True, text=True).stdout.strip()
        full, an, at = out.split('\x00')
        deed_t = max(datetime.fromisoformat(x['time']) for x in c['deed_commits'] if x['repo'] == repo)
        heir_t, mend_t = datetime.fromisoformat(at), datetime.fromisoformat(c['repair_time'])
        is_mending = any(q['repair'] == full for q in jn)
        rows.append({'row': p['row'], 'deed': p['deed'], 'repo': repo, 'heir': full, 'signer': signer(an),
                     'hours_after_deed': round((heir_t - deed_t).total_seconds() / 3600, 1),
                     'days_before_mending': round((mend_t - heir_t).total_seconds() / 86400, 1),
                     'heir_is_a_mending': is_mending})
    hrs = [r['hours_after_deed'] for r in rows]
    res = {'pairs': len(rows), 'median_hours': statistics.median(hrs), 'within_1h': sum(h < 1 for h in hrs),
           'within_24h': sum(h < 24 for h in hrs),
           'signers': {k: sum(r['signer'] == k for r in rows) for k in sorted({r['signer'] for r in rows})},
           'heir_is_a_mending': sum(r['heir_is_a_mending'] for r in rows)}
    (HERE / 'heirs89.json').write_text(json.dumps({'results': res, 'heirs': rows}, indent=1, ensure_ascii=False) + '\n')
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
