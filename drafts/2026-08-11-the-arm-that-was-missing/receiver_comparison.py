#!/usr/bin/env python3
"""What the null model can and cannot say about the receiver's published decomposition.

Session 113, 2026-08-12. Every figure here is computed from presence-baseline.json and from
numbers quoted verbatim out of the receiver's own report (SOURCE-READING-113.md); nothing is
asserted. Output: receiver-comparison.json

THE ONE THING THIS FILE MUST NOT DO, and it is written here because it is the temptation:
it must not state a public-absence figure FOR THE RECEIVER'S CORPUS. Their report publishes
no upload dates and no age distribution for the ~260,000 donated videos, and this practice
has not measured them. Everything below is either (a) conditional on an age profile stated
as an assumption, or (b) a bound that holds across EVERY age profile our reference
population can express. Those are the only two honest forms.
"""

import json

BASELINE = "presence-baseline.json"
OUT = "receiver-comparison.json"

# --- quoted verbatim from the receiver's report, arXiv:2506.09746v2 (see SOURCE-READING-113)
RECEIVER = {
    "source": "arXiv:2506.09746v2, TikTok's Research API: Problems Without Explanations",
    "authors": "Entrena-Serrano, Degeling, Romano, Cetin",
    "url": "https://arxiv.org/abs/2506.09746v2",
    "read_utc": "2026-08-12",
    "initial_sample": 260000,          # "approximately 260,000 TikToks"
    "initially_unretrievable": 70239,  # "we were initially unable to retrieve metadata for 70,239"
    "share_not_public": 0.36,          # "approximately 36% were not public - either deleted,
                                       #  private, or only visible to friends"   (both sections)
    # The report gives the public-but-unavailable share TWICE, and the two do not agree.
    # Method section : "The other 62.7% were all publicly available on the platform, but not
    #                   retrievable through the API"                    -> share of 70,239
    # Summary section: "We were able to successfully retrieve, after multiple attempts, only
    #                   18% ... the largest share (36%) ... the remaining 46% of the videos
    #                   were public, but not available via the API"     -> share of 70,239
    # 18 + 36 + 46 = 100, so the summary's decomposition is AFTER the retry recoveries and
    # the method section's is BEFORE them: 62.7 - 18 = 44.7 against 46. Both are carried;
    # neither is quietly chosen. The reconciliation residual is computed below, not asserted.
    "share_public_not_in_api_method_section": 0.627,
    "share_public_not_in_api_summary_section": 0.46,
    "share_retrieved_on_retry": 0.18,  # "successfully retrieve, after multiple attempts,
                                       #  only 18% of the videos for which we missed metadata"
    "headline": 0.1246,                # "roughly 1 in 8 posts (12,46%) of videos could not be
                                       #  analyzed"
    # The summary section decomposes its own 46% further: part is a known API limitation
    # (videos from Canada), "a similar share" is advertisements, and "For the remaining 21%
    # of videos, we do not know why the API did not return any information". 25 + 21 = 46,
    # so the 21% is a share of the 70,239 like the others. This is the share their own body
    # leaves genuinely unexplained.
    "share_unexplained_summary_section": 0.21,
    "method_for_not_public": ("scraping TikTok to check if the unavailable posts were "
                              "publicly available on the platform"),
}


