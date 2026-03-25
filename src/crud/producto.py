from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.entities.producto import Producto


def crear(
    db: Session,
    id_categoria: UUID,
    nombre: str,
    descripcion: Optional[str],
    id_usuario_creacion: UUID,
) -> Producto:
    producto = Producto(
        id_categoria=id_categoria,
        nombre=nombre.strip(),
        descripcion=descripcion,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def obtener(db: Session, id_producto: UUID) -> Optional[Producto]:
    return db.query(Producto).filter(Producto.id_producto == id_producto).first()


def listar(db: Session, skip: int = 0, limit: int = 100) -> List[Producto]:
    return db.query(Producto).offset(skip).limit(limit).all()


def actualizar(
    db: Session,
    id_producto: UUID,
    id_usuario_edita: UUID,
    **kwargs: object,
) -> Optional[Producto]:
    producto = obtener(db, id_producto)
    if not producto:
        return None
    for key, value in kwargs.items():
        if hasattr(producto, str(key)) and str(key) != "id_producto":
            setattr(producto, str(key), value)
    producto.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(producto)
    return producto


def eliminar(db: Session, id_producto: UUID) -> bool:
    producto = obtener(db, id_producto)
    if not producto:
        return False
    db.delete(producto)
    db.commit()
    return True
