import os
import subprocess
import time
import webbrowser
import threading
import sys

def start_api():
    print("[API] Iniciando Uvicorn en background...", flush=True)
    # Ejecutamos con el entorno virtual para asegurarnos de que encuentre todo
    cmd = 'powershell -Command "& .\\.venv\\Scripts\\Activate.ps1 ; $env:PYTHONPATH=\'.\' ; uvicorn src.model_service.infrastructure.entrypoints.api:app --host 0.0.0.0 --port 8000"'
    # Subproceso bloqueante para el hilo
    subprocess.run(cmd, shell=True)

def main():
    print("====================================")
    print("=== MLOps Platform Runner (E2E)  ===")
    print("====================================")

    # 1. Iniciar Docker Compose
    print("\n[1/3] Levantando infraestructura (MLflow, MinIO, Postgres)...")
    subprocess.run("docker-compose up -d", shell=True)

    # 2. Iniciar API Backend
    print("\n[2/3] Levantando la API REST Server en puerto 8000...")
    api_thread = threading.Thread(target=start_api, daemon=True)
    api_thread.start()

    # Esperar prudencial
    print("Esperando 10s a que los servicios esten listos...")
    time.sleep(10)
    
    # 3. Mostrar URLs y abrir
    print("\n[3/3] ¡Servicios en línea!")
    print("------------------------------------------------")
    print("🌐 FastAPI Docs (Swagger): http://localhost:8000/docs")
    print("📊 MLflow UI (Métricas):   http://localhost:5000")
    print("🗄️  MinIO (Artefactos):    http://localhost:9001 (user: minio_user / pass: minio_password)")
    print("------------------------------------------------")

    print("\n[INFO] Abriendo las interfaces en tu navegador por defecto...\n")
    try:
        webbrowser.open("http://localhost:8000/docs")
        webbrowser.open("http://localhost:5000")
        webbrowser.open("http://localhost:9001")
    except Exception as e:
        print(f"Nota: No se pudo abrir el navegador automáticamente: {e}")

    print("🚀 PARA GENERAR MUESTRAS EN VIVO Y VERIFICAR MLFLOW:")
    print("Abre *OTRA* terminal e ingresa uno de los siguientes comandos:")
    print("  python scripts/e2e_demo_mlflow.py           -> Corre 35 ejemplos de golpe y fuerza entrenamiento")
    print("  python scripts/simulate_multi_streaming.py    -> Ingesta data gota a gota como eventos web")

    print("\nPresiona CTRL+C en cualquier momento para detener el servidor API y Salir...\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nDeteniendo ejecución del script de consola...")
        print("¿Deseas apagar también los contenedores Docker? (s/n)")
        try:
            ans = input().strip().lower()
            if ans == 's':
                print("Ejecutando docker-compose down...")
                subprocess.run("docker-compose down", shell=True)
                print("Contenedores detenidos.")
        except:
            pass
        print("¡Hasta luego!")
        sys.exit(0)

if __name__ == "__main__":
    main()
