import subprocess
import time

import psutil
import streamlit as st

from streamlit_app.utils import check_port, get_python, log_event


def render_api() -> None:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("▶  Start API", key="btn_api_start", use_container_width=True):
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
        if st.button("■  Stop API", key="btn_api_stop", use_container_width=True):
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    cmdline = " ".join(proc.info.get("cmdline") or [])
                    if "uvicorn" in cmdline and "8000" in cmdline:
                        proc.kill()
                except Exception:
                    pass
            log_event("API", "FastAPI stopped", "info")
            st.rerun()
