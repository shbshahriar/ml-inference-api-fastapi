from fastapi import FastAPI, HTTPException,Path
from pathlib import Path as filePath
import json

app = FastAPI()

def load_data():
    path = filePath(__file__).parent.parent / "Data" / "patients.json"
    with open(path, "r") as f:
        return json.load(f)

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/view")
def view_patients():
    data = load_data()
    return {"patients": data}

@app.get('/patient/{patient_id}')
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve",example="p001")):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"patient": data[patient_id]}
