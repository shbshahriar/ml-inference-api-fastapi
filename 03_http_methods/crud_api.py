# =============================================================================
# Lesson 03 — HTTP Methods (CRUD)
# =============================================================================
# Covers:
#   - GET    : Retrieve all patients
#   - POST   : Add a new patient
#   - PUT    : Update an existing patient
#   - DELETE : Remove a patient
#
# Data source: Data/patients.json (dict keyed by patient ID e.g. "p001")
#
# Run from project root:
#   uv run uvicorn 03_http_methods.crud_api:app --reload
# =============================================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json
from typing import List

app = FastAPI()


# -----------------------------------------------------------------------------
# Data Loader
# -----------------------------------------------------------------------------

def load_data() -> dict:
    """
    Load patient data from the JSON file.

    Uses Path(__file__) to build an absolute path so the file is found
    correctly regardless of where uvicorn is started from.
    """
    path = Path(__file__).parent.parent / "Data" / "patients.json"
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