def main():
    b = json.load(open(BASELINE))
    bands = b["by_age_band"]

    # 1. Is the headline the residual, or the whole gap? Checked by arithmetic on their own
    #    numbers rather than by reading the abstract's compression.
    N0, U = RECEIVER["initial_sample"], RECEIVER["initially_unretrievable"]
    n_not_public = U * RECEIVER["share_not_public"]
    n_pub_summary = U * RECEIVER["share_public_not_in_api_summary_section"]
    n_pub_method = U * RECEIVER["share_public_not_in_api_method_section"]
    funnel = {
        "initially_unretrievable_share_of_sample": U / N0,
        "not_public_count": n_not_public,
        "not_public_share_of_sample": n_not_public / N0,
        "public_but_not_in_api_summary_section": {
            "count": n_pub_summary, "share_of_sample": n_pub_summary / N0},
        "public_but_not_in_api_method_section": {
            "count": n_pub_method, "share_of_sample": n_pub_method / N0},
        "published_headline": RECEIVER["headline"],
        "headline_matches_summary_section":
            abs(n_pub_summary / N0 - RECEIVER["headline"]) < 0.005,
        "headline_matches_method_section":
            abs(n_pub_method / N0 - RECEIVER["headline"]) < 0.005,
        "internal_reconciliation": {
            "summary_shares_sum": (RECEIVER["share_retrieved_on_retry"]
                                   + RECEIVER["share_not_public"]
                                   + RECEIVER["share_public_not_in_api_summary_section"]),
            "method_shares_sum": (RECEIVER["share_not_public"]
                                  + RECEIVER["share_public_not_in_api_method_section"]),
            "method_minus_retry": (RECEIVER["share_public_not_in_api_method_section"]
                                   - RECEIVER["share_retrieved_on_retry"]),
            "residual_against_summary": (RECEIVER["share_public_not_in_api_method_section"]
                                         - RECEIVER["share_retrieved_on_retry"]
                                         - RECEIVER["share_public_not_in_api_summary_section"]),
            "note": ("Reported as observed, not as an error found. The two sections are "
                     "reconcilable if the method section's split is taken before the retry "
                     "recoveries and the summary's after; a small residual remains, and the "
                     "method section's own two shares sum to 98.7 rather than 100."),
        },
        "unexplained_by_their_own_body": {
            "count": U * RECEIVER["share_unexplained_summary_section"],
            "share_of_sample": U * RECEIVER["share_unexplained_summary_section"] / N0,
            "one_in": N0 / (U * RECEIVER["share_unexplained_summary_section"]),
            "note": ("The abstract compresses this: it says one in eight fails 'without an "
                     "apparent reason' while naming advertisements inside that eight. The "
                     "body's own residual - the share it says it cannot explain at all - is "
                     "the figure computed here. Both are the authors' own numbers; the point "
                     "is which question each answers, not that either is wrong."),
        },
        "reading": ("Whichever share the published headline reproduces is the share the "
                    "one-in-eight actually names. If it is the public-but-unavailable one, "
                    "then the headline is ALREADY NET of the videos their own scrape found "
                    "not to be public - it is not the raw gap, and a public-presence null "
                    "cannot deflate it, because they already applied one."),
    }

    # 2. The bound that holds across every age profile our reference population can express.
    #    A weighted average cannot exceed its largest component, so the most non-public a
    #    corpus can look under this curve is the worst single band.
    worst = max((c for c in bands.values() if c["n"]), key=lambda c: c["absent_rate"])
    worst_band = [k for k, v in bands.items() if v is worst][0]
    ceiling = {
        "worst_band": worst_band,
        "worst_band_n": worst["n"],
        "max_expected_absence_point": worst["absent_rate"],
        "max_expected_absence_upper_ci": worst["absent_ci"][1],
        "receiver_share_not_public": RECEIVER["share_not_public"],
        "receiver_exceeds_ceiling":
            RECEIVER["share_not_public"] > worst["absent_ci"][1],
        "reading": ("No age composition of this reference population can produce a "
                    "non-public share as high as the receiver measured among API-failing "
                    "videos, because a weighted mean cannot exceed its largest component. "
                    "Under the cross-population assumption stated below, their API-failure "
                    "set is enriched for non-public content beyond what age alone explains."),
    }

    # 3. The conditional form: IF their videos had the age profile of the eleven their own
    #    dashboard tracks - the only videos of theirs whose ages this practice can derive -
    #    then this is what our curve expects. n = 11. This is a worked example of the
    #    transfer function, NOT an estimate for their corpus.
    try:
        chk = json.load(open("presence-check-receiver-113.json"))
        exp = chk["expectation_for_this_age_profile"]
        conditional = {
            "assumed_profile": "the eleven identifiers on the receiver's own dashboard",
            "n_dated": exp["n_dated"],
            "age_histogram": exp["age_histogram"],
            "expected_absence": exp["expected_absent_rate"],
            "expected_lo": exp["expected_lo"],
            "expected_hi": exp["expected_hi"],
            "observed_absence_in_those_eleven": chk["public_absence_rate"],
            "warning": ("n = 11. This is a worked example of the transfer function on the "
                        "only videos of theirs whose ages are derivable from public "
                        "identifiers. It is NOT an estimate of their corpus's age profile, "
                        "and eleven videos selected for being API-failures are not a sample "
                        "of their 260,000."),
        }
    except Exception as e:
        conditional = {"unavailable": f"{type(e).__name__}"}

    out = {
        "schema": "field-research/receiver-comparison/1",
        "written_by": "session 113, 2026-08-12",
        "baseline": {"file": BASELINE, "pooled_n": b["pooled"]["n"],
                     "run_id": b["source_run"]["run_id"]},
        "receiver_numbers_quoted": RECEIVER,
        "funnel_arithmetic": funnel,
        "ceiling_bound": ceiling,
        "conditional_worked_example": conditional,
        "what_is_NOT_claimed": [
            "No public-absence figure is stated for the receiver's ~260,000 donated videos.",
            "Their report publishes no upload dates and no age distribution for that corpus.",
            "Our NOT-RETRIEVABLE cannot distinguish deleted from private from never-existed; "
            "their 2025 scrape did distinguish them, and on that axis their method was the "
            "more discriminating one.",
            "Our reference population is citation-selected and forum-selected. Transfer to a "
            "donation-selected corpus is an assumption, stated, never established here.",
        ],
    }
    json.dump(out, open(OUT, "w"), indent=1)

    print("FUNNEL")
    print(f"  initially unretrievable      {U:,} / {N0:,} = "
          f"{funnel['initially_unretrievable_share_of_sample']:.4f}")
    print(f"  not public (their scrape)    {n_not_public:,.0f} = "
          f"{funnel['not_public_share_of_sample']:.4f} of sample")
    print(f"  public-but-not-in-API (summary 46%) {n_pub_summary:,.0f} = "
          f"{funnel['public_but_not_in_api_summary_section']['share_of_sample']:.4f}")
    print(f"  public-but-not-in-API (method 62.7%) {n_pub_method:,.0f} = "
          f"{funnel['public_but_not_in_api_method_section']['share_of_sample']:.4f}")
    print(f"  published headline           {RECEIVER['headline']:.4f}")
    print(f"  headline == summary share ?  {funnel['headline_matches_summary_section']}")
    print(f"  headline == method share  ?  {funnel['headline_matches_method_section']}")
    ux = funnel['unexplained_by_their_own_body']
    print(f"  unexplained by their own body {ux['count']:,.0f} = "
          f"{ux['share_of_sample']:.4f} of sample = one in {ux['one_in']:.1f}")
    r = funnel['internal_reconciliation']
    print(f"  summary shares sum {r['summary_shares_sum']:.3f}; method shares sum "
          f"{r['method_shares_sum']:.3f}; method-minus-retry {r['method_minus_retry']:.3f} "
          f"vs summary {RECEIVER['share_public_not_in_api_summary_section']:.3f} "
          f"(residual {r['residual_against_summary']:+.3f})")
    print("\nCEILING")
    print(f"  worst band {worst_band}: absence {worst['absent_rate']:.4f} "
          f"(upper CI {worst['absent_ci'][1]:.4f}), n={worst['n']}")
    print(f"  receiver's not-public share among API failures {RECEIVER['share_not_public']:.4f}")
    print(f"  exceeds every age composition of our reference population: "
          f"{ceiling['receiver_exceeds_ceiling']}")
    if "expected_absence" in conditional:
        print("\nCONDITIONAL WORKED EXAMPLE (n=11, not an estimate of their corpus)")
        print(f"  expected {conditional['expected_absence']:.4f} "
              f"[{conditional['expected_lo']:.4f}, {conditional['expected_hi']:.4f}]  "
              f"observed {conditional['observed_absence_in_those_eleven']:.4f}")
    print("\nwritten", OUT)


if __name__ == "__main__":
    main()
