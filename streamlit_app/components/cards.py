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


def service_card(
    name: str, port: int, running: bool, logo_url: str | None = None
) -> None:
    badge_cls = "svc-status-up" if running else "svc-status-down"
    badge_txt = "Online" if running else "Offline"
    if logo_url:
        logo_html = (
            f'<div class="svc-icon">'
            f'<img src="{logo_url}" alt="{name}" class="svc-logo-img" '
            f"onerror=\"this.style.display='none';"
            f"this.nextElementSibling.style.display='block'\" />"
            f'<span class="svc-fallback" style="display:none">{name[0]}</span>'
            f"</div>"
        )
    else:
        logo_html = f"""<div class="svc-icon">
                <span class="svc-fallback">{name[0]}</span>
            </div>"""
    st.markdown(
        f"""
    <div class="svc-card">
        <span class="svc-name">{name}</span>
        {logo_html}
        <div class="svc-info">
            <span class="svc-port">Port: {port}</span>
            <span class="{badge_cls}">State: {badge_txt}</span>
        </div>
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
