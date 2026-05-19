# ruff: noqa: E501
import subprocess

import psutil
import streamlit as st

from streamlit_app.components.cards import page_header
from streamlit_app.utils import get_python, log_event


def render() -> None:
    page_header("Traffic", "Generate and manage streaming data for ML training")

    streaming = any(
        "simulate_multi_streaming" in " ".join(p.info.get("cmdline") or [])
        for p in psutil.process_iter(["cmdline"])
    )

    st.markdown(
        """
        <style>
        .traffic-status-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 16px;
            margin-bottom: 24px;
        }
        .traffic-status-card {
            background: var(--bg-surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-card);
            overflow: hidden;
        }
        .traffic-status-card-header {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 12px 16px;
            background: rgba(0, 161, 201, 0.08);
            border-bottom: 1px solid var(--border);
        }
        .traffic-status-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--text-muted);
        }
        .traffic-status-indicator--live {
            background: var(--aws-green);
            box-shadow: 0 0 8px rgba(29, 129, 2, 0.5);
            animation: trafficPulse 2s infinite;
        }
        @keyframes trafficPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .traffic-status-label {
            font-family: 'Cabinet Grotesk', sans-serif;
            font-size: 11px;
            font-weight: 700;
            color: var(--text-primary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .traffic-status-card-body {
            padding: 16px;
        }
        .traffic-status-card-body--actions {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .traffic-status-value {
            font-family: 'Cabinet Grotesk', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 4px;
        }
        .traffic-status-sub {
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            color: var(--text-muted);
        }
        .traffic-ml-section {
            margin-top: 24px;
        }
        .traffic-btn .stButton > button {
            height: 40px !important;
            font-size: 12px !important;
            font-weight: 700 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="traffic-status-grid">', unsafe_allow_html=True)

    stream_cols = st.columns([2, 1])
    with stream_cols[0]:
        status_text = "Streaming" if streaming else "Not Running"
        indicator_class = (
            "traffic-status-indicator--live"
            if streaming
            else "traffic-status-indicator"
        )
        st.markdown(
            f"""
            <div class="traffic-status-card">
                <div class="traffic-status-card-header">
                    <span class="{indicator_class}"></span>
                    <span class="traffic-status-label">Streaming Status</span>
                </div>
                <div class="traffic-status-card-body">
                    <div class="traffic-status-value">{status_text}</div>
                    <div class="traffic-status-sub">0 events/sec • 0 total events</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with stream_cols[1]:
        st.markdown(
            """
            <div class="traffic-status-card">
                <div class="traffic-status-card-header">
                    <span class="traffic-status-label">Quick Actions</span>
                </div>
                <div class="traffic-status-card-body traffic-status-card-body--actions">
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "▶ Start", key="traffic_start", use_container_width=True, type="primary"
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

        if st.button("■ Stop", key="traffic_stop", use_container_width=True):
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    cmdline = " ".join(proc.info.get("cmdline") or [])
                    if "simulate_multi_streaming" in cmdline:
                        proc.kill()
                except Exception:
                    pass
            log_event("GEN", "Streaming stopped", "info")
            st.rerun()

        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="traffic-ml-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">ML Training</div>', unsafe_allow_html=True)
    ml_cols = st.columns(2)
    with ml_cols[0]:
        if st.button(
            "⚡ E2E Burst", key="traffic_e2e", use_container_width=True, type="primary"
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

    with ml_cols[1]:
        if st.button("⟳ Retrain", key="traffic_retrain", use_container_width=True):
            log_event("ML", "Manual retrain triggered", "info")
            py = get_python()
            subprocess.Popen([py, "scripts/e2e_demo_mlflow.py"])
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


render()
