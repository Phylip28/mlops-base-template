# ruff: noqa: E501
import json
import os
import urllib.request
from typing import Any, cast

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="MLOps Prediction UI")

static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

API_BASE = os.environ.get("API_BASE_URL", "http://localhost:8000")


CSS = '<link rel="stylesheet" href="/static/styles.css">'


def nav_bar(active: str) -> str:
    predict_active = (
        'class="nav-btn active"' if active == "predict" else 'class="nav-btn"'
    )
    ingest_active = (
        'class="nav-btn active"' if active == "ingest" else 'class="nav-btn"'
    )
    return f"""
    <header class="app-header">
        <div style="display:flex;align-items:center;">
            <span class="app-header-title">
                <span class="logo-dot"></span>
                Prediction UI
                <span class="app-header-sub">MLOps Multi-Tenant</span>
            </span>
        </div>
        <nav class="nav">
            <a href="/"><button {predict_active}>⚡ Predict</button></a>
            <a href="/ingest"><button {ingest_active}>💧 Ingest</button></a>
        </nav>
    </header>
    """


def get_use_cases() -> list[str]:
    try:
        req = urllib.request.Request(
            f"{API_BASE}/health",
            headers={"Accept": "application/json"},
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            models_raw = data.get("cached_models", [])
            if models_raw:
                return cast(list[str], models_raw)
    except Exception:
        pass
    return ["fraud_alert", "abandono_clientes", "fraude_financiero"]


PREDICT_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Predict — MLOps Platform</title>
    {CSS}
</head>
<body>
    {NAV}
    <main class="main">
        <div class="card">
            <div class="card-title">Make a Prediction</div>
            <div class="form-group full" style="margin-bottom:16px;">
                <label for="use_case">Use Case (Tenant)</label>
                <select id="use_case">{UC_OPTIONS}</select>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="f_monto">Monto</label>
                    <input type="number" id="f_monto" placeholder="e.g. 142.50" step="0.01">
                </div>
                <div class="form-group">
                    <label for="f_distancia">Distancia (km)</label>
                    <input type="number" id="f_distancia" placeholder="e.g. 5.0" step="0.1">
                </div>
                <div class="form-group">
                    <label for="f_hora">Hora Transacci&#243;n</label>
                    <input type="number" id="f_hora" placeholder="e.g. 14.5" step="0.1">
                </div>
            </div>
            <div class="btn-row">
                <button id="predict-btn" class="btn btn-primary" onclick="predict_doPredict()">
                    ⚡ Predict
                </button>
                <button class="btn btn-secondary" onclick="predict_clearForm()">Clear</button>
            </div>
            <div id="loading" class="loading"><span class="spinner"></span> Running prediction...</div>
            <div id="result" class="result"></div>
        </div>
        <div class="card">
            <div class="card-title">Prediction History</div>
            <div class="history-section" style="overflow-x:auto;">
                <table class="history-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Use Case</th>
                            <th>Prediction</th>
                            <th>Model</th>
                            <th>Anomaly</th>
                        </tr>
                    </thead>
                    <tbody id="history_body">
                        <tr class="empty-row">
                            <td colspan="5">No predictions yet</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
    <footer class="app-footer">MLOps Platform &mdash; Stream Learning</footer>
    <script>
        (function() {{
            const STORAGE_KEY = 'mlops_predict_history';
            let history = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');

            function save() {{
                localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
            }}

            window.predict_doPredict = function() {{
                const btn = document.getElementById('predict-btn');
                btn.disabled = true;
                btn.innerHTML = '⏳ Predicting...';

                const uc = document.getElementById('use_case').value;
                const monto = parseFloat(document.getElementById('f_monto').value) || 0;
                const distancia = parseFloat(document.getElementById('f_distancia').value) || 0;
                const hora = parseFloat(document.getElementById('f_hora').value) || 0;
                if (!monto && !distancia && !hora) {{
                    predict_showResult('error', 'Please fill in at least one feature');
                    btn.disabled = false;
                    btn.innerHTML = '⚡ Predict';
                    return;
                }}
                document.getElementById('loading').classList.add('show');
                document.getElementById('result').classList.remove('show', 'ok', 'error');
                const features = {{}};
                if (document.getElementById('f_monto').value) features.monto = monto;
                if (document.getElementById('f_distancia').value) features.distancia_km = distancia;
                if (document.getElementById('f_hora').value) features.hora_transaccion = hora;
                fetch('{API_BASE}/predict/' + encodeURIComponent(uc), {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ features }})
                }})
                .then(r => {{
                    if (!r.ok) return r.text().then(t => {{ throw new Error(t || 'HTTP ' + r.status); }});
                    return r.json();
                }})
                .then(d => {{
                    document.getElementById('loading').classList.remove('show');
                    const pred = d.prediction;
                    const anom = d.is_anomaly;
                    const badge = anom
                        ? '<span class="badge badge-anomaly">Anomaly</span>'
                        : '<span class="badge badge-normal">Normal</span>';
                    const predBadge = pred === 1
                        ? '<span class="badge badge-1">Fraud (1)</span>'
                        : '<span class="badge badge-0">Normal (0)</span>';
                    const now = new Date().toLocaleTimeString();
                    history.unshift({{ ts: now, uc, pred, version: d.model_version, anomaly: anom }});
                    if (history.length > 20) history.pop();
                    save();
                    render();
                    predict_showResult('ok',
                        '<div class="result-row"><span class="result-label">Prediction:</span><span class="result-value">' + predBadge + '</span></div>' +
                        '<div class="result-row"><span class="result-label">Anomaly:</span><span class="result-value">' + badge + '</span></div>' +
                        '<div class="result-row"><span class="result-label">Model:</span><span class="result-value mono">' + d.model_version + '</span></div>'
                    );
                }})
                .catch(err => {{
                    document.getElementById('loading').classList.remove('show');
                    predict_showResult('error', 'Request failed: ' + err.message);
                }})
                .finally(() => {{
                    btn.disabled = false;
                    btn.innerHTML = '⚡ Predict';
                }});
            }};

            function render() {{
                const body = document.getElementById('history_body');
                if (history.length === 0) {{
                    body.innerHTML = '<tr class="empty-row"><td colspan="5">No predictions yet</td></tr>';
                    return;
                }}
                body.innerHTML = history.map(h => {{
                    const predBadge = h.pred === 1
                        ? '<span class="badge badge-1">Fraud</span>'
                        : '<span class="badge badge-0">Normal</span>';
                    const anomBadge = h.anomaly
                        ? '<span class="badge badge-anomaly">!</span>'
                        : '<span class="badge badge-normal">OK</span>';
                    return '<tr>' +
                        '<td class="mono ts">' + h.ts + '</td>' +
                        '<td class="mono">' + h.uc + '</td>' +
                        '<td>' + predBadge + '</td>' +
                        '<td class="mono">' + h.version + '</td>' +
                        '<td>' + anomBadge + '</td>' +
                        '</tr>';
                }}).join('');
            }}

            window.predict_showResult = function(type, html) {{
                const el = document.getElementById('result');
                el.className = 'result show ' + type;
                el.innerHTML = html;
            }};

            window.predict_clearForm = function() {{
                ['f_monto','f_distancia','f_hora'].forEach(id => document.getElementById(id).value = '');
                document.getElementById('result').classList.remove('show');
            }};

            render();
        }})();
    </script>
