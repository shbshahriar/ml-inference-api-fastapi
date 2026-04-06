# =============================================================================
# Lesson 06 — PUT and DELETE Requests
# =============================================================================
# Covers:
#   - PUT endpoint    : update an existing patient record (partial or full)
#   - DELETE endpoint : remove a patient record by ID
#   - Optional fields : Pydantic model where every field is optional for PATCH-style PUT
#   - 404 guard       : raise HTTPException before any mutation if ID not found
#   - computed_field  : bmi and obesity auto-generated from height and weight
#
# Data source: Data/patients.json (dict keyed by patient ID e.g. "p001")
#
# Run from project root:
#   uv run uvicorn 06_put_delete_requests.put_delete_requests_api:app --reload
# =============================================================================

from fastapi import FastAPI, HTTPException, Path, Query

# pathlib.Path conflicts with fastapi.Path — aliased to avoid the name clash.
from pathlib import Path as filePath

from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()


# -----------------------------------------------------------------------------
# BMI Helpers
# -----------------------------------------------------------------------------

def compute_bmi(height: float, weight: float) -> float:
    # Formula: weight(kg) / (height(m))^2
    return round(weight / (height / 100) ** 2, 2)


def compute_obesity(bmi: float) -> str:
    # WHO BMI classification.
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


# -----------------------------------------------------------------------------
# Pydantic Models
# -----------------------------------------------------------------------------

class Patient(BaseModel):
    """
    Request body schema for POST /create.

    All fields are required. Pydantic validates types and constraints before
    the endpoint function runs — invalid input returns 422 automatically.
    bmi and obesity are computed from height and weight; the client never sends them.
    """

    id: Annotated[str, Field(
        ...,
        title="Patient ID",
        description="Unique patient ID, e.g. p001",
        json_schema_extra={"example": "p001"}
    )]

    name: Annotated[str, Field(
        ...,
        title="Patient Name",
        description="Full name of the patient",
        json_schema_extra={"example": "John Doe"}
    )]

    age: Annotated[int, Field(
        ...,
        title="Patient Age",
        description="Age of the patient (1–120)",
        gt=0, lt=120,
        json_schema_extra={"example": 30}
    )]

    city: Annotated[str, Field(
        ...,
        title="Patient City",
        description="City of the patient",
        json_schema_extra={"example": "New York"}
    )]

    gender: Annotated[Literal["male", "female"], Field(
        ...,
        title="Patient Gender",
        description="Gender: male or female",
        json_schema_extra={"example": "male"}
    )]

    disease: Annotated[str, Field(
        ...,
        title="Patient Disease",
        description="Disease of the patient",
        json_schema_extra={"example": "Diabetes"}
    )]

    height: Annotated[float, Field(
        ...,
        title="Patient Height",
        description="Height in cm (50–250)",
        gt=50, lt=250,
        json_schema_extra={"example": 175}
    )]

    weight: Annotated[float, Field(
        ...,
        title="Patient Weight",
        description="Weight in kg (2–300)",
        gt=2, lt=300,
        json_schema_extra={"example": 75.0}
    )]

    @computed_field
    @property
    def bmi(self) -> float:
        return compute_bmi(self.height, self.weight)

    @computed_field
    @property
    def obesity(self) -> str:
        return compute_obesity(self.bmi)


class PatientUpdate(BaseModel):
    """
    Request body schema for PUT /patient/{patient_id}.

    Every field is Optional so the client can send only the fields they want
    to change — unset fields are ignored and the existing values are kept.
    Validation constraints still apply to any field that is provided.
    """

    name: Optional[str] = Field(
        None,
        title="Patient Name",
        description="Full name of the patient",
        json_schema_extra={"example": "John Doe"}
    )

    age: Optional[int] = Field(
        None,
        title="Patient Age",
        description="Age of the patient (1–120)",
        gt=0, lt=120,
        json_schema_extra={"example": 30}
    )

    city: Optional[str] = Field(
        None,
        title="Patient City",
        description="City of the patient",
        json_schema_extra={"example": "New York"}
    )

    gender: Optional[Literal["male", "female"]] = Field(
        None,
        title="Patient Gender",
        description="Gender: male or female",
        json_schema_extra={"example": "male"}
    )

    disease: Optional[str] = Field(
        None,
        title="Patient Disease",
        description="Disease of the patient",
        json_schema_extra={"example": "Diabetes"}
    )

    height: Optional[float] = Field(
        None,
        title="Patient Height",
        description="Height in cm (50–250)",
        gt=50, lt=250,
        json_schema_extra={"example": 175}
    )

    weight: Optional[float] = Field(
        None,
        title="Patient Weight",
        description="Weight in kg (2–300)",
        gt=2, lt=300,
        json_schema_extra={"example": 75.0}
    )


# -----------------------------------------------------------------------------
# Data Helpers
# -----------------------------------------------------------------------------

