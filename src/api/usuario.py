from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr

from .deps import DbSession
from src.crud import usuario as crud_usuario

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


class UsuarioCreate(BaseModel):
    nombre_completo: str
    nombre_usuario: str
    email: EmailStr
    clave: str
    rol: str
    telefono: Optional[str] = None
    activo: bool = True


class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    nombre_usuario: Optional[str] = None
    email: Optional[EmailStr] = None
    clave: Optional[str] = None
    rol: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: UUID
    nombre_completo: str
    nombre_usuario: str
    email: str
    rol: str
    telefono: Optional[str] = None
    activo: bool


@router.get("/", response_model=List[UsuarioRead])
def listar_usuarios(db: DbSession, skip: int = 0, limit: int = 100) -> List[UsuarioRead]:
    return crud_usuario.listar(db, skip=skip, limit=limit)


@router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(db: DbSession, id_usuario: UUID) -> UsuarioRead:
    u = crud_usuario.obtener(db, id_usuario)
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return u


@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(db: DbSession, body: UsuarioCreate) -> UsuarioRead:
    u = crud_usuario.crear(
        db,
        nombre_completo=body.nombre_completo,
        nombre_usuario=body.nombre_usuario,
        email=str(body.email),
        clave=body.clave,
        rol=body.rol,
        telefono=body.telefono,
        activo=body.activo,
    )
    return u


@router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(db: DbSession, id_usuario: UUID, body: UsuarioUpdate) -> UsuarioRead:
    data = body.model_dump(exclude_unset=True)
    if "email" in data and data["email"] is not None:
        data["email"] = str(data["email"])
    u = crud_usuario.actualizar(db, id_usuario, **data)
    if not u:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return u


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(db: DbSession, id_usuario: UUID) -> None:
    if not crud_usuario.eliminar(db, id_usuario):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
