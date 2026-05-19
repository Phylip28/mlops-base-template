# ruff: noqa: E402
import streamlit as st

st.set_page_config(
    page_title="MLOps Command Center",
    layout="wide",
    page_icon="🛰️",
    initial_sidebar_state="expanded",
)

from streamlit_app.styles import CSS
from streamlit_app.utils import log_event

st.markdown(CSS, unsafe_allow_html=True)

if "activity_log" not in st.session_state:
    st.session_state.activity_log = []

log_event("SYS", "Dashboard initialized", "info")

with st.sidebar:
    st.markdown(
        """
    <div class="sidebar-brand">
        <div class="sidebar-brand-title">
            <span class="brand-dot"></span>
            <span>MLOps</span>
        </div>
        <div class="sidebar-brand-sub">Command Center</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

dashboard = st.Page(
    "streamlit_app/pages/overview.py",
    title="Overview",
    default=True,
)
services = st.Page(
    "streamlit_app/pages/services.py",
    title="Services",
)
activity = st.Page(
    "streamlit_app/pages/activity.py",
    title="Activity",
)
docker = st.Page(
    "streamlit_app/pages/docker.py",
    title="Docker",
)
api_page = st.Page(
    "streamlit_app/pages/api.py",
    title="API",
)
traffic = st.Page(
    "streamlit_app/pages/traffic.py",
    title="Traffic",
)
links = st.Page(
    "streamlit_app/pages/links.py",
    title="Links",
)

nav = st.navigation(
    {
        "Monitor": [dashboard, services, activity],
        "Control": [docker, api_page, traffic],
        "Access": [links],
    }
)

nav.run()
