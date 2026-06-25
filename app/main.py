"""Punto de entrada de la API de reservas de TicketFast."""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import Base, engine, obtener_sesion
from app.models import ReservaDB
from app.precios import calcular_total
from app.schemas import ReservaCrear, ReservaRespuesta, ResumenEvento


@asynccontextmanager
async def ciclo_de_vida(_: FastAPI):
    """Crea las tablas declaradas al iniciar la aplicación."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="TicketFast API", lifespan=ciclo_de_vida)


@app.post(
    "/reservas/{evento_id}",
    response_model=ReservaRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_reserva(
    evento_id: str,
    datos: ReservaCrear,
    sesion: Session = Depends(obtener_sesion),
) -> ReservaDB:
    """Registra una reserva para el evento indicado y la persiste."""
    total = calcular_total(datos.zona, datos.cantidad)
    reserva = ReservaDB(
        evento_id=evento_id,
        zona=datos.zona,
        cantidad=datos.cantidad,
        cliente_email=datos.cliente_email,
        total=total,
    )
    sesion.add(reserva)
    sesion.commit()
    sesion.refresh(reserva)
    return reserva


@app.get("/reservas/{evento_id}/resumen", response_model=ResumenEvento)
def obtener_resumen(
    evento_id: str,
    sesion: Session = Depends(obtener_sesion),
) -> ResumenEvento:
    """Devuelve el agregado de reservas y el total recaudado de un evento."""
    consulta = select(
        func.count(ReservaDB.id),
        func.coalesce(func.sum(ReservaDB.cantidad), 0),
        func.coalesce(func.sum(ReservaDB.total), 0),
    ).where(ReservaDB.evento_id == evento_id)

    total_reservas, total_asientos, total_recaudado = sesion.execute(consulta).one()

    return ResumenEvento(
        evento_id=evento_id,
        total_reservas=total_reservas,
        total_asientos=total_asientos,
        total_recaudado=total_recaudado,
    )
