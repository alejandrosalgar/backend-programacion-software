"""Tests HTTP alineados con el tag OpenAPI `pagos` (prefijo `/pagos`)."""

import uuid

from fastapi.testclient import TestClient


def test_listar_pagos(client: TestClient) -> None:
    res = client.get("/pagos/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_obtener_pago_inexistente_404(client: TestClient) -> None:
    res = client.get(f"/pagos/{uuid.uuid4()}")
    assert res.status_code == 404
