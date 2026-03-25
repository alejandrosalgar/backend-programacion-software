# Proyecto ORM con trazabilidad y API REST

Proyecto en Python con **SQLAlchemy (ORM)**, **FastAPI**, **Pydantic** y **PostgreSQL** (por ejemplo Neon). Varias entidades incluyen trazabilidad: usuario que creó y usuario que editó cada registro.

## Estructura del proyecto

```
.
├── main.py              # Arranca el servidor (uvicorn + FastAPI)
├── init_db.py           # Opcional: crea tablas sin levantar la API
├── requirements.txt
├── .env                 # Variables de entorno (no versionar; ver .gitignore)
└── src/
    ├── database/
    │   └── config.py    # Engine, SessionLocal, get_db, create_tables
    ├── entities/        # Modelos ORM (SQLAlchemy)
    │   ├── usuario.py
    │   ├── categoria.py
    │   ├── producto.py
    │   ├── pedido.py
    │   ├── detalle_pedido.py
    │   └── pago.py
    ├── crud/            # Lógica por entidad (crear, leer, listar, actualizar, eliminar)
    │   ├── usuario.py
    │   ├── categoria.py
    │   ├── producto.py
    │   ├── pedido.py
    │   ├── detalle_pedido.py
    │   └── pago.py
    └── api/               # Capa HTTP (FastAPI)
        ├── app.py         # Instancia FastAPI, routers y arranque (create_tables)
        ├── deps.py        # Dependencia de sesión de BD
        ├── usuario.py
        ├── categoria.py
        ├── producto.py
        ├── pedido.py
        ├── detalle_pedido.py
        └── pago.py
```

Flujo: **`main.py`** → **`src.api.app`** (FastAPI) → **`src.api.*`** (rutas) → **`src.crud.*`** → **`src.database`** + modelos en **`src.entities`**.

## Entidades

| Entidad | Descripción breve |
|--------|-------------------|
| **Usuario** | Usuarios del sistema (rol, credenciales, etc.). Base para FKs de trazabilidad en otras tablas. |
| **Categoria** | Categorías de productos; incluye `id_usuario_creacion` / `id_usuario_edita`. |
| **Producto** | Productos asociados a una categoría; trazabilidad de creación/edición. |
| **Pedido** | Pedidos vinculados a un usuario; trazabilidad. |
| **DetallePedido** | Líneas de pedido (pedido + producto). |
| **Pago** | Pagos asociados a un pedido; trazabilidad. |

En las rutas de creación/actualización que lo requieren, el cuerpo JSON incluye los UUID de usuario necesarios para auditoría (`id_usuario_creacion`, `id_usuario_edita`, etc., según el endpoint).

## API REST

Con el servidor en marcha, la documentación interactiva está en:

- **Swagger UI:** http://127.0.0.1:8000/docs  
- **ReDoc:** http://127.0.0.1:8000/redoc  

Prefijos aproximados:

| Prefijo | Entidad |
|--------|---------|
| `/usuarios` | Usuario |
| `/categorias` | Categoria |
| `/productos` | Producto |
| `/pedidos` | Pedido |
| `/detalles-pedido` | DetallePedido |
| `/pagos` | Pago |

Cada recurso expone, salvo detalles del esquema: **GET** (lista y por id), **POST**, **PUT**, **DELETE**. Comprobación rápida: **GET** `/health`.

## Requisitos

- Python 3.10+
- PostgreSQL o servicio compatible (por ejemplo Neon)

## Instalación

1. Crear y activar un entorno virtual:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   En Linux/macOS: `source .venv/bin/activate`

2. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Configurar la base de datos: en la raíz del proyecto, crea un archivo **`.env`** con:

   ```
   DATABASE_URL=postgresql://usuario:password@host:5432/nombre_bd
   ```

   Si la contraseña tiene caracteres especiales (`@`, `&`, `#`, etc.), codifícala en la URL (por ejemplo `@` → `%40`).

4. Arrancar la API:

   ```bash
   python main.py
   ```

   Al iniciar, la aplicación registra los modelos y ejecuta **`create_tables()`** si las tablas no existen (equivalente a ejecutar `init_db.py` manualmente).

## Scripts útiles

| Comando | Uso |
|--------|-----|
| `python main.py` | Levanta FastAPI con uvicorn (recarga en caliente). |
| `python init_db.py` | Solo crea tablas en la BD configurada en `.env` (sin servidor HTTP). |

## Validaciones

- **Pydantic** valida los cuerpos de entrada en cada módulo bajo `src/api/` (modelos `*Create`, `*Update`, `*Read`).
- Las respuestas de usuario **no** incluyen el campo de contraseña (`clave`).

## Notas

- No subas **`.env`** al repositorio (debe estar en `.gitignore`).
- En **producción** conviene usar **migraciones** (por ejemplo Alembic) en lugar de depender solo de `create_all` / `create_tables()` al arranque.
- El archivo `src/entities/rol.py` en el repositorio puede duplicar el modelo de usuario; la fuente de verdad para la tabla `usuarios` es `src/entities/usuario.py`.
