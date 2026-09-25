#!/usr/bin/env python3
"""Units and sample, per PREREGISTRATION §2. Session 170, 2026-09-25.
Imports 09-23's rule unchanged; converts JATS to plain text (abstract EXCLUDED) for the reading."""
import html, json, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'a-number-you-cannot-check'))
import handover  # noqa: E402

W = sys.argv[1]
SEED = 20260925
SAMPLE = 120


def jats_text(xml):
    """Body, tables (one row per line, cells joined by ' | '), captions, footnotes. No abstract,
    no front matter, no reference list."""
    x = re.sub(r"<front>.*?</front>", " ", xml, flags=re.S)
    x = re.sub(r"<ref-list[ >].*?</ref-list>", " ", x, flags=re.S)
    x = re.sub(r"<abstract[ >].*?</abstract>", " ", x, flags=re.S)
    x = re.sub(r"</t[dh]>", " | ", x)
    x = re.sub(r"</tr>|</p>|</title>|<break/>|</caption>|</label>", "\n", x)
    x = re.sub(r"<[^>]+>", "", x)
    x = html.unescape(x)
    x = x.replace(' ', ' ').replace(' ', ' ').replace(' ', ' ')
    return "\n".join(l.strip() for l in x.split("\n") if l.strip())


def main():
    abstracts = json.load(open(os.path.join(W, 'abstracts.json')))
    man = [r for r in json.load(open(os.path.join(W, 'fulltext-manifest.json')))['rows'] if r['has_body']]
    os.makedirs(os.path.join(W, 'txt'), exist_ok=True)
    units = []
    for r in man:
        open(os.path.join(W, 'txt', r['id'] + '.txt'), 'w').write(
            jats_text(open(os.path.join(W, 'pmc', r['pmcid'] + '.xml')).read()))
        for j, tok in enumerate(handover.analyse(abstracts[r['id']], r['id'])):
            if tok['verdict'] == 'not_recomputable':
                units.append({"uid": f"{r['id']}#{j}", "doc": r['id'], "pmcid": r['pmcid'],
                              "printed": tok['text'], "value": tok['value'],
                              "decimals": tok['decimals'], "sentence": tok['sentence']})
    rnd = random.Random(SEED)
    sample = sorted(rnd.sample(range(len(units)), min(SAMPLE, len(units))))
    json.dump({"papers_with_body": len(man),
               "papers_with_a_unit": len({u['doc'] for u in units}),
               "units": len(units), "seed": SEED, "sample_index": sample,
               "units_list": units}, open(os.path.join(W, 'units.json'), 'w'), indent=1, ensure_ascii=False)
    print(len(man), "papers;", len({u['doc'] for u in units}), "with a unit;", len(units), "units;",
          len(sample), "sampled from", len({units[i]['doc'] for i in sample}), "papers")


if __name__ == "__main__":
    main()
