import json
import os
import urllib.request
from typing import Any

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="MLOps Prediction UI")

API_BASE = os.environ.get("API_BASE_URL", "http://localhost:8000")


CSS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700'
    '&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" '
    'rel="stylesheet">\n'
    "<style>\n"
    "    :root {\n"
    "        --bg:       #f8fafc;\n"
    "        --card:     #ffffff;\n"
    "        --subtle:   #f1f5f9;\n"
    "        --primary:  #3b82f6;\n"
    "        --hover:    #2563eb;\n"
    "        --accent:   #06b6d4;\n"
    "        --success:  #10b981;\n"
    "        --danger:   #ef4444;\n"
    "        --warning:  #f59e0b;\n"
    "        --text:     #1e293b;\n"
    "        --muted:    #64748b;\n"
    "        --border:   #e2e8f0;\n"
    "        --shadow:   0 2px 12px #0a0a0a10;\n"
    "        --radius:   12px;\n"
    "    }\n"
    "    * { box-sizing: border-box; margin: 0; padding: 0; }\n"
    "    body {\n"
    "        font-family: 'Inter', sans-serif;\n"
    "        background: var(--bg);\n"
    "        color: var(--text);\n"
    "        min-height: 100vh;\n"
    "        padding: 0;\n"
    "    }\n"
    "    a { text-decoration: none; }\n"
    "\n"
    "    .header {\n"
    "        background: var(--card);\n"
    "        border-bottom: 1px solid var(--border);\n"
    "        padding: 0 32px;\n"
    "        display: flex;\n"
    "        align-items: center;\n"
    "        justify-content: space-between;\n"
    "        height: 60px;\n"
    "        position: sticky;\n"
    "        top: 0;\n"
    "        z-index: 100;\n"
    "        box-shadow: var(--shadow);\n"
    "    }\n"
    "    .header-title {\n"
    "        font-family: 'DM Sans', sans-serif;\n"
    "        font-size: 18px;\n"
    "        font-weight: 700;\n"
    "        color: var(--primary);\n"
    "        letter-spacing: -0.3px;\n"
    "    }\n"
    "    .header-sub {\n"
    "        font-size: 12px;\n"
    "        color: var(--muted);\n"
    "        margin-left: 12px;\n"
    "        padding-left: 12px;\n"
    "        border-left: 1px solid var(--border);\n"
    "    }\n"
    "    .nav { display: flex; gap: 8px; }\n"
    "    .nav-btn {\n"
    "        font-family: 'DM Sans', sans-serif;\n"
    "        font-size: 13px;\n"
    "        font-weight: 600;\n"
    "        padding: 7px 18px;\n"
    "        border-radius: 8px;\n"
    "        border: 1px solid var(--border);\n"
    "        background: transparent;\n"
    "        color: var(--text);\n"
    "        cursor: pointer;\n"
    "        transition: all 0.15s;\n"
    "    }\n"
    "    .nav-btn:hover {\n"
    "        border-color: var(--primary);\n"
    "        color: var(--primary);\n"
    "        background: #eff6ff;\n"
    "    }\n"
    "    .nav-btn.active {\n"
    "        background: var(--primary);\n"
    "        color: #fff;\n"
    "        border-color: var(--primary);\n"
    "    }\n"
    "\n"
    "    .main { max-width: 900px; margin: 0 auto; padding: 32px 24px; }\n"
    "\n"
    "    .card {\n"
    "        background: var(--card);\n"
    "        border: 1px solid var(--border);\n"
    "        border-radius: var(--radius);\n"
    "        box-shadow: var(--shadow);\n"
    "        padding: 28px;\n"
    "        margin-bottom: 24px;\n"
    "    }\n"
    "    .card-title {\n"
    "        font-family: 'DM Sans', sans-serif;\n"
    "        font-size: 11px;\n"
    "        font-weight: 700;\n"
    "        letter-spacing: 1.5px;\n"
    "        text-transform: uppercase;\n"
    "        color: var(--muted);\n"
    "        margin-bottom: 20px;\n"
    "        display: flex;\n"
    "        align-items: center;\n"
    "        gap: 8px;\n"
    "    }\n"
    "    .card-title::before {\n"
    "        content: '';\n"
    "        width: 3px; height: 14px;\n"
    "        background: var(--primary);\n"
    "        border-radius: 2px;\n"
    "    }\n"
    "\n"
    "    .form-row {\n"
    "        display: grid;\n"
    "        grid-template-columns: 1fr 1fr;\n"
    "        gap: 16px;\n"
    "        margin-bottom: 16px;\n"
    "    }\n"
    "    .form-group { display: flex; flex-direction: column; gap: 6px; }\n"
    "    .form-group.full { grid-column: 1 / -1; }\n"
    "    label {\n"
    "        font-family: 'Inter', sans-serif;\n"
    "        font-size: 12px;\n"
    "        font-weight: 500;\n"
    "        color: var(--muted);\n"
    "    }\n"
    "    select, input {\n"
    "        font-family: 'Inter', sans-serif;\n"
    "        font-size: 13px;\n"
    "        padding: 9px 12px;\n"
    "        border: 1px solid var(--border);\n"
    "        border-radius: 8px;\n"
    "        background: var(--bg);\n"
    "        color: var(--text);\n"
    "        outline: none;\n"
    "        transition: border-color 0.15s;\n"
    "        width: 100%;\n"
    "    }\n"
    "    select:focus, input:focus {  # noqa: E501\n"
    "        border-color: var(--primary);\n"
    "        background: #fff;\n"
    "    }\n"
    "    input::placeholder { color: var(--muted); }\n"
    "\n"
    "    .btn-row { display: flex; gap: 12px; margin-top: 8px; }\n"
    "    .btn {\n"
    "        font-family: 'DM Sans', sans-serif;\n"
    "        font-size: 13px;\n"
    "        font-weight: 600;\n"
    "        padding: 10px 22px;\n"
    "        border-radius: 8px;\n"
    "        border: none;\n"
    "        cursor: pointer;\n"
    "        transition: all 0.15s;\n"
    "        display: inline-flex;\n"
    "        align-items: center;\n"
    "        gap: 8px;\n"
    "    }\n"
    "    .btn-primary {\n"
    "        background: var(--primary);\n"
    "        color: #fff;\n"
    "        flex: 1;\n"
    "        justify-content: center;\n"
    "    }\n"
    "    .btn-primary:hover { background: var(--hover); }\n"
    "    .btn-secondary {\n"
    "        background: transparent;\n"
    "        color: var(--text);\n"
    "        border: 1px solid var(--border);\n"
    "    }\n"
    "    .btn-secondary:hover {\n"
    "        border-color: var(--primary);\n"
    "        color: var(--primary);\n"
    "        background: #eff6ff;\n"
    "    }\n"
    "    .btn-danger {\n"
    "        background: transparent;\n"
    "        color: var(--danger);\n"
    "        border: 1px solid #fecaca;\n"
    "    }\n"
    "    .btn-danger:hover { background: #fef2f2; }\n"
    "\n"
    "    .result {\n"
    "        margin-top: 20px;\n"
    "        padding: 16px 20px;\n"
    "        border-radius: 10px;\n"
    "        font-family: 'JetBrains Mono', monospace;\n"
    "        font-size: 13px;\n"
    "        display: none;\n"
    "    }\n"
    "    .result.show { display: block; }\n"
    "    .result.ok {  # noqa: E501\n"
    "        background: #dcfce7;\n"
    "        color: #15803d;\n"
    "        border: 1px solid #86efac;\n"
    "    }\n"
    "    .result.error {  # noqa: E501\n"
    "        background: #fee2e2;\n"
    "        color: #dc2626;\n"
    "        border: 1px solid #fecaca;\n"
    "    }\n"
    "    .result-row { display: flex; gap: 16px; margin-bottom: 6px; }\n"
    "    .result-row:last-child { margin-bottom: 0; }\n"
    "    .result-label { color: var(--muted); min-width: 110px; }\n"
    "\n"
    "    .badge {\n"
    "        display: inline-block;\n"
    "        padding: 3px 12px;\n"
    "        border-radius: 20px;\n"
    "        font-size: 12px;\n"
    "        font-weight: 700;\n"
    "    }\n"
    "    .badge-0 { background: #dcfce7; color: #15803d; }\n"
    "    .badge-1 { background: #fee2e2; color: #dc2626; }\n"
    "    .badge-anomaly { background: #fef3c7; color: #b45309; }\n"
    "    .badge-normal  { background: #dbeafe; color: #1d4ed8; }\n"
    "\n"
    "    .history-table {\n"
    "        width: 100%;\n"
    "        border-collapse: collapse;\n"
    "        font-size: 12px;\n"
    "        margin-top: 8px;\n"
    "    }\n"
    "    .history-table th {\n"
    "        font-family: 'DM Sans', sans-serif;\n"
    "        font-size: 10px;\n"
    "        font-weight: 700;\n"
    "        text-transform: uppercase;\n"
    "        letter-spacing: 1px;\n"
    "        color: var(--muted);\n"
    "        padding: 8px 12px;\n"
    "        text-align: left;\n"
    "        border-bottom: 2px solid var(--border);\n"
    "    }\n"
    "    .history-table td {\n"
    "        padding: 9px 12px;\n"
    "        border-bottom: 1px solid var(--border);\n"
    "        vertical-align: middle;\n"
    "    }\n"
    "    .history-table tr:last-child td { border-bottom: none; }\n"
    "    .history-table tr:hover td { background: var(--subtle); }\n"
    "    .mono { font-family: 'JetBrains Mono', monospace; }\n"
    "    .ts { color: var(--muted); font-size: 11px; }\n"
    "\n"
    "    .footer {\n"
    "        text-align: center;\n"
    "        padding: 24px;\n"
    "        font-size: 11px;\n"
    "        color: var(--muted);\n"
    "        letter-spacing: 0.5px;\n"
    "    }\n"
    "\n"
    "    .loading {\n"
    "        display: none;\n"
    "        font-size: 13px;\n"
    "        color: var(--muted);\n"
    "        padding: 12px;\n"
    "        text-align: center;\n"
    "    }\n"
    "    .loading.show { display: block; }\n"
    "\n"
    "    @media (max-width: 640px) {\n"
    "        .form-row { grid-template-columns: 1fr; }\n"
    "        .header { padding: 0 16px; }\n"
    "    }\n"
    "</style>\n"
)


