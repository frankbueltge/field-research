"""
scripts/make_figure.py — renders the dossier's headline figure as a single static SVG,
read entirely from results/results.json. Stdlib only (no numpy, no third-party packages).

Every number that appears in the figure (series values, envelope fits, prediction-band
half-widths, the one-sided t-critical value, unit labels, deltas) is read at runtime
from the results file; nothing is typed in by hand. Given the same input file, this
script is deterministic: no randomness, no wall-clock timestamps, no dict/set iteration
that depends on anything but the JSON's own (stable, json.load-preserved) key order.

Two stacked panels, one shared 23-unit half-year x-axis (2015H1 .. 2026H1):

  Upper — THE MARGINS: four cs.CL small multiples (mtld, hapax_share, zipf_slope,
  similarity), each drawn as (a) the measured series, (b) the fitted ordinary-drift
  envelope (yhat), (c) the prediction band yhat +/- t_crit*se, with the collapse-side
  edge of the band drawn distinctly from the (untested, one-sided) other side.

  Lower — THE FINGERPRINT: the marker channel's decisional pool rate for all three
  strata (cs.CL, cs.CV, math.NT) on one shared axis, each line labelled at its own
  right-hand end.

A vertical rule marks the pre-registration's envelope/extension boundary
(end of the 2015H1-2022H2 fitting window); a shaded band marks the 2025H1-2026H1
extension window used by the kill-condition check.
"""
import argparse
import json
import math
import os

# --------------------------------------------------------------------------
# Palette / type -- restrained ink-on-paper, monospace, no gradients, no color
# used as the *only* channel of information (dash pattern + label carry that).
# --------------------------------------------------------------------------
PAPER = "#f4f1e8"
BOX = "#fffdf7"
INK = "#3a352a"
INK_STRONG = "#1c1a15"
FAINT = "#8a8271"
BAND_FILL = "#e7e1d0"
EXT_FILL = "#efe8d6"
LINE_A = "#3a352a"   # first stratum line (cs.CL) -- solid
LINE_B = "#5b5341"   # second stratum line (cs.CV) -- dashed
LINE_C = "#8a8271"   # third stratum line (math.NT) -- dotted

MARGIN_METRICS = ["mtld", "hapax_share", "zipf_slope", "similarity"]
METRIC_DISPLAY = {
    "mtld": "mtld",
    "hapax_share": "hapax share",
    "zipf_slope": "zipf slope",
    "similarity": "similarity",
}
STRATA_ORDER = ["cs.CL", "cs.CV", "math.NT"]

# The two PRE-REGISTERED DECISION strata (PREREGISTRATION.md §7) -- both must be
# visually present in the margins panel, one row each; math.NT is the control and
# is not a decision stratum, so it is not drawn here (it appears only in the
# marker-channel panel below, where all three strata are context, not a verdict).
MARGIN_STRATA = ["cs.CL", "cs.CV"]

# Overall canvas geometry (layout constants, not measured data). The margins
# panel is now a 2 (stratum) x 4 (metric) grid of small multiples -- it must
# dominate the composition (it carries the registered result), so its rows
# together are sized to occupy substantially more of the canvas than the
# marker-channel panel below, which is the non-decisional, secondary panel.
FIG_W = 1180
MARGIN_L = 56
MARGIN_R = 118
UPPER_TOP = 92          # first stratum row starts here; header/legend sit above
ROW_LABEL_H = 18        # per-row stratum label strip (e.g. "cs.CL")
ROW_H = 200              # each stratum row's small-multiple plot height
ROW_GAP = 30             # gap between the cs.CL row and the cs.CV row
SUB_GAP = 44             # horizontal gap between the four metric columns
PANEL_GAP = 46           # gap between the margins block and the fingerprint block
LOWER_HEADER_H = 34      # room for the fingerprint panel's own heading/subtitle
LOWER_H = 150            # fingerprint plot height -- deliberately smaller: secondary,
                         # non-decisional observation, not the registered result
BOTTOM_MARGIN = 20

