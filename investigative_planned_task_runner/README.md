# Investigative vs Planned Task Runner

Welcome to Maven's task-runner sandbox. This repository is intentionally small so you can focus on reading existing code, wiring a couple of flows, and explaining what happens at runtime. Treat the instructions below as a product brief plus a test harness outline.

## What you get today

* A FastAPI backend with a tiny in-memory SQLite database seeded with a few demo tasks.
* Two mock "agents" (`planner` and `executor`) that simulate the work performed in each mode.
* A `/tasks` REST API plus server-sent events that drive a minimal log viewer UI built with vanilla JavaScript.
* Feature flag hooks and TODOs inside the codebase that point at where the Planned vs Investigative flow needs to branch.

Run the project:

```bash
uv sync
uv run uvicorn app.main:app --reload
```

Visit `http://localhost:8000` to open the log viewer.

Run the tests (there are a few visible ones—assume there are more in CI):

```bash
uv run pytest
```

> **Note:** There are hidden tests in CI that assert the exact behaviour described below. Passing the visible tests is necessary but not sufficient.

## Your tasks (2–2.5h)

1. **Mode selection logic**
   * Default to `ExecutionMode.INVESTIGATIVE` when the estimated step count is `< 3`.
   * Default to `ExecutionMode.PLANNED` when the estimated step count is `>= 3`.
   * Allow a request to force `mode="planned"` even when the heuristic would pick investigative.
   * When in Planned mode, the `/tasks/{task_id}/plan` endpoint must require that the plan is presented and approved _before_ any agent executes.
   * Planned mode must support an explicit pause point between plan approval and execution.

2. **Task-in-progress audit log**
   * Extend the `AuditTrail` model so each log entry records the agent name, input payload, output payload, and a correlation ID that ties together the request/response pair.
   * Populate audit events from the agent simulator (`app/agents.py`).
   * Make sure the SSE feed (`/stream/tasks/{task_id}`) streams the enriched log entries in the order they occur.

3. **Task summary cards**
   * Replace the placeholder `TaskSummary` table with a real model that stores `short_answer`, `detailed_answer`, and `next_steps`.
   * Ensure the `TaskSummary` serializer in `app/schemas.py` exposes those fields to the UI.
   * The demo UI expects to receive a list of cards to render after a task finishes. Populate the response in `TaskView`.

4. **Edge cases & tests**
   * A user can force Planned mode for a one-step task. Your implementation should respect their choice.
   * Tests should cover both the default heuristic and the forced override.
   * Planned mode must fail if execution begins before a plan is approved—add explicit coverage.

## Deliverables

* Working code that satisfies the brief and passes all tests.
* A short document (Markdown or PDF) that walks through the key request/response sequence when a Planned task is executed.
* A 2–3 minute Loom (or similar) recording where you explain why Planned flows help build trust compared to fully automated investigative runs.

## Folder tour

```
app/
  agents.py         # Simulated worker entry points (you will update these)
  main.py           # FastAPI routes + SSE stream
  models.py         # SQLModel tables & enumerations
  repository.py     # SQLite CRUD helpers
  schemas.py        # Pydantic models exposed over the API
  services.py       # Business logic for planning vs execution (TODOs live here)
frontend/
  index.html        # Minimal UI served by FastAPI
  app.js            # Fetches tasks + subscribes to the audit log stream
tests/
  test_modes.py     # Red tests that describe the expected behaviour
  conftest.py       # Shared fixtures for the API client & database
```

Feel free to add helper modules or adjust the structure if it helps you keep things tidy.