def load_data() -> dict:
    """
    Load patient data from the JSON file.

    Uses filePath(__file__) to build an absolute path so the file is found
    correctly regardless of where uvicorn is started from.

    Returns:
        dict: Patient records keyed by patient ID (e.g. {"p001": {...}, ...})
    """
    path = filePath(__file__).parent.parent / "Data" / "patients.json"
    with open(path, "r") as f:
        return json.load(f)


def save_data(data: dict):
    """
    Write the updated patient dict back to patients.json.

    Args:
        data: Full patient dict after the update or deletion.
    """
    path = filePath(__file__).parent.parent / "Data" / "patients.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@app.get("/")
def hello():
    # Root endpoint — confirms the API is reachable.
    return {"message": "Patient Management System API"}


@app.get("/view")
def view_patients():
    # GET /view — returns all patients from the JSON file.
    data = load_data()
    return {"patients": data}


@app.get("/patient/{patient_id}")
def get_patient(
    patient_id: str = Path(
        ...,                                        # required — no default value
        description="Unique patient ID, e.g. p001",
        examples=["p001"]
    )
):
    """
    GET /patient/{patient_id}

    Retrieves a single patient by their ID.
    Returns 404 if the patient ID does not exist in the data.
    """
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {"patient": data[patient_id]}


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ...,                                        # required
        description="Field to sort by: name, age, gender, height, weight, city, disease",
        examples=["age"]
    ),
    order: str = Query(
        "desc",                                     # default value
        description="Sort order: asc (low to high) or desc (high to low)",
        examples=["desc", "asc"]
    )
):
    """
    GET /sort?sort_by=age&order=asc

    Sorts the full patient list by any allowed field.
    Raises 400 if sort_by or order values are not in the allowed list.
    """
    data = load_data()

    # Validate sort_by against allowed fields to prevent KeyError on the sort.
    allowed_fields = ["name", "age", "gender", "height", "weight", "city", "disease", "bmi", "obesity"]
    if sort_by not in allowed_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Allowed: {allowed_fields}")

    # Validate order direction.
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Use 'asc' or 'desc'.")

    # Sort the dict values (patient records) by the requested field.
    reverse = (order == "desc")
    sorted_patients = sorted(data.values(), key=lambda x: x[sort_by], reverse=reverse)

    return {"sorted_patients": sorted_patients}


@app.post("/create")
def create_patient(patient: Patient):
    """
    POST /create

    Accepts a JSON request body validated against the Patient model.
    FastAPI reads and validates the body automatically — the function
    receives a fully typed Patient object, not raw JSON.

    Steps:
        1. Load existing records from patients.json.
        2. Reject the request if the patient ID already exists (400).
        3. Serialize the model — id is used as the dict key so it is excluded
           from the stored value to avoid duplication.
        4. Save the updated dict back to patients.json.
    """
    data = load_data()

    # Duplicate check — patient IDs must be unique across the database.
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")

    # model_dump() serializes the Pydantic model to a plain dict.
    # exclude={"id"} omits the ID because it is already used as the dict key.
    # bmi and obesity are computed fields — they are included automatically.
    data[patient.id] = patient.model_dump(exclude={"id"})
    save_data(data)

    return {"message": "Patient created successfully"}


@app.put("/patient/{patient_id}")
def update_patient(
    patient: PatientUpdate,
    patient_id: str = Path(
        ...,
        description="Unique patient ID of the patient to update, e.g. p001",
        examples=["p001"]
    )
):
    """
    PUT /patient/{patient_id}

    Partially updates an existing patient record.
    Only the fields included in the request body are updated —
    omitted fields retain their existing values.

    Steps:
        1. Load existing records.
        2. Return 404 if the patient ID does not exist.
        3. Merge only the provided (non-None) fields into the existing record.
        4. Recompute bmi and obesity if height or weight changed.
        5. Save the updated dict back to patients.json.
    """
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing = data[patient_id]

    # model_dump(exclude_unset=True) returns only the fields the client actually sent,
    # so unset optional fields don't overwrite existing values with None.
    updates = patient.model_dump(exclude_unset=True)
    existing.update(updates)

    # Recompute bmi and obesity whenever height or weight is part of the update.
    # The stored values are static — they must be recalculated manually after a merge.
    if "height" in updates or "weight" in updates:
        bmi = compute_bmi(existing["height"], existing["weight"])
        existing["bmi"]     = bmi
        existing["obesity"] = compute_obesity(bmi)

    data[patient_id] = existing
    save_data(data)

    return {"message": "Patient updated successfully"}


@app.delete("/patient/{patient_id}")
def delete_patient(
    patient_id: str = Path(
        ...,
        description="Unique patient ID of the patient to delete, e.g. p001",
        examples=["p001"]
    )
):
    """
    DELETE /patient/{patient_id}

    Removes a patient record by ID.
    Returns 404 if the patient does not exist.
    """
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Remove the patient from the dict and persist the change.
    del data[patient_id]
    save_data(data)

    return {"message": f"Patient {patient_id} deleted successfully"}
