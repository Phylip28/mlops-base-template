import streamlit as st

from streamlit_app.components.cards import page_header, section_title, service_card
from streamlit_app.utils import SERVICES, check_docker_service, check_port


def render() -> None:
    page_header("Services", "Live status of all infrastructure services")

    section_title("Infrastructure")
    cols = st.columns(3)
    for idx, (container, name, port) in enumerate(SERVICES):
        running = check_docker_service(container)
        with cols[idx % 3]:
            if idx > 0 and idx % 3 == 0:
                cols = st.columns(3)
            service_card(name, port, running)

    section_title("Application")
    api_up = check_port(8000)
    with st.columns(3)[0]:
        service_card("FastAPI", 8000, api_up)


render()
