# ruff: noqa: E501
import streamlit as st

from streamlit_app.components.cards import page_header
from streamlit_app.utils import SERVICE_LOGOS

_LINKS = [
    ("Grafana", "http://localhost:3000", "Grafana"),
    ("MLflow", "http://localhost:5000", "MLflow"),
    ("MinIO", "http://localhost:9001", "MinIO"),
    ("FastAPI", "http://localhost:8000/docs", "FastAPI"),
    ("Prometheus", "http://localhost:9090", "Prometheus"),
    ("Prediction", "http://localhost:8001", "FastAPI"),
]


def _build_grid() -> str:
    parts = ['<div class="link-grid">']
    for name, url, logo_key in _LINKS:
        logo_url = SERVICE_LOGOS.get(logo_key) if logo_key else None
        if logo_url:
            logo_html = (
                f'<div class="link-icon-badge">'
                f'<img src="{logo_url}" alt="{name}" class="link-logo-img" '
                f"onerror=\"this.style.display='none';"
                f"this.nextElementSibling.style.display='block'\" />"
                f'<span class="link-initial" style="display:none">{name[0]}</span>'
                f"</div>"
            )
        else:
            logo_html = (
                f'<div class="link-icon-badge">'
                f'<span class="link-initial">{name[0]}</span>'
                f"</div>"
            )
        parts.append(
            f'<a href="{url}" target="_blank" rel="noopener" '
            f'class="link-card-wrapper">'
            f'<div class="link-card">'
            f"{logo_html}"
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
