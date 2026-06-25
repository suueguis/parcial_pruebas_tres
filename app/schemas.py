"""Esquemas de validación y serialización con Pydantic."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ReservaCrear(BaseModel):
    """Datos de entrada para registrar una reserva."""

    zona: Literal["General", "VIP"]
    cantidad: int = Field(gt=0, description="Número de asientos a reservar")
    cliente_email: EmailStr


class ReservaRespuesta(BaseModel):
    """Representación de una reserva ya persistida."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    evento_id: str
    zona: str
    cantidad: int
    cliente_email: EmailStr
    total: int


class ResumenEvento(BaseModel):
    """Resumen agregado de las reservas de un evento."""

    evento_id: str
    total_reservas: int
    total_asientos: int
    total_recaudado: int
