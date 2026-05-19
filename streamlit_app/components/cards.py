import streamlit as st


def metric_tile(value: str, label: str, color: str = "accent") -> None:
    st.markdown(
        f"""
    <div class="metric-tile {color}">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def service_card(name: str, port: int, running: bool) -> None:
    indicator = "up" if running else "down"
    badge_cls = "badge-up" if running else "badge-down"
    badge_txt = "ONLINE" if running else "OFFLINE"
    st.markdown(
        f"""
    <div class="svc-card">
        <div class="svc-header">
            <span class="svc-name">{name}</span>
            <span class="svc-indicator {indicator}"></span>
        </div>
        <div class="svc-port">:{port}</div>
        <span class="badge {badge_cls}">{badge_txt}</span>
    </div>
    """,
        unsafe_allow_html=True,
    )


def section_title(text: str) -> None:
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
    <div class="page-header">
        <div class="page-title">{title}</div>
        {f'<div class="page-subtitle">{subtitle}</div>' if subtitle else ""}
    </div>
    """,
        unsafe_allow_html=True,
    )
