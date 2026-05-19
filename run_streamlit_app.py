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
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None,
    },
)

# ── Theme configuration — applied before any rendering ──
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #0f141a !important;
    }
    [data-testid="stMain"] {
        background-color: #0f141a !important;
    }
    [data-testid="stSidebar"] {
        background-color: #16191f !important;
    }
    .stApp {
        background-color: #0f141a !important;
    }
    iframe {
        background-color: #0f141a !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

from streamlit_app.styles import CSS
from streamlit_app.utils import log_event

st.markdown(CSS, unsafe_allow_html=True)

# ── Force sidebar always open + flash prevention ──
st.markdown(
    """
    <script>
    (function() {
        // Prevent white flash — set dark background immediately
        document.documentElement.style.backgroundColor = '#0f141a';
        var styleEl = document.createElement('style');
        styleEl.textContent = 'html, body, .stApp, iframe { background-color: #0f141a !important; }';
        document.head.appendChild(styleEl);

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

# ── Sidebar ──────────────────────────────────────────────────────────────────

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
    <div class="sidebar-nav">
    """,
        unsafe_allow_html=True,
    )

    for section in _NAV_SECTIONS:
        st.markdown(
            f'<div class="sidebar-section-label">{section["label"]}</div>',
            unsafe_allow_html=True,
        )
        for item in section["items"]:
            page_key = item["key"]
            page_label = item["label"]
            icon_svg = item["icon"]
            active = " sidebar-nav-link--active" if page == page_key else ""
            st.markdown(
                f"""<a class="sidebar-nav-link{active}" href="?nav={page_key}" target="_self">
                  <span class="sidebar-nav-icon">{icon_svg}</span>
                  <span class="sidebar-nav-label">{page_label}</span>
                </a>""",
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

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
