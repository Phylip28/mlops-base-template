import subprocess
import time

import streamlit as st

from streamlit_app.utils import get_docker_compose_cmd, log_event


def render_docker() -> None:
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("▶  Start", key="btn_docker_start", use_container_width=True):
            with st.spinner("Starting containers..."):
                try:
                    cmd = get_docker_compose_cmd() + ["up", "-d"]
                    subprocess.run(cmd, check=True)
                    log_event("DOCKER", "Containers started", "info")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    log_event("DOCKER", f"Start failed: {e}", "error")

    with c2:
        if st.button("■  Stop", key="btn_docker_stop", use_container_width=True):
            with st.spinner("Stopping containers..."):
                try:
                    cmd = get_docker_compose_cmd() + ["down"]
                    subprocess.run(cmd, check=True)
                    log_event("DOCKER", "Containers stopped", "info")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    log_event("DOCKER", f"Stop failed: {e}", "error")

    with c3:
        if st.button("↺  Restart", key="btn_docker_restart", use_container_width=True):
            with st.spinner("Restarting..."):
                try:
                    dc = get_docker_compose_cmd()
                    subprocess.run(dc + ["down"], check=True)
                    subprocess.run(dc + ["up", "-d"], check=True)
                    log_event("DOCKER", "Containers restarted", "info")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    log_event("DOCKER", f"Restart failed: {e}", "error")
