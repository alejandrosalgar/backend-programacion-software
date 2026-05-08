import os

# Debe ejecutarse antes de importar `src.database.config` / la app.
os.environ["TESTING"] = "1"

import pytest
from fastapi.testclient import TestClient

from sqlalchemy.orm import Session

from src.api.app import app
from src.database.config import SessionLocal


@pytest.fixture
def db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as c:
        yield c
