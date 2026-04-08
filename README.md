# FastAPI for Machine Learning

A structured, hands-on learning repository for building REST APIs with FastAPI — from basic routing to deploying ML models in production.
Each lesson lives in its own numbered folder with a working Python API and a markdown guide.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.13** | Core language |
| **FastAPI** | Web framework |
| **Uvicorn** | ASGI server |
| **Pydantic** | Data validation |
| **uv** | Package & environment manager |
| **LangChain** | LLM orchestration framework |
| **langchain-openai** | LangChain wrapper for the OpenAI API |

---

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) installed

```bash
pip install uv
```

---

## Setup

```bash
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
| 05 — POST Requests | `uv run uvicorn 05_post_requests.post_requests_api:app --reload` |
| 06 — PUT & DELETE | `uv run uvicorn 06_put_delete_requests.put_delete_requests_api:app --reload` |
| 07 — LLM with LangChain | `uv run uvicorn 07_serving_llm_models.llm_health_api:app --reload` |

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

Patient Management API introducing all four HTTP methods and their CRUD mapping.

| Method | Endpoint | Action |
|--------|----------|--------|
| `GET` | `/` | Health check |
| `GET` | `/view` | Retrieve all patients |

Key concepts: CRUD → HTTP mapping, `HTTPException` for error responses, JSON as a flat-file database.

---

### 04 — Path & Query Parameters
**File:** `04_path_query_params/path_query_api.py`
**Data:** `Data/patients.json`

| Endpoint | Type | Example |
|----------|------|---------|
| `/patient/{patient_id}` | Path parameter | `/patient/p001` |
| `/sort?sort_by=age&order=asc` | Query parameters | `/sort?sort_by=name&order=desc` |

Key concepts:
- **Path parameter** — identifies *which* resource (`/patient/p001`)
- **Query parameter** — controls *how* to retrieve data (`?sort_by=age`)
- `Path()` — adds descriptions, examples, and validation to path params in Swagger
- `Query()` — adds defaults, allowed values, and descriptions to query params
- HTTP status codes — returning correct 400/404 instead of empty responses

---

### 05 — POST Requests
**File:** `05_post_requests/post_requests_api.py`
**Data:** `Data/patients.json`

| Endpoint | Action |
|----------|--------|
| `POST /create` | Add a new patient record |

Key concepts:
- Request body — structured JSON sent by the client
- Pydantic model with `Annotated` + `Field` — type hints and metadata in one declaration
- `Literal["male", "female"]` — restrict gender to allowed values
- `computed_field` — auto-generate `bmi` and `obesity` from `height` and `weight`
- Duplicate check — `400` if the patient ID already exists
- `model_dump(exclude={"id"})` — use ID as dict key, exclude from stored value

---

### 06 — PUT & DELETE Requests
**File:** `06_put_delete_requests/put_delete_requests_api.py`
**Data:** `Data/patients.json`

Completes the full CRUD cycle.

| Endpoint | Action |
|----------|--------|
| `PUT /patient/{patient_id}` | Partially update an existing patient |
| `DELETE /patient/{patient_id}` | Remove a patient record |

Key concepts:
- `PatientUpdate` model — all fields `Optional` for partial updates
- `model_dump(exclude_unset=True)` — only apply fields the client actually sent
- BMI recomputation — `compute_bmi()` and `compute_obesity()` helper functions called by both the model and the PUT endpoint, single source of truth
- 404 guard — validate existence before any mutation

---

### 07 — Serving an LLM with FastAPI + LangChain
**Files:** `07_serving_llm_models/`
**Frontend:** `07_serving_llm_models/frontend/`

Full-stack AI Health Advisor. The patient submits their profile and health concern through a browser UI; FastAPI validates it, builds a prompt, and returns personalized advice from an OpenAI LLM via LangChain.

| Endpoint | Action |
|----------|--------|
| `GET /` | Serves the HTML frontend |
| `POST /chat` | Validates input, calls LLM, returns health advice |

Key concepts:
- `LangChain` — LLM orchestration with `ChatOpenAI`, `SystemMessage`, `HumanMessage`
- `Prompt engineering` — separate `SYSTEM_PROMPT` (persona) and dynamic user prompt (patient data)
- `computed_field` — Pydantic auto-generates `bmi` and `obesity` from height and weight
- `CORSMiddleware` — allows browsers to make cross-origin API calls
- `StaticFiles` — FastAPI serves the HTML/CSS/JS frontend from the same process
- `.env` — API key and model name loaded securely via `python-dotenv`

```bash
# Copy the env template and add your OpenAI API key
cp 07_serving_llm_models/.env.example 07_serving_llm_models/.env

# Run — frontend available at http://127.0.0.1:8000
uv run uvicorn 07_serving_llm_models.llm_health_api:app --reload
```

---

## Project Structure

```
FastAPI_practice/
│
├── Data/
│   └── patients.json                      # Shared dataset (dict keyed by patient ID)
│
├── 01_what_is_api/
│   ├── The Modern API Handbook.html
│   └── FastAPI_Mastery_Interactive_Guide.html
│
├── 02_fastapi_setup/
│   ├── first_app.py                       # First FastAPI app
│   └── guide.md
│
├── 03_http_methods/
│   ├── crud_api.py                        # GET endpoints
│   └── guide.md
│
├── 04_path_query_params/
│   ├── path_query_api.py                  # Path & query parameters
│   └── guide.md
│
├── 05_post_requests/
│   ├── post_requests_api.py               # POST /create with Pydantic validation
│   └── guide.md
│
├── 06_put_delete_requests/
│   ├── put_delete_requests_api.py         # PUT /patient/{id}, DELETE /patient/{id}
│   └── guide.md
│
├── 07_serving_llm_models/
│   ├── llm_health_api.py                  # FastAPI app — LangChain + static frontend
│   ├── schema.py                          # ChatMessage Pydantic model
│   ├── prompts.py                         # System prompt + user prompt builder
│   ├── utils.py                           # BMI and obesity helpers
│   ├── .env.example                       # API key template
│   ├── guide.md
│   └── frontend/
│       ├── index.html                     # Patient form UI
│       ├── style.css                      # Custom styles
│       └── script.js                      # Validation, fetch, typewriter
│
├── main.py                                # Root stub (not used for lessons)
├── pyproject.toml                         # uv project config & dependencies
├── .python-version                        # Pins Python 3.13
└── README.md
```

---

## Key Rules

- **Always use `uv`** — never `pip` directly
- **Run from the project root** — relative imports and file paths depend on it
- **Data file** — `Data/patients.json` is shared across lessons 03–06

---

## Dependencies

Managed by `uv` in `pyproject.toml`:

```toml
[dependencies]
fastapi = ">=0.135.3"
uvicorn = ">=0.43.0"
pydantic = ">=2.12.5"
langchain = ">=0.3"
langchain-openai = ">=0.3"
python-dotenv = ">=1.0"
aiofiles = ">=23.0"
```

```bash
uv add <package-name>
```
