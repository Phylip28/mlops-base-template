# ruff: noqa: E501
import streamlit as st

from streamlit_app.components.cards import page_header


def render() -> None:
    page_header("Quick Access", "Open your platform services in new tabs")

    links = [
        ("📊", "Grafana", "http://localhost:3000"),
        ("📈", "MLflow", "http://localhost:5000"),
        ("🗄️", "MinIO", "http://localhost:9001"),
        ("🌐", "FastAPI", "http://localhost:8000/docs"),
        ("🔔", "Prometheus", "http://localhost:9090"),
        ("🧮", "Prediction", "http://localhost:8002"),
    ]

    st.markdown('<div class="link-grid">', unsafe_allow_html=True)
    cols = st.columns(6)
    for idx, (icon, name, url) in enumerate(links):
        with cols[idx]:
            st.markdown(
                f'<div class="link-card" onclick="window.open(\'{url}\',\'_blank\')">'
                f'<div class="link-icon">{icon}</div>'
                f'<div class="link-name">{name}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


render()
