# FastAPI Setup — Lesson 02

## Run the Server

```bash
uv run uvicorn 02_fastapi_setup.first_app:app --reload
```

| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:8000` | Live API |
| `http://127.0.0.1:8000/docs` | Interactive Swagger UI |

Press `Ctrl+C` to stop.

---

## Objective

- Install FastAPI and Uvicorn via `uv`
- Write your first FastAPI app (`first_app.py`)
- Start the development server with hot-reload
- Understand the project's module path convention

---

## Step 1 — Install Dependencies

```bash
uv add fastapi
uv add uvicorn
uv add pydantic
```

`uv` manages the virtual environment automatically under `.venv/`.  
Never use `pip` in this project.

---

## Step 2 — Write the First App

**File:** `02_fastapi_setup/first_app.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI server is running"}
```

Three things every FastAPI file needs:

| Part | What it does |
|------|-------------|
| `FastAPI()` | Creates the application instance |
| `@app.get("/")` | Registers a route for GET / |
| `return {...}` | FastAPI converts the dict to JSON automatically |

---

## Step 3 — Start the Server

```bash
uv run uvicorn 02_fastapi_setup.first_app:app --reload
```

**Module path convention:**

```
02_fastapi_setup.first_app : app
│                │            │
folder           file         FastAPI object name
```

`--reload` restarts the server automatically whenever you save a file.

---

## Step 4 — Test in Browser

Visit `http://127.0.0.1:8000`

Expected response:

```json
{"message": "FastAPI server is running"}
```

---

## Step 5 — Explore the Auto Docs

FastAPI generates interactive docs with zero configuration.

- **Swagger UI** → `http://127.0.0.1:8000/docs`  
  Test every endpoint from the browser. No Postman needed.

- **ReDoc** → `http://127.0.0.1:8000/redoc`  
  Cleaner read-only documentation view.

---

## Key Concepts

| Concept | Explanation |
|---------|-------------|
| `uvicorn` | ASGI server that runs FastAPI |
| `--reload` | Hot-reload for development only |
| Auto docs | Generated from your code — always in sync |
| `uv run` | Runs commands inside the managed `.venv` |

---

## What's Next

Lesson 03 — HTTP Methods (GET, POST, PUT, DELETE) with a Patient Management API.
