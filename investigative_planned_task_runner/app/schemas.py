"""API schemas exposed by the FastAPI application."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .models import ExecutionMode


class AuditLogEntry(BaseModel):
    id: int
    created_at: datetime
    message: str
    level: str
    # TODO: expose agent metadata once stored in the database.


class TaskSummaryView(BaseModel):
    id: int
    content: str  # TODO: replace with structured summary fields


class TaskView(BaseModel):
    id: int
    title: str
    description: str
    estimated_steps: int
    mode: ExecutionMode
    status: str
    forced_mode: Optional[ExecutionMode]
    plan_presented_at: Optional[datetime]
    plan_approved_at: Optional[datetime]
    summary: Optional[TaskSummaryView]


class CreateTaskRequest(BaseModel):
    title: str
    description: str
    estimated_steps: int
    forced_mode: Optional[ExecutionMode] = None


class PlanApprovalRequest(BaseModel):
    approved: bool
