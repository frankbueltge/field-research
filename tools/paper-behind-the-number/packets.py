#!/usr/bin/env python3
"""Reading packets for the sampled units: the abstract sentence, and every place in the full
text (body paragraphs; table rows shown with their caption and header) where the printed number
string appears. A reading aid only — verdicts are written by hand in reading.json."""
import html, json, os, re, sys

W = sys.argv[1]


def clean(s):
    s = re.sub(r"</t[dh]>", " | ", s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def blocks(xml):
    x = re.sub(r"<front>.*?</front>|<ref-list[ >].*?</ref-list>|<abstract[ >].*?</abstract>", " ", xml, flags=re.S)
    out = []
    for tw in re.finditer(r"<table-wrap[ >].*?</table-wrap>", x, re.S):
        t = tw.group(0)
        cap = clean(" ".join(re.findall(r"<label>.*?</label>|<caption>.*?</caption>", t, re.S)))[:300]
        head = [clean(r) for r in re.findall(r"<thead>.*?</thead>", t, re.S)]
        rows = [clean(r) for r in re.findall(r"<tr[ >].*?</tr>", re.sub(r"<thead>.*?</thead>", "", t, flags=re.S), re.S)]
        foot = clean(" ".join(re.findall(r"<table-wrap-foot>.*?</table-wrap-foot>", t, re.S)))[:300]
        out.append(("table", cap, head, rows, foot))
    x2 = re.sub(r"<table-wrap[ >].*?</table-wrap>", " ", x, flags=re.S)
    for p in re.findall(r"<p[ >].*?</p>|<caption>.*?</caption>", x2, re.S):
        out.append(("p", clean(p)))
    return out


def main():
    u = json.load(open(os.path.join(W, 'units.json')))
    units = u['units_list']
    lo, hi = int(sys.argv[2]), int(sys.argv[3])
    for si, idx in enumerate(u['sample_index'][lo:hi], start=lo):
        x = units[idx]
        num = re.match(r'[\d,]+(?:\.\d+)?', x['printed']).group(0)
        rx = re.compile(r'(?<![\d.,])' + re.escape(num) + r'(?![\d])(?!\.\d)')
        print(f"\n=== S{si} {x['uid']} printed={x['printed']}\nABS: {x['sentence'][:500]}")
        xml = open(os.path.join(W, 'pmc', x['pmcid'] + '.xml')).read()
        shown = 0
        for b in blocks(xml):
            if shown >= 6:
                break
            if b[0] == 'p' and rx.search(b[1]):
                m = rx.search(b[1]); s = max(0, m.start() - 260)
                print(f"  P: …{b[1][s:m.end() + 160]}…"); shown += 1
            elif b[0] == 'table':
                hits = [r for r in b[3] if rx.search(r)]
                if hits:
                    print(f"  T: {b[1][:200]}\n     HEAD: {' // '.join(h[:300] for h in b[2])}")
                    for r in hits[:3]:
                        print(f"     ROW: {r[:300]}")
                    if b[4]:
                        print(f"     FOOT: {b[4][:200]}")
                    shown += 1
        if shown == 0:
            print("  (printed number string not found in full text)")


if __name__ == "__main__":
    main()
