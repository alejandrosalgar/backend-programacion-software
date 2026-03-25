import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.database.config import Base


class Pago(Base):
    """Modelo de pago"""

    __tablename__ = "pago"

    id_pago = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_pedido = Column(
        UUID(as_uuid=True), ForeignKey("pedido.id_pedido"), nullable=False
    )

    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    estado = Column(Text, default=True)
    referencia = Column(String(100), nullable=False, unique=True)
    tipo_pago = Column(Text, nullable=False)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
    pedido = relationship("Pedido", foreign_keys=[id_pedido])
