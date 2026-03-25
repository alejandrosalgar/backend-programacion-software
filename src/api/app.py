from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.config import create_tables

from . import categoria, detalle_pedido, pago, pedido, producto, usuario


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Registra modelos y crea tablas si no existen (misma lógica que init_db.py)
    import src.entities.categoria  # noqa: F401
    import src.entities.detalle_pedido  # noqa: F401
    import src.entities.pago  # noqa: F401
    import src.entities.pedido  # noqa: F401
    import src.entities.producto  # noqa: F401
    import src.entities.usuario  # noqa: F401
    create_tables()
    yield


app = FastAPI(title="API", version="1.0.0", lifespan=lifespan)

app.include_router(usuario.router)
app.include_router(categoria.router)
app.include_router(producto.router)
app.include_router(pedido.router)
app.include_router(detalle_pedido.router)
app.include_router(pago.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
