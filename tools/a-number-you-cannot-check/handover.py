#!/usr/bin/env python3
"""The hand-over rule — session 168, 2026-09-23.

Reads a text and reports, for every percentage token in it, whether the integers that
would let a reader recompute it stand in the same sentence, and whether the printed
value agrees with them.

The rule is specified in artifacts/2026-09-23-a-number-you-cannot-check/PREREGISTRATION.md
(R-1..R-6, amended A-1..A-7, all dated before any corpus was fetched). This file implements
that specification and nothing else. No model, no network.
"""
import re
import sys

WINDOW = 40                      # A-1: no match above this character gap
INTNUM = r'(?:\d{1,3}(?:,\d{3})+|\d+)'
PCT_RE = re.compile(r'(?<![\w.,])(' + INTNUM + r'(?:\.\d+)?)\s*(%|percent\b)', re.I)
PCT_NUM_RE = re.compile(r'(?<![\w.,])(' + INTNUM + r'(?:\.\d+)?)')
PAIR_WORD_RE = re.compile(
    r'(?<![\w.,])(' + INTNUM + r')\s+(?:out\s+of|of\s+the|of|among|in)\s+(' + INTNUM + r')(?!\.\d)(?![\w])',
    re.I)
PAIR_SLASH_RE = re.compile(
    r'(?<![\w.,])(' + INTNUM + r')\s*/\s*(' + INTNUM + r')(?!\.\d)(?![\w])')
LINK_RE = re.compile(r'\[([^\]\n]*)\]\([^)\n]*\)')
TABLE_ROW_RE = re.compile(r'^\s*\|.*\|\s*$')


def normalise(text):
    """R-1, as amended by A-3."""
    text = text.replace(' ', ' ').replace(' ', ' ').replace(' ', ' ')
    text = LINK_RE.sub(r'\1', text)
    out = []
    for line in text.split('\n'):
        if TABLE_ROW_RE.match(line):
            line = line.replace('|', ' ')            # A-3: a table row is one sentence
        line = re.sub(r'^\s*#{1,6}\s*', '', line)
        line = re.sub(r'^\s*>\s?', '', line)
        line = line.replace('`', '')
        line = re.sub(r'\*+', '', line)
        line = re.sub(r'(?<![A-Za-z0-9])_+|_+(?![A-Za-z0-9])', '', line)
        out.append(line)
    return '\n'.join(out)


def sentences(text):
    """R-1: newline boundaries, then . ; ! ? followed by whitespace."""
    for line in normalise(text).split('\n'):
        start = 0
        for m in re.finditer(r'[.;!?]\s+', line):
            piece = line[start:m.end()]
            if piece.strip():
                yield piece
            start = m.end()
        tail = line[start:]
        if tail.strip():
            yield tail


def _val(s):
    return float(s.replace(',', ''))


def _decimals(s):
    return len(s.split('.')[1]) if '.' in s else 0


def _round_half_up(x, d):
    f = 10 ** d
    return float(int(x * f + 0.5)) / f if x >= 0 else -float(int(-x * f + 0.5)) / f


def _trunc(x, d):
    f = 10 ** d
    return float(int(x * f)) / f


def _matches(p, d, k, n):
    exp = 100.0 * k / n
    return abs(p - _round_half_up(exp, d)) < 1e-9 or abs(p - _trunc(exp, d)) < 1e-9


def pairs_in(sentence, pct_num_spans):
    """R-3, as amended by A-2. Returns (span, k, n) for every linked pair."""
    found = []
    for rx in (PAIR_WORD_RE, PAIR_SLASH_RE):
        for m in rx.finditer(sentence):
            k, n = _val(m.group(1)), _val(m.group(2))
            if k != int(k) or n != int(n):
                continue
            k, n = int(k), int(n)
            if not (0 <= k <= n and n >= 2):
                continue
            a = (m.start(1), m.end(1))
            b = (m.start(2), m.end(2))
            if any(s <= a[0] < e or s <= b[0] < e for s, e in pct_num_spans):   # A-2
                continue
            found.append({'span': (m.start(), m.end()), 'k': k, 'n': n})
    seen, uniq = set(), []
    for p in sorted(found, key=lambda x: x['span']):
        if p['span'] in seen:
            continue
        seen.add(p['span'])
        uniq.append(p)
    return uniq


def gap(a, b):
    return max(0, b[0] - a[1]) if b[0] >= a[1] else max(0, a[0] - b[1])


def analyse_sentence(sentence):
    """R-2, R-4 (A-1), R-5. Returns one record per percentage token, in order."""
    pcts = []
    for m in PCT_RE.finditer(sentence):
        pcts.append({'span': (m.start(), m.end()), 'num_span': (m.start(1), m.end(1)),
                     'text': m.group(0), 'value': _val(m.group(1)),
                     'decimals': _decimals(m.group(1)), 'pair': None, 'verdict': 'not_recomputable'})
    if not pcts:
        return []
    prs = pairs_in(sentence, [p['num_span'] for p in pcts])
    cands = []
    for i, p in enumerate(pcts):
        for j, q in enumerate(prs):
            g = gap(p['span'], q['span'])
            if g <= WINDOW:
                cands.append((g, i, j))
    cands.sort()
    used_p, used_q = set(), set()
    for g, i, j in cands:                                            # A-1: greedy one-to-one
        if i in used_p or j in used_q:
            continue
        used_p.add(i)
        used_q.add(j)
        k, n = prs[j]['k'], prs[j]['n']
        p = pcts[i]
        p['pair'] = [k, n]
        p['gap'] = g
        if _matches(p['value'], p['decimals'], k, n):
            p['verdict'] = 'consistent'
        elif _matches(p['value'], p['decimals'], n - k, n):
            p['verdict'] = 'complement'
        else:
            p['verdict'] = 'inconsistent'
    for p in pcts:
        p.pop('num_span', None)
        p['span'] = list(p['span'])
    return pcts


def analyse(text, doc_id=None):
    """Every percentage token in a document, with its sentence."""
    out = []
    for si, sent in enumerate(sentences(text)):
        for tok in analyse_sentence(sent):
            tok['sentence'] = sent.strip()
            tok['sentence_index'] = si
            if doc_id is not None:
                tok['doc'] = doc_id
            out.append(tok)
    return out


if __name__ == '__main__':
    import json
    txt = sys.stdin.read()
    print(json.dumps(analyse(txt), indent=2, ensure_ascii=False))