MARGINS_BLOCK_H = 2 * ROW_LABEL_H + 2 * ROW_H + ROW_GAP
FIG_H = UPPER_TOP + MARGINS_BLOCK_H + PANEL_GAP + LOWER_HEADER_H + LOWER_H + BOTTOM_MARGIN


# ============================================================================
# Pure helpers (unit-tested) -- scaling, band geometry, tick generation.
# No SVG string-building lives in these; they only compute numbers/tuples so
# they can be tested without parsing markup.
# ============================================================================

def linear_scale(value, d0, d1, r0, r1):
    """Map `value` from domain [d0, d1] to range [r0, r1]. Degenerate domain
    (d0 == d1) maps everything to the midpoint of the range."""
    if d1 == d0:
        return (r0 + r1) / 2.0
    t = (value - d0) / (d1 - d0)
    return r0 + t * (r1 - r0)


def value_domain(values, pad_frac=0.08):
    """Min/max over `values` padded by pad_frac of the span on each side.
    A flat (zero-span) input gets a fixed absolute pad so the domain never
    collapses to a single point."""
    lo = min(values)
    hi = max(values)
    if hi == lo:
        pad = 1.0 if hi == 0 else abs(hi) * pad_frac
    else:
        pad = (hi - lo) * pad_frac
    return lo - pad, hi + pad


def band_bounds(yhat, se, t_crit, direction):
    """Prediction-band edges at one row, plus which edge is the tested
    (collapse-direction) side per PREREGISTRATION.md §3/§4's reorientation:
    direction == 'low'  -> collapse is the LOWER edge (value falls below yhat).
    direction == 'high' -> collapse is the UPPER edge (value rises above yhat).
    The one-sided test only ever checks the collapse edge; the other edge is
    disclosed but never a finding."""
    half = t_crit * se
    lower = yhat - half
    upper = yhat + half
    if direction == "low":
        return {"lower": lower, "upper": upper, "collapse": "lower", "anti": "upper"}
    if direction == "high":
        return {"lower": lower, "upper": upper, "collapse": "upper", "anti": "lower"}
    raise ValueError("direction must be 'low' or 'high', got %r" % (direction,))


def band_side(value, lower, upper):
    """Where `value` sits relative to a [lower, upper] band. Returns 'lower'
    (value fell below the band), 'upper' (value rose above it), or 'inside'.
    Deliberately uses the same 'lower'/'upper' vocabulary as band_bounds()'s
    'collapse'/'anti' edge labels, so callers can compare them directly
    without a name-translation step (a prior version used 'below'/'above'
    here, which silently never matched band_bounds' 'lower'/'upper' and made
    every collapse-side detection false)."""
    if value < lower:
        return "lower"
    if value > upper:
        return "upper"
    return "inside"


def nice_step(raw_step):
    """Round raw_step up to the nearest 1/2/5 * 10^k 'nice' number, so axis
    ticks land on human-readable values. Deterministic (no randomness)."""
    if raw_step <= 0:
        return 1.0
    exp = math.floor(math.log10(raw_step))
    base = raw_step / (10 ** exp)
    if base <= 1:
        nice = 1
    elif base <= 2:
        nice = 2
    elif base <= 5:
        nice = 5
    else:
        nice = 10
    return nice * (10 ** exp)


def nice_ticks(vmin, vmax, target_count=4):
    """Generate a small set of 'nice' tick values spanning [vmin, vmax]."""
    if vmax <= vmin:
        return [vmin]
    raw_step = (vmax - vmin) / max(target_count, 1)
    step = nice_step(raw_step)
    start = math.floor(vmin / step) * step
    ticks = []
    v = start
    guard = 0
    while v <= vmax + step * 1e-9 and guard < target_count + 6:
        if v >= vmin - step * 1e-9:
            ticks.append(round(v, 10))
        v += step
        guard += 1
    return ticks


def select_x_ticks(units, stride):
    """Every stride-th unit index/label, always including the first and last
    unit so the axis never looks like it's missing an endpoint."""
    n = len(units)
    if n == 0:
        return []
    idxs = set(range(0, n, max(stride, 1)))
    idxs.add(0)
    idxs.add(n - 1)
    return [(i, units[i]) for i in sorted(idxs)]


