"""Tests HTTP alineados con el tag OpenAPI `detalles-pedido` (prefijo `/detalles-pedido`)."""

import uuid

from fastapi.testclient import TestClient


def test_listar_detalles_pedido(client: TestClient) -> None:
    res = client.get("/detalles-pedido/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_obtener_detalle_inexistente_404(client: TestClient) -> None:
    res = client.get(f"/detalles-pedido/{uuid.uuid4()}")
    assert res.status_code == 404
