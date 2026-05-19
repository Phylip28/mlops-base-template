import streamlit as st

from streamlit_app.utils import (
    SERVICE_LOGOS,
    SERVICES,
    check_docker_service,
    check_port,
)


def _card_html(
    name: str, port: int, running: bool, idx: int, logo_url: str | None = None
) -> str:
    badge_cls = "svc-status-up" if running else "svc-status-down"
    badge_txt = "Activo" if running else "Inactivo"
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
        logo_html = (
            f'<div class="svc-icon"><span class="svc-fallback">{name[0]}</span></div>'
        )
    col = idx % 3 + 1
    row = idx // 3 + 1
    if name == "Grafana":
        col = 3
        row = 2
    return f"""<div class="svc-card" style="grid-column:{col};grid-row:{row}">
        <span class="svc-name">{name}</span>
        {logo_html}
        <div class="svc-info">
            <span class="svc-port">Puerto: {port}</span>
            <span class="{badge_cls}">Estado: {badge_txt}</span>
        </div>
    </div>"""


def render_services() -> None:
    all_services: list[tuple[str, str, int]] = [
        (container, name, port) for container, name, port in SERVICES
    ]
    all_services.append(("", "FastAPI", 8000))

    cards: list[str] = []
    for idx, (container, name, port) in enumerate(all_services):
        running = check_docker_service(container) if container else check_port(8000)
        cards.append(_card_html(name, port, running, idx, SERVICE_LOGOS.get(name)))

    st.markdown(
        f'<div class="svc-grid">{"".join(cards)}</div>',
        unsafe_allow_html=True,
    )
