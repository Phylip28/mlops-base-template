# ruff: noqa: E501
CSS = """
<style>
/* ── Flash prevention — runs before anything else ── */
html, body, .stApp, div[data-testid="stMain"], section.main, section.main > div, .main > div, .element-container {
    background-color: #0f141a !important;
}
.stApp > * {
    animation: none !important;
}

@import url('https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@700,800,500,600&f[]=satoshi@400,500,700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

/* ── AWS Dark Mode Palette ── */
:root {
    --bg-body:       #0f141a;
    --bg-surface:    #1e242b;
    --bg-elevated:   #232a32;
    --bg-sidebar:    #16191f;
    --bg-input:      #0f141a;
    --border:        #2a2f36;
    --border-active: #00a1c9;
    --border-hover:  #3e4652;

    --text-primary:  #d5dbdb;
    --text-body:     #95a5a6;
    --text-muted:    #5f6b7a;
    --text-inverse:  #0f141a;

    --accent:        #00a1c9;
    --accent-hover:  #44b9d6;
    --accent-glow:   rgba(0,161,201,0.15);

    --aws-orange:    #ff9900;
    --aws-green:     #1d8102;
    --aws-red:       #d13212;
    --aws-blue:      #44b9d6;
    --aws-purple:    #8b5cf6;
    --aws-yellow:    #ffe600;

    --shadow-card:   0 1px 8px rgba(0,0,0,0.5);
    --shadow-glow:   0 0 16px rgba(0,161,201,0.12);
    --radius-card:   8px;
    --radius-btn:    4px;
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
/* Force sidebar always expanded (fixes Firefox collapsed-on-load) */
section[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border) !important;
    width: 260px !important;
    min-width: 260px !important;
    max-width: 260px !important;
    padding-top: 0 !important;
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    transform: none !important;
    margin-left: 0 !important;
    left: 0 !important;
    position: relative !important;
    overflow: visible !important;
    flex-shrink: 0 !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
    width: 100% !important;
}

/* Collapse header to zero height but KEEP in DOM (Firefox-safe) */
div[data-testid="stSidebarHeader"] {
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    overflow: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
    opacity: 0 !important;
    pointer-events: none !important;
    border: none !important;
}

/* Also nuke the collapse button itself */
div[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

/* section labels: Monitor / Control / Access */
.sidebar-section-label {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 20px 16px 6px;
}

/* ── Sidebar Navigation ── */
.sidebar-nav {
    display: flex;
    flex-direction: column;
    padding: 0 8px;
}

.sidebar-nav-link {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 10px;
    border-radius: 6px;
    text-decoration: none !important;
    color: var(--text-body);
    font-family: 'Satoshi', sans-serif;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.12s ease;
    border-left: 2px solid transparent;
    margin-bottom: 1px;
}
.sidebar-nav-link:hover {
    background: var(--bg-surface);
    color: var(--text-primary);
    border-left-color: var(--border-hover);
}

.sidebar-nav-link--active {
    background: rgba(0,161,201,0.08);
    color: var(--text-primary);
    border-left-color: var(--accent);
    font-weight: 700;
}
.sidebar-nav-link--active:hover {
    border-left-color: var(--accent);
    background: rgba(0,161,201,0.12);
}

.sidebar-nav-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    color: var(--text-muted);
    transition: color 0.12s ease;
}
.sidebar-nav-link:hover .sidebar-nav-icon,
.sidebar-nav-link--active .sidebar-nav-icon {
    color: var(--accent);
}

.sidebar-nav-label {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Keep generic sidebar button styles for non-nav buttons */
section[data-testid="stSidebar"] .stButton > button {
    font-family: 'Satoshi', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    color: var(--text-body) !important;
    background: transparent !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-btn) !important;
    padding: 8px 14px !important;
    transition: all 0.15s ease !important;
    box-shadow: none !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--bg-surface) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-hover) !important;
}

/* ── Custom Sidebar ── */
.sidebar-brand {
    padding: 22px 20px 18px;
    border-bottom: 1px solid var(--border);
}
.sidebar-brand-title {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.3px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.sidebar-brand-title .brand-dot {
    width: 10px; height: 10px;
    border-radius: 3px;
    background: var(--accent);
    display: inline-block;
    box-shadow: 0 0 10px rgba(0,161,201,0.45);
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
    background: linear-gradient(135deg, rgba(0,161,201,0.08) 0%, rgba(15,23,42,0.8) 100%);
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
    font-weight: 700;
    margin-top: 6px;
}
.health-ok    { background: rgba(16,185,129,0.12); color: #34d399; border: 1px solid rgba(29,129,2,0.2); }
.health-warn  { background: rgba(245,158,11,0.12); color: #fbbf24; border: 1px solid rgba(245,158,11,0.2); }
.health-dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; }
.health-ok  .health-dot  { background: var(--aws-green); box-shadow: 0 0 8px rgba(29,129,2,0.5); }
.health-warn .health-dot { background: var(--aws-orange); box-shadow: 0 0 8px rgba(255,153,0,0.5); }

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
    font-weight: 700;
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
.card-striped.green  { border-top-color: var(--aws-green); }
.card-striped.red    { border-top-color: var(--aws-red); }
.card-striped.amber  { border-top-color: var(--aws-orange); }
.card-striped.blue   { border-top-color: var(--aws-blue); }
.card-striped.purple { border-top-color: var(--aws-purple); }

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
.metric-tile.green   { border-top-color: var(--aws-green); }
.metric-tile.amber   { border-top-color: var(--aws-orange); }
.metric-tile.red     { border-top-color: var(--aws-red); }
.metric-tile.purple  { border-top-color: var(--aws-purple); }

.metric-value {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--accent);
    line-height: 1;
    margin-bottom: 6px;
}
.metric-tile.green  .metric-value { color: var(--aws-green); }
.metric-tile.amber  .metric-value { color: var(--aws-orange); }
.metric-tile.red    .metric-value { color: var(--aws-red); }
.metric-tile.purple .metric-value { color: var(--aws-purple); }

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
    row-gap: 24px;
}
.svc-card {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 18px 16px;
    transition: all 0.2s ease;
    text-align: center;
    min-height: 180px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.svc-card:hover {
    box-shadow: var(--shadow-card);
    border-color: var(--border-active);
    transform: translateY(-2px);
}
.svc-name {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 12px;
    letter-spacing: -0.2px;
}
.svc-icon {
    width: 52px;
    height: 52px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 14px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    transition: transform 0.2s ease;
    flex-shrink: 0;
}
.svc-card:hover .svc-icon {
    transform: scale(1.10);
}
.svc-logo-img {
    width: 34px;
    height: 34px;
    object-fit: contain;
}
.svc-fallback {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: var(--accent);
    line-height: 1;
}
.svc-info {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    margin-top: auto;
    padding-top: 4px;
}
.svc-port {
    font-family: 'Satoshi', sans-serif;
    font-size: 11px;
    color: var(--text-primary);
    font-weight: 500;
}
.svc-status-up {
    font-family: 'Satoshi', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: var(--aws-green);
}
.svc-status-down {
    font-family: 'Satoshi', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: var(--aws-red);
}
.svc-status-online {
    font-family: 'Satoshi', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: var(--aws-green);
}
.svc-status-offline {
    font-family: 'Satoshi', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: var(--aws-red);
}

/* ── Buttons ── */
.btn-row { display: flex; gap: 12px; margin: 16px 0; }
.stButton > button {
    font-family: 'Satoshi', sans-serif !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    border-radius: var(--radius-btn) !important;
    padding: 10px 18px !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
    height: 40px !important;
}
.stButton > button[kind="primary"] {
    background: var(--accent) !important;
    color: #fff !important;
    border: 1px solid var(--accent) !important;
    box-shadow: none !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--accent-hover) !important;
    border-color: var(--accent-hover) !important;
    box-shadow: 0 2px 8px rgba(0,161,201,0.3) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: var(--text-body) !important;
    border: 1px solid var(--border-hover) !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--text-primary) !important;
    background: var(--bg-surface) !important;
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
.log-tag-DOCKER { background: rgba(0,161,201,0.1); color: var(--accent); }
.log-tag-API    { background: rgba(68,185,214,0.1); color: var(--aws-blue); }
.log-tag-GEN    { background: rgba(139,92,246,0.1); color: var(--aws-purple); }
.log-tag-ML     { background: rgba(255,153,0,0.1); color: var(--aws-orange); }
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
.link-card-wrapper {
    text-decoration: none !important;
}
.link-card-wrapper:hover .link-card {
    border-color: var(--accent);
    box-shadow: var(--shadow-glow);
    transform: translateY(-2px);
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
.link-icon-badge {
    width: 56px; height: 56px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 6px;
    transition: transform 0.15s ease;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
}
.link-card:hover .link-icon-badge { transform: scale(1.08); }
.link-logo-img {
    width: 32px;
    height: 32px;
    object-fit: contain;
}
.link-initial {
    font-family: 'Cabinet Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #fff;
    line-height: 1;
}
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
    font-weight: 700;
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
