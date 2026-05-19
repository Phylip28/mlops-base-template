# ruff: noqa: E501
import streamlit as st

from streamlit_app.components.cards import page_header

_BRANDS = [
    {
        "name": "Grafana",
        "url": "http://localhost:3000",
        "bg": "#F46800",
        "icon": (
            '<svg viewBox="0 0 24 24" fill="none" width="28" height="28">'
            '<rect x="3" y="14" width="4" height="7" rx="1" fill="#fff"/>'
            '<rect x="10" y="10" width="4" height="11" rx="1" fill="#fff"/>'
            '<rect x="17" y="4" width="4" height="17" rx="1" fill="#fff"/>'
            "</svg>"
        ),
    },
    {
        "name": "MLflow",
        "url": "http://localhost:5000",
        "bg": "#0194E2",
        "icon": (
            '<svg viewBox="0 0 24 24" fill="none" width="28" height="28">'
            '<path d="M12 2C9 2 6 5 6 8c0 2 1.2 3.8 3 4.7V18l3 3 3-3v-5.3'
            "c1.8-.9 3-2.7 3-4.7 0-3-3-6-6-6z"
            '" fill="none" stroke="#fff" stroke-width="1.8"/>'
            '<path d="M10 9h4M11 12h2" stroke="#fff" stroke-width="1.4"'
            ' stroke-linecap="round"/>'
            "</svg>"
        ),
    },
    {
        "name": "MinIO",
        "url": "http://localhost:9001",
        "bg": "#C72E49",
        "icon": (
            '<svg viewBox="0 0 24 24" fill="none" width="28" height="28">'
            '<path d="M12 4C7 4 4 7 4 10c0 1.5.5 3 1.5 4.2L12 20l6.5-5.8'
            "C19.5 13 20 11.5 20 10c0-3-3-6-8-6z"
            '" fill="none" stroke="#fff" stroke-width="1.8"/>'
            '<circle cx="12" cy="10" r="2" fill="#fff"/>'
            "</svg>"
        ),
    },
    {
        "name": "FastAPI",
        "url": "http://localhost:8000/docs",
        "bg": "#009688",
        "icon": (
            '<svg viewBox="0 0 24 24" fill="none" width="28" height="28">'
            '<path d="M13 2L4 14h5l-1 8 9-12h-5l1-8z"'
            ' fill="#fff"/>'
            "</svg>"
        ),
    },
    {
        "name": "Prometheus",
        "url": "http://localhost:9090",
        "bg": "#E6522C",
        "icon": (
            '<svg viewBox="0 0 24 24" fill="none" width="28" height="28">'
            '<path d="M12 2c-1.5 3-1.5 5-1 7 .5 2 2 3 1 5-1 2-3 3-2 5'
            ' 1 2 4 3 5 1 1-2-.5-4 1-6s4-3 4-6-2-5-4-5-2 0-4-1z"'
            '" fill="none" stroke="#fff" stroke-width="1.6"/>'
            '<path d="M10 6l2 2 2-2M9 10l3 3 3-3"'
            ' stroke="#fff" stroke-width="1.2" stroke-linecap="round"/>'
            "</svg>"
        ),
    },
    {
        "name": "Prediction UI",
        "url": "http://localhost:8002",
        "bg": "#8b5cf6",
        "icon": (
            '<svg viewBox="0 0 24 24" fill="none" width="28" height="28">'
            '<rect x="3" y="16" width="4" height="5" rx="1" fill="#fff"/>'
            '<rect x="9.5" y="11" width="4" height="10" rx="1" fill="#fff"/>'
            '<rect x="16" y="5" width="4" height="16" rx="1" fill="#fff"/>'
            "</svg>"
        ),
    },
]


def _brand_card(name: str, url: str, bg: str, icon: str) -> str:
    """Render a brand link card with SVG logo."""
    return (
        f'<div class="link-card" onclick="window.open(\'{url}\',\'_blank\')">'
        f'<div class="link-icon-badge" style="background:{bg};">'
        f"{icon}</div>"
        f'<div class="link-name">{name}</div>'
        f"</div>"
    )


def render() -> None:
    page_header("Quick Access", "Open your platform services in new tabs")

    st.markdown('<div class="link-grid">', unsafe_allow_html=True)
    cols = st.columns(6)
    for idx, brand in enumerate(_BRANDS):
        with cols[idx]:
            st.markdown(
                _brand_card(
                    brand["name"],
                    brand["url"],
                    brand["bg"],
                    brand["icon"],
                ),
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


render()
