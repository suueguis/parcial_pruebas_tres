"""Prueba de integración de la API de reservas contra la base de datos."""

from sqlalchemy import select

from app.models import ReservaDB


def test_crear_reserva_persiste_en_base_de_datos(client_con_bd, db_session):
    """Una reserva válida responde 201 y queda registrada con el email correcto."""
    payload = {
        "zona": "VIP",
        "cantidad": 2,
        "cliente_email": "test@ticketfast.com",
    }

    respuesta = client_con_bd.post("/reservas/concierto-2026", json=payload)

    assert respuesta.status_code == 201

    reserva = db_session.execute(
        select(ReservaDB).where(ReservaDB.evento_id == "concierto-2026")
    ).scalar_one()
    assert reserva.cliente_email == "test@ticketfast.com"
