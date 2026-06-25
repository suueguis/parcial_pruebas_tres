"""Prueba de sistema de extremo a extremo sobre la API en ejecución.

Requiere que la API esté disponible en ``BASE_URL`` (por defecto el puerto de
pruebas 8001). No utiliza fixtures internos de base de datos: interactúa con el
servicio únicamente a través de HTTP.
"""

import os

import httpx

BASE_URL = os.getenv("BASE_URL", "http://localhost:8001")

PRECIO_GENERAL = 50_000
ASIENTOS = 3
TOTAL_ESPERADO = ASIENTOS * PRECIO_GENERAL


def test_flujo_reserva_y_resumen():
    """Crear una reserva General y verificar el total recaudado en el resumen."""
    evento_id = "sistema-evento-xyz"
    payload = {
        "zona": "General",
        "cantidad": ASIENTOS,
        "cliente_email": "sistema@ticketfast.com",
    }

    with httpx.Client(base_url=BASE_URL, timeout=10.0) as cliente:
        respuesta_creacion = cliente.post(f"/reservas/{evento_id}", json=payload)
        assert respuesta_creacion.status_code == 201

        respuesta_resumen = cliente.get(f"/reservas/{evento_id}/resumen")
        assert respuesta_resumen.status_code == 200

    total_recaudado = respuesta_resumen.json()["total_recaudado"]
    assert total_recaudado == TOTAL_ESPERADO == 150_000
