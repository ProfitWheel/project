"""Data access helpers for the task runner sandbox."""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator

from sqlmodel import Session, SQLModel, create_engine, select

from .models import AuditTrail, Task, TaskSummary

_DB_PATH = Path("task_runner.db")
ENGINE = create_engine(f"sqlite:///{_DB_PATH}", echo=False, connect_args={"check_same_thread": False})


def init_db() -> None:
    """Create tables and seed demo data."""
    SQLModel.metadata.create_all(ENGINE)
    with session_scope() as session:
        if session.exec(select(Task)).first():
            return
        demo_tasks = [
            Task(title="Research competitor pricing", description="Look up pricing tiers", estimated_steps=4),
            Task(
                title="Draft FAQ update",
                description="Investigate customer complaints and produce FAQ entries",
                estimated_steps=2,
            ),
            Task(
                title="Summarise call transcript",
                description="Parse transcripts and produce highlights",
                estimated_steps=5,
                forced_mode=None,
            ),
        ]
        session.add_all(demo_tasks)
        session.commit()


@contextmanager
def session_scope() -> Iterator[Session]:
    session = Session(ENGINE)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class TaskRepository:
    """Thin repository that isolates DB-specific code from service logic."""

    def __init__(self, session: Session):
        self.session = session

    def list_tasks(self) -> Iterable[Task]:
        return self.session.exec(select(Task)).all()

    def get(self, task_id: int) -> Task:
        return self.session.get(Task, task_id)

    def save(self, task: Task) -> Task:
        self.session.add(task)
        self.session.flush()
        return task

    def log_event(self, event: AuditTrail) -> AuditTrail:
        self.session.add(event)
        self.session.flush()
        return event

    def upsert_summary(self, summary: TaskSummary) -> TaskSummary:
        self.session.add(summary)
        self.session.flush()
        return summary
