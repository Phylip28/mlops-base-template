import os
import subprocess
import sys
import time
import webbrowser

import psutil
import streamlit as st

st.set_page_config(
    page_title="Centro de Operaciones MLOps",
    layout="wide",
    page_icon="🚀",
)

# --- UI Header ---
st.title("🚀 MLOps Platform Runner (E2E)")
st.caption("Control Panel Multi-Tenant para Simulación y Observabilidad")
st.markdown("---")

# --- Utils & Background Processes ---
@st.cache_resource
def get_state():
    return {
        "docker_running": False,
        "api_process": None,
        "sim_process": None
    }

state = get_state()

def is_port_in_use(port: int) -> bool:
    try:
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                return True
        return False
    except Exception:
        return False

def open_url(url: str):
    try:
        webbrowser.open(url)
    except Exception:
        pass

# --- 1. Docker Compose ---
st.header("1. Infraestructura Base")
col1, col2, col3 = st.columns([1,1,1])

with col1:
    if st.button(
        "Levantar Contenedores Docker",
        use_container_width=True,
        type="primary",
    ):
        with st.spinner("Iniciando MLflow, MinIO, Grafana..."):
            try:
                subprocess.run("docker-compose up -d", shell=True, check=True)
                state["docker_running"] = True
                st.success("Docker Compose levantado exitosamente.")
            except Exception as e:
                st.error(f"Error al iniciar Docker: {e}")

with col2:
    if st.button("Apagar Docker", use_container_width=True):
        with st.spinner("Apagando contenedores..."):
            subprocess.run("docker-compose down", shell=True)
            state["docker_running"] = False
            st.info("Contenedores detenidos.")

with col3:
    if st.button("Reiniciar Docker", use_container_width=True):
        with st.spinner("Reiniciando..."):
            subprocess.run("docker-compose down && docker-compose up -d", shell=True)
            st.success("Contenedores reiniciados.")

# --- 2. API Backend ---
st.header("2. Backend API (FastAPI)")
c1, c2, _ = st.columns([1,1,2])

api_status_placeholder = st.empty()
if is_port_in_use(8000):
    api_status_placeholder.write("Estado de la API:** 🟢 ONLINE")
else:
    api_status_placeholder.write("Estado de la API:** 🔴 OFFLINE")

with c1:
    if st.button("Iniciar API Backend", use_container_width=True, type="primary"):
        if is_port_in_use(8000):
            st.warning("El puerto 8000 ya está en uso. Detenla primero.")
        else:
            venv_python = os.path.join(".venv", "Scripts", "python.exe")
            if not os.path.exists(venv_python):
                venv_python = sys.executable
            api_entrypoint = (
            "src.model_service.infrastructure.entrypoints.api:app"
        )
            cmd = [
                venv_python,
                "-m",
                "uvicorn",
                api_entrypoint,
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
            ]
            try:
                state["api_process"] = subprocess.Popen(cmd)
                st.success("API iniciada en background.")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Fallo iniciando API: {e}")

with c2:
    if st.button("Detener API Backend", use_container_width=True):
        if state["api_process"]:
            state["api_process"].terminate()
            state["api_process"] = None
        else:
             for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'uvicorn' in proc.info.get('cmdline', []):
                        proc.kill()
                except Exception:
                    pass
        st.info("API Detenida.")
        time.sleep(2)
        st.rerun()

st.markdown("---")

# --- 3. Simulación de Tráfico en Vivo ---
st.header("3. Generadores de Tráfico (Para Grafana)")
sc1, sc2, sc3 = st.columns(3)

with sc1:
    st.info("⚡ Ráfaga Batch (35 Ejemplos)")
    if st.button("Ejecutar e2e_demo_mlflow", use_container_width=True):
        venv_python = os.path.join(".venv", "Scripts", "python.exe")
        if not os.path.exists(venv_python):
            venv_python = sys.executable
        log_file = open("e2e_demo.log", "w", encoding="utf-8")
        subprocess.Popen(
            [venv_python, "scripts/e2e_demo_mlflow.py"],
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )
        st.success("Ráfaga enviada. Revisa e2e_demo.log")

with sc2:
    st.info("💧 Simulación Streaming Fluida")
    if st.button("Iniciar Streaming", use_container_width=True):
        venv_python = os.path.join(".venv", "Scripts", "python.exe")
        if not os.path.exists(venv_python):
            venv_python = sys.executable
        log_file = open("streaming.log", "w", encoding="utf-8")
        state["sim_process"] = subprocess.Popen(
            [venv_python, "scripts/simulate_multi_streaming.py"],
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )
        st.success("Streaming Iniciado. Revisa streaming.log")

with sc3:
    st.info("🛑 Detener Streaming")
    if st.button("Parar Simulación Streaming", use_container_width=True):
        if state["sim_process"]:
             state["sim_process"].terminate()
             state["sim_process"] = None
             st.info("Streaming Detenido.")
        else:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try: # Mato cualquier rastro del script
                    cmdline_str = " ".join(proc.info.get("cmdline") or [])
                    if "simulate_multi_streaming.py" in cmdline_str:
                        proc.kill()
                except Exception:
                    pass
            st.info("Procesos de streaming terminados.")

st.markdown("---")

# --- 4. Enlaces de Observabilidad ---
st.header("4. Observabilidad y Dashboards")
link1, link2, link3, link4 = st.columns(4)

with link1:
    st.button(
        "📊 Abrir Grafana\n(Métricas MLOps en Vivo)",
        on_click=open_url,
        args=("http://localhost:3000",),
        use_container_width=True,
    )
    st.caption("User: `admin` | Pass: `admin`")
with link2:
    st.button(
        "📈 Abrir MLflow\n(Historial de Modelos)",
        on_click=open_url,
        args=("http://localhost:5000",),
        use_container_width=True,
    )
with link3:
    st.button(
        "🗄️ Abrir MinIO\n(Artefactos .pkl)",
        on_click=open_url,
        args=("http://localhost:9001",),
        use_container_width=True,
    )
    st.caption("User: `minio_user` | Pass: `minio_password`")
with link4:
    st.button(
        "🌐 Abrir FastAPI Docs\n(Swagger UI)",
        on_click=open_url,
        args=("http://localhost:8000/docs",),
        use_container_width=True,
    )