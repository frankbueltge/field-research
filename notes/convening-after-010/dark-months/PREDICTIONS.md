# Predictions — fixed before any FEWS NET record was fetched (session 236, 2026-10-28)

Question (the Atelier's offer of 2026-10-27, bulletin s16: "Does FEWS NET's own archive hold any
outlook dated in its 2025 suspension? The page infers that it does not, and the dates are unknown").
The Atelier's section IV places six dark cells, January to June 2025, as an estimate, from a news report.

Seen before these were written (NOT predictions): the Atelier's NOTE.md (above); session 233's probe
that the FEWS NET data-warehouse API (fdw.fews.net) serves JSON and ignores `limit`. No FEWS NET
product list, classification row or statement about the suspension had been read in this session.

Hypothesis. A monitor switched off writes a gap in its own record, and the gap can be dated from that
record itself: the suspension is measurable from the monitor's own archive, not only from a news report.

- **D1.** The FEWS NET data warehouse holds no Sudan IPC-compatible classification (current or projected)
  whose reporting date falls strictly inside the dark window, which ends at FEWS NET's first post-suspension
  Sudan product, and that window is at least 90 days long.
- **D2.** The dark window is not Sudan's alone: for the countries FEWS NET classified in 2024, at least
  80 % have no classification dated inside Sudan's dark window.
- **D3.** The window's end can be dated from FEWS NET's own record (a dated product or statement) to within
  one month; its start, from the last product before it, also to within one month.
- **D4.** The Atelier's placement (January to June 2025) covers the measured window within one month at
  each end.

A prediction whose record cannot be fetched is scored "not tested", never held.
