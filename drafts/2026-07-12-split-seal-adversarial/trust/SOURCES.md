# Trust-list sources — round 3 (the trust-list re-validation gate)

Real, published C2PA trust configurations, fetched and pinned for the round-3 test
(`tools/run_layer3_trust.py`). No fabrication: every file is a verbatim copy of a publicly
maintained list, with its source URL, fetch date, and sha256 below. Re-fetch and re-pin to verify.

**Fetched:** 2026-07-13 (collective session 36).

| file | sha256 | source (raw) | what it is |
|---|---|---|---|
| `C2PA-TRUST-LIST.pem` | `b1f399a7235f188a22f3db97992f1cc1417517664600335f9d105a6a7cdb46c1` | `raw.githubusercontent.com/c2pa-org/conformance-public/main/trust-list/C2PA-TRUST-LIST.pem` | The **current official C2PA Trust List** — CA trust anchors certified under the C2PA Conformance Program (launched mid-2025). The Adobe/CAI Content Authenticity Inspect tool uses this list. 28 CA certs. |
| `C2PA-TSA-TRUST-LIST.pem` | `76788c4c36644ee24674f6d63e9ee6f0186c3e25e39ea80da67d1b6f35dbea62` | `raw.githubusercontent.com/c2pa-org/conformance-public/main/trust-list/C2PA-TSA-TRUST-LIST.pem` | The official C2PA **TSA** (time-stamp authority) trust list. 21 certs. Not load-bearing for this round (the specimens validate/fail on signer chain, not timestamp trust); committed for full disclosure. |
| `ITL-anchors.pem` | `db57e50b9bd4e4c786cbb91f38fd85e2af6a9d5412438a8cddcc42688df07ae5` | `raw.githubusercontent.com/contentauth/verify-site/main/static/trust/anchors.pem` | The **Interim Trust List (ITL)** root/intermediate anchors — the legacy "known-certificate list" the C2PA **Verify** site (contentcredentials.org/verify) uses. Frozen January 2026; no new certs added. 27 certs, incl. Truepic, Microsoft, Adobe, Nikon, Sony, Leica roots. |
| `ITL-allowed.pem` | `dfe328032e56f98b83f27f48a3642314124568b9f71ff471dffabf9b307c65d5` | `raw.githubusercontent.com/contentauth/verify-site/main/static/trust/allowed.pem` | The ITL **end-entity** allowed list (signer certs trusted directly). 115 certs. Paired with `ITL-anchors.pem` to form the full ITL configuration Verify applies. |

## Why two lists, and why both are "standard"

The C2PA trust layer is mid-migration. The **Interim Trust List** was the ecosystem's de-facto
known-certificate list through the 2022–2025 window these specimens were produced in, and is what
the reference **Verify** site still applies. The **official C2PA Trust List** (conformance program)
is the designated forward standard, but as of early 2026 it is sparse — publicly, DigiCert and
SSL.com were among the first CAs to enroll (September 2025). Testing the specimens against **both**,
and disclosing which discriminates, is the non-cherry-picked way to answer the pre-registered
question; picking one silently would be exactly the kind of trust-list shopping the pre-registration
guards against. The pre-registration's own wording invites this: "a standard C2PA trust
configuration (the c2pa library's own bundled trust anchors and/or the published C2PA
known-certificate list)".

## Sourcing references (retrieved 2026-07-13)

- Official C2PA Trust List and its role in the Conformance Program: `c2pa.org/conformance`;
  `github.com/c2pa-org/conformance-public` (the trust-list repository).
- c2patool / c2pa-rs trust configuration and the distinction between the official trust list and the
  interim (legacy, frozen) list: `github.com/contentauth/c2pa-rs/blob/main/cli/docs/usage.md`.
- The ITL as the list the Verify site uses, and its January-2026 freeze:
  `github.com/contentauth/c2pa-conformance-tool` (README).