def nav_bar(active: str) -> str:
    predict_active = 'class="nav-btn active"' if active == "predict" else 'class="nav-btn"'  # noqa: E501
    ingest_active = 'class="nav-btn active"' if active == "ingest" else 'class="nav-btn"'  # noqa: E501
    return f"""
    <div class="header">
        <div style="display:flex;align-items:center;">
            <span class="header-title">🧮 Prediction UI</span>
            <span class="header-sub">MLOps Multi-Tenant</span>
        </div>
        <nav class="nav">
            <a href="/"><button {predict_active}>⚡ Predict</button></a>
            <a href="/ingest"><button {ingest_active}>💧 Ingest</button></a>
        </nav>
    </div>
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
            models = data.get("cached_models", [])
            if models:
                return models
    except Exception:
        pass
    return ["fraud_alert", "abandono_clientes", "fraude_financiero"]


PREDICT_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prediction UI — MLOps</title>
    {CSS}
</head>
<body>
    {NAV}
    <main class="main">
        <div class="card">
            <div class="card-title">Make a Prediction</div>
            <div class="form-group" style="margin-bottom:16px;">
                <label for="use_case">Use Case (Tenant)</label>
                <select id="use_case">{UC_OPTIONS}</select>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="f_monto">Monto</label>
                    <input type="number" id="f_monto" placeholder="e.g. 142.50"
                        step="0.01">
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
                <button class="btn btn-primary" onclick="doPredict()">
                    ⚡ Predict
                </button>
                <button class="btn btn-secondary" onclick="clearForm()">Clear</button>
            </div>
            <div id="loading" class="loading">Sending request...</div>
            <div id="result" class="result"></div>
        </div>
        <div class="card">
            <div class="card-title">Prediction History</div>
            <div style="overflow-x:auto;">
                <table class="history-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Use Case</th>
                            <th>Prediction</th>
                            <th>Model Version</th>
                            <th>Anomaly</th>
                        </tr>
                    </thead>
                    <tbody id="history_body">
                        <tr>
                            <td colspan="5" style="text-align:center;
                                color:var(--muted);padding:20px;">
                                No predictions yet
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
    <div class="footer">MLOps Prediction UI // Stream Learning Platform</div>
    <script>
        let history = [];
        function doPredict() {{
            const uc = document.getElementById('use_case').value;
            const monto = parseFloat(document.getElementById('f_monto').value) || 0;
            const distancia = parseFloat(document.getElementById('f_distancia').value) || 0;
            const hora = parseFloat(document.getElementById('f_hora').value) || 0;
            if (!monto && !distancia && !hora) {{
                showResult('error', 'Please fill in at least one feature');
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
            .then(r => r.json())
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
                history.unshift({{
                    ts: now, uc, pred, version: d.model_version, anomaly: anom
                }});
                if (history.length > 10) history.pop();
                renderHistory();
                const predRow = '<div class="result-row"><span class="result-label">'
                    + 'Prediction:</span>' + predBadge + '</div>';
                const anomRow = '<div class="result-row"><span class="result-label">'
                    + 'Anomaly:</span>' + badge + '</div>';
                const modelRow = '<div class="result-row"><span class="result-label">'
                    + 'Model:</span>' + d.model_version + '</div>';
                showResult('ok', predRow + anomRow + modelRow);
            }})
            .catch(err => {{
                document.getElementById('loading').classList.remove('show');
                showResult('error', 'Request failed: ' + err.message);
            }});
        }}
        function renderHistory() {{
            const body = document.getElementById('history_body');
            if (history.length === 0) {{
                body.innerHTML = '<tr><td colspan="5" style='
                    + '"text-align:center;color:var(--muted);padding:20px;">'
                    + 'No predictions yet</td></tr>';
                return;
            }}
            body.innerHTML = history.map(h => {{
                const predBadge = h.pred === 1
                    ? '<span class="badge badge-1">Fraud (1)</span>'
                    : '<span class="badge badge-0">Normal (0)</span>';
                const anomBadge = h.anomaly
                    ? '<span class="badge badge-anomaly">!</span>'
                    : '<span class="badge badge-normal">OK</span>';
                return '<tr>'
                    + '<td class="mono ts">' + h.ts + '</td>'
                    + '<td class="mono">' + h.uc + '</td>'
                    + '<td>' + predBadge + '</td>'
                    + '<td class="mono">' + h.version + '</td>'
                    + '<td>' + anomBadge + '</td>'
                    + '</tr>';
            }}).join('');
        }}
        function showResult(type, html) {{
            const el = document.getElementById('result');
            el.className = 'result show ' + type;
            el.innerHTML = html;
        }}
        function clearForm() {{
            ['f_monto','f_distancia','f_hora'].forEach(
                id => document.getElementById(id).value = ''
            );
            document.getElementById('result').classList.remove('show');
        }}
    </script>
</body>
</html>"""


