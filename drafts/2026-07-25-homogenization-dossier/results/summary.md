# Homogenization Dossier — envelope results

Generated: 2026-07-25T05:15:43Z

Both decision strata NO SIGNAL: **True**

## cs.CL

| metric | label | sub | decidable(ref/ext) | A_ref | A_ext | Δ_ref | Δ_ext | δ |
|---|---|---|---|---|---|---|---|---|
| mtld | NO-ANOMALY |  | True/True | False | False | 2.089 | 11.749 | 9.659 |
| hapax_share | NO-ANOMALY |  | True/True | False | False | -0.203 | 1.024 | 1.227 |
| zipf_slope | NO-ANOMALY |  | True/True | False | False | 1.893 | 2.722 | 0.829 |
| similarity | NO-ANOMALY |  | True/True | False | False | -0.800 | -1.782 | -0.982 |

Marker channel (decisional, pool-based, excess direction): A_ref=True, A_ext=True, A_validity(2023H1-2026H1)=True. Whole-cell rate reported as context only in the JSON (never fed to an envelope).

Verdict: **NO SIGNAL BEYOND ORDINARY DRIFT** (headline_state=NO SIGNAL, step=2, soft_downgrade_unresolved=False)

## cs.CV

| metric | label | sub | decidable(ref/ext) | A_ref | A_ext | Δ_ref | Δ_ext | δ |
|---|---|---|---|---|---|---|---|---|
| mtld | NO-ANOMALY |  | True/True | False | False | 4.212 | 18.044 | 13.832 |
| hapax_share | NO-ANOMALY |  | True/True | False | False | -0.645 | -0.485 | 0.160 |
| zipf_slope | NO-ANOMALY |  | True/True | False | False | 0.636 | 0.099 | -0.538 |
| similarity | NO-ANOMALY |  | True/True | False | False | -0.186 | -0.528 | -0.342 |

Marker channel (decisional, pool-based, excess direction): A_ref=True, A_ext=True, A_validity(2023H1-2026H1)=True. Whole-cell rate reported as context only in the JSON (never fed to an envelope).

Verdict: **NO SIGNAL BEYOND ORDINARY DRIFT** (headline_state=NO SIGNAL, step=2, soft_downgrade_unresolved=False)

## math.NT

| metric | label | sub | decidable(ref/ext) | A_ref | A_ext | Δ_ref | Δ_ext | δ |
|---|---|---|---|---|---|---|---|---|
| mtld | NO-ANOMALY |  | True/True | False | False | -0.169 | 2.966 | 3.135 |
| hapax_share | NO-ANOMALY |  | True/True | False | False | -0.341 | 0.481 | 0.822 |
| zipf_slope | NO-ANOMALY |  | True/True | False | False | -0.078 | 0.231 | 0.309 |
| similarity | NO-ANOMALY |  | True/True | False | False | 0.280 | -0.815 | -1.095 |

Marker channel (decisional, pool-based, excess direction): A_ref=False, A_ext=False, A_validity(2023H1-2026H1)=False. Whole-cell rate reported as context only in the JSON (never fed to an envelope).

## Control

math.NT marker-channel valid: **True** — control_clear: True — ext-anomalous margin metrics: [] (of 4 decidable)

## Familywise false-positive arithmetic (disclosed, static)

- P(one metric A_ext) ≈ 0.00123
- P(>=2 of 4, independent) ≈ 9e-06
- P(>=2 of 4, totally correlated) ≈ 0.0012
- P(across two decision strata, correlated) ≈ 0.0025

Sensitivity: each stratum's headline_state is computed under BOTH the linear and quadratic envelope (§4 soft-downgrade rule); disagreement is flagged 'soft_downgrade_unresolved' above and both headlines ship in the JSON.
