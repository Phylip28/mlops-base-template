import os
from typing import Any, Dict

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Variables de entorno para conectar con MinIO y MLflow Server de Docker
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["AWS_ACCESS_KEY_ID"] = "minio_user"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minio_password"


class MultiTenantAutoMLOrchestrator:
    def __init__(self) -> None:
        # Conectar al contenedor MLflow real
        mlflow.set_tracking_uri("http://localhost:5000")

    def process_streaming_data(self, use_case: str, raw_data: Dict[str, Any]) -> None:
        base_path = f"data/raw/streaming/{use_case}"
        os.makedirs(base_path, exist_ok=True)
        file_path = f"{base_path}/data.csv"

        df_new = pd.DataFrame([raw_data])
        df_new.to_csv(
            file_path, mode="a", header=not os.path.exists(file_path), index=False
        )

        df_total = pd.read_csv(file_path)
        # Reducimos umbral a 30 para demostracion rapida
        if len(df_total) >= 30:
            self._trigger_retraining(use_case, df_total, file_path)

    def _trigger_retraining(
        self, use_case: str, df: pd.DataFrame, file_path: str
    ) -> None:
        mlflow.set_experiment(f"{use_case}_experiment")
        client = mlflow.tracking.MlflowClient()

        if "target" not in df.columns:
            return

        with mlflow.start_run(run_name=f"auto_retrain_{use_case}") as run:
            print("\n[MLOps] ----------------------------------------------------")
            print(
                f"[MLOps] Entrenando modelo REAL para {use_case} "
                f"con {len(df)} eventos..."
            )

            # Limpiar datos
            X = df.drop(columns=["target", "is_anomaly"], errors="ignore")
            y = df["target"]

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # Entrenar
            model = RandomForestClassifier(n_estimators=10, random_state=42)
            model.fit(X_train, y_train)

            # Evaluar
            preds = model.predict(X_test)
            acc = accuracy_score(y_test, preds)

            # Loguear Metric y Model a MinIO
            mlflow.log_metric("accuracy", acc)
            model_name = f"{use_case}_model"

            print("[MLOps] Subiendo artefactos a MinIO / S3...")
            mlflow.sklearn.log_model(
                model, "model_artifact", registered_model_name=model_name
            )

            # Obtener ultima version para promoverla
            latest_version = client.get_latest_versions(model_name, stages=["None"])[
                0
            ].version
            client.set_registered_model_alias(model_name, "champion", latest_version)

            print(
                f"[MLOps] Modelo '{model_name}' (v{latest_version}) "
                "guardado en MinIO y MLflow!"
            )
            print(f"[MLOps] Exactitud (Accuracy) obtenida: {acc:.2f}")
            print("[MLOps] ----------------------------------------------------\n")

            # Archivar el lote usado
            archive_path = file_path.replace(
                "data.csv", f"data_archived_{run.info.run_id}.csv"
            )
            try:
                if os.path.exists(archive_path):
                    os.remove(archive_path)
                if os.path.exists(file_path):
                    os.rename(file_path, archive_path)
            except Exception as e:
                print(f"[MLOps] Ignorando error archivar: {e}")