INGEST_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ingest UI — MLOps</title>
    {CSS}
</head>
<body>
    {NAV}
    <main class="main">
        <div class="card">
            <div class="card-title">Ingest Streaming Data</div>
            <div class="form-group" style="margin-bottom:16px;">
                <label for="use_case">Use Case (Tenant)</label>
                <select id="use_case">{UC_OPTIONS}</select>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="f_monto">Monto</label>
                    <input type="number" id="f_monto"
                        placeholder="e.g. 142.50" step="0.01">
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
            <div class="form-group" style="margin-bottom:16px;">
                <label for="f_target">Target (optional — for retraining)</label>
                <input type="number" id="f_target"
                    placeholder="0 or 1. Blank for streaming-only." step="1">
            </div>
            <div class="btn-row">
                <button class="btn btn-primary" onclick="doIngest()">
                    Ingest Event
                </button>
                <button class="btn btn-secondary" onclick="clearForm()">Clear</button>
            </div>
            <div id="loading" class="loading">Sending request...</div>
            <div id="result" class="result"></div>
        </div>
        <div class="card">
            <div class="card-title">Ingest History</div>
            <div style="overflow-x:auto;">
                <table class="history-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Use Case</th>
                            <th>Amount</th>
                            <th>Anomaly Flagged</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody id="history_body">
                        <tr>
                            <td colspan="5" style="text-align:center;
                                color:var(--muted);padding:20px;">
                                No events yet
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
    <div class="footer">MLOps Prediction UI // Stream Learning Platform</div>
    <script>
        let history = [];
        function doIngest() {{
            const uc = document.getElementById('use_case').value;
            const monto = parseFloat(document.getElementById('f_monto').value) || 0;
            const distancia = parseFloat(document.getElementById('f_distancia').value) || 0;
            const hora = parseFloat(document.getElementById('f_hora').value) || 0;
            const target = document.getElementById('f_target').value;
            if (!monto && !distancia && !hora) {{
                showResult('error', 'Please fill in at least one feature');
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
            .then(r => r.json())
            .then(d => {{
                document.getElementById('loading').classList.remove('show');
                const now = new Date().toLocaleTimeString();
                const anomBadge = d.anomaly_flagged
                    ? '<span class="badge badge-anomaly">Anomaly</span>'
                    : '<span class="badge badge-normal">Normal</span>';
                history.unshift({{
                    ts: now, uc, amt: amt.toFixed(2),
                    anomaly: d.anomaly_flagged, status: d.status
                }});
                if (history.length > 10) history.pop();
                renderHistory();
                const statusRow = '<div class="result-row"><span class="result-label">'
                    + 'Status:</span>' + d.status + '</div>';
                const anomRow = '<div class="result-row"><span class="result-label">'
                    + 'Anomaly:</span>' + anomBadge + '</div>';
                showResult('ok', statusRow + anomRow);
            }})
            .catch(err => {{
                document.getElementById('loading').classList.remove('show');
                showResult('error', 'Request failed: ' + err.message);
            }});
        }}
        function renderHistory() {{
            const body = document.getElementById('history_body');
            if (history.length === 0) {{
                body.innerHTML = '<tr><td colspan="5" style='
                    + '"text-align:center;color:var(--muted);padding:20px;">'
                    + 'No events yet</td></tr>';
                return;
            }}
            body.innerHTML = history.map(h => {{
                const anomBadge = h.anomaly
                    ? '<span class="badge badge-anomaly">!</span>'
                    : '<span class="badge badge-normal">OK</span>';
                return '<tr>'
                    + '<td class="mono ts">' + h.ts + '</td>'
                    + '<td class="mono">' + h.uc + '</td>'
                    + '<td class="mono">' + h.amt + '</td>'
                    + '<td>' + anomBadge + '</td>'
                    + '<td class="mono" '
                    + 'style="color:var(--success)">' + h.status + '</td>'
                    + '</tr>';
            }}).join('');
        }}
        function showResult(type, html) {{
            const el = document.getElementById('result');
            el.className = 'result show ' + type;
            el.innerHTML = html;
        }}
        function clearForm() {{
            ['f_monto','f_distancia','f_hora','f_target'].forEach(
                id => document.getElementById(id).value = ''
            );
            document.getElementById('result').classList.remove('show');
        }}
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
