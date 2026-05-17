<!-- refreshed: 2026-05-17 -->
# Architecture

**Analysis Date:** 2026-05-17

## System Overview

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                                  │
│  ┌──────────────────────┐  ┌─────────────────┐  ┌────────────────────────┐  │
│  │  Streamlit Command   │  │  Prediction UI   │  │  Swagger / OpenAPI    │  │
│  │  Center (run_ui)     │  │  (FastAPI +      │  │  (auto from FastAPI)  │  │
│  │  Port:8502           │  │   vanilla JS)    │  │  Port:8000/docs       │  │
│  │  run_streamlit_app.py│  │  Port:8001       │  │                        │  │
│  └──────────┬───────────┘  └────────┬─────────┘  └────────────────────────┘  │
└─────────────┼───────────────────────┼────────────────────────────────────────┘
              │  HTTP REST            │  HTTP REST
              ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      API GATEWAY / HTTP ENTRYPOINT                          │
│  src/model_service/infrastructure/entrypoints/api.py                        │
│  FastAPI app with:                                                          │
│    POST /predict/{use_case}   → real-time inference                         │
│    POST /ingest/{use_case}    → async data ingestion + retrain trigger       │
│    GET  /metrics              → Prometheus endpoint                         │
│    GET  /health               → health check with cached model list         │
│  Global model_cache: dict for champion models per use_case                  │
└──────┬───────────────────────────────┬──────────────────────────────────────┘
       │                               │
       ▼                               ▼
┌─────────────────┐     ┌───────────────────────────────┐
│  APPLICATION    │     │  APPLICATION                   │
│  Service Layer  │     │  Service Layer                 │
│  AnomalyDetect  │     │  MultiTenantOrchestrator       │
│  Service        │     │  - process_streaming_data()    │
│  (IsolationForest│    │  - _trigger_retraining()       │
│   per use_case) │     │  - RF training + MLflow logging │
│  anomaly_service│     │  orchestrator.py                │
│  .py            │     │                                │
└─────────────────┘     └──────────────┬─────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PERSISTENCE / STORAGE                              │
├────────────────────┬────────────────────┬───────────────────────────────────┤
│  PostgreSQL        │  MinIO (S3 API)    │  CSV Filesystem                  │
│  (MLflow metadata) │  (MLflow artifacts)│  data/raw/streaming/{use_case}/   │
│  Port:5432         │  Port:9000/9001    │  data.csv + archived CSV files   │
└────────────────────┴────────────────────┴───────────────────────────────────┘
                                       ▲
                                       │
┌─────────────────────────────────────────────────────────────────────────────┐
│                      MLFLOW TRACKING SERVER                                 │
│  http://localhost:5000                                                      │
│  Tracks experiments, model registry, artifacts                              │
│  Model alias: {use_case}_model@champion                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                      MONITORING STACK                                       │
│  ┌────────────────┐  ┌────────────────┐                                     │
│  │  Prometheus     │  │  Grafana       │                                     │
│  │  Port:9090      │→│  Port:3000     │                                     │
│  │  Scrapes API    │  │  Pre-provisioned│                                    │
│  │  /metrics every │  │  dashboard     │                                     │
│  │  10s            │  │  mlops-overview│                                     │
│  └────────────────┘  └────────────────┘                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 0 — BATCH EXPERIMENTS (PLANNED / PARTIAL)                            │
│  experiments/baselines/ (expected structure):                               │
│  - data_preprocessing.py  - base_model.py  - *_model.py  - steps.py        │
│  - data_drift_simulation.py  - dashboard.py                                │
│  Uses: requirements.txt (pip), SMOTE, KS-test, PowerShell runner           │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| FastAPI Entrypoint | HTTP routing, model cache, metrics, request tracking | `src/model_service/infrastructure/entrypoints/api.py` |
| AnomalyDetectionService | Per-use-case IsolationForest model for anomaly flagging | `src/model_service/application/services/anomaly_service.py` |
| MultiTenantAutoMLOrchestrator | Streaming data ingestion, CSV persistence, threshold-based retraining | `src/model_service/application/services/orchestrator.py` |
| PredictionRequestDTO | Input schema for prediction requests (features dict) | `src/model_service/application/dto/prediction_dto.py` |
| PredictionResponseDTO | Output schema: use_case, prediction, model_version, is_anomaly | `src/model_service/application/dto/prediction_dto.py` |
| IngestionDTO | Input schema for data ingestion (features + optional target) | `src/model_service/application/dto/prediction_dto.py` |
| Streamlit Command Center | Control panel UI for Docker/API/traffic management | `run_streamlit_app.py` |
| Prediction UI | Minimal inference UI (FastAPI + vanilla HTML/JS) | `services/prediction-ui/src/app.py` |
| E2E Demo Script | Sends 35 ingest events per use_case to force retraining | `scripts/e2e_demo_mlflow.py` |
| Streaming Simulator | Drip-feed random events across use_cases | `scripts/simulate_multi_streaming.py` |
| Platform Runner | Orchestrates Docker + API + Streamlit startup | `run_platform.py` |

