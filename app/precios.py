"""Reglas de negocio para el cálculo del valor de las reservas."""

PRECIOS_POR_ZONA = {
    "General": 50_000,
    "VIP": 150_000,
}


def calcular_total(zona: str, cantidad: int) -> int:
    """Calcula el valor total de una reserva según la zona y la cantidad.

    Args:
        zona: Zona del evento ("General" o "VIP").
        cantidad: Número de asientos reservados.

    Returns:
        El valor total a recaudar por la reserva.

    Raises:
        ValueError: Si la zona no está registrada o la cantidad no es válida.
    """
    if zona not in PRECIOS_POR_ZONA:
        raise ValueError(f"Zona no válida: {zona}")
    if cantidad <= 0:
        raise ValueError("La cantidad de asientos debe ser mayor que cero")
    return PRECIOS_POR_ZONA[zona] * cantidad
