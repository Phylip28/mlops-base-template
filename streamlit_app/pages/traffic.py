# ruff: noqa: E501
import subprocess

import psutil
import streamlit as st

from streamlit_app.components.cards import page_header
from streamlit_app.utils import get_python, log_event


def render() -> None:
    page_header("Traffic", "Generate and manage streaming data for ML training")

    st.markdown(
        """
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px;">
        <div class="metric-tile purple"><div class="metric-value">⚡</div>
            <div class="metric-label">E2E Burst</div></div>
        <div class="metric-tile accent"><div class="metric-value">▶</div>
            <div class="metric-label">Stream</div></div>
        <div class="metric-tile red"><div class="metric-value">■</div>
            <div class="metric-label">Stop</div></div>
        <div class="metric-tile amber"><div class="metric-value">⟳</div>
            <div class="metric-label">Retrain</div></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    with cols[0]:
        if st.button(
            "⚡  E2E Burst", key="traffic_e2e", use_container_width=True, type="primary"
        ):
            py = get_python()
            with open("e2e_demo.log", "w", encoding="utf-8") as log_file:
                subprocess.Popen(
                    [py, "scripts/e2e_demo_mlflow.py"],
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                )
            log_event("GEN", "E2E burst triggered — 35 events", "info")
            st.rerun()

    with cols[1]:
        if st.button(
            "▶  Start Stream",
            key="traffic_start",
            use_container_width=True,
            type="primary",
        ):
            py = get_python()
            with open("streaming.log", "w", encoding="utf-8") as log_file:
                subprocess.Popen(
                    [py, "scripts/simulate_multi_streaming.py"],
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                )
            log_event("GEN", "Streaming simulation started", "info")
            st.rerun()

    with cols[2]:
        if st.button("■  Stop Stream", key="traffic_stop", use_container_width=True):
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    cmdline = " ".join(proc.info.get("cmdline") or [])
                    if "simulate_multi_streaming" in cmdline:
                        proc.kill()
                except Exception:
                    pass
            log_event("GEN", "Streaming stopped", "info")
            st.rerun()

    with cols[3]:
        if st.button("⟳  Retrain", key="traffic_retrain", use_container_width=True):
            log_event("ML", "Manual retrain triggered", "info")
            py = get_python()
            subprocess.Popen([py, "scripts/e2e_demo_mlflow.py"])
            st.rerun()


render()
