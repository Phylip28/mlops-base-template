# ruff: noqa: E501
import subprocess
import time

import streamlit as st

from streamlit_app.components.cards import page_header
from streamlit_app.utils import check_docker_service, get_docker_compose_cmd, log_event


def render() -> None:
    page_header("Docker", "Manage your container infrastructure")

    status_cols = st.columns(5)
    services_status = [
        ("postgres", "PostgreSQL", 5432),
        ("mlops_minio", "MinIO", 9000),
        ("mlops_mlflow", "MLflow", 5000),
        ("mlops_prometheus", "Prometheus", 9090),
        ("mlops_grafana", "Grafana", 3000),
    ]
    for idx, (container, name, port) in enumerate(services_status):
        running = check_docker_service(container)
        with status_cols[idx]:
            st.markdown(
                f"""
            <div class="svc-card" style="text-align:center;">
                <div class="svc-name" style="font-size:12px;">{name}</div>
                <div style="margin:8px 0;">
                    <span class="svc-indicator {"up" if running else "down"}"
                    style="display:inline-block;"></span>
                </div>
                <span class="badge {"badge-up" if running else "badge-down"}">
                    {"ONLINE" if running else "OFFLINE"}
                </span>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.markdown(
        "<hr style='border-color:var(--border);margin:24px 0;'>", unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(
            "▶  Start All", key="docker_start", use_container_width=True, type="primary"
        ):
            with st.spinner("Starting containers..."):
                try:
                    cmd = get_docker_compose_cmd() + ["up", "-d"]
                    subprocess.run(cmd, check=True)
                    log_event("DOCKER", "Containers started", "info")
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    log_event("DOCKER", f"Start failed: {e}", "error")

    with c2:
        if st.button("■  Stop All", key="docker_stop", use_container_width=True):
            with st.spinner("Stopping containers..."):
                try:
                    cmd = get_docker_compose_cmd() + ["down"]
                    subprocess.run(cmd, check=True)
                    log_event("DOCKER", "Containers stopped", "info")
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    log_event("DOCKER", f"Stop failed: {e}", "error")

    with c3:
        if st.button("↺  Restart All", key="docker_restart", use_container_width=True):
            with st.spinner("Restarting..."):
                try:
                    dc = get_docker_compose_cmd()
                    subprocess.run(dc + ["down"], check=True)
                    subprocess.run(dc + ["up", "-d"], check=True)
                    log_event("DOCKER", "Containers restarted", "info")
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    log_event("DOCKER", f"Restart failed: {e}", "error")


render()
