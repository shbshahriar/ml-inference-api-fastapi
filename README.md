# FastAPI for Machine Learning

A structured, hands-on learning repository for building REST APIs with FastAPI — from basic routing to deploying ML models in production.
Each lesson lives in its own numbered folder with a working Python API, a markdown guide, and interactive HTML references.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.13** | Core language |
| **FastAPI** | Web framework |
| **Uvicorn** | ASGI server |
| **Pydantic** | Data validation |
| **uv** | Package & environment manager |

---

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) installed

```bash
# Install uv (if not already installed)
pip install uv
```

---

## Setup

```bash
# Clone the repository
git clone https://github.com/shbshahriar/ml-inference-api-fastapi.git
cd FastAPI_practice

# uv creates the virtual environment and installs all dependencies automatically
uv sync
```

---

## Running a Lesson

All servers are started from the **project root** using dot-notation for the module path:

```bash
uv run uvicorn <folder>.<file>:app --reload
```

| Lesson | Command |
|--------|---------|
| 02 — First App | `uv run uvicorn 02_fastapi_setup.first_app:app --reload` |
| 03 — HTTP Methods | `uv run uvicorn 03_http_methods.crud_api:app --reload` |
| 04 — Path & Query Params | `uv run uvicorn 04_path_query_params.path_query_api:app --reload` |

Once running, visit:

| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:8000` | Live API |
| `http://127.0.0.1:8000/docs` | Swagger UI — interactive testing |
| `http://127.0.0.1:8000/redoc` | ReDoc — clean documentation view |

Press `Ctrl+C` to stop the server.

---

## Curriculum

### 01 — What is an API
Interactive HTML guides explaining REST concepts, request/response cycles, and how APIs work.
No Python code — pure learning material.

---

### 02 — FastAPI Setup
**File:** `02_fastapi_setup/first_app.py`

First working FastAPI app. Covers:
- Installing FastAPI, Uvicorn, and Pydantic via `uv`
- Creating an `app` instance and registering a `GET /` route
- Running the dev server with hot-reload (`--reload`)
- Exploring auto-generated Swagger and ReDoc docs

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI server is running"}
```

---

### 03 — HTTP Methods (CRUD)
**File:** `03_http_methods/crud_api.py`  
**Data:** `Data/patients.json`

Patient Management API demonstrating all four HTTP methods:

| Method | Endpoint | Action |
|--------|----------|--------|
| `GET` | `/view` | Retrieve all patients |
| `GET` | `/view/{id}` | Retrieve one patient |
| `POST` | `/create` | Add a new patient |
| `PUT` | `/update/{id}` | Replace a patient record |
| `DELETE` | `/delete/{id}` | Remove a patient |

Key concepts: CRUD → HTTP mapping, idempotency, JSON as a flat-file database, `HTTPException` for proper error responses.

---

### 04 — Path & Query Parameters
**File:** `04_path_query_params/path_query_api.py`  
**Data:** `Data/patients.json`

Extends the Patient API with parameter handling:

| Endpoint | Type | Example |
|----------|------|---------|
| `/patient/{patient_id}` | Path parameter | `/patient/p001` |
| `/sort?sort_by=age&order=asc` | Query parameters | `/sort?sort_by=name&order=desc` |

Key concepts:

- **Path parameter** — identifies *which* resource (`/patient/p001`)
- **Query parameter** — controls *how* to retrieve data (`?sort_by=age`)
- `Path()` — adds descriptions, examples, and validation to path params in Swagger
- `Query()` — adds defaults, allowed values, and descriptions to query params
- `HTTPException` — returns correct 400/404 status codes instead of empty responses

---

### 05 — POST Requests *(coming soon)*
Request body handling with Pydantic models.

---

### 06 — PUT & DELETE Requests *(coming soon)*
Update and delete operations with validation.

---

### 07 — Serving ML Models *(coming soon)*
Load a trained model → accept input → return prediction as JSON.  
Projects: Iris Classification, House Price Prediction, Insurance Cost, Customer Churn.

---

### 08 — Improving APIs *(coming soon)*
Route structure, response formatting, and API best practices.

---

### 09 — Docker for ML *(coming soon)*
Writing a `Dockerfile`, `docker build`, and `docker run`.

---

### 10 — Dockerizing FastAPI *(coming soon)*
Containerizing a complete FastAPI application.

---

### 11 — Deploying on AWS *(coming soon)*
Deploying a containerized FastAPI app to a cloud platform.

---

## Project Structure

```
FastAPI_practice/
│
├── Data/
│   └── patients.json              # Shared dataset (dict keyed by patient ID)
│
├── 01_what_is_api/
│   ├── The Modern API Handbook.html
│   └── FastAPI_Mastery_Interactive_Guide.html
│
├── 02_fastapi_setup/
│   ├── first_app.py               # First FastAPI app
│   └── guide.md                   # Lesson notes
│
├── 03_http_methods/
│   ├── crud_api.py                # GET, POST, PUT, DELETE
│   └── guide.md
│
├── 04_path_query_params/
│   ├── path_query_api.py          # Path & query parameter demo
│   └── guide.md
│
├── main.py                        # Root stub (not used for lessons)
├── pyproject.toml                 # uv project config & dependencies
├── .python-version                # Pins Python 3.13
└── README.md
```

---

## Key Rules

- **Always use `uv`** — never `pip` directly
- **Run from the project root** — relative imports and file paths depend on it
- **Data file** — `Data/patients.json` is shared across lessons 03 and 04

---

## Dependencies

Managed by `uv` in `pyproject.toml`:

```toml
[dependencies]
fastapi = ">=0.135.3"
uvicorn = ">=0.43.0"
pydantic = ">=2.12.5"
```

Add a new package:

```bash
uv add <package-name>
```
