# ruff: noqa: E501
from datetime import datetime

import streamlit as st

from streamlit_app.components.cards import metric_tile, page_header, section_title
from streamlit_app.utils import (
    SERVICES,
    check_docker_service,
    check_port,
    check_prometheus_scrape,
    refresh_services,
)


def _service_row(container: str, name: str, port: int) -> str:
    running = check_docker_service(container)
    dot = f'<span class="svc-indicator {"up" if running else "down"}"></span>'
    badge = (
        '<span class="badge badge-up">ONLINE</span>'
        if running
        else '<span class="badge badge-down">OFFLINE</span>'
    )
    return f"""
    <div style="display:flex;align-items:center;justify-content:space-between;
        padding:10px 14px;border-bottom:1px solid var(--border);gap:12px;">
        <div style="display:flex;align-items:center;gap:10px;min-width:0;">
            {dot}
            <span style="font-family:'Satoshi',sans-serif;font-size:13px;
                font-weight:500;color:var(--text-body);">{name}</span>
        </div>
        <div style="display:flex;align-items:center;gap:10px;flex-shrink:0;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                color:var(--text-muted);">:{port}</span>
            {badge}
        </div>
    </div>"""


def render() -> None:
    page_header("Overview", "")

    # ── Hero Banner ──
    now = datetime.now()
    svcs = refresh_services()
    prom_up, prom_err = check_prometheus_scrape()
    all_up = all(v["running"] for v in svcs.values()) and prom_up
    health_class = "health-ok" if all_up else "health-warn"
    health_label = "All systems nominal" if all_up else "Degraded mode"
    prom_label = "Prometheus OK" if prom_up else f"Prometheus: {prom_err[:25]}"

    st.markdown(
        f"""
    <div class="hero-banner">
        <div class="hero-left">
            <div class="hero-title">MLOps Command Center</div>
            <div class="hero-subtitle">Multi-Tenant Fraud Detection · Stream Learning Platform</div>
        </div>
        <div class="hero-right">
            <div>
                <div class="hero-clock">{now.strftime("%H:%M:%S")}</div>
                <div class="hero-date">{now.strftime("%A, %d %B %Y")}</div>
                <div class="health-badge {health_class}">
                    <span class="health-dot"></span>
                    {health_label}
                </div>
                <div style="margin-top:5px;font-family:'JetBrains Mono',monospace;
                    font-size:10px;color:#64748b;">{prom_label}</div>
            </div>
            <button class="refresh-btn" onclick="location.reload()">↻</button>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # ── Metric Tiles ──
    st.markdown('<div class="metric-row">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        metric_tile("5", "Total Services", "accent")
    with col2:
        metric_tile(str(len(st.session_state.activity_log)), "Log Events", "green")
    with col3:
        metric_tile("2", "Docker Groups", "purple")
    with col4:
        metric_tile("30", "Retrain Threshold", "amber")
    with col5:
        metric_tile("6", "Endpoints", "red")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Two-column: Services + Log ──
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown(
            '<div class="card card-striped" style="min-height:310px;">',
            unsafe_allow_html=True,
        )
        section_title("Infrastructure Status")
        html_parts = []
        for container, name, port in SERVICES:
            html_parts.append(_service_row(container, name, port))
        api_up = check_port(8000)
        api_dot = (
            '<span class="svc-indicator up"></span>'
            if api_up
            else '<span class="svc-indicator down"></span>'
        )
        api_badge = (
            '<span class="badge badge-up">ONLINE</span>'
            if api_up
            else '<span class="badge badge-down">OFFLINE</span>'
        )
        html_parts.append(
            f"""
        <div style="display:flex;align-items:center;justify-content:space-between;
            padding:10px 14px;gap:12px;">
            <div style="display:flex;align-items:center;gap:10px;min-width:0;">
                {api_dot}
                <span style="font-family:'Satoshi',sans-serif;font-size:13px;
                    font-weight:500;color:var(--text-body);">FastAPI</span>
            </div>
            <div style="display:flex;align-items:center;gap:10px;flex-shrink:0;">
                <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                    color:var(--text-muted);">:8000</span>
                {api_badge}
            </div>
        </div>"""
        )
        st.markdown("".join(html_parts), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown(
            '<div class="card card-striped purple" style="min-height:310px;">',
            unsafe_allow_html=True,
        )
        section_title("Recent Activity")
        entries = st.session_state.activity_log[-8:]
        if entries:
            log_html = ""
            for ts, tag, msg, _level in reversed(entries):
                log_html += f"""
                <div class="log-entry">
                    <span class="log-ts">{ts}</span>
                    <span class="log-tag log-tag-{tag}">{tag}</span>
                    <span class="log-msg">{msg}</span>
                </div>"""
            st.markdown(
                f'<div style="max-height:240px;overflow-y:auto;">{log_html}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="log-entry">'
                '<span class="log-ts">--:--:--</span>'
                '<span class="log-tag log-tag-SYS">SYS</span>'
                '<span class="log-msg">No events recorded</span>'
                "</div>",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)


render()