## Pattern Overview

**Overall:** Hexagonal Architecture (Ports & Adapters) — applied in `src/model_service/`

**Key Characteristics:**
- Strict layer separation: `domain` → `application` → `infrastructure` (inward dependencies only)
- Multi-tenancy via dynamic path parameters (`use_case`) — not separate deployments
- Background task processing for non-blocking ingestion
- CSV-based storage with archival rotation after retraining
- Prometheus metrics exposed at a single `/metrics` endpoint
- No message broker (Kafka/Redpanda) currently wired — future Phase 1 enhancement

## Layers

**Domain Layer:**
- Purpose: Core business logic, entities, exceptions
- Location: `src/model_service/domain/`
- Contains: `entities/` (currently empty), `exceptions/` (currently empty)
- Depends on: Nothing external
- Used by: Application layer
- Status: **STUB — no domain entities or exceptions implemented yet**

**Application Layer:**
- Purpose: Use cases, service orchestration, DTOs
- Location: `src/model_service/application/`
- Contains: `services/orchestrator.py`, `services/anomaly_service.py`, `dto/prediction_dto.py`, `use_cases/` (empty)
- Depends on: Domain layer (target), sklearn, mlflow, pandas, prometheus_client
- Used by: Infrastructure layer

**Infrastructure Layer:**
- Purpose: HTTP entrypoints, adapters, external integrations
- Location: `src/model_service/infrastructure/`
- Contains: `entrypoints/api.py` (FastAPI app)
- Depends on: Application layer
- Used by: External callers (HTTP clients, prediction UI, scripts)

## Data Flow

### Primary Request Path — Prediction

1. HTTP POST to `/predict/{use_case}` (`api.py:88`)
2. Model cache check — loads from MLflow registry on miss, using `models:/{use_case}_model@champion` (`api.py:57-66`)
3. Anomaly detection via IsolationForest (`anomaly_service.py:24-38`)
4. If model loaded: pandas DataFrame transformation → sklearn predict → response (`api.py:116-127`)
5. If no model: returns `prediction=-1, model_version="none"` (`api.py:107-112`)
6. Request metrics recorded (counter, latency histogram) (`api.py:78-82`)

### Primary Request Path — Ingestion

1. HTTP POST to `/ingest/{use_case}` (`api.py:130`)
2. Anomaly check on incoming features (`api.py:137`)
3. Background task enqueued with `BackgroundTasks` (`api.py:145`)
4. Immediate response: `{"status": "Ingested", "use_case": ..., "anomaly_flagged": ...}` (`api.py:147-151`)
5. Background: orchestrator appends row to CSV (`orchestrator.py:44-54`)
6. If total samples >= 30: trigger retraining (`orchestrator.py:58-65`)
7. Retraining: RandomForestClassifier, train/test split, log to MLflow (`orchestrator.py:87-169`)
8. On success: archive CSV file with run_id (`orchestrator.py:156-165`)

