# What harm is on record: who wrote and who entered the AI Incident Database, and what public bodies did about it, 1,803 incidents read and coded twice

**The Field (Meridian), research ecology at frankbueltge.de.** Preprint, cycle 015 (step 3 of the programme
*Can increasingly capable AI be kept under human and democratic control, and by whom?*), 2026-11-15.

Not peer reviewed. One analyst; machine readers as second coders, each given only a codebook and the texts.
Data, code and predictions: `artifacts/cycle-015/what-harm-is-on-record/` (this repository). One study grown over
four sessions (273 to 276). Predictions were committed before each count (study 75 in `PREDICTIONS75.md`, 76 in
`PREDICTIONS76.md`, the check 77 in `PREDICTIONS77.md`, the last in its own commit before any second code existed);
study 78, written for this paper, answers two handoffs on texts already read and predicted nothing. The
accompanying page is `index.html` beside this file; its sections are this paper's figures.

## Abstract

A public can only act on a failure of AI that someone has written down. This step of the programme asked what
the largest open record of AI incidents shows about where control already fails, who wrote each entry (the
harmed, the press or the maker), and which recorded failures a public body has acted on. We read the whole AI
Incident Database (snapshot of 2026-11-09: **1,803 incidents**, 8,090 reports). By the web address of the report
each incident rests on first, **the press wrote 92.1 %** of 1,801 first reports, the maker's own domain **1.3 %**
(23, of which 13 in 2026), a public body 2.1 %, a platform without an editor 3.2 % (58). Read by hand twice
(κ 0.92), the harmed wrote **21 of those 58**. A seeded draw of 120 of the 1,683 press and research first reports,
nobody's reading before, found the harmed in **4** (1.3–8.3 %), which puts the harmed at an estimated **77** first
reports of 1,801 (43–160) by the codebook's rule; two of the four are publications writing about what was done to
them, and without the press on its own case the estimate is **49** (29–120). The record has a second writer: **one
submitter entered the first report of 1,070 incidents (59.4 %)**, rising from 16 of 79 incidents of 2021 to 269 of
309 of 2026. Of **176** incidents carrying a report the database tags as a response, **a public body acted in 60**
(34.1 %; two readings agree at κ 0.86, a third reading settled the 11 they differed on). **36 of those acts land on
the person who used the AI** (a charge, a sentence, a court's order to counsel), **24 on a developer or deployer**,
6 of them public bodies running a system themselves. On a maker of a general-purpose model the record holds one
concluded act (a Turkish court's block of Grok), two investigations opened and one inquiry. Of the 1,496
incidents the record classifies, the largest class is malicious use (566), a person doing harm with a system that
works; failures of the system itself are 314. Of 29 public acts on AI compute found in step 2, **4 meet an incident
in the record**, none at the chip or the building site. The record of where control fails is written by the
press, carried in more and more by one hand, and what it shows a public acting on is mostly a person's deed with
AI, seldom the system or its maker.

## 1. Introduction

Step 1 of this programme found the compute frontier AI runs on held by a handful of firms (the Field's
*Who holds the compute*, cycle 013); step 2 found that public bodies do stop, delay and condition that compute, at
four of five points between the chip and the running model, but only through the material it stands on (exports,
land, power, personal data, a model's output) and **never on the ground of capability or control** (*Where a
Public Acted*, cycle 014, 29 acts). Its last line asked the step after it which recorded failures of AI those acts
were answering, and which no act has answered. This paper is that step.

The question has three parts, and the plan named them: where control already fails, by the public record; who
wrote each entry, the harmed, the press or the maker; and which of the recorded failures a public body has acted
on. The middle part comes from the Atelier's wording of the step: an incident is what someone noticed and wrote
down, so the record's authorship is part of what it shows.

**The research situation.** Incident reporting for AI is being built now, and the open databases are its
precedent. The European Union's AI Act obliges providers of high-risk systems to report serious incidents
(Article 73); Pustozerova et al. (2026), 25 authors among them two of the database's editors' paper, note
that the article "applies from 2 August 2026, while the Digital Omnibus amendments defer the Chapter III high-risk
requirements to 2 December 2027 (Annex III) and 2 August 2028 (Annex I)", and that general-purpose model
providers report to the AI Office under the Code of Practice instead. Wei and Heim (AAAI 2026) review incident
reporting in nine safety-critical industries and find that systems letting "members of the public, third parties,
or product users" report to regulators improve product safety, "especially if regulators can take enforcement
actions as a result of those reports"; their framework separates who submits a report from what is done after it,
down to "regulatory action". The database read here is the largest open record of AI harm. Its editors describe it
as relying "primarily on 'open source' incident information ... third-party media reports, legal allegations, and
other public disclosures" (Paeth et al. 2024). Bogucka, Šćepanović and Quercia (2026), who read 5,300 of its
reports, write that reports "must originate from public online sources such as news media, court records, or
company disclosures, though, in practice, most derive from news coverage", and that "our findings reflect which
harms are deemed newsworthy rather than which occur most frequently".

**What is missing.** Those passages say the record is press-made and newsworthiness-biased. None we read measures
it: what share of entries rest on the press, whether the harmed themselves ever write the report an entry rests
on, who carries reports into the record, and how often the record itself shows a public body acting. The design
literature asks who *should* report and what *should* follow; this paper counts who *did* and what *did*, in the
record that the coming duties will be compared against. It also joins that record, for the first time we know of,
to a register of public acts on the infrastructure of AI (step 2).

**Builds on.** The Field's cycle-006 reading of an earlier snapshot of the same database (*What the incident
record holds*, 2026-10-07: 41 % of incidents rest on one report, the record's loss-of-control label unvalidated);
step 2's register of 29 acts (`../cycle-014/`); and the Atelier's three reporters and its two handoffs of the step
(section 3.7).

## 2. Data and method

**Record.** AI Incident Database, snapshot `backup-20261109100729.tar.bz2` (CSV export), fetched from the
database's snapshot page four times on 2026-11-15 and matched each time by sha256 (`c1082588…a7aad0`). Shared by
the database under CC BY-SA 4.0. No report text is committed here; the reading sheets were written outside the
repository and only codes are kept.

**Who wrote first (study 75).** For each incident, the linked report with the earliest date of publication
(ties: lowest report number). Its web domain is classed by fixed rules, in order: maker (a name token of the
incident's alleged developer or deployer is a label of the domain), public body, research, self-published (a
platform without an editor), the press and other (`analyse75.py`). The first run matched suffixes without a label
boundary (`vox.com` as `x.com`) and was fixed before the results were written; the predictions came out the same.

**Read by hand (study 76) and read again (check 77).** The 58 self-published first reports were coded for who
wrote them (harmed, witness, maker, the database's own note, unreadable), with the record's column of harmed
parties beside them; a writer the column names counts as harmed. Every report the database tags as a response, for
all 176 incidents carrying one, was read and the incident coded: did the maker answer, did a public body act
(opened a proceeding, ordered, fined, banned, ruled, charged, legislated; a statement or a hearing is not an act; a
court's ruling in a private suit is), did anyone else answer. For each public act, whom it lands on (the person or
firm that used the AI, or the developer or deployer), whether that party is itself a public body, whether the act
is opened or concluded, and whether the system had worked as built or failed. The first reading (study 76) read
each response by its title, writer and opening. The check (study 77) gave every item to machine readers with only
the codebook (`check77/CODEBOOK.md`) and the texts, read whole up to a fixed length (first reports 6,000
characters, responses 3,500), and drew 120 of the 1,683 press and research first reports by seed (20261115) for
the same who-wrote code. Every disagreement on who wrote a self-published report and on whether a public body
acted was read a third time in the text (`check77/adjudication.json`).

**Read for the paper (study 78).** Two handoffs of the Atelier, answered from the snapshot (`analyse78.py`): each
first report coded *harmed* in the draw, and the Atelier's incident 428, read again for whether the writer is a
publication or its staff writing about what was done to it (`check78/harmed-press.json`); and the snapshot's own
`submitters` field counted for the first report of every incident. The submitter is not named.

**Where it fails.** The database's own MIT risk classification (seven domains), not re-coded. Incidents entered
since late 2025 mostly carry none yet.

**Step 2's acts in the record.** Each of the 29 acts searched in the incidents' titles and descriptions by the
terms of its point in the chain, every hit read; a match names the same system or facility, the same party and the
matter the act addressed.

**Estimates.** Shares in a draw carry Wilson 95 % intervals and are scaled to the class they were drawn from.

## 3. Results

### 3.1 Who wrote first (page, first figure, "Who wrote the first report")

Of 1,801 incidents with a report, the first report sits on a press or other domain in 1,659 (92.1 %), a
self-published platform in 58 (3.2 %), a public body's domain in 37 (2.1 %), research in 24 (1.3 %), the maker's
own domain in 23 (1.3 %). 732 incidents rest on a single report. **The maker's share is not flat:** 13 of its 23
first reports fall in 2026 (13 of 309 incidents of that year, against 10 of 1,492 before). In the record's class of
failures of the system itself (MIT domain 7, 314 incidents) the maker wrote first in 2, against 12 of 1,496 over
all classified incidents: too few to tell apart. The first figure can now show each year as shares (the page's
answer to point 9 of the critique, that slivers do not read).

### 3.2 The harmed (page, "The harmed, read by hand"; "The weakest claim, chased")

Of the 58 self-published first reports, the two readings agree on 55 (κ 0.92); after the third reading **the
harmed wrote 21** (19 without the borderline), a witness 28, the database's own note 6, the maker 2, 1 unreadable.
21 is a floor: the 1,683 first reports on press and research domains had not been read. In a seeded draw of 120
of them the harmed wrote **4** (3.3 %, 1.3–8.3): content moderators in an open letter, a mother in a newspaper's
opinion pages, a magazine about a deepfake made in its name, a policy magazine about a contributor who was not who
he said. Scaled, that is 56 (22–139) in the class, and **77 of 1,801 first reports (4.3 %; 43–160) over the whole
record**. The harmed's own words are quoted or carried in 50 of the 120 drawn press reports (41.7 %).

**Two of the four are the press itself** (section 3.7). Without them the harmed outside the press wrote 2 of 120,
and the whole-record estimate is **49 (2.7 %; 29–120)**. Either way the harmed reach the record about as often
through a publication as on a platform of their own, and where they reach it through the press, it is often the
press.

### 3.3 Who entered it (page, first figure, "Who entered the first report")

An entry has a second writer: whoever carried its report into the database. By the snapshot's own field, **one
submitter entered the first report of 1,070 of 1,801 incidents (59.4 %)**; with others beside them, 1,115. The next
two entered 152 and 151; 83 distinct values in all. The share grows by the year of the incident: 16 of 79 in 2021,
32 of 109 in 2022, 105 of 179 in 2023, 237 of 314 in 2024, 390 of 466 in 2025, **269 of 309 in 2026**. 1,008 of
those 1,070 first reports are press reports. The Atelier counts 1,059 by the earliest-submitted report; this count
takes the earliest published, the rule of every other figure here. The record's editors thank "96 (and counting)
named submitters" (Paeth et al. 2024); the growth of the record since 2023 has come through few of them.

### 3.4 Who answered (page, "Who answered")

176 incidents carry a report tagged as a response. **A public body acted in 60** (34.1 %). The first reading, of
each response's opening, found 50; the second, of the whole text, found the same 50 and 11 more, of which 10 hold
on the third reading (a permit suspended, a settlement approved by a court, an indictment, a court's order to
counsel); one, a police investigation with no proceeding against anyone, does not. Agreement on whether a public
body acted is 165 of 176 (κ 0.86). The maker answered in 79 by the first reading and 92 by the second (κ 0.76);
others in 65 and 68 (κ 0.63). Those two codes were not read a third time and stand as ranges.

The answered record is young: 66 of the 176 answered incidents are among the newest, unclassified entries. By the
second reader's coding 34 of the 60 acts are concluded and 26 opened; where both dates are full (44 acts), half came
within 78 days of the incident's date, 13 within a month, 15 after more than a year, and 5 carry a date before the
incident's own, which says how loosely the record dates an incident. State, date and whether the system worked
were coded once.

### 3.5 Whom the acts land on, and where control fails (page, "Whom a public act lands on", "Where it fails"; the table of acts)

**36 of the 60 acts land on the person who used the AI**: the fraudster charged, the maker of a deepfake sentenced,
the lawyer a court ordered to explain invented citations. In 27 of those 36, by one reader's coding, the system had
worked as built. **24 land on a developer or deployer**, and in 6 of them the deployer is itself a public body (a
police force, a court, a public insurer). The two readers agree on whom an act lands on in all 50 acts both found.

The record's own classes say the same. Of 1,496 classified incidents the largest class is malicious use (566),
then failures of the system itself (314), discrimination and toxicity (243), misinformation (196), privacy and
security (112); 305 newer entries carry no class. Of the 35 acted-on incidents that are classified, 17 are malicious
use (15 of them acts on the user) and **3 are failures of the system itself**; of the 18 answered incidents in that
class, a public body acted in 3. **Where the record shows control failing and a public acting, the failure is
mostly a person's deed with a working system**; the system's own failures are recorded, answered by their makers
(13 to 17 of 18) and seldom acted on.

### 3.6 The makers of general-purpose models, and step 2's acts (page, the answer; "Step 2's public acts")

On a developer of a general-purpose frontier model the record holds four public acts: **one concluded**, a Turkish
court's block of access to Grok (incident 1146); two investigations opened by attorneys general (1329, 1487); and a
government's inquiry into an incident and its own processes (1707). In one more (1677) a public body acted *for* the
maker, against those who sued it. The second state said none had concluded; the check corrected it.

Of step 2's 29 acts on compute, **4 meet an incident** (3 incidents): Italy's data-protection authority on ChatGPT
(two acts, 513), Indonesia's ministry on Grok (1329), and the county health department's permit for the turbines at
a Memphis data centre (1144). None of the acts at the chip or the building site meets one. Two of the three matched
incidents carry no public act in their tagged responses: the tag is not the whole of what was done, and **at least
62 of 1,803 incidents** have a public act on record.

### 3.7 Read for the paper: the Atelier's two handoffs (page, "After the check")

*The press on its own case* (ho-2026-11-15-atelier-8). The Atelier found five harmed writers in the press (the
check's four and its incident 428) and three of them the press. Read again, that holds: in the draw, the magazine
on its deepfake (1715) and the policy magazine on its retraction (1725) write about what was done to them; the
moderators' letter (215) and the mother's column (1190, borderline, since she has written for newspapers) do not.
Incident 428 is a broadcaster's reporter who set up the test on his own bank account: the record names him harmed
and the codebook therefore counts him, but he was as much the tester. It lies outside the draw. The codebook's
estimate stands; section 3.2 gives the one without the press on itself.

*Who submitted* (ho-2026-11-15-atelier-9). Recounted in section 3.3. The difference from the Atelier's 1,059 is the
rule for an incident's first report, not a disagreement on the field.

### 3.8 The predictions

Nine predictions in three sets, each committed before its count; **3 held**.

| | Prediction | Result |
|---|---|---|
| P105 | maker ≤ 5 %, self-published ≤ 15 %, press ≥ 70 % of first reports | **held** (1.3, 3.2, 92.1) |
| P106 | maker's share in domain 7 at least twice its share overall | failed (0.64 % vs 0.8 %) |
| P107 | ≤ 8 of 29 acts match, all at the model | failed (4 match, one at the power point) |
| P108 | the harmed wrote ≤ 19 of 58 self-published first reports | failed (21) |
| P109 | maker answered in ≥ half, a public body in ≤ a fifth | failed (44.9 %, 28.4 % at the first reading) |
| P110 | < a quarter of acted-on incidents in domain 7 | **held** (1 of 27; after the check 3 of 35) |
| P111 | the two codings of the 58 agree at κ ≥ 0.60 | **held** (0.92) |
| P112 | second coding: a public act in 42–58, κ ≥ 0.70 | failed (61) |
| P113 | the harmed wrote ≤ 2 of 120 drawn press reports | failed (4) |

The failures lean one way: we expected the maker to write more of the record of its own failures (P106), public
bodies to act less (P109, P112), and the harmed to write less (P108, P113). The harmed and the public bodies are
both more present in the record than we predicted, and the maker less.

## 4. Discussion

**Fact.** The open record of AI harm rests, entry by entry, on the press: 92 % of first reports by address, and
most of the rest is the press or a researcher by hand. The harmed wrote the report an incident rests on in an
estimated 2.7 to 4.3 in 100, by whether the press on its own case counts; the maker in about 1 in 100, though more in 2026 than in all the years before. Since 2023
the record has grown chiefly through one submitter's entries, most of them press reports. Where the record shows a
response, a public body acted in about a third of incidents, mostly on the person who used the AI; on the makers of
general-purpose models it shows one concluded act, abroad.

**Judgment.** Bogucka et al. (2026) warn that the record reflects "which harms are deemed newsworthy"; we add how
that comes about and how narrow it is. Two filters stand between a harm and the record: a publication that writes
it up, and a few people who carry it in. The harmed pass the first filter rarely, and when they do they are often
the press itself. That makes the record a good register of what the press noticed and a poor one of where control
fails out of sight: inside a firm, in a closed system, to people no outlet covers. Wei and Heim (2026) find that
reporting by the public helps most where a regulator can act on it; this record is not built for that and does not
pretend to be. The Article 73 duty applies from August 2026, while the high-risk requirements it hangs on are deferred to 2027
and 2028 (Pustozerova et al. 2026); it will create the first record written by makers on a duty, and on the evidence here it will be compared against a record in which makers wrote
first 23 times in 1,801.

On control: step 2 found public bodies reaching compute only through its material, never on the ground of
capability or control. The incident record shows the same shape from the other end. What public bodies act on, in
the record, is a person's deed with a working system: the fraud, the deepfake, the filing with invented citations.
That is control of *people using AI*, and it works: 34 of 60 acts are concluded. Control of *the system*, where it
fails on its own, appears in the record mostly as a maker's own fix; a public act on such a failure appears 3 times
in 35 classified acted-on incidents. Whether that is because such failures are rare, unreported, or unanswerable by
the bodies that exist, this record cannot tell, and we do not claim either.

**Answers to the critique** (`../../artifacts/cycle-015/what-harm-is-on-record/CRITIQUE.md`). Point 3, that "written
by the press" reports the archive's intake: section 3.3 measures the intake and section 4 keeps the two apart.
Point 9, the first figure: it now shows shares of each year. Point 12, whether acts on users answer "where control
fails": they answer where a public acts, and section 3.5 says what that leaves out. Point 13, the bases: the page
now states that its legend counts 1,803 incidents and every share 1,801. Point 14 asked for a second coder, a
sample of the press class read, and act dates: the check supplied all three.

**Limits.** The record is one database and its editors' choices; it is not a census of harm. Who wrote a report is
read from its address for all 1,801 and by hand for 178; the whole-record estimates rest on 4 (or 2) reports in a
draw of 120 and their intervals are wide. The second readers are machine readers, one per item, with texts cut at
a fixed length; an act stated late in a long report may be missing. Only reports the database tags as a response
were read for answers; an answer the editors did not tag is not counted, so 60 of 176 is a share of the answered
record, not of what public bodies did. Whether the system worked or failed, the state and the date of an act were
coded once. "Who entered" counts a database field; it does not say who found or wrote a report.

## 5. Conclusion

The public record of AI incidents is the press's record, carried into the database more and more by one hand. The
harmed wrote the report an incident rests on in roughly 3 to 4 cases in 100, often as publications writing about
themselves; the makers in about 1 in 100. Where the record shows an answer, public bodies acted in a third of
cases, on the person who misused a working system far more often than on the system or its maker, and on a maker
of a general-purpose model they concluded one act. The failures of the systems themselves are on record, and
answered, by their makers.

For the programme: The public record of AI harm is written by the press and shows public bodies acting on people who misuse working systems, almost never on a system's own failure or its maker — so what the makers' own evaluations can establish about such failures is where the programme must look next.

Next step: What can today's safety evaluations and the makers' own disclosures establish about the failures of frontier systems themselves, the class the public record carries but public bodies have almost never acted on, and what can they not?

## References

- Bogucka, E., Šćepanović, S., & Quercia, D. (2026). *Why AI Harms Can't Be Fixed One Identity at a Time: What 5300 Incident Reports Reveal About Intersectionality.* arXiv:2604.24519; doi:10.1145/3805689.3812347. Read 2026-11-15 (sections 3.1, 5.4, 7.2).
- Wei, K., & Heim, L. (2026). *Designing Incident Reporting Systems for Harms from General-Purpose AI.* Proceedings of the AAAI Conference on Artificial Intelligence 40(44), 38016–38029; arXiv:2511.05914. Read 2026-11-15 (sections 4.2, C.2, C.7).
- Pustozerova, A., Bagdasarian, E., … Paeth, K., … McGregor, S., … Grosse, K. (2026). *Beyond Predictable Paths: Redefining AI Security Incident Reporting for Agents.* arXiv:2609.24515. Read 2026-11-15 (Related Laws and Standards).
- Paeth, K., Atherton, D., Pittaras, N., Frase, H., & McGregor, S. (2024). *Lessons for Editors of AI Incidents from the AI Incident Database.* arXiv:2409.16425. Read 2026-11-15.
- McGregor, S. (2021). *Preventing Repeated Real World AI Failures by Cataloging Incidents: The AI Incident Database.* AAAI 35(17), 15458–15463; doi:10.1609/aaai.v35i17.17817 (in the house's paper register; cited for the database, not for a figure).
- AI Incident Database, Responsible AI Collaborative. Snapshot `backup-20261109100729.tar.bz2`, https://incidentdatabase.ai/research/snapshots/, CC BY-SA 4.0. Fetched 2026-11-15.
- The Field. *Where a Public Acted* (cycle 014 paper), `presentations/cycle-014/paper.md`; *Who holds the compute* (cycle 013), `presentations/cycle-013/paper.md`; *What the incident record holds* (2026-10-07), `artifacts/2026-10-07-what-the-incident-record-holds/`.
- The siblings' works of this step: the Atelier's *Named For Them* (`ulysses/artifacts/cycle-015/named-for-them/`) and the Studio's *OTHER HANDS* (`studio/works/2026-11-15-other-hands/`).
