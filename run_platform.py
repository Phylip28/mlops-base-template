import os
import shutil
import subprocess
import sys
import time
import webbrowser


def _resolve_docker_compose() -> list[str]:
    """Resuelve el comando disponible entre docker compose y docker-compose."""
    if shutil.which("docker-compose"):
        return ["docker-compose"]

    if shutil.which("docker"):
        result = subprocess.run(
            ["docker", "compose", "version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode == 0:
            return ["docker", "compose"]

    raise RuntimeError(
        "No se encontro Docker Compose. Instala 'docker compose' o 'docker-compose'."
    )


def start_api() -> subprocess.Popen[bytes]:
    print("[API] Iniciando Uvicorn en background...", flush=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = "."

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "src.model_service.infrastructure.entrypoints.api:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
    ]
    return subprocess.Popen(cmd, env=env)


def _stop_api_process(api_process: subprocess.Popen[bytes]) -> None:
    if api_process.poll() is not None:
        return

    api_process.terminate()
    try:
        api_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        api_process.kill()


def main() -> None:
    print("====================================")
    print("=== MLOps Platform Runner (E2E)  ===")
    print("====================================")

    # 1. Iniciar Docker Compose
    print("\n[1/3] Levantando infraestructura (MLflow, MinIO, Postgres)...")
    try:
        compose_cmd = _resolve_docker_compose()
        subprocess.run(compose_cmd + ["up", "-d"], check=True)
    except (RuntimeError, subprocess.CalledProcessError) as err:
        print(f"Error levantando Docker Compose: {err}")
        sys.exit(1)

    # 2. Iniciar API Backend
    print("\n[2/3] Levantando la API REST Server en puerto 8000...")
    try:
        api_process = start_api()
    except Exception as err:
        print(f"Error iniciando API: {err}")
        sys.exit(1)

    # Esperar prudencial
    print("Esperando 10s a que los servicios esten listos...")
    time.sleep(10)

    # 3. Mostrar URLs y abrir
    print("\n[3/3] ¡Servicios en línea!")
    print("------------------------------------------------")
    print("🌐 FastAPI Docs (Swagger): http://localhost:8000/docs")
    print("📊 MLflow UI (Métricas):   http://localhost:5000")
    print(
        "🗄️  MinIO (Artefactos):    http://localhost:9001 "
        "(user: minio_user / pass: minio_password)"
    )
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
    print(
        "  python scripts/e2e_demo_mlflow.py "
        "-> Corre 35 ejemplos de golpe y fuerza entrenamiento"
    )
    print(
        "  python scripts/simulate_multi_streaming.py "
        "-> Ingesta data gota a gota como eventos web"
    )

    print(
        "\nPresiona CTRL+C en cualquier momento para detener "
        "el servidor API y Salir...\n"
    )
    try:
        while True:
            if api_process.poll() is not None:
                print("\nLa API se detuvo inesperadamente. Revisa logs del proceso.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nDeteniendo ejecución del script de consola...")
        _stop_api_process(api_process)
        print("¿Deseas apagar también los contenedores Docker? (s/n)")
        try:
            ans = input().strip().lower()
            if ans in {"s", "y", "yes"}:
                print("Ejecutando docker-compose down...")
                subprocess.run(compose_cmd + ["down"], check=False)
                print("Contenedores detenidos.")
        except Exception:
            pass
        print("¡Hasta luego!")
        sys.exit(0)

    _stop_api_process(api_process)


if __name__ == "__main__":
    main()
