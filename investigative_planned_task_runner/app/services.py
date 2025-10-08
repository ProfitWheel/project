"""Business logic for task execution."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from fastapi import HTTPException

from . import agents
from .models import AuditTrail, ExecutionMode, Task
from .repository import TaskRepository


@dataclass
class ExecutionResult:
    task: Task
    events: Iterable[AuditTrail]


class TaskService:
    """Coordinates the flow between planner and executor agents."""

    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def select_mode(self, task: Task) -> ExecutionMode:
        """Determine which execution mode should run for the given task."""
        if task.forced_mode:
            task.mode = task.forced_mode
            return task.mode

        # TODO: Replace this placeholder with the heuristic described in the brief.
        task.mode = ExecutionMode.INVESTIGATIVE
        return task.mode

    def generate_plan(self, task: Task) -> AuditTrail:
        """Call the planner agent and store an audit event."""
        if task.mode == ExecutionMode.INVESTIGATIVE:
            raise HTTPException(status_code=400, detail="Investigative tasks do not require a plan")

        planner_result = agents.run_agent(agents.PlannerAgent.name, task)
        event = AuditTrail(task_id=task.id, message=planner_result.output, level="info")
        # TODO: enrich with agent metadata + payloads once the model is extended.
        self.repo.log_event(event)
        task.plan_presented_at = datetime.utcnow()
        self.repo.save(task)
        return event

    def approve_plan(self, task: Task) -> Task:
        if task.mode != ExecutionMode.PLANNED:
            raise HTTPException(status_code=400, detail="Only planned tasks can be approved")
        task.plan_approved_at = datetime.utcnow()
        return self.repo.save(task)

    def execute(self, task: Task) -> ExecutionResult:
        """Execute the task using the appropriate agent(s)."""
        mode = self.select_mode(task)
        if mode == ExecutionMode.PLANNED and not task.plan_approved_at:
            # TODO: Block execution until a plan is approved.
            pass

        result = agents.run_agent(agents.ExecutorAgent.name, task)
        event = AuditTrail(task_id=task.id, message=result.output, level="info")
        self.repo.log_event(event)
        task.status = "complete"
        self.repo.save(task)
        return ExecutionResult(task=task, events=[event])
