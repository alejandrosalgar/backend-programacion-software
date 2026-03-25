from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.entities.detalle_pedido import DetallePedido


def crear(
    db: Session,
    id_pedido: UUID,
    id_producto: UUID,
    nombre: str,
    descripcion: Optional[str] = None,
    estado: Optional[str] = None,
) -> DetallePedido:
    detalle_pedido = DetallePedido(
        id_pedido=id_pedido,
        id_producto=id_producto,
        nombre=nombre.strip(),
        descripcion=descripcion,
        estado=estado if estado is not None else "activo",
    )
    db.add(detalle_pedido)
    db.commit()
    db.refresh(detalle_pedido)
    return detalle_pedido


def obtener(db: Session, id_detalle_pedido: UUID) -> Optional[DetallePedido]:
    return (
        db.query(DetallePedido)
        .filter(DetallePedido.id_detalle_pedido == id_detalle_pedido)
        .first()
    )


def listar(db: Session, skip: int = 0, limit: int = 100) -> List[DetallePedido]:
    return db.query(DetallePedido).offset(skip).limit(limit).all()


def actualizar(
    db: Session,
    id_detalle_pedido: UUID,
    **kwargs: object,
) -> Optional[DetallePedido]:
    detalle_pedido = obtener(db, id_detalle_pedido)
    if not detalle_pedido:
        return None
    for key, value in kwargs.items():
        setattr(detalle_pedido, str(key), value)
    db.commit()
    db.refresh(detalle_pedido)
    return detalle_pedido


def eliminar(db: Session, id_detalle_pedido: UUID) -> bool:
    detalle_pedido = obtener(db, id_detalle_pedido)
    if not detalle_pedido:
        return False
    db.delete(detalle_pedido)
    db.commit()
    return True
