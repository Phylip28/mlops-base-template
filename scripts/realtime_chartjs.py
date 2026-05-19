"""
Real-time streaming chart — zero flicker.
Chart.js + chartjs-plugin-streaming render at 60fps client-side.
Python only injects via postMessage without destroying the iframe.

Run: streamlit run scripts/realtime_chartjs.py
"""

import random
import time

import streamlit as st

st.set_page_config(page_title="Real-time Chart.js", layout="wide")

# ── CSS: match AWS dark palette ──
st.markdown(
    """
<style>
.stApp { background: #0f141a; }
iframe { border: none !important; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div style="font-family:'Cabinet Grotesk',sans-serif; font-size:18px;
font-weight:700; color:#d5dbdb; margin-bottom:16px;">
    CPU Usage — sliding window (20s)
</div>
""",
    unsafe_allow_html=True,
)

# ── Chart.js iframe (rendered ONCE — never destroyed) ──
CHART_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js">
</script>
<script src="https://cdn.jsdelivr.net/npm/luxon@3.4.0/build/global/luxon.min.js">
</script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-luxon@1.3.0/dist/chartjs-adapter-luxon.min.js">
</script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-streaming@2.0.0/dist/chartjs-plugin-streaming.min.js">
</script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#0f141a; display:flex; align-items:center; justify-content:center;
       height:100vh; padding:12px; }
canvas { max-height:100%; }
</style>
</head>
<body>
<canvas id="cpu"></canvas>
<script>
// ── Chart.js config ──
var ctx = document.getElementById('cpu').getContext('2d');

var chart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'CPU %',
            data: [],
            borderColor: '#00a1c9',
            backgroundColor: 'rgba(0,161,201,0.06)',
            borderWidth: 2,
            pointRadius: 0,
            fill: 'origin',
            tension: 0.3
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 0 },
        interaction: { intersect: false, mode: 'index' },
        plugins: {
            legend: { display: false },
            streaming: {
                duration: 20000,
                delay: 1000,
                frameRate: 60,
                refresh: 1000,
                onRefresh: function(chart) {
                    // Generate data client-side — zero flicker
                    var v = 40 + 20 * Math.sin(Date.now() / 3000)
                          + (Math.random() - 0.5) * 30;
                    chart.data.datasets[0].data.push({
                        x: Date.now(),
                        y: Math.round(v)
                    });
                }
            }
        },
        scales: {
            x: {
                type: 'realtime',
                time: { displayFormats: { second: 'HH:mm:ss' } },
                ticks: { color: '#5f6b7a',
                         font: { family: 'JetBrains Mono', size: 10 } },
                grid: { color: 'rgba(42,47,54,0.4)' }
            },
            y: {
                min: 0,
                max: 100,
                ticks: { color: '#5f6b7a', font: { family: 'JetBrains Mono', size: 10 },
                         stepSize: 20 },
                grid: { color: 'rgba(42,47,54,0.4)' },
                title: { display: true, text: 'CPU %', color: '#5f6b7a',
                         font: { family: 'JetBrains Mono', size: 11 } }
            }
        }
    }
});

// ── Python → JS bridge via postMessage (iframe never destroyed) ──
window.addEventListener('message', function(e) {
    if (!e.data || e.data.value === undefined) return;
    chart.data.datasets[0].data.push({
        x: e.data.ts || Date.now(),
        y: e.data.value
    });
    chart.update('quiet');
});
</script>
</body>
</html>
"""

st.markdown(
    f"<iframe id=\"realtimeChart\" srcdoc='{CHART_HTML}' "
    f'width="100%" height="380" frameborder="0"></iframe>',
    unsafe_allow_html=True,
)

# ── Python → JS data push (no iframe destruction) ──
st.markdown("---")
st.caption("Python pushing data via postMessage every 1s")
place = st.empty()

while True:
    cpu_value = random.randint(20, 80)
    place.markdown(
        f"""
        <script>
        (function() {{
            var f = document.getElementById('realtimeChart');
            if (f && f.contentWindow) {{
                var d = {{value: {cpu_value}, ts: Date.now()}};
                f.contentWindow.postMessage(d, '*');
            }}
        }})();
        </script>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(1)
