import os
import shutil
import socket
import subprocess
import sys
import time
import webbrowser

import psutil


def _resolve_docker_compose() -> list[str]:
    if shutil.which("docker-compose"):
        return ["docker-compose"]
    if shutil.which("docker"):
        return ["docker", "compose"]
    raise RuntimeError("No se encontro Docker Compose.")


def _get_host_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)
        s.connect(("10.254.254.254", 1))
        ip: str = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def _build_cors_origins() -> str:
    host_ip = _get_host_ip()
    ports = ["8000", "8001", "8002", "8501", "8502", "8503"]
    origins: list[str] = []
    for p in ports:
        origins.append(f"http://localhost:{p}")
        origins.append(f"http://127.0.0.1:{p}")
        if host_ip != "127.0.0.1":
            origins.append(f"http://{host_ip}:{p}")
    return ",".join(origins)


def start_api() -> subprocess.Popen:  # type: ignore[type-arg]
    print("[API] Iniciando Uvicorn (FastAPI) en background...", flush=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    env["CORS_ORIGINS"] = _build_cors_origins()
    venv_python = os.path.join(".venv", "Scripts", "python.exe")
    if not os.path.exists(venv_python):
        venv_python = sys.executable
    cmd = [
        venv_python,
        "-m",
        "uvicorn",
        "src.model_service.infrastructure.entrypoints.api:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
    ]
    return subprocess.Popen(cmd, env=env)


def start_prediction_ui() -> subprocess.Popen:  # type: ignore[type-arg]
    print("[Prediction-UI] Iniciando servicio en background...", flush=True)
    venv_python = os.path.join(
        "services", "prediction-ui", ".venv", "Scripts", "python.exe"
    )
    if not os.path.exists(venv_python):
        venv_python = sys.executable
    cmd = [
        venv_python,
        "-m",
        "uvicorn",
        "src.app:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8001",
    ]
    return subprocess.Popen(cmd)


def main() -> None:
    print("====================================")
    print("=== MLOps Platform Runner (E2E)  ===")
    print("====================================")

    print(
        "\n[1/4] Levantando infraestructura "
        "(MLflow, MinIO, Postgres, Prometheus, Grafana)..."
    )
    try:
        compose_cmd = _resolve_docker_compose()
        subprocess.run(compose_cmd + ["up", "-d"], check=True)
    except Exception as err:
        print(f"Error levantando Docker Compose: {err}")
        sys.exit(1)

    print("\n[2/4] Levantando la API REST Server en puerto 8000...")
    try:
        api_process = start_api()
        time.sleep(5)  # Wait for it to boot
    except Exception as err:
        print(f"Error iniciando API: {err}")
        sys.exit(1)

    print("\n[3/4] Levantando Prediction UI en puerto 8001...")
    try:
        pred_ui_process = start_prediction_ui()
        time.sleep(2)  # Wait for it to boot
    except Exception as err:
        print(f"Error iniciando Prediction UI: {err}")
        sys.exit(1)

    print("\n[4/4] Levantando Interfaz Grafica de Control Visual (Streamlit)...")
    venv_python = os.path.join(".venv", "Scripts", "python.exe")

    if not os.path.exists(venv_python):
        venv_python = sys.executable

    cmd = [
        venv_python,
        "-m",
        "streamlit",
        "run",
        "run_streamlit_app.py",
        "--server.port",
        "8502",
    ]  # noqa: E501

    print("\n Servicios en linea!")
    print("------------------------------------------------")
    print("El Centro de Control se abrira en tu navegador automaticamente.")
    print("  Command Center: http://localhost:8502")
    print("  Prediction UI:  http://localhost:8001")
    print("------------------------------------------------")
    try:
        webbrowser.open("http://localhost:8502")
    except Exception:
        pass

    try:
        print("Presiona CTRL+C en esta terminal para apagar el ecosistema...")
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\nCentro de control detenido.")
        print("Apagando Uvicorn si estaba abierto...")
        if api_process.poll() is None:
            api_process.terminate()
            try:
                api_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                api_process.kill()
        print("Apagando Prediction UI...")
        if pred_ui_process.poll() is None:
            pred_ui_process.terminate()
            try:
                pred_ui_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pred_ui_process.kill()
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                cmdline = proc.info.get("cmdline") or []
                if "uvicorn" in " ".join(cmdline):
                    proc.kill()
            except Exception:
                pass
        print("Ejecutando docker-compose down...")
        try:
            subprocess.run(compose_cmd + ["down"], check=False)
        except Exception:
            pass
        print("Contenedores detenidos.")
        sys.exit(0)


if __name__ == "__main__":
    main()
