"""
Demo: Rolling-window line chart sin flicker.
Ejecutar con: streamlit run scripts/streaming_demo.py
"""

import time
from collections import deque
from datetime import datetime

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Streaming Demo", layout="wide")

# ── Parámetros ──
WINDOW_SECONDS = 60
UPDATE_INTERVAL = 1.0  # segundos

# ── Inicializar buffers en session_state ──
for key, base in [("cpu", 40), ("mem", 60), ("rps", 80)]:
    if key not in st.session_state:
        st.session_state[key] = {
            "timestamps": deque(maxlen=WINDOW_SECONDS),
            "values": deque(maxlen=WINDOW_SECONDS),
            "current": float(base),
        }


def _tick(key: str, base: float, noise: float = 3.0) -> None:
    """Generar un nuevo punto con random walk + mean reversion."""
    s = st.session_state[key]
    drift = (base - s["current"]) * 0.05
    s["current"] += np.random.normal(drift, noise)
    s["current"] = max(0, min(100, s["current"]))
    s["timestamps"].append(datetime.now())
    s["values"].append(s["current"])


def _build_chart(
    key: str, title: str, color: str, y_label: str, y_range: tuple
) -> go.Figure:
    s = st.session_state[key]
    fig = go.Figure(
        go.Scatter(
            x=list(s["timestamps"]),
            y=list(s["values"]),
            mode="lines",
            line=dict(color=color, width=2.5),
            fill="tozeroy",
            fillcolor=(
                f"rgba({int(color[1:3],16)},"
                f"{int(color[3:5],16)},"
                f"{int(color[5:7],16)},0.08)"
            ),
            hovertemplate="%{x|%H:%M:%S}<br>%{y:.1f}<extra></extra>",
        )
    )

    # Dot indicator
    if s["values"]:
        fig.add_trace(
            go.Scatter(
                x=[s["timestamps"][-1]],
                y=[s["values"][-1]],
                mode="markers",
                marker=dict(color=color, size=10, symbol="circle"),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family="JetBrains Mono, monospace", size=13, color="#d5dbdb"),
            x=0,
            xanchor="left",
        ),
        margin=dict(l=40, r=20, t=50, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        showlegend=False,
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(42,47,54,0.3)",
            gridwidth=0.5,
            linecolor="#2a2f36",
            tickfont=dict(family="JetBrains Mono, monospace", size=10, color="#5f6b7a"),
            tickformat="%H:%M:%S",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(42,47,54,0.3)",
            gridwidth=0.5,
            linecolor="#2a2f36",
            tickfont=dict(family="JetBrains Mono, monospace", size=10, color="#5f6b7a"),
            title=dict(text=y_label, font=dict(size=10, color="#5f6b7a")),
            range=y_range,
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#1e242b",
            bordercolor="#2a2f36",
            font=dict(family="JetBrains Mono, monospace", size=11, color="#d5dbdb"),
        ),
        uirevision="constant",  # ← evita que Plotly resetee zoom/pan
    )
    return fig


# ── UI ──
st.markdown("## Streaming demo — sliding window (60s)")
placeholder = st.empty()

# ── Loop infinito ──
while True:
    _tick("cpu", base=40, noise=5)
    _tick("mem", base=60, noise=3)
    _tick("rps", base=80, noise=8)

    with placeholder.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            st.plotly_chart(
                _build_chart("cpu", "CPU Usage", "#00a1c9", "CPU %", (0, 100)),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        with c2:
            st.plotly_chart(
                _build_chart("mem", "Memory", "#ff9900", "MEM %", (0, 100)),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        with c3:
            st.plotly_chart(
                _build_chart("rps", "Requests/s", "#44b9d6", "RPS", (0, 150)),
                use_container_width=True,
                config={"displayModeBar": False},
            )

    time.sleep(UPDATE_INTERVAL)
