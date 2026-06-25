"""Fixtures compartidos para las pruebas de integración."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, obtener_sesion
from app.main import app


@pytest.fixture
def db_session():
    """Provee una sesión sobre una base de datos SQLite en memoria y aislada.

    Las tablas se crean al inicio de cada prueba y se eliminan al final, de
    modo que cada caso se ejecuta contra un esquema limpio.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    FabricaSesion = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    sesion = FabricaSesion()
    try:
        yield sesion
    finally:
        sesion.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client_con_bd(db_session):
    """Cliente HTTP de pruebas que comparte la sesión con ``db_session``.

    Sobrescribe la dependencia ``obtener_sesion`` para que la API y la prueba
    operen sobre la misma base de datos en memoria.
    """

    def _sobrescribir_sesion():
        yield db_session

    app.dependency_overrides[obtener_sesion] = _sobrescribir_sesion
    with TestClient(app) as cliente:
        yield cliente
    app.dependency_overrides.clear()
