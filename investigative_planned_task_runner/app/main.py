"""Entry point for the FastAPI app."""
from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse

from .models import Task
from .repository import TaskRepository, init_db, session_scope
from .schemas import AuditLogEntry, CreateTaskRequest, PlanApprovalRequest, TaskSummaryView, TaskView
from .services import TaskService

app = FastAPI(title="Investigative vs Planned Task Runner")


@asynccontextmanager
def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app.router.lifespan_context = lifespan
app.mount("/static", StaticFiles(directory="frontend"), name="static")


def get_repo() -> TaskRepository:
    with session_scope() as session:
        yield TaskRepository(session)


def get_service(repo: TaskRepository = Depends(get_repo)) -> TaskService:
    return TaskService(repo)


@app.get("/")
def home() -> FileResponse:
    return FileResponse("frontend/index.html")


@app.get("/tasks", response_model=list[TaskView])
def list_tasks(service: TaskService = Depends(get_service)) -> list[TaskView]:
    tasks = service.repo.list_tasks()
    return [_serialize_task(task) for task in tasks]


@app.post("/tasks", response_model=TaskView, status_code=201)
def create_task(
    request: CreateTaskRequest,
    service: TaskService = Depends(get_service),
) -> TaskView:
    task = Task(
        title=request.title,
        description=request.description,
        estimated_steps=request.estimated_steps,
        forced_mode=request.forced_mode,
    )
    service.repo.save(task)
    service.select_mode(task)
    return _serialize_task(task)


@app.post("/tasks/{task_id}/plan", response_model=AuditLogEntry)
def present_plan(task_id: int, service: TaskService = Depends(get_service)) -> AuditLogEntry:
    task = service.repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    event = service.generate_plan(task)
    return _serialize_event(event)


@app.post("/tasks/{task_id}/plan/approval", response_model=TaskView)
def approve_plan(
    task_id: int,
    payload: PlanApprovalRequest,
    service: TaskService = Depends(get_service),
) -> TaskView:
    if not payload.approved:
        raise HTTPException(status_code=400, detail="Only approvals are supported in this sandbox")
    task = service.repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = service.approve_plan(task)
    return _serialize_task(updated)


@app.post("/tasks/{task_id}/execute", response_model=TaskView)
def execute_task(task_id: int, service: TaskService = Depends(get_service)) -> TaskView:
    task = service.repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    result = service.execute(task)
    # TODO: capture the resulting audit events + summary cards once implemented.
    return _serialize_task(result.task)


@app.get("/stream/tasks/{task_id}")
async def stream_task(task_id: int, service: TaskService = Depends(get_service)) -> Response:
    task = service.repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    async def event_generator() -> AsyncIterator[dict]:
        # This naive generator polls every second; feel free to replace it with DB triggers or push notifications.
        last_id = None
        while True:
            events = [e for e in task.audit_trail if last_id is None or e.id > last_id]
            for event in events:
                last_id = event.id
                payload = _serialize_event(event)
                # TODO: include agent payloads once stored in the model.
                yield {"event": "audit", "data": payload.json()}
            await asyncio.sleep(1)

    return EventSourceResponse(event_generator())


def _serialize_task(task: Task) -> TaskView:
    summary = task.summary
    return TaskView(
        id=task.id,
        title=task.title,
        description=task.description,
        estimated_steps=task.estimated_steps,
        mode=task.mode,
        status=task.status,
        forced_mode=task.forced_mode,
        plan_presented_at=task.plan_presented_at,
        plan_approved_at=task.plan_approved_at,
        summary=None if not summary else TaskSummaryView(id=summary.id, content=summary.content),
    )


def _serialize_event(event) -> AuditLogEntry:  # type: ignore[no-untyped-def]
    return AuditLogEntry(
        id=event.id,
        created_at=event.created_at,
        message=event.message,
        level=event.level,
    )