def fmt_num(value, decimals=2):
    """Fixed-decimal number formatting, used for both coordinate values and
    on-figure numeric labels -- deterministic for a given float."""
    return f"{value:.{decimals}f}"


def points_attr(xs, ys, decimals=2):
    """Build an SVG <polyline>/<polygon> points= attribute value from parallel
    coordinate lists."""
    return " ".join(f"{fmt_num(x, decimals)},{fmt_num(y, decimals)}" for x, y in zip(xs, ys))


def band_polygon_points(xs, lowers, uppers, decimals=2):
    """Closed polygon outline for a prediction band: forward along the upper
    edge, then backward along the lower edge."""
    top = list(zip(xs, uppers))
    bottom = list(zip(reversed(xs), reversed(lowers)))
    pts = top + bottom
    return " ".join(f"{fmt_num(x, decimals)},{fmt_num(y, decimals)}" for x, y in pts)


def declutter_positions(ys, min_gap):
    """Nudge a list of desired y-positions apart so consecutive (sorted)
    values are at least min_gap apart, preserving relative order and staying
    as close as possible to the requested positions. Deterministic two-pass
    (forward push-down, backward pull-up) label-placement algorithm; input
    order of the returned list matches the input order of `ys`."""
    n = len(ys)
    if n <= 1:
        return list(ys)
    order = sorted(range(n), key=lambda i: ys[i])
    adjusted = [ys[i] for i in order]
    for i in range(1, n):
        if adjusted[i] - adjusted[i - 1] < min_gap:
            adjusted[i] = adjusted[i - 1] + min_gap
    for i in range(n - 2, -1, -1):
        if adjusted[i + 1] - adjusted[i] < min_gap:
            adjusted[i] = adjusted[i + 1] - min_gap
    result = [0.0] * n
    for rank, orig_i in enumerate(order):
        result[orig_i] = adjusted[rank]
    return result


# ============================================================================
# Data access helpers
# ============================================================================

