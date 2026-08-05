#!/usr/bin/env python3
"""score_day2.py — score the three pre-registered predictions of PREREGISTRATION-DAY2.md.

WRITTEN AND COMMITTED BEFORE ANY DAY-2 ARTICLE FILE EXISTED. It does no measuring of its
own: it reads the outputs of the two committed measurement scripts (run unmodified) for
day 1 and day 2 and applies the thresholds fixed in the pre-registration. Offline,
deterministic, standard library only.

Run from this directory (drafts/2026-08-04-echo-below-the-line/day2) after:
    python3 ../scripts/measure_echo.py            # writes results/
    python3 ../scripts/decompose_drop.py          # writes results/drop_decomposition.json
and after the same two scripts have been re-run over day 1 under identical flags
(day-1 outputs for the comparison are expected at ../day1-rerun/results/; if that
directory is absent the script falls back to the committed ../results/ and SAYS SO,
because day 1's committed decomposition was produced under the pre-fix ASCII-only
normalisation and is therefore not strictly like-for-like).

Exit code 0 always: scoring a refutation is not an error.
"""
import json, os, sys

MIN_POOL = 150            # Band 0 floor, pre-registered
P1_SLACK_PP = 1.0         # B(0.9) <= A + 1.0 pp
P2_MIN_DROP_PP = 10.0     # A - P >= 10.0 pp
P3_MIN_TOP4_SHARE = 0.60  # top-4 groups >= 60% of the drop


def load(path):
    with open(path) as fh:
        return json.load(fh)


def summarise(summary, decomp):
    """Pull the four numbers the predictions are about out of a run's outputs."""
    a = summary['rule_a_result']['echo_index'] * 100.0
    b09 = next(r['echo_index'] for r in summary['rule_b_sweep'] if abs(r['threshold'] - 0.9) < 1e-9) * 100.0
    p = summary['rule_c_result']['echo_index_a_collapsed_by_publisher'] * 100.0
    drop = summary['rule_c_result']['drop_pp_original_minus_collapsed']
    total_drop = decomp['total_drop_pp']
    top4 = decomp['share_of_drop_from_top_four_groups_pp']
    return {
        'pool': summary['pool']['pool_size_after_url_dedup'],
        'domains': summary['pool']['distinct_domains'],
        'publisher_groups': summary['rule_c_result']['distinct_publisher_groups_after_collapse'],
        'A_pp': a, 'B09_pp': b09, 'P_pp': p, 'drop_pp': drop,
        'decomp_total_drop_pp': total_drop,
        'decomp_top4_pp': top4,
        'top4_share': (top4 / total_drop) if total_drop else float('nan'),
        'groups_causing_loss': decomp['number_of_publisher_groups_causing_any_loss'],
        'normalisation': decomp.get('normalisation'),
    }


def main():
    d2 = summarise(load('results/summary.json'), load('results/drop_decomposition.json'))

    rerun = '../day1-rerun'
    if os.path.isdir(rerun):
        d1 = summarise(load(f'{rerun}/results/summary.json'), load(f'{rerun}/results/drop_decomposition.json'))
        d1_src = 'day 1 re-run under identical flags'
    else:
        d1 = summarise(load('../results/summary.json'), load('../results/drop_decomposition.json'))
        d1_src = ('day 1 AS COMMITTED IN SESSION 89 — NOT like-for-like: its decomposition was '
                  'produced under the pre-fix ASCII-only normalisation')

    print('=' * 78)
    print('PRE-REGISTERED SCORING — PREREGISTRATION-DAY2.md, politics beat, primary comparison')
    print('=' * 78)
    for label, d, src in (('DAY 1', d1, d1_src), ('DAY 2', d2, 'this session')):
        print(f'\n{label}  ({src})')
        print(f'  pool after URL dedup      {d["pool"]}')
        print(f'  distinct domains          {d["domains"]}   -> publisher groups {d["publisher_groups"]}')
        print(f'  A  (published rule)       {d["A_pp"]:.2f} %')
        print(f'  B(0.9) (near-duplicate)   {d["B09_pp"]:.2f} %      gap B-A = {d["B09_pp"]-d["A_pp"]:+.2f} pp')
        print(f'  P  (publisher units)      {d["P_pp"]:.2f} %       drop A-P = {d["drop_pp"]:.2f} pp')
        print(f'  decomposition             {d["groups_causing_loss"]} groups cause any loss; '
              f'top four = {d["decomp_top4_pp"]:.2f} of {d["decomp_total_drop_pp"]:.2f} pp '
              f'= {d["top4_share"]*100:.1f} %   [{d["normalisation"]}]')

    print('\n' + '-' * 78)
    if d2['pool'] < MIN_POOL:
        print(f'BAND 0 — pool is {d2["pool"]} < {MIN_POOL} usable records. NO PREDICTION IS SCORED.')
        print('The session reports the attempt and the refusal; the predictions stay open.')
        return

    p1 = d2['B09_pp'] <= d2['A_pp'] + P1_SLACK_PP
    p2 = d2['drop_pp'] >= P2_MIN_DROP_PP
    p3 = d2['top4_share'] >= P3_MIN_TOP4_SHARE
    print(f'P1  B(0.9) <= A + {P1_SLACK_PP} pp        '
          f'{d2["B09_pp"]:.2f} <= {d2["A_pp"] + P1_SLACK_PP:.2f}   ->  {"HOLDS" if p1 else "REFUTED"}')
    print(f'P2  A - P  >= {P2_MIN_DROP_PP} pp           '
          f'{d2["drop_pp"]:.2f} >= {P2_MIN_DROP_PP}        ->  {"HOLDS" if p2 else "REFUTED"}')
    print(f'P3  top-4 share >= {P3_MIN_TOP4_SHARE:.0%}         '
          f'{d2["top4_share"]:.1%} >= {P3_MIN_TOP4_SHARE:.0%}      ->  {"HOLDS" if p3 else "REFUTED"}')

    print('-' * 78)
    if not p1:
        band = 'BAND 4 — P1 refuted: a title-level paraphrase gap appears on day 2. Day 1\'s null was day-specific.'
    elif not p2:
        band = ('BAND 3 — P2 refuted: the publisher-unit drop did not reproduce. The finding this concept '
                'rests on failed its first out-of-sample test.')
    elif not p3:
        band = 'BAND 2 — P1 and P2 hold, P3 fails: the effect reproduces, its concentration does not.'
    else:
        band = 'BAND 1 — P1, P2 and P3 all hold: the day-1 result is not a one-day artifact at n = 2.'
    print(band)
    if not p2 and d2['P_pp'] >= d2['A_pp']:
        print('  ... and catastrophically: P >= A. The direction of the effect did not reproduce either.')


if __name__ == '__main__':
    main()
