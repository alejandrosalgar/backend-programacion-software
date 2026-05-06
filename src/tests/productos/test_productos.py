"""Tests HTTP alineados con el tag OpenAPI `productos` (prefijo `/productos`)."""

import uuid

from fastapi.testclient import TestClient


def test_listar_productos(client: TestClient) -> None:
    res = client.get("/productos/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_obtener_producto_inexistente_404(client: TestClient) -> None:
    res = client.get(f"/productos/{uuid.uuid4()}")
    assert res.status_code == 404
