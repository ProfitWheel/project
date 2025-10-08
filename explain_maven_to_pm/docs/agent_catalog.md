# Agent Catalog

| Agent | Responsibilities | Notes |
| ----- | ---------------- | ----- |
| Planner | Breaks a user request into discrete plan steps. | Produces machine-readable plans; humans approve before execution. |
| Researcher | Executes plan steps that require data gathering or synthesis. | Can run subtasks in parallel in the real system; serialized here for clarity. |
| Summariser | (Implicit in the orchestrator) combines plan outputs into short answers, detailed answers, and next steps. | In production this is a dedicated agent; in the sandbox it lives inside `TaskOrchestrator._summarise`. |

Missing pieces in this sandbox:

* Feedback collector agents that solicit user satisfaction scores.
* Guardrail agents that enforce compliance constraints.
* Cost control agents that track spend per task.
