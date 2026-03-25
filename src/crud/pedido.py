from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.entities.pedido import Pedido


def crear(
    db: Session,
    id_usuario: UUID,
    nombre: str,
    descripcion: Optional[str],
    estado: Optional[str],
    id_usuario_creacion: UUID,
) -> Pedido:
    pedido = Pedido(
        id_usuario=id_usuario,
        nombre=nombre.strip(),
        descripcion=descripcion,
        estado=estado if estado is not None else "pendiente",
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido


def obtener(db: Session, id_pedido: UUID) -> Optional[Pedido]:
    return db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()


def listar(db: Session, skip: int = 0, limit: int = 100) -> List[Pedido]:
    return db.query(Pedido).offset(skip).limit(limit).all()


def actualizar(
    db: Session,
    id_pedido: UUID,
    id_usuario_edita: UUID,
    **kwargs: object,
) -> Optional[Pedido]:
    pedido = obtener(db, id_pedido)
    if not pedido:
        return None
    for key, value in kwargs.items():
        if hasattr(pedido, str(key)) and str(key) != "id_pedido":
            setattr(pedido, str(key), value)
    pedido.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(pedido)
    return pedido


def eliminar(db: Session, id_pedido: UUID) -> bool:
    pedido = obtener(db, id_pedido)
    if not pedido:
        return False
    db.delete(pedido)
    db.commit()
    return True
