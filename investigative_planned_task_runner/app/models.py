"""Database models for the task runner sandbox."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class ExecutionMode(str, Enum):
    """The two execution styles Maven supports."""

    INVESTIGATIVE = "investigative"
    PLANNED = "planned"


class Task(SQLModel, table=True):
    """A lightweight task that can be executed by agents."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    estimated_steps: int = Field(description="Candidate heuristic for how many steps this task will take")
    forced_mode: Optional[ExecutionMode] = Field(
        default=None, description="Optional override selected by the requestor"
    )
    mode: ExecutionMode = Field(
        default=ExecutionMode.INVESTIGATIVE,
        description="The mode the system will actually execute",
    )
    plan_presented_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of when the plan was shown to the user",
    )
    plan_approved_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of when the user approved the plan",
    )
    status: str = Field(default="pending")

    summary: Optional["TaskSummary"] = Relationship(back_populates="task")
    audit_trail: list["AuditTrail"] = Relationship(back_populates="task")


class TaskSummary(SQLModel, table=True):
    """Placeholder summary information for a task."""

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    # TODO: Replace these placeholders with real persisted summary fields.
    content: str = Field(default="TODO")

    task: Task = Relationship(back_populates="summary")


class AuditTrail(SQLModel, table=True):
    """Event log of what happened while executing a task."""

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    message: str
    level: str = Field(default="info")
    # TODO: Extend this model with agent metadata & payloads to support the audit view.

    task: Task = Relationship(back_populates="audit_trail")
