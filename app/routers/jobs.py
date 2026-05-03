from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import List
from app.models.job import JobCreate, JobResponse, JobEstado
from app.core.procesador import jobs_db, crear_job, ejecutar_job

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)

@router.post("/", response_model=JobResponse, status_code=202)
async def crear_job_endpoint(
    datos: JobCreate,
    background_tasks: BackgroundTasks  # ← inyectado por FastAPI
):
    """
    Crea un job y lo procesa en background.
    Responde INMEDIATO con job_id — no espera el procesamiento.
    202 Accepted = recibido pero aún no procesado.
    """
    # Crea el job en memoria
    job = crear_job(datos.items)

    # Agrega el procesamiento al background
    # FastAPI lo ejecuta DESPUÉS de responder al cliente
    background_tasks.add_task(
        ejecutar_job,
        job.id,
        datos.items
    )

    # Responde INMEDIATO — el job sigue procesando en background
    return job

@router.get("/", response_model=List[JobResponse])
async def listar_jobs():
    """Retorna todos los jobs"""
    return list(jobs_db.values())

@router.get("/{job_id}", response_model=JobResponse)
async def obtener_job(job_id: str):
    """
    Consulta el estado de un job.
    El cliente llama este endpoint periódicamente
    para saber si el job terminó.
    """
    job = jobs_db.get(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail=f"Job {job_id} no encontrado"
        )

    return job

@router.get("/{job_id}/resultado")
async def obtener_resultado(job_id: str):
    """
    Descarga el resultado cuando el job está done.
    Si el job no terminó devuelve el estado actual.
    """
    job = jobs_db.get(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail=f"Job {job_id} no encontrado"
        )

    if job.estado == JobEstado.PENDING:
        return {"mensaje": "Job en cola, aún no comenzó", "estado": job.estado}

    if job.estado == JobEstado.PROCESSING:
        return {
            "mensaje": "Job procesando...",
            "estado": job.estado,
            "progreso": f"{job.progreso}%",
            "procesados": f"{job.items_procesados}/{job.total_items}"
        }

    if job.estado == JobEstado.ERROR:
        raise HTTPException(
            status_code=500,
            detail=f"Job falló: {job.error}"
        )

    # Job done — devuelve resultado completo
    return {
        "estado": job.estado,
        "total_procesados": job.total_items,
        "resultado": job.resultado
    }

@router.delete("/{job_id}")
async def eliminar_job(job_id: str):
    """Elimina un job de la memoria"""
    if job_id not in jobs_db:
        raise HTTPException(
            status_code=404,
            detail=f"Job {job_id} no encontrado"
        )

    del jobs_db[job_id]
    return {"mensaje": f"Job {job_id} eliminado ✅"}