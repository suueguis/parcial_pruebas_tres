# TicketFast — Suite de pruebas

Plataforma de reservas de eventos con su batería de pruebas de integración,
sistema y extremo a extremo (frontend).

## Arquitectura

```
app/        API FastAPI + modelo ReservaDB + reglas de negocio (precios)
frontend/   Formulario de reservas (servido en :4200) + servidor estático
tests/      conftest (fixtures) + integration / system / e2e
```

Reglas de negocio: **General = $50.000** y **VIP = $150.000** por asiento.

## Requisitos

```bash
python -m venv .venv
.\.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python -m playwright install chromium
```

## Ejecución de las pruebas

### Punto 2 — Integración (autónoma)

Usa una base de datos SQLite en memoria; no requiere servidores.

```bash
pytest tests/integration -v
```

### Punto 3 — Sistema

Requiere la API en ejecución en el puerto 8001.

```bash
uvicorn app.main:app --port 8001        # terminal 1
pytest tests/system -v                   # terminal 2
```

### Punto 4 — Frontend E2E

Requiere la API (:8001) y el frontend (:4200).

```bash
uvicorn app.main:app --port 8001        # terminal 1
python frontend/servidor.py              # terminal 2  -> http://localhost:4200/reservas
pytest tests/e2e -v                      # terminal 3
```

## Infraestructura de pruebas con Docker (Punto 1)

```bash
docker compose -f docker-compose.test.yml up --build
```

Levanta `db-test` (PostgreSQL 16 en `tmpfs`, volátil) y `api-test` en el
puerto 8001, dependiente del estado saludable de la base de datos.
