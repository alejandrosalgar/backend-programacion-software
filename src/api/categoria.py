from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import categoria as crud_categoria

router = APIRouter(prefix="/categorias", tags=["categorias"])


class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estado: bool = True
    id_usuario_creacion: UUID


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[bool] = None
    id_usuario_edita: UUID


class CategoriaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_categoria: UUID
    nombre: str
    descripcion: Optional[str] = None
    estado: bool
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None


@router.get("", response_model=List[CategoriaRead])
def listar_categorias(db: DbSession, skip: int = 0, limit: int = 100) -> List[CategoriaRead]:
    return crud_categoria.listar(db, skip=skip, limit=limit)


@router.get("/{id_categoria}", response_model=CategoriaRead)
def obtener_categoria(db: DbSession, id_categoria: UUID) -> CategoriaRead:
    c = crud_categoria.obtener(db, id_categoria)
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return c


@router.post("", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
def crear_categoria(db: DbSession, body: CategoriaCreate) -> CategoriaRead:
    c = crud_categoria.crear(
        db,
        nombre=body.nombre,
        descripcion=body.descripcion,
        estado=body.estado,
        id_usuario_creacion=body.id_usuario_creacion,
    )
    return c


@router.put("/{id_categoria}", response_model=CategoriaRead)
def actualizar_categoria(db: DbSession, id_categoria: UUID, body: CategoriaUpdate) -> CategoriaRead:
    id_edita = body.id_usuario_edita
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edita"})
    c = crud_categoria.actualizar(db, id_categoria, id_usuario_edita=id_edita, **data)
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    return c


@router.delete("/{id_categoria}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(db: DbSession, id_categoria: UUID) -> None:
    if not crud_categoria.eliminar(db, id_categoria):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
