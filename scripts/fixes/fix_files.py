import os

def w(p, t):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(t)

w('src/model_service/application/services/anomaly_service.py', '''import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.exceptions import NotFittedError
from typing import Dict, Any

class AnomalyDetectionService:
    def __init__(self):
        self.models: Dict[str, IsolationForest] = {}

    def _get_or_create_model(self, use_case: str) -> IsolationForest:
        if use_case not in self.models:
            self.models[use_case] = IsolationForest(contamination=0.05, random_state=42)
        return self.models[use_case]

    def detect_anomaly(self, use_case: str, features: Dict[str, float]) -> bool:
        model = self._get_or_create_model(use_case)
        df = pd.DataFrame([features])
        
        try:
            prediction = model.predict(df)
            return prediction[0] == -1
        except NotFittedError:
            model.fit(df)
            return False
''')

w('src/model_service/application/services/orchestrator.py', '''import os
import pandas as pd
import mlflow
from typing import Dict, Any

class MultiTenantAutoMLOrchestrator:
    def __init__(self):
        mlflow.set_tracking_uri("sqlite:///mlflow.db")

    def process_streaming_data(self, use_case: str, raw_data: Dict[str, Any]):
        base_path = f"data/raw/streaming/{use_case}"
        os.makedirs(base_path, exist_ok=True)
        file_path = f"{base_path}/data.csv"
        
        df_new = pd.DataFrame([raw_data])
        df_new.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
        
        df_total = pd.read_csv(file_path)
        if len(df_total) >= 50:
            self._trigger_retraining(use_case, df_total, file_path)

    def _trigger_retraining(self, use_case: str, df: pd.DataFrame, file_path: str):
        mlflow.set_experiment(f"experiment_{use_case}")
        with mlflow.start_run(run_name=f"auto_retrain_{use_case}"):
            print(f"[MLOps] Reentrenando {use_case} con {len(df)} samples...")
            mlflow.log_metric("accuracy_simulada", 0.95)
            
            archive_path = file_path.replace("data.csv", "data_archived.csv")
            if os.path.exists(archive_path):
                os.remove(archive_path)
            os.rename(file_path, archive_path)
            print(f"[MLOps] Lote {use_case} archivado. Listo para el siguiente ciclo.")
''')

w('src/model_service/infrastructure/entrypoints/api.py', '''from fastapi import FastAPI, BackgroundTasks, HTTPException
from contextlib import asynccontextmanager
from typing import Dict, Any

from model_service.application.dto.prediction_dto import PredictionRequestDTO, PredictionResponseDTO, IngestionDTO
from model_service.application.services.anomaly_service import AnomalyDetectionService
from model_service.application.services.orchestrator import MultiTenantAutoMLOrchestrator

model_cache: Dict[str, Any] = {}
anomaly_detector = AnomalyDetectionService()
orchestrator = MultiTenantAutoMLOrchestrator()

def load_champion_model(use_case: str):
    import mlflow
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    try:
        model_uri = f"models:/{use_case}_model@champion"
        return mlflow.pyfunc.load_model(model_uri)
    except Exception:
        return None

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando API MLOps Multi-tenant...")
    yield
    print("Apagando API y liberando memoria...")
    model_cache.clear()

app = FastAPI(title="Multi-Tenant MLOps API", lifespan=lifespan)

@app.post("/predict/{use_case}", response_model=PredictionResponseDTO)
async def predict_dynamic(use_case: str, payload: PredictionRequestDTO):
    if use_case not in model_cache:
        model_cache[use_case] = load_champion_model(use_case)
        
    model = model_cache.get(use_case)
    if not model:
        is_anomaly = anomaly_detector.detect_anomaly(use_case, payload.features)
        return PredictionResponseDTO(
            use_case=use_case,
            prediction=-1,
            model_version="none",
            is_anomaly=bool(is_anomaly)
        )

    is_anomaly = anomaly_detector.detect_anomaly(use_case, payload.features)
    
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
''')
