# PUT and DELETE Requests — Lesson 06

## Run the Server

```bash
uv run uvicorn 06_put_delete_requests.put_delete_requests_api:app --reload
```

| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:8000` | Live API |
| `http://127.0.0.1:8000/docs` | Interactive Swagger UI — try PUT and DELETE here |

Press `Ctrl+C` to stop.

---

## Objective

- Update existing patient records using PUT
- Handle partial updates safely — only change what the client sends
- Validate update requests using Pydantic
- Recompute BMI and obesity verdict when height or weight changes
- Delete patient records using DELETE
- Return correct error responses when records do not exist

---

## Recap of Previous Endpoints

Lessons 03–05 covered retrieval and creation:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/view` | Return all patients |
| GET | `/patient/{patient_id}` | Return one patient by ID |
| GET | `/sort?sort_by=age&order=desc` | Return sorted patient list |
| POST | `/create` | Add a new patient record |

Now completing CRUD with:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| PUT | `/patient/{patient_id}` | Update an existing patient |
| DELETE | `/patient/{patient_id}` | Remove a patient record |

---

## What is a PUT Request?

PUT is used to **update an existing resource** on the server.

```
PUT /patient/p006
```

The client sends only the fields they want to change:

```json
{
  "weight": 78,
  "city": "Dhaka"
}
```

The server merges those changes into the existing record and saves.

> **Rule:** Use POST to create. Use PUT to update.

---

## Why Partial Updates Need Special Handling

A patient record has many fields — name, age, city, disease, height, weight, etc.
The client should be able to update just one field without resending all the others.

**Problem with a standard required model:**

```
client sends only weight → all other fields would be missing → 422 error
```

**Solution:** make every field in the update model `Optional` with a default of `None`.

---

## Creating the PatientUpdate Model

```python
from typing import Optional

class PatientUpdate(BaseModel):
    name:    Optional[str]                       = Field(None, ...)
    age:     Optional[int]                       = Field(None, gt=0, lt=120, ...)
    city:    Optional[str]                       = Field(None, ...)
    gender:  Optional[Literal["male", "female"]] = Field(None, ...)
    disease: Optional[str]                       = Field(None, ...)
    height:  Optional[float]                     = Field(None, gt=50, lt=250, ...)
    weight:  Optional[float]                     = Field(None, gt=2,  lt=300, ...)
```

Key points:

| Point | Why |
|-------|-----|
| All fields are `Optional` | Client can omit any field |
| Default is `None` | Unset fields won't appear in the serialized output |
| Validation constraints still apply | A provided value is still validated before the update runs |

---

## Ignoring Unset Fields During Update

`model_dump(exclude_unset=True)` returns **only the fields the client actually sent** — fields the client omitted are not included at all, so they don't overwrite existing values with `None`.

```python
updates = patient.model_dump(exclude_unset=True)
existing.update(updates)
```

**Example:**

Client sends `{"weight": 78}` → `updates = {"weight": 78}` → only weight is changed.

---

## Recomputing BMI and Obesity After Update

`bmi` and `obesity` are stored as plain values in the JSON file — they are not recalculated automatically when the record is modified.

If `height` or `weight` changes, they must be recomputed manually:

```python
if "height" in updates or "weight" in updates:
    bmi = compute_bmi(existing["height"], existing["weight"])
    existing["bmi"]     = bmi
    existing["obesity"] = compute_obesity(bmi)
```

`compute_bmi()` and `compute_obesity()` are standalone helper functions defined at the top of the file — the `Patient` model uses the same helpers, so the logic is never duplicated.

---

## Creating the PUT Endpoint

```python
@app.put("/patient/{patient_id}")
def update_patient(
    patient: PatientUpdate,
    patient_id: str = Path(...)
):
```

**Steps:**

1. Load existing records from `patients.json`
2. Return `404` if the patient ID does not exist
3. Merge only the provided fields using `model_dump(exclude_unset=True)`
4. Recompute `bmi` and `obesity` if `height` or `weight` changed
5. Save the updated record back to `patients.json`

---

## What is a DELETE Request?

DELETE **permanently removes a resource** from the server.

```
DELETE /patient/p006
```

No request body is needed — the ID in the URL path is enough to identify the record.

> **Rule:** Always check the record exists before deleting — never silently succeed on a missing ID.

---

## Creating the DELETE Endpoint

```python
@app.delete("/patient/{patient_id}")
def delete_patient(
    patient_id: str = Path(...)
):
```

**Steps:**

1. Load existing records
2. Return `404` if the patient ID does not exist
3. `del data[patient_id]`
4. Save the updated dict back to `patients.json`
5. Return a confirmation message

---

## Error Handling

Both PUT and DELETE validate the patient ID before making any changes:

```python
if patient_id not in data:
    raise HTTPException(status_code=404, detail="Patient not found")
```

**Example — invalid ID:**

```
PUT  /patient/p999  →  404 Patient not found
DELETE /patient/p999  →  404 Patient not found
```

This prevents silent failures and gives the client a clear, actionable response.

---

## Testing PUT and DELETE using Swagger UI

**Test PUT:**

1. Open `http://127.0.0.1:8000/docs`
2. Find **PUT /patient/{patient_id}**, click **Try it out**
3. Enter a valid patient ID (e.g. `p001`)
4. Send a partial body:

```json
{
  "weight": 90,
  "height": 165
}
```

5. Verify the update — call `GET /patient/p001` and confirm `bmi` and `obesity` reflect the new values

**Test DELETE:**

1. Find **DELETE /patient/{patient_id}**, click **Try it out**
2. Enter the patient ID to remove (e.g. `p006`)
3. Execute — then call `GET /view` to confirm the record is gone

---

## Summary

After completing this lesson you can:

- Update records using PUT with partial request bodies
- Use `Optional` fields in Pydantic to allow flexible updates
- Use `model_dump(exclude_unset=True)` to ignore fields the client did not send
- Recompute derived fields (`bmi`, `obesity`) after a partial update
- Delete records using DELETE with a 404 guard
- Return correct HTTP error responses for missing resources
- Complete the full CRUD cycle: Create → Read → Update → Delete

---

## What's Next

Lesson 07 — Serving ML Models: load a trained model, accept prediction input, and return results as a JSON response.
