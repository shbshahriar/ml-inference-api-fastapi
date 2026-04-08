import sys
from pathlib import Path

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

load_dotenv(Path(__file__).parent / ".env")

app = FastAPI(title="LLM Health Advisor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "frontend"),
    name="static",
)

llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "gpt-4.1-nano"),
)


@app.get("/")
def serve_frontend():
    return FileResponse(Path(__file__).parent / "frontend" / "index.html")


@app.post("/chat")
def chat(data: ChatMessage):
    user_prompt = build_user_prompt(data)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)

    return {"response": response.content}
