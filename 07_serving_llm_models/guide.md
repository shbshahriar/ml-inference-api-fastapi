# Lesson 07 — Serving an LLM with FastAPI + LangChain

## What You'll Build

A full-stack AI Health Advisor — a FastAPI backend that accepts a patient's profile, sends it to an OpenAI LLM via LangChain, and returns personalized health advice. The same server also hosts the HTML/CSS/JS frontend.

---

## How It Works — End to End

```
Browser (frontend)
      │
      │  POST /chat  {"name": "Alice", "age": 30, ...}
      ▼
FastAPI (llm_health_api.py)
      │
      │  Pydantic validates body → computes bmi & obesity
      │
      ▼
prompts.py → build_user_prompt()
      │
      │  Formats patient profile + concern into a readable prompt
      │
      ▼
LangChain (ChatOpenAI)
      │
      │  [SystemMessage, HumanMessage] → OpenAI API
      │
      ▼
LLM Response
      │
      │  {"response": "Here is your personalized advice..."}
      │
      ▼
Browser (typewriter animation)
```

---

## File Structure

```
07_serving_llm_models/
│
├── llm_health_api.py   ← FastAPI app — routes, middleware, LangChain client
├── schema.py           ← Pydantic model — request body validation + computed fields
├── prompts.py          ← System prompt + user prompt builder
├── utils.py            ← BMI and obesity helper functions
├── .env                ← API key and model name (never commit this)
├── .env.example        ← Template — copy to .env and fill in your key
├── guide.md            ← This file
│
└── frontend/
    ├── index.html      ← Form UI — patient profile + concern input
    ├── style.css       ← Custom styles (focus rings, spinner, typewriter)
    └── script.js       ← Validation, fetch, typewriter animation
```

---

## Setup

### 1. Install dependencies

```bash
uv add langchain langchain-openai python-dotenv aiofiles
```

### 2. Configure your API key

```bash
cp 07_serving_llm_models/.env.example 07_serving_llm_models/.env
```

Open `.env` and set your real OpenAI API key:

```
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4.1-nano
```

### 3. Run the server

```bash
uv run uvicorn 07_serving_llm_models.llm_health_api:app --reload
```

### 4. Open the frontend

Go to **`http://127.0.0.1:8000`** in your browser.

> Do not open `index.html` by double-clicking — the `/static/` asset paths
> only resolve when the page is served through FastAPI.

---

## Key Concepts

### LangChain + OpenAI

LangChain is a framework for building LLM-powered applications. It wraps the
OpenAI API and provides a consistent interface for sending messages.

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOpenAI(model_name="gpt-4.1-nano")

response = llm.invoke([
    SystemMessage(content="You are a health advisor."),
    HumanMessage(content="I feel tired all the time."),
])

print(response.content)
```

| Class | Role |
|-------|------|
| `ChatOpenAI` | LangChain wrapper around the OpenAI Chat API |
| `SystemMessage` | Sets the AI's persona, tone, and guardrails |
| `HumanMessage` | The user's input — the patient profile + concern |

---

### Prompt Engineering

The quality of the LLM's answer depends entirely on the quality of the prompt.
This lesson separates prompts into their own file (`prompts.py`) for clarity.

**System Prompt** — defines who the AI is:
```
You are a professional health advisor AI assistant.
You provide personalized, evidence-based health guidance...
Do not diagnose conditions — only offer lifestyle and wellness advice.
```

**User Prompt** — structured patient data the AI reasons over:
```
Patient Profile:
- Name    : Alice Smith
- Age     : 30
- Gender  : female
- BMI     : 22.86 (Normal weight)
- Exercise: moderate
...

Current concern:
I feel tired all the time and cannot focus at work.
```

---

### Pydantic — Schema Validation + Computed Fields

```python
class ChatMessage(BaseModel):
    name: Annotated[str, Field(..., min_length=5, max_length=50)]
    age:  Annotated[int, Field(..., ge=0, le=120)]
    # ...

    @computed_field
    @property
    def bmi(self) -> Optional[float]:
        return calculate_bmi(self.weight, self.height)
```

- FastAPI validates the request body against `ChatMessage` automatically.
- If validation fails, FastAPI returns a `422 Unprocessable Entity` — no manual error handling needed.
- `@computed_field` auto-generates `bmi` and `obesity` from `height` and `weight` — the client never sends them.

---

### Serving Frontend with FastAPI

```python
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Serve CSS/JS at /static/filename
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Serve the HTML page at the root URL
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")
```

This means one `uvicorn` process serves both the API and the frontend —
no separate dev server needed.

---

### CORS Middleware

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict to specific domains in production
    allow_methods=["*"],
    allow_headers=["*"],
)
```

CORS (Cross-Origin Resource Sharing) allows browsers to make `fetch` calls
to the API. Without it, the browser blocks the request for security reasons.

---

## API Reference

### `POST /chat`

**Request body** (JSON):

| Field | Type | Required | Constraint |
|-------|------|----------|------------|
| `name` | string | Yes | 5–50 chars |
| `age` | integer | Yes | 0–120 |
| `gender` | `"male"` \| `"female"` | Yes | — |
| `text` | string | Yes | 10–1000 chars |
| `city` | string | No | max 100 chars |
| `height` | float | No | 0–300 cm |
| `weight` | float | No | 0–500 kg |
| `exercise` | `"none"` \| `"light"` \| `"moderate"` \| `"heavy"` | No | — |
| `sleep_hours` | float | No | 0–24 |
| `smooking` | `"yes"` \| `"no"` | No | — |

**Response**:

```json
{
  "response": "Based on your profile, here are some personalized recommendations..."
}
```

**Example request**:

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Smith",
    "age": 30,
    "gender": "female",
    "height": 165,
    "weight": 68,
    "exercise": "light",
    "sleep_hours": 6,
    "smooking": "no",
    "text": "I feel exhausted every day and cannot focus at work."
  }'
```

---

## Interactive Docs

With the server running:

| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:8000` | Frontend UI |
| `http://127.0.0.1:8000/docs` | Swagger — interactive API testing |
| `http://127.0.0.1:8000/redoc` | ReDoc — clean documentation view |
