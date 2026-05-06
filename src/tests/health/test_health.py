"""Endpoint raíz `/health` (sin tag de grupo en OpenAPI)."""

from fastapi.testclient import TestClient


def test_health_ok(client: TestClient) -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}
