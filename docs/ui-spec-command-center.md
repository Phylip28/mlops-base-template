# MLOps Command Center — UI Specification v2

## 1. Concept & Vision

A clean, professional SaaS control panel for managing a multi-tenant fraud detection platform. Designed for **non-technical operators** who need to monitor infrastructure health, trigger ML workflows, and access observability tools without deep system knowledge. The aesthetic is approachable and calm — a tool that inspires confidence, not anxiety. Think: "mission control made friendly."

---

## 2. Design Language

### Aesthetic Direction
**Clean SaaS / White-label** — Light, spacious, and readable. Professional without being cold. Inspired by tools like Vercel dashboard, Linear, and Datadog's clean mode.

### Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `bg-page` | `#f8fafc` | Page background (cool gray) |
| `bg-card` | `#ffffff` | Card surfaces |
| `bg-subtle` | `#f1f5f9` | Metric tile tints, section backgrounds |
| `primary` | `#3b82f6` | Primary actions (blue) |
| `primary-hover` | `#2563eb` | Hover state |
| `accent` | `#06b6d4` | Secondary accents (teal) |
| `success` | `#10b981` | Online, running, healthy (green) |
| `danger` | `#ef4444` | Offline, error, stopped (red) |
| `warning` | `#f59e0b` | Degraded, pending (amber) |
| `text` | `#1e293b` | Primary text (dark slate) |
| `text-muted` | `#64748b` | Secondary text, captions |
| `border` | `#e2e8f0` | Dividers, card borders |
| `shadow` | `0 2px 12px #0a0a0a10` | Card elevation |

### Typography

| Role | Font | Size | Weight | Notes |
|------|------|------|--------|-------|
| Page title | **DM Sans** | 24px | 700 | Bold, clean sans-serif |
| Section header | **DM Sans** | 12px | 700 | Uppercase, letter-spacing 1.5px |
| Card title | **DM Sans** | 16px | 600 | Service names, section titles |
| Body / labels | **Inter** | 13px | 400 | Paragraphs, descriptions |
| Metric number | **DM Sans** | 32px | 700 | Large stat values |
| Metric label | **Inter** | 11px | 500 | Small uppercase label |
| Monospace / logs | **JetBrains Mono** | 12px | 400 | Timestamps, log entries |
| Caption / meta | **Inter** | 11px | 400 | Port numbers, hints |

### Spacing System

- **Base unit**: 4px
- **Card padding**: 20px 24px
- **Section gap**: 32px
- **Grid gap**: 16px
- **Button padding**: 10px 20px
- **Border radius**: 12px (cards), 8px (buttons), 6px (inputs/badges)

### Motion Philosophy

- **Purposeful, not decorative** — animation communicates state change, not aesthetics
- **Entrance**: fade-in on page load (200ms ease-out, staggered 50ms per section)
- **Hover**: scale(1.02) on cards, background shift on buttons (150ms ease)
- **Status transitions**: smooth color transitions (300ms) when services go online/offline
- **No spinning or pulsing** — status is conveyed through color and shape, not motion
- **Loading**: spinner uses primary blue, centered, respects motion guidelines

---

## 3. Layout & Structure

### Page Architecture (top → bottom)

```
┌─────────────────────────────────────────────────────────────┐
│  HERO HEADER                                                 │
│  [Title + subtitle + live clock]        [Date + Health]     │
├─────────────────────────────────────────────────────────────┤
│  METRIC TILES (5 cards, equal width)                        │
│  [Services] [Containers] [Log Events] [Retrain] [API Port]  │
├─────────────────────────────────────────────────────────────┤
│  SERVICE STATUS GRID (6 cards)                              │
│  [Postgres] [MinIO] [MLflow] [Prometheus] [Grafana] [API]  │
├─────────────────────────────────────────────────────────────┤
│  CONTROL PANEL (2 columns)                                  │
│  [Docker START/STOP/RESTART]    [API START/STOP]           │
├─────────────────────────────────────────────────────────────┤
│  TRAFFIC GENERATORS (4 cards, equal)                       │
│  [E2E BURST] [STREAM START] [STREAM STOP] [TRIGGER RETRAIN]│
├─────────────────────────────────────────────────────────────┤
│  ACTIVITY LOG (full width, scrolling panel)                 │
│  [timestamp] [tag] [message] ← colored rows                │
├─────────────────────────────────────────────────────────────┤
│  QUICK ACCESS (5 cards, equal)                              │
│  [Grafana] [MLflow] [MinIO] [FastAPI] [Prometheus]         │
└─────────────────────────────────────────────────────────────┘
```

