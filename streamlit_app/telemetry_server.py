"""Tiny HTTP endpoint that serves latest + historical metrics to Chart.js iframes.

Runs in a background thread.  Maintains 120-point rolling history so
charts survive page reload and pick up where they left off.
"""

from __future__ import annotations

import json
import threading
from collections import deque
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

TELEMETRY_PORT = 8503
HISTORY_MAX = 120

_latest: dict[str, float] = {}
_history: dict[str, deque[dict[str, object]]] = {}
_lock = threading.Lock()


def update_snapshot(data: dict[str, float]) -> None:
    """Store latest snapshot + append to rolling history (called from fragment)."""
    global _latest, _history
    with _lock:
        _latest = dict(data)
        from datetime import datetime, timezone

        ts = datetime.now(timezone.utc).isoformat()
        for key, val in data.items():
            if key not in _history:
                _history[key] = deque(maxlen=HISTORY_MAX)
            _history[key].append({"ts": ts, "val": val})


def _get_snapshot() -> dict[str, float]:
    with _lock:
        return dict(_latest)


def _get_history(metric_key: str) -> list[dict[str, object]]:
    with _lock:
        dq = _history.get(metric_key)
        return list(dq) if dq else []


def _get_all_history() -> dict[str, list[dict[str, object]]]:
    with _lock:
        return {k: list(v) for k, v in _history.items()}


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/metrics":
            if "history" in parsed.query:
                body = json.dumps(_get_all_history()).encode()
            else:
                body = json.dumps(_get_snapshot()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        pass


_server: HTTPServer | None = None


def _start_server() -> None:
    global _server
    try:
        _server = HTTPServer(("0.0.0.0", TELEMETRY_PORT), _Handler)
        _server.serve_forever()
    except Exception:
        pass


_server_started = False
_start_lock = threading.Lock()


def ensure_running() -> None:
    global _server_started
    if _server_started:
        return
    with _start_lock:
        if _server_started:
            return
        t = threading.Thread(target=_start_server, daemon=True)
        t.start()
        _server_started = True
