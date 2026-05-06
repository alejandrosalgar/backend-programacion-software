import os

# Debe ejecutarse antes de importar `src.database.config` / la app.
os.environ["TESTING"] = "1"

import pytest
from fastapi.testclient import TestClient

from src.api.app import app


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as c:
        yield c
