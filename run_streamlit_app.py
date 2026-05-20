# ruff: noqa: E402, E501
"""MLOps Command Center — Streamlit entry point with redesigned sidebar."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypedDict

import streamlit as st


class _NavItem(TypedDict):
    key: str
    label: str
    icon: str


class _NavSection(TypedDict):
    label: str
    items: list[_NavItem]


st.set_page_config(
    page_title="MLOps Command Center",
    layout="wide",
    page_icon="🛰️",
    initial_sidebar_state="expanded",
)

# ── Immediate dark background — prevents white flash on full page reload ──
st.markdown(
    "<style>html,body,#root,#root>*,.stApp,[data-testid='stAppViewContainer'],div[data-testid='stApp'],.main,.block-container,iframe{background:#0f141a!important}</style>",
    unsafe_allow_html=True,
)

from streamlit_app.styles import CSS
from streamlit_app.utils import log_event

st.markdown(CSS, unsafe_allow_html=True)

# ── Sidebar styling handled via CSS; avoid JS reloads ──

if "activity_log" not in st.session_state:
    st.session_state.activity_log = []
if "nav_page" not in st.session_state:
    st.session_state.nav_page = "overview"
if "_first_load" not in st.session_state:
    st.session_state._first_load = True
    st.session_state.nav_page = "overview"

# Sync from URL query param on initial load / refresh
nav_qp = st.query_params.get("nav")
if nav_qp and nav_qp in {
    "overview",
    "services",
    "activity",
    "docker",
    "api",
    "traffic",
    "links",
}:
    st.session_state.nav_page = nav_qp
elif st.session_state.get("_first_load"):
    st.session_state.nav_page = "overview"
    st.session_state._first_load = False

if st.session_state.get("nav_choice") != st.session_state.nav_page:
    st.session_state.nav_choice = st.session_state.nav_page

page: str = st.session_state.nav_page

log_event("SYS", "Dashboard initialized", "info")

# ── SVG Icons ────────────────────────────────────────────────────────────────

_ICONS: dict[str, str] = {
    "overview": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <rect x="3" y="3" width="7" height="7" rx="1.5"/>
      <rect x="14" y="3" width="7" height="7" rx="1.5"/>
      <rect x="3" y="14" width="7" height="7" rx="1.5"/>
      <rect x="14" y="14" width="7" height="7" rx="1.5"/>
    </svg>""",
    "services": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <rect x="2" y="2" width="20" height="8" rx="2"/>
      <rect x="2" y="14" width="20" height="8" rx="2"/>
      <line x1="6" y1="6" x2="6" y2="6.01" stroke-width="2.5"/>
      <line x1="6" y1="18" x2="6" y2="18.01" stroke-width="2.5"/>
    </svg>""",
    "activity": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="10"/>
      <polyline points="12 6 12 12 16 14"/>
    </svg>""",
    "docker": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <rect x="2" y="4" width="20" height="16" rx="2"/>
      <line x1="2" y1="8" x2="22" y2="8"/>
      <circle cx="9" cy="14" r="1.5" fill="currentColor"/>
      <circle cx="13" cy="14" r="1.5" fill="currentColor"/>
    </svg>""",
    "api": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="16 18 22 12 16 6"/>
      <polyline points="8 6 2 12 8 18"/>
    </svg>""",
    "traffic": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="22 2 14 10 18 10 18 18 10 18 10 14 2 22"/>
    </svg>""",
    "links": """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
      <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
    </svg>""",
}

_NAV_SECTIONS: list[_NavSection] = [
    {
        "label": "Monitor",
        "items": [
            {"key": "overview", "label": "Overview", "icon": _ICONS["overview"]},
            {"key": "services", "label": "Services", "icon": _ICONS["services"]},
            {"key": "activity", "label": "Activity", "icon": _ICONS["activity"]},
        ],
    },
    {
        "label": "Control",
        "items": [
            {"key": "docker", "label": "Infrastructure", "icon": _ICONS["docker"]},
            {"key": "api", "label": "API", "icon": _ICONS["api"]},
            {"key": "traffic", "label": "Traffic", "icon": _ICONS["traffic"]},
        ],
    },
    {
        "label": "Access",
        "items": [
            {"key": "links", "label": "Links", "icon": _ICONS["links"]},
        ],
    },
]

_NAV_KEYS: list[str] = []
_NAV_LABELS: dict[str, str] = {}
for section in _NAV_SECTIONS:
    for item in section["items"]:
        key = item["key"]
        _NAV_KEYS.append(key)
        _NAV_LABELS[key] = item["label"]

# ── Sidebar ──────────────────────────────────────────────────────────────────


def _nav_callback() -> None:
    page_key = st.session_state.nav_choice
    st.session_state.nav_page = page_key
    st.query_params["nav"] = page_key
    log_event("NAV", f"Navigated to {page_key}", "info")


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

    st.radio(
        "Navigation",
        options=_NAV_KEYS,
        index=_NAV_KEYS.index(page) if page in _NAV_KEYS else 0,
        format_func=lambda key: _NAV_LABELS.get(key, key),
        key="nav_choice",
        label_visibility="collapsed",
        on_change=_nav_callback,
    )

# ── Page routing ─────────────────────────────────────────────────────────────

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
