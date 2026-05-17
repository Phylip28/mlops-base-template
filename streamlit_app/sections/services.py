import streamlit as st

from streamlit_app.utils import SERVICES, check_docker_service, check_port


def render_services() -> None:
    cols = st.columns(6)
    for idx, (container, name, port) in enumerate(SERVICES):
        running = check_docker_service(container)
        indicator_class = "up" if running else "down"
        badge_class = "badge-up" if running else "badge-down"
        badge_txt = "ONLINE" if running else "OFFLINE"
        with cols[idx]:
            st.markdown(
                f"""
            <div class="svc-card">
                <div class="svc-header">
                    <span class="svc-name">{name}</span>
                    <span class="svc-indicator {indicator_class}"></span>
                </div>
                <div class="svc-port">:{port}</div>
                <span class="badge {badge_class}">{badge_txt}</span>
            </div>
            """,
                unsafe_allow_html=True,
            )

    api_up = check_port(8000)
    indicator_class = "up" if api_up else "down"
    badge_class = "badge-up" if api_up else "badge-down"
    badge_txt = "ONLINE" if api_up else "OFFLINE"
    with cols[5]:
        st.markdown(
            f"""
        <div class="svc-card">
            <div class="svc-header">
                <span class="svc-name">FastAPI</span>
                <span class="svc-indicator {indicator_class}"></span>
            </div>
            <div class="svc-port">:8000</div>
            <span class="badge {badge_class}">{badge_txt}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )
