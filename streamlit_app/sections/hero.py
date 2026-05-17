from datetime import datetime

import streamlit as st

from streamlit_app.utils import check_prometheus_scrape, refresh_services


def render_hero() -> None:
    now = datetime.now()
    clock_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")

    svcs = refresh_services()
    prom_up, prom_err = check_prometheus_scrape()
    all_up = all(v["running"] for v in svcs.values()) and prom_up
    health_class = "health-ok" if all_up else "health-warn"
    health_label = "ALL SYSTEMS NOMINAL" if all_up else "DEGRADED MODE"
    prom_status = "SCRAPE OK" if prom_up else f"ERR: {prom_err[:30]}"

    col_left, col_right = st.columns([3, 1])
    with col_left:
        st.markdown(
            """
        <div class="hero">
            <div class="hero-left">
                <div class="hero-title">MLOps Command Center</div>
                <div class="hero-subtitle">
                    Multi-Tenant Fraud Detection // Stream Learning Platform
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            f"""
        <div class="hero" style="justify-content:flex-end;gap:12px;">
            <div>
                <div class="hero-clock">{clock_str}</div>
                <div class="hero-date">{date_str}</div>
                <div class="health-badge {health_class}">
                    <span class="health-dot"></span>
                    {health_label}
                </div>
                <div style="margin-top:5px;font-family:'JetBrains Mono',monospace;
                    font-size:10px;color:#64748b;">Prometheus: {prom_status}</div>
            </div>
            <button class="refresh-btn" onclick="location.reload()">🔄</button>
        </div>
        """,
            unsafe_allow_html=True,
        )
