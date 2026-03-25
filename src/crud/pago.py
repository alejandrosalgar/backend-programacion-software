from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.entities.pago import Pago


def crear(
    db: Session,
    id_pedido: UUID,
    nombre: str,
    descripcion: Optional[str],
    estado: Optional[str],
    referencia: str,
    tipo_pago: str,
    id_usuario_creacion: UUID,
) -> Pago:
    pago = Pago(
        id_pedido=id_pedido,
        nombre=nombre.strip(),
        descripcion=descripcion,
        estado=estado if estado is not None else "pendiente",
        referencia=referencia.strip(),
        tipo_pago=tipo_pago,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(pago)
    db.commit()
    db.refresh(pago)
    return pago


def obtener(db: Session, id_pago: UUID) -> Optional[Pago]:
    return db.query(Pago).filter(Pago.id_pago == id_pago).first()


def listar(db: Session, skip: int = 0, limit: int = 100) -> List[Pago]:
    return db.query(Pago).offset(skip).limit(limit).all()


def actualizar(
    db: Session,
    id_pago: UUID,
    id_usuario_edita: UUID,
    **kwargs: object,
) -> Optional[Pago]:
    pago = obtener(db, id_pago)
    if not pago:
        return None
    for key, value in kwargs.items():
        if hasattr(pago, str(key)) and str(key) != "id_pago":
            setattr(pago, str(key), value)
    pago.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(pago)
    return pago


def eliminar(db: Session, id_pago: UUID) -> bool:
    pago = obtener(db, id_pago)
    if not pago:
        return False
    db.delete(pago)
    db.commit()
    return True
