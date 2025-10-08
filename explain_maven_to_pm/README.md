# Explain Maven to a New PM

This repo is intentionally read-only. You will not need to write any code—your job is to understand how this miniature “Maven” orchestrator works and then teach it back.

## What you get today

* A tiny orchestrator that simulates a Planned task flowing through planner and executor agents.
* Lightweight agent implementations that return deterministic responses.
* A stubbed memory module that stores conversation snippets.
* Architecture notes scattered across `docs/` that you will consolidate.

You are expected to:

1. Read through the code (`orchestrator.py`, `agents.py`, `memory.py`, and the docs).
2. Produce a **sequence diagram** that walks a Planned task through detection, plan presentation, approval, subtask execution, and summarisation.
3. Write a **one-page explainer** for a product manager that answers:
   * What roles the orchestrator and agents play.
   * How asynchronous execution and memory work together.
   * Why Maven differentiates between Planned and Investigative flows.
4. Identify **two risks** in the system and propose mitigations (e.g., guardrails, rate limits, retries, cost controls).

## Deliverables (2 hours recommended)

* Sequence diagram (`.mmd`, `.png`, or `.pdf`).
* 1-page explainer (`.md`, Google Doc link, etc.).
* Risk & mitigation write-up (can be part of the explainer).

## Reference material

* [`docs/architecture_overview.md`](docs/architecture_overview.md)
* [`docs/planned_vs_investigative.md`](docs/planned_vs_investigative.md)
* [`docs/agent_catalog.md`](docs/agent_catalog.md)

## Stretch goal (optional)

* Record a 2–3 minute Loom explaining the flow to a hypothetical PM stakeholder.

Happy reverse-engineering!
