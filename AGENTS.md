# AGENTS.md

## Start Here

1. Read `README.md` for project overview and phases.
2. Read `pyproject.toml` for Python version (>=3.11) and quality rules (ruff, mypy strict).
3. Read `src/model_service/infrastructure/entrypoints/api.py` and `src/model_service/application/services/orchestrator.py` for runtime behavior.
4. If docs conflict with code, trust the code.

## Architecture

- **Hexagonal Architecture** in `src/model_service/` with strict layers: `domain` → `application` → `infrastructure`.
- **Multi-tenant by `use_case`**: routes `/predict/{use_case}` and `/ingest/{use_case}` partition data and models per tenant.
- **HTTP entrypoint**: `src.model_service.infrastructure.entrypoints.api:app` (FastAPI).
- **Retraining logic**: `orchestrator.py` triggers training when 30 samples accumulate per `use_case`; logs model and promotes alias `champion`.
- **MLflow tracking**: `http://localhost:5000`; model registry stores as `{use_case}_model`.
- **Phase 0** (batch experiments): `experiments/baselines/` with Streamlit dashboard.
- **Phase 1** (streaming): services/fraud-engine/ (Poetry) + the `src/model_service/` hexagonal core.

## Developer Commands

```bash
# Infrastructure (Docker Compose)
docker-compose up -d          # Start: Postgres, MinIO, MLflow
docker-compose down           # Stop

# API (run from repo root)
uvicorn src.model_service.infrastructure.entrypoints.api:app --host 0.0.0.0 --port 8000

# E2E runner (auto-starts infra + API; Windows/PowerShell preferred)
python run_platform.py

# Streaming simulation (in another terminal after API is up)
python scripts/simulate_multi_streaming.py    # drip-feed events
python scripts/e2e_demo_mlflow.py             # fast-forward: 35 samples → triggers retraining

# Quality (root of repo)
pytest tests/
ruff check src/
ruff format src/
mypy src/

# Pre-commit hooks
pre-commit run --all-files
```

## Key Conventions

- **Strict typing required**: `mypy` runs in strict mode (`pyproject.toml`). Use typed hints on all new code.
- **Ruff config**: line-length 88, target Python 3.11. Lint set: `E`, `F`, `I`.
- **Run commands from repo root**: orchestrator uses relative paths (`data/raw/streaming/{use_case}/`).
- **MLflow model alias**: always `{use_case}_model@champion` — code hardcodes this.
- **Pre-commit**: conventional commits with types `feat, fix, mlops, infra, data, exp, docs, chore, test, refactor, style, ci, perf`.
- **Phase 0 / Phase 1 separation**: Phase 0 uses `requirements.txt` (pip) and `run_pipeline.ps1`. Phase 1 uses `services/fraud-engine/` with Poetry.

## Pitfalls

- **Hardcoded dev credentials**: API and orchestrator hardcode `MLFLOW_S3_ENDPOINT_URL=http://localhost:9000`, `AWS_ACCESS_KEY_ID=minio_user`, `AWS_SECRET_ACCESS_KEY=minio_password`. Do not assume cloud config.
- **`run_platform.py` is not portable**: it calls PowerShell activation (`.venv\\Scripts\\Activate.ps1`) on Windows. On Linux/macOS, use `uvicorn` directly.
- **Retrain threshold is 30 samples** (demo mode in `orchestrator.py`). Real deployments may need different values.
- **CSV corruption under concurrency**: orchestrator cleans invalid rows before training (`pd.to_numeric` + dropna). This is intentional.
- **Phase 0 pipeline** uses SMOTE for class imbalance and KS-test for data drift — these are in `experiments/baselines/`, not part of the Phase 1 streaming stack.