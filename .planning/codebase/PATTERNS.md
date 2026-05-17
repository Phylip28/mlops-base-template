# Design Patterns

**Analysis Date:** 2026-05-17

## 1. Hexagonal Architecture (Ports & Adapters)

**Used in:** `src/model_service/`

The project explicitly adopts Hexagonal Architecture (Alistair Cockburn) to decouple the ML core from infrastructure concerns. The layer structure is:

```
src/model_service/
├── domain/          # Entities, exceptions (currently stubs)
├── application/     # Service orchestration, DTOs
└── infrastructure/  # HTTP entrypoints, external integrations
```

### Layer Rules (as documented and partially enforced)

| Layer | Can import from | Cannot import from |
|-------|----------------|-------------------|
| `domain/` | Nothing external | `application/`, `infrastructure/` |
| `application/` | `domain/` | `infrastructure/` |
| `infrastructure/` | `application/` | Nothing (top layer) |

**Current state:** The structural skeleton exists but the domain layer is empty (`domain/entities/__init__.py` and `domain/exceptions/__init__.py` are zero-line stubs). Business logic lives in `application/services/` instead of domain entities. The `application/use_cases/` directory is also empty.

### Ports (Interfaces)
None defined. In a complete hexagonal implementation, `domain/ports/` would contain repository interfaces (e.g., `ModelRepository`, `SampleStore`) implemented by infrastructure adapters.

### Adapters (Implementations)
- **HTTP Inbound Adapter:** `infrastructure/entrypoints/api.py` — FastAPI routes
- **MLflow Adapter:** Inline in `application/services/orchestrator.py` — model registry operations
- **CSV File Adapter:** Inline in `application/services/orchestrator.py` — streaming data persistence
- **Prometheus Metrics Adapter:** Inline in `api.py` and service files — `prometheus_client` counters/gauges

### Violation
The `application` layer directly calls `mlflow`, `pandas`, `sklearn`, and `prometheus_client`. In a strict hexagonal architecture, these external dependencies should be behind interfaces in infrastructure adapters, and the application layer should only define port interfaces.

## 2. Multi-Tenancy via Dynamic Routing

**Used in:** `api.py`, `orchestrator.py`, `anomaly_service.py`

All state is partitioned by a `use_case` string that flows through every layer:

```
POST /predict/{use_case}          → model_cache[use_case]
POST /ingest/{use_case}           → data/raw/streaming/{use_case}/
orchestrator.process_streaming_data(use_case, ...)  → {use_case}_experiment, {use_case}_model
anomaly_detector.detect_anomaly(use_case, ...)      → models[use_case] (IsolationForest)
```

**How it works:**
- Routes use FastAPI path parameters (`{use_case}`)
- Model cache is a `Dict[str, Any]` keyed by use_case
- Anomaly detectors are `Dict[str, IsolationForest]` keyed by use_case
- Orchestrator uses per-use-case `threading.Lock` for thread safety
- MLflow artifacts use `{use_case}_model` as model name and `{use_case}_experiment` for experiments
- CSV files stored at `data/raw/streaming/{use_case}/data.csv`
- Archives: `data_archived_{run_id}.csv` per use_case

**Discovered tenants in data:**
- `fraude_financiero` — features: monto, distancia_km, hora_transaccion; fraud detection
- `abandono_clientes` — features: dias_inactivo, tickets_soporte, gasto_mensual; churn detection
- `fraud_alert` — data present but no script reference

## 3. Background Task Processing

**Used in:** `api.py` — FastAPI `BackgroundTasks`

Instead of a message broker, the API uses FastAPI's built-in `BackgroundTasks` for asynchronous ingestion:

```python
@app.post("/ingest/{use_case}")
async def ingest_continuo(
    use_case: str, payload: IngestionDTO, background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    # ... anomaly check ...
    background_tasks.add_task(orchestrator.process_streaming_data, use_case, row_data)
    return {"status": "Ingested", ...}  # Immediate response
```

**Trade-off:** Simple but not durable. If the API process crashes, in-flight background tasks are lost. No retry, no acknowledgment, no ordering guarantees.

## 4. Lazy-Loading with Caching (Model Registry Pattern)

**Used in:** `api.py:57-98`

Models are loaded from MLflow registry on first request per use_case and cached in memory:

```python
model_cache: Dict[str, Any] = {}

def load_champion_model(use_case: str) -> Any | None:
    model_uri = f"models:/{use_case}_model@champion"
    return mlflow.pyfunc.load_model(model_uri)

# On predict:
if use_case not in model_cache or model_cache[use_case] is None:
    model_cache[use_case] = load_champion_model(use_case)
```

**Key characteristics:**
- No cache invalidation strategy — once loaded, same model is served until API restart
- No periodic refresh or background model update
- `CACHED_MODELS` Prometheus gauge tracks cache size
- On restart, model_cache is cleared (`lifespan` shutdown)

## 5. Threshold-Based Auto-Retraining

