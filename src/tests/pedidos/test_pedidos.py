"""Tests HTTP alineados con el tag OpenAPI `pedidos` (prefijo `/pedidos`)."""

import uuid

from fastapi.testclient import TestClient


def test_listar_pedidos(client: TestClient) -> None:
    res = client.get("/pedidos/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_obtener_pedido_inexistente_404(client: TestClient) -> None:
    res = client.get(f"/pedidos/{uuid.uuid4()}")
    assert res.status_code == 404
