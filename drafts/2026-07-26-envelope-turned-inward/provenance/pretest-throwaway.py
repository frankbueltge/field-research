"""Feasibility pretest (SIZES ONLY — no metric values).

Throwaway script. Splits journal/*.md into top-level session sections, applies the
exclusion rules the pre-registration will fix, and reports token counts only.
"""
import os
import re
import sys
import glob

sys.path.insert(0, "/home/user/field-research/works/2026-07-25-no-signal-to-extend/scripts")
from tokenizer import tokenize

FENCE = re.compile(r"^\s*```")
BLOCKQUOTE = re.compile(r"^\s*>")
TABLE = re.compile(r"^\s*\|")
HEADING = re.compile(r"^\s*#")
INLINE_CODE = re.compile(r"`[^`]*`")


def prose_lines(lines):
    out = []
    in_fence = False
    for ln in lines:
        if FENCE.match(ln):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if BLOCKQUOTE.match(ln) or TABLE.match(ln) or HEADING.match(ln):
            continue
        out.append(INLINE_CODE.sub(" ", ln))
    return out


units = []
for path in sorted(glob.glob("/home/user/field-research/journal/*.md")):
    date = os.path.basename(path)[:-3]
    lines = open(path, encoding="utf-8").read().split("\n")
    idxs = [i for i, ln in enumerate(lines) if ln.startswith("# ")]
    for k, start in enumerate(idxs):
        end = idxs[k + 1] if k + 1 < len(idxs) else len(lines)
        heading = lines[start][2:].strip()
        body = prose_lines(lines[start + 1:end])
        toks = tokenize("\n".join(body))
        units.append((date, k, heading, len(toks), len(set(toks))))

print("total units:", len(units))
counts = sorted(u[3] for u in units)
print("min/p5/median/p95/max tokens:", counts[0], counts[len(counts)//20], counts[len(counts)//2],
      counts[int(len(counts)*0.95)], counts[-1])
print("total tokens:", sum(counts))
print("units below 400/600/800/1000/1200/1500 tokens:",
      [sum(1 for c in counts if c < t) for t in (400, 600, 800, 1000, 1200, 1500)])
print()
print("idx date       ntok  ntypes  heading")
for i, (date, k, heading, n, t) in enumerate(units, 1):
    print(f"{i:3d} {date} {n:6d} {t:6d}  {heading[:70]}")
print()
from collections import Counter
print("units per date:", sorted(Counter(u[0] for u in units).items()))

# works corpus (secondary series)
print()
print("=== works README prose ===")
for path in sorted(glob.glob("/home/user/field-research/works/*/README.md")):
    lines = open(path, encoding="utf-8").read().split("\n")
    toks = tokenize("\n".join(prose_lines(lines)))
    print(f"{os.path.basename(os.path.dirname(path))[:44]:46s} {len(toks):6d} {len(set(toks)):5d}")
