"""Overview page — real-time F1 telemetry dashboard with rolling window."""

from __future__ import annotations

import random
from collections import deque
from datetime import datetime, timedelta
from typing import Any

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from streamlit_app.utils import log_event

WINDOW_SECONDS = 120
MAX_POINTS = WINDOW_SECONDS

_SERIES_DEFAULTS: dict[str, dict[str, float]] = {
    "uptime": {"base": 95, "variance": 8, "noise": 2, "spike": 0.03},
    "latency": {"base": 45, "variance": 20, "noise": 5, "spike": 0.05},
    "rps": {"base": 120, "variance": 30, "noise": 10, "spike": 0.04},
    "errors": {"base": 2, "variance": 3, "noise": 1, "spike": 0.08},
    "pg": {"base": 95, "variance": 5, "noise": 2, "spike": 0.02},
    "fastapi": {"base": 98, "variance": 3, "noise": 1, "spike": 0.02},
    "mlflow": {"base": 88, "variance": 12, "noise": 3, "spike": 0.04},
}


def _init_series(key: str) -> None:
    """Pre-fill series with historical data so chart starts full."""
    if key in st.session_state:
        return
    cfg = _SERIES_DEFAULTS[key]
    now = datetime.now()
    ts: deque[datetime] = deque(maxlen=MAX_POINTS)
    vals: deque[float] = deque(maxlen=MAX_POINTS)
    current = cfg["base"]
    for i in range(MAX_POINTS - 1, -1, -1):
        t = now - timedelta(seconds=i)
        drift = (cfg["base"] - current) * 0.1
        current += np.random.normal(drift, cfg["variance"] * 0.15)
        if random.random() < cfg["spike"]:
            current += random.choice([-1, 1]) * 40 * random.random()
        current += np.random.normal(0, cfg["noise"])
        current = max(0, min(100, current))
        ts.append(t)
        vals.append(current)
    st.session_state[key] = {
        "timestamps": ts,
        "values": vals,
        "current": current,
    }


def _tick(key: str) -> None:
    """Append one data point via random walk + mean reversion."""
    s = st.session_state[key]
    cfg = _SERIES_DEFAULTS[key]
    drift = (cfg["base"] - s["current"]) * 0.1
    s["current"] += np.random.normal(drift, cfg["variance"] * 0.15)
    if random.random() < cfg["spike"]:
        s["current"] += random.choice([-1, 1]) * 40 * random.random()
    s["current"] += np.random.normal(0, cfg["noise"])
    s["current"] = max(0, min(100, s["current"]))
    s["timestamps"].append(datetime.now())
    s["values"].append(s["current"])


def _hex_to_rgba(hex_color: str, alpha: float) -> str:
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _axis_base() -> dict[str, Any]:
    return dict(
        showgrid=True,
        gridcolor="rgba(42,47,54,0.5)",
        gridwidth=0.5,
        linecolor="#2a2f36",
        linewidth=1,
        tickfont=dict(
            family="JetBrains Mono, monospace",
            size=10,
            color="#5f6b7a",
        ),
        tickformat="%H:%M:%S",
    )


