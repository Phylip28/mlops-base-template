# Technology Stack

**Analysis Date:** 2026-05-17

## Languages

**Primary:**
- Python >=3.11 — All backend services, ML code, scripts, and CLI tools.
  - .python-version: `3.11`
  - pyproject.toml: `requires-python = ">=3.11"`

**Secondary:**
- JavaScript (vanilla) — Inline in Prediction UI (`services/prediction-ui/src/app.py`), no bundler/framework.
- YAML — Docker Compose, Pre-commit config, Grafana provisioning, Prometheus config.
- CSS — Custom styles injected via Streamlit and FastAPI HTML responses.
- HTML — Inline HTML templates in Prediction UI.

## Runtime

**Environment:**
- Python 3.11+ interpreter (CPython)
- Docker engine with Compose plugin (for infrastructure containers)

**Package Manager:**
- **uv** (primary) — Lockfile: `uv.lock` at repo root. Used for the root project and all commands.
- **Poetry** (referenced in docs for `services/fraud-engine/`) — Not yet used; Phase 1 future.
- **pip** (Phase 0) — Referenced `requirements.txt` for batch experiments (file not found, may need creation).

## Frameworks

**Core API:**
- **FastAPI** >=0.110.0 — HTTP entrypoint for multi-tenant MLOps API.
  - Routes: `/predict/{use_case}`, `/ingest/{use_case}`, `/metrics`, `/health`
  - ASGI server: **uvicorn** >=0.29.0
  - Schema validation: **Pydantic** >=2.6.0

**Control Dashboard:**
- **Streamlit** >=1.30.0 — Command Center UI (`run_streamlit_app.py`)
  - Run via: `uv run streamlit run run_streamlit_app.py --server.port 8502`

**ML Platform:**
- **MLflow** >=3.10.1 — Experiment tracking and model registry.
  - Docker image: `ghcr.io/mlflow/mlflow:v3.10.1`
  - Backend store: PostgreSQL (mlflow_db)
  - Artifact store: MinIO (S3-compatible, bucket `mlflow-artifacts`)
  - Tracking URI: `http://localhost:5000`

**Testing:**
- **pytest** >=8.1.1 — Single smoke test. Coverage: `pytest-cov` >=4.1.0.

**Linting/Formatting:**
- **ruff** >=0.3.4 — Linter + formatter. Config: line-length 88, target `py311`, rulesets E, F, I.
- **mypy** >=1.9.0 — Strict mode. Config: `strict = true`, `ignore_missing_imports = true`.

## Key Dependencies

**Critical (root pyproject.toml):**

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | >=0.110.0 | REST API framework for inference/ingestion |
| `uvicorn` | >=0.29.0 | ASGI server to run FastAPI |
| `pydantic` | >=2.6.0 | Request/response schema validation |
| `mlflow` | >=3.10.1 | Experiment tracking, model registry, artifact storage |
| `scikit-learn` | >=1.8.0 | ML models: RandomForestClassifier, IsolationForest, metrics |
| `boto3` | >=1.42.83 | S3 SDK required by MLflow for MinIO connectivity |
| `prometheus-client` | >=0.20.0 | Metrics exposition for Prometheus scraping |
| `psutil` | >=5.9.0 | System process monitoring (Streamlit dashboard) |
| `streamlit` | >=1.30.0 | Control dashboard framework |
| `pre-commit` | >=4.5.1 | Git hooks for quality gates |

**Infrastructure (Docker containers):**

| Image | Version | Purpose |
|-------|---------|---------|
| `postgres:15-alpine` | 15 | MLflow backend database |
| `minio/minio:latest` | latest | S3-compatible artifact storage |
| `ghcr.io/mlflow/mlflow` | v3.10.1 | MLflow tracking server |
| `prom/prometheus:latest` | latest | Metrics collection and alerting |
| `grafana/grafana:latest` | latest | Metrics visualization dashboards |

**Services Dependencies:**

| Service | Packages | Notes |
|---------|----------|-------|
| `services/prediction-ui/` | fastapi, uvicorn | Minimal — inline HTML/JS via string templates |
| `scripts/` | requests (runtime), mlflow, pandas | Script dependencies not in pyproject dev deps |

## Configuration

**Environment:**
- No `.env` file or dotenv usage. Key env vars hardcoded in source:
  - `MLFLOW_S3_ENDPOINT_URL=http://localhost:9000` (api.py, orchestrator.py)
  - `AWS_ACCESS_KEY_ID=minio_user` (api.py, orchestrator.py)
  - `AWS_SECRET_ACCESS_KEY=minio_password` (api.py, orchestrator.py)
- Prediction UI reads `API_BASE_URL` from environment (default `http://localhost:8000`) (`services/prediction-ui/src/app.py:11`)

**Build:**
- Root build system: `hatchling` (`[build-system]` in pyproject.toml)
- Wheel packages: `src/model_service`
- Dockerfiles: `services/prediction-ui/Dockerfile` (uses `uv sync`)

**Quality Config:**
- `pyproject.toml` — ruff and mypy settings
- `.pre-commit-config.yaml` — Pre-commit hooks: trailing-whitespace, end-of-file-fixer, check-yaml, conventional-commit, ruff (check+format), mypy, pytest
- `ruff` ruleset: E (pycodestyle errors), F (pyflakes), I (import sorting)
- `mypy` strict mode with `ignore_missing_imports = true`, `disallow_untyped_decorators = false`

## Platform Requirements

**Development:**
- Python 3.11+
- Docker Engine + Docker Compose
- `uv` package manager (`pip install uv`)
- No OS restrictions, but `run_platform.py` PowerShell-heavy (Windows bias)

**Production:**
- Not currently defined — no production Dockerfile for the API, no Kubernetes manifests, no cloud configuration.
- The hardcoded `localhost` URLs and dev credentials must be replaced for production.
- MLflow, Postgres, MinIO would need proper networking, auth, and persistence in production.

## What NOT to Use

- **No TypeScript/Node.js** — Frontends are Python-based (Streamlit) or vanilla HTML/JS.
- **No database ORM** — No SQLAlchemy, no Alembic. Application stores data in CSVs. MLflow uses PostgreSQL internally.
- **No message broker** — Kafka, Redpanda, RabbitMQ referenced in documentation but not wired. Uses `BackgroundTasks` instead.
- **No Redis/cache layer** — In-memory Python dict for model cache. No external caching.
- **No Kubernetes/container orchestration** — Docker Compose only.
- **No CI/CD pipeline** — No GitHub Actions, GitLab CI, or Jenkins config found (`.github/` contains only `copilot-instructions.md`).
- **No authentication middleware** — All endpoints are public.

---

*Stack analysis: 2026-05-17*
