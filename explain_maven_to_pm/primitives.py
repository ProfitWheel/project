"""Shared dataclasses used across the comprehension repo."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class PlanStep:
    description: str
    agent: str


@dataclass
class SubTaskResult:
    agent: str
    output: str
    started_at: datetime
    completed_at: datetime


@dataclass
class TaskSummary:
    short_answer: str
    detailed_answer: str
    next_steps: List[str]
