# ruff: noqa: E402
import streamlit as st

st.set_page_config(
    page_title="MLOps Command Center",
    layout="wide",
    page_icon="🛰️",
)

from streamlit_app.sections import (
    render_api,
    render_docker,
    render_hero,
    render_links,
    render_log,
    render_overview,
    render_services,
    render_traffic,
)
from streamlit_app.styles import CSS
from streamlit_app.utils import log_event

st.markdown(CSS, unsafe_allow_html=True)

if "activity_log" not in st.session_state:
    st.session_state.activity_log = []

log_event("SYS", "Dashboard initialized", "info")


from collections.abc import Callable


def render_section(name: str, title: str, content_fn: Callable[[], None]) -> None:
    st.markdown(
        f'<div class="section-block"><span class="section-title">{title}</span></div>',
        unsafe_allow_html=True,
    )
    content_fn()
    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)


render_hero()

render_section(
    "system_overview",
    "System Overview",
    lambda: render_overview(len(st.session_state.activity_log)),
)
render_section("service_status", "Service Status", render_services)
render_section("docker_infra", "Docker Infrastructure", render_docker)
render_section("api_backend", "API Backend", render_api)
render_section("traffic_gen", "Traffic Generators", render_traffic)
render_section("activity_log", "Activity Log", render_log)
render_section("quick_access", "Quick Access", render_links)

st.markdown(
    '<div class="footer">'
    "MLOps Command Center // Multi-Tenant Fraud Detection // Stream Learning Platform"
    "</div>",
    unsafe_allow_html=True,
)