### Secondary Flow — E2E Burst

1. `scripts/e2e_demo_mlflow.py` sends 35 ingest events per use_case (`e2e_demo_mlflow.py:29-47`)
2. Each event goes through standard ingestion flow (above)
3. After all events: sleeps 15s for background processing (`e2e_demo_mlflow.py:49`)
4. Queries MLflow for experiment/metrics (`e2e_demo_mlflow.py:52-73`)

**State Management:**
- `model_cache: Dict[str, Any]` at module level in `api.py` — holds loaded MLflow champion models per use_case
- `anomaly_detector.models: Dict[str, IsolationForest]` per use_case
- `orchestrator._locks: Dict[str, Lock]` per use_case for thread-safe CSV writes
- MLflow state: experiments (`{use_case}_experiment`), model registry (`{use_case}_model@champion`)
- CSV files: `data/raw/streaming/{use_case}/data.csv` (active), `data_archived_{run_id}.csv` (historic)

## Key Abstractions

**Multi-Tenancy via `use_case`:**
- Purpose: Partitions data, models, and anomaly detectors per tenant without separate deployments
- Examples: `POST /predict/fraude_financiero`, `POST /ingest/abandono_clientes`
- Pattern: Dynamic URL parameter routing — no separate table or config per tenant

**Background Task Ingestion:**
- Purpose: Decouple ingestion acknowledgment from processing (write to CSV, check threshold, retrain)
- Pattern: FastAPI `BackgroundTasks` — lightweight, no message broker
- File: `api.py:145`

**Champion Model Loading:**
- Purpose: Lazy-load the best model from MLflow registry per use_case, cache in memory
- Pattern: `load_champion_model()` called on-demand, caches with `model_cache` dict
- File: `api.py:57-66`

## Entry Points

| Entry Point | Location | Triggers | Responsibilities |
|-------------|----------|----------|------------------|
| FastAPI HTTP | `api.py:85` | HTTP requests (port 8000) | Routing, metrics, model cache |
| Streamlit UI | `run_streamlit_app.py` | `streamlit run` (port 8502) | Infrastructure control, monitoring |
| Prediction UI | `services/prediction-ui/src/app.py` | uvicorn (port 8001) | Inference form, history display |
| Platform Runner | `run_platform.py` | `python run_platform.py` | Orchestrates Docker + API + UI startup |
| E2E Demo | `scripts/e2e_demo_mlflow.py` | `python scripts/e2e_demo_mlflow.py` | Force retraining, verify MLflow |
| Streaming Sim | `scripts/simulate_multi_streaming.py` | `python simulate_multi_streaming.py` | Generate continuous traffic |

## Architectural Constraints

- **Threading:** Single-threaded async (FastAPI with `BackgroundTasks`). Per-use-case `threading.Lock` in orchestrator for CSV write safety. No asyncio locks — the lock is synchronous inside background tasks.
- **Global state:** `model_cache` dict at module level in `api.py` — mutable, shared across requests. `anomaly_detector.models` dict also module-level. These are not thread-safe for concurrent model loading/writing.
- **Circular imports:** Not detected. Dependency direction is strict: `infrastructure` imports `application` imports `domain`. DTOs are in `application/dto/` but are imported by `infrastructure` for response models.
- **No message broker:** Currently uses FastAPI `BackgroundTasks` for async processing — no Kafka/Redpanda wired despite documentation references.
- **No database for application state:** All state is in CSV files, MLflow (PostgreSQL), and in-memory caches.

## Anti-Patterns

### Empty Domain Layer

