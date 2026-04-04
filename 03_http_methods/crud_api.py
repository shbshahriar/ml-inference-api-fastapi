from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import json
from typing import List

app = FastAPI()

def load_data():
    path = Path(__file__).parent.parent / "Data" / "patients.json"
    with open(path, "r") as f:
        return json.load(f)

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/view")
def view_patients():
    data = load_data()
    return {"patients": data}

