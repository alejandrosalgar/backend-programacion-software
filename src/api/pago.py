from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import pago as crud_pago

router = APIRouter(prefix="/pagos", tags=["pagos"])


class PagoCreate(BaseModel):
    id_pedido: UUID
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    referencia: str
    tipo_pago: str
    id_usuario_creacion: UUID


class PagoUpdate(BaseModel):
    id_pedido: Optional[UUID] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    referencia: Optional[str] = None
    tipo_pago: Optional[str] = None
    id_usuario_edita: UUID


class PagoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_pago: UUID
    id_pedido: UUID
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    referencia: str
    tipo_pago: str
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None


@router.get("", response_model=List[PagoRead])
def listar_pagos(db: DbSession, skip: int = 0, limit: int = 100) -> List[PagoRead]:
    return crud_pago.listar(db, skip=skip, limit=limit)


@router.get("/{id_pago}", response_model=PagoRead)
def obtener_pago(db: DbSession, id_pago: UUID) -> PagoRead:
    p = crud_pago.obtener(db, id_pago)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    return p


@router.post("", response_model=PagoRead, status_code=status.HTTP_201_CREATED)
def crear_pago(db: DbSession, body: PagoCreate) -> PagoRead:
    p = crud_pago.crear(
        db,
        id_pedido=body.id_pedido,
        nombre=body.nombre,
        descripcion=body.descripcion,
        estado=body.estado,
        referencia=body.referencia,
        tipo_pago=body.tipo_pago,
        id_usuario_creacion=body.id_usuario_creacion,
    )
    return p


@router.put("/{id_pago}", response_model=PagoRead)
def actualizar_pago(db: DbSession, id_pago: UUID, body: PagoUpdate) -> PagoRead:
    id_edita = body.id_usuario_edita
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edita"})
    p = crud_pago.actualizar(db, id_pago, id_usuario_edita=id_edita, **data)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    return p


@router.delete("/{id_pago}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_pago(db: DbSession, id_pago: UUID) -> None:
    if not crud_pago.eliminar(db, id_pago):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
