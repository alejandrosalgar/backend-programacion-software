"""Tests HTTP alineados con el tag OpenAPI `usuarios` (prefijo `/usuarios`)."""

import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.crud.usuario import crear, eliminar


def test_listar_usuario_error_ruta_incorrecta(client: TestClient) -> None:
    res = client.get("/usuari/")
    assert res.status_code == 404


def test_listar_usuarios(client: TestClient) -> None:
    res = client.get("/usuarios/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_obtener_usuario_inexistente_404(client: TestClient) -> None:
    res = client.get(f"/usuarios/{uuid.uuid4()}")
    assert res.status_code == 404


def test_obtener_usuario_existente(client: TestClient, db_session: Session) -> None:
    suffix = uuid.uuid4().hex[:8]
    usuario = crear(
        db_session,
        nombre_completo="John Doe",
        nombre_usuario=f"johndoe_{suffix}",
        email=f"johndoe_{suffix}@example.com",
        clave="password",
        rol="admin",
        telefono="1234567890",
        activo=True,
    )

    res = client.get(f"/usuarios/{usuario.id_usuario}")
    assert res.status_code == 200
    eliminar(db_session, usuario.id_usuario)


def test_crear_usuario(client: TestClient) -> None:
    suffix = uuid.uuid4().hex[:8]
    res = client.post(
        "/usuarios/",
        json={
            "nombre_completo": "John Doe",
            "nombre_usuario": f"johndoe_{suffix}",
            "email": f"johndoe_{suffix}@example.com",
            "clave": "password",
            "rol": "admin",
            "telefono": "1234567890",
            "activo": True,
        },
    )
    assert res.status_code == 201


def test_crear_usuario_error_email_invalido(client: TestClient) -> None:
    suffix = uuid.uuid4().hex[:8]
    res = client.post(
        "/usuarios/",
        json={
            "nombre_completo": "John Doe",
            "nombre_usuario": f"johndoe_inv_{suffix}",
            "email": "johndoekdashdjkashd",
            "clave": "password",
            "rol": "admin",
            "telefono": "1234567890",
            "activo": True,
        },
    )
    assert res.status_code == 422


def test_editar_usuario_inexistente_404(client: TestClient) -> None:
    res = client.put(
        f"/usuarios/{uuid.uuid4()}",
        json={
            "nombre_completo": "John Doe",
            "nombre_usuario": "johndoe",
            "email": "johndoe@example.com",
            "clave": "password",
            "rol": "admin",
            "telefono": "1234567890",
            "activo": True,
        },
    )
    assert res.status_code == 404


def test_editar_usuario_existente(client: TestClient, db_session: Session) -> None:
    suffix = uuid.uuid4().hex[:8]
    usuario = crear(
        db_session,
        nombre_completo="John Doe",
        nombre_usuario=f"johndoe_{suffix}",
        email=f"johndoe_{suffix}@example.com",
        clave="password",
        rol="admin",
        telefono="1234567890",
        activo=True,
    )
    res = client.put(
        f"/usuarios/{usuario.id_usuario}",
        json={
            "nombre_completo": "John Doe Updated",
            "nombre_usuario": f"johndoe_{suffix}",
            "email": f"johndoe_{suffix}@example.com",
            "clave": "password",
            "rol": "admin",
            "telefono": "1234567890",
            "activo": True,
        },
    )
    assert res.status_code == 200
    eliminar(db_session, usuario.id_usuario)


def test_eliminar_usuario_inexistente_404(client: TestClient) -> None:
    res = client.delete(f"/usuarios/{uuid.uuid4()}")
    assert res.status_code == 404


def test_eliminar_usuario_existente(client: TestClient, db_session: Session) -> None:
    suffix = uuid.uuid4().hex[:8]
    usuario = crear(
        db_session,
        nombre_completo="John Doe",
        nombre_usuario=f"johndoe_{suffix}",
        email=f"johndoe_{suffix}@example.com",
        clave="password",
        rol="admin",
        telefono="1234567890",
        activo=True,
    )
    res = client.delete(f"/usuarios/{usuario.id_usuario}")
    assert res.status_code == 204