### Responsive Strategy
- Desktop-first (control panel used on large screens)
- On narrow viewports: grid collapses to 2 columns, metric tiles wrap
- Sidebar hidden
- Wide layout (`layout="wide"`) inherited from Streamlit config

---

## 4. Features & Interactions

### 4.1 Hero Header

| Element | Description |
|---------|-------------|
| **Title** | "🛰 MLOps Command Center" — DM Sans 24px bold, primary blue |
| **Subtitle** | "MULTI-TENANT FRAUD DETECTION // STREAM LEARNING PLATFORM" — muted text |
| **Clock** | Live time `HH:MM:SS` — monospace, right-aligned |
| **Date** | `YYYY-MM-DD` below clock — muted |
| **Health badge** | Green dot + "ALL SYSTEMS NOMINAL" or Amber + "DEGRADED MODE" |

### 4.2 Metric Tiles

5 cards showing platform statistics:
1. **Services** — count of registered services
2. **Containers** — number of Docker containers
3. **Log Events** — count from activity log session state
4. **Retrain Threshold** — static "30" (configurable)
5. **API Port** — static "8000"

Each card: white bg, rounded corners, subtle shadow, large number in primary/accent color.

### 4.3 Service Status Grid

6 cards (PostgreSQL, MinIO, MLflow, Prometheus, Grafana, FastAPI):

| Element | Description |
|---------|-------------|
| **Status indicator** | 8px circle — green (`#10b981`) if running, red (`#ef4444`) if stopped |
| **Service name** | DM Sans 14px semibold — e.g., "PostgreSQL" |
| **Port label** | Muted caption, e.g., `:5432` |
| **Badge** | Rounded pill "ONLINE" (green bg) or "OFFLINE" (red bg) |

Check runs on every page rerun (button press or manual refresh).

### 4.4 Control Panel — Docker

3 buttons in a row:
- **▶ START** — primary blue, starts `docker-compose up -d`
- **■ STOP** — gray outline, runs `docker-compose down`
- **↺ RESTART** — teal outline, restart sequence

On click: spinner shows "Iniciando..." / "Apagando..." etc. After action completes, page reruns to update status grid.

### 4.5 Control Panel — API

2 buttons:
- **▶ START API** — primary blue, starts uvicorn on port 8000
- **■ STOP API** — gray outline, kills uvicorn processes on port 8000

Port conflict: if 8000 already in use, show warning banner and log event.

### 4.6 Traffic Generators

4 cards in a row:
| Button | Action |
|--------|--------|
| **⚡ E2E BURST** | Runs `scripts/e2e_demo_mlflow.py` — 35 events in burst, triggers retraining |
| **💧 START STREAMING** | Runs `scripts/simulate_multi_streaming.py` in background |
| **■ STOP STREAMING** | Kills streaming process |
| **📊 TRIGGER RETRAIN** | Sends 35 events + logs manual retrain event |

Each button logs an event to the activity log on press.

### 4.7 Activity Log

Scrollable panel showing last 80 events (newest at top):
- **Timestamp** — `HH:MM:SS` in monospace, muted
- **Tag** — 3-4 letter code: `DOCKER`, `API`, `GEN`, `ML`, `SYS` — colored chip
- **Message** — human-readable description

Color coding for tags:
| Tag | Color |
|-----|-------|
| `DOCKER` | Blue |
| `API` | Teal |
| `GEN` | Purple |
| `ML` | Amber |
| `SYS` | Gray |

Level colors: INFO (blue), OK (green), WARN (amber), ERROR (red).

