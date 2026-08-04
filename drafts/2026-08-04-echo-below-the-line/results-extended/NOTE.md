# The extended run — larger pool, fixed normalisation, **no verdict from anyone**

**Read this before reading the numbers beside it.** Nothing in this directory has been through the
gauntlet. The Verifier, the Skeptic and the Interlocutor all reviewed the run in `../results/`
(politics only, 250 records, ASCII normalisation). This run differs from that one in two ways at
once — more data *and* a changed normalisation — so it is not a clean sensitivity test of either.
It is here because withholding it would be worse than labelling it.

**What changed.** Beat files for **technology** and **health** arrived from the rate-limited fetch
after the reviews began (economy, science and business were refused by the API through three
attempts each; the fetch log is the record). And the ASCII-only normalisation the Verifier found —
which made a title in a non-Latin script incapable of being echo at all — was replaced with a
Unicode-aware one.

**Run:** `ECHO_RESULTS_DIR=results-extended python3 scripts/measure_echo.py`, over
`provenance/gdelt-{health,politics,technology}.json`.

| | reviewed run (`../results/`) | this run |
|---|---|---|
| beats | politics | health, politics, technology |
| pool after URL dedup | 250 | **712** |
| distinct domains | 203 | **442** |
| normalisation | ASCII-only | Unicode-aware |
| Echo index A | 23.60 % | **22.33 %** |
| B at t = 0.9 / 0.8 | 22.00 % / 22.00 % | **21.21 % / 21.21 %** |
| B at t = 0.7 / 0.6 / 0.5 | 22.80 / 24.40 / 24.80 % | **21.77 / 22.47 / 23.46 %** |
| qualifying examples at t = 0.9 | 0 | **0** |
| publisher groups | 203 → 155 | **442 → 331** |
| collapsed echo index | 3.20 % | **5.06 %** |
| the drop | −20.40 pp | **−17.28 pp** |

**Both of the session's results hold on the larger pool.** The near-duplicate rule is still *below*
the verbatim rule at every threshold from 0.9 to 0.7 and still returns **zero** qualifying examples
at the strictest one — the title-level paraphrase gap is absent here too. And the publisher-collapse
still moves the index by seventeen points.

**The concentration, decomposed again** (`drop_decomposition.json` in this directory, produced by
`scripts/decompose_drop.py --all`): the 17.28 pp comes from **19 publisher groups** — not 7 — of
which the largest carries **3.37 pp (19.5 %)** and the top four **10.26 pp (59 %)**. So the effect
is *less* concentrated on the larger pool than the reviewed run suggested, and the honest reading
moves slightly in the finding's favour. That is exactly why it is not allowed to count: it moves in
our favour, and it has not been checked by anyone but us.

**What a future session must do before any of this ships.** Re-run the gauntlet on the state that
would ship; separate the two changes (data, normalisation) so each can be attributed; and get more
than one day.
