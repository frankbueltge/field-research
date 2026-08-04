#!/usr/bin/env python3
"""Build `data.json` for "Where the Reader Declines".

Deterministic. Reads four committed files from the Meridian runtime repository,
joins them, and writes one JSON file. No network, no clock, no model. Same
inputs, byte-identical output.

    python3 build_data.py --runtime ../../../meridian-runtime --out data.json

--- What it joins ------------------------------------------------------------

1. `corpora/gold-classification/mb-cls-ulysses-v1-restamped.json`
   Sixty cases labelled BLIND by a sibling practice (Ulysses) against criteria
   locked before the labelling. Each label carries the rule that decided it.

2. `corpora/gold-classification/citations.manifest.json`
   Which sources those cases are — titles and arXiv identifiers. The gold set
   itself carries no titles, deliberately: a title is a hint.

3. `corpora/gold-classification/predictions-gemini-3.5-flash-lite.json`
   What a machine reader said about the same sixty, under the same criteria,
   with no access to the labels.

4. `benchmarks/meridianbench/fixtures/mb-cls-criteria.v3.json`
   The four definitions both readers worked from, verbatim.

--- The one judgement this script carries ------------------------------------

`POPULATION` below is a hand-made, READ classification: does this source's own
system do research — form hypotheses, run experiments, analyse, write up,
review — or does it do something else (reasoning, code, robotics, arithmetic,
computer operation, fact-checking, negotiation, style)?

It matters because the claim under test is about a population:

    "Systems that automate the research cycle end to end verify their own
     outputs independently of the component that produced them."

A paper about self-verification in code generation is evidence about code
generation. Counting it as evidence about research automation inflates the
denominator with sources the claim never addressed.

**It is a judgement and it is not machine-derived.** An earlier pass used a
keyword test over titles and got it wrong: it missed "Towards Verifiable and
Self-Correcting AI Physicists" because that title contains neither "science"
nor "research", and that case is the single `supports` in the whole set — so
the keyword version reported the exact opposite of the truth about the one
case that carries the most weight. The list is written out case by case, with
the reason, so a reader can disagree with any single line without having to
re-derive the whole thing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

# CORRECTION 2026-08-04 — READ THIS BEFORE REGENERATING data.json.
#
# This dict was re-made from scratch, blind, by two independent readers on 2026-08-04
# under a rule committed before either saw a case. Both returned 23 sources, not the 39
# below. They agreed with each other at Cohen's kappa 0.96 and with this dict at 0.54 and
# 0.70, and NEITHER of them added a single source this dict excludes -- 0 cases moved from
# excluded to included under either reader, which is the load-bearing fact. (Corrected the
# same day by this correction's own Verifier, F1: an earlier draft of this note said all 21
# exclusions were confirmed *unanimously*, which is false. Twenty were; position 52 drew
# UNDECIDABLE from R1 and OUT from R2.) Every disagreement is this dict including something
# an independent reader would not.
#
# The entries below are DELIBERATELY UNCHANGED. They are what was published, this work's
# figures are computed from them, and the second-reader study's own rule (§9) fixes that
# no reader is ground truth. Regenerating data.json from this file therefore reproduces
# the published split — which is correct, and is also why `apply_second_reader.py` must
# be re-run afterwards, or the regenerated file will carry the unreproduced split with
# nothing attached to it.
#
# The readers' verdicts, per case, with their reasons: second-reader-2026-08-04.json.
# What the figures become under each split: CORRECTIONS.md, entry 2026-08-04.
#
# Position in the gold set (1-based) -> why this source is IN the claim's
# population. Read from title and excerpt, one line each, so any single line
# can be contested on its own.
POPULATION: dict[int, str] = {
    3: "benchmark for an AI agent doing biomedical knowledge-graph checking — a research task",
    5: "The AI Scientist: idea, code, experiment, paper, review",
    6: "LLM ideation agent measured against 100+ NLP researchers",
    7: "automated machine-learning research",
    11: "scaling laws for AI and robot scientists",
    13: "agents evaluated in realistic scientific workflows",
    14: "LLM evolutionary algorithm generating optimisation algorithms — automated method design",
    15: "survey of hypothesis discovery and rule learning",
    17: "autonomous discovery and annotation",
    21: "hypothesis-driven discovery with LLMs and knowledge graphs",
    22: "retrosynthesis planning — chemistry research",
    23: "open-access ecosystem for AI-generated science",
    24: "physics-informed symbolic regression — scientific model discovery",
    25: "benchmark for deep research agents",
    27: "Jr. AI Scientist, autonomous scientific exploration",
    28: "evaluation of the autonomous AI scientist KOSMOS in radiation biology",
    32: "automating peer review",
    34: "four autonomous research attempts and why they failed",
    35: "benchmark for multimodal deep research agents",
    39: "triggering innovative capability — research ideation",
    40: "multi-agent automated design exploration on HPC",
    41: "verifiable evaluation suite for deep research agents",
    42: "scientific reasoning steps for molecule optimisation",
    43: "verifiable and self-correcting AI physicists for quantum many-body simulation",
    44: "automated peer review by reinforcement learning",
    45: "AI co-historian — a research assistant in a discipline",
    46: "EvoMaster, a framework for agentic science at scale",
    47: "benchmark for expert-level medical evidence integration",
    48: "audit framework for medical research agent skills",
    49: "toolkit for biomedical deep research agents",
    51: "benchmark for LLM peer reviewers",
    53: "benchmark for end-to-end autonomous scientific research",
    54: "collective intelligence of AI agents for new discoveries",
    55: "unique identifiers for AI scientists",
    56: "rethinking scientific discovery in the agentic era",
    57: "auditable AI scientists, hypothesis evolution protocol",
    58: "graph-augmented evolution for scientific discovery",
    59: "reviewer guideline design for automated peer review",
    60: "a new scientific paradigm for trustworthy science under AI agents",
}


# Position -> why this source is OUTSIDE the claim's population. Written out for
# the same reason the inclusions are: a reader who disputes an exclusion should
# be able to dispute that one line, not reconstruct the whole judgement. Added
# after the Skeptic's S4 recorded their absence as owed.
EXCLUDED: dict[int, str] = {
    1: "adversarial pre-training for logical reasoning — reasoning capability, no research cycle",
    2: "benchmark for verifiers of chain-of-thought — reasoning verification, not research",
    4: "claim verification through fact detection — fact-checking, not research automation",
    8: "long-horizon robotic planning",
    9: "formalising logical reasoning tasks with theorem provers",
    10: "self-rewarding correction on mathematical reasoning",
    12: "multi-agent framework for disruption-aware planning — operations, not research",
    16: "world modelling for language-model agents in general",
    18: "LLM-as-a-judge for code validation and refinement",
    19: "self-evolving code agents, measured on a code benchmark",
    20: "repairing language-model pipelines at runtime — engineering, not research",
    26: "cross-platform computer-use agents",
    29: "self-training and continual learning as capability growth",
    30: "hallucination versus creativity in LLMs — a property study, no research system",
    31: "negotiation tactics in Diplomacy",
    33: "decomposing self-correction on grade-school word problems",
    36: "reliability of LLM-as-a-judge via item response theory — judging in general",
    37: "how context errors affect LLM reasoning",
    38: "stylistic evaluation of Chinese legalese",
    50: "topology optimisation — engineering design, not a research cycle",
    52: "an information-theoretic study using AlphaFold2 representations: science done WITH a model, not a system automating research",
}


def sha256_of(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def build(runtime: Path) -> dict:
    gold_path = runtime / "corpora/gold-classification/mb-cls-ulysses-v1-restamped.json"
    manifest_path = runtime / "corpora/gold-classification/citations.manifest.json"
    predictions_path = (
        runtime / "corpora/gold-classification/predictions-gemini-3.5-flash-lite.json"
    )
    criteria_path = runtime / "benchmarks/meridianbench/fixtures/mb-cls-criteria.v3.json"

    gold = json.loads(gold_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    predictions = json.loads(predictions_path.read_text(encoding="utf-8"))
    criteria = json.loads(criteria_path.read_text(encoding="utf-8"))

    titles = {
        c["citation_id"]: (c.get("claimed_title") or c.get("cited_as") or "")
        for c in manifest["citations"]
    }
    machine = predictions["predictions"]
    machine_rationale = {p["case_id"]: p for p in predictions["proposals"]}

    cases = []
    for position, case in enumerate(gold["cases"], start=1):
        case_id = case["case_id"]
        proposal = machine_rationale.get(case_id, {})
        cases.append(
            {
                "position": position,
                "case_id": case_id,
                "arxiv": case["source_identifiers"].get("repository_id"),
                "title": titles.get(case_id, ""),
                "excerpt": case["excerpt"],
                "excerpt_sha256": case["excerpt_sha256"],
                "in_population": position in POPULATION,
                "population_reason": POPULATION.get(position) or EXCLUDED.get(position),
                "exclusion_reason": EXCLUDED.get(position),
                "gold": {
                    "relation": case["expected_relation"],
                    "rationale": case["expected_rationale"],
                    "decided_by": case["decided_by"],
                    "tie_with": case["tie_with"],
                    "undecidable": bool(case.get("undecidable")),
                    "undecidable_reason": case.get("undecidable_reason"),
                },
                "machine": {
                    "relation": machine.get(case_id),
                    "rationale": proposal.get("rationale"),
                    "decided_by": proposal.get("decided_by"),
                    "tie_with": proposal.get("tie_with"),
                    "undecidable": bool(proposal.get("undecidable")),
                },
            }
        )

    return {
        "_note": (
            "Sixty arXiv abstracts, labelled blind by a sibling practice against criteria "
            "locked before the labelling, and classified again by a machine reader under the "
            "same criteria with no access to the labels. Built deterministically by "
            "build_data.py from four committed files in the meridian-runtime repository; the "
            "one judgement added here is `in_population`, which is hand-read and reasoned "
            "case by case in that script."
        ),
        "claim": gold["cases"][0]["claim_text"],
        "criteria": {
            "version": gold["criteria_version"],
            "locked_at": gold["criteria_locked_at"],
            "definitions": {
                k: v for k, v in criteria.items() if k in
                ("supports", "contradicts", "qualifies", "contextualizes")
            },
        },
        "sources": {
            "gold_set": {"path": str(gold_path.relative_to(runtime)), "sha256": sha256_of(gold_path)},
            "manifest": {"path": str(manifest_path.relative_to(runtime)), "sha256": sha256_of(manifest_path)},
            "predictions": {
                "path": str(predictions_path.relative_to(runtime)),
                "sha256": sha256_of(predictions_path),
                "system_id": predictions["system_id"],
                "model_name": predictions["model_name"],
            },
            "criteria_file": {
                "path": str(criteria_path.relative_to(runtime)),
                "sha256": sha256_of(criteria_path),
            },
        },
        "labelling": {
            "practice": gold["label_provenance"]["producing_practice"],
            "blind": True,
            "labelled_at": gold["labelled_at"],
            "account": gold["label_provenance"]["account"],
        },
        "cases": cases,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    document = build(args.runtime.resolve())
    args.out.write_text(
        json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"{args.out}: {len(document['cases'])} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