**What happens:** `src/model_service/domain/entities/__init__.py` and `src/model_service/domain/exceptions/__init__.py` are empty files. `src/model_service/application/use_cases/__init__.py` is also empty.
**Why it's wrong:** The hexagonal architecture structure exists but the domain layer has no actual entities, value objects, repository ports, or domain exceptions. All business logic lives in application services.
**Do this instead:** Define domain entities (e.g., `Transaction`, `Prediction`) in `domain/entities/`, domain exceptions (e.g., `ModelNotFoundError`, `InsufficientDataError`) in `domain/exceptions/`, and repository port interfaces in `domain/ports/`. Move business rules out of services into domain entities.

### Hardcoded Development Credentials

**What happens:** `MLFLOW_S3_ENDPOINT_URL=http://localhost:9000`, `AWS_ACCESS_KEY_ID=minio_user`, `AWS_SECRET_ACCESS_KEY=minio_password` are hardcoded at module top-level in `api.py:27-29` and `orchestrator.py:26-28`.
**Why it's wrong:** These should come from environment variables with sensible defaults or a `.env` file. Hardcoding credentials is a security risk and prevents cloud deployment.
**Do this instead:** Read from `os.environ.get("MLFLOW_S3_ENDPOINT_URL", "http://localhost:9000")` with a config class or Pydantic `Settings`.

### Module-Level Side Effects

**What happens:** `api.py:27-29` sets `os.environ[...]` at import time. `api.py:52-55` instantiates `model_cache`, `anomaly_detector`, `orchestrator` as module globals.
**Why it's wrong:** Importing the module triggers environment mutations. Module globals make testing harder (state leaks between tests).
**Do this instead:** Use a factory or dependency injection pattern. Move instantiation into the `lifespan` context manager.

### CSV-Based Storage with Race Conditions

**What happens:** The orchestrator reads/writes `data.csv` via pandas. It uses `threading.Lock` per use_case, but pandas `read_csv` loads the entire file into memory. Under concurrent background tasks, there's still a risk of reading stale state.
**Why it's wrong:** CSV is not a database. Read-modify-write patterns with CSV files are inherently racy and don't scale. The lock mitigates but doesn't eliminate race conditions.
**Do this instead:** Use an append-only log (e.g., Kafka), or a real database (PostgreSQL), or Redis for streaming sample counting. Use atomic appends without read-back.

### Mixed Package Managers

**What happens:** Root project uses `uv`/`pyproject.toml` for dependency management, `services/prediction-ui/` has its own `pyproject.toml`, and Phase 0 references `requirements.txt` (not present in repo).
**Why it's wrong:** Creates confusion about which packages are available where. The orchestrator imports `pandas`, `sklearn`, `mlflow` from root's `pyproject.toml`, but `services/prediction-ui/pyproject.toml` lists only `fastapi` and `uvicorn`.
**Do this instead:** Unify under a single monorepo tool (e.g., `uv` workspace or Poetry) with consistent dependency resolution.

## Error Handling

**Strategy:** Minimal — most errors are caught and logged, not raised to caller.

**Patterns:**
- `load_champion_model()` catches all exceptions and returns `None` (`api.py:64-66`)
- `process_streaming_data()` catches all exceptions during retraining, logs, continues (`orchestrator.py:61-65`)
- Retraining catches all exceptions, records failure metric, re-raises (`orchestrator.py:168-169`)
- No structured error responses — prediction endpoint returns `prediction=-1` on model miss rather than a 404/503

## Cross-Cutting Concerns

**Logging:** `print()` statements throughout — no logging framework. Logs go to stdout/terminal.
**Validation:** Pydantic models validate input shape (`features: Dict[str, Any]`) but don't validate feature names or types at the domain level. `extra="allow"` on `PredictionRequestDTO` makes validation permissive.
**Authentication:** None — all endpoints are public. No API keys, tokens, or auth middleware.
**Metrics:** Prometheus counters and histograms for request volume, latency, predictions, retrain triggers, anomalies. Grafana dashboard pre-configured (`grafana/provisioning/dashboards/mlops-overview.json`).

---

*Architecture analysis: 2026-05-17*
