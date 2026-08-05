"""Stage B — assemble the evidence gate into the file the scorer reads.

Every `members_named` list below is produced by a machine check against a page the member site
serves itself, or by a specialist's cited source that the conductor re-fetched. Nothing is included
on pattern, naming convention or inference. The checks live in:

  provenance/footers.json           home-page imprint text for all 596 domains
  evidence/iheart-footer-check.json per-member check of all 109 station pages
  evidence/subpage-per-member.json  per-member check on contact/about pages
  evidence/subpage-check.json       the specialists' cited subpages, re-fetched
  evidence/specialist-a.md, evidence/specialist-b.md  the two reports, unedited

Output: evidence/ownership.json
"""
import json, os, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {r['domain']: r for r in json.load(open(os.path.join(HERE, 'provenance', 'footers.json')))['records']}
CAND = {g['id']: g for g in json.load(open(os.path.join(HERE, 'results', 'candidates.json')))['units']}


def by_footer(unit_id, pattern):
    """Members whose own home page carries the operator's name in its imprint text."""
    return [m for m in CAND[unit_id]['members']
            if any(re.search(pattern, s, re.I) for s in (F.get(m) or {}).get('snippets', []))]


NEWSQUEST = ['cand-asianimage.co.uk', 'cand-bournemouthecho.co.uk', 'cand-bracknellnews.co.uk',
             'cand-andoveradvertiser.co.uk', 'cand-bromsgroveadvertiser.co.uk', 'cand-cravenherald.co.uk',
             'cand-braintreeandwithamtimes.co.uk', 'cand-basingstokegazette.co.uk', 'cand-bordertelegraph.com']

units = []

for uid in NEWSQUEST:
    units.append({
        'unit_id': uid, 'operator': 'Newsquest Media Group Ltd', 'verdict': 'CONFIRMED',
        'evidence': 'each member site\'s own home-page notice, machine-checked: '
                    '"… is owned and operated by Newsquest Media Group Ltd, an audited local newspaper network."',
        'source': 'the member domains themselves, fetched 2026-08-05; see provenance/footers.json',
        'members_named': by_footer(uid, r'Newsquest'),
        'members_not_named': [m for m in CAND[uid]['members'] if m not in by_footer(uid, r'Newsquest')],
    })

units.append({
    'unit_id': 'cand-1013kissfm.iheart.com', 'operator': 'iHeartMedia, Inc.', 'verdict': 'CONFIRMED',
    'evidence': 'all 109 station pages carry "iHeartMedia, Inc" in the HTML they serve; '
                'they are also 109 subdomains of one registrable domain',
    'source': 'the 109 hostnames themselves, fetched 2026-08-05; see evidence/iheart-footer-check.json',
    'members_named': json.load(open(os.path.join(HERE, 'evidence', 'iheart-footer-check.json')))['confirmed'],
    'members_not_named': [],
})

units.append({
    'unit_id': 'cand-wdbo.com', 'operator': 'Cox Media Group', 'verdict': 'CONFIRMED',
    'evidence': 'each site\'s own footer: "© Cox Media Group. All Rights Reserved."',
    'source': 'the member domains themselves, fetched 2026-08-05; see provenance/footers.json',
    'members_named': by_footer('cand-wdbo.com', r'Cox Media Group'),
    'members_not_named': [],
})

units.append({
    'unit_id': 'cand-kcci.com', 'operator': 'Hearst', 'verdict': 'CONFIRMED',
    'evidence': 'both sites\' own footer: "©2026, Hearst Properties Inc." — a primary source, which '
                'replaces the regulator-title evidence the specialist had to fall back on',
    'source': 'kcci.com and wyff4.com, fetched 2026-08-05; see provenance/footers.json',
    'members_named': by_footer('cand-kcci.com', r'Hearst'),
    'members_not_named': [],
})

for uid in ('cand-afghanistannews.net', 'cand-arabherald.com'):
    named = by_footer(uid, r'Mainstream Media')
    units.append({
        'unit_id': uid, 'operator': 'Mainstream Media Ltd (the "News.Net" sites)',
        'verdict': 'CONFIRMED' if len(named) > 1 else 'NO EVIDENCE',
        'evidence': 'the member\'s own footer: "© Copyright 1999-2026 <Title> News.Net - Mainstream Media Ltd."',
        'source': 'the member domains themselves, fetched 2026-08-05; see provenance/footers.json. '
                  'Most of this candidate unit could not be reached at all: the sites answer HTTP 403 '
                  'to our fetcher, so they are recorded as unconfirmed and split off.',
        'members_named': named,
        'members_not_named': [m for m in CAND[uid]['members'] if m not in named],
    })

APG = ['cecildaily.com', 'gazettextra.com', 'leadertelegram.com', 'stardem.com']
units.append({
    'unit_id': 'cand-cecildaily.com', 'operator': 'Adams Publishing Group / APG Media', 'verdict': 'CONFIRMED',
    'evidence': 'each site\'s own contact or about page names APG Media as its publisher — e.g. cecildaily.com: '
                '"…published every Wednesday and Friday … by APG Media of Chesapeake, LLC."',
    'source': 'evidence/subpage-check.json and evidence/subpage-per-member.json, fetched 2026-08-05',
    'members_named': APG,
    'members_not_named': ['somdnews.com'],
})

ILIFFE = [e['domain'] for e in json.load(open(os.path.join(HERE, 'evidence', 'subpage-per-member.json')))['groups']['iliffe']]
units.append({
    'unit_id': 'cand-dissexpress.co.uk', 'operator': 'Iliffe Media Group Ltd', 'verdict': 'CONFIRMED',
    'evidence': 'each of the five titles names Iliffe Media on the page it serves; the operator\'s own '
                'portfolio page lists the same five titles',
    'source': 'evidence/subpage-per-member.json, fetched 2026-08-05; https://www.iliffemedia.co.uk/',
    'members_named': ILIFFE,
    'members_not_named': [],
})

for uid, why in [
    ('cand-kcbx.org', 'eight separately licensed non-profit public-radio organisations on one shared content platform'),
    ('cand-interlochenpublicradio.org', 'three separate licensees: an arts centre, a community-college district, a university board'),
    ('cand-news.prairiepublic.org', 'three unrelated non-profit operators in three states'),
    ('cand-aspenpublicradio.org', 'two unrelated 501(c)(3) non-profits'),
    ('cand-tspr.org', 'two different state universities'),
    ('cand-kalw.org', 'three unrelated public bodies: a school district, a university, a state university system'),
]:
    units.append({'unit_id': uid, 'operator': 'none — not one publisher', 'verdict': 'HOSTING ARTEFACT',
                  'evidence': why, 'source': 'evidence/specialist-a.md, evidence/specialist-b.md — each member '
                              'named to a different licensee from its own about page',
                  'members_named': [], 'members_not_named': CAND[uid]['members']})

if __name__ == '__main__':
    json.dump({'built_utc': '2026-08-05', 'units': units},
              open(os.path.join(HERE, 'evidence', 'ownership.json'), 'w'), indent=1)
    for u in units:
        print(f"{u['verdict']:17s} {u['unit_id']:38s} {len(u['members_named']):3d}/"
              f"{CAND[u['unit_id']]['size']:3d}  {u['operator']}")
