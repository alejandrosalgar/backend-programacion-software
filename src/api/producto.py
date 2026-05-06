from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import producto as crud_producto

router = APIRouter(prefix="/productos", tags=["productos"])


class ProductoCreate(BaseModel):
    id_categoria: UUID
    nombre: str
    descripcion: Optional[str] = None
    id_usuario_creacion: UUID


class ProductoUpdate(BaseModel):
    id_categoria: Optional[UUID] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    id_usuario_edita: UUID


class ProductoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_producto: UUID
    id_categoria: UUID
    nombre: str
    descripcion: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None


@router.get("/", response_model=List[ProductoRead])
def listar_productos(db: DbSession, skip: int = 0, limit: int = 100) -> List[ProductoRead]:
    return crud_producto.listar(db, skip=skip, limit=limit)


@router.get("/{id_producto}", response_model=ProductoRead)
def obtener_producto(db: DbSession, id_producto: UUID) -> ProductoRead:
    p = crud_producto.obtener(db, id_producto)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return p


@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(db: DbSession, body: ProductoCreate) -> ProductoRead:
    p = crud_producto.crear(
        db,
        id_categoria=body.id_categoria,
        nombre=body.nombre,
        descripcion=body.descripcion,
        id_usuario_creacion=body.id_usuario_creacion,
    )
    return p


@router.put("/{id_producto}", response_model=ProductoRead)
def actualizar_producto(db: DbSession, id_producto: UUID, body: ProductoUpdate) -> ProductoRead:
    id_edita = body.id_usuario_edita
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edita"})
    p = crud_producto.actualizar(db, id_producto, id_usuario_edita=id_edita, **data)
    if not p:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return p


@router.delete("/{id_producto}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(db: DbSession, id_producto: UUID) -> None:
    if not crud_producto.eliminar(db, id_producto):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
