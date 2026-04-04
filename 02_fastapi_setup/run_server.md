# Running the First FastAPI Server

This guide explains how to start and test your first FastAPI application.

---

## Step 1: Install Dependencies

Install FastAPI and Uvicorn using uv:

uv add fastapi
uv add uvicorn
uv add pydantic

---

## Step 2: Start the Server

Run the application:

uv run python 02_fastapi_setup/first_app.py


Alternatively, you can start the server using Uvicorn directly:

uv run uvicorn 02_fastapi_setup.first_app:app --reload

---

## Step 3: Open the API in Browser

Visit:

http://127.0.0.1:8000

Expected response:

{"message": "FastAPI server is running"}

---

## Step 4: Open Interactive API Documentation

FastAPI automatically generates documentation here:

http://127.0.0.1:8000/docs

Use this page to test endpoints directly from the browser.

---

## Step 5: Stop the Server

Press:

CTRL + C

to stop the running server.