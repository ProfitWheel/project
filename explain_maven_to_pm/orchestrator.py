"""Minimal orchestration engine that simulates Maven's Planned flow."""
from __future__ import annotations

from typing import Iterable

from agents import PlannerAgent, ResearchAgent
from memory import MemoryStore
from primitives import PlanStep, SubTaskResult, TaskSummary


class TaskOrchestrator:
    """Coordinates the lifecycle of a Planned task."""

    def __init__(self, memory: MemoryStore) -> None:
        self.memory = memory
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent()

    def run_task(self, title: str, description: str, estimated_steps: int) -> TaskSummary:
        """High-level entry point used by the sample notebook/tests."""
        mode = self._select_mode(estimated_steps)
        if mode == "investigative":
            raise ValueError("This sandbox only covers planned tasks")

        plan = self.planner.create_plan(title=title, description=description, steps=estimated_steps)
        self.memory.store_plan(title, plan)

        approved = self._await_plan_approval(plan)
        if not approved:
            raise RuntimeError("Plan rejected")

        results = list(self._execute_plan(title, plan))
        summary = self._summarise(title, description, results)
        self.memory.store_summary(title, summary)
        return summary

    def _select_mode(self, estimated_steps: int) -> str:
        if estimated_steps >= 3:
            return "planned"
        return "investigative"

    def _await_plan_approval(self, plan: list[PlanStep]) -> bool:
        """Simulate a human-in-the-loop approval check."""
        return True

    def _execute_plan(self, task_title: str, plan: list[PlanStep]) -> Iterable[SubTaskResult]:
        for step in plan:
            result = self.researcher.execute(step.description)
            event = SubTaskResult(
                agent=step.agent,
                output=result,
                started_at=self.memory.now(),
                completed_at=self.memory.now(),
            )
            self.memory.store_event(task_title, step.description, event)
            yield event

    def _summarise(
        self,
        title: str,
        description: str,
        results: list[SubTaskResult],
    ) -> TaskSummary:
        highlights = " ".join(result.output for result in results)
        callouts = ["Verify pricing with finance", "Prepare customer-facing update"]
        return TaskSummary(
            short_answer=f"Completed {title}",
            detailed_answer=f"{description}. Key findings: {highlights}",
            next_steps=callouts,
        )
