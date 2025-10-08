"""Tiny script that exercises the orchestrator."""
from __future__ import annotations

from memory import MemoryStore
from orchestrator import TaskOrchestrator


if __name__ == "__main__":
    orchestrator = TaskOrchestrator(memory=MemoryStore())
    summary = orchestrator.run_task(
        title="Competitive Pricing Review",
        description="Understand how competitors price premium tiers",
        estimated_steps=3,
    )
    print("Short answer:", summary.short_answer)
    print("Detailed answer:", summary.detailed_answer)
    print("Next steps:")
    for step in summary.next_steps:
        print("-", step)
