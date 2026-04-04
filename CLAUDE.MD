# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Structured learning repository following the CampusX FastAPI for Machine Learning curriculum. Content is organized into 11 numbered topic folders, each containing Python scripts, interactive HTML guides, and markdown notes.

## Environment & Commands

This project uses **uv** exclusively — never use `pip`.

```bash
# Add dependencies
uv add fastapi
uv add uvicorn

# Run dev server (from project root)
uv run uvicorn 02_fastapi_setup.first_app:app --reload

# Run production server
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

- Python: **3.13** (pinned in `.python-version`)
- Core deps: `fastapi>=0.135.3`, `uvicorn>=0.43.0`, `pydantic>=2.12.5`
- uv manages `.venv/` automatically

### Uvicorn module path convention

When the app file is inside a subfolder, use dot-notation:

```bash
uv run uvicorn 02_fastapi_setup.first_app:app --reload
#               [folder].[file]:[FastAPI object]
```

## Folder Structure

| Folder | Topic |
|--------|-------|
| `01_what_is_api/` | What is an API — interactive HTML guides |
| `02_fastapi_setup/` | Install, first app (`first_app.py`), server commands |
| `03_http_methods/` | GET, POST, PUT, DELETE |
| `04_path_query_params/` | Path and query parameters |
| `05_post_requests/` | POST request body handling |
| `06_put_delete_requests/` | PUT and DELETE |
| `07_serving_ml_models/` | Load model → predict → return JSON; saved models go in `models/` |
| `08_improving_apis/` | Route structure, response formatting |
| `09_docker_for_ml/` | Dockerfile, `docker build`, `docker run` |
| `10_dockerizing_fastapi/` | Containerizing FastAPI |
| `11_deploying_on_aws/` | AWS deployment |

`main.py` at the root is a stub. Working app files live inside topic folders.

## Curriculum Constraints

- **Pydantic**: do not explain unless explicitly requested.
- **ML projects**: only Iris Classification, House Price Prediction, Insurance Cost Prediction, Customer Churn Prediction.
- **Model serialization**: only `pickle` or `joblib`.
- **Docker**: only Dockerfile creation, `docker build`, `docker run` — no orchestration.
- **Deployment targets**: Render, Railway, Heroku, AWS, GCP, Azure.
- Do not introduce frameworks or topics outside this curriculum.

## Interactive HTML Guides

`01_what_is_api/` and `02_fastapi_setup/` contain self-contained single-page HTML learning guides (Tailwind CSS CDN + Chart.js). When creating or modifying them:

- Typewriter effects for terminal/code output
- Copy-to-clipboard buttons on all code blocks
- Keyboard navigation (← → arrow keys) between steps/sections
- Prefer HTML/CSS flow diagrams over canvas-based charts
- No SVG graphics, no Mermaid JS