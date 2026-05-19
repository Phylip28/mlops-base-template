# ruff: noqa: E501
from datetime import datetime

import streamlit as st

from streamlit_app.components.cards import metric_tile, page_header
from streamlit_app.utils import check_prometheus_scrape, refresh_services


def render() -> None:
    page_header("Overview", "System health and key metrics at a glance")

    now = datetime.now()
    svcs = refresh_services()
    prom_up, prom_err = check_prometheus_scrape()
    all_up = all(v["running"] for v in svcs.values()) and prom_up
    health_class = "health-ok" if all_up else "health-warn"
    health_label = "ALL SYSTEMS NOMINAL" if all_up else "DEGRADED MODE"

    st.markdown(
        f"""
    <div class="hero-banner">
        <div class="hero-left">
            <div class="hero-title">MLOps Command Center</div>
            <div class="hero-subtitle">
                Multi-Tenant Fraud Detection // Stream Learning Platform
            </div>
        </div>
        <div class="hero-right">
            <div>
                <div class="hero-clock">{now.strftime("%H:%M:%S")}</div>
                <div class="hero-date">{now.strftime("%Y-%m-%d")}</div>
                <div class="health-badge {health_class}">
                    <span class="health-dot"></span>
                    {health_label}
                </div>
                <div style="margin-top:5px;font-family:'JetBrains Mono',monospace;
                    font-size:10px;color:var(--text-muted);">
                    Prometheus: {"SCRAPE OK" if prom_up else f"ERR: {prom_err[:30]}"}
                </div>
            </div>
            <button class="refresh-btn" onclick="location.reload()">🔄</button>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="metric-row">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        metric_tile("5", "Services", "accent")
    with col2:
        metric_tile("2", "Containers", "purple")
    with col3:
        metric_tile(str(len(st.session_state.activity_log)), "Log Events", "green")
    with col4:
        metric_tile("30", "Retrain Threshold", "amber")
    with col5:
        metric_tile("8000", "API Port", "red")
    st.markdown("</div>", unsafe_allow_html=True)


render()
