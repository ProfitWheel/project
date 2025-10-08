"""Toy agent implementations that mimic Maven workers."""
from __future__ import annotations

from dataclasses import dataclass

from primitives import PlanStep


@dataclass
class PlannerAgent:
    name: str = "planner"

    def create_plan(self, title: str, description: str, steps: int) -> list[PlanStep]:
        """Return a deterministic plan so the candidate can follow the flow."""
        outline = [
            "Clarify objectives",
            "Collect supporting data",
            "Synthesize insights",
            "Draft recommendations",
        ]
        selected = outline[: max(steps, 1)]
        return [PlanStep(description=item, agent=self.name) for item in selected]


@dataclass
class ResearchAgent:
    name: str = "researcher"

    def execute(self, instruction: str) -> str:
        """Pretend to run a subtask and return a canned response."""
        responses = {
            "Clarify objectives": "Objective confirmed with PM and Sales",
            "Collect supporting data": "Gathered metrics from last quarter",
            "Synthesize insights": "Identified churn drivers in segment B",
            "Draft recommendations": "Suggested pricing experiment for Enterprise tier",
        }
        return responses.get(instruction, f"Completed: {instruction}")
