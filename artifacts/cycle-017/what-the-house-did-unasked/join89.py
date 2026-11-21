#!/usr/bin/env python3
"""Reading 89 (session 287, 2026-11-21): does Git alone join each deed of the decision log to its mending, and does it
lead from the deed to the mending? Rules in CODEBOOK89.md, predictions in PREDICTIONS89.md.

Usage: python3 join89.py <dir holding full bare clones named <repo>.git>
Reads credit88.json beside this file; writes join89.json (per pair: hashes, paths counted, codes; no line of any commit
is copied, so that nothing of the old record is published again).
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEEN_BEFORE = {'e6558c8', '86532f4', 'd93ca69', 'd34d42a', 'c538beb'}
HUNK = re.compile(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@')
ENV = {**os.environ, 'GIT_NO_LAZY_FETCH': '1'}  # a blob the clone lacks (over 2 MB) is never fetched: its path is unread
UNREAD = set()  # (repo, path) pairs whose blobs the clone lacks, reported per pair
NULL = '0' * 40


def git(clones, repo, *args):
    r = subprocess.run(['git', '--git-dir', str(clones / f'{repo}.git'), *args], capture_output=True, env=ENV)
    return r.returncode, r.stdout.decode('utf-8', 'replace')


def present(clones, repo, blob):
    if blob == NULL:
        return True
    r = subprocess.run(['git', '--git-dir', str(clones / f'{repo}.git'), 'cat-file', '-e', blob], capture_output=True,
                       env=ENV)
    return r.returncode == 0


def parents(clones, repo, h):
    code, out = git(clones, repo, 'rev-list', '--parents', '-n', '1', h)
    if code != 0 or not out.strip():
        return None
    return out.split()[1:]


def is_ancestor(clones, repo, a, b):
    r = subprocess.run(['git', '--git-dir', str(clones / f'{repo}.git'), 'merge-base', '--is-ancestor', a, b],
                       capture_output=True, env=ENV)
    return r.returncode == 0


def ctime(clones, repo, h):
    code, out = git(clones, repo, 'show', '-s', '--format=%ct', h)
    return int(out.strip()) if code == 0 and out.strip() else None


def diff(clones, repo, a, b, paths=None):
    """Removed line numbers (old side) per old path, added texts per new path, changed paths."""
    raw = ['diff', '--raw', '--no-abbrev', '--no-renames', '-z', a, b]
    if paths:
        raw += ['--', *paths]
    code, out = git(clones, repo, *raw)
    parts = out.split('\0')
    entries, paths_changed = [], set()
    for i in range(0, len(parts) - 1, 2):
        meta, path = parts[i], parts[i + 1]
        f = meta.split()
        if len(f) < 5:
            continue
        paths_changed.add(path)
        entries.append((path, f[2], f[3]))
    blobs = sorted({b for _, x, y in entries for b in (x, y) if b != NULL})
    missing = set()
    if blobs:
        r = subprocess.run(['git', '--git-dir', str(clones / f'{repo}.git'), 'cat-file', '--batch-check'],
                           input=('\n'.join(blobs) + '\n').encode(), capture_output=True, env=ENV)
        missing = {ln.split()[0] for ln in r.stdout.decode().split('\n') if ln.endswith(' missing')}
    readable = []
    for path, x, y in entries:
        if x in missing or y in missing:
            UNREAD.add((repo, path))
        else:
            readable.append(path)
    removed, removed_text, added_text = {}, {}, {}
    if not readable:
        return removed, removed_text, added_text, paths_changed
    code, out = git(clones, repo, 'diff', '-U0', '--no-color', '--no-ext-diff', '--no-renames', a, b, '--', *readable)
    old = new = None
    oline = 0
    for line in out.split('\n'):
        if line.startswith('diff --git '):
            old = new = None
            continue
        if line.startswith('--- '):
            old = None if line[4:] == '/dev/null' else line[6:]
            continue
        if line.startswith('+++ '):
            new = None if line[4:] == '/dev/null' else line[6:]
            continue
        m = HUNK.match(line)
        if m:
            oline = int(m.group(1))
            continue
        if line.startswith('-') and old:
            removed.setdefault(old, []).append(oline)
            removed_text.setdefault(old, {})[oline] = line[1:]
            oline += 1
        elif line.startswith('+') and new:
            added_text.setdefault(new, set()).add(line[1:])
    return removed, removed_text, added_text, paths_changed


def ranges(nums):
    nums = sorted(set(nums))
    out, start, prev = [], None, None
    for n in nums:
        if start is None:
            start = prev = n
        elif n == prev + 1:
            prev = n
        else:
            out.append((start, prev))
            start = prev = n
    if start is not None:
        out.append((start, prev))
    return out


def blame(clones, repo, rev, path, nums):
    """The commits git blame at rev gives the listed line numbers of path."""
    args = ['blame', '-l', '-s', '--no-progress']
    for a, b in ranges(nums):
        args += ['-L', f'{a},{b}']
    args += [rev, '--', path]
    code, out = git(clones, repo, *args)
    if code != 0:
        return None
    return {ln.split()[0].lstrip('^') for ln in out.split('\n') if ln.strip()}


def deed_set(clones, repo, hashes):
    """The deed's commits in repo, merges expanded to the commits they brought in."""
    full = set()
    for h in hashes:
        ps = parents(clones, repo, h)
        if ps is None:
            continue
        code, out = git(clones, repo, 'rev-parse', h)
        full.add(out.strip())
        if len(ps) > 1:
            code, out = git(clones, repo, 'rev-list', f'{ps[0]}..{h}')
            full.update(x for x in out.split() if x)
    return full


