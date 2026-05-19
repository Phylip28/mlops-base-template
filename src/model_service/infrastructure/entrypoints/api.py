import os
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict

from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from starlette.responses import Response

from src.model_service.application.dto.prediction_dto import (
    IngestionDTO,
    PredictionRequestDTO,
    PredictionResponseDTO,
)
from src.model_service.application.services.anomaly_service import (
    AnomalyDetectionService,
)
from src.model_service.application.services.orchestrator import (
    MultiTenantAutoMLOrchestrator,
)

os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["AWS_ACCESS_KEY_ID"] = "minio_user"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minio_password"

REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API requests",
    ["endpoint", "method", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "api_request_duration_seconds",
    "Request latency in seconds",
    ["endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)
PREDICTIONS_TOTAL = Counter(
    "predictions_total",
    "Total predictions made",
    ["use_case", "model_version"],
)
CACHED_MODELS = Gauge(
    "cached_models_count",
    "Number of models currently cached",
)

model_cache: Dict[str, Any] = {}
anomaly_detector = AnomalyDetectionService()
orchestrator = MultiTenantAutoMLOrchestrator()


def load_champion_model(use_case: str) -> Any | None:
    import mlflow

    mlflow.set_tracking_uri("http://localhost:5000")
    try:
        model_uri = f"models:/{use_case}_model@champion"
        return mlflow.pyfunc.load_model(model_uri)
    except Exception as e:
        print(f"El modelo aun no existe en MLflow ({e})")
        return None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    print("Iniciando API MLOps Multi-tenant conectada a Docker...")
    CACHED_MODELS.set(0)
    yield
    print("Apagando API y liberando memoria...")
    model_cache.clear()


def track_request(endpoint: str, method: str, status_code: int, latency: float) -> None:
    REQUEST_COUNT.labels(
        endpoint=endpoint, method=method, status_code=status_code
    ).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)


app = FastAPI(title="Multi-Tenant MLOps API", lifespan=lifespan)

def _build_cors_origins() -> list[str]:
    raw = os.environ.get("CORS_ORIGINS", "")
    if raw:
        return [o.strip() for o in raw.split(",") if o.strip()]
    default_ports = ["8000", "8001", "8002", "8501", "8502", "8503", "3000"]
    origins: list[str] = []
    for p in default_ports:
        origins.append(f"http://localhost:{p}")
        origins.append(f"http://127.0.0.1:{p}")
    return origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=_build_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict/{use_case}", response_model=PredictionResponseDTO)
async def predict_dynamic(
    use_case: str, payload: PredictionRequestDTO
) -> PredictionResponseDTO:
    import time

    start = time.perf_counter()

    if use_case not in model_cache or model_cache[use_case] is None:
        model_cache[use_case] = load_champion_model(use_case)
        CACHED_MODELS.set(len(model_cache))

    model = model_cache.get(use_case)
    is_anomaly = anomaly_detector.detect_anomaly(use_case, payload.features)
    latency = time.perf_counter() - start

    if not model:
        track_request("/predict/{use_case}", "POST", 200, latency)
        PREDICTIONS_TOTAL.labels(use_case=use_case, model_version="none").inc()
        return PredictionResponseDTO(
            use_case=use_case,
            prediction=-1,
            model_version="none",
            is_anomaly=bool(is_anomaly),
        )

    import pandas as pd

    df_features = pd.DataFrame([payload.features])
    prediction = model.predict(df_features)[0]
    latency = time.perf_counter() - start

    track_request("/predict/{use_case}", "POST", 200, latency)
    PREDICTIONS_TOTAL.labels(use_case=use_case, model_version="champion").inc()
    return PredictionResponseDTO(
        use_case=use_case,
        prediction=int(prediction),
        model_version="champion",
        is_anomaly=bool(is_anomaly),
    )


@app.post("/ingest/{use_case}")
async def ingest_continuo(
    use_case: str, payload: IngestionDTO, background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    import time

    start = time.perf_counter()
    is_anomaly = anomaly_detector.detect_anomaly(use_case, payload.features)
    latency = time.perf_counter() - start

    row_data = payload.features.copy()
    if payload.target is not None:
        row_data["target"] = payload.target
    row_data["is_anomaly"] = is_anomaly

    background_tasks.add_task(orchestrator.process_streaming_data, use_case, row_data)
    track_request("/ingest/{use_case}", "POST", 202, latency)
    return {
        "status": "Ingested",
        "use_case": use_case,
        "anomaly_flagged": bool(is_anomaly),
    }


@app.get("/metrics")
def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/health")
def health_check() -> Dict[str, Any]:
    track_request("/health", "GET", 200, 0.0)
    return {"status": "healthy", "cached_models": list(model_cache.keys())}
