"""Tiny HTTP endpoint that serves latest metrics snapshot to Chart.js iframes.

Runs in a background thread, started once when the module is imported.
"""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

TELEMETRY_PORT = 8503

_latest: dict[str, float] = {}
_lock = threading.Lock()


def update_snapshot(data: dict[str, float]) -> None:
    """Store latest snapshot (called from Streamlit fragment)."""
    global _latest
    with _lock:
        _latest = dict(data)


def _get_snapshot() -> dict[str, float]:
    with _lock:
        return dict(_latest)


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/metrics":
            data = _get_snapshot()
            body = json.dumps(data).encode()
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
        pass  # silent


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
