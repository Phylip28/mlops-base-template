"""Telemetry page — F1-style service monitoring dashboards."""

from __future__ import annotations

import random
from datetime import datetime, timedelta

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


def _f1_line_chart(
    df: pd.DataFrame,
    title: str,
    color: str,
    y_label: str,
    y_range: tuple[float, float] | None = None,
    height: int = 260,
) -> go.Figure:
    """Build an F1-telemetry-style line chart."""
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
                family="JetBrains Mono, monospace", size=13, color="#d5dbdb"
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
        ),
        yaxis=dict(
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


def _gauge_card(
    title: str, value: float, color: str, unit: str = "%"
) -> str:
    """Render an F1-style gauge indicator."""
    bar_width = int(value)
    shadow = f"0 0 8px {color}80"
    return (
        f'<div style="background:linear-gradient(180deg, #16191f 0%, '
        f'#0f141a 100%); border:1px solid #2a2f36; border-radius:8px; '
        f'padding:16px; margin-bottom:12px;">'
        f'<div style="display:flex; justify-content:space-between; '
        f'align-items:center; margin-bottom:10px;">'
        f'<span style="font-family:Cabinet Grotesk,sans-serif; '
        f'font-size:12px; font-weight:600; color:#5f6b7a; '
        f'text-transform:uppercase; letter-spacing:1px;">'
        f"{title}</span>"
        f'<span style="font-family:JetBrains Mono,monospace; '
        f'font-size:20px; font-weight:700; color:{color};">'
        f'{value:.1f}<span style="font-size:12px; color:#5f6b7a; '
        f'margin-left:2px;">{unit}</span></span></div>'
        f'<div style="background:#0f141a; border-radius:4px; '
        f'height:6px; overflow:hidden;">'
        f'<div style="width:{bar_width}%; height:100%; '
        f'background:{color}; border-radius:4px; box-shadow:{shadow}; '
        f'transition:width 0.5s ease;"></div></div></div>'
    )


def render() -> None:
    """Render the Telemetry page."""
    log_event("TELEMETRY", "Telemetry dashboard viewed", "info")

    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">Telemetry</div>
            <div class="page-subtitle">
                Real-time service telemetry
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### System Health Gauges")
    cols = st.columns(4)
    services = [
        ("PostgreSQL", 98.2, "#1d8102"),
        ("FastAPI", 99.7, "#1d8102"),
        ("MLflow", 94.5, "#ff9900"),
        ("Prometheus", 91.3, "#ff9900"),
    ]
    for col, (name, val, color) in zip(cols, services, strict=True):
        with col:
            st.markdown(
                _gauge_card(name, val, color), unsafe_allow_html=True
            )

    st.markdown("<div style='margin:20px 0;'></div>", unsafe_allow_html=True)

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

    st.markdown("<div style='margin:20px 0;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-family:Cabinet Grotesk,sans-serif; "
        "font-size:12px; font-weight:600; color:#5f6b7a; "
        "text-transform:uppercase; letter-spacing:1px; "
        "margin-bottom:12px;'>Service Status Timeline</div>",
        unsafe_allow_html=True,
    )

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.35, 0.35, 0.30],
        subplot_titles=("PostgreSQL", "FastAPI", "MLflow"),
    )

    service_configs = [
        ("PostgreSQL", "#1d8102", 95, 5),
        ("FastAPI", "#00a1c9", 98, 3),
        ("MLflow", "#ff9900", 88, 12),
    ]

    for i, (name, color, base, var) in enumerate(service_configs, 1):
        df = _generate_time_series(
            minutes=120, base_value=base, variance=var, noise=2
        )
        fig.add_trace(
            go.Scatter(
                x=df["timestamp"],
                y=df["value"],
                mode="lines",
                line=dict(color=color, width=1.5),
                fill="tozeroy",
                fillcolor=_hex_to_rgba(color, 0.06),
                hovertemplate="%{x|%H:%M:%S}<br>%{y:.1f}%<extra></extra>",
                name=name,
            ),
            row=i,
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
