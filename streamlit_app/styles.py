CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

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
    --shadow:        0 4px 16px rgba(0,0,0,0.06);
    --radius-card:   12px;
    --radius-btn:    8px;
    --radius-badge:  20px;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-page:       #0f172a;
        --bg-card:       #1e293b;
        --bg-subtle:     #334155;
        --border:        #334155;
        --text:          #f1f5f9;
        --text-muted:    #94a3b8;
        --shadow:        0 4px 16px rgba(0,0,0,0.3);
    }
}

.stApp { background: var(--bg-page) !important; }
.stMarkdown, .stText { font-family: 'Inter', sans-serif; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-subtle); border-radius: 4px; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    box-shadow: var(--shadow);
    padding: 20px 24px;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.card:hover {
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    transform: translateY(-1px);
}

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
    height: 16px;
    background: linear-gradient(180deg, var(--primary), var(--accent));
    border-radius: 2px;
    flex-shrink: 0;
}

.hero {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    box-shadow: var(--shadow-lg, var(--shadow));
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
    font-size: 22px;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 4px 0;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    color: #94a3b8;
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
    color: #e2e8f0;
    letter-spacing: 1px;
}
.hero-date {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    color: #64748b;
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
    margin-top: 6px;
}
.health-ok    { background: rgba(16,185,129,0.15); color: #34d399; }
.health-warn  { background: rgba(245,158,11,0.15); color: #fbbf24; }
.health-dot {
    width: 7px; height: 7px; border-radius: 50%;
}
.health-ok  .health-dot  { background: var(--success); }
.health-warn .health-dot { background: var(--warning); }

.refresh-btn {
    width: 36px; height: 36px;
    border-radius: 8px;
    border: 1px solid #475569;
    background: transparent;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s ease;
    flex-shrink: 0;
    color: #94a3b8;
}
.refresh-btn:hover {
    border-color: var(--primary);
    color: #fff;
    background: rgba(59,130,246,0.1);
}

.section-block {
    display: flex;
    align-items: center;
    padding: 8px 14px;
    background: var(--bg-subtle);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    margin-bottom: 12px;
}

.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-top: 3px solid var(--primary);
    border-radius: var(--radius-card);
    box-shadow: var(--shadow);
    padding: 16px 20px;
    text-align: center;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
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

.svc-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    box-shadow: var(--shadow);
    padding: 16px 18px;
    transition: box-shadow 0.2s ease;
}
.svc-card:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.08); }
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
    width: 8px; height: 8px; border-radius: 50%;
    flex-shrink: 0;
}
.svc-indicator.up   { background: var(--success); animation: pulse-online 2s infinite; }
.svc-indicator.down { background: var(--danger); }
@keyframes pulse-online {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
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
.badge-up   { background: rgba(16,185,129,0.1); color: #16a34a; }
.badge-down { background: rgba(239,68,68,0.1); color: #dc2626; }

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
div[data-testid="stHorizontalBlock"] .stButton > button { width: 100%; }

.btn-primary > button {
    background: linear-gradient(135deg, var(--primary), #2563eb) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(59,130,246,0.3) !important;
}
.btn-primary > button:hover {
    box-shadow: 0 4px 12px rgba(59,130,246,0.4) !important;
    transform: translateY(-1px) !important;
}

.btn-secondary > button {
    background: transparent !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border) !important;
}
.btn-secondary > button:hover {
    border-color: var(--primary) !important;
    color: var(--primary) !important;
    background: rgba(59,130,246,0.05) !important;
}

.btn-danger > button {
    background: transparent !important;
    color: var(--danger) !important;
    border: 1.5px solid rgba(239,68,68,0.2) !important;
}
.btn-danger > button:hover {
    background: rgba(239,68,68,0.05) !important;
    border-color: var(--danger) !important;
}

.btn-accent > button {
    background: transparent !important;
    color: var(--accent) !important;
    border: 1.5px solid rgba(6,182,212,0.2) !important;
}
.btn-accent > button:hover {
    background: rgba(6,182,212,0.05) !important;
    border-color: var(--accent) !important;
}

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
.log-tag-DOCKER { background: rgba(59,130,246,0.1); color: var(--primary); }
.log-tag-API    { background: rgba(6,182,212,0.1); color: var(--accent); }
.log-tag-GEN    { background: rgba(147,51,234,0.1); color: #9333ea; }
.log-tag-ML     { background: rgba(245,158,11,0.1); color: #b45309; }
.log-tag-SYS    { background: var(--bg-subtle); color: var(--text-muted); }
.log-msg {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    color: var(--text);
    flex: 1;
    padding-top: 1px;
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
    box-shadow: 0 4px 16px rgba(59,130,246,0.2);
    transform: translateY(-2px);
}
.link-icon { font-size: 24px; line-height: 1; }
.link-name {
    font-family: 'DM Sans', sans-serif;
    font-size: 12px;
    font-weight: 600;
    color: var(--text);
}

.footer {
    text-align: center;
    margin-top: 24px;
    padding: 14px;
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    color: var(--text-muted);
    letter-spacing: 0.5px;
}

.section-spacer { margin-bottom: 6px; }
.st-spinner { color: var(--primary) !important; }
div[data-testid="stDecoration"] { display: none; }
section[data-testid="stSidebar"] { display: none; }
"""