**Used in:** `orchestrator.py:44-65`

```python
def process_streaming_data(self, use_case: str, raw_data: Dict[str, Any]) -> None:
    # ... append to CSV ...
    df_total = pd.read_csv(file_path)
    if len(df_total) >= 30:  # configurable threshold
        self._trigger_retraining(use_case, df_total, file_path)
```

**Pattern:**
- Accumulate samples in CSV until threshold reached
- Trigger retraining synchronously in background task
- On success: archive CSV file (rename to `data_archived_{run_id}.csv`)
- On failure: log error, keep CSV for retry
- Uses `RandomForestClassifier(n_estimators=10, random_state=42)` — fixed model, no hyperparameter tuning

**Current threshold:** 30 samples (demo mode). Documented as configurable but not externalized.

## 6. Prometheus Metrics Exposition

**Used in:** `api.py`, `orchestrator.py`, `anomaly_service.py`

Metrics are defined as module-level `prometheus_client` objects and exposed at `/metrics`:

| Metric | Type | Labels | File |
|--------|------|--------|------|
| `api_requests_total` | Counter | endpoint, method, status_code | `api.py:31-35` |
| `api_request_duration_seconds` | Histogram | endpoint | `api.py:36-41` |
| `predictions_total` | Counter | use_case, model_version | `api.py:42-46` |
| `cached_models_count` | Gauge | (none) | `api.py:47-50` |
| `retrain_triggers_total` | Counter | use_case, status | `orchestrator.py:14-18` |
| `retrain_accuracy` | Gauge | use_case | `orchestrator.py:19-23` |
| `anomalies_detected_total` | Counter | use_case | `anomaly_service.py:8-12` |

Prometheus scrapes `http://172.17.0.1:8000/metrics` every 10s (`prometheus.yml:10-14`).

## 7. Grafana Auto-Provisioning

**Used in:** `grafana/provisioning/`

Grafana is configured with automatic datasource and dashboard provisioning on container startup:

```
grafana/provisioning/
├── datasources/
│   └── prometheus.yml     # Points to Prometheus at http://prometheus:9090
└── dashboards/
    ├── dashboards.yml     # Provider config (file-based, 10s refresh)
    └── mlops-overview.json # Pre-built dashboard for API traffic metrics
```

## 8. Run Platform Pattern (Monolithic Orchestrator)

**Used in:** `run_platform.py`

A single Python script orchestrates the full local development environment:

1. Starts Docker Compose (Postgres, MinIO, MLflow, Prometheus, Grafana)
2. Starts FastAPI via subprocess
3. Starts Streamlit dashboard
4. Opens browser
5. On Ctrl+C: stops API, runs `docker-compose down`

**Pattern:** All-in-one development launcher. Not suitable for production but convenient for local demos.

## 9. Feature-Based Script Segmentation

**Used in:** `scripts/`

Each script has a single responsibility:

| Script | Responsibility |
|--------|----------------|
| `generate_data.py` | Synthetic dataset creation (make_classification) |
| `train_dummy.py` | One-off model training + MLflow registration |
| `simulate_multi_streaming.py` | Continuous ingestion simulation across tenants |
| `e2e_demo_mlflow.py` | Fast-forward: 35 samples → force retrain → verify MLflow |

## 10. Command Center UX Pattern

**Used in:** `run_streamlit_app.py`

A section-based dashboard layout:

1. **Hero Header** — System title, live clock, overall health badge
2. **Metric Tiles** — 5 static stat displays (Services, Containers, Log Events, Retrain Threshold, API Port)
3. **Service Status Grid** — 6 cards (Postgres, MinIO, MLflow, Prometheus, Grafana, FastAPI) with live health checks
4. **Docker Controls** — Start/Stop/Restart buttons
5. **API Controls** — Start/Stop buttons
6. **Traffic Generators** — E2E Burst, Start/Stop Streaming, Trigger Retrain
7. **Activity Log** — Scrolling event log (max 80 entries)
8. **Quick Access** — Links to Grafana, MLflow, MinIO, FastAPI docs, Prometheus, Prediction UI

**Technical choices:**
- Single-file Streamlit app (~955 lines)
- Custom CSS injected via `st.markdown(..., unsafe_allow_html=True)`
- `st.session_state` for activity log
- `psutil` for port checking; `subprocess` for Docker/API control
- No external component libraries

## 11. Metrics-Driven Quality Gates

**Used in:** `.pre-commit-config.yaml`

Pre-commit hooks enforce quality in this order:
1. **Formatting** — `ruff-format`
2. **Linting** — `ruff-check` with auto-fix
3. **Type Checking** — `mypy` in strict mode
4. **Testing** — `pytest` (all tests)
5. **Commit Message** — `conventional-pre-commit` with allowed types: feat, fix, mlops, infra, data, exp, docs, chore, test, refactor, style, ci, perf
6. **File Hygiene** — trailing-whitespace, end-of-file-fixer, check-yaml

---

*Patterns analysis: 2026-05-17*
