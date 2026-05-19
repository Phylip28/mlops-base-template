# ruff: noqa: E501
CSS = """
<style>
@import url('https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@700,800,500,600&f[]=satoshi@400,500,700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-body:       #0a0e17;
    --bg-surface:    #111827;
    --bg-elevated:   #1a2332;
    --bg-sidebar:    #0d1117;
    --border:        #1e293b;
    --border-active: #2dd4bf;

    --text-primary:  #f1f5f9;
    --text-body:     #cbd5e1;
    --text-muted:    #64748b;

    --accent:        #2dd4bf;
    --accent-hover:  #14b8a6;
    --accent-glow:   rgba(45,212,191,0.12);

    --amber:         #f59e0b;
    --green:         #10b981;
    --red:           #ef4444;
    --purple:        #8b5cf6;
    --blue:          #3b82f6;

    --shadow-card:   0 4px 20px rgba(0,0,0,0.4);
    --shadow-glow:   0 0 20px rgba(45,212,191,0.08);
    --radius-card:   10px;
    --radius-btn:    8px;
    --radius-pill:   20px;
}

* { box-sizing: border-box; }

.stApp {
    background: var(--bg-body) !important;
}

/* ── Hide Streamlit chrome ── */
div[data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
#MainMenu { display: none !important; }
.stAppToolbar { display: none !important; }
div[data-testid="stStatusWidget"] { display: none !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 260px !important;
    max-width: 260px !important;
    padding-top: 0 !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}
section[data-testid="stSidebar"] > div:first-child > div:first-child {
    padding: 0 !important;
}
section[data-testid="stSidebar"] .st-emotion-cache-16idsys p {
    font-family: 'Satoshi', sans-serif !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    padding: 20px 20px 8px !important;
}
section[data-testid="stSidebar"] .st-emotion-cache-1aezh43 {
    padding: 0 8px !important;
    gap: 2px !important;
}
section[data-testid="stSidebar"] label {
    font-family: 'Satoshi', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--text-body) !important;
    padding: 10px 14px !important;
    border-radius: 8px !important;
    transition: all 0.15s ease !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
}
section[data-testid="stSidebar"] label:hover {
    background: var(--bg-surface) !important;
    color: var(--text-primary) !important;
}
section[data-testid="stSidebar"] label[data-baseweb="radio"] {
    padding-left: 14px !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: transparent !important;
}
section[data-testid="stSidebar"] input:checked + div + label {
    background: var(--accent-glow) !important;
    color: var(--accent) !important;
    box-shadow: inset 3px 0 0 var(--accent) !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] .st-emotion-cache-1vixtbp {
    font-family: 'Cabinet Grotesk', sans-serif !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    padding: 20px 20px 8px !important;
}
section[data-testid="stSidebar"] hr {
    border-color: var(--border) !important;
    margin: 0 20px !important;
}
section[data-testid="stSidebar"] .st-emotion-cache-1rtdyuf {
    display: flex !important;
    flex-direction: column !important;
}
section[data-testid="stSidebar"] div[data-testid="stImage"] {
    display: none !important;
}

/* ── Custom Sidebar ── */
.sidebar {
    padding: 0;
}
.sidebar-brand {
    padding: 24px 20px 20px;
    border-bottom: 1px solid var(--border);
    background: linear-gradient(180deg, rgba(45,212,191,0.06) 0%, transparent 100%);
}
.sidebar-brand-title {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 17px;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.3px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.sidebar-brand-title .brand-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), #0891b2);
    display: inline-block;
    box-shadow: 0 0 12px rgba(45,212,191,0.4);
}
.sidebar-brand-sub {
    font-family: 'Satoshi', sans-serif;
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 4px;
    padding-left: 20px;
}

/* ── Content Area ── */
.block-container {
    max-width: 1200px !important;
    padding: 28px 32px !important;
}

/* ── Page Header ── */
.page-header {
    margin-bottom: 24px;
}
.page-title {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 4px 0;
    letter-spacing: -0.5px;
}
.page-subtitle {
    font-family: 'Satoshi', sans-serif;
    font-size: 13px;
    color: var(--text-muted);
    margin: 0;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, rgba(45,212,191,0.08) 0%, rgba(15,23,42,0.8) 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 28px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24px;
    gap: 16px;
    box-shadow: var(--shadow-card);
}
.hero-left { flex: 1; }
.hero-title {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: #fff;
    margin: 0 0 4px 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-family: 'Satoshi', sans-serif;
    font-size: 13px;
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
    font-size: 20px;
    font-weight: 500;
    color: var(--text-primary);
    letter-spacing: 1px;
}
.hero-date {
    font-family: 'Satoshi', sans-serif;
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 2px;
}
.health-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 14px;
    border-radius: var(--radius-pill);
    font-family: 'Satoshi', sans-serif;
    font-size: 11px;
    font-weight: 600;
    margin-top: 6px;
}
.health-ok    { background: rgba(16,185,129,0.12); color: #34d399; border: 1px solid rgba(16,185,129,0.2); }
.health-warn  { background: rgba(245,158,11,0.12); color: #fbbf24; border: 1px solid rgba(245,158,11,0.2); }
.health-dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; }
.health-ok  .health-dot  { background: var(--green); box-shadow: 0 0 8px rgba(16,185,129,0.5); }
.health-warn .health-dot { background: var(--amber); box-shadow: 0 0 8px rgba(245,158,11,0.5); }

.refresh-btn {
    width: 36px; height: 36px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--bg-surface);
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s ease;
    flex-shrink: 0;
    color: var(--text-muted);
}
.refresh-btn:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--accent-glow);
}

/* ── Cards ── */
.card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 20px 24px;
    transition: all 0.2s ease;
    position: relative;
}
.card:hover {
    box-shadow: var(--shadow-card), var(--shadow-glow);
}
.card-title {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.card-title::before {
    content: '';
    width: 3px; height: 16px;
    background: var(--accent);
    border-radius: 2px;
    flex-shrink: 0;
}
.card-striped {
    border-top: 2px solid var(--accent);
}
.card-striped.green  { border-top-color: var(--green); }
.card-striped.red    { border-top-color: var(--red); }
.card-striped.amber  { border-top-color: var(--amber); }
.card-striped.blue   { border-top-color: var(--blue); }
.card-striped.purple { border-top-color: var(--purple); }

/* ── Metric Tiles ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}
.metric-tile {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 18px 16px;
    text-align: center;
    transition: all 0.2s ease;
    border-top: 2px solid var(--accent);
}
.metric-tile:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-card), var(--shadow-glow);
}
.metric-tile.accent  { border-top-color: var(--accent); }
.metric-tile.green   { border-top-color: var(--green); }
.metric-tile.amber   { border-top-color: var(--amber); }
.metric-tile.red     { border-top-color: var(--red); }
.metric-tile.purple  { border-top-color: var(--purple); }

.metric-value {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
    margin-bottom: 6px;
}
.metric-tile.green  .metric-value { color: var(--green); }
.metric-tile.amber  .metric-value { color: var(--amber); }
.metric-tile.red    .metric-value { color: var(--red); }
.metric-tile.purple .metric-value { color: var(--purple); }

.metric-label {
    font-family: 'Satoshi', sans-serif;
    font-size: 10px;
    font-weight: 500;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Service Cards ── */
.svc-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}
.svc-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 18px 20px;
    transition: all 0.2s ease;
}
.svc-card:hover {
    box-shadow: var(--shadow-card);
    border-color: var(--border-active);
}
.svc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}
.svc-name {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
}
.svc-indicator {
    width: 8px; height: 8px; border-radius: 50%;
    flex-shrink: 0;
}
.svc-indicator.up {
    background: var(--green);
    box-shadow: 0 0 8px rgba(16,185,129,0.6);
    animation: pulse-dot 2s infinite;
}
.svc-indicator.down { background: var(--red); }
@keyframes pulse-dot {
    0%, 100% { opacity: 1; box-shadow: 0 0 8px rgba(16,185,129,0.6); }
    50% { opacity: 0.5; box-shadow: 0 0 4px rgba(16,185,129,0.2); }
}
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
    border-radius: var(--radius-pill);
    font-family: 'Satoshi', sans-serif;
    font-size: 10px;
    font-weight: 600;
}
.badge-up   { background: rgba(16,185,129,0.1); color: var(--green); border: 1px solid rgba(16,185,129,0.2); }
.badge-down { background: rgba(239,68,68,0.1); color: var(--red); border: 1px solid rgba(239,68,68,0.2); }

/* ── Buttons ── */
.btn-row { display: flex; gap: 12px; margin: 16px 0; }
.stButton > button {
    font-family: 'Satoshi', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    border-radius: var(--radius-btn) !important;
    padding: 10px 18px !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
    height: 40px !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent), #0d9488) !important;
    color: #0a0e17 !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(45,212,191,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 4px 16px rgba(45,212,191,0.4) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: var(--text-body) !important;
    border: 1.5px solid var(--border) !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: var(--accent-glow) !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button { width: 100% !important; }

/* ── Log Panel ── */
.log-panel {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 16px 18px;
    height: 280px;
    overflow-y: auto;
}
.log-panel::-webkit-scrollbar { width: 4px; }
.log-panel::-webkit-scrollbar-track { background: transparent; }
.log-panel::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

.log-entry {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 6px 0;
    border-bottom: 1px solid rgba(30,41,59,0.5);
}
.log-entry:last-child { border-bottom: none; }
.log-ts {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--text-muted);
    min-width: 60px;
    padding-top: 1px;
}
.log-tag {
    font-family: 'Satoshi', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
    padding: 2px 8px;
    border-radius: 4px;
    min-width: 52px;
    text-align: center;
    flex-shrink: 0;
}
.log-tag-DOCKER { background: rgba(45,212,191,0.1); color: var(--accent); }
.log-tag-API    { background: rgba(59,130,246,0.1); color: var(--blue); }
.log-tag-GEN    { background: rgba(139,92,246,0.1); color: var(--purple); }
.log-tag-ML     { background: rgba(245,158,11,0.1); color: var(--amber); }
.log-tag-SYS    { background: rgba(100,116,139,0.1); color: var(--text-muted); }
.log-msg {
    font-family: 'Satoshi', sans-serif;
    font-size: 12px;
    color: var(--text-body);
    flex: 1;
    padding-top: 1px;
}

/* ── Link Cards ── */
.link-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 12px;
}
.link-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 18px 12px;
    text-align: center;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
}
.link-card:hover {
    border-color: var(--accent);
    box-shadow: var(--shadow-glow);
    transform: translateY(-2px);
}
.link-icon { font-size: 24px; line-height: 1; }
.link-name {
    font-family: 'Satoshi', sans-serif;
    font-size: 12px;
    font-weight: 500;
    color: var(--text-body);
}

/* ── Footer ── */
.footer {
    text-align: center;
    margin-top: 40px;
    padding: 16px;
    font-family: 'Satoshi', sans-serif;
    font-size: 11px;
    color: var(--text-muted);
    letter-spacing: 0.5px;
    border-top: 1px solid var(--border);
}

/* ── Section header ── */
.section-title {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::before {
    content: '';
    width: 3px; height: 16px;
    background: linear-gradient(180deg, var(--accent), #0891b2);
    border-radius: 2px;
    flex-shrink: 0;
}

/* ── Responsive ── */
@media (max-width: 1024px) {
    .svc-grid { grid-template-columns: repeat(2, 1fr); }
    .link-grid { grid-template-columns: repeat(3, 1fr); }
    .metric-row { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 768px) {
    .svc-grid { grid-template-columns: 1fr; }
    .metric-row { grid-template-columns: repeat(2, 1fr); }
    .link-grid { grid-template-columns: repeat(2, 1fr); }
    .hero-banner { flex-direction: column; text-align: center; }
    .hero-right { justify-content: center; }
}
</style>
"""