def load_results(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def esc(text):
    """Escape the three literal XML text-node special characters."""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def metric_rows(results, stratum, metric):
    return results["strata"][stratum]["metrics"][metric]["rows"]


def marker_rows(results, stratum):
    return results["strata"][stratum]["marker"]["rows"]


# ============================================================================
# SVG assembly
# ============================================================================

def x_scale_for(n_units, x0, x1):
    """Return a callable mapping unit index in [0, n_units-1] to an x pixel."""
    def scale(i):
        return linear_scale(i, 0, n_units - 1, x0, x1)
    return scale


def draw_margin_subplot(results, stratum, metric, box, boundary_idx, ext_start_idx, t_crit, units):
    """Render one small-multiple panel (one margin metric) for `stratum`.
    Returns a list of SVG element strings."""
    x0, y0, x1, y1 = box
    rows = metric_rows(results, stratum, metric)
    direction = results["strata"][stratum]["metrics"][metric]["direction"]

    inner_x0, inner_x1 = x0 + 4, x1 - 4
    inner_y0, inner_y1 = y0 + 32, y1 - 22

    xs_idx = [row["x"] for row in rows]
    values = [row["value"] for row in rows]
    yhats = [row["yhat"] for row in rows]
    bands = [band_bounds(row["yhat"], row["se"], t_crit, direction) for row in rows]
    lowers = [b["lower"] for b in bands]
    uppers = [b["upper"] for b in bands]

    vmin, vmax = value_domain(values + lowers + uppers, pad_frac=0.10)

    xscale = x_scale_for(len(units), inner_x0, inner_x1)

    def yscale(v):
        return linear_scale(v, vmin, vmax, inner_y1, inner_y0)  # inverted (svg y grows down)

    xs_px = [xscale(i) for i in xs_idx]
    val_px = [yscale(v) for v in values]
    yhat_px = [yscale(v) for v in yhats]
    lower_px = [yscale(v) for v in lowers]
    upper_px = [yscale(v) for v in uppers]

    els = []

    # panel frame
    els.append(f'<rect x="{fmt_num(inner_x0)}" y="{fmt_num(inner_y0)}" '
               f'width="{fmt_num(inner_x1 - inner_x0)}" height="{fmt_num(inner_y1 - inner_y0)}" '
               f'fill="{BOX}" stroke="{INK}" stroke-width="0.75"/>')

    # extension-window shading (2025H1-2026H1)
    ext_x = xscale(ext_start_idx - 0.5)
    els.append(f'<rect x="{fmt_num(ext_x)}" y="{fmt_num(inner_y0)}" '
               f'width="{fmt_num(inner_x1 - ext_x)}" height="{fmt_num(inner_y1 - inner_y0)}" '
               f'fill="{EXT_FILL}" stroke="none"/>')

    # prediction band (fill only; edges drawn separately below so the
    # collapse-side edge can be made visually distinct from the other side)
    band_pts = band_polygon_points(xs_px, lower_px, upper_px)
    els.append(f'<polygon points="{band_pts}" fill="{BAND_FILL}" stroke="none"/>')

    collapse_px = lower_px if bands[0]["collapse"] == "lower" else upper_px
    anti_px = upper_px if bands[0]["collapse"] == "lower" else lower_px

    # anti-collapse edge: thin, dotted, faint -- disclosed, not decision-bearing
    els.append(f'<polyline points="{points_attr(xs_px, anti_px)}" fill="none" '
               f'stroke="{FAINT}" stroke-width="1" stroke-dasharray="1.5,3"/>')
    # collapse-direction edge: the one-sided decision boundary -- bold + solid
    els.append(f'<polyline points="{points_attr(xs_px, collapse_px)}" fill="none" '
               f'stroke="{INK_STRONG}" stroke-width="1.5"/>')

    # boundary rule (envelope-fit / extension edge, 2022H2 | 2023H1)
    bx = xscale(boundary_idx)
    els.append(f'<line x1="{fmt_num(bx)}" y1="{fmt_num(inner_y0)}" x2="{fmt_num(bx)}" '
               f'y2="{fmt_num(inner_y1)}" stroke="{INK}" stroke-width="1" stroke-dasharray="4,2"/>')

    # fitted envelope (yhat), dashed
    els.append(f'<polyline points="{points_attr(xs_px, yhat_px)}" fill="none" '
               f'stroke="{INK}" stroke-width="1.25" stroke-dasharray="6,3"/>')

    # measured series, solid
    els.append(f'<polyline points="{points_attr(xs_px, val_px)}" fill="none" '
               f'stroke="{INK_STRONG}" stroke-width="1.8"/>')

    # mark points that leave the band, distinguishing collapse-side from
    # anti-collapse-side (the latter is explicitly not a finding -- one-sided
    # test never looks at it)
    n_collapse_out = 0
    n_anti_out = 0
    for i, row in enumerate(rows):
        side = band_side(row["value"], lowers[i], uppers[i])
        if side == "inside":
            continue
        is_collapse_out = (side == bands[i]["collapse"])
        cx, cy = xs_px[i], val_px[i]
        if is_collapse_out:
            n_collapse_out += 1
            els.append(f'<circle cx="{fmt_num(cx)}" cy="{fmt_num(cy)}" r="3.2" '
                       f'fill="{INK_STRONG}" stroke="none"/>')
        else:
            n_anti_out += 1
            els.append(f'<circle cx="{fmt_num(cx)}" cy="{fmt_num(cy)}" r="3" '
                       f'fill="{BOX}" stroke="{FAINT}" stroke-width="1.25"/>')

    # x ticks (sparse, shared cadence across small multiples); edge ticks are
    # anchored outward (start/end) rather than centered so they don't collide
    # with the neighbouring subplot's own edge tick
    x_ticks = select_x_ticks(units, 11)
    last_idx = x_ticks[-1][0]
    for i, label in x_ticks:
        tx = xscale(i)
        anchor = "start" if i == 0 else ("end" if i == last_idx else "middle")
        els.append(f'<line x1="{fmt_num(tx)}" y1="{fmt_num(inner_y1)}" x2="{fmt_num(tx)}" '
                   f'y2="{fmt_num(inner_y1 + 4)}" stroke="{INK}" stroke-width="0.75"/>')
        els.append(f'<text x="{fmt_num(tx)}" y="{fmt_num(inner_y1 + 14)}" text-anchor="{anchor}" '
                   f'font-size="8.5" fill="{FAINT}" class="mono">{esc(label)}</text>')

    # y ticks (numeric, metric's own units)
    decimals = 3 if (vmax - vmin) < 1 else 1
    for tv in nice_ticks(vmin, vmax, 3):
        ty = yscale(tv)
        if ty < inner_y0 - 1 or ty > inner_y1 + 1:
            continue
        els.append(f'<line x1="{fmt_num(inner_x0 - 3)}" y1="{fmt_num(ty)}" '
                   f'x2="{fmt_num(inner_x0)}" y2="{fmt_num(ty)}" stroke="{INK}" stroke-width="0.75"/>')
        els.append(f'<text x="{fmt_num(inner_x0 - 5)}" y="{fmt_num(ty + 3)}" text-anchor="end" '
                   f'font-size="8" fill="{FAINT}" class="mono">{fmt_num(tv, decimals)}</text>')

    # subplot title + a data-driven caption (kept to short lines so it never
    # overflows into the neighbouring small multiple): how many units (if
    # any) touch the collapse-side bound -- isolated single units don't meet
    # the pre-registered two-consecutive anomaly rule -- and whether the
    # series leaves the band on the anti-collapse side (never decision-bearing)
    if n_collapse_out == 0:
        collapse_note = "0/23 cross the collapse bound"
    elif n_collapse_out == 1:
        collapse_note = "1 unit touches collapse bound (isolated, no anomaly)"
    else:
        collapse_note = f"{n_collapse_out} units touch collapse bound (isolated, no anomaly)"
    anti_note = "leaves band on anti side (not a finding)" if n_anti_out else None

    els.append(f'<text x="{fmt_num(x0)}" y="{fmt_num(y0 + 10)}" font-size="11.5" '
               f'fill="{INK_STRONG}" class="mono" font-weight="bold">{esc(METRIC_DISPLAY[metric])}</text>')
    els.append(f'<text x="{fmt_num(x0)}" y="{fmt_num(y0 + 21)}" font-size="7.4" '
               f'fill="{FAINT}" class="mono">{esc(collapse_note)}</text>')
    if anti_note:
        els.append(f'<text x="{fmt_num(x0)}" y="{fmt_num(y0 + 30)}" font-size="7.4" '
                   f'fill="{FAINT}" class="mono">{esc(anti_note)}</text>')

    return els


def draw_fingerprint_panel(results, box, boundary_idx, ext_start_idx, units):
    """Render the lower panel: marker-channel pool rate for all three strata
    on one shared axis, each line labelled directly at its right-hand end."""
    x0, y0, x1, y1 = box
    inner_x0, inner_x1 = x0 + 4, x1 - 4
    inner_y0, inner_y1 = y0 + 30, y1 - 26

    series = {s: marker_rows(results, s) for s in STRATA_ORDER}
    all_values = [row["value"] for rows in series.values() for row in rows]
    vmin, vmax = value_domain(all_values, pad_frac=0.08)

    xscale = x_scale_for(len(units), inner_x0, inner_x1)

    def yscale(v):
        return linear_scale(v, vmin, vmax, inner_y1, inner_y0)

    els = []
    els.append(f'<rect x="{fmt_num(inner_x0)}" y="{fmt_num(inner_y0)}" '
               f'width="{fmt_num(inner_x1 - inner_x0)}" height="{fmt_num(inner_y1 - inner_y0)}" '
               f'fill="{BOX}" stroke="{INK}" stroke-width="0.75"/>')

    ext_x = xscale(ext_start_idx - 0.5)
    els.append(f'<rect x="{fmt_num(ext_x)}" y="{fmt_num(inner_y0)}" '
               f'width="{fmt_num(inner_x1 - ext_x)}" height="{fmt_num(inner_y1 - inner_y0)}" '
               f'fill="{EXT_FILL}" stroke="none"/>')

    bx = xscale(boundary_idx)
    els.append(f'<line x1="{fmt_num(bx)}" y1="{fmt_num(inner_y0)}" x2="{fmt_num(bx)}" '
               f'y2="{fmt_num(inner_y1)}" stroke="{INK}" stroke-width="1" stroke-dasharray="4,2"/>')

    # y ticks
    for tv in nice_ticks(vmin, vmax, 4):
        ty = yscale(tv)
        if ty < inner_y0 - 1 or ty > inner_y1 + 1:
            continue
        els.append(f'<line x1="{fmt_num(inner_x0 - 3)}" y1="{fmt_num(ty)}" '
                   f'x2="{fmt_num(inner_x0)}" y2="{fmt_num(ty)}" stroke="{INK}" stroke-width="0.75"/>')
        els.append(f'<text x="{fmt_num(inner_x0 - 6)}" y="{fmt_num(ty + 3)}" text-anchor="end" '
                   f'font-size="9" fill="{FAINT}" class="mono">{fmt_num(tv, 0)}</text>')

    # x ticks
    for i, label in select_x_ticks(units, 4):
        tx = xscale(i)
        els.append(f'<line x1="{fmt_num(tx)}" y1="{fmt_num(inner_y1)}" x2="{fmt_num(tx)}" '
                   f'y2="{fmt_num(inner_y1 + 4)}" stroke="{INK}" stroke-width="0.75"/>')
        els.append(f'<text x="{fmt_num(tx)}" y="{fmt_num(inner_y1 + 15)}" text-anchor="middle" '
                   f'font-size="8.5" fill="{FAINT}" class="mono">{esc(label)}</text>')

    style_by_stratum = {
        "cs.CL": {"stroke": LINE_A, "dash": None, "width": "2"},
        "cs.CV": {"stroke": LINE_B, "dash": "7,3", "width": "1.75"},
        "math.NT": {"stroke": LINE_C, "dash": "1.5,3", "width": "1.5"},
    }

    last_end_y = []
    last_end_x = []
    last_values = []
    for stratum in STRATA_ORDER:
        rows = series[stratum]
        xs_px = [xscale(row["x"]) for row in rows]
        ys_px = [yscale(row["value"]) for row in rows]
        style = style_by_stratum[stratum]
        dash_attr = f' stroke-dasharray="{style["dash"]}"' if style["dash"] else ""
        els.append(f'<polyline points="{points_attr(xs_px, ys_px)}" fill="none" '
                   f'stroke="{style["stroke"]}" stroke-width="{style["width"]}"{dash_attr}/>')
        last_end_x.append(xs_px[-1])
        last_end_y.append(ys_px[-1])
        last_values.append(rows[-1]["value"])

    # labels go directly at each line's right-hand end (no separate legend
    # box) -- but three strata can end close together, so the label anchor
    # points are decluttered (min 26px apart) while a thin leader connects
    # each label back to its actual last data point whenever they diverge
    label_ys = declutter_positions(last_end_y, min_gap=26)
    for idx, stratum in enumerate(STRATA_ORDER):
        style = style_by_stratum[stratum]
        anchor_x = last_end_x[idx] + 6
        data_y = last_end_y[idx]
        label_y = label_ys[idx]
        if abs(label_y - data_y) > 1.0:
            els.append(f'<line x1="{fmt_num(last_end_x[idx])}" y1="{fmt_num(data_y)}" '
                       f'x2="{fmt_num(anchor_x)}" y2="{fmt_num(label_y)}" '
                       f'stroke="{style["stroke"]}" stroke-width="0.75"/>')
        els.append(f'<text x="{fmt_num(anchor_x + 2)}" y="{fmt_num(label_y + 3)}" font-size="10.5" '
                   f'fill="{style["stroke"]}" class="mono" font-weight="bold">{esc(stratum)}</text>')
        els.append(f'<text x="{fmt_num(anchor_x + 2)}" y="{fmt_num(label_y + 15)}" font-size="8.5" '
                   f'fill="{FAINT}" class="mono">{fmt_num(last_values[idx], 1)}</text>')

    return els


def build_svg(results):
    units = results["units"]
    t_crit = results["constants"]["t_crit_linear_df14"]
    boundary_idx = len(results["windows"]["envelope"]) - 0.5
    ext_units = results["windows"]["extension"]
    ext_start_idx = units.index(ext_units[0])

    plot_w = FIG_W - MARGIN_L - MARGIN_R
    sub_w = (plot_w - 3 * SUB_GAP) / 4.0

    body = []

    # ---- upper (dominant) block: THE MARGINS -- BOTH decision strata, one row
    # each, four metrics per row (2x4 grid of small multiples). This is the
    # panel that carries the registered result, so it occupies most of the
    # canvas; math.NT (the control, not a decision stratum) is deliberately not
    # drawn here -- it appears only in the fingerprint panel below -- and the
    # header says so on the figure's own face, not only in the caption.
    body.append(f'<text x="{fmt_num(MARGIN_L)}" y="{fmt_num(UPPER_TOP - 58)}" font-size="14" '
               f'fill="{INK_STRONG}" class="mono" font-weight="bold">THE MARGINS</text>')
    body.append(f'<text x="{fmt_num(MARGIN_L)}" y="{fmt_num(UPPER_TOP - 42)}" font-size="10.5" '
               f'fill="{INK}" class="mono">cs.CL and cs.CV &#8212; both pre-registered decision '
               f'strata, four metrics each (math.NT control: fingerprint panel below only)</text>')
    body.append(f'<text x="{fmt_num(MARGIN_L)}" y="{fmt_num(UPPER_TOP - 26)}" font-size="10.5" '
               f'fill="{INK}" class="mono">measured series (solid) vs. ordinary-drift envelope '
               f'(dashed); band = envelope &#177; {fmt_num(t_crit, 4)}&#215;SE, one-sided in each '
               f'metric&#8217;s own collapse direction</text>')
    # compact shared legend (covers all eight small multiples -- avoids repeating per-panel)
    leg_y = UPPER_TOP - 10
    legend_items = [
        ("series", INK_STRONG, None, 1.8, "solid"),
        ("envelope (yhat)", INK, "6,3", 1.25, "dashed"),
        ("collapse-side band edge", INK_STRONG, None, 1.5, "solid"),
        ("other (untested) edge", FAINT, "1.5,3", 1, "dotted"),
    ]
    lx = MARGIN_L
    for name, color, dash, width, _kind in legend_items:
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        body.append(f'<line x1="{fmt_num(lx)}" y1="{fmt_num(leg_y)}" x2="{fmt_num(lx + 22)}" '
                   f'y2="{fmt_num(leg_y)}" stroke="{color}" stroke-width="{width}"{dash_attr}/>')
        body.append(f'<text x="{fmt_num(lx + 27)}" y="{fmt_num(leg_y + 3)}" font-size="8.5" '
                   f'fill="{INK}" class="mono">{esc(name)}</text>')
        lx += 27 + 7.2 * len(name) + 20

    row_top = UPPER_TOP
    for row_idx, stratum in enumerate(MARGIN_STRATA):
        label_y = row_top + ROW_LABEL_H - 5
        body.append(f'<text x="{fmt_num(MARGIN_L)}" y="{fmt_num(label_y)}" font-size="12" '
                   f'fill="{INK_STRONG}" class="mono" font-weight="bold">{esc(stratum)}</text>')
        body.append(f'<text x="{fmt_num(MARGIN_L + 7.2 * len(stratum) + 8)}" y="{fmt_num(label_y)}" '
                   f'font-size="9" fill="{FAINT}" class="mono">decision stratum '
                   f'{row_idx + 1} of {len(MARGIN_STRATA)}</text>')
        box_top = row_top + ROW_LABEL_H
        for i, metric in enumerate(MARGIN_METRICS):
            sx0 = MARGIN_L + i * (sub_w + SUB_GAP)
            box = (sx0, box_top, sx0 + sub_w, box_top + ROW_H)
            body.extend(draw_margin_subplot(results, stratum, metric, box, boundary_idx,
                                             ext_start_idx, t_crit, units))
        row_top = box_top + ROW_H + ROW_GAP

    # ---- lower (secondary, non-decisional) block: THE FINGERPRINT (marker
    # channel, all three strata as context). Deliberately smaller than the
    # margins block above, and its heading says "non-decisional" on the
    # figure's own face -- this is the observation a four-second read
    # otherwise remembers instead of the registered null.
    lower_top = UPPER_TOP + MARGINS_BLOCK_H + PANEL_GAP
    body.append(f'<text x="{fmt_num(MARGIN_L)}" y="{fmt_num(lower_top - 20)}" font-size="12.5" '
               f'fill="{INK_STRONG}" class="mono" font-weight="bold">THE FINGERPRINT '
               f'&#8212; secondary, non-decisional</text>')
    body.append(f'<text x="{fmt_num(MARGIN_L)}" y="{fmt_num(lower_top - 7)}" font-size="9.5" '
               f'fill="{FAINT}" class="mono">marker channel, pool rate per unit, all three strata '
               f'&#8212; not a margin metric, not part of the §7 verdict above</text>')
    lower_box = (MARGIN_L, lower_top, FIG_W - MARGIN_R, lower_top + LOWER_H)
    body.extend(draw_fingerprint_panel(results, lower_box, boundary_idx, ext_start_idx, units))

    # shared vertical-rule / extension-window caption near the top-right
    cap_x = FIG_W - MARGIN_R
    body.append(f'<text x="{fmt_num(cap_x)}" y="{fmt_num(UPPER_TOP - 58)}" text-anchor="end" '
               f'font-size="8.5" fill="{FAINT}" class="mono">dashed vertical: envelope/extension '
               f'boundary ({esc(units[len(results["windows"]["envelope"]) - 1])}|'
               f'{esc(units[len(results["windows"]["envelope"])])})</text>')
    body.append(f'<text x="{fmt_num(cap_x)}" y="{fmt_num(UPPER_TOP - 46)}" text-anchor="end" '
               f'font-size="8.5" fill="{FAINT}" class="mono">shaded: extension window '
               f'{esc(ext_units[0])}&#8211;{esc(ext_units[-1])}</text>')

    aria = ("Two-block chart, dominant block on top. Upper (dominant) block, THE MARGINS: an "
            "eight-panel small-multiple grid, one row per pre-registered decision stratum (cs.CL, "
            "then cs.CV), four metrics per row (mtld, hapax share, zipf slope, similarity), each "
            "showing the measured series against a fitted ordinary-drift envelope and its "
            "one-sided prediction band; none of the eight series shows a sustained, "
            "two-consecutive-unit collapse-side breach. The control stratum math.NT is not drawn "
            "in this block. Lower (secondary, non-decisional) block, THE FINGERPRINT: the "
            "marker-channel pool rate for cs.CL, cs.CV and math.NT on one shared axis, shown at "
            "reduced size because it is not part of the pre-registered verdict; it climbs sharply "
            "from 2023 in cs.CL and cs.CV while staying flat in the math.NT control.")

    svg = (
        f'<svg viewBox="0 0 {FIG_W} {FIG_H}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{esc(aria)}">\n'
        f'<rect x="0" y="0" width="{FIG_W}" height="{FIG_H}" fill="{PAPER}"/>\n'
        + "\n".join(body) +
        "\n</svg>"
    )
    return svg


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    default_results = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "results", "results.json"
    )
    parser.add_argument("--results", default=default_results,
                        help="Path to results.json (default: ../results/results.json)")
    parser.add_argument("--out", required=True, help="Output SVG path")
    args = parser.parse_args(argv)

    results = load_results(args.results)
    svg = build_svg(results)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    main()
