"""Tests HTTP alineados con el tag OpenAPI `usuarios` (prefijo `/usuarios`)."""

import uuid

from fastapi.testclient import TestClient


def test_listar_usuarios(client: TestClient) -> None:
    res = client.get("/usuarios/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_obtener_usuario_inexistente_404(client: TestClient) -> None:
    res = client.get(f"/usuarios/{uuid.uuid4()}")
    assert res.status_code == 404
