# Planned vs Investigative

| Mode | When it triggers | Human touchpoints | Observability |
| ---- | ---------------- | ----------------- | ------------- |
| Investigative | Small or ambiguous tasks (<= 2 steps). | Optional pause; humans mostly inspect outputs after the fact. | Lightweight logs summarising the agent's exploration. |
| Planned | Multi-step tasks (>= 3 steps), regulated workflows, or when a user explicitly requests extra oversight. | Mandatory plan presentation + approval before execution. Optional pause after approval. | Full audit log including agent inputs, outputs, and status transitions. |

Why the distinction matters:

* Planned tasks build trust by exposing the plan ahead of time, letting stakeholders redirect effort before expensive work starts.
* Investigative tasks keep the system nimble for quick-turnaround questions.
* Both modes produce summaries, but only Planned tasks guarantee a pre-execution plan and correlation IDs across logs.
