import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID

from src.database.config import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )

    nombre_completo = Column(String(100), nullable=False)
    nombre_usuario = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    clave = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)
    telefono = Column(String(20), nullable=True)
    activo = Column(Boolean, default=True)
