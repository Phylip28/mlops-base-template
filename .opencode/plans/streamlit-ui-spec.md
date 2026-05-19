# UI-SPEC: MLOps Streamlit Command Center

**Phase:** Streamlit Dashboard Redesign
**Date:** 2026-05-18
**Status:** Draft

---

## 1. Visual Identity & Aesthetic Direction

### Tone
Dark, professional operations dashboard. Inspired by Grafana/Datadog but with a sharper, more modern edge. Think "mission control for ML" — authoritative, data-dense, but clean.

### Design Keywords
Dark, precise, data-rich, teal-amber accent, glassmorphic cards, subtle glow

### Differentiation
The sidebar uses a **gradient glass panel** with a subtle grid pattern overlay. Active nav items glow with a teal neon underline + left border. Cards have **subtle colored top borders** that pulse for active services — like a server rack's status LEDs.

---

## 2. Layout & Navigation

### Structure
```
┌──────────────┬─────────────────────────────────────────────┐
│   SIDEBAR     │              CONTENT AREA                    │
│  (260px)     │                                               │
│              │  ┌─────────────────────────────────────────┐  │
│  🛰️ MLOps    │  │  Section Title / Breadcrumb            │  │
│  Command     │  ├─────────────────────────────────────────┤  │
│  Center      │  │                                         │  │
│              │  │  Section-specific content               │  │
│  ─────────── │  │  (cards, metrics, controls, tables)     │  │
│              │  │                                         │  │
│  ◆ Overview  │  │                                         │  │
│  ■ Services  │  │                                         │  │
│  ■ Docker    │  │                                         │  │
│  ■ API       │  │                                         │  │
│  ■ Traffic   │  │                                         │  │
│  ■ Activity  │  └─────────────────────────────────────────┘  │
│  ■ Links     │                                               │
│              │                                               │
└──────────────┴─────────────────────────────────────────────┘
```

### Navigation
- **Sidebar**: Fixed left panel, 260px wide, full height
- **Items**: Icon + Label, with active state (teal glow left border)
- **Streamlit**: Use `st.navigation` with `st.Page` objects (multi-page app pattern)
- **Mobile**: Sidebar collapses to icon-only or bottom nav

### Pages / Sections

| # | Nav Item | Route | Content |
|---|----------|-------|---------|
| 1 | Overview | `overview` | Hero header + 5 metric tiles + quick health summary |
| 2 | Services | `services` | Service cards (Postgres, MinIO, MLflow, Prometheus, Grafana, FastAPI) with live status indicators |
| 3 | Docker | `docker` | Start/Stop/Restart controls + container status |
| 4 | API | `api` | Start/Stop API controls + port status |
| 5 | Traffic | `traffic` | E2E Burst, Start/Stop Stream, Trigger Retrain buttons |
| 6 | Activity | `activity` | Scrollable activity log with tag-colored entries |
| 7 | Links | `links` | Quick access cards to Grafana, MLflow, MinIO, FastAPI, Prometheus, Prediction UI |

---

## 3. Typography

| Role | Font | Weight | Size | Usage |
|------|------|--------|------|-------|
| Display | **Cabinet Grotesk** | 700-800 | 22px | Page titles, hero |
| Headings | **Cabinet Grotesk** | 600 | 13px | Section headers, card titles |
| Body | **Satoshi** | 400-500 | 12-13px | Labels, descriptions, log messages |
| Mono | **JetBrains Mono** | 400-500 | 10-11px | Port numbers, timestamps, code values |
| Nav | **Cabinet Grotesk** | 500 | 13px | Sidebar navigation items |

**Why these fonts?**
Cabinet Grotesk gives a distinctive, slightly compressed geometric look that feels technical and authoritative without being sterile. Satoshi pairs as a refined, warm body font. This avoids the generic Inter/DM Sans combo seen in most dashboards.

**Loading:** Google Fonts via `@import` or self-hosted woff2.

---

## 4. Color Palette

### Theme: Dark (default — no light mode for v1)

