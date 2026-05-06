"""
Configuración de la base de datos PostgreSQL.
Conexión mediante variables de entorno (.env).
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

_TESTING = os.getenv("TESTING") == "1"
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL and _TESTING:
    DATABASE_URL = "sqlite+pysqlite:///:memory:"
elif not DATABASE_URL:
    raise ValueError("Se requiere DATABASE_URL en el archivo .env")

_connect_args: dict = {}
if DATABASE_URL.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}
elif "neon.tech" in DATABASE_URL:
    _connect_args = {"sslmode": "require"}

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args=_connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Generador de sesiones de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Crea todas las tablas definidas en los modelos."""
    Base.metadata.create_all(bind=engine)
