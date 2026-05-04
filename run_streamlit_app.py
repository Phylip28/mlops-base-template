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
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-page:       #f8fafc;
        --bg-card:      #ffffff;
        --bg-subtle:    #f1f5f9;
        --primary:      #3b82f6;
        --primary-hover:#2563eb;
        --accent:       #06b6d4;
        --success:      #10b981;
        --danger:       #ef4444;
        --warning:      #f59e0b;
        --text:         #1e293b;
        --text-muted:   #64748b;
        --border:       #e2e8f0;
        --shadow:       0 2px 12px #0a0a0a10;
        --radius-card:  12px;
        --radius-btn:   8px;
        --radius-badge: 20px;
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
    .section-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--text-muted);
        margin-bottom: 14px;
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
    }

    /* ── Hero ── */
    .hero {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-card);
        box-shadow: var(--shadow);
        padding: 28px 32px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 28px;
    }
    .hero-left {}
    .hero-title {
        font-family: 'DM Sans', sans-serif;
        font-size: 22px;
        font-weight: 700;
        color: var(--primary);
        margin: 0 0 4px 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: var(--text-muted);
        margin: 0;
        letter-spacing: 0.3px;
    }
    .hero-right {
        text-align: right;
    }
    .hero-clock {
        font-family: 'JetBrains Mono', monospace;
        font-size: 20px;
        font-weight: 500;
        color: var(--text);
        letter-spacing: 1px;
    }
    .hero-date {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        color: var(--text-muted);
        margin-top: 2px;
    }
    .health-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-top: 10px;
        padding: 4px 12px;
        border-radius: var(--radius-badge);
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        font-weight: 600;
    }
    .health-ok {
        background: #dcfce7;
        color: #15803d;
    }
    .health-warn {
        background: #fef3c7;
        color: #b45309;
    }
    .health-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
    }
    .health-ok .health-dot  { background: var(--success); }
    .health-warn .health-dot { background: var(--warning); }

    /* ── Metric Tiles ── */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-top: 3px solid var(--primary);
        border-radius: var(--radius-card);
        box-shadow: var(--shadow);
        padding: 18px 22px;
        text-align: center;
    }
    .metric-card.accent-top  { border-top-color: var(--accent); }
    .metric-card.success-top { border-top-color: var(--success); }
    .metric-card.warn-top    { border-top-color: var(--warning); }
    .metric-card.danger-top { border-top-color: var(--danger); }

    .metric-value {
        font-family: 'DM Sans', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: var(--primary);
        line-height: 1;
        margin-bottom: 6px;
    }
    .metric-card.accent-top  .metric-value { color: var(--accent); }
    .metric-card.success-top .metric-value { color: var(--success); }
    .metric-card.warn-top    .metric-value { color: var(--warning); }
    .metric-card.danger-top  .metric-value { color: var(--danger); }

    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 11px;
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
        padding: 18px 20px;
    }
    .svc-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    .svc-name {
        font-family: 'DM Sans', sans-serif;
        font-size: 14px;
        font-weight: 600;
        color: var(--text);
    }
    .svc-indicator {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .svc-indicator.up   { background: var(--success); }
    .svc-indicator.down{ background: var(--danger); }
    .svc-port {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: var(--text-muted);
        margin-bottom: 10px;
    }
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 10px;
        border-radius: var(--radius-badge);
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 600;
    }
    .badge-up {
        background: #dcfce7;
        color: #15803d;
    }
    .badge-down {
        background: #fee2e2;
        color: #dc2626;
    }

    /* ── Buttons ── */
    .stButton > button {
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        border-radius: var(--radius-btn) !important;
        padding: 10px 18px !important;
        transition: all 0.15s ease !important;
        width: 100%;
    }
    div[data-testid="stHorizontalBlock"] .stButton > button {
        width: 100%;
    }

    /* Primary button - blue */
    .btn-primary > button {
        background: var(--primary) !important;
        color: #ffffff !important;
        border: none !important;
    }
    .btn-primary > button:hover {
        background: var(--primary-hover) !important;
        box-shadow: 0 4px 12px #3b82f640 !important;
    }

    /* Secondary button - ghost with border */
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

    /* Danger button - red */
    .btn-danger > button {
        background: transparent !important;
        color: var(--danger) !important;
        border: 1px solid #fecaca !important;
    }
    .btn-danger > button:hover {
        background: #fef2f2 !important;
        border-color: var(--danger) !important;
    }

    /* Accent button - teal */
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
        padding: 16px 20px;
        height: 220px;
        overflow-y: auto;
    }
    .log-entry {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 6px 0;
        border-bottom: 1px solid var(--bg-subtle);
    }
    .log-entry:last-child { border-bottom: none; }
    .log-ts {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: var(--text-muted);
        min-width: 60px;
        padding-top: 1px;
    }
    .log-tag {
        font-family: 'Inter', sans-serif;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.5px;
        padding: 2px 8px;
        border-radius: 4px;
        min-width: 50px;
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

    .log-caption {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: var(--text-muted);
    }

    /* ── Quick Access Cards ── */
    .link-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-card);
        box-shadow: var(--shadow);
        padding: 16px 14px;
        text-align: center;
        cursor: pointer;
        transition: all 0.15s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        text-decoration: none;
    }
    .link-card:hover {
        border-color: var(--primary);
        box-shadow: 0 4px 16px #3b82f620;
        transform: translateY(-2px);
    }
    .link-icon {
        font-size: 26px;
        line-height: 1;
    }
    .link-name {
        font-family: 'DM Sans', sans-serif;
        font-size: 13px;
        font-weight: 600;
        color: var(--text);
    }
    .link-caption {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: var(--text-muted);
    }

    /* ── Section header row ── */
    .section-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 14px;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        margin-top: 28px;
        padding: 16px;
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        color: var(--text-muted);
        letter-spacing: 0.5px;
    }

    /* ── Streamlit overrides ── */
    .st-spinner { color: var(--primary) !important; }
    div[data-testid="stDecoration"] { display: none; }
    section[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

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
            capture_output=True, text=True, timeout=3,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except Exception:
        return False


SERVICES = [
    ("postgres",        "PostgreSQL",  5432),
    ("mlops_minio",      "MinIO",       9000),
    ("mlops_mlflow",     "MLflow",      5000),
    ("mlops_prometheus", "Prometheus",  9090),
    ("mlops_grafana",    "Grafana",     3000),
]


def refresh_services() -> dict:
    out = {}
    for container, name, port in SERVICES:
        running = check_docker_service(container)
        out[name] = {"running": running, "port": port}
    out["FastAPI"] = {"running": check_port(8000), "port": 8000}
    return out


# ─────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────────────────────
now = datetime.now()
clock_str = now.strftime("%H:%M:%S")
date_str  = now.strftime("%Y-%m-%d")

svcs = refresh_services()
all_up = all(v["running"] for v in svcs.values())
health_class = "health-ok" if all_up else "health-warn"
health_label = "ALL SYSTEMS NOMINAL" if all_up else "DEGRADED MODE"

col_hero_left, col_hero_right = st.columns([3, 1])
with col_hero_left:
    st.markdown("""
    <div class="hero">
        <div class="hero-left">
            <div class="hero-title">🛰 MLOps Command Center</div>
            <div class="hero-subtitle">
                Multi-Tenant Fraud Detection // Stream Learning Platform
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_hero_right:
    st.markdown(f"""
    <div class="hero" style="text-align:right;">
        <div class="hero-clock">{clock_str}</div>
        <div class="hero-date">{date_str}</div>
        <div class="health-badge {health_class}">
            <span class="health-dot"></span>
            {health_label}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# METRIC TILES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">System Overview</div>', unsafe_allow_html=True)

m_cols = st.columns(5)
metrics = [
    ("5",              "Services",     "primary"),
    ("2",              "Containers",    "accent"),
    (str(len(st.session_state.activity_log)), "Log Events", "success"),
    ("30",             "Retrain Threshold", "warning"),
    ("8000",           "API Port",     "danger"),
]
for col, (val, lbl, color) in zip(m_cols, metrics):
    border_class = f"{color}-top"
    with col:
        st.markdown(f"""
        <div class="metric-card {border_class}">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")

# ─────────────────────────────────────────────────────────────────────────────
# SERVICE STATUS GRID
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Service Status</div>', unsafe_allow_html=True)

svc_cols = st.columns(6)
for idx, (container, name, port) in enumerate(SERVICES):
    running = check_docker_service(container)
    indicator_class = "up" if running else "down"
    badge_class = "badge-up" if running else "badge-down"
    badge_txt = "ONLINE" if running else "OFFLINE"
    with svc_cols[idx]:
        st.markdown(f"""
        <div class="svc-card">
            <div class="svc-header">
                <span class="svc-name">{name}</span>
                <span class="svc-indicator {indicator_class}"></span>
            </div>
            <div class="svc-port">:{port}</div>
            <span class="badge {badge_class}">{badge_txt}</span>
        </div>
        """, unsafe_allow_html=True)

# FastAPI card
api_up = check_port(8000)
indicator_class = "up" if api_up else "down"
badge_class = "badge-up" if api_up else "badge-down"
badge_txt = "ONLINE" if api_up else "OFFLINE"
with svc_cols[5]:
    st.markdown(f"""
    <div class="svc-card">
        <div class="svc-header">
            <span class="svc-name">FastAPI</span>
            <span class="svc-indicator {indicator_class}"></span>
        </div>
        <div class="svc-port">:8000</div>
        <span class="badge {badge_class}">{badge_txt}</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ─────────────────────────────────────────────────────────────────────────────
# CONTROL PANEL
# ─────────────────────────────────────────────────────────────────────────────
ctrl_col1, ctrl_col2 = st.columns(2)

with ctrl_col1:
    st.markdown(
        '<div class="section-title">Docker Infrastructure</div>',
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
        if st.button("▶  Start", key="btn_docker_start", use_container_width=True):
            with st.spinner("Starting containers..."):
                try:
                    subprocess.run("docker-compose up -d", shell=True, check=True)
                    log_event("DOCKER", "Containers started", "info")
                    st.rerun()
                except Exception as e:
                    log_event("DOCKER", f"Start failed: {e}", "error")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("■  Stop", key="btn_docker_stop", use_container_width=True):
            with st.spinner("Stopping containers..."):
                subprocess.run("docker-compose down", shell=True)
                log_event("DOCKER", "Containers stopped", "info")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="btn-accent">', unsafe_allow_html=True)
        if st.button("↺  Restart", key="btn_docker_restart", use_container_width=True):
            with st.spinner("Restarting..."):
                subprocess.run(
                    "docker-compose down && docker-compose up -d",
                    shell=True,
                )
                log_event("DOCKER", "Containers restarted", "info")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with ctrl_col2:
    st.markdown(
        '<div class="section-title">API Backend</div>',
        unsafe_allow_html=True,
    )
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
                    py, "-m", "uvicorn",
                    "src.model_service.infrastructure.entrypoints.api:app",
                    "--host", "0.0.0.0", "--port", "8000",
                ]
                subprocess.Popen(cmd)
                log_event("API", "FastAPI started on port 8000", "info")
                time.sleep(1)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

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
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# ─────────────────────────────────────────────────────────────────────────────
# TRAFFIC GENERATORS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-title">Traffic Generators</div>',
    unsafe_allow_html=True,
)

t_cols = st.columns(4)

with t_cols[0]:
    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("⚡  E2E Burst", key="btn_e2e", use_container_width=True):
        py = get_python()
        log_file = open("e2e_demo.log", "w", encoding="utf-8")
        subprocess.Popen(
            [py, "scripts/e2e_demo_mlflow.py"],
            stdout=log_file, stderr=subprocess.STDOUT,
        )
        log_event("GEN", "E2E burst triggered — 35 events", "info")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with t_cols[1]:
    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("💧  Start Stream", key="btn_stream_start", use_container_width=True):
        py = get_python()
        log_file = open("streaming.log", "w", encoding="utf-8")
        subprocess.Popen(
            [py, "scripts/simulate_multi_streaming.py"],
            stdout=log_file, stderr=subprocess.STDOUT,
        )
        log_event("GEN", "Streaming simulation started", "info")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with t_cols[2]:
    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    if st.button("■  Stop Streaming", key="btn_stream_stop", use_container_width=True):
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                cmdline = " ".join(proc.info.get("cmdline") or [])
                if "simulate_multi_streaming" in cmdline:
                    proc.kill()
            except Exception:
                pass
        log_event("GEN", "Streaming stopped", "info")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with t_cols[3]:
    st.markdown('<div class="btn-accent">', unsafe_allow_html=True)
    if st.button("📊  Trigger Retrain", key="btn_retrain", use_container_width=True):
        log_event("ML", "Manual retrain triggered", "info")
        py = get_python()
        subprocess.Popen([py, "scripts/e2e_demo_mlflow.py"])
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# ─────────────────────────────────────────────────────────────────────────────
# ACTIVITY LOG
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-row">'
    '<div class="section-title">Activity Log</div>'
    '<span class="log-caption">LAST 80 EVENTS</span>'
    '</div>',
    unsafe_allow_html=True,
)

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
        '</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("")

# ─────────────────────────────────────────────────────────────────────────────
# QUICK ACCESS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Quick Access</div>', unsafe_allow_html=True)

links = [
    ("📊", "Grafana",    "http://localhost:3000"),
    ("📈", "MLflow",     "http://localhost:5000"),
    ("🗄️", "MinIO",      "http://localhost:9001"),
    ("🌐", "FastAPI",    "http://localhost:8000/docs"),
    ("🔔", "Prometheus", "http://localhost:9090"),
]

link_cols = st.columns(len(links))
for idx, (icon, name, url) in enumerate(links):
    with link_cols[idx]:
        if st.button(
            f"{icon}  {name}",
            key=f"link_{name}",
            use_container_width=True,
        ):
            webbrowser.open(url)
        st.caption(f"→ {url}")

st.markdown("")
st.markdown("""
<div class="footer">
    MLOps Command Center // Multi-Tenant Fraud Detection // Stream Learning Platform
</div>
""", unsafe_allow_html=True)