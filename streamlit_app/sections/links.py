import webbrowser

import streamlit as st


def render_links() -> None:
    links = [
        ("📊", "Grafana", "http://localhost:3000", "3000"),
        ("📈", "MLflow", "http://localhost:5000", "5000"),
        ("🗄️", "MinIO", "http://localhost:9001", "9001"),
        ("🌐", "FastAPI", "http://localhost:8000/docs", "8000"),
        ("🔔", "Prometheus", "http://localhost:9090", "9090"),
        ("🧮", "Prediction UI", "http://localhost:8001", "8001"),
    ]

    cols = st.columns(len(links))
    for idx, (icon, name, url, port_str) in enumerate(links):
        with cols[idx]:
            if st.button(
                f"{icon}  {name}",
                key=f"link_{name.replace(' ', '_')}",
                use_container_width=True,
            ):
                webbrowser.open(url)
