# ⚙️ FastAPI Background Jobs

API REST para procesamiento de tareas en background sin bloquear al cliente.

## 🛠️ Stack tecnológico

- **Python 3.11**
- **FastAPI** — framework para APIs REST
- **BackgroundTasks** — procesamiento async en background
- **Pydantic v2** — validación de datos
- **Docker** — contenedorización
- **pytest** — testing

## 📁 Estructura del proyecto

```
app/
├── core/
│   ├── config.py       # configuración central
│   └── procesador.py   # lógica de procesamiento en background
├── models/
│   └── job.py          # modelos de Job y estados
├── routers/
│   └── jobs.py         # endpoints de jobs
└── main.py             # entrada principal
tests/
└── test_jobs.py        # 6 tests
```

## 🔄 Flujo de un Job

```
1. POST /jobs        → crea job, responde INMEDIATO con job_id
2. Background        → procesa items sin bloquear
3. GET /jobs/{id}    → consulta estado (pending/processing/done/error)
4. GET /jobs/{id}/resultado → descarga resultado cuando está done
```

## 📊 Estados de un Job

```
pending    → recién creado, en cola
processing → procesando ahora
done       → terminó exitosamente
error      → falló
```

## 🚀 Cómo correr el proyecto

### 1️⃣ Clona el repositorio
```bash
git clone git@github.com:JairoFR/fastapi-background-jobs.git
cd fastapi-background-jobs
```

### 2️⃣ Crea el ambiente virtual
```bash
python3 -m venv env
source env/bin/activate
```

### 3️⃣ Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Configura las variables de entorno
```bash
cp .env.example .env
```

### 5️⃣ Corre el servidor
```bash
uvicorn app.main:app --reload
```

## 🐳 Con Docker

```bash
docker build -t fastapi-background-jobs .
docker run -p 8000:8000 fastapi-background-jobs
```

## 🧪 Tests

```bash
pytest tests/ -v
```

## 📡 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /health | Estado del servidor |
| POST | /jobs | Crear job |
| GET | /jobs | Listar todos los jobs |
| GET | /jobs/{id} | Estado de un job |
| GET | /jobs/{id}/resultado | Resultado del job |
| DELETE | /jobs/{id} | Eliminar job |

## 💡 Caso de uso real

```
Rocketbot → POST /jobs/procesar → job_id inmediato
          → GET /jobs/{id}      → consulta cada 30 seg
          → cuando done         → descarga resultado
```

## 📖 Documentación

```
http://localhost:8000/docs
```