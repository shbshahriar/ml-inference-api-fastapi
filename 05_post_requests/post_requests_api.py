from fastapi import FastAPI, HTTPException, Path, Query
from pathlib import Path as filePath
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id:      Annotated[str,             Field(..., title="Patient ID",      description="Unique patient ID, e.g. p001",         json_schema_extra={"example": "p001"})]
    name:    Annotated[str,             Field(..., title="Patient Name",    description="Full name of the patient",             json_schema_extra={"example": "John Doe"})]
    age:     Annotated[int,             Field(..., title="Patient Age",     description="Age of the patient (1–120)",           gt=0, lt=120,  json_schema_extra={"example": 30})]
    city:    Annotated[str,             Field(..., title="Patient City",    description="City of the patient",                  json_schema_extra={"example": "New York"})]
    gender:  Annotated[Literal["male", "female"], Field(..., title="Patient Gender",  description="Gender: male or female",               json_schema_extra={"example": "male"})]
    disease: Annotated[str,             Field(..., title="Patient Disease", description="Disease of the patient",               json_schema_extra={"example": "Diabetes"})]
    height:  Annotated[float,           Field(..., title="Patient Height",  description="Height in cm (50–250)",                gt=50, lt=250, json_schema_extra={"example": 175})]
    weight:  Annotated[float,           Field(..., title="Patient Weight",  description="Weight in kg (2–300)",                 gt=2,  lt=300, json_schema_extra={"example": 75.0})]

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

def load_data() -> dict:
    path = filePath(__file__).parent.parent / "Data" / "patients.json"
    with open(path, "r") as f:
        return json.load(f)

def save_data(data: dict):
    path = filePath(__file__).parent.parent / "Data" / "patients.json"
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


@app.get("/view")
def view_patients():
    data = load_data()
    return {"patients": data}


@app.get("/patient/{patient_id}")
def get_patient(
    patient_id: str = Path(
        ...,
        description="Unique patient ID, e.g. p001",
        examples=["p001"]
    )
):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    return {"patient": data[patient_id]}


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ...,
        description="Field to sort by: name, age, gender, height, weight, city, disease",
        examples=["age"]
    ),
    order: str = Query(
        "desc",
        description="Sort order: asc (low to high) or desc (high to low)",
        examples=["desc", "asc"]
    )
):
    data = load_data()
    allowed_fields = ["name", "age", "gender", "height", "weight", "city", "disease", "bmi", "obesity"]
    if sort_by not in allowed_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. Allowed: {allowed_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Use 'asc' or 'desc'.")
    reverse = (order == "desc")
    sorted_patients = sorted(data.values(), key=lambda x: x[sort_by], reverse=reverse)

    return {"sorted_patients": sorted_patients}

@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient ID already exists")
    else:
        data[patient.id] = patient.model_dump(exclude={"id"})
        save_data(data)
        return HTTPException(status_code=201, detail="Patient created successfully")