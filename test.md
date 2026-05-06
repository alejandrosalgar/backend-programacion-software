# Tests de la API (pytest)

## Qué se hizo

Se creó la carpeta `src/tests/` dentro del backend, con **subcarpetas por tag de OpenAPI** (los mismos `tags=[...]` definidos en cada `APIRouter` de `src/api/`). Cada carpeta contiene un archivo `test_*.py` que ejercita los endpoints HTTP de ese grupo usando `TestClient` de FastAPI.

Además:

- `pytest.ini` en la raíz del backend indica `testpaths = src/tests` y `pythonpath = .` para resolver imports `src.*`.
- `src/tests/conftest.py` define la variable de entorno `TESTING=1` y el fixture `client` compartido por todos los tests.
- En modo `TESTING=1`, si no hay `DATABASE_URL`, la aplicación usa **SQLite en memoria** (`src/database/config.py`) para que los tests puedan correr sin PostgreSQL ni archivo `.env`.

El endpoint global `/health` no pertenece a un router con tag; sus pruebas están en `src/tests/health/`.

## Qué hace cada parte

| Ubicación | Tag OpenAPI / nota | Qué validan los tests |
|-----------|--------------------|------------------------|
| `src/tests/health/` | (sin tag; ruta `/health`) | Respuesta 200 y cuerpo `{"status":"ok"}`. |
| `src/tests/usuarios/` | `usuarios` | `GET /usuarios/` → 200 y lista JSON; `GET /usuarios/{uuid}` con UUID inexistente → 404. |
| `src/tests/categorias/` | `categorias` | Listado y 404 para recurso inexistente. |
| `src/tests/productos/` | `productos` | Listado y 404 para recurso inexistente. |
| `src/tests/pedidos/` | `pedidos` | Listado y 404 para recurso inexistente. |
| `src/tests/detalles_pedido/` | `detalles-pedido` | Rutas bajo `/detalles-pedido/`; listado y 404. El nombre de carpeta usa guión bajo por convención de Python. |
| `src/tests/pagos/` | `pagos` | Listado y 404 para recurso inexistente. |

Estos tests son **smoke / contrato ligero**: comprueban que la app responde y que los códigos HTTP esperados se cumplen con una base vacía. Para pruebas que creen datos encadenados (usuario → categoría → producto → pedido, etc.) se pueden ampliar los mismos archivos con más casos `POST`/`PUT`/`DELETE`.

## Cómo ejecutar

Desde la carpeta del backend (`backend-programacion-software`):

```bash
pip install -r requirements.txt
pytest
```

Para ejecutar solo un tag (carpeta):

```bash
pytest src/tests/usuarios/
```

## Ejecución contra PostgreSQL

Si defines `DATABASE_URL` en el entorno (por ejemplo copiando `.env`), esa URL tiene prioridad incluso con `TESTING=1`. Útil para validar la API contra una base real.
