# Architecture Overview

The miniature Maven orchestrator mirrors three high-level layers that exist in production:

1. **Intake & Mode Selection** – The orchestrator inspects the requested task and decides whether to run it in Investigative or Planned mode. In this sandbox the cut-off is `estimated_steps >= 3`.
2. **Plan Creation & Approval** – Planned tasks trigger the planner agent, which proposes a sequence of subtasks. Human stakeholders approve or reject the plan before any execution happens.
3. **Execution & Summarisation** – After approval, executor agents pick up each plan step, produce outputs, and feed them into a summariser that crafts an answer plus next steps.

Supporting capabilities:

* **Memory** keeps track of plans, intermediate agent outputs, and final summaries so the orchestrator can reason about previous work.
* **Observability** (omitted from this toy repo) normally emits task-level events and audit logs for humans to follow along.
