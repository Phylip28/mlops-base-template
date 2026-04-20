import os
import random
import time

import mlflow
import requests  # type: ignore[import-untyped]
from mlflow.tracking import MlflowClient

API_URL = "http://localhost:8000"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["AWS_ACCESS_KEY_ID"] = "minio_user"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minio_password"
mlflow.set_tracking_uri("http://localhost:5000")


client = MlflowClient()

USE_CASES = ["fraude_financiero", "abandono_clientes"]


def run() -> None:
    print("Enviando +30 muestras por caso forzar entrenamiento...")
    for uc in USE_CASES:
        print(f"Para el caso {uc}...")
        for i in range(35):
            payload = {
                "features": {
                    "a": random.random(),
                    "b": random.random(),
                    "c": random.random(),
                },
                "target": 1,
            }
            try:
                r = requests.post(f"{API_URL}/ingest/{uc}", json=payload)
                if i % 10 == 0:
                    print(
                        f"  Enviado req {i}, status: {r.status_code}, "
                        f"response: {r.text}"
                    )
            except Exception as e:
                print("Error de conexion API: ", e)
                return
    print("Muestras enviadas, esperando BackgroundTasks de FastAPI (15s)...")
    time.sleep(15)

    print("\n========= METRICAS MLFLOW ============")
    for uc in USE_CASES:
        try:
            exp = client.get_experiment_by_name(f"{uc}_experiment")
            if exp:
                runs = client.search_runs(
                    experiment_ids=[exp.experiment_id], max_results=1
                )
                latest = runs[0] if runs else None
                if latest:
                    accuracy = latest.data.metrics.get("accuracy")
                    print(f"✅ {uc} entrenado. Accuracy = {accuracy}")
                else:
                    print(f"❌ {uc} Sin Runs adentro del experimento")

                versions = client.get_latest_versions(f"{uc}_model", stages=["None"])
                if versions:
                    print(f"   Modelo subido a MinIO: {versions[0].source}")
                    print(f"   Version Alias 'champion': v{versions[0].version}")
            else:
                print(f"❌ {uc} No se creo experimento")
        except Exception as e:
            print(f"Error mlflow: {e}")


if __name__ == "__main__":
    run()
