from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import detalle_pedido as crud_detalle_pedido

router = APIRouter(prefix="/detalles-pedido", tags=["detalles-pedido"])


class DetallePedidoCreate(BaseModel):
    id_pedido: UUID
    id_producto: UUID
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[str] = None


class DetallePedidoUpdate(BaseModel):
    id_pedido: Optional[UUID] = None
    id_producto: Optional[UUID] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None


class DetallePedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_detalle_pedido: UUID
    id_pedido: UUID
    id_producto: UUID
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[str] = None


@router.get("", response_model=List[DetallePedidoRead])
def listar_detalles(db: DbSession, skip: int = 0, limit: int = 100) -> List[DetallePedidoRead]:
    return crud_detalle_pedido.listar(db, skip=skip, limit=limit)


@router.get("/{id_detalle_pedido}", response_model=DetallePedidoRead)
def obtener_detalle(db: DbSession, id_detalle_pedido: UUID) -> DetallePedidoRead:
    d = crud_detalle_pedido.obtener(db, id_detalle_pedido)
    if not d:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detalle no encontrado")
    return d


@router.post("", response_model=DetallePedidoRead, status_code=status.HTTP_201_CREATED)
def crear_detalle(db: DbSession, body: DetallePedidoCreate) -> DetallePedidoRead:
    d = crud_detalle_pedido.crear(
        db,
        id_pedido=body.id_pedido,
        id_producto=body.id_producto,
        nombre=body.nombre,
        descripcion=body.descripcion,
        estado=body.estado,
    )
    return d


@router.put("/{id_detalle_pedido}", response_model=DetallePedidoRead)
def actualizar_detalle(
    db: DbSession, id_detalle_pedido: UUID, body: DetallePedidoUpdate
) -> DetallePedidoRead:
    data = body.model_dump(exclude_unset=True)
    d = crud_detalle_pedido.actualizar(db, id_detalle_pedido, **data)
    if not d:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detalle no encontrado")
    return d


@router.delete("/{id_detalle_pedido}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_detalle(db: DbSession, id_detalle_pedido: UUID) -> None:
    if not crud_detalle_pedido.eliminar(db, id_detalle_pedido):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detalle no encontrado")
