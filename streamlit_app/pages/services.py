import streamlit as st

from streamlit_app.components.cards import page_header, section_title, service_card
from streamlit_app.utils import (
    SERVICE_LOGOS,
    SERVICES,
    check_docker_service,
    check_port,
)


def render() -> None:
    page_header("Services", "Live status of all infrastructure services")

    section_title("Infrastructure")
    for idx, (container, name, port) in enumerate(SERVICES):
        if idx % 3 == 0:
            cols = st.columns(3)
        running = check_docker_service(container)
        with cols[idx % 3]:
            service_card(name, port, running, SERVICE_LOGOS.get(name))

    st.markdown("<div style='margin:28px 0 16px 0;'></div>", unsafe_allow_html=True)
    section_title("Application")
    api_up = check_port(8000)
    with st.columns(3)[0]:
        service_card("FastAPI", 8000, api_up, SERVICE_LOGOS.get("FastAPI"))


render()
