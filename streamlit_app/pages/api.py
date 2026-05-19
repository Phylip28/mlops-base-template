# ruff: noqa: E501
import subprocess
import time

import psutil
import streamlit as st

from streamlit_app.components.cards import page_header
from streamlit_app.utils import check_port, get_python, log_event, refresh_services


def render() -> None:
    page_header("API", "Start and stop the FastAPI prediction server")

    svcs = refresh_services()
    api_up = svcs.get("FastAPI", {}).get("running", False)

    st.markdown(
        f"""
    <div class="card card-striped {"green" if api_up else "red"}">
        <div style="display:flex;align-items:center;justify-content:space-between;">
            <div>
                <div style="font-family:'Cabinet Grotesk',sans-serif;font-size:16px;
                    font-weight:600;color:var(--text-primary);">FastAPI Server</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:11px;
                    color:var(--text-muted);margin-top:4px;">:8000</div>
            </div>
            <span class="{"svc-status-up" if api_up else "svc-status-down"}">
                {"Activo" if api_up else "Inactivo"}
            </span>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "▶  Start API", key="api_start", use_container_width=True, type="primary"
        ):
            if check_port(8000):
                st.warning("Port 8000 already in use")
                log_event("API", "Start blocked — port in use", "info")
            else:
                py = get_python()
                cmd = [
                    py,
                    "-m",
                    "uvicorn",
                    "src.model_service.infrastructure.entrypoints.api:app",
                    "--host",
                    "0.0.0.0",
                    "--port",
                    "8000",
                ]
                subprocess.Popen(cmd)
                log_event("API", "FastAPI started on port 8000", "info")
                time.sleep(1)
                st.rerun()

    with c2:
        if api_up:
            if st.button(
                "■  Stop API",
                key="api_stop",
                use_container_width=True,
                type="secondary",
            ):
                for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                    try:
                        cmdline = " ".join(proc.info.get("cmdline") or [])
                        if "uvicorn" in cmdline and "8000" in cmdline:
                            proc.kill()
                    except Exception:
                        pass
                log_event("API", "FastAPI stopped", "info")
                st.rerun()


render()
