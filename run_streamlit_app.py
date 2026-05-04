import os
import subprocess
import sys
import time
import webbrowser
from datetime import datetime

import psutil
import streamlit as st

st.set_page_config(
    page_title="MLOps Command Center",
    layout="wide",
    page_icon="🛰️",
)

# ─────────────────────────────────────────────────────────────────────────────
# CLEAN SaaS CSS THEME
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-page:       #f8fafc;
        --bg-card:       #ffffff;
        --bg-subtle:     #f1f5f9;
        --primary:       #3b82f6;
        --primary-hover: #2563eb;
        --accent:        #06b6d4;
        --success:       #10b981;
        --danger:        #ef4444;
        --warning:       #f59e0b;
        --text:          #1e293b;
        --text-muted:    #64748b;
        --border:        #e2e8f0;
        --shadow:        0 2px 12px #0a0a0a10;
        --radius-card:   12px;
        --radius-btn:    8px;
        --radius-badge:  20px;
    }

    /* ── Base ── */
    .stApp { background: var(--bg-page) !important; }
    .stMarkdown, .stText { font-family: 'Inter', sans-serif; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg-subtle); border-radius: 4px; }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

    /* ── Cards ── */
    .card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-card);
        box-shadow: var(--shadow);
        padding: 20px 24px;
        position: relative;
        transition: box-shadow 0.15s ease, transform 0.15s ease;
    }
    .card:hover {
        box-shadow: 0 4px 20px #0a0a0a14;
        transform: translateY(-1px);
    }

    /* ── Section Title ── */
    .section-title-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 100%;
    }
    .section-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--text-muted);
        margin: 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-title::before {
        content: '';
        display: inline-block;
        width: 3px;
        height: 14px;
        background: var(--primary);
        border-radius: 2px;
        flex-shrink: 0;
    }

    /* ── Hero ── */
    .hero {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-card);
        box-shadow: var(--shadow);
        padding: 24px 28px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        gap: 16px;
    }
    .hero-left { flex: 1; }
    .hero-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 20px;
        font-weight: 700;
        color: var(--primary);
        margin: 0 0 4px 0;
    }
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        color: var(--text-muted);
        margin: 0;
    }
    .hero-right {
        display: flex;
        align-items: center;
        gap: 16px;
        text-align: right;
    }
    .hero-clock {
        font-family: 'JetBrains Mono', monospace;
        font-size: 18px;
        font-weight: 500;
        color: var(--text);
        letter-spacing: 1px;
    }
    .hero-date {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        color: var(--text-muted);
        margin-top: 2px;
    }
    .health-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: var(--radius-badge);
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        font-weight: 600;
    }
    .health-ok    { background: #dcfce7; color: #15803d; }
    .health-warn  { background: #fef3c7; color: #b45309; }
    .health-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
    }
    .health-ok  .health-dot  { background: var(--success); }
    .health-warn .health-dot { background: var(--warning); }

    /* ── Refresh Button ── */
    .refresh-btn {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        border: 1px solid var(--border);
        background: var(--bg-card);
        font-size: 16px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.15s ease;
        flex-shrink: 0;
    }
    .refresh-btn:hover {
        border-color: var(--primary);
        color: var(--primary);
        background: #eff6ff;
    }

    /* ── Section Block (static, no collapse) ── */
    .section-block {
        display: flex;
        align-items: center;
        padding: 8px 14px;
        background: var(--bg-subtle);
        border: 1px solid var(--border);
        border-radius: var(--radius-card);
        margin-bottom: 12px;
    }

    /* ── Metric Tiles ── */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-top: 3px solid var(--primary);
        border-radius: var(--radius-card);
        box-shadow: var(--shadow);
        padding: 16px 20px;
        text-align: center;
    }
    .metric-card.accent-top  { border-top-color: var(--accent); }
    .metric-card.success-top { border-top-color: var(--success); }
    .metric-card.warn-top    { border-top-color: var(--warning); }
    .metric-card.danger-top { border-top-color: var(--danger); }

    .metric-value {
        font-family: 'DM Sans', sans-serif;
        font-size: 30px;
        font-weight: 700;
        color: var(--primary);
        line-height: 1;
        margin-bottom: 5px;
    }
    .metric-card.accent-top  .metric-value { color: var(--accent); }
    .metric-card.success-top .metric-value { color: var(--success); }
    .metric-card.warn-top    .metric-value { color: var(--warning); }
    .metric-card.danger-top  .metric-value { color: var(--danger); }

    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 500;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ── Service Status Card ── */
    .svc-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-card);
        box-shadow: var(--shadow);
        padding: 16px 18px;
    }
    .svc-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    .svc-name {
        font-family: 'DM Sans', sans-serif;
        font-size: 13px;
        font-weight: 600;
        color: var(--text);
    }
    .svc-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .svc-indicator.up   { background: var(--success); }
    .svc-indicator.down { background: var(--danger); }
    .svc-port {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: var(--text-muted);
        margin-bottom: 8px;
    }
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2px 9px;
        border-radius: var(--radius-badge);
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 600;
    }
    .badge-up   { background: #dcfce7; color: #15803d; }
    .badge-down { background: #fee2e2; color: #dc2626; }

    /* ── Buttons ── */
    .stButton > button {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        border-radius: var(--radius-btn) !important;
        padding: 9px 16px !important;
        transition: all 0.15s ease !important;
        width: 100%;
    }
    div[data-testid="stHorizontalBlock"] .stButton > button {
        width: 100%;
    }

    .btn-primary > button {
        background: var(--primary) !important;
        color: #ffffff !important;
        border: none !important;
    }
    .btn-primary > button:hover {
        background: var(--primary-hover) !important;
        box-shadow: 0 4px 12px #3b82f640 !important;
    }

    .btn-secondary > button {
        background: transparent !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
    }
    .btn-secondary > button:hover {
        border-color: var(--primary) !important;
        color: var(--primary) !important;
        background: #eff6ff !important;
    }

    .btn-danger > button {
        background: transparent !important;
        color: var(--danger) !important;
        border: 1px solid #fecaca !important;
    }
    .btn-danger > button:hover {
        background: #fef2f2 !important;
        border-color: var(--danger) !important;
    }

    .btn-accent > button {
        background: transparent !important;
        color: var(--accent) !important;
        border: 1px solid #a5f3fc !important;
    }
    .btn-accent > button:hover {
        background: #ecfeff !important;
        border-color: var(--accent) !important;
    }

    /* ── Activity Log ── */
    .log-panel {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-card);
        box-shadow: var(--shadow);
        padding: 14px 18px;
        height: 200px;
        overflow-y: auto;
    }
    .log-entry {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 5px 0;
        border-bottom: 1px solid var(--bg-subtle);
    }
    .log-entry:last-child { border-bottom: none; }
    .log-ts {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: var(--text-muted);
        min-width: 58px;
        padding-top: 1px;
    }
    .log-tag {
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.5px;
        padding: 2px 7px;
        border-radius: 4px;
        min-width: 48px;
        text-align: center;
        flex-shrink: 0;
    }
    .log-tag-DOCKER { background: #eff6ff; color: var(--primary); }
    .log-tag-API    { background: #ecfeff; color: var(--accent); }
    .log-tag-GEN    { background: #f3e8ff; color: #9333ea; }
    .log-tag-ML     { background: #fef3c7; color: #b45309; }
    .log-tag-SYS    { background: var(--bg-subtle); color: var(--text-muted); }
    .log-msg {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        color: var(--text);
        flex: 1;
        padding-top: 1px;
    }

    /* ── Quick Access Cards ── */
    .link-card-wrap {
        display: flex;
        flex-direction: column;
        align-items: stretch;
        gap: 4px;
        position: relative;
    }
    .link-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-card);
        box-shadow: var(--shadow);
        padding: 14px 12px;
        text-align: center;
        cursor: pointer;
        transition: all 0.15s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 5px;
        text-decoration: none;
    }
    .link-card:hover {
        border-color: var(--primary);
        box-shadow: 0 4px 16px #3b82f620;
        transform: translateY(-2px);
    }
    .link-icon { font-size: 24px; line-height: 1; }
    .link-name {
        font-family: 'DM Sans', sans-serif;
        font-size: 12px;
        font-weight: 600;
        color: var(--text);
    }

    /* ── Info Button (tooltip) ── */
    .info-btn {
        position: absolute;
        top: 4px;
        right: 4px;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        border: 1px solid var(--border);
        background: var(--bg-card);
        font-size: 10px;
        color: var(--text-muted);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        cursor: default;
        flex-shrink: 0;
        z-index: 10;
    }
    .info-btn::after {
        content: attr(data-tip);
        position: absolute;
        bottom: 130%;
        left: 50%;
        transform: translateX(-50%);
        background: var(--text);
        color: #fff;
        font-size: 10px;
        font-family: 'JetBrains Mono', monospace;
        padding: 3px 8px;
        border-radius: 4px;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.15s;
        z-index: 100;
    }
    .info-btn:hover::after { opacity: 1; }

/* ── Section header row ── */
    .section-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        margin-top: 24px;
        padding: 14px;
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        color: var(--text-muted);
        letter-spacing: 0.5px;
    }

    /* ── Spacer ── */
    .section-spacer { margin-bottom: 6px; }

    /* ── Streamlit overrides ── */
    .st-spinner { color: var(--primary) !important; }
    div[data-testid="stDecoration"] { display: none; }
    section[data-testid="stSidebar"] { display: none; }
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "activity_log" not in st.session_state:
    st.session_state.activity_log = []


def log_event(tag: str, msg: str, level: str = "info") -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.activity_log.append((ts, tag, msg, level))
    if len(st.session_state.activity_log) > 80:
        st.session_state.activity_log.pop(0)


def get_python() -> str:
    venv = os.path.join(".venv", "Scripts", "python.exe")
    return venv if os.path.exists(venv) else sys.executable


def check_port(port: int) -> bool:
    try:
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                return True
    except Exception:
        pass
    return False


def check_docker_service(name: str) -> bool:
    try:
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", name],
            capture_output=True,
            text=True,
            timeout=3,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except Exception:
        return False


def check_prometheus_scrape() -> tuple[bool, str]:
    try:
        import urllib.request

        url = "http://localhost:9090/api/v1/targets"
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = resp.read()
        import json

        targets = json.loads(data)
        for t in targets.get("data", {}).get("activeTargets", []):
            if "mlops-api" in t.get("labels", {}).get("job", ""):
                return t.get("health") == "up", t.get("lastError", "ok")
        return False, "target not found"
    except Exception as e:
        return False, str(e)


def _get_docker_compose_cmd() -> list[str]:
    import shutil
    if shutil.which("docker-compose"):
        return ["docker-compose"]
    if shutil.which("docker"):
        return ["docker", "compose"]
    raise RuntimeError("Docker Compose no encontrado en este sistema")


SERVICES = [
    ("postgres", "PostgreSQL", 5432),
    ("mlops_minio", "MinIO", 9000),
    ("mlops_mlflow", "MLflow", 5000),
    ("mlops_prometheus", "Prometheus", 9090),
    ("mlops_grafana", "Grafana", 3000),
]


def refresh_services() -> dict:
    out = {}
    for container, name, port in SERVICES:
        running = check_docker_service(container)
        out[name] = {"running": running, "port": port}
    out["FastAPI"] = {"running": check_port(8000), "port": 8000}
    return out


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: SECTION BLOCK RENDERER (static, no collapse)
# ─────────────────────────────────────────────────────────────────────────────
def render_section(name: str, title: str, content_fn):
    st.markdown(
        f'<div class="section-block">'
        f'<span class="section-title">{title}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    content_fn()
    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────────────────────
now = datetime.now()
clock_str = now.strftime("%H:%M:%S")
date_str = now.strftime("%Y-%m-%d")

svcs = refresh_services()
prom_up, prom_err = check_prometheus_scrape()
all_up = all(v["running"] for v in svcs.values()) and prom_up
health_class = "health-ok" if all_up else "health-warn"
health_label = "ALL SYSTEMS NOMINAL" if all_up else "DEGRADED MODE"
prom_status = "SCRAPE OK" if prom_up else f"ERR: {prom_err[:30]}"

col_hero_left, col_hero_right = st.columns([3, 1])
with col_hero_left:
    st.markdown(
        """
    <div class="hero">
        <div class="hero-left">
            <div class="hero-title">🛰 MLOps Command Center</div>
            <div class="hero-subtitle">
                Multi-Tenant Fraud Detection // Stream Learning Platform
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

with col_hero_right:
    st.markdown(
        f"""
    <div class="hero" style="justify-content:flex-end;gap:12px;">
        <div>
            <div class="hero-clock">{clock_str}</div>
            <div class="hero-date">{date_str}</div>
            <div class="health-badge {health_class}" style="margin-top:6px;">
                <span class="health-dot"></span>
                {health_label}
            </div>
            <div style="
                margin-top:5px;
                font-family:'JetBrains Mono',monospace;
                font-size:10px;
                color:var(--text-muted);
            ">Prometheus: {prom_status}</div>
        </div>
        <button class="refresh-btn" onclick="location.reload()"
            >🔄
        </button>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: SYSTEM OVERVIEW (METRIC TILES)
# ─────────────────────────────────────────────────────────────────────────────
def section1_content():
    m_cols = st.columns(5)
    metrics = [
        ("5", "Services", "primary"),
        ("2", "Containers", "accent"),
        (str(len(st.session_state.activity_log)), "Log Events", "success"),
        ("30", "Retrain Threshold", "warning"),
        ("8000", "API Port", "danger"),
    ]
    for col, (val, lbl, color) in zip(m_cols, metrics):
        border_class = f"{color}-top"
        with col:
            st.markdown(
                f"""
            <div class="metric-card {border_class}">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{lbl}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )


render_section("system_overview", "System Overview", section1_content)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: SERVICE STATUS
# ─────────────────────────────────────────────────────────────────────────────
def section2_content():
    svc_cols = st.columns(6)
    for idx, (container, name, port) in enumerate(SERVICES):
        running = check_docker_service(container)
        indicator_class = "up" if running else "down"
        badge_class = "badge-up" if running else "badge-down"
        badge_txt = "ONLINE" if running else "OFFLINE"
        with svc_cols[idx]:
            st.markdown(
                f"""
            <div class="svc-card">
                <div class="svc-header">
                    <span class="svc-name">{name}</span>
                    <span class="svc-indicator {indicator_class}"></span>
                </div>
                <div class="svc-port">:{port}</div>
                <span class="badge {badge_class}">{badge_txt}</span>
            </div>
            """,
                unsafe_allow_html=True,
            )

    api_up = check_port(8000)
    indicator_class = "up" if api_up else "down"
    badge_class = "badge-up" if api_up else "badge-down"
    badge_txt = "ONLINE" if api_up else "OFFLINE"
    with svc_cols[5]:
        st.markdown(
            f"""
        <div class="svc-card">
            <div class="svc-header">
                <span class="svc-name">FastAPI</span>
                <span class="svc-indicator {indicator_class}"></span>
            </div>
            <div class="svc-port">:8000</div>
            <span class="badge {badge_class}">{badge_txt}</span>
        </div>
        """,
            unsafe_allow_html=True,
        )


render_section("service_status", "Service Status", section2_content)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: DOCKER INFRASTRUCTURE
# ─────────────────────────────────────────────────────────────────────────────
def section3_content():
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("▶  Start", key="btn_docker_start", use_container_width=True):
            with st.spinner("Starting containers..."):
                try:
                    cmd = _get_docker_compose_cmd() + ["up", "-d"]
                    subprocess.run(cmd, check=True)
                    log_event("DOCKER", "Containers started", "info")
                    st.rerun()
                except Exception as e:
                    log_event("DOCKER", f"Start failed: {e}", "error")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("■  Stop", key="btn_docker_stop", use_container_width=True):
            with st.spinner("Stopping containers..."):
                try:
                    cmd = _get_docker_compose_cmd() + ["down"]
                    subprocess.run(cmd, check=True)
                    log_event("DOCKER", "Containers stopped", "info")
                    st.rerun()
                except Exception as e:
                    log_event("DOCKER", f"Stop failed: {e}", "error")
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="btn-accent">', unsafe_allow_html=True)
        if st.button("↺  Restart", key="btn_docker_restart", use_container_width=True):
            with st.spinner("Restarting..."):
                try:
                    dc = _get_docker_compose_cmd()
                    subprocess.run(dc + ["down"], check=True)
                    subprocess.run(dc + ["up", "-d"], check=True)
                    log_event("DOCKER", "Containers restarted", "info")
                    st.rerun()
                except Exception as e:
                    log_event("DOCKER", f"Restart failed: {e}", "error")
        st.markdown("</div>", unsafe_allow_html=True)


render_section("docker_infra", "Docker Infrastructure", section3_content)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: API BACKEND
# ─────────────────────────────────────────────────────────────────────────────
def section4_content():
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("▶  Start API", key="btn_api_start", use_container_width=True):
            if check_port(8000):
                st.warning("Port 8000 already in use")
                log_event("API", "Start blocked — port in use", "info")
            else:
                py = get_python()
                cmd = [
                    py,
                    "-m",
                    "uvicorn",
                    "src.model_service.infrastructure.entrypoints.api:app",
                    "--host",
                    "0.0.0.0",
                    "--port",
                    "8000",
                ]
                subprocess.Popen(cmd)
                log_event("API", "FastAPI started on port 8000", "info")
                time.sleep(1)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("■  Stop API", key="btn_api_stop", use_container_width=True):
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    cmdline = " ".join(proc.info.get("cmdline") or [])
                    if "uvicorn" in cmdline and "8000" in cmdline:
                        proc.kill()
                except Exception:
                    pass
            log_event("API", "FastAPI stopped", "info")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


render_section("api_backend", "API Backend", section4_content)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: TRAFFIC GENERATORS
# ─────────────────────────────────────────────────────────────────────────────
def section5_content():
    t_cols = st.columns(4)

    with t_cols[0]:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("⚡  E2E Burst", key="btn_e2e", use_container_width=True):
            py = get_python()
            log_file = open("e2e_demo.log", "w", encoding="utf-8")
            subprocess.Popen(
                [py, "scripts/e2e_demo_mlflow.py"],
                stdout=log_file,
                stderr=subprocess.STDOUT,
            )
            log_event("GEN", "E2E burst triggered — 35 events", "info")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with t_cols[1]:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("Start Stream", key="btn_stream_start", use_container_width=True):
            py = get_python()
            log_file = open("streaming.log", "w", encoding="utf-8")
            subprocess.Popen(
                [py, "scripts/simulate_multi_streaming.py"],
                stdout=log_file,
                stderr=subprocess.STDOUT,
            )
            log_event("GEN", "Streaming simulation started", "info")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with t_cols[2]:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("Stop Streaming", key="btn_stream_stop", use_container_width=True):
            for proc in psutil.process_iter(["pid", "name", "cmdline"]):
                try:
                    cmdline = " ".join(proc.info.get("cmdline") or [])
                    if "simulate_multi_streaming" in cmdline:
                        proc.kill()
                except Exception:
                    pass
            log_event("GEN", "Streaming stopped", "info")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with t_cols[3]:
        st.markdown('<div class="btn-accent">', unsafe_allow_html=True)
        if st.button("Trigger Retrain", key="btn_retrain", use_container_width=True):
            log_event("ML", "Manual retrain triggered", "info")
            py = get_python()
            subprocess.Popen([py, "scripts/e2e_demo_mlflow.py"])
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


render_section("traffic_gen", "Traffic Generators", section5_content)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: ACTIVITY LOG
# ─────────────────────────────────────────────────────────────────────────────
def section6_content():
    log_entries = st.session_state.activity_log[-40:]
    if log_entries:
        log_html = ""
        for entry in reversed(log_entries):
            ts, tag, msg, level = entry
            log_html += f"""
            <div class="log-entry">
                <span class="log-ts">{ts}</span>
                <span class="log-tag log-tag-{tag}">{tag}</span>
                <span class="log-msg">{msg}</span>
            </div>
            """
        st.markdown(f'<div class="log-panel">{log_html}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="log-panel">'
            '<div class="log-entry">'
            '<span class="log-ts">--:--:--</span>'
            '<span class="log-tag log-tag-SYS">SYS</span>'
            '<span class="log-msg">Awaiting events...</span>'
            "</div></div>",
            unsafe_allow_html=True,
        )


render_section("activity_log", "Activity Log", section6_content)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7: QUICK ACCESS
# ─────────────────────────────────────────────────────────────────────────────
def section7_content():
    links = [
        ("📊", "Grafana", "http://localhost:3000", "3000"),
        ("📈", "MLflow", "http://localhost:5000", "5000"),
        ("🗄️", "MinIO", "http://localhost:9001", "9001"),
        ("🌐", "FastAPI", "http://localhost:8000/docs", "8000"),
        ("🔔", "Prometheus", "http://localhost:9090", "9090"),
        ("🧮", "Prediction UI", "http://localhost:8001", "8001"),
    ]

    link_cols = st.columns(len(links))
    for idx, (icon, name, url, port_str) in enumerate(links):
        with link_cols[idx]:
            st.markdown(
                f'<div class="link-card-wrap">'
                f'<span class="info-btn" data-tip=":{port_str}">ⓘ</span>',
                unsafe_allow_html=True,
            )
            if st.button(
                f"{icon}  {name}",
                key=f"link_{name.replace(' ', '_')}",
                use_container_width=True,
            ):
                webbrowser.open(url)
            st.markdown("</div>", unsafe_allow_html=True)


render_section("quick_access", "Quick Access", section7_content)

st.markdown("")
st.markdown(
    """
<div class="footer">
    MLOps Command Center // Multi-Tenant Fraud Detection // Stream Learning Platform
</div>
""",
    unsafe_allow_html=True,
)
