"""Overview page — real-time F1 telemetry dashboard."""

from __future__ import annotations

import random
import time
from datetime import datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from streamlit_app.utils import log_event


def _generate_time_series(
    minutes: int = 60,
    base_value: float = 80.0,
    variance: float = 15.0,
    noise: float = 5.0,
    spike_prob: float = 0.02,
    spike_magnitude: float = 40.0,
) -> pd.DataFrame:
    """Generate synthetic telemetry data with realistic patterns."""
    now = datetime.now()
    timestamps = [now - timedelta(minutes=i) for i in range(minutes, 0, -1)]

    values = []
    current = base_value
    for _ in range(minutes):
        drift = (base_value - current) * 0.1
        change = np.random.normal(drift, variance * 0.15)
        current += change
        if random.random() < spike_prob:
            current += (
                random.choice([-1, 1]) * spike_magnitude * random.random()
            )
        current += np.random.normal(0, noise)
        current = max(0, min(100, current))
        values.append(current)

    return pd.DataFrame({"timestamp": timestamps, "value": values})


def _hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Convert hex color to rgba string."""
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _axis_base() -> dict[str, Any]:
    """Shared axis styling for F1 charts."""
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
        tickformat="%H:%M",
    )


def _f1_line_chart(
    df: pd.DataFrame,
    title: str,
    color: str,
    y_label: str,
    y_range: tuple[float, float] | None = None,
    height: int = 260,
) -> go.Figure:
    """Build a static F1-telemetry-style line chart."""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["value"],
            mode="lines",
            line=dict(color=color, width=2),
            fill="tozeroy",
            fillcolor=_hex_to_rgba(color, 0.08),
            hovertemplate="%{x|%H:%M:%S}<br>%{y:.1f}<extra></extra>",
            name=title,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[df["timestamp"].iloc[-1]],
            y=[df["value"].iloc[-1]],
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
            range=[df["timestamp"].iloc[0], df["timestamp"].iloc[-1]],
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
    )

    return fig


def _static_timeline(
    dfs: list[pd.DataFrame],
    titles: list[str],
    colors: list[str],
    height: int = 520,
) -> go.Figure:
    """Build a static multi-service timeline."""
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.35, 0.35, 0.30],
        subplot_titles=titles,
    )

    for i in range(3):
        fig.add_trace(
            go.Scatter(
                x=dfs[i]["timestamp"],
                y=dfs[i]["value"],
                mode="lines",
                line=dict(color=colors[i], width=1.5),
                fill="tozeroy",
                fillcolor=_hex_to_rgba(colors[i], 0.06),
                hovertemplate="%{x|%H:%M:%S}<br>%{y:.1f}%<extra></extra>",
                name=titles[i],
            ),
            row=i + 1,
            col=1,
        )

    x_min = min(df["timestamp"].iloc[0] for df in dfs)
    x_max = max(df["timestamp"].iloc[-1] for df in dfs)

    fig.update_layout(
        margin=dict(l=50, r=20, t=60, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
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
            tickformat="%H:%M",
            range=[x_min, x_max],
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

    return fig


def render() -> None:
    """Render the Overview page with auto-refresh."""
    log_event("SYS", "Overview dashboard viewed", "info")

    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">Overview</div>
            <div class="page-subtitle">
                Real-time platform telemetry — auto-refresh 5s
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Row 1: Uptime & Latency ──
    col1, col2 = st.columns(2)

    with col1:
        df_uptime = _generate_time_series(
            minutes=120, base_value=95, variance=8, noise=2, spike_prob=0.03
        )
        fig = _f1_line_chart(
            df_uptime,
            title="Platform Uptime",
            color="#00a1c9",
            y_label="UPTIME %",
            y_range=(70, 105),
        )
        st.plotly_chart(
            fig, use_container_width=True, config={"displayModeBar": False}
        )

    with col2:
        df_latency = _generate_time_series(
            minutes=120,
            base_value=45,
            variance=20,
            noise=5,
            spike_prob=0.05,
            spike_magnitude=80,
        )
        fig = _f1_line_chart(
            df_latency,
            title="API Latency",
            color="#ff9900",
            y_label="MS",
            y_range=(0, 200),
        )
        st.plotly_chart(
            fig, use_container_width=True, config={"displayModeBar": False}
        )

    # ── Row 2: Throughput & Error Rate ──
    col1, col2 = st.columns(2)

    with col1:
        df_rps = _generate_time_series(
            minutes=120,
            base_value=120,
            variance=30,
            noise=10,
            spike_prob=0.04,
        )
        fig = _f1_line_chart(
            df_rps,
            title="Requests / Second",
            color="#44b9d6",
            y_label="RPS",
            y_range=(0, 250),
        )
        st.plotly_chart(
            fig, use_container_width=True, config={"displayModeBar": False}
        )

    with col2:
        df_errors = _generate_time_series(
            minutes=120,
            base_value=2,
            variance=3,
            noise=1,
            spike_prob=0.08,
            spike_magnitude=15,
        )
        fig = _f1_line_chart(
            df_errors,
            title="Error Rate",
            color="#d13212",
            y_label="ERR %",
            y_range=(0, 25),
        )
        st.plotly_chart(
            fig, use_container_width=True, config={"displayModeBar": False}
        )

    # ── Row 3: Multi-service timeline ──
    st.markdown("<div style='margin:20px 0;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-family:Cabinet Grotesk,sans-serif; "
        "font-size:12px; font-weight:600; color:#5f6b7a; "
        "text-transform:uppercase; letter-spacing:1px; "
        "margin-bottom:12px;'>Service Status Timeline</div>",
        unsafe_allow_html=True,
    )

    service_configs = [
        ("PostgreSQL", "#1d8102", 95, 5),
        ("FastAPI", "#00a1c9", 98, 3),
        ("MLflow", "#ff9900", 88, 12),
    ]
    dfs = [
        _generate_time_series(
            minutes=120, base_value=base, variance=var, noise=2
        )
        for _name, _color, base, var in service_configs
    ]
    titles = [c[0] for c in service_configs]
    colors = [c[1] for c in service_configs]

    fig = _static_timeline(dfs, titles, colors)
    st.plotly_chart(
        fig, use_container_width=True, config={"displayModeBar": False}
    )

    # Auto-refresh every 5 seconds (AWS CloudWatch style)
    time.sleep(5)
    st.rerun()
