"""Overview page — real-time telemetry with self-polling Chart.js components.

Each chart is a st.iframe that polls the telemetry
HTTP endpoint every 1s.  Iframes are rendered ONCE (persist forever)
so hover tooltips never disappear.  A fragment updates the shared
snapshot that the endpoint serves.
"""

from __future__ import annotations

from typing import TypedDict

import streamlit as st

from streamlit_app.chart_html import build_chart_html
from streamlit_app.metrics_provider import collect_snapshot
from streamlit_app.telemetry_server import ensure_running, update_snapshot
from streamlit_app.utils import log_event


class _ChartCfg(TypedDict):
    id: str
    title: str
    metric_key: str
    color: str
    y_label: str
    y_min: float
    y_max: float
    height: int


CHARTS: list[_ChartCfg] = [
    {
        "id": "chart_api_uptime",
        "title": "Platform Uptime",
        "metric_key": "api_uptime",
        "color": "#00a1c9",
        "y_label": "UPTIME %",
        "y_min": -5,
        "y_max": 105,
        "height": 240,
    },
    {
        "id": "chart_api_latency",
        "title": "API Latency (p50)",
        "metric_key": "api_latency_ms",
        "color": "#ff9900",
        "y_label": "MS",
        "y_min": -5,
        "y_max": 200,
        "height": 240,
    },
    {
        "id": "chart_api_rps",
        "title": "Requests / Second",
        "metric_key": "api_rps",
        "color": "#44b9d6",
        "y_label": "RPS",
        "y_min": -0.5,
        "y_max": 10,
        "height": 240,
    },
    {
        "id": "chart_api_error",
        "title": "Error Rate",
        "metric_key": "api_error_pct",
        "color": "#d13212",
        "y_label": "ERR %",
        "y_min": -1,
        "y_max": 20,
        "height": 240,
    },
]

SERVICE_CHARTS: list[_ChartCfg] = [
    {
        "id": "chart_svc_pg",
        "title": "PostgreSQL",
        "metric_key": "pg_status",
        "color": "#1d8102",
        "y_label": "STATUS %",
        "y_min": -5,
        "y_max": 105,
        "height": 240,
    },
    {
        "id": "chart_svc_mlflow",
        "title": "MLflow",
        "metric_key": "mlflow_status",
        "color": "#ff9900",
        "y_label": "STATUS %",
        "y_min": -5,
        "y_max": 105,
        "height": 240,
    },
    {
        "id": "chart_svc_minio",
        "title": "MinIO",
        "metric_key": "minio_status",
        "color": "#00a1c9",
        "y_label": "STATUS %",
        "y_min": -5,
        "y_max": 105,
        "height": 240,
    },
    {
        "id": "chart_svc_prometheus",
        "title": "Prometheus",
        "metric_key": "prometheus_status",
        "color": "#8b5cf6",
        "y_label": "STATUS %",
        "y_min": -5,
        "y_max": 105,
        "height": 240,
    },
    {
        "id": "chart_svc_grafana",
        "title": "Grafana",
        "metric_key": "grafana_status",
        "color": "#ff9900",
        "y_label": "STATUS %",
        "y_min": -5,
        "y_max": 105,
        "height": 240,
    },
]


def render() -> None:
    log_event("SYS", "Overview dashboard viewed", "info")

    ensure_running()

    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">Overview</div>
            <div class="page-subtitle">
                Live service health and performance monitoring
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Row 1: 4 main charts in 2x2 grid ──
    col1, col2 = st.columns(2)
    for i, cfg in enumerate(CHARTS):
        target = col1 if i % 2 == 0 else col2
        with target:
            st.iframe(
                build_chart_html(
                    chart_id=cfg["id"],
                    title=cfg["title"],
                    metric_key=cfg["metric_key"],
                    color=cfg["color"],
                    y_label=cfg["y_label"],
                    y_min=cfg["y_min"],
                    y_max=cfg["y_max"],
                    height=cfg["height"],
                ),
                height=cfg["height"],
            )

    st.markdown("<div style='margin:24px 0 12px 0;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-family:Cabinet Grotesk,sans-serif; "
        "font-size:12px; font-weight:600; color:#5f6b7a; "
        "text-transform:uppercase; letter-spacing:1px; "
        "margin-bottom:12px;'>Service Status Timeline</div>",
        unsafe_allow_html=True,
    )

    # ── Row 2: 5 service charts en 2 filas (3 + 2) ──
    st.markdown("<div style='margin:24px 0 16px 0;'></div>", unsafe_allow_html=True)

    row1_cols = st.columns(3)
    for i, cfg in enumerate(SERVICE_CHARTS[:3]):
        with row1_cols[i]:
            st.iframe(
                build_chart_html(
                    chart_id=cfg["id"],
                    title=cfg["title"],
                    metric_key=cfg["metric_key"],
                    color=cfg["color"],
                    y_label=cfg["y_label"],
                    y_min=cfg["y_min"],
                    y_max=cfg["y_max"],
                    height=cfg["height"],
                ),
                height=cfg["height"],
            )

    st.markdown("<div style='margin:24px 0;'></div>", unsafe_allow_html=True)

    row2_cols = st.columns(2)
    for i, cfg in enumerate(SERVICE_CHARTS[3:]):
        with row2_cols[i]:
            st.iframe(
                build_chart_html(
                    chart_id=cfg["id"],
                    title=cfg["title"],
                    metric_key=cfg["metric_key"],
                    color=cfg["color"],
                    y_label=cfg["y_label"],
                    y_min=cfg["y_min"],
                    y_max=cfg["y_max"],
                    height=cfg["height"],
                ),
                height=cfg["height"],
            )

    # Fragment: polls metrics every 1s, updates shared snapshot
    _data_fragment()


@st.fragment(run_every=1)
def _data_fragment() -> None:
    snapshot = collect_snapshot()
    update_snapshot(snapshot)
