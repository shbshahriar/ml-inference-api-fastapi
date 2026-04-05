# POST Requests — Lesson 05

## Run the Server

```bash
uv run uvicorn 05_post_requests.post_requests_api:app --reload
```

| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:8000` | Live API |
| `http://127.0.0.1:8000/docs` | Interactive Swagger UI — try the POST endpoint here |

Press `Ctrl+C` to stop.

---

## Objective

- Send data to the server using a POST request
- Understand the request body structure
- Validate incoming data using Pydantic
- Prevent duplicate patient records
- Store new data inside the JSON database
- Automatically compute BMI and obesity verdict

---

## Recap of Previous Endpoints

Lessons 03 and 04 covered data retrieval:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/view` | Return all patients |
| GET | `/patient/{patient_id}` | Return one patient by ID |
| GET | `/sort?sort_by=age&order=desc` | Return sorted patient list |

Now moving to data creation:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/create` | Add a new patient record |

---

## What is a POST Request?

POST is used to **send structured data from the client to the server** — typically to create a new resource.

```
POST /create
```

The client sends a JSON body:

```json
{
  "id": "p006",
  "name": "Rahim",
  "age": 35,
  "city": "Dhaka",
  "gender": "Male",
  "disease": "Diabetes",
  "height": 170,
  "weight": 72
}
```

The server reads, validates, and stores it.

> **Rule:** Use GET to read. Use POST to create.

---

## What is a Request Body?

The request body contains structured JSON sent by the client alongside the HTTP request.

**When to use a request body:**

| Scenario | Example |
|----------|---------|
| Creating a record | Add a new patient |
| Updating a record | Change patient details |
| Sending prediction input | Submit features for ML model |

FastAPI reads the JSON request body automatically when you declare a Pydantic model as a function argument.

---

## Creating a Pydantic Model for Validation

A Pydantic model defines the **shape, types, and constraints** of the incoming data.

```python
from pydantic import BaseModel, Field, computed_field
from typing import Annotated

class Patient(BaseModel):
    id:      Annotated[str, Field(..., title="Patient ID",      description="Unique patient ID, e.g. p001",               json_schema_extra={"example": "p001"})]
    name:    Annotated[str, Field(..., title="Patient Name",    description="Full name of the patient",                   json_schema_extra={"example": "John Doe"})]
    age:     Annotated[int, Field(..., title="Patient Age",     description="Age of the patient",                         json_schema_extra={"example": 30})]
    city:    Annotated[str, Field(..., title="Patient City",    description="City of the patient",                        json_schema_extra={"example": "New York"})]
    gender:  Annotated[str, Field(..., title="Patient Gender",  description="Gender of the patient",                      json_schema_extra={"example": "Male"})]
    disease: Annotated[str, Field(..., title="Patient Disease", description="Disease of the patient",                     json_schema_extra={"example": "Diabetes"})]
    height:  Annotated[int, Field(..., title="Patient Height",  description="Height of the patient in centimeters",       json_schema_extra={"example": 175})]
    weight:  Annotated[int, Field(..., title="Patient Weight",  description="Weight of the patient in kilograms",         json_schema_extra={"example": 75})]
```

**Why `Annotated` + `Field`?**

`Annotated[type, Field(...)]` keeps the type hint and metadata together in one place — Pydantic reads both. This is the Pydantic v2 recommended pattern.

| Part | Purpose |
|------|---------|
| `Annotated[str, ...]` | Declares the Python type |
| `Field(...)` | Adds title, description, example for Swagger |
| `json_schema_extra={"example": ...}` | Pre-fills the Swagger input box |

---

## Computed Fields — BMI and Obesity Verdict

Some fields don't come from the client — they are **calculated from other fields** inside the model.

**BMI formula:**

```
BMI = weight / (height / 100) ** 2
```

**Obesity verdict categories:**

| BMI Range | Verdict |
|-----------|---------|
| Below 18.5 | Underweight |
| 18.5 – 24.9 | Normal weight |
| 25 – 29.9 | Overweight |
| 30 and above | Obese |

Implementation using `@computed_field` and `@property`:

```python
@computed_field
@property
def bmi(self) -> float:
    return round(self.weight / (self.height / 100) ** 2, 2)

@computed_field
@property
def obesity(self) -> str:
    if self.bmi < 18.5:
        return "Underweight"
    elif 18.5 <= self.bmi < 25:
        return "Normal weight"
    elif 25 <= self.bmi < 30:
        return "Overweight"
    else:
        return "Obese"
```

The client never sends `bmi` or `obesity` — they are generated automatically from `height` and `weight` before the record is saved.

---

## Creating the POST Endpoint

```python
@app.post("/create")
def create_patient(patient: Patient):
    ...
```

FastAPI automatically:

1. Reads the JSON request body
2. Validates it against the `Patient` model
3. Converts it to a Python object

The function argument `patient: Patient` is all it takes — no manual JSON parsing.

---

## Preventing Duplicate Records

Before saving, check whether the patient ID already exists:

```python
@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")
```

**Response when duplicate is found:**

```json
{
  "detail": "Patient ID already exists"
}
```

> `400 Bad Request` — the client sent an ID that already exists in the database.

---

## Saving Data into the JSON Database

After the duplicate check, save the new record into `patients.json`:

```python
data[patient.id] = patient.model_dump(exclude={"id"})
save_data(data)
```

**Why `exclude={"id"}`?**

The patient ID is already used as the **dictionary key** (`data["p006"] = ...`). Storing it again inside the value would be redundant — so it is excluded from the saved dict.

**`save_data()` steps:**

```python
def save_data(data: dict):
    path = filePath(__file__).parent.parent / "Data" / "patients.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
```

1. Build the file path using `pathlib` — never plain relative strings
2. Open `patients.json` in write mode
3. Write the updated dict back as formatted JSON

---

## Helper: `load_data()`

```python
def load_data() -> dict:
    path = filePath(__file__).parent.parent / "Data" / "patients.json"
    with open(path, "r") as f:
        return json.load(f)
```

> `filePath` is an alias for `pathlib.Path` — avoids a name conflict with `fastapi.Path`.

---

## Complete Implementation Workflow

```
Client sends POST /create with JSON body
        ↓
FastAPI validates using Patient model
        ↓
Check if patient.id already exists in data
        ↓
    Exists? → 400 Bad Request
        ↓
Compute bmi and obesity (computed fields)
        ↓
Save record to patients.json (id used as key, excluded from value)
        ↓
Return success response
```

---

## Testing POST Endpoint using Swagger UI

1. Open `http://127.0.0.1:8000/docs`
2. Find **POST /create** and click it
3. Click **Try it out**
4. Paste an example request body:

```json
{
  "id": "p006",
  "name": "Rahim",
  "age": 35,
  "city": "Dhaka",
  "gender": "Male",
  "disease": "Diabetes",
  "height": 170,
  "weight": 72
}
```

5. Click **Execute**

Verify the new record exists by calling:

```
GET /view
```

The new patient should appear with `bmi` and `obesity` fields included — even though you never sent them.

---

## Summary

After completing this lesson you can:

- Send data to a FastAPI endpoint using a POST request
- Define the request body using a Pydantic model with `Annotated` + `Field`
- Add Swagger metadata (`title`, `description`, `example`) per field
- Generate computed fields (`bmi`, `obesity`) automatically from input
- Prevent duplicate records with a `400 Bad Request` response
- Save structured data to a local JSON file using `pathlib`
- Test POST endpoints using Swagger UI

---

## What's Next

Lesson 06 — PUT and DELETE Requests: updating and removing existing patient records.
