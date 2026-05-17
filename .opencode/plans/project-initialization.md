# MLOps Base Template — Project Initialization

## Project Overview

Plataforma MLOps para automatizar el ciclo de vida del machine learning, resolviendo el problema de la "última milla" — modelos que completan su ciclo de vida pero nunca llegan a producción. Arquitectura basada en Streamlit + microservicios con contenedores.

## Current State (from codebase mapping)

### Architecture
- Hexagonal skeleton (`domain` → `application` → `infrastructure`) con multi-tenencia por `use_case`
- Capa `domain` vacía — toda la lógica vive en `application/services/` con acoplamiento directo a sklearn, mlflow, pandas
- Sin message broker — usa FastAPI `BackgroundTasks`
- Sin base de datos para estado de app — todo va a CSV + MLflow
- Hardcoded dev credentials (bloquea deploy cloud)

### Stack
- Python 3.11+, FastAPI + Pydantic v2, MLflow 3.10.1 (PostgreSQL + MinIO)
- scikit-learn (RandomForest + IsolationForest)
- Streamlit 1.30+, Prometheus + Grafana auto-provisioned
- Package management: `uv` para root, referencias a poetry/pip
- Sin CI/CD, sin auth, sin Dockerfile para la API

### UI Components
- **Streamlit Command Center** (p8502): `run_streamlit_app.py` — Dashboard de operaciones (955 líneas, CSS inline)
- **Prediction UI** (p8001): `services/prediction-ui/src/app.py` — FastAPI + HTML/JS vanilla (655 líneas, CSS inline)
  - Predict panel (`GET /`)
  - Ingest panel (`GET /ingest`)

## Known Issues

### Critical Bugs
1. **No CORS middleware** en la API (`src/model_service/infrastructure/entrypoints/api.py`) — el navegador bloquea todas las fetch() del prediction-ui (p8001) a la API (p8000). Causa que ningún panel devuelva resultados.
2. **ReferenceError en Ingest JS** (`services/prediction-ui/src/app.py:581`) — `amt` vs `monto`, variable undefined.

### UX Problems
3. Features fields hardcodeadas (`monto`, `distancia_km`, `hora_transaccion`) no sirven para todos los use cases
4. Sin protección contra doble clic en botones
5. Sin feedback visual de carga en botones
6. Historial solo en memoria JS — se pierde al recargar
7. Sin manejo de errores HTTP (4xx/5xx)
8. Sin diferenciación de errores del backend (siempre devuelve "Ingested")
9. Namespace de funciones JS compartido entre predict e ingest (posibles conflictos)

### UI/Visual
10. CSS inline en archivos monolíticos (difícil de mantener)
11. Diseño visual básico — sin sistema de diseño coherente
12. Sin responsive design completo
13. Sin tema oscuro
14. Streamlit dashboard y Prediction UI tienen estilos duplicados pero separados

## Requirements

### Phase 1: Fix Core Functionality
- Fix CORS middleware en API
- Fix ReferenceError en ingest JS
- Agregar protección anti-doble-clic
- Agregar loading states en botones
- Agregar manejo de errores HTTP (4xx/5xx)
- Validar que predict e ingest funcionan end-to-end

### Phase 2: Prediction Panel Redesign
- Rediseñar panel Predict con nueva UI
- Features dinámicos según use case seleccionado
- Historial persistente (localStorage o server-side)
- Diseño responsive
- Sistema de diseño coherente (design tokens, componentes reutilizables)

### Phase 3: Ingestion Panel Redesign
- Rediseñar panel Ingest con nueva UI
- Feedback claro de estado de ingesta
- Validaciones de formulario
- Historial de ingestas

### Phase 4: Streamlit Dashboard Redesign
- Rediseñar comando center con nueva identidad visual
- Componentes modulares (no todo en un archivo)
- Sistema de diseño compartido con Prediction UI
- Posible refactor a multi-page app

### Phase 5: Refinements
- Pruebas E2E de los paneles
- Documentación de uso
- Performance optimization

## Technical Approach

### UI Architecture Decision
Convertir `services/prediction-ui/` a una SPA moderna con componentes. Opciones:
- **Opción A (Recomendada)**: FastAPI + Jinja2 templates + Alpine.js + Tailwind CSS — mantiene backend Python, mejora frontend
- **Opción B**: Streamlit multi-page app — consistente con el dashboard existente
- **Opción C**: React/Vue SPA servida por FastAPI — más complejo, mayor capacidad

### Design System
Crear un sistema de diseño compartido:
- Design tokens (colores, typography, spacing, shadows)
- Componentes base (card, button, form, badge, table, modal)
- Tema claro/oscuro
- Responsive breakpoints

### Shared CSS/Packaging
Extraer CSS a archivos estáticos servidos por FastAPI (no inline) para mejor mantenibilidad.

## Configuration

```json
{
  "mode": "interactive",
  "granularity": "standard",
  "parallelization": true,
  "commit_docs": true,
  "model_profile": "inherit",
  "project_mode": "mvp",
  "workflow": {
    "research": true,
    "plan_check": true,
    "verifier": true,
    "nyquist_validation": true,
    "auto_advance": false
  }
}
```
