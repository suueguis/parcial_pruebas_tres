"""Servidor estático mínimo para el frontend de reservas en el puerto 4200."""

import http.server
import socketserver
from pathlib import Path

DIRECTORIO = Path(__file__).parent
PUERTO = 4200


class Manejador(http.server.SimpleHTTPRequestHandler):
    """Sirve los archivos del frontend y resuelve la ruta de reservas."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORIO), **kwargs)

    def do_GET(self):  # noqa: N802 (nombre impuesto por la librería estándar)
        if self.path.startswith("/reservas"):
            self.path = "/index.html"
        return super().do_GET()


if __name__ == "__main__":
    with socketserver.TCPServer(("", PUERTO), Manejador) as servidor:
        print(f"Frontend disponible en http://localhost:{PUERTO}/reservas")
        servidor.serve_forever()
