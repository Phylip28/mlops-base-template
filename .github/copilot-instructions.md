# Project Guidelines

## Context First

- Antes de iniciar cualquier tarea, revisa el contexto base en este orden:
- `README.md` para visión general y fases del proyecto.
- `pyproject.toml` para versión de Python y reglas de calidad (`ruff`, `mypy`).
- `src/model_service/infrastructure/entrypoints/api.py` y `src/model_service/application/services/orchestrator.py` para comportamiento real del sistema en runtime.
- Si hay conflicto entre documentación y código, el código actual es la fuente de verdad.

## Architecture

- Mantener Arquitectura Hexagonal: no mezclar responsabilidades entre `domain`, `application` e `infrastructure`.
- El entrypoint HTTP está en `src/model_service/infrastructure/entrypoints/api.py` (FastAPI).
- El sistema es multi-tenant por `use_case` en rutas dinámicas (`/predict/{use_case}`, `/ingest/{use_case}`).
- La lógica de reentrenamiento está en `src/model_service/application/services/orchestrator.py` y se dispara por umbral de muestras.

## Build And Test

- Levantar infraestructura local: `docker-compose up -d`
- Apagar infraestructura local: `docker-compose down`
- Runner E2E completo (solo PowerShell/Windows): `python run_platform.py`
- Levantar API manualmente (Linux/macOS recomendado): `uvicorn src.model_service.infrastructure.entrypoints.api:app --host 0.0.0.0 --port 8000`
- Prueba rápida E2E: `python scripts/e2e_demo_mlflow.py`
- Simulación streaming: `python scripts/simulate_multi_streaming.py`
- Tests: `pytest tests/`
- Lint: `ruff check src/`
- Formato: `ruff format src/`
- Tipado: `mypy src/`

## Conventions

- Usar tipado estático en código nuevo y cambios relevantes (`mypy` en modo estricto en `pyproject.toml`).
- Mantener rutas y contratos multi-tenant basados en `use_case`.
- Si se cambia lógica de entrenamiento/modelo, preservar logging y registro en MLflow.
- Seguir convención de ramas y commits documentada en `docs/git-workflow/git-workflow.md`.

## Environment Pitfalls

- `run_platform.py` ejecuta comandos PowerShell (`.venv\\Scripts\\Activate.ps1`), no portable a bash sin ajustes.
- La API fija `MLFLOW_S3_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY` para entorno local; no asumir configuración cloud.
- El orquestador usa rutas relativas (`data/raw/streaming/{use_case}`): ejecutar comandos desde la raíz del repo.
- El modelo se carga por alias `champion` en MLflow (`models:/{use_case}_model@champion`).

## Documentation Map (Link, Don’t Embed)

- `README.md`: visión general y estructura.
- `docs/README.md`: indice y categorizacion de documentos.
- `docs/setup-verification.md`: checklist de verificacion de servicios.
- `docs/phase-0-pipeline.md`: detalle de pipeline fase 0.
- `docs/phase-1-streaming.md`: notas de fase streaming multi-tenant.
- `docs/quick-commands.md`: comandos rapidos de ejecucion.
- `docs/git-workflow/git-workflow.md`: flujo de ramas, commits y PR.
