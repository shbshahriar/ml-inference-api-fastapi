# =============================================================================
# Lesson 02 — First FastAPI App
# =============================================================================
# Covers:
#   - Creating a FastAPI app instance
#   - Defining a basic GET route
#   - Running the server programmatically with uvicorn
#
# Run from project root:
#   uv run uvicorn 02_fastapi_setup.first_app:app --reload
# =============================================================================

from fastapi import FastAPI
import uvicorn

# Create the FastAPI application instance.
# All routes are registered on this object using decorators.
app = FastAPI()


@app.get("/")
def home():
    # Root endpoint — used to verify the server is running.
    # Returns a simple JSON response.
    return {"message": "FastAPI server is running"}


# Allows running the file directly with: python first_app.py
# When using uvicorn via CLI (recommended), this block is not executed.
if __name__ == "__main__":
    uvicorn.run(
        "first_app:app",  # module:app_instance
        host="127.0.0.1",
        port=8000,
        reload=True       # auto-restart on code changes (dev only)
    )
