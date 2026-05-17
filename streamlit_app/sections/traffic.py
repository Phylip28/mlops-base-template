import subprocess

import psutil
import streamlit as st

from streamlit_app.utils import get_python, log_event


def render_traffic() -> None:
    cols = st.columns(4)

    with cols[0]:
        if st.button("⚡  E2E Burst", key="btn_e2e", use_container_width=True):
            py = get_python()
            log_file = open("e2e_demo.log", "w", encoding="utf-8")
            subprocess.Popen(
                [py, "scripts/e2e_demo_mlflow.py"],
                stdout=log_file,
                stderr=subprocess.STDOUT,
            )
            log_event("GEN", "E2E burst triggered — 35 events", "info")
            st.rerun()

    with cols[1]:
        if st.button(
            "▶  Start Stream", key="btn_stream_start", use_container_width=True
        ):
            py = get_python()
            log_file = open("streaming.log", "w", encoding="utf-8")
            subprocess.Popen(
                [py, "scripts/simulate_multi_streaming.py"],
                stdout=log_file,
                stderr=subprocess.STDOUT,
            )
            log_event("GEN", "Streaming simulation started", "info")
            st.rerun()

    with cols[2]:
        if st.button(
            "■  Stop Streaming", key="btn_stream_stop", use_container_width=True
        ):
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
        if st.button("⟳  Trigger Retrain", key="btn_retrain", use_container_width=True):
            log_event("ML", "Manual retrain triggered", "info")
            py = get_python()
            subprocess.Popen([py, "scripts/e2e_demo_mlflow.py"])
            st.rerun()
