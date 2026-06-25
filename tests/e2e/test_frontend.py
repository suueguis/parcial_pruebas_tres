"""Prueba de extremo a extremo del frontend de reservas con Playwright.

Requiere el frontend servido en ``http://localhost:4200`` y la API disponible
en el puerto 8001. La verificación usa aserciones nativas de Playwright
(``expect``), que esperan automáticamente sin necesidad de pausas explícitas.
"""

from playwright.sync_api import Page, expect


def test_reserva_vip_muestra_total(page: Page):
    """Diligenciar el formulario con una reserva VIP y validar el total mostrado."""
    page.goto("http://localhost:4200/reservas")

    page.get_by_test_id("input-email-cliente").fill("e2e@ticketfast.com")
    page.get_by_test_id("select-zona-evento").select_option("VIP")
    page.get_by_test_id("input-cantidad-asientos").fill("1")
    page.get_by_test_id("btn-confirmar-reserva").click()

    expect(page.get_by_test_id("seccion-resumen-total")).to_contain_text("150.000")
