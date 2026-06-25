"""Configuración de la conexión a la base de datos y la sesión de SQLAlchemy."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ticketfast.db")

_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=_connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Clase base declarativa para los modelos ORM."""


def obtener_sesion():
    """Provee una sesión de base de datos por request y la cierra al finalizar."""
    sesion = SessionLocal()
    try:
        yield sesion
    finally:
        sesion.close()
