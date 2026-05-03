from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import jobs
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(
    title="FastAPI Background Jobs",
    version="1.0.0",
    description="API para procesamiento de tareas en background",
)

# ── Manejo global de errores ──────────────────────────
@app.exception_handler(Exception)
async def error_global(request: Request, exc: Exception):
    logger.error(
        f"Error en {request.method} {request.url}: {exc}",
        exc_info=True
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "detalle": str(exc)
        }
    )

# ── Healthcheck ───────────────────────────────────────
@app.get("/health", tags=["Sistema"])
def health():
    return {
        "estado": "ok",
        "version": "1.0.0",
        "app": "FastAPI Background Jobs"
    }

# ── Registrar routers ─────────────────────────────────
app.include_router(jobs.router)