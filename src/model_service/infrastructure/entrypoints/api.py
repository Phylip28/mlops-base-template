import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from contextlib import asynccontextmanager
from typing import Dict, Any

from src.model_service.application.dto.prediction_dto import PredictionRequestDTO, PredictionResponseDTO, IngestionDTO
from src.model_service.application.services.anomaly_service import AnomalyDetectionService
from src.model_service.application.services.orchestrator import MultiTenantAutoMLOrchestrator

os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["AWS_ACCESS_KEY_ID"] = "minio_user"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minio_password"

model_cache: Dict[str, Any] = {}
anomaly_detector = AnomalyDetectionService()
orchestrator = MultiTenantAutoMLOrchestrator()

def load_champion_model(use_case: str):
    import mlflow
    mlflow.set_tracking_uri("http://localhost:5000")
    try:
        model_uri = f"models:/{use_case}_model@champion"
        return mlflow.pyfunc.load_model(model_uri)
    except Exception as e:
        print(f"El modelo aun no existe en MLflow ({e})")
        return None

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando API MLOps Multi-tenant conectada a Docker...")
    yield
    print("Apagando API y liberando memoria...")
    model_cache.clear()

app = FastAPI(title="Multi-Tenant MLOps API", lifespan=lifespan)

@app.post("/predict/{use_case}", response_model=PredictionResponseDTO)
async def predict_dynamic(use_case: str, payload: PredictionRequestDTO):
    if use_case not in model_cache or model_cache[use_case] is None:
        model_cache[use_case] = load_champion_model(use_case)
        
    model = model_cache.get(use_case)
    is_anomaly = anomaly_detector.detect_anomaly(use_case, payload.features)

    if not model:
        # Simulando si todavia no hay modelo entrenado en MinIO
        return PredictionResponseDTO(
            use_case=use_case,
            prediction=-1,
            model_version="none",
            is_anomaly=bool(is_anomaly)
        )

    import pandas as pd
    df_features = pd.DataFrame([payload.features])
    prediction = model.predict(df_features)[0]

    return PredictionResponseDTO(
        use_case=use_case,
        prediction=int(prediction),
        model_version="champion",
        is_anomaly=bool(is_anomaly)
    )

@app.post("/ingest/{use_case}")
async def ingest_continuo(use_case: str, payload: IngestionDTO, background_tasks: BackgroundTasks):
    is_anomaly = anomaly_detector.detect_anomaly(use_case, payload.features)
    
    row_data = payload.features.copy()
    if payload.target is not None:
        row_data['target'] = payload.target
    row_data['is_anomaly'] = is_anomaly
    
    background_tasks.add_task(orchestrator.process_streaming_data, use_case, row_data)
    return {"status": "Ingested", "use_case": use_case, "anomaly_flagged": bool(is_anomaly)}

@app.get("/health")
def health_check():
    return {"status": "healthy", "cached_models": list(model_cache.keys())}
