# ruff: noqa: E501
import streamlit as st

from streamlit_app.components.cards import page_header

_BRANDS = [
    ("Grafana", "http://localhost:3000", "#F46800", "G"),
    ("MLflow", "http://localhost:5000", "#0194E2", "ML"),
    ("MinIO", "http://localhost:9001", "#C72E49", "M"),
    ("FastAPI", "http://localhost:8000/docs", "#009688", "F"),
    ("Prometheus", "http://localhost:9090", "#E6522C", "P"),
    ("Prediction", "http://localhost:8002", "#8b5cf6", "P"),
]


def _build_grid() -> str:
    parts = ['<div class="link-grid">']
    for name, url, color, initial in _BRANDS:
        parts.append(
            f'<a href="{url}" target="_blank" rel="noopener" '
            f'class="link-card-wrapper">'
            f'<div class="link-card">'
            f'<div class="link-icon-badge" style="background:{color};">'
            f'<span class="link-initial">{initial}</span>'
            f"</div>"
            f'<div class="link-name">{name}</div>'
            f"</div>"
            f"</a>"
        )
    parts.append("</div>")
    return "".join(parts)


def render() -> None:
    page_header("Quick Access", "Open your platform services in new tabs")
    st.markdown(_build_grid(), unsafe_allow_html=True)


render()
