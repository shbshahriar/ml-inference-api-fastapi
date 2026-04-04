from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import List

app = FastAPI()

def load_data():
    with open("03_http_methods/patients.json", "r") as f:
        return json.load(f)

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/view")
def view_patients():
    data = load_data()
    return {"patients": data}

