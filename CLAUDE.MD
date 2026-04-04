# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

Structured learning repository for building REST APIs with FastAPI — from basic routing to deploying ML models in production. Organized into 11 numbered topic folders, each with Python scripts, markdown guides, and interactive HTML references.

GitHub: `https://github.com/shbshahriar/ml-inference-api-fastapi`

## Environment & Commands

This project uses **uv** exclusively — never use `pip`.

```bash
uv add <package>                                          # add dependency
uv run uvicorn 04_path_query_params.path_query_api:app --reload  # run a lesson
```

- Python: **3.13** (pinned in `.python-version`)
- Core deps: `fastapi>=0.135.3`, `uvicorn>=0.43.0`, `pydantic>=2.12.5`
- uv manages `.venv/` automatically

### Uvicorn module path convention

```bash
uv run uvicorn <folder>.<file>:app --reload
```

## Data

- Shared dataset lives at `Data/patients.json` — a dict keyed by string IDs (`"p001"`, `"p002"`, ...)
- Always use `pathlib.Path(__file__)` to build file paths — never plain relative strings
- `pathlib.Path` conflicts with `fastapi.Path` — alias one: `from pathlib import Path as filePath`

## Folder Structure

| Folder | Topic |
|--------|-------|
| `01_what_is_api/` | What is an API — interactive HTML guides |
| `02_fastapi_setup/` | First app, server commands |
| `03_http_methods/` | GET, POST, PUT, DELETE |
| `04_path_query_params/` | Path and query parameters |
| `05_post_requests/` | POST request body handling |
| `06_put_delete_requests/` | PUT and DELETE |
| `07_serving_ml_models/` | Load model → predict → return JSON; models in `models/` |
| `08_improving_apis/` | Route structure, response formatting |
| `09_docker_for_ml/` | Dockerfile, `docker build`, `docker run` |
| `10_dockerizing_fastapi/` | Containerizing FastAPI |
| `11_deploying_on_aws/` | Cloud deployment |

`main.py` at root is a stub — working files live inside topic folders.

## Constraints

- **Pydantic**: do not explain unless explicitly requested
- **ML projects**: only Iris Classification, House Price Prediction, Insurance Cost Prediction, Customer Churn Prediction
- **Model serialization**: only `pickle` or `joblib`
- **Docker**: only Dockerfile, `docker build`, `docker run` — no orchestration
- **Deployment targets**: Render, Railway, Heroku, AWS, GCP, Azure
- Do not introduce frameworks or topics outside this scope

## Interactive HTML Guides

`01_what_is_api/` and `02_fastapi_setup/` contain single-page HTML guides (Tailwind CSS CDN + Chart.js):

- Typewriter effects for terminal/code output
- Copy-to-clipboard buttons on all code blocks
- Keyboard navigation (← → arrow keys)
- HTML/CSS flow diagrams — no SVG, no Mermaid JS
