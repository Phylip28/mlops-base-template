import os
import shutil
import subprocess
import sys
from datetime import datetime

import psutil
import streamlit as st

SERVICES = [
    ("postgres", "PostgreSQL", 5432),
    ("mlops_minio", "MinIO", 9000),
    ("mlops_mlflow", "MLflow", 5000),
    ("mlops_prometheus", "Prometheus", 9090),
    ("mlops_grafana", "Grafana", 3000),
]


def log_event(tag: str, msg: str, level: str = "info") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.activity_log.append((ts, tag, msg, level))
    if len(st.session_state.activity_log) > 80:
        st.session_state.activity_log.pop(0)


def get_python() -> str:
    venv = os.path.join(".venv", "Scripts", "python.exe")
    return venv if os.path.exists(venv) else sys.executable


def check_port(port: int) -> bool:
    try:
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                return True
    except Exception:
        pass
    return False


def check_docker_service(name: str) -> bool:
    try:
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", name],
            capture_output=True,
            text=True,
            timeout=3,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except Exception:
        return False


def check_prometheus_scrape() -> tuple[bool, str]:
    try:
        import json
        import urllib.request

        url = "http://localhost:9090/api/v1/targets"
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = resp.read()
        targets = json.loads(data)
        for t in targets.get("data", {}).get("activeTargets", []):
            if "mlops-api" in t.get("labels", {}).get("job", ""):
                return t.get("health") == "up", t.get("lastError", "ok")
        return False, "target not found"
    except Exception as e:
        return False, str(e)


def get_docker_compose_cmd() -> list[str]:
    if shutil.which("docker-compose"):
        return ["docker-compose"]
    if shutil.which("docker"):
        return ["docker", "compose"]
    raise RuntimeError("Docker Compose no encontrado en este sistema")


def refresh_services() -> dict[str, dict[str, bool | int]]:
    out: dict[str, dict[str, bool | int]] = {}
    for container, name, port in SERVICES:
        running = check_docker_service(container)
        out[name] = {"running": running, "port": port}
    out["FastAPI"] = {"running": check_port(8000), "port": 8000}
    return out
