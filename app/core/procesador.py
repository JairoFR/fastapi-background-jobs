import asyncio
import uuid
from datetime import datetime, timezone
from typing import Dict
from app.models.job import Job, JobEstado

# Base de datos en memoria de jobs
# después será PostgreSQL
jobs_db: Dict[str, Job] = {}

async def procesar_item(item: str) -> dict:
    """
    Simula el procesamiento de un item.
    En tu caso real sería llamar a Kread API.
    """
    # Simula tiempo de procesamiento
    await asyncio.sleep(2)

    return {
        "item": item,
        "resultado": f"Procesado: {item}",
        "estado": "ok"
    }

async def ejecutar_job(job_id: str, items: list[str]):
    """
    Procesa todos los items de un job en background.
    Actualiza el estado del job en cada paso.
    """
    job = jobs_db[job_id]

    try:
        # Cambia estado a processing
        job.estado = JobEstado.PROCESSING
        job.actualizado_en = datetime.now(timezone.utc)

        resultados = []

        # Procesa cada item
        for i, item in enumerate(items):
            try:
                resultado = await procesar_item(item)
                resultados.append(resultado)
            except Exception as e:
                resultados.append({
                    "item": item,
                    "estado": "error",
                    "error": str(e)
                })

            # Actualiza progreso
            job.items_procesados = i + 1
            job.progreso = int((i + 1) / len(items) * 100)
            job.actualizado_en = datetime.now(timezone.utc)

        # Job completado
        job.estado = JobEstado.DONE
        job.resultado = resultados
        job.progreso = 100
        job.actualizado_en = datetime.now(timezone.utc)

    except Exception as e:
        # Job falló
        job.estado = JobEstado.ERROR
        job.error = str(e)
        job.actualizado_en = datetime.now(timezone.utc)

def crear_job(items: list[str]) -> Job:
    """
    Crea un nuevo job y lo guarda en memoria.
    Retorna el job para que el endpoint lo devuelva inmediato.
    """
    job_id = str(uuid.uuid4())  # ID único

    job = Job(
        id=job_id,
        total_items=len(items)
    )

    jobs_db[job_id] = job
    return job