```
--bg-body:       #0a0e17     (deepest navy-black)
--bg-surface:    #111827     (card backgrounds)
--bg-elevated:   #1a2332     (hovered cards, elevated surfaces)
--bg-sidebar:    #0d1117     (sidebar, slightly lighter than body)
--border:        #1e293b     (subtle borders)
--border-active: #2dd4bf     (teal — active/focus borders)

--text-primary:  #f1f5f9     (headings, primary text)
--text-body:     #cbd5e1     (body text)
--text-muted:    #64748b     (labels, secondary info)

--accent:        #2dd4bf     (teal — primary action, active states)
--accent-hover:  #14b8a6     (teal dark — hover states)
--accent-glow:   rgba(45,212,191,0.15)  (teal glow — card glows)

--amber:         #f59e0b     (warnings, anomalies)
--green:         #10b981     (success, online)
--red:           #ef4444     (errors, offline)
--purple:        #8b5cf6     (ML/training status)
--blue:          #3b82f6     (info, general)

--gradient-sidebar: linear-gradient(180deg, #0d1117 0%, #111827 100%)
--gradient-glass: linear-gradient(135deg, rgba(45,212,191,0.08) 0%, transparent 50%)
--shadow-card:   0 4px 20px rgba(0,0,0,0.3)
--shadow-glow:   0 0 20px rgba(45,212,191,0.1)
```

### Usage Rules
- Cards use `--bg-surface` with `--border` and subtle `--shadow-card`
- Active sidebar item: `--accent` left border + `--accent-glow` background
- Service status dot: `--green` (online), `--red` (offline), with pulse animation
- Metric values use `--accent` color by default
- Toast/alerts use semantic colors with subtle background tints (e.g., `rgba(16,185,129,0.1)` for success)

---

## 5. Components & States

### Sidebar Nav Item
```
┌─────────────────────────────┐
│ ◆  Overview                 │  ← inactive
├─────────────────────────────┤
│ │  ■  Services              │  ← active (teal left border + glow bg)
└─────────────────────────────┘
```
- Height: 44px
- Padding: 12px 16px
- Border-radius: 0 (full-width line)
- Active: 2px solid `--accent` left border, `--accent-glow` background
- Hover: `--bg-surface` background
- Icon: Unicode or emoji (◆ ■ ▲ ●)

### Service Card
```
┌─────────────────────┐
│ PostgreSQL    ●      │  ← name + status dot
│ :5432               │
│ [ONLINE]            │  ← badge
└─────────────────────┘
```
- Border-top: 2px colored stripe (teal=online, red=offline)
- Status dot: 8px circle, pulsing when online
- Badge: rounded pill, green for online, red for offline
- Hover: slight translateY(-1px) + elevated shadow

### Metric Card
```
┌──────┐
│  5   │  ← large number (accent color)
│ SRV  │  ← small label (muted)
└──────┘
```
- Centered layout
- Value: Cabinet Grotesk 700, 28px
- Label: uppercase, 10px, letter-spaced
- Border-top colored stripe (per metric type)

### Buttons
- Primary: `--accent` background, white text, subtle glow shadow
- Secondary: transparent, `--border` outline
- Danger: `--red` outline
- Hover: translateY(-1px), increased shadow
- Disabled: 0.5 opacity, no hover effects

### Activity Log
- Scrollable container (max-height: 300px)
- Each entry: timestamp (mono, muted) + colored tag + message
- Tags are color-coded: DOCKER=teal, API=blue, GEN=purple, ML=amber, SYS=gray

---

## 6. Micro-interactions & Motion

| Element | Animation | Duration | Timing |
|---------|-----------|----------|--------|
| Service indicator (online) | Pulse opacity 1→0.5→1 | 2s | Infinite |
| Card hover | translateY(-1px) + shadow increase | 0.2s | Ease |
| Page transition | Fade in + slight translateY(8px→0) | 0.3s | Ease-out |
| Sidebar active indicator | Width expand from 0→2px | 0.15s | Ease-out |
| Button hover | translateY(-1px) + shadow | 0.15s | Ease |
| Log entry new item | Fade slide in | 0.2s | Ease |

