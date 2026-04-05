# =============================================================================
# Lesson 04 — Path & Query Parameters
# =============================================================================
# Covers:
#   - Path parameters  : identify a specific resource  e.g. /patient/p001
#   - Query parameters : control how to retrieve data  e.g. /sort?sort_by=age
#   - Path()  : adds description, example, and validation to path params
#   - Query() : adds description, example, and allowed values to query params
#   - HTTPException : returns proper error responses (400, 404, etc.)
#
# Data source: Data/patients.json (dict keyed by patient ID e.g. "p001")
#
# Run from project root:
#   uv run uvicorn 04_path_query_params.path_query_api:app --reload
# =============================================================================

from fastapi import FastAPI, HTTPException, Path, Query

# pathlib.Path conflicts with fastapi.Path — aliased to avoid the name clash.
from pathlib import Path as filePath

import json

app = FastAPI()


# -----------------------------------------------------------------------------
# Data Loader
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
        ...,                                            # required — no default value
        description="Unique patient ID, e.g. p001",
        examples=["p001"]
    )
):
    """
    GET /patient/{patient_id}

    Path parameter example — retrieves a single patient by their ID.
    The ID is part of the URL itself, which is the standard REST pattern
    for identifying one specific resource.

    Returns 404 if the patient ID does not exist in the data.
    """
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {"patient": data[patient_id]}


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ...,                                                            # required
        description="Field to sort by: name, age, gender, height, weight, city, disease",
        examples=["age"]
    ),
    order: str = Query(
        "desc",                                                         # default value
        description="Sort order: asc (low to high) or desc (high to low)",
        examples=["desc", "asc"]
    )
):
    """
    GET /sort?sort_by=age&order=asc

    Query parameter example — sorts the full patient list by any field.
    Query params appear after '?' in the URL and control *how* data is
    returned, not *which* resource to target (that's what path params are for).

    Raises 400 Bad Request if sort_by or order values are not in the allowed list.
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