def _f1_line_chart(
    key: str,
    title: str,
    color: str,
    y_label: str,
    y_range: tuple[float, float] | None = None,
    height: int = 260,
) -> go.Figure:
    """Build chart from accumulated session_state series."""
    s = st.session_state[key]
    ts = list(s["timestamps"])
    vs = list(s["values"])
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=ts,
            y=vs,
            mode="lines",
            line=dict(color=color, width=2),
            fill="tozeroy",
            fillcolor=_hex_to_rgba(color, 0.08),
            hovertemplate="%{x|%H:%M:%S}<br>%{y:.1f}<extra></extra>",
            name=title,
        )
    )

    if vs:
        fig.add_trace(
            go.Scatter(
                x=[ts[-1]],
                y=[vs[-1]],
                mode="markers",
                marker=dict(color=color, size=10, symbol="circle"),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(
                family="JetBrains Mono, monospace",
                size=13,
                color="#d5dbdb",
            ),
            x=0,
            xanchor="left",
        ),
        margin=dict(l=40, r=20, t=50, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        showlegend=False,
        xaxis=dict(
            **_axis_base(),
        ),
        yaxis=dict(
            **_axis_base(),
            title=dict(text=y_label, font=dict(size=10, color="#5f6b7a")),
            range=y_range,
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#1e242b",
            bordercolor="#2a2f36",
            font=dict(
                family="JetBrains Mono, monospace",
                size=11,
                color="#d5dbdb",
            ),
        ),
        uirevision="constant",
    )

    return fig


def render() -> None:
    log_event("SYS", "Overview dashboard viewed", "info")

    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">Overview</div>
            <div class="page-subtitle">
                Rolling-window telemetry — 1s updates
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _render_telemetry()


@st.fragment(run_every=1)
def _render_telemetry() -> None:
    """Fragment: updates every 1s, appends 1 data point, slides window."""

    # Init all series on first run
    for key in _SERIES_DEFAULTS:
        _init_series(key)

    # Tick one new data point for each series
    for key in _SERIES_DEFAULTS:
        _tick(key)

    # ── Row 1: Uptime, Latency, RPS, Errors ──
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            _f1_line_chart(
                "uptime",
                "Platform Uptime",
                "#00a1c9",
                "UPTIME %",
                (70, 105),
            ),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with col2:
        st.plotly_chart(
            _f1_line_chart(
                "latency",
                "API Latency",
                "#ff9900",
                "MS",
                (0, 200),
            ),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            _f1_line_chart(
                "rps",
                "Requests / Second",
                "#44b9d6",
                "RPS",
                (0, 250),
            ),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with col2:
        st.plotly_chart(
            _f1_line_chart(
                "errors",
                "Error Rate",
                "#d13212",
                "ERR %",
                (0, 25),
            ),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    # ── Row 2: Multi-service timeline ──
    st.markdown("<div style='margin:20px 0;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-family:Cabinet Grotesk,sans-serif; "
        "font-size:12px; font-weight:600; color:#5f6b7a; "
        "text-transform:uppercase; letter-spacing:1px; "
        "margin-bottom:12px;'>Service Status Timeline</div>",
        unsafe_allow_html=True,
    )

    timeline_keys = ["pg", "fastapi", "mlflow"]
    timeline_colors = ["#1d8102", "#00a1c9", "#ff9900"]
    timeline_titles = ["PostgreSQL", "FastAPI", "MLflow"]

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.35, 0.35, 0.30],
        subplot_titles=timeline_titles,
    )

    for i, (key, color) in enumerate(zip(timeline_keys, timeline_colors, strict=True)):
        s = st.session_state[key]
        fig.add_trace(
            go.Scatter(
                x=list(s["timestamps"]),
                y=list(s["values"]),
                mode="lines",
                line=dict(color=color, width=1.5),
                fill="tozeroy",
                fillcolor=_hex_to_rgba(color, 0.06),
                hovertemplate="%{x|%H:%M:%S}<br>%{y:.1f}%<extra></extra>",
                name=timeline_titles[i],
            ),
            row=i + 1,
            col=1,
        )

    fig.update_layout(
        margin=dict(l=50, r=20, t=60, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=520,
        showlegend=False,
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#1e242b",
            bordercolor="#2a2f36",
            font=dict(
                family="JetBrains Mono, monospace",
                size=11,
                color="#d5dbdb",
            ),
        ),
        uirevision="constant",
    )

    for i in range(1, 4):
        fig.update_xaxes(
            showgrid=True,
            gridcolor="rgba(42,47,54,0.5)",
            gridwidth=0.5,
            linecolor="#2a2f36",
            tickfont=dict(
                family="JetBrains Mono, monospace",
                size=9,
                color="#5f6b7a",
            ),
            tickformat="%H:%M:%S",
            row=i,
            col=1,
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(42,47,54,0.5)",
            gridwidth=0.5,
            linecolor="#2a2f36",
            tickfont=dict(
                family="JetBrains Mono, monospace",
                size=9,
                color="#5f6b7a",
            ),
            range=(50, 105),
            row=i,
            col=1,
        )

    for annotation in fig["layout"]["annotations"]:
        annotation["font"] = dict(
            family="JetBrains Mono, monospace", size=11, color="#5f6b7a"
        )
        annotation["x"] = 0
        annotation["xanchor"] = "left"

    st.plotly_chart(
        fig, use_container_width=True, config={"displayModeBar": False}
    )
