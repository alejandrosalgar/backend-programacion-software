from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.entities.categoria import Categoria


def crear(
    db: Session,
    nombre: str,
    descripcion: Optional[str],
    estado: bool,
    id_usuario_creacion: UUID,
) -> Categoria:
    categoria = Categoria(
        nombre=nombre.strip(),
        descripcion=descripcion,
        estado=estado,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


def obtener(db: Session, id_categoria: UUID) -> Optional[Categoria]:
    return (
        db.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()
    )


def listar(db: Session, skip: int = 0, limit: int = 100) -> List[Categoria]:
    return db.query(Categoria).offset(skip).limit(limit).all()


def actualizar(
    db: Session,
    id_categoria: UUID,
    id_usuario_edita: UUID,
    **kwargs: object,
) -> Optional[Categoria]:
    categoria = obtener(db, id_categoria)
    if not categoria:
        return None
    for key, value in kwargs.items():
        if hasattr(categoria, str(key)) and str(key) != "id_categoria":
            setattr(categoria, str(key), value)
    categoria.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(categoria)
    return categoria


def eliminar(db: Session, id_categoria: UUID) -> bool:
    categoria = obtener(db, id_categoria)
    if not categoria:
        return False
    db.delete(categoria)
    db.commit()
    return True
