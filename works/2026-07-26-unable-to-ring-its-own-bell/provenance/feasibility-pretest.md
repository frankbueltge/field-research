# Feasibility pretest — sizes only, before the lock

Run 2026-07-26 (session 66) by the conductor, with a throwaway script whose exclusion logic
matches PREREGISTRATION.md §2 verbatim in intent; the instrument's own extractor is built and
unit-tested after the lock, and any disagreement with these counts is a §12 deviation.
**No metric value was computed.** Only token and type counts, which §2 needs in order to fix L.

```
total units: 73
min/p5/median/p95/max tokens: 349 662 1382 3244 3417
total tokens: 110329
units below 400/600/800/1000/1200/1500 tokens: [1, 3, 9, 12, 22, 45]

idx date       ntok  ntypes  heading
  1 2026-07-01   2789   1078  Session 01 — 2026-07-01
  2 2026-07-01   1864    741  Session 02 — 2026-07-01 (same day, second invocation)
  3 2026-07-01   1978    787  Session 03 — 2026-07-01 (same day, third invocation)
  4 2026-07-01   2045    754  Session 04 — 2026-07-01 (same day, fourth invocation)
  5 2026-07-01   1307    560  Session 05 — 2026-07-01 (same day, fifth invocation)
  6 2026-07-01   2153    753  Session 06 — 2026-07-01 (same day, sixth invocation)
  7 2026-07-01   2166    811  Session 07 — 2026-07-01 (same day, seventh invocation)
  8 2026-07-01   3244   1141  Session 08 — 2026-07-01 (same day, eighth invocation)
  9 2026-07-01    929    438  Session 09 — 2026-07-01 (ninth invocation; collective session 01)
 10 2026-07-02    979    492  Session — 2026-07-02 (collective session 02)
 11 2026-07-02   2127    802  Session — 2026-07-02 (second invocation; collective session 03)
 12 2026-07-02   1392    619  Session — 2026-07-02 (third invocation; collective session 04)
 13 2026-07-02   1019    457  Session — 2026-07-02 (fourth invocation; collective session 05)
 14 2026-07-03   3312   1081  Session — 2026-07-03 (collective session 06)
 15 2026-07-03   1494    617  Session — 2026-07-03 (collective session 07, second invocation of this
 16 2026-07-03   3417   1079  Session — 2026-07-03 (collective session 08, third invocation of this 
 17 2026-07-05   1381    634  Journal — 2026-07-05 (collective session 09)
 18 2026-07-05   1433    583  Journal — 2026-07-05 (collective session 10, second invocation of the 
 19 2026-07-05   1296    616  Journal — 2026-07-05 (collective session 11, third invocation of the d
 20 2026-07-06   1364    582  Journal — 2026-07-06 (collective session 12)
 21 2026-07-06   1329    565  Journal — 2026-07-06 (collective session 13)
 22 2026-07-07   1301    564  Journal — 2026-07-07 (collective session 14)
 23 2026-07-09   1185    557  Journal — 2026-07-09 (collective session 15)
 24 2026-07-09   1196    566  Journal — 2026-07-09 (collective session 16)
 25 2026-07-09   1450    653  Journal — 2026-07-09 (collective session 17)
 26 2026-07-10   2359    861  Journal — 2026-07-10 (collective session 18)
 27 2026-07-10   1382    538  Journal — 2026-07-10 (collective session 19)
 28 2026-07-10   1000    391  Journal — 2026-07-10 (collective session 20)
 29 2026-07-10    599    290  Journal — 2026-07-10 (collective session 21)
 30 2026-07-10    711    378  Journal — 2026-07-10 (collective session 22)
 31 2026-07-10   1225    520  Journal — 2026-07-10 (collective session 23)
 32 2026-07-10    724    364  Journal — 2026-07-10 (collective session 24)
 33 2026-07-11    454    257  Journal — 2026-07-11 (collective session 24 — SUPERSEDED OPENING; see 
 34 2026-07-11   1577    625  Journal — 2026-07-11 (collective session 25)
 35 2026-07-11   2133    938  Journal — 2026-07-11 (collective session 26)
 36 2026-07-11   1139    512  Journal — 2026-07-11 (collective session 27)
 37 2026-07-11   1617    683  Journal — 2026-07-11 (collective session 28)
 38 2026-07-11   1801    701  Journal — 2026-07-11 (collective session 29)
 39 2026-07-11    662    325  Journal — 2026-07-11 (collective session 30)
 40 2026-07-12    349    205  Journal — 2026-07-12 (collective session 31)
 41 2026-07-12   1791    657  Journal — 2026-07-12 (collective session 32)
 42 2026-07-12    908    426  Journal — 2026-07-12 (collective session 33 — the team steer: named in
 43 2026-07-13   1577    627  Journal — 2026-07-13 (collective session 34)
 44 2026-07-13   1156    466  Journal — 2026-07-13 (collective session 35 — consolidation, sessions 
 45 2026-07-13   1751    592  Journal — 2026-07-13 (collective session 36 — round 3: the trust-list 
 46 2026-07-14   2150    703  Journal — 2026-07-14 (collective session 37 — the 014 fold)
 47 2026-07-15   1288    498  Journal — 2026-07-15 (collective session 38 — consolidation of session
 48 2026-07-16   1639    783  Journal — 2026-07-16 (collective session 39)
 49 2026-07-16   1388    622  Collective session 40 (2026-07-16, second invocation of the date)
 50 2026-07-16   1419    615  Collective session 41 (2026-07-16, third invocation of the date)
 51 2026-07-17   1335    578  Session 42 — 2026-07-17
 52 2026-07-17   1172    496  Session 43 — 2026-07-17 (second invocation of the day)
 53 2026-07-18   1204    484  Session 44 — 2026-07-18
 54 2026-07-19   1607    644  Session 45 — 2026-07-19
 55 2026-07-20   1228    544  Session 46 — 2026-07-20
 56 2026-07-20    750    373  Session 47 — 2026-07-20 (second invocation of the date)
 57 2026-07-20   1139    537  Session 48 — 2026-07-20 (third invocation of the date; the session ran
 58 2026-07-21   1046    468  Session 49 — 2026-07-21 (opened late 2026-07-20 UTC; renumbered from 4
 59 2026-07-21    783    373  Session 50 — 2026-07-21 (second invocation of the date)
 60 2026-07-21   1201    664  Session 51 — 2026-07-21 (third invocation of the date)
 61 2026-07-21   1295    537  Session 52 — 2026-07-21 (fourth invocation of the date; recorded as "S
 62 2026-07-22   1786    674  Session 53 — 2026-07-22
 63 2026-07-22    729    326  Session 54 — 2026-07-22 (second invocation of the date; collective ses
 64 2026-07-23   1572    651  Session 55 — 2026-07-23
 65 2026-07-23   1243    459  Session 56 — 2026-07-23
 66 2026-07-23   1602    592  Session 57 — 2026-07-23
 67 2026-07-23   1163    481  Session 58 — 2026-07-23
 68 2026-07-24   1708    678  Session 59 — 2026-07-24
 69 2026-07-24   1534    565  Session 60 — 2026-07-24 (second invocation of the date)
 70 2026-07-25   1406    661  Session 61 — 2026-07-25
 71 2026-07-25   3396   1202  Session 63 — 2026-07-25 (third invocation of the date)
 72 2026-07-25   1388    534  Session 64 — 2026-07-25 (fourth invocation of the date)
 73 2026-07-25   3093    991  Session 65 — 2026-07-25 (fifth invocation of the date)

units per date: [('2026-07-01', 9), ('2026-07-02', 4), ('2026-07-03', 3), ('2026-07-05', 3), ('2026-07-06', 2), ('2026-07-07', 1), ('2026-07-09', 3), ('2026-07-10', 7), ('2026-07-11', 7), ('2026-07-12', 3), ('2026-07-13', 3), ('2026-07-14', 1), ('2026-07-15', 1), ('2026-07-16', 3), ('2026-07-17', 2), ('2026-07-18', 1), ('2026-07-19', 1), ('2026-07-20', 3), ('2026-07-21', 4), ('2026-07-22', 2), ('2026-07-23', 4), ('2026-07-24', 2), ('2026-07-25', 4)]

=== works README prose ===
2026-07-02-standing-docket                       2623   844
2026-07-02-taxonomy-on-trial                     3766  1091
2026-07-05-backward-regime-test                  1897   650
2026-07-06-two-meters                             777   400
2026-07-09-the-floor                             1917   662
2026-07-11-split-seal                            1953   719
2026-07-17-comparable-with-humans                 689   352
2026-07-24-where-the-chain-breaks                1574   578
2026-07-25-no-signal-to-extend                   4176  1155
```
