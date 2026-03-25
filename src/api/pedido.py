from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import pedido as crud_pedido

router = APIRouter(prefix="/pedidos", tags=["pedidos"])


class PedidoCreate(BaseModel):
    id_usuario: UUID
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    id_usuario_creacion: UUID


class PedidoUpdate(BaseModel):
    id_usuario: Optional[UUID] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    id_usuario_edita: UUID


class PedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_pedido: UUID
    id_usuario: UUID
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None


@router.get("", response_model=List[PedidoRead])
def listar_pedidos(db: DbSession, skip: int = 0, limit: int = 100) -> List[PedidoRead]:
    return crud_pedido.listar(db, skip=skip, limit=limit)


@router.get("/{id_pedido}", response_model=PedidoRead)
def obtener_pedido(db: DbSession, id_pedido: UUID) -> PedidoRead:
    p = crud_pedido.obtener(db, id_pedido)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    return p


@router.post("", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def crear_pedido(db: DbSession, body: PedidoCreate) -> PedidoRead:
    p = crud_pedido.crear(
        db,
        id_usuario=body.id_usuario,
        nombre=body.nombre,
        descripcion=body.descripcion,
        estado=body.estado,
        id_usuario_creacion=body.id_usuario_creacion,
    )
    return p


@router.put("/{id_pedido}", response_model=PedidoRead)
def actualizar_pedido(db: DbSession, id_pedido: UUID, body: PedidoUpdate) -> PedidoRead:
    id_edita = body.id_usuario_edita
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edita"})
    p = crud_pedido.actualizar(db, id_pedido, id_usuario_edita=id_edita, **data)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
    return p


@router.delete("/{id_pedido}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pedido(db: DbSession, id_pedido: UUID) -> None:
    if not crud_pedido.eliminar(db, id_pedido):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
