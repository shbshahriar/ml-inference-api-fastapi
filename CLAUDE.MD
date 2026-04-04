# claude.md

## Project Overview

This project follows the CampusX FastAPI for Machine Learning deployment curriculum.

Claude must generate explanations and code strictly limited to the following topics:

1. What is an API
2. FastAPI philosophy and setup
3. HTTP methods in FastAPI
4. Path parameters and query parameters
5. POST request handling
6. PUT and DELETE requests
7. Serving machine learning models with FastAPI
8. Improving FastAPI APIs
9. Docker for machine learning
10. Dockerizing FastAPI applications
11. Deploying FastAPI APIs on AWS

Pydantic explanations must not be included unless explicitly requested.

Package installation must use uv instead of pip.

Do not introduce additional frameworks or topics outside this curriculum.

---

## Environment Setup Rules

Claude must use:

uv add fastapi
uv add uvicorn

Do not use pip.

Server execution must use:

uv run uvicorn main:app --reload

---

## API Fundamentals

Claude should explain:

- what an API is
- how clients communicate with servers
- request–response cycle basics
- role of APIs in machine learning deployment

Examples must remain beginner-friendly and practical.

---

## FastAPI Setup and Philosophy

Claude should demonstrate:

- creating a FastAPI application
- running a FastAPI server
- defining basic routes
- returning JSON responses

Example structure:

@app.get("/")
def home():
    return {"message": "Hello World"}

Avoid introducing alternative backend frameworks.

---

## HTTP Methods in FastAPI

Claude should support usage of:

GET → retrieve data  
POST → create predictions  
PUT → update data  
DELETE → remove data

Examples must follow REST-style usage.

---

## Path and Query Parameters

Claude should demonstrate:

path parameter example:

/predict/123

query parameter example:

/predict?age=25

Explain when to use each type.

---

## POST Request Handling

Claude should demonstrate:

- request body handling
- sending JSON input
- receiving structured prediction data
- returning JSON output

Prediction-style endpoint example:

@app.post("/predict")

Return format example:

{"prediction": result}

---

## PUT and DELETE Requests

Claude should demonstrate:

PUT request usage for updating resources

DELETE request usage for removing resources

Examples must remain simple and API-focused.

---

## Serving Machine Learning Models

Claude should demonstrate:

- loading trained models
- using pickle
- using joblib
- running model.predict()
- returning prediction responses

Prediction workflow:

Receive request → prepare input → run prediction → return JSON result

Do not introduce alternative serialization tools.

---

## Improving FastAPI APIs

Claude should support:

clean route structure

clear response formatting

organized endpoint logic

readable API design

Avoid introducing unrelated optimization frameworks.

---

## Docker for Machine Learning

Claude should demonstrate:

creating Dockerfile

building Docker image

running container locally

Example commands:

docker build -t ml-api

docker run -p 8000:8000 ml-api

No advanced Docker orchestration topics allowed.

---

## Dockerizing FastAPI Applications

Claude should demonstrate:

containerizing FastAPI apps

running FastAPI inside Docker

exposing API ports correctly

Examples must remain beginner-friendly.

---

## Deploying FastAPI APIs on AWS

Claude should explain:

basic FastAPI deployment workflow on AWS

running production server using:

uv run uvicorn main:app --host 0.0.0.0 --port 8000

Avoid introducing infrastructure automation tools.