# ruff: noqa: E501
from datetime import datetime

import streamlit as st

from streamlit_app.components.cards import page_header
from streamlit_app.utils import (
    SERVICES,
    check_docker_service,
    check_port,
    check_prometheus_scrape,
    refresh_services,
)


def _service_list_html() -> str:
    rows = []
    for container, name, port in SERVICES:
        running = check_docker_service(container)
        dot_cls = "up" if running else "down"
        badge = (
            '<span class="badge badge-up">ONLINE</span>'
            if running
            else '<span class="badge badge-down">OFFLINE</span>'
        )
        rows.append(
            f"""<div style="display:flex;align-items:center;justify-content:space-between;
            padding:10px 14px;border-bottom:1px solid var(--border);gap:12px;">
            <div style="display:flex;align-items:center;gap:10px;min-width:0;">
                <span class="svc-indicator {dot_cls}"></span>
                <span style="font-family:'Satoshi',sans-serif;font-size:13px;
                    font-weight:500;color:var(--text-body);">{name}</span>
            </div>
            <div style="display:flex;align-items:center;gap:10px;flex-shrink:0;">
                <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                    color:var(--text-muted);">:{port}</span>
                {badge}
            </div></div>"""
        )
    api_up = check_port(8000)
    api_dot = "up" if api_up else "down"
    api_badge = (
        '<span class="badge badge-up">ONLINE</span>'
        if api_up
        else '<span class="badge badge-down">OFFLINE</span>'
    )
    rows.append(
        f"""<div style="display:flex;align-items:center;justify-content:space-between;
        padding:10px 14px;gap:12px;">
        <div style="display:flex;align-items:center;gap:10px;min-width:0;">
            <span class="svc-indicator {api_dot}"></span>
            <span style="font-family:'Satoshi',sans-serif;font-size:13px;
                font-weight:500;color:var(--text-body);">FastAPI</span>
        </div>
        <div style="display:flex;align-items:center;gap:10px;flex-shrink:0;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                color:var(--text-muted);">:8000</span>
            {api_badge}
        </div></div>"""
    )
    return "".join(rows)


def _log_preview_html() -> str:
    entries = st.session_state.activity_log[-8:]
    if not entries:
        return (
            '<div class="log-entry">'
            '<span class="log-ts">--:--:--</span>'
            '<span class="log-tag log-tag-SYS">SYS</span>'
            '<span class="log-msg">No events recorded</span>'
            "</div>"
        )
    parts = []
    for ts, tag, msg, _level in reversed(entries):
        parts.append(
            f'<div class="log-entry">'
            f'<span class="log-ts">{ts}</span>'
            f'<span class="log-tag log-tag-{tag}">{tag}</span>'
            f'<span class="log-msg">{msg}</span>'
            f"</div>"
        )
    return "".join(parts)


def render() -> None:
    page_header("Overview", "")

    now = datetime.now()
    svcs = refresh_services()
    prom_up, prom_err = check_prometheus_scrape()
    all_up = all(v["running"] for v in svcs.values()) and prom_up
    health_class = "health-ok" if all_up else "health-warn"
    health_label = "All systems nominal" if all_up else "Degraded mode"
    prom_label = "Prometheus OK" if prom_up else f"Prometheus: {prom_err[:25]}"

    # ── Hero ──
    st.markdown(
        f"""<div class="hero-banner">
        <div class="hero-left">
            <div class="hero-title">MLOps Command Center</div>
            <div class="hero-subtitle">Multi-Tenant Fraud Detection · Stream Learning Platform</div>
        </div>
        <div class="hero-right">
            <div>
                <div class="hero-clock">{now.strftime("%H:%M:%S")}</div>
                <div class="hero-date">{now.strftime("%A, %d %B %Y")}</div>
                <div class="health-badge {health_class}">
                    <span class="health-dot"></span>{health_label}
                </div>
                <div style="margin-top:5px;font-family:'JetBrains Mono',monospace;
                    font-size:10px;color:#64748b;">{prom_label}</div>
            </div>
            <button class="refresh-btn" onclick="location.reload()">↻</button>
        </div></div>""",
        unsafe_allow_html=True,
    )

    # ── Metric Tiles ──
    st.markdown(
        '<div class="metric-row">'
        '<div class="metric-tile accent"><div class="metric-value">5</div><div class="metric-label">Total Services</div></div>'
        '<div class="metric-tile green"><div class="metric-value">'
        + str(len(st.session_state.activity_log))
        + '</div><div class="metric-label">Log Events</div></div>'
        '<div class="metric-tile purple"><div class="metric-value">2</div><div class="metric-label">Docker Groups</div></div>'
        '<div class="metric-tile amber"><div class="metric-value">30</div><div class="metric-label">Retrain Threshold</div></div>'
        '<div class="metric-tile red"><div class="metric-value">6</div><div class="metric-label">Endpoints</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    # ── Two-column: Infrastructure + Activity ──
    svc_html = _service_list_html()
    log_html = _log_preview_html()

    st.markdown(
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">'
        f'<div class="card card-striped" style="min-height:310px;">'
        f'<div class="section-title">Infrastructure Status</div>'
        f"{svc_html}</div>"
        f'<div class="card card-striped purple" style="min-height:310px;">'
        f'<div class="section-title">Recent Activity</div>'
        f'<div style="max-height:240px;overflow-y:auto;">{log_html}</div></div>'
        "</div>",
        unsafe_allow_html=True,
    )


render()
