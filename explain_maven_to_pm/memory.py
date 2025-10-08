"""Simplified memory store for the comprehension exercise."""
from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List

from primitives import PlanStep, SubTaskResult, TaskSummary


@dataclass
class MemoryStore:
    """Records plans, execution events, and summaries."""

    plans: Dict[str, list[PlanStep]] = field(default_factory=dict)
    events: Dict[str, list[SubTaskResult]] = field(default_factory=dict)
    summaries: Dict[str, TaskSummary] = field(default_factory=dict)

    def store_plan(self, task_title: str, plan: list[PlanStep]) -> None:
        self.plans[task_title] = plan

    def store_event(self, task_title: str, description: str, result: SubTaskResult) -> None:
        self.events.setdefault(task_title, []).append(result)

    def store_summary(self, task_title: str, summary: TaskSummary) -> None:
        self.summaries[task_title] = summary

    def history(self, task_title: str) -> List[str]:
        """Return a flattened view of everything that happened for a task."""
        plan = self.plans.get(task_title, [])
        events = self.events.get(task_title, [])
        summary = self.summaries.get(task_title)
        lines = [f"Plan: {step.description}" for step in plan]
        lines.extend(f"Result: {event.output}" for event in events)
        if summary:
            lines.append(f"Summary: {summary.short_answer}")
        return lines

    @staticmethod
    def now() -> datetime:
        """Expose a timestamp helper so the orchestrator doesn't import datetime directly."""
        return datetime.utcnow()
