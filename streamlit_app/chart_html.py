# ruff: noqa: E501
"""Generate self-polling Chart.js widgets for st.iframe."""

from __future__ import annotations


def build_chart_html(
    chart_id: str,
    title: str,
    metric_key: str,
    color: str,
    y_label: str,
    y_min: float,
    y_max: float,
    height: int = 260,
) -> str:
    escaped_title = title.replace("'", "\\'")
    escaped_y_label = y_label.replace("'", "\\'")
    y_range = y_max - y_min
    y_padding = y_range * 0.05

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0f141a;font-family:'JetBrains Mono',monospace;color:#d5dbdb;padding:10px 12px 6px 12px;overflow:hidden;margin:0}}
.chart-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;min-height:22px}}
.chart-title{{font-size:12px;font-weight:600;color:#d5dbdb;text-transform:uppercase;letter-spacing:.5px;white-space:nowrap}}
.ctrl-group{{display:flex;gap:6px;align-items:center}}
.aws-btn{{background:rgba(0,161,201,.08);border:1px solid rgba(0,161,201,.25);color:#00a1c9;border-radius:4px;padding:2px 8px;cursor:pointer;font-size:13px;font-family:inherit;line-height:1.4;transition:background .15s,border-color .15s}}
.aws-btn:hover{{background:rgba(0,161,201,.18);border-color:rgba(0,161,201,.45)}}
.aws-btn:active{{background:rgba(0,161,201,.25)}}
.aws-select{{background:#1e242b;border:1px solid #2a2f36;color:#95a5a6;border-radius:4px;padding:2px 6px;font-size:11px;font-family:inherit;cursor:pointer;outline:none;-webkit-appearance:none;appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='8' height='5'%3E%3Cpath d='M0 0l4 5 4-5z' fill='%235f6b7a'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 6px center;padding-right:18px}}
.aws-select:focus{{border-color:#00a1c9}}
.aws-select option{{background:#1e242b;color:#d5dbdb}}
.canvas-wrap{{width:100%;height:{height - 32}px}}
canvas{{width:100%!important;height:100%!important;cursor:crosshair}}
</style></head>
<body>
<div class="chart-header">
  <span class="chart-title">{escaped_title}</span>
  <div class="ctrl-group">
    <button class="aws-btn" id="btn-refresh" title="Refresh chart">&#x21bb;</button>
    <select class="aws-select" id="sel-interval" title="Auto-refresh interval">
      <option value="1">1s</option>
      <option value="5">5s</option>
      <option value="10" selected>10s</option>
      <option value="30">30s</option>
      <option value="60">1m</option>
      <option value="300">5m</option>
    </select>
  </div>
</div>
<div class="canvas-wrap"><canvas id="chart"></canvas></div>
<script>
(function() {{
  var METRIC_KEY = '{metric_key}';
  var BORDER_COLOR = '{color}';
  var BG_COLOR = '{color}1a';
  var Y_MIN = {y_min - y_padding};
  var Y_MAX = {y_max + y_padding};
  var WINDOW_MS = 120000;
  var ctx = document.getElementById('chart').getContext('2d');
  var isHovering = false;
  var pendingValue = null;
  var pollIntervalMs = 10000;
  var pollTimer = null;
  var dataBuffer = [];
  var seenKeys = new Set();
  var historyLoaded = false;

  function fmtTime(ts) {{
    var d = new Date(ts);
    var h = String(d.getHours()).padStart(2,'0');
    var m = String(d.getMinutes()).padStart(2,'0');
    var s = String(d.getSeconds()).padStart(2,'0');
    return h + ':' + m + ':' + s;
  }}

  var chart = new Chart(ctx, {{
    type: 'line',
    data: {{ datasets: [{{
      label: '{escaped_y_label}',
      borderColor: BORDER_COLOR,
      backgroundColor: BG_COLOR,
      borderWidth: 2,
      pointRadius: 0,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: BORDER_COLOR,
      pointHoverBorderColor: '#fff',
      pointHoverBorderWidth: 2,
      fill: true,
      tension: 0.15,
      data: []
    }}] }},
    options: {{
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      interaction: {{ intersect: false, mode: 'index' }},
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          backgroundColor: '#1e242b', titleColor: '#d5dbdb', bodyColor: '#95a5a6',
          borderColor: '#2a2f36', borderWidth: 1, displayColors: false,
          titleFont: {{ family: 'JetBrains Mono', size: 11, weight: '500' }},
          bodyFont: {{ family: 'JetBrains Mono', size: 12, weight: '500' }},
          padding: 10, cornerRadius: 4,
          callbacks: {{
            title: function(items) {{ return items.length ? fmtTime(items[0].parsed.x) : ''; }},
            label: function(c) {{ return c.parsed.y.toFixed(1); }}
          }}
        }}
      }},
      scales: {{
        x: {{
          type: 'linear',
          ticks: {{
            color: '#5f6b7a', font: {{ family: 'JetBrains Mono', size: 9 }},
            maxTicksLimit: 8,
            callback: function(v) {{ return fmtTime(v); }}
          }},
          grid: {{ color: 'rgba(42,47,54,.4)' }}
        }},
        y: {{
          min: Y_MIN, max: Y_MAX,
          ticks: {{ color: '#5f6b7a', font: {{ family: 'JetBrains Mono', size: 9 }}, callback: function(v) {{ return v.toFixed(0); }} }},
          grid: {{ color: 'rgba(42,47,54,.4)' }}
        }}
      }}
    }}
  }});

  var canvas = chart.canvas;
  canvas.addEventListener('mouseenter', function() {{ isHovering = true; }});
  canvas.addEventListener('mouseleave', function() {{ isHovering = false; if (pendingValue !== null) {{ addPoint(pendingValue); pendingValue = null; tick(); }} }});

  function addPoint(val) {{
    var now = Date.now();
    var key = Math.floor(now / 100) * 100;
    if (seenKeys.has(key)) return;
    seenKeys.add(key);
    if (seenKeys.size > 600) {{
      var a = Array.from(seenKeys); seenKeys = new Set(a.slice(a.length - 400));
    }}
    dataBuffer.push({{ x: now, y: val }});
    while (dataBuffer.length > 0 && dataBuffer[0].x < now - WINDOW_MS) dataBuffer.shift();
  }}

  function addHistoryPoint(tsStr, val) {{
    var t = new Date(tsStr).getTime();
    if (isNaN(t)) return;
    var key = Math.floor(t / 100) * 100;
    if (seenKeys.has(key)) return;
    seenKeys.add(key);
    dataBuffer.push({{ x: t, y: val }});
  }}

  function tick() {{
    if (isHovering && pendingValue !== null) return;
    chart.data.datasets[0].data = dataBuffer.slice();
    var now = Date.now();
    chart.options.scales.x.min = now - WINDOW_MS;
    chart.options.scales.x.max = now + 3000;
    chart.update('none');
  }}

  function poll() {{
    fetch('http://localhost:8503/metrics')
      .then(function(r) {{ return r.json(); }})
      .then(function(data) {{
        var val = data[METRIC_KEY];
        if (val === undefined || val === null) return;
        if (isHovering) {{ pendingValue = val; return; }}
        addPoint(val);
        tick();
      }})
      .catch(function(){{}});
  }}

  function loadHistory() {{
    fetch('http://localhost:8503/metrics?history=true')
      .then(function(r) {{ return r.json(); }})
      .then(function(all) {{
        var points = all[METRIC_KEY];
        if (!points || !points.length) {{ historyLoaded = true; poll(); startLoop(); return; }}
        seenKeys.clear();
        dataBuffer = [];
        for (var i = 0; i < points.length; i++) {{
          addHistoryPoint(points[i].ts, points[i].val);
        }}
        historyLoaded = true;
        tick();
        poll();
        startLoop();
      }})
      .catch(function(){{ historyLoaded = true; poll(); startLoop(); }});
  }}

  function handleRefresh() {{
    dataBuffer = [];
    seenKeys.clear();
    pendingValue = null;
    chart.data.datasets[0].data = [];
    chart.update('none');
  }}

  function handleInterval(v) {{
    pollIntervalMs = parseInt(v) * 1000;
    clearInterval(pollTimer);
    pollTimer = setInterval(poll, pollIntervalMs);
  }}

  function startLoop() {{
    pollTimer = setInterval(poll, pollIntervalMs);
  }}

  document.getElementById('btn-refresh').addEventListener('click', handleRefresh);
  document.getElementById('sel-interval').addEventListener('change', function() {{ handleInterval(this.value); }});

  loadHistory();
}})();
</script>
</body></html>"""
