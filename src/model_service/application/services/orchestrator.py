import os
from threading import Lock
from typing import Any, Dict

import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.exceptions import MlflowException
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
        self._locks: Dict[str, Lock] = {}
        self._locks_guard = Lock()

    def _get_use_case_lock(self, use_case: str) -> Lock:
        with self._locks_guard:
            if use_case not in self._locks:
                self._locks[use_case] = Lock()
            return self._locks[use_case]

    def process_streaming_data(self, use_case: str, raw_data: Dict[str, Any]) -> None:
        use_case_lock = self._get_use_case_lock(use_case)
        with use_case_lock:
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
                try:
                    self._trigger_retraining(use_case, df_total, file_path)
                except Exception as exc:
                    print(
                        f"[MLOps] Error reentrenando '{use_case}': {exc}. "
                        "Se conserva el lote para reintento."
                    )

    def _set_or_restore_experiment(
        self, client: mlflow.tracking.MlflowClient, experiment_name: str
    ) -> None:
        experiment = client.get_experiment_by_name(experiment_name)
        if experiment and experiment.lifecycle_stage == "deleted":
            client.restore_experiment(experiment.experiment_id)

        try:
            mlflow.set_experiment(experiment_name)
        except MlflowException as exc:
            if "Cannot set a deleted experiment" not in str(exc):
                raise

            experiment = client.get_experiment_by_name(experiment_name)
            if not experiment:
                raise

            client.restore_experiment(experiment.experiment_id)
            mlflow.set_experiment(experiment_name)

    def _trigger_retraining(
        self, use_case: str, df: pd.DataFrame, file_path: str
    ) -> None:
        client = mlflow.tracking.MlflowClient()
        experiment_name = f"{use_case}_experiment"
        self._set_or_restore_experiment(client, experiment_name)

        if "target" not in df.columns:
            return

        # Si hubo escrituras concurrentes en el pasado, pueden quedar filas corruptas
        # (por ejemplo, headers repetidos dentro del CSV). Convertimos todo a numerico
        # y descartamos filas invalidas antes de entrenar.
        X = df.drop(columns=["target", "is_anomaly"], errors="ignore")
        y = pd.to_numeric(df["target"], errors="coerce")

        X = X.apply(pd.to_numeric, errors="coerce")
        valid_rows = y.notna()
        X = X.loc[valid_rows]
        y = y.loc[valid_rows]

        X = X.dropna(axis=0)
        y = y.loc[X.index]

        if len(X) < 2:
            print(
                f"[MLOps] Se omite entrenamiento de {use_case}: "
                "no hay suficientes filas validas despues de limpiar datos."
            )
            return

        with mlflow.start_run(run_name=f"auto_retrain_{use_case}") as run:
            print("\n[MLOps] ----------------------------------------------------")
            print(
                f"[MLOps] Entrenando modelo REAL para {use_case} "
                f"con {len(X)} eventos validos..."
            )

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
