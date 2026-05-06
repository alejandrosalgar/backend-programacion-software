"""Tests HTTP alineados con el tag OpenAPI `categorias` (prefijo `/categorias`)."""

import uuid

from fastapi.testclient import TestClient


def test_listar_categorias(client: TestClient) -> None:
    res = client.get("/categorias/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_obtener_categoria_inexistente_404(client: TestClient) -> None:
    res = client.get(f"/categorias/{uuid.uuid4()}")
    assert res.status_code == 404
