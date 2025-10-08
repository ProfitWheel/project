from __future__ import annotations

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repository import _DB_PATH, init_db


@pytest.fixture(autouse=True)
def reset_db() -> Generator[None, None, None]:
    if _DB_PATH.exists():
        os.remove(_DB_PATH)
    init_db()
    yield
    if _DB_PATH.exists():
        os.remove(_DB_PATH)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
