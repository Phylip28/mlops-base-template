# ruff: noqa: E402
from collections.abc import Callable

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

# Nuclear JS: force sidebar open on Firefox / any browser
st.markdown(
    """
    <script>
    (function() {
        function forceOpen() {
            var s = document.querySelector('section[data-testid="stSidebar"]');
            if (!s) return;
            s.setAttribute('aria-expanded', 'true');
            s.style.setProperty('width', '260px', 'important');
            s.style.setProperty('min-width', '260px', 'important');
            s.style.setProperty('max-width', '260px', 'important');
            s.style.setProperty('transform', 'none', 'important');
            s.style.setProperty('margin-left', '0', 'important');
            s.style.setProperty('display', 'flex', 'important');
            s.style.setProperty('visibility', 'visible', 'important');
            s.style.setProperty('opacity', '1', 'important');
            s.style.setProperty('position', 'relative', 'important');
            s.style.setProperty('left', '0', 'important');
            s.style.setProperty('overflow', 'visible', 'important');
            s.style.setProperty('flex-shrink', '0', 'important');
            var header = s.querySelector('div[data-testid="stSidebarHeader"]');
            if (header) {
                header.style.setProperty('height', '0', 'important');
                header.style.setProperty('min-height', '0', 'important');
                header.style.setProperty('overflow', 'hidden', 'important');
                header.style.setProperty('padding', '0', 'important');
                header.style.setProperty('margin', '0', 'important');
                header.style.setProperty('opacity', '0', 'important');
                header.style.setProperty('pointer-events', 'none', 'important');
            }
            var cb = s.querySelector('div[data-testid="stSidebarCollapseButton"]');
            if (cb) cb.style.setProperty('display', 'none', 'important');
        }
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', forceOpen);
        } else {
            forceOpen();
        }
        setTimeout(forceOpen, 300);
        setTimeout(forceOpen, 1000);
        setTimeout(forceOpen, 2000);
    })();
    </script>
    """,
    unsafe_allow_html=True,
)

if "activity_log" not in st.session_state:
    st.session_state.activity_log = []
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "overview"

log_event("SYS", "Dashboard initialized", "info")

# ── Custom sidebar via st.sidebar ──
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

    st.markdown(
        '<div class="sidebar-section-label">Monitor</div>',
        unsafe_allow_html=True,
    )
    if st.button("⌂  Overview", key="nav_overview", use_container_width=True):
        st.session_state.nav_page = "overview"
        st.rerun()
    if st.button("⚙  Services", key="nav_services", use_container_width=True):
        st.session_state.nav_page = "services"
        st.rerun()
    if st.button("⌛  Activity", key="nav_activity", use_container_width=True):
        st.session_state.nav_page = "activity"
        st.rerun()

    st.markdown(
        '<div class="sidebar-section-label">Control</div>',
        unsafe_allow_html=True,
    )
    if st.button("⊞  Docker", key="nav_docker", use_container_width=True):
        st.session_state.nav_page = "docker"
        st.rerun()
    if st.button("⚡\ufe0e  API", key="nav_api", use_container_width=True):
        st.session_state.nav_page = "api"
        st.rerun()
    if st.button("⇆  Traffic", key="nav_traffic", use_container_width=True):
        st.session_state.nav_page = "traffic"
        st.rerun()

    st.markdown(
        '<div class="sidebar-section-label">Access</div>',
        unsafe_allow_html=True,
    )
    if st.button("⌘  Links", key="nav_links", use_container_width=True):
        st.session_state.nav_page = "links"
        st.rerun()

# ── Page routing ──
page = st.session_state.nav_page

from streamlit_app.pages.activity import render as activity_render
from streamlit_app.pages.api import render as api_render
from streamlit_app.pages.docker import render as docker_render
from streamlit_app.pages.links import render as links_render
from streamlit_app.pages.overview import render as overview_render
from streamlit_app.pages.services import render as services_render
from streamlit_app.pages.traffic import render as traffic_render

renderers: dict[str, Callable[[], None]] = {
    "overview": overview_render,
    "services": services_render,
    "activity": activity_render,
    "docker": docker_render,
    "api": api_render,
    "traffic": traffic_render,
    "links": links_render,
}

render_fn = renderers.get(page, overview_render)
render_fn()
