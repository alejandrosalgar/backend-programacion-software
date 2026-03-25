import uuid

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class DetallePedido(Base):
    """Modelo de pedido"""

    __tablename__ = "detalle_pedido"

    id_detalle_pedido = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_pedido = Column(
        UUID(as_uuid=True), ForeignKey("pedido.id_pedido"), nullable=False
    )
    id_producto = Column(
        UUID(as_uuid=True), ForeignKey("producto.id_producto"), nullable=False
    )

    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    estado = Column(Text, default=True)
    


    pedido = relationship("Pedido", foreign_keys=[id_pedido])
    producto = relationship("Producto", foreign_keys=[id_producto])
