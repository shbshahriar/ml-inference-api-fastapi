# HTTP Methods — Lesson 03

## Run the Server

```bash
uv run uvicorn 03_http_methods.crud_api:app --reload
```

| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:8000` | Live API |
| `http://127.0.0.1:8000/docs` | Interactive Swagger UI |

Press `Ctrl+C` to stop.

---

## Objective

- Build a **Patient Management API** with full CRUD
- Understand how CRUD operations map to HTTP methods
- Read and write patient data from a JSON file
- Return correct HTTP status codes

---

## Problem Statement

Doctors store prescriptions on paper → records get lost, can't be searched, can't be shared.

**Solution:** A REST API where staff can add, view, update, and delete patient records digitally.

---

## CRUD → HTTP Mapping

Every dynamic application performs these four operations internally.

| CRUD | HTTP Method | What it does |
|------|-------------|--------------|
| Create | `POST` | Send data to create a new resource |
| Retrieve | `GET` | Fetch data from the server |
| Update | `PUT` | Modify an existing resource |
| Delete | `DELETE` | Remove a resource permanently |

**Real-world examples:**

| App | Create | Retrieve | Update | Delete |
|-----|--------|----------|--------|--------|
| Instagram | Upload post | View feed | Edit caption | Delete post |
| Excel | Add row | View sheet | Edit cell | Remove row |
| Hospital | Register patient | View record | Update prescription | Discharge patient |

---

## API Endpoints

| Method | Endpoint | Action | Status |
|--------|----------|--------|--------|
| `GET` | `/view` | Return all patients | 200 |
| `GET` | `/view/{id}` | Return one patient by ID | 200 / 404 |
| `POST` | `/create` | Add a new patient | 201 |
| `PUT` | `/update/{id}` | Update an existing patient | 200 / 404 |
| `DELETE` | `/delete/{id}` | Remove a patient | 200 / 404 |

`{id}` is a **path parameter** — FastAPI extracts it from the URL automatically.

---

## JSON as a Database

Instead of SQL, we use a flat file for simplicity.

**File:** `03_http_methods/patients.json`

```json
{
  "p001": {
    "name": "John Doe",
    "age": 45,
    "city": "New York",
    "gender": "male",
    "disease": "Diabetes",
    "height": 175,
    "weight": 80
  },
  "p002": {
    "name": "Jane Smith",
    "age": 32,
    "city": "Los Angeles",
    "gender": "female",
    "disease": "Hypertension",
    "height": 162,
    "weight": 65
  }
}
```

**Why JSON?** Simple, human-readable, zero setup. Not for production — use a proper database there.

Helper functions used in every route:

```python
import json

def load_data():
    with open("patients.json", "r") as f:
        return json.load(f)

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=2)
```

---

## GET — Retrieve Data

Safe and idempotent. Never modifies data.

```python
# All patients
@app.get("/view")
def view_patients():
    return load_data()

# One patient
@app.get("/view/{patient_id}")
def view_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    return data[patient_id]
```

---

## POST — Create Data

Not idempotent — calling twice with the same ID causes an error.

```python
@app.post("/create", status_code=201)
def create_patient(patient_id: str, patient: Patient):
    data = load_data()
    if patient_id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")
    data[patient_id] = patient.model_dump()
    save_data(data)
    return {"message": "Patient created"}
```

Request body example:

```json
{
  "name": "Alice Brown",
  "age": 28,
  "city": "Chicago",
  "gender": "female",
  "disease": "Asthma",
  "height": 160,
  "weight": 58
}
```

---

## PUT — Update Data

Idempotent — calling the same PUT 10 times gives the same result.

```python
@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient: Patient):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    data[patient_id] = patient.model_dump()
    save_data(data)
    return {"message": "Patient updated"}
```

PUT replaces the **entire record**. Send all fields, not just the changed one.

---

## DELETE — Remove Data

Permanent. No recovery from a JSON file.

```python
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    del data[patient_id]
    save_data(data)
    return {"message": "Patient deleted"}
```

No request body needed — just the ID in the URL.

---

## Quick Reference

| Method | Idempotent | Safe | Typical Status |
|--------|------------|------|----------------|
| GET | Yes | Yes | 200 |
| POST | No | No | 201 |
| PUT | Yes | No | 200 |
| DELETE | Yes | No | 200 |

**Common status codes:**

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Resource created |
| 400 | Bad request (client error) |
| 404 | Resource not found |
| 500 | Server error |

---

## What's Next

Lesson 04 — Path & Query Parameters: filter, sort, and document your API.
