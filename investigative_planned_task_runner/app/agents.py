"""Mock agents used by the sandbox."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .models import Task


@dataclass
class AgentResponse:
    agent: str
    output: str


class PlannerAgent:
    name = "planner"

    def run(self, task: Task) -> AgentResponse:
        """Pretend to create a multi-step plan for a task."""
        steps = [f"Step {i+1}" for i in range(max(1, task.estimated_steps))]
        plan_text = " -> ".join(steps)
        return AgentResponse(agent=self.name, output=f"Plan: {plan_text}")


class ExecutorAgent:
    name = "executor"

    def run(self, task: Task, plan: str | None = None) -> AgentResponse:
        """Pretend to execute the plan or improvise if none was provided."""
        if plan:
            result = f"Executed plan for task {task.id}: {plan}"
        else:
            result = f"Investigated task {task.id} without plan"
        return AgentResponse(agent=self.name, output=result)


def run_agent(agent_name: str, task: Task, *, plan: str | None = None) -> AgentResponse:
    """Dispatch helper used by the service layer."""
    agents: Dict[str, Any] = {
        PlannerAgent.name: PlannerAgent(),
        ExecutorAgent.name: ExecutorAgent(),
    }
    return agents[agent_name].run(task, plan=plan)  # type: ignore[arg-type]
