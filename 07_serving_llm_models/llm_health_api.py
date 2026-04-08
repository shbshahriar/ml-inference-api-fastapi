# =============================================================================
# Lesson 07 — Serving an LLM with FastAPI + LangChain
# =============================================================================
# Covers:
#   - Integrating LangChain + langchain-openai with FastAPI
#   - Structured request body validation via Pydantic (ChatMessage schema)
#   - Prompt engineering : system prompt (persona) + dynamic user prompt
#   - CORS middleware     : allows the browser frontend to call the API
#   - StaticFiles        : serves the HTML/CSS/JS frontend from the same server
#   - Environment config : API key and model name loaded from a .env file
#
# Run from the project root:
#   uv run uvicorn 07_serving_llm_models.llm_health_api:app --reload
#
# Then open: http://127.0.0.1:8000
# =============================================================================

import sys
from pathlib import Path

# Add this file's directory to sys.path so Python can find schema.py,
# prompts.py, and utils.py when uvicorn is launched from the project root.
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

from schema import ChatMessage
from prompts import SYSTEM_PROMPT, build_user_prompt

# Load environment variables from the .env file in this folder.
# Using an explicit path ensures the file is found even if uvicorn
# is started from a different working directory.
load_dotenv(Path(__file__).parent / ".env")

# -----------------------------------------------------------------------------
# LangSmith — Automatic LLM Tracing
# -----------------------------------------------------------------------------
# LangChain reads these environment variables automatically — no code change
# needed. Every llm.invoke() call is logged to your LangSmith dashboard.
#
#   LANGCHAIN_TRACING_V2=true         → enables tracing
#   LANGCHAIN_API_KEY=<your key>      → authenticates with LangSmith
#   LANGCHAIN_PROJECT=ai-health-advisor → groups traces under this project
#
# View traces at: https://smith.langchain.com
# To disable: set LANGCHAIN_TRACING_V2=false (or remove it from .env)

# -----------------------------------------------------------------------------
# App
# -----------------------------------------------------------------------------

app = FastAPI(
    title="AI Health Advisor",
    description="A FastAPI app that uses LangChain + OpenAI to give personalized health advice.",
    version="1.0.0",
)

# -----------------------------------------------------------------------------
# Middleware — CORS
# -----------------------------------------------------------------------------
# Allows browsers to make cross-origin requests to this API.
# allow_origins=["*"] is fine for local development; restrict in production.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Static Files — Frontend
# -----------------------------------------------------------------------------
# Mounts the frontend/ folder at /static so the browser can load CSS and JS.
# Example: /static/style.css → frontend/style.css

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "frontend"),
    name="static",
)

# -----------------------------------------------------------------------------
# LangChain LLM Client
# -----------------------------------------------------------------------------
# ChatOpenAI reads OPENAI_API_KEY from the environment automatically.
# MODEL_NAME defaults to gpt-4.1-nano if not set in .env.

llm = ChatOpenAI(
    model_name=os.getenv("MODEL_NAME", "gpt-4.1-nano"),  # type: ignore[call-arg]
)


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@app.get("/", include_in_schema=False)
def serve_frontend():
    """
    GET /
    Serves the frontend HTML page.
    include_in_schema=False hides this utility route from the Swagger docs.
    """
    return FileResponse(Path(__file__).parent / "frontend" / "index.html")


@app.post("/chat")
def chat(data: ChatMessage):
    """
    POST /chat

    Accepts a validated ChatMessage body, builds a prompt from the patient's
    profile, sends it to the LLM, and returns the AI-generated health advice.

    Flow:
        1. FastAPI validates the request body against ChatMessage (Pydantic).
        2. Pydantic auto-computes bmi and obesity from height and weight.
        3. build_user_prompt() formats all fields into a readable prompt.
        4. LangChain sends [SystemMessage, HumanMessage] to the OpenAI API.
        5. The LLM response content is returned as JSON.

    Args:
        data: Validated ChatMessage instance — FastAPI injects this automatically.

    Returns:
        dict: {"response": "<LLM health advice text>"}
    """

    # Format patient data into a structured prompt for the LLM.
    user_prompt = build_user_prompt(data)

    # Build the message list:
    #   SystemMessage → sets the AI's role, tone, and guardrails
    #   HumanMessage  → the patient's profile + health concern
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_prompt),
    ]

    # Invoke the LLM with a LangSmith trace config.
    # run_name  → readable label instead of the default "ChatOpenAI"
    # tags      → filterable labels in the LangSmith dashboard
    # metadata  → structured patient context attached to each trace
    #             (never include PII like name — only anonymised signals)
    response = llm.invoke(
        messages,
        config={
            "run_name": "health-advice",
            "tags": [
                os.getenv("MODEL_NAME", "gpt-4.1-nano"),
                "health-advisor",
                data.gender,
                data.obesity or "bmi-unknown",
                data.exercise or "exercise-unknown",
            ],
            "metadata": {
                "age":          data.age,
                "gender":       data.gender,
                "bmi":          data.bmi,
                "bmi_category": data.obesity,
                "exercise":     data.exercise,
                "sleep_hours":  data.sleep_hours,
                "smooking":     data.smooking,
                "city":         data.city,
                "model":        os.getenv("MODEL_NAME", "gpt-4.1-nano"),
            },
        },
    )

    return {"response": response.content.markdown}
