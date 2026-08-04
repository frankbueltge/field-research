"""
scripts/render_summary.py — writes results/summary.md: a plain table dump of every
series, every z, every label, every branch verdict, the marker channel, the MDE table
and both power curves, read from results/envelope.json and results/sensitivity.json
(both already written by envelope_units.py / sensitivity_units.py). No prose
interpretation, no headline claims -- purely so a verifier can check any later text
against these numbers. Full, unrounded values live in the JSON; this file rounds for
readability only.
"""
import json
import os

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DRAFT_DIR = os.path.dirname(_SCRIPT_DIR)
ENVELOPE_PATH = os.path.join(_DRAFT_DIR, "results", "envelope.json")
SENSITIVITY_PATH = os.path.join(_DRAFT_DIR, "results", "sensitivity.json")
OUT_PATH = os.path.join(_DRAFT_DIR, "results", "summary.md")


def f(v, nd=4):
    if v is None:
        return ""
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, (int,)):
        return str(v)
    return f"{v:.{nd}f}"


def render_metric_table(lines, name, report):
    fit = report["fit"]
    lines.append(f"#### {name}  (direction={report['direction']}, anomaly_rule={report['anomaly_rule']})")
    lines.append("")
    lines.append(
        f"n_fit={fit['n_fit']}  df={fit['df']}  t_crit={f(fit['t_crit'],6)}  "
        f"fit_range={fit['fit_range']}  degree={fit['degree']}  s={f(fit['s'],6)}"
    )
    lines.append("")
    lines.append(
        f"ref_decidable={report['ref_decidable']}  ext_decidable={report['ext_decidable']}  "
        f"A_ref={report['a_ref']}  A_ext={report['a_ext']}  "
        f"Delta_ref={f(report['delta_ref'])}  Delta_ext={f(report['delta_ext'])}  "
        f"delta={f(report['delta'])}  label={report['label']}  sub_label={report['sub_label']}"
    )
    lines.append("")
    lines.append("| index | value | yhat | se | z_raw | z | out_of_band |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in report["rows"]:
        lines.append(
            f"| {r['index']} | {f(r['value'],6)} | {f(r['yhat'],6)} | {f(r['se'],6)} | "
            f"{f(r['z_raw'],4)} | {f(r['z'],4)} | {r['out_of_band']} |"
        )
    lines.append("")


def render_verdict(lines, verdict):
    lines.append(
        f"**headline_state={verdict['headline_state']}**  step={verdict['step']} ({verdict['step_name']})  "
        f"kill_condition_met={verdict['kill_condition_met']}"
    )
    lines.append("")
    lines.append(f"verdict text: {verdict['verdict']}")
    lines.append("")
    # Dated correction, 2026-08-04 (session 87): where a verdict carries the notice,
    # the notice is printed immediately beneath it, not once at the top of the file.
    # A reader who lands on line 1780 of this dump must meet it there.
    if verdict.get("verdict_status"):
        lines.append(f"> **{verdict['verdict_status']}**")
        lines.append("")
    lines.append(f"denominator={verdict.get('denominator')}  single_channel={verdict.get('single_channel')}")
    lines.append(f"headline_bucket_counts={verdict.get('headline_bucket_counts')}")
    lines.append(f"headline_label_counts={verdict.get('headline_label_counts')}")
    lines.append("")


def render_branch(lines, title, note, branch):
    lines.append(f"### {title}")
    lines.append("")
    if note:
        lines.append(note)
        lines.append("")
    for name, report in branch["metrics"].items():
        render_metric_table(lines, name, report)
    lines.append(f"**Branch verdict** (disagrees_with_decisional_headline={branch['disagrees_with_decisional_headline']}):")
    lines.append("")
    render_verdict(lines, branch["verdict"])


def render_envelope(lines, env):
    lines.append("## 1. Windows and constants")
    lines.append("")
    lines.append(f"envelope={env['windows']['envelope']}  reference={env['windows']['reference']}  "
                  f"extension={env['windows']['extension']}  combined_v2={env['windows']['combined_v2']}")
    lines.append(f"delta_threshold={env['constants']['delta_threshold']}  "
                  f"min_computable_for_decidable={env['constants']['min_computable_for_decidable']}")
    lines.append("")

    lines.append("## 2. Decisional run (all-units linear prefix600 fit, sim_trailing)")
    lines.append("")
    lines.append(env["decisional"]["note"])
    lines.append("")
    for name, report in env["decisional"]["metrics"].items():
        render_metric_table(lines, name, report)
    lines.append("**§7 verdict (THE decisional headline):**")
    lines.append("")
    render_verdict(lines, env["decisional"]["verdict"])

    lines.append("### Similarity out-of-band top-contributor concentration (§3(d) partial discriminator)")
    lines.append("")
    contribs = env["decisional"]["similarity_top_contributor_concentration_partial_discriminator"]
    if not contribs:
        lines.append("(no out-of-band similarity units in the decisional run)")
        lines.append("")
    else:
        lines.append("| index | z | window_indices | top_contributors (token, contrib, share) |")
        lines.append("|---|---|---|---|")
        for c in contribs:
            lines.append(f"| {c['index']} | {f(c['z'])} | {c['window_indices']} | {c['top_contributors']} |")
        lines.append("")

    lines.append("## 3. Marker channel (§8) -- never in §7's counts")
    lines.append("")
    marker = env["marker_channel"]
    fit = marker["fit"]
    lines.append(f"n_fit={fit['n_fit']}  df={fit['df']}  t_crit={f(fit['t_crit'],6)}  "
                  f"fit_range={fit['fit_range']}  slope={f(fit['slope'],6)}  intercept={f(fit['intercept'],6)}")
    lines.append("")
    cw = marker["combined_window_v2_48_73"]
    lines.append(f"Combined v2 window (48-73): decidable={cw['decidable']}  anomaly(excess-direction)={cw['anomaly']}  "
                  f"mean_z={f(cw['delta_mean_z'])}")
    lines.append("")
    lv = marker["levels"]
    lines.append(f"levels (marker per 1000, prefix600): envelope_era_mean={f(lv['envelope_era_mean'])}  "
                  f"envelope_era_range={[f(x) for x in lv['envelope_era_range']] if lv['envelope_era_range'] else None}  "
                  f"reference_mean={f(lv['reference_mean'])}  extension_mean={f(lv['extension_mean'])}  "
                  f"extension_range={[f(x) for x in lv['extension_range']] if lv['extension_range'] else None}")
    lines.append("")
    lines.append("Parent instrument's published levels (per 1000, declared-invalid cross-genre comparison, §8): "
                  f"{marker['cross_genre_comparison_declared_invalid']['parent_instrument_published_levels_per_1000']}")
    lines.append("")
    lines.append("| index | value(prefix600) | yhat | z_raw | out_of_band(excess) | context(whole_unit) |")
    lines.append("|---|---|---|---|---|---|")
    context_by_idx = {r["index"]: r["value"] for r in marker["context_whole_cell_rate"]["rows"]}
    for r in marker["rows"]:
        lines.append(f"| {r['index']} | {f(r['value'])} | {f(r['yhat'])} | {f(r['z_raw'],4)} | {r['out_of_band']} | "
                      f"{f(context_by_idx.get(r['index']))} |")
    lines.append("")

    lines.append("## 4. Zipf-tail diagnostic (§3, transferability -- no verdict)")
    lines.append("")
    zd = env["zipf_tail_diagnostic"]
    lines.append(f"window={zd['window']}  n_prefix600_computable={zd['n_prefix600_computable']}  "
                  f"n_exactly_zero={zd['n_exactly_zero']}  n_non_computable={zd['n_non_computable']}  "
                  f"n_degenerate_total={zd['n_degenerate_total']}")
    lines.append("")
    lines.append("| index | prefix600_computable | zipf_slope | zipf_non_computable |")
    lines.append("|---|---|---|---|")
    for v in zd["values"]:
        lines.append(f"| {v['index']} | {v['prefix600_computable']} | {f(v['zipf_slope'],6)} | {v['zipf_non_computable']} |")
    lines.append("")

    lines.append("## 5. Declared non-decisional branches")
    lines.append("")
    branches = env["branches"]
    render_branch(lines, "5a. Quadratic curvature check", branches["quadratic_curvature"]["note"], branches["quadratic_curvature"])
    render_branch(lines, "5b. Founding-transient (units 10-47)", branches["founding_transient_10_47"]["note"], branches["founding_transient_10_47"])
    render_branch(lines, "5c. Prop40 fixed-proportion companion series", branches["prop40_fixed_proportion"]["note"], branches["prop40_fixed_proportion"])
    render_branch(lines, "5d. Sim_content companion series", branches["sim_content_companion"]["note"], branches["sim_content_companion"])
    render_branch(lines, "5e. Sim_block companion series", branches["sim_block_companion"]["note"], branches["sim_block_companion"])

    lines.append(f"**soft_downgrade_unresolved (linear vs quadratic, decisional roster): {env['soft_downgrade_unresolved']}**")
    lines.append("")


def render_sensitivity(lines, sens):
    lines.append("## 6. Sensitivity and power (§9)")
    lines.append("")
    lines.append(f"p_grid={sens['p_grid']}")
    lines.append(f"recipes={sens['recipes']}")
    lines.append("")
    lines.append(sens["injection_scope_note"])
    lines.append("")

    lines.append("### 6.1 MDE table (§9.1)")
    lines.append("")
    for name, m in sens["mde"].items():
        lines.append(f"**{name}** (direction={m['direction']}, t_crit={f(m['t_crit'],6)}, n_fit={m['n_fit']}, df={m['df']}): "
                      f"range=[{f(m['range'][0])}, {f(m['range'][1])}]")
        lines.append("")
        lines.append("| index | se | mde_magnitude | required_direction | required_raw_delta |")
        lines.append("|---|---|---|---|---|")
        for row in m["per_unit"]:
            lines.append(f"| {row['index']} | {f(row['se'],6)} | {f(row['mde_magnitude'],6)} | "
                          f"{row['required_direction']} | {f(row['required_raw_delta'],6)} |")
        lines.append("")

    lines.append("### 6.2 Power curves, per recipe")
    lines.append("")
    for recipe in ("A", "B"):
        lines.append(f"#### Recipe {recipe} ({sens['recipes'][recipe]['donor_rank_range']}, "
                      f"{sens['recipes'][recipe]['donor_count']} donors)")
        lines.append("")
        lines.append("| p | battery_step | headline_state | mtld a_ext/oob | hapax_share a_ext/oob | "
                      "top50_mass a_ext/oob | similarity a_ext/oob |")
        lines.append("|---|---|---|---|---|---|---|")
        for p in sens["p_grid"]:
            cell = sens["power_curve"][recipe][str(p)] if str(p) in sens["power_curve"][recipe] else sens["power_curve"][recipe][p]
            v = cell["verdict"]
            pm = cell["per_metric_out_of_band"]
            row = f"| {p} | {v['step']} | {v['headline_state']} |"
            for name in ("mtld", "hapax_share", "top50_mass", "similarity"):
                row += f" {pm[name]['a_ext']}/{pm[name]['any_out_of_band']} |"
            lines.append(row)
        lines.append("")
        fs = sens["firing_summary"][recipe]
        lines.append(f"battery_fires_at_p={fs['battery_fires_at_p']}")
        lines.append(f"per_metric_first_out_of_band_p={fs['per_metric_first_out_of_band_p']}")
        lines.append(f"per_metric_first_own_anomaly_p={fs['per_metric_first_own_anomaly_p']}")
        lines.append("")

    lines.append(f"**structurally_blind_metrics = {sens['structurally_blind_metrics']}**")
    lines.append("")
    lines.append(f"**informativeness label = {sens['informativeness']['label']}** (bar_p={sens['informativeness']['bar_p']})")
    lines.append("")


def main():
    with open(ENVELOPE_PATH, "r", encoding="utf-8") as fh:
        env = json.load(fh)
    with open(SENSITIVITY_PATH, "r", encoding="utf-8") as fh:
        sens = json.load(fh)

    lines = []
    lines.append("# Results summary — plain table dump")
    lines.append("")
    lines.append(
        "Machine-generated by `scripts/render_summary.py` from `results/envelope.json` and "
        "`results/sensitivity.json`. No prose interpretation, no headline claims: every number "
        "here is traceable to those two JSON files (full, unrounded precision there; values "
        "below are rounded for readability only)."
    )
    lines.append("")
    # Dated correction, 2026-08-04 (session 87). Read from envelope.json, not
    # written here: the notice is defined once, in scripts/envelope_units.py.
    lines.append(f"> **{env['_void_notice']}**")
    lines.append("")
    render_envelope(lines, env)
    render_sensitivity(lines, sens)

    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