### 4.8 Quick Access

5 cards in a row — each shows:
- **Icon** — emoji (📊 📈 🗄 🌐 🔔)
- **Service name** — "Grafana", "MLflow", etc. (no port shown)
- **Caption** — small muted text: `→ localhost:3000` (subtle, not prominent)

On click: opens URL in new browser tab via `webbrowser.open()`.

---

## 5. Component Inventory

### 5.1 Card
- **Default**: white bg, `#e2e8f0` border, 12px radius, soft shadow, 20px padding
- **Hover**: slight translateY(-1px), shadow increases slightly (CSS only, not Streamlit)
- **States**: normal, loading (spinner overlay)

### 5.2 Button
- **Primary**: filled `#3b82f6`, white text, 8px radius, full width
- **Primary hover**: darker `#2563eb`, slight shadow
- **Secondary/ghost**: transparent bg, `#e2e8f0` border, muted text
- **Secondary hover**: border darkens to primary blue
- **Disabled**: opacity 0.5, cursor not-allowed
- **Loading**: shows Streamlit spinner, disabled state

### 5.3 Status Badge
- **Online**: `#dcfce7` bg, `#16a34a` text, green dot
- **Offline**: `#fee2e2` bg, `#dc2626` text, red dot
- **Warning/Degraded**: `#fef3c7` bg, `#d97706` text, amber dot

### 5.4 Activity Log Entry
- **Container**: white bg, full width, 4px vertical padding
- **Timestamp**: muted monospace
- **Tag chip**: rounded, colored per tag type
- **Message**: dark slate text

### 5.5 Metric Tile
- **Container**: white bg, subtle colored top border (3px, accent color)
- **Number**: 32px DM Sans bold, primary blue
- **Label**: 11px uppercase muted text below

### 5.6 Quick Access Card
- **Container**: white bg, border, centered content, 12px radius
- **Hover**: border turns primary blue, subtle shadow, scale(1.02)
- **Icon**: 24px emoji
- **Name**: DM Sans 13px semibold
- **Caption**: muted, small, JetBrains Mono

---

## 6. Technical Approach

### Framework
- **Streamlit** (Python) — `st.set_page_config(layout="wide")`
- Single file: `run_streamlit_app.py` (~760 lines)
- No external component libraries — pure Streamlit + custom CSS injection

### CSS Strategy
- Single `<style>` block injected via `st.markdown(..., unsafe_allow_html=True)` at top of script
- CSS custom properties (variables) for all colors and spacing
- Google Fonts loaded via `@import` inside CSS block
- No Tailwind — vanilla CSS with BEM-like class names

### State Management
- `st.session_state` for:
  - `activity_log`: list of `(timestamp, tag, message, level)` tuples (max 80)
  - Services registry defined as constant at top of file

### Service Health Checks
- `check_port(port)` — uses `psutil.net_connections()` to detect if port is in use
- `check_docker_service(name)` — runs `docker inspect` command
- Called on every rerun (Streamlit's natural refresh cycle)

### Process Management
- Subprocess calls for Docker, uvicorn, Python scripts
- `subprocess.Popen` for background processes (API, streaming)
- `subprocess.run` for synchronous Docker commands
- `psutil.process_iter()` for killing processes by name/port

### Key Functions
```python
log_event(tag, msg, level)     # appends to session log
get_python()                   # cross-platform venv python path
check_port(port)               # True if port in use
check_docker_service(name)     # True if container running
refresh_services()             # dict of {name: {running, port}}
```

### Quality
- `uv run ruff check run_streamlit_app.py` — zero errors before commit
- `uv run mypy src/` — clean on all 14 source files
- CSS class names avoid collisions with Streamlit's internal classes

### Font Stack
```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
```

### File Structure
```
run_streamlit_app.py      # Single-file Streamlit app
├── CSS theme (embedded)
├── Session state init
├── Helper functions
├── SERVICES registry
├── Hero header
├── Metric tiles
├── Service status grid
├── Docker controls
├── API controls
├── Traffic generators
├── Activity log
└── Quick access cards
```