def takes_out(clones, repo, c, deed, prefilter=None):
    """How many lines commit c removes or rewrites that blame at its first parent gives to the deed."""
    ps = parents(clones, repo, c)
    if not ps:
        return 0, 0
    removed, removed_text, _, _ = diff(clones, repo, ps[0], c)
    hits = blamed = 0
    for path, nums in removed.items():
        if prefilter is not None:
            nums = [n for n in nums if removed_text[path][n] in prefilter]
            if not nums:
                continue
        blamed += len(nums)
        args = ['blame', '-l', '-s', '--no-progress']
        for a, b in ranges(nums):
            args += ['-L', f'{a},{b}']
        args += [ps[0], '--', path]
        code, out = git(clones, repo, *args)
        if code != 0:
            UNREAD.add((repo, path))
            continue
        for ln in out.split('\n'):
            if ln.strip() and ln.split()[0].lstrip('^') in deed:
                hits += 1
    return hits, blamed


def main():
    clones = Path(sys.argv[1]).resolve()
    c88 = json.loads((HERE / 'credit88.json').read_text())
    out = []
    for d in c88['deeds']:
        if not d.get('repair_found'):
            continue
        repo = d['repair_repo']
        m = d['repair_hash']
        UNREAD.clear()
        same_repo = [c['hash'] for c in d['deed_commits'] if c['repo'] == repo]
        deed = deed_set(clones, repo, same_repo)
        rec = {'row': d['row'], 'deed': d['deed'], 'log_line': d['log_line'], 'repair': m, 'repair_repo': repo,
               'deed_repos': sorted({c['repo'] for c in d['deed_commits']}), 'deed_commits_in_repair_repo': len(deed),
               'seen_before': any(m.startswith(s) for s in SEEN_BEFORE)}
        rec['same_commit'] = m in deed
        rec['deed_on_path'] = all(is_ancestor(clones, repo, h, m) for h in same_repo) if same_repo else None
        # paths the deed changed, in the mending's repository
        dpaths, dadded = set(), set()
        for h in deed:
            ps = parents(clones, repo, h)
            if ps is None or len(ps) > 1:
                continue
            base = ps[0] if ps else '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
            _, _, added, changed = diff(clones, repo, base, h)
            dpaths |= changed
            for texts in added.values():
                dadded |= texts
        mps = parents(clones, repo, m) or []
        if mps:
            _, _, _, mchanged = diff(clones, repo, mps[0], m)
        else:
            mchanged = set()
        rec['deed_paths'] = len(dpaths)
        rec['shared_paths'] = len(dpaths & mchanged)
        rec['file'] = bool(dpaths & mchanged)
        if rec['same_commit'] or not mps:
            rec['lines_taken_out'] = None
            rec['lines'] = False
        else:
            hits, blamed = takes_out(clones, repo, m, deed)
            rec['lines_taken_out'] = hits
            rec['lines_removed_blamed'] = blamed
            rec['lines'] = hits > 0
        rec['name'] = bool(d.get('names_deed'))
        if rec['same_commit']:
            code = 'same_commit'
        elif rec['lines']:
            code = 'lines'
        elif rec['name']:
            code = 'name'
        elif rec['file']:
            code = 'file'
        else:
            code = 'log_only'
        rec['code'] = code
        rec['class'] = {'same_commit': 'joined', 'lines': 'joined', 'name': 'joined', 'file': 'file',
                        'log_only': 'log'}[code]
        # from the deed alone
        if rec['lines']:
            latest = max(deed, key=lambda h: ctime(clones, repo, h) or 0)
            if is_ancestor(clones, repo, latest, mps[0]):
                code_, revs = git(clones, repo, 'rev-list', '--no-merges', f'{latest}..{mps[0]}', '--',
                                  *sorted(dpaths))
                cands = [c for c in revs.split() if c and c not in deed]
            else:
                cands = None
            if cands is None:
                rec['git_points'] = None
                rec['candidates'] = None
                rec['heirs_before'] = None
            else:
                heirs = []
                alnum = {t for t in dadded if re.search(r'[A-Za-z0-9]', t)}
                for c in reversed(cands):  # oldest first; the first earlier heir decides
                    hits, _ = takes_out(clones, repo, c, deed, prefilter=alnum)
                    if hits:
                        heirs.append(c)
                        break
                rec['candidates'] = len(cands)
                rec['heirs_before'] = len(heirs)
                rec['heirs_before_hashes'] = heirs
                rec['git_points'] = not heirs
        rec['unread_paths'] = sorted(p for _, p in UNREAD)
        out.append(rec)
        print(rec['row'], rec['deed'], repo, m[:7], rec['code'], rec.get('git_points'), rec.get('heirs_before'),
              file=sys.stderr, flush=True)

    def summary(rows):
        s = {'pairs': len(rows)}
        for k in ('same_commit', 'lines', 'name', 'file', 'log_only'):
            s[k] = sum(r['code'] == k for r in rows)
        for k in ('joined', 'file', 'log'):
            s['class_' + k] = sum(r['class'] == k for r in rows)
        s['lines_any'] = sum(bool(r['lines']) for r in rows)
        s['name_any'] = sum(bool(r['name']) for r in rows)
        s['file_any'] = sum(bool(r['file']) for r in rows)
        lines = [r for r in rows if r['code'] == 'lines']
        decided = [r for r in lines if r.get('git_points') is not None]
        s['lines_pairs'] = len(lines)
        s['points_decided'] = len(decided)
        s['git_points'] = sum(r['git_points'] for r in decided)
        s['not_on_path'] = len(lines) - len(decided)
        s['with_unread'] = sum(bool(r['unread_paths']) for r in rows)
        s['P145'] = ('held' if s['git_points'] * 2 >= len(decided) else 'failed') if decided else 'undecided'
        return s

    res = {'reading': 89, 'session': 287, 'date': '2026-11-21', 'all': summary(out),
           'without_seen_before': summary([r for r in out if not r['seen_before']])}
    (HERE / 'join89.json').write_text(json.dumps({'results': res, 'pairs': out}, indent=1, ensure_ascii=False) + '\n')
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
