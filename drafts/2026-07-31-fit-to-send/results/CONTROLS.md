# Controls — run before the census (§5)

None of the five controls below are inside the probed corpus.

- **C1 (true 404)** — `https://arxiv.org/abs/9999.99999-nonsense-fit-to-send-c1-check` -> status 404, verdict `GONE` (expected `GONE`). PASS.
- **C2 (consent/bot wall)** — `https://x.com/9_tzav` (source: works/2026-07-20-coverage-not-custody/sample.json (x-twitter stratum, object-data)) -> status 200, title 'תנועת צו 9- בשירות העם (@9_tzav) / X', verdict `OK`. OK: the wall (if any) is invisible to a plain GET at Layer 1
- **C3 (soft-404-as-200)** — `https://www.kaggle.com/dsv/18354222` -> status 200, final URL `https://www.kaggle.com/deleted-dataset-version/18354222`, title 'Kaggle Deleted Dataset Version', verdict `SOFT-GONE` (expected `SOFT-GONE`). PASS.
- **C4 (Layer-2b token check)** — `https://example.com`: real token -> `HELD`; altered token -> `NOT-HELD`. PASS.
- **C5 (per-host soft-404 sweep)** — 89 hosts swept; soft-404 hosts found: ['hackerfactor.com', 'metricgate.com', 'ohchr.org'].

## Stop rule

C1 fired correctly: **True**. C3 fired correctly: **True**. Stop rule: **PASS — census may proceed**.

## C5 detail

| host | probe status | verdict | soft-404 host? |
|---|---|---|---|
| aafp.org | 404 | GONE |  |
| academicintegrity.org | 410 | GONE |  |
| aclanthology.org | 404 | GONE |  |
| ai-act-service-desk.ec.europa.eu | 404 | GONE |  |
| amacad.org | 404 | GONE |  |
| apaf.org | 404 | GONE |  |
| api.github.com | 403 | BLOCKED |  |
| archive.cdc.gov | 404 | GONE |  |
| artificialintelligenceact.eu | 404 | GONE |  |
| arxiv.org | 404 | GONE |  |
| cambridge.org | 403 | BLOCKED |  |
| caselaw.nationalarchives.gov.uk | 404 | GONE |  |
| cdn-dynmedia-1.microsoft.com | 404 | GONE |  |
| commons.wikimedia.org | 404 | GONE |  |
| community.openai.com | 404 | GONE |  |
| cv.iptc.org | 404 | GONE |  |
| datacenters.lbl.gov | 404 | GONE |  |
| datamatters.sidley.com | 404 | GONE |  |
| digimarc.com | 404 | GONE |  |
| documentcloud.org | 404 | GONE |  |
| doi.org | 400 | GONE |  |
| en.wikipedia.org | 404 | GONE |  |
| eur-lex.europa.eu | 404 | GONE |  |
| export.arxiv.org | 404 | GONE |  |
| frankbueltge.de | 404 | GONE |  |
| ghgprotocol.org | 404 | GONE |  |
| github.com | 403 | BLOCKED |  |
| hackerfactor.com | 200 | OK | yes |
| harvardlawreview.org | 404 | GONE |  |
| info.arxiv.org | 404 | GONE |  |
| jaapl.org | 404 | GONE |  |
| jabfm.org | None | NETFAIL |  |
| lrb.co.uk | 404 | GONE |  |
| marcellodibello.com | None | NETFAIL |  |
| metricgate.com | 200 | OK | yes |
| minnlawyer.com | 404 | GONE |  |
| motherjones.com | 404 | GONE |  |
| nber.org | 404 | GONE |  |
| ncbi.nlm.nih.gov | 404 | GONE |  |
| noclimateresultsfound.com | 404 | GONE |  |
| ohchr.org | 200 | OK | yes |
| partnershiponai.org | 404 | GONE |  |
| pmc.ncbi.nlm.nih.gov | 404 | GONE |  |
| policyreview.info | 404 | GONE |  |
| propublica.org | 404 | GONE |  |
| psychiatry.org | 404 | GONE |  |
| pubmed.ncbi.nlm.nih.gov | 404 | GONE |  |
| rand.org | 403 | BLOCKED |  |
| raw.githubusercontent.com | 404 | GONE |  |
| reuters.com | 401 | GONE |  |
| spec.c2pa.org | 404 | GONE |  |
| storage.googleapis.com | 404 | GONE |  |
| sustainability.google | 404 | GONE |  |
| tbray.org | 404 | GONE |  |
| web.williams.edu | 404 | GONE |  |
| websites.umich.edu | 403 | BLOCKED |  |
| worldprivacyforum.org | 404 | GONE |  |
| www.aafp.org | 404 | GONE |  |
| www.abc.net.au | 404 | GONE |  |
| www.brookings.edu | 404 | GONE |  |
| www.bsfrey.ch | 404 | GONE |  |
| www.cambridge.org | 403 | BLOCKED |  |
| www.computerweekly.com | 404 | GONE |  |
| www.datacenterdynamics.com | 403 | BLOCKED |  |
| www.devsustainability.com | 404 | GONE |  |
| www.documentcloud.org | 404 | GONE |  |
| www.gov.uk | 404 | GONE |  |
| www.gstatic.com | 404 | GONE |  |
| www.kaggle.com | 404 | GONE |  |
| www.legislation.gov.uk | 404 | GONE |  |
| www.marcellodibello.com | 404 | GONE |  |
| www.ncbi.nlm.nih.gov | 404 | GONE |  |
| www.ohchr.org | 403 | BLOCKED |  |
| www.oiahe.org.uk | 404 | GONE |  |
| www.postofficehorizoninquiry.org.uk | 404 | GONE |  |
| www.propublica.org | 404 | GONE |  |
| www.psychiatry.org | 404 | GONE |  |
| www.rehva.eu | 404 | GONE |  |
| www.scconline.com | 404 | GONE |  |
| www.science.org | 403 | BLOCKED |  |
| www.sciencedirect.com | 403 | BLOCKED |  |
| www.smartenergydecisions.com | 403 | BLOCKED |  |
| www.strausstroy.com | 404 | GONE |  |
| www.sunbirddcim.com | 404 | GONE |  |
| www.tbray.org | 404 | GONE |  |
| www.theguardian.com | 404 | GONE |  |
| www.turnitin.com | 403 | BLOCKED |  |
| www.w3.org | 404 | GONE |  |
| yaledailynews.com | 429 | BLOCKED |  |

