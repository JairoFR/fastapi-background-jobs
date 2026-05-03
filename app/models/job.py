from datetime import datetime, timezone
from typing import Optional, Any
from enum import Enum
from pydantic import BaseModel, ConfigDict

class JobEstado(str, Enum):
    """
    Estados posibles de un job.
    str + Enum = se serializa como string en JSON
    """
    PENDING    = "pending"     # recién creado, en cola
    PROCESSING = "processing"  # procesando ahora
    DONE       = "done"        # terminó exitosamente
    ERROR      = "error"       # falló

class Job(BaseModel):
    """
    Representa un trabajo en background.
    Se guarda en memoria — después será PostgreSQL.
    """
    id: str                              # UUID único
    estado: JobEstado = JobEstado.PENDING
    creado_en: datetime = datetime.now(timezone.utc)
    actualizado_en: datetime = datetime.now(timezone.utc)
    progreso: int = 0                    # 0 a 100
    total_items: int = 0                 # total a procesar
    items_procesados: int = 0            # cuántos van
    resultado: Optional[Any] = None      # resultado final
    error: Optional[str] = None          # mensaje de error

    model_config = ConfigDict(from_attributes=True)

class JobCreate(BaseModel):
    """Para crear un job — recibe lista de items a procesar"""
    items: list[str]                     # lista de archivos/URLs
    descripcion: Optional[str] = None

class JobResponse(BaseModel):
    """Lo que devuelve la API"""
    id: str
    estado: JobEstado
    progreso: int
    total_items: int
    items_procesados: int
    creado_en: datetime
    actualizado_en: datetime
    resultado: Optional[Any] = None
    error: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)