"""PromptOps release quality gate package.

Modules are added in later phases:
    validators.py     - pure check functions (required sections, banned phrases, grounding, ...)
    quality_gate.py   - orchestrator that loads prompts/metadata/cases and runs the checks
    scorecard.py      - aggregation + release recommendation logic
    report_writer.py  - renders the markdown release report
    cli.py            - `python -m src.cli run|report --version <vN>`
"""
