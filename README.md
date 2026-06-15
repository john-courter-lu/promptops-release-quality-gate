# promptops-release-quality-gate

A **PromptOps release quality gate**: a small, dependency-light tool that treats prompts
like releaseable software assets. It versions prompts, runs them against golden / edge /
compliance test cases, scores the results, flags risks (missing sections, banned phrases,
overconfident wording, weak source grounding, compliance-sensitive items), and produces a
**release recommendation** — *approve*, *approve with review*, or *block* — before a prompt
change ships.

> **Portfolio demo, not a production product.** This repo runs entirely on synthetic data and
> pre-saved sample outputs. It does **not** call live LLM APIs and makes **no** real
> deployment claims. All sample content is fictional and contains no legal, tax, financial,
> audit, or investment advice. The goal is to demonstrate *process and QA discipline applied
> to prompt engineering*.

---

## What "PromptOps" means in this repo

PromptOps here is the practice of applying software release discipline to prompts:

- **Version control** — every prompt has a `v1` (baseline) and `v2` (release candidate).
- **Specification** — each prompt carries machine-readable metadata describing what a "good"
  output must contain and must avoid.
- **Regression testing** — prompts are exercised against a fixed suite of golden, edge, and
  compliance test cases with saved sample outputs.
- **Scoring** — each output is graded `pass` / `warning` / `fail` against the spec.
- **Gating** — a release recommendation is computed; failures block, compliance items require
  human review.
- **Reporting** — a human-readable release report documents the decision and rollback criteria.

## Why prompt changes need release gates

Prompts are code-like artifacts: a small wording change can silently regress output quality,
introduce hallucinations, drop a required section, or produce overconfident claims in a
compliance-sensitive context. Without a gate, those regressions ship to users. A quality gate
makes prompt changes **testable, reviewable, and reversible** — the same guarantees we expect
from application code.

## How this maps to AI Prompt & Skills Engineering

- Prompt **versioning and change management** (`prompts/v1` → `prompts/v2`, change log).
- **Prompt QA**: regression suites, output validation, hallucination-risk flagging.
- **Compliance-minded review**: compliance-sensitive prompts always route to a human.
- **Production-readiness thinking**: explicit release criteria, rollback criteria, reviewer
  checklist, known failure modes — packaged as a knowledge base under `docs/`.

## How this maps to SDET / QA automation skills

- **Test design**: golden / edge / negative (compliance) case taxonomy.
- **Deterministic, isolated assertions**: validators are pure functions, unit-tested with pytest.
- **Build–test–deploy discipline**: a CLI quality gate plus a GitHub Actions CI check.
- **Defect triage & reporting**: severity levels (`pass`/`warning`/`fail`), top failure modes,
  and an auditable release report.
- **Release validation & rollback**: documented criteria for approving or rolling back a change.

---

## Repository structure

```
promptops-release-quality-gate/
├── prompts/                  # prompt text under version control
│   ├── v1/                   #   baseline versions
│   └── v2/                   #   release candidate versions
├── prompt_metadata/          # per-prompt rules: required sections, banned phrases, etc. (YAML)
├── test_cases/               # golden / edge / compliance cases (JSON)
├── sample_outputs/           # pre-saved outputs per version (no live LLM calls)
│   ├── v1/
│   └── v2/
├── release_reports/          # generated markdown release reports
├── src/                      # CLI + quality gate / validators / scorecard / report writer
├── docs/                     # knowledge base: process, rollback, reviewer checklist, ...
├── tests/                    # pytest unit tests
├── .github/workflows/        # CI (runs the tests)
├── requirements.txt
└── README.md
```

**Naming convention (the glue):** a test case with `case_id: client_summary_golden_01` is
graded against the sample output at `sample_outputs/<version>/client_summary_golden_01.md`.
This 1:1 mapping makes "missing output" a trivial, deterministic check.

---

## Installation

```bash
python -m venv .venv && source .venv/bin/activate   # optional
python -m pip install -r requirements.txt
```

## Running the quality gate (CLI)

> The CLI is implemented in a later phase (Day 6–7). Documented here so the intended interface
> is clear from the start.

```bash
# Run the gate against a prompt version and print a readable scorecard
python -m src.cli run --version v2

# Generate a markdown release report for a version
python -m src.cli report --version v2
# -> writes release_reports/release_candidate_v2.md
```

## How to add a new prompt

> Detailed walkthrough lands once the data formats are finalized (Day 2–5).

1. Add `prompts/v1/<prompt_id>.md` (and `prompts/v2/<prompt_id>.md` for a candidate).
2. Add `prompt_metadata/<prompt_id>.yaml` describing required sections, banned phrases,
   certainty terms, grounding rule, and whether it is compliance-sensitive.
3. Add test cases referencing the `prompt_id` in `test_cases/*.json`.
4. Add the matching sample outputs under `sample_outputs/<version>/<case_id>.md`.
5. Run `python -m src.cli run --version <version>`.

## How to interpret a release report

> Expanded once the scorecard logic exists (Day 6–8). A report will summarize prompts tested,
> `pass`/`warning`/`fail` counts, the top failure modes, required human-review items, the
> overall release recommendation, and the rollback criteria.

---

## Limitations & future improvements

- **No live LLM calls.** Outputs are pre-saved samples; the tool validates *process and
  artifacts*, not live model behavior. A natural extension is an adapter that calls a model
  API and writes outputs into `sample_outputs/`.
- **Heuristic checks.** Grounding / hallucination-risk and certainty checks are keyword-based
  heuristics for demonstration, not statistical evaluators.
- **Synthetic data only.** All prompts, cases, and outputs are fictional.
- **Possible extensions:** semantic similarity scoring, diff-based regression between versions,
  richer reviewer routing, and HTML report output.

---

*Author: John Lu — SDET / QA Automation Engineer. Built to demonstrate release-quality
discipline applied to prompt engineering.*
