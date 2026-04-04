# Path & Query Parameters — Lesson 04

## Run the Server

```bash
uv run uvicorn 04_path_query_params.path_query_api:app --reload
```

| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:8000` | Live API |
| `http://127.0.0.1:8000/docs` | Interactive Swagger UI — shows dropdowns from `Query(enum=...)` |

Press `Ctrl+C` to stop.

---

## Objective

- Retrieve a single patient using a path parameter (ID in the URL)
- Filter and sort patients using optional query parameters
- Return correct HTTP status codes instead of misleading responses
- Improve Swagger documentation using `Path()` and `Query()`

---

## Path Parameters

Used to **identify one specific resource** — the value is embedded in the URL path.

```
/patient/P001
         ^^^^
         path parameter value
```

FastAPI syntax — curly braces in the route string, matching argument name in the function:

```python
@app.get("/patient/{patient_id}")
def get_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    return data[patient_id]
```

FastAPI extracts the value automatically and passes it as a function argument.

**Common use cases:**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/patient/{id}` | Retrieve a patient |
| PUT | `/patient/{id}` | Update a patient |
| DELETE | `/patient/{id}` | Delete a patient |

> **Rule:** Use a path parameter when the value *identifies which resource* you are acting on.

---

## Using Path() for Documentation

`Path()` improves Swagger by adding descriptions, example values, and validation — all auto-rendered in the docs.

```python
from fastapi import FastAPI, Path, HTTPException

@app.get("/patient/{patient_id}")
def get_patient(
    patient_id: str = Path(
        ...,
        description="Unique patient ID, e.g. P001",
        example="P001",
        min_length=2,
        max_length=10
    )
):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    return data[patient_id]
```

**Path() arguments:**

| Argument | Purpose |
|----------|---------|
| `...` | Required field (use a value here to set a default) |
| `description` | Text shown next to the field in Swagger |
| `example` | Pre-fills the input box so testers don't have to guess |
| `min_length` / `max_length` | FastAPI validates before your function runs |

---

## HTTP Status Codes

Return the right code so clients know exactly what happened.

| Code | Name | When to use |
|------|------|-------------|
| `200` | OK | Successful GET, PUT, DELETE |
| `201` | Created | Successful POST (new resource added) |
| `204` | No Content | Successful DELETE with no response body |
| `301` | Moved Permanently | Resource URL has permanently changed |
| `302` | Found | Temporary redirect to another URL |
| `304` | Not Modified | Cached response is still valid, no data sent |
| `400` | Bad Request | Client sent invalid or malformed data |
| `401` | Unauthorized | Not authenticated — login required |
| `403` | Forbidden | Authenticated but not allowed to access this resource |
| `404` | Not Found | Resource does not exist |
| `405` | Method Not Allowed | HTTP method not supported on this route |
| `409` | Conflict | Request conflicts with current state (e.g. duplicate entry) |
| `422` | Unprocessable Entity | FastAPI validation failed (wrong type, missing field) |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Unhandled exception on the server |
| `502` | Bad Gateway | Upstream server returned invalid response |
| `503` | Service Unavailable | Server is down or overloaded |

**Why it matters — bad vs good:**

```python
# Wrong — returns empty dict, client is confused
return {}

# Correct — raises 404 with a clear message
raise HTTPException(status_code=404, detail="Patient not found")
```

Usage:

```python
from fastapi import HTTPException

if patient_id not in data:
    raise HTTPException(status_code=404, detail="Patient not found")
```

---

## Query Parameters

Optional key-value pairs appended after `?` in the URL. They don't change *which* resource you access — they change *how* you access it.

```
/patients?sort_by=age&order=asc
          ^^^^^^^^^^^^^^^^^^^
          query parameters
```

**Structure:** `URL?key=value&key=value`

FastAPI auto-detects query params — any function argument that is **not** a path segment becomes a query parameter:

```python
@app.get("/patients")
def sort_patients(
    sort_by: str = "age",
    order: str = "asc"
):
    data = load_data()
    patients = list(data.values())
    reverse = (order == "desc")
    patients.sort(key=lambda p: p.get(sort_by, ""), reverse=reverse)
    return patients
```

**Use cases:**

| Purpose | Example |
|---------|---------|
| Sorting | `?sort_by=age&order=asc` |
| Filtering | `?city=New+York` |
| Searching | `?disease=diabetes` |

> **Rule:** Use a query parameter when the value controls *how* to retrieve a collection — not which single resource to target.

---

## Using Query() for Validation

`Query()` adds default values, allowed choices, and descriptions to query parameters.

```python
from fastapi import Query

@app.get("/patients")
def sort_patients(
    sort_by: str = Query(
        "age",
        description="Field to sort by: age, name, city",
        enum=["age", "name", "city"]
    ),
    order: str = Query(
        "asc",
        description="Sort order: asc or desc",
        enum=["asc", "desc"]
    )
):
    data = load_data()
    patients = list(data.values())
    reverse = (order == "desc")
    patients.sort(key=lambda p: p.get(sort_by, ""), reverse=reverse)
    return patients
```

**Query() arguments:**

| Argument | Purpose |
|----------|---------|
| `"age"` (first positional) | Default value used when the client omits the parameter |
| `description` | Shown in Swagger next to the field |
| `enum` | Restricts to a fixed list — Swagger renders this as a **dropdown** |

**Example requests:**

```bash
GET /patients                          # uses defaults: sort_by=age, order=asc
GET /patients?sort_by=age&order=asc    # sort by age, ascending
GET /patients?sort_by=name&order=desc  # sort by name, descending
```

---

## Path vs Query — Quick Rule

| Question | Use |
|----------|-----|
| Which patient? `/patient/P001` | Path parameter |
| How to list them? `/patients?sort_by=age` | Query parameter |

---

## What's Next

Lesson 05 — POST Requests: handling request bodies with Pydantic models.
