# Tests de la API (pytest)

Este documento combina **marco teórico** (qué es probar software, qué es pytest, cómo funcionan las aserciones) con la **descripción concreta** de cómo están organizados los tests en este backend.

---

## Marco teórico: qué es el testing de software

El **testing** (pruebas de software) es el proceso de **ejecutar el programa bajo condiciones controladas** y **comprobar que el comportamiento coincide con lo esperado**. No sustituye el análisis ni el diseño, pero reduce el riesgo de regresiones (que algo que funcionaba deje de hacerlo) y documenta, de forma ejecutable, qué se considera “correcto”.

Algunas ideas útiles:

- **Verificación vs. validación**: la *verificación* pregunta “¿lo construimos bien?” (cumple especificación); la *validación* pregunta “¿construimos lo correcto?” (sirve al usuario). Los tests automatizados suelen apoyar sobre todo la verificación repetible.
- **Pirámide de pruebas**: en la base, muchas pruebas **rápidas y aisladas** (unidad); encima, pruebas que combinan componentes (**integración**); arriba, menos pruebas **end-to-end** (flujo completo, más lentas y frágiles). Este proyecto usa principalmente **tests de API con `TestClient`**, que se acercan a integración ligera: se levanta la app, se llama HTTP real contra rutas, y a veces una base en memoria.
- **Cobertura**: “cuánto código ejecutan los tests” es una métrica; **alta cobertura no garantiza buenos tests**, pero **baja cobertura** suele indicar zonas sin comprobar.
- **Casos de prueba**: conviene pensar en **entrada**, **acción** y **resultado esperado**, más **casos límite** (listas vacías, IDs inexistentes, errores 4xx/5xx esperados).

---

## Qué es pytest

**pytest** es un **framework de ejecución y organización de pruebas** para Python. No es el único (existen `unittest` de la biblioteca estándar, `nose`, etc.), pero es muy usado por su sintaxis simple y sus extensiones (plugins).

pytest se encarga de:

1. **Descubrir** archivos y funciones de prueba (por convención: archivos `test_*.py` o `*_test.py`, funciones `test_*`).
2. **Ejecutar** cada prueba de forma aislada y **informar** fallos con trazas legibles.
3. **Gestionar fixtures** (datos o clientes preparados antes del test), definición de opciones en `pytest.ini`, marcadores, etc.

En este backend, las pruebas llaman a la API mediante **`TestClient`** de FastAPI/Starlette: son peticiones HTTP al proceso de prueba sin abrir un puerto real en muchos escenarios, pero sí pasan por el enrutado y gran parte de la pila de la aplicación.

---

## Conceptos que conviene tener claros

| Concepto | Qué es |
|----------|--------|
| **Caso de prueba** | Un escenario concreto: por ejemplo “listar usuarios con base vacía devuelve 200 y una lista”. |
| **Aserción** | La comprobación explícita del resultado (`assert ...`). Si falla, el test se marca como fallido. |
| **Fixture** | Función u objeto reutilizable preparado antes del test (en pytest, con `@pytest.fixture`). Aquí, `client` en `conftest.py` entrega un `TestClient` listo. |
| **Arrange – Act – Assert** | Patrón mental: **preparar** datos/estado, **actuar** (llamar al endpoint), **afirmar** el resultado. Ayuda a leer y escribir tests claros. |
| **Smoke test** | Prueba muy básica de que “algo arranca y responde”; no profundiza en todos los casos. |
| **Test de contrato (ligero)** | Comprueba aspectos estables del contrato HTTP: código de estado, forma general del JSON (por ejemplo que sea lista), sin modelar toda la lógica de negocio. |

---

## Cómo funciona `assert` en Python y qué aporta pytest

### En Python

`assert <expresión>` es una **sentencia**: evalúa `<expresión>`; si el resultado es “falso” (`False`, `None`, `0`, listas vacías, etc., según contexto booleano), lanza **`AssertionError`**. Si es verdadero, no hace nada y el programa sigue.

Ejemplo mínimo:

```python
assert 1 + 1 == 2
assert len([]) == 0
```

Si falla:

```python
assert 1 + 1 == 3  # AssertionError
```

En modo optimizado (`python -O`), los `assert` pueden **eliminarse**; por eso **no** debe usarse `assert` para validaciones de seguridad en producción (solo para desarrollo y tests). En archivos de **pytest**, el uso habitual es precisamente en pruebas.

### En pytest

pytest **intercepta** los fallos de `assert` y muestra **qué expresión falló** y los **valores** involucrados cuando puede introspectar la comparación. Por eso en tests se prefiere escribir:

```python
assert res.status_code == 200
```

en lugar de construir manualmente mensajes de error para cada comprobación (a menos que quieras un mensaje muy específico; también puedes usar `assert condición, "mensaje opcional"`).

**Equivale a:** “si no se cumple la condición, este test **falla** y pytest lo reporta como fallo en el resumen”.

---

## Qué se hizo en este proyecto

Se creó la carpeta `src/tests/` dentro del backend, con **subcarpetas por tag de OpenAPI** (los mismos `tags=[...]` definidos en cada `APIRouter` de `src/api/`). Cada carpeta contiene un archivo `test_*.py` que ejercita los endpoints HTTP de ese grupo usando `TestClient` de FastAPI.

Además:

- `pytest.ini` en la raíz del backend indica `testpaths = src/tests` y `pythonpath = .` para resolver imports `src.*`.
- `src/tests/conftest.py` define la variable de entorno `TESTING=1` y el fixture `client` compartido por todos los tests.
- En modo `TESTING=1`, si no hay `DATABASE_URL`, la aplicación usa **SQLite en memoria** (`src/database/config.py`) para que los tests puedan correr sin PostgreSQL ni archivo `.env`.

El endpoint global `/health` no pertenece a un router con tag; sus pruebas están en `src/tests/health/`.

---

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

---

## Cómo ejecutar

Desde la carpeta del backend (`backend-programacion-software`):

```bash
pip install -r requirements.txt
python -m pytest
```

En Windows, si el comando `pytest` no está en el `PATH`, usa siempre `python -m pytest`.

Para ejecutar solo un tag (carpeta):

```bash
python -m pytest src/tests/usuarios/
```

Si aparece un error relacionado con plugins (por ejemplo `anyio` y `_pytest.scope`), actualiza pytest: `python -m pip install -U pytest`.

---

## Ejecución contra PostgreSQL

Si defines `DATABASE_URL` en el entorno (por ejemplo copiando `.env`), esa URL tiene prioridad incluso con `TESTING=1`. Útil para validar la API contra una base real.
