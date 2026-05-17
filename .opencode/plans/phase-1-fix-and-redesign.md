# Phase 1: Fix Core Bugs + Prediction UI Redesign

## Goal
Que los paneles Predict e Ingest funcionen correctamente y tengan una UI rediseñada atractiva.

## Bugs to Fix

### 1. Add CORS Middleware to API
**File:** `src/model_service/infrastructure/entrypoints/api.py`
**Action:** Add `CORSMiddleware` allowing origins `["http://localhost:8001", "http://127.0.0.1:8001"]` with credentials.
**Why:** Browser blocks cross-origin fetch() from prediction-ui (p8001) → API (p8000).

### 2. Fix ReferenceError in Ingest JS
**File:** `services/prediction-ui/src/app.py` line 581
**Action:** Change `amt.toFixed(2)` to `monto.toFixed(2)`.
**Why:** Variable `amt` is never declared; `monto` is the correct local variable.

### 3. Anti-double-click Protection
**File:** `services/prediction-ui/src/app.py`
**Action:** Disable button on click, re-enable after response.
**Why:** Prevents duplicate ingestions/predictions.

### 4. HTTP Error Handling
**File:** `services/prediction-ui/src/app.py`
**Action:** Check `response.ok` before `r.json()`, show appropriate error messages for 4xx/5xx.
**Why:** Currently shows generic "Request failed" for all errors.

### 5. Namespace JS Functions
**File:** `services/prediction-ui/src/app.py`
**Action:** Prefix functions per page (`predict_*`, `ingest_*`) or use IIFE/module pattern.
**Why:** Shared `showResult()`, `clearForm()` cause cross-page interference.

## Prediction UI Redesign

### 5. Extract CSS to Static File
**Action:** Move inline CSS from `app.py` to `services/prediction-ui/static/styles.css`.
**Why:** Maintainability — CSS inline en HTML monolítico es difícil de mantener.

### 6. Redesign Predict Panel
**Action:** Rediseñar el formulario Predict con:
- Diseño moderno con sombras suaves, bordes redondeados, espaciado generoso
- Gradient header y mejor jerarquía visual
- Dynamic feature fields según use case seleccionado (fetch schema from API or use dynamic key-value input)
- Better result display con animaciones suaves
- Loading spinner en botón
- Historial con persistencia en localStorage

### 7. Redesign Ingest Panel
**Action:** Rediseñar el formulario Ingest con:
- Mismo design system que Predict
- Target field mejor integrado
- Status badges más claros (verde/rojo/amarillo)
- Timeline view de ingestas recientes
- Same feature dynamics

### 8. Design System
**Action:** Create shared CSS design tokens:
- `:root` variables for colors, typography, spacing
- Font: DM Sans (headings), Inter (body), JetBrains Mono (code)
- Color palette: Slate/Blue/Cyan/Green/Red/Amber
- Component classes: `.card`, `.btn`, `.badge`, `.table`, `.form-group`
- Dark mode support via `prefers-color-scheme`

## Streamlit Dashboard Redesign (Phase 2)

### 9. Modular Streamlit App
**Action:** Refactor `run_streamlit_app.py` into:
- `streamlit_app/main.py` — entry point
- `streamlit_app/sections/` — section modules (hero, services, docker, api, traffic, log)
- `streamlit_app/styles.py` — CSS
- `streamlit_app/utils.py` — helper functions

### 10. Redesign Streamlit UI
**Action:** Apply same design system:
- Modern cards con hover effects
- Metrics con iconos y colores
- Service status con badges animados
- Docker controls con feedback visual
- Activity log mejorado

## Files Modified
```
src/model_service/infrastructure/entrypoints/api.py       # CORS
services/prediction-ui/src/app.py                          # Fixes + Redesign
services/prediction-ui/static/styles.css                   # NEW: extracted CSS
streamlit_app/main.py                                      # NEW: modular app
streamlit_app/sections/                                    # NEW: section modules
streamlit_app/styles.py                                    # NEW: extracted CSS
streamlit_app/utils.py                                     # NEW: helpers
```

## Dependencies Added
```
# pyproject.toml
fastapi-cors         # already in fastapi[standard] — no new dep needed
```

## Testing
1. Start API: `uvicorn src.model_service.infrastructure.entrypoints.api:app --host 0.0.0.0 --port 8000`
2. Start Prediction UI: `cd services/prediction-ui && uvicorn src.app:app --host 0.0.0.0 --port 8001`
3. Open `http://localhost:8001` — test Predict
4. Open `http://localhost:8001/ingest` — test Ingest
5. Verify no console errors
6. Test with wrong use case → error message shown
7. Test rapid double-click → no duplicate
8. Refresh page → history persists (localStorage)