</body>
</html>"""


INGEST_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ingest — MLOps Platform</title>
    {CSS}
</head>
<body>
    {NAV}
    <main class="main">
        <div class="card">
            <div class="card-title">Ingest Streaming Data</div>
            <div class="form-group full" style="margin-bottom:16px;">
                <label for="use_case">Use Case (Tenant)</label>
                <select id="use_case">{UC_OPTIONS}</select>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="f_monto">Monto</label>
                    <input type="number" id="f_monto" placeholder="e.g. 142.50" step="0.01">
                </div>
                <div class="form-group">
                    <label for="f_distancia">Distancia (km)</label>
                    <input type="number" id="f_distancia" placeholder="e.g. 5.0" step="0.1">
                </div>
                <div class="form-group">
                    <label for="f_hora">Hora Transacci&#243;n</label>
                    <input type="number" id="f_hora" placeholder="e.g. 14.5" step="0.1">
                </div>
            </div>
            <div class="form-group full" style="margin-bottom:16px;">
                <label for="f_target">Target <span style="font-weight:400;color:var(--text-muted);">(optional — for retraining)</span></label>
                <input type="number" id="f_target" placeholder="0 or 1. Leave blank for streaming-only." step="1">
            </div>
            <div class="btn-row">
                <button id="ingest-btn" class="btn btn-primary" onclick="ingest_doIngest()">
                    💧 Ingest Event
                </button>
                <button class="btn btn-secondary" onclick="ingest_clearForm()">Clear</button>
            </div>
            <div id="loading" class="loading"><span class="spinner"></span> Ingesting...</div>
            <div id="result" class="result"></div>
        </div>
        <div class="card">
            <div class="card-title">Ingest History</div>
            <div class="history-section" style="overflow-x:auto;">
                <table class="history-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Use Case</th>
                            <th>Amount</th>
                            <th>Anomaly</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody id="history_body">
                        <tr class="empty-row">
                            <td colspan="5">No events yet</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
    <footer class="app-footer">MLOps Platform &mdash; Stream Learning</footer>
    <script>
        (function() {{
            const STORAGE_KEY = 'mlops_ingest_history';
            let history = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');

            function save() {{
                localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
            }}

            window.ingest_doIngest = function() {{
                const btn = document.getElementById('ingest-btn');
                btn.disabled = true;
                btn.innerHTML = '⏳ Ingesting...';

                const uc = document.getElementById('use_case').value;
                const monto = parseFloat(document.getElementById('f_monto').value) || 0;
                const distancia = parseFloat(document.getElementById('f_distancia').value) || 0;
                const hora = parseFloat(document.getElementById('f_hora').value) || 0;
                const target = document.getElementById('f_target').value;
                if (!monto && !distancia && !hora) {{
                    ingest_showResult('error', 'Please fill in at least one feature');
                    btn.disabled = false;
                    btn.innerHTML = '💧 Ingest Event';
                    return;
                }}
                document.getElementById('loading').classList.add('show');
                document.getElementById('result').classList.remove('show', 'ok', 'error');
                const features = {{}};
                if (document.getElementById('f_monto').value) features.monto = monto;
                if (document.getElementById('f_distancia').value) features.distancia_km = distancia;
                if (document.getElementById('f_hora').value) features.hora_transaccion = hora;
                const body = {{ features }};
                if (target !== '') body.target = parseInt(target);
                fetch('{API_BASE}/ingest/' + encodeURIComponent(uc), {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(body)
                }})
                .then(r => {{
                    if (!r.ok) return r.text().then(t => {{ throw new Error(t || 'HTTP ' + r.status); }});
                    return r.json();
                }})
                .then(d => {{
                    document.getElementById('loading').classList.remove('show');
                    const now = new Date().toLocaleTimeString();
                    const anomBadge = d.anomaly_flagged
                        ? '<span class="badge badge-anomaly">Anomaly</span>'
                        : '<span class="badge badge-normal">Normal</span>';
                    const statusBadge = d.status === 'Ingested'
                        ? '<span class="badge badge-ingested">' + d.status + '</span>'
                        : '<span class="badge badge-processing">' + d.status + '</span>';
                    history.unshift({{
                        ts: now, uc, amt: monto.toFixed(2),
                        anomaly: d.anomaly_flagged, status: d.status
                    }});
                    if (history.length > 20) history.pop();
                    save();
                    render();
                    ingest_showResult('ok',
                        '<div class="result-row"><span class="result-label">Status:</span><span class="result-value">' + statusBadge + '</span></div>' +
                        '<div class="result-row"><span class="result-label">Anomaly:</span><span class="result-value">' + anomBadge + '</span></div>'
                    );
                }})
                .catch(err => {{
                    document.getElementById('loading').classList.remove('show');
                    ingest_showResult('error', 'Request failed: ' + err.message);
                }})
                .finally(() => {{
                    btn.disabled = false;
                    btn.innerHTML = '💧 Ingest Event';
                }});
            }};

            function render() {{
                const body = document.getElementById('history_body');
                if (history.length === 0) {{
                    body.innerHTML = '<tr class="empty-row"><td colspan="5">No events yet</td></tr>';
                    return;
                }}
                body.innerHTML = history.map(h => {{
                    const anomBadge = h.anomaly
                        ? '<span class="badge badge-anomaly">!</span>'
                        : '<span class="badge badge-normal">OK</span>';
                    const statusBadge = h.status === 'Ingested'
                        ? '<span class="badge badge-ingested">' + h.status + '</span>'
                        : '<span class="badge badge-processing">' + h.status + '</span>';
                    return '<tr>' +
                        '<td class="mono ts">' + h.ts + '</td>' +
                        '<td class="mono">' + h.uc + '</td>' +
                        '<td class="mono">' + h.amt + '</td>' +
                        '<td>' + anomBadge + '</td>' +
                        '<td>' + statusBadge + '</td>' +
                        '</tr>';
                }}).join('');
            }}

            window.ingest_showResult = function(type, html) {{
                const el = document.getElementById('result');
                el.className = 'result show ' + type;
                el.innerHTML = html;
            }};

            window.ingest_clearForm = function() {{
                ['f_monto','f_distancia','f_hora','f_target'].forEach(id => document.getElementById(id).value = '');
                document.getElementById('result').classList.remove('show');
            }};

            render();
        }})();
    </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def predict_page() -> str:
    use_cases = get_use_cases()
    uc_options = "".join(f'<option value="{u}">{u}</option>' for u in use_cases)
    return PREDICT_PAGE.format(
        CSS=CSS, NAV=nav_bar("predict"), UC_OPTIONS=uc_options, API_BASE=API_BASE
    )


@app.get("/ingest", response_class=HTMLResponse)
async def ingest_page() -> str:
    use_cases = get_use_cases()
    uc_options = "".join(f'<option value="{u}">{u}</option>' for u in use_cases)
    return INGEST_PAGE.format(
        CSS=CSS, NAV=nav_bar("ingest"), UC_OPTIONS=uc_options, API_BASE=API_BASE
    )


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"status": "ok", "service": "prediction-ui", "api_base": API_BASE}
