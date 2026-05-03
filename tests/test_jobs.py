from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    """Servidor respondiendo"""
    response = client.get("/health")
    assert response.status_code == 200

def test_crear_job():
    """Debe crear job y responder inmediato"""
    response = client.post("/jobs/", json={
        "items": ["factura1.pdf", "factura2.pdf"],
        "descripcion": "Test"
    })
    assert response.status_code == 202
    data = response.json()
    assert "id" in data
    assert data["estado"] == "pending"
    assert data["total_items"] == 2

def test_obtener_job():
    """Debe encontrar el job creado"""
    # Crear job
    response = client.post("/jobs/", json={
        "items": ["test.pdf"],
    })
    job_id = response.json()["id"]

    # Consultar estado
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    assert response.json()["id"] == job_id

def test_job_no_existe():
    """Debe retornar 404 si no existe"""
    response = client.get("/jobs/id-que-no-existe")
    assert response.status_code == 404

def test_listar_jobs():
    """Debe retornar lista de jobs"""
    response = client.get("/jobs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_eliminar_job():
    """Debe eliminar el job"""
    # Crear job
    response = client.post("/jobs/", json={
        "items": ["test.pdf"],
    })
    job_id = response.json()["id"]

    # Eliminar
    response = client.delete(f"/jobs/{job_id}")
    assert response.status_code == 200

    # Verificar que no existe
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 404