---

## 7. Spacing & Sizing

| Token | Value | Usage |
|-------|-------|-------|
| --space-xs | 4px | Internal gaps, dot spacing |
| --space-sm | 8px | Between label and value |
| --space-md | 16px | Between form elements |
| --space-lg | 24px | Between sections, card padding |
| --space-xl | 32px | Page padding, hero padding |
| --sidebar-w | 260px | Sidebar width |
| --card-radius | 10px | Card border-radius |
| --btn-radius | 8px | Button border-radius |

---

## 8. Technical Implementation

### Approach
- **Streamlit multi-page app** using `st.navigation()` + `st.Page()`
- Each section becomes a separate page file under `streamlit_app/pages/`
- Sidebar built with `st.sidebar` and custom HTML/CSS
- Shared CSS in `streamlit_app/styles.py`
- Shared utils in `streamlit_app/utils.py`

### File Structure
```
streamlit_app/
├── __init__.py
├── run.py              ← entry point (replaces run_streamlit_app.py)
├── styles.py           ← CSS design system
├── utils.py            ← helpers (log_event, check_port, etc.)
├── components/         ← reusable components
│   └── cards.py        ← card rendering helpers
└── pages/
    ├── __init__.py
    ├── overview.py     ← hero + metrics
    ├── services.py     ← service status
    ├── docker.py       ← docker controls
    ├── api.py          ← API controls
    ├── traffic.py      ← traffic generators
    ├── activity.py     ← activity log
    └── links.py        ← quick access links
```

### Streamlit Multi-page Setup
```python
# run.py
import streamlit as st
from streamlit_app.styles import CSS

st.set_page_config(page_title="MLOps Command Center", layout="wide")

pg = st.navigation({
    "Monitor": [
        st.Page("streamlit_app/pages/overview.py", title="Overview", icon="📊"),
        st.Page("streamlit_app/pages/services.py", title="Services", icon="⚙️"),
        st.Page("streamlit_app/pages/activity.py", title="Activity", icon="📋"),
    ],
    "Control": [
        st.Page("streamlit_app/pages/docker.py", title="Docker", icon="🐳"),
        st.Page("streamlit_app/pages/api.py", title="API", icon="🌐"),
        st.Page("streamlit_app/pages/traffic.py", title="Traffic", icon="📡"),
    ],
    "Access": [
        st.Page("streamlit_app/pages/links.py", title="Links", icon="🔗"),
    ],
})

st.markdown(CSS, unsafe_allow_html=True)
pg.run()
```

### Design System Inheritance
- New design tokens in CSS (dark palette, teal accent)
- Cabinet Grotesk + Satoshi via Google Fonts
- Same component patterns but restyled for dark theme
- Sidebar replaces all `st.sidebar` defaults with custom HTML

---

## 9. Edge Cases & States

| State | Handling |
|-------|----------|
| API offline | Service card shows red dot + "OFFLINE" badge. Docker/API controls show warning if API isn't running |
| Docker not installed | `get_docker_compose_cmd()` raises → buttons show error toast, not crash |
| Empty activity log | Shows "Awaiting events..." placeholder with SYS tag |
| All services offline | Hero health badge shows "DEGRADED MODE" in amber |
| Rapid button clicks | Streamlit's rerun handles this — but buttons disable during loading via `st.spinner` |
| Long service names | Cards use CSS `word-break` to handle overflow |
| Mobile/small screens | Sidebar collapses to top nav bar with dropdown or icon-only |

---

## 10. Accessibility

- All interactive elements keyboard-accessible (Streamlit handles this)
- Color contrast ratios ≥ 4.5:1 for body text
- Status not conveyed by color alone (text label + icon + dot)
- Focus states visible (default browser focus + custom glow)
- Font sizes in rem/px (not vw) — no zoom breakage
