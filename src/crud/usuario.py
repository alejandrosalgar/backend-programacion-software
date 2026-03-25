from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.entities.usuario import Usuario


def crear(
    db: Session,
    nombre_completo: str,
    nombre_usuario: str,
    email: str,
    clave: str,
    rol: str,
    telefono: Optional[str] = None,
    activo: bool = True,
) -> Usuario:
    usuario = Usuario(
        nombre_completo=nombre_completo.strip(),
        nombre_usuario=nombre_usuario.strip(),
        email=email.strip(),
        clave=clave,
        rol=rol,
        telefono=telefono,
        activo=activo,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def obtener(db: Session, id_usuario: UUID) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def listar(db: Session, skip: int = 0, limit: int = 100) -> List[Usuario]:
    return db.query(Usuario).offset(skip).limit(limit).all()


def actualizar(db: Session, id_usuario: UUID, **kwargs: object) -> Optional[Usuario]:
    usuario = obtener(db, id_usuario)
    if not usuario:
        return None
    for key, value in kwargs.items():
        if hasattr(usuario, str(key)) and str(key) not in ("id_usuario",):
            setattr(usuario, str(key), value)
    db.commit()
    db.refresh(usuario)
    return usuario


def eliminar(db: Session, id_usuario: UUID) -> bool:
    usuario = obtener(db, id_usuario)
    if not usuario:
        return False
    db.delete(usuario)
    db.commit()
    return True
