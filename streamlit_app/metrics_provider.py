"""Real metrics from Prometheus + Docker — no random data."""

from __future__ import annotations

import math
import subprocess
from datetime import datetime, timezone

import requests  # type: ignore[import-untyped]


def _sanitize(val: float | None) -> float:
    if val is None:
        return 0.0
    if math.isnan(val) or math.isinf(val):
        return 0.0
    return float(val)


PROMETHEUS_URL = "http://localhost:9090"
API_HEALTH_URL = "http://localhost:8000/health"
REQUEST_TIMEOUT = 3.0

CONTAINER_NAMES = [
    "mlops_postgres",
    "mlops_mlflow",
    "mlops_minio",
    "mlops_prometheus",
    "mlops_grafana",
    "mlops_prediction_ui",
]


def _promql_scalar(query: str) -> float | None:
    try:
        r = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={"query": query},
            timeout=REQUEST_TIMEOUT,
        )
        r.raise_for_status()
        results = r.json().get("data", {}).get("result", [])
        if results:
            return float(results[0]["value"][1])
        return None
    except Exception:
        return None


def _promql_range(query: str, step: str, minutes: int) -> list[dict[str, object]]:
    """Range query returning list of {ts: datetime, value: float}."""
    try:
        end = datetime.now(timezone.utc)
        start_ts = int((end.timestamp() - minutes * 60))
        end_ts = int(end.timestamp())
        r = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query_range",
            params={
                "query": query,
                "start": start_ts,
                "end": end_ts,
                "step": step,
            },
            timeout=REQUEST_TIMEOUT,
        )
        r.raise_for_status()
        results = r.json().get("data", {}).get("result", [])
        points: list[dict[str, object]] = []
        for series in results:
            for ts, val in series.get("values", []):
                points.append(
                    {
                        "ts": datetime.fromtimestamp(float(ts), tz=timezone.utc),
                        "value": float(val),
                    }
                )
        points.sort(key=lambda p: p["ts"])  # type: ignore[arg-type, return-value]
        return points
    except Exception:
        return []


def api_uptime() -> float:
    val = _promql_scalar('up{job="mlops-api"}')
    if val is not None:
        return val * 100.0
    try:
        r = requests.get(API_HEALTH_URL, timeout=2)
        return 100.0 if r.status_code == 200 else 0.0
    except Exception:
        return 0.0


def api_latency_ms() -> float:
    val = _promql_scalar(
        "histogram_quantile(0.5, "
        "rate(api_request_duration_seconds_bucket{job='mlops-api'}[1m])) * 1000"
    )
    return _sanitize(val)


def api_rps() -> float:
    val = _promql_scalar("rate(api_requests_total{job='mlops-api'}[1m])")
    return _sanitize(val)


def api_error_rate_pct() -> float:
    val = _promql_scalar(
        "rate(api_requests_total{job='mlops-api',status_code=~'5..'}[1m])"
        " / rate(api_requests_total{job='mlops-api'}[1m]) * 100"
    )
    val = _sanitize(val)
    return max(0.0, min(100.0, val))


def api_cpu_percent() -> float:
    val = _promql_scalar("rate(process_cpu_seconds_total{job='mlops-api'}[1m]) * 100")
    return _sanitize(val)


def api_memory_mb() -> float:
    val = _promql_scalar("process_resident_memory_bytes{job='mlops-api'} / 1024 / 1024")
    return _sanitize(val)


def container_status(container_name: str) -> float:
    try:
        result = subprocess.run(
            [
                "docker",
                "inspect",
                "-f",
                "{{.State.Running}}",
                container_name,
            ],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return 100.0 if result.stdout.strip() == "true" else 0.0
    except Exception:
        return 0.0


_CONTAINER_CPU_NAMES = [
    "mlops_postgres",
    "mlops_mlflow",
    "mlops_minio",
    "mlops_prometheus",
    "mlops_grafana",
]


def container_cpu_stats() -> dict[str, float]:
    """Return CPU % for infrastructure containers via a single docker stats call."""
    out: dict[str, float] = {name: 0.0 for name in _CONTAINER_CPU_NAMES}
    try:
        result = subprocess.run(
            ["docker", "stats", "--no-stream", "--format", "{{.Name}}|{{.CPUPerc}}"]
            + _CONTAINER_CPU_NAMES,
            capture_output=True,
            text=True,
            timeout=10,
        )
        for line in result.stdout.splitlines():
            if "|" not in line:
                continue
            name, raw = line.split("|", 1)
            name = name.strip()
            raw = raw.strip().replace("%", "")
            if name in out and raw != "--":
                try:
                    out[name] = float(raw)
                except ValueError:
                    out[name] = 0.0
    except Exception:
        pass
    return out


def collect_snapshot() -> dict[str, float]:
    cpu_map = container_cpu_stats()
    return {
        "api_uptime": api_uptime(),
        "api_latency_ms": api_latency_ms(),
        "api_rps": api_rps(),
        "api_error_pct": api_error_rate_pct(),
        "api_cpu": api_cpu_percent(),
        "api_memory": api_memory_mb(),
        "pg_status": container_status("mlops_postgres"),
        "mlflow_status": container_status("mlops_mlflow"),
        "minio_status": container_status("mlops_minio"),
        "prometheus_status": container_status("mlops_prometheus"),
        "grafana_status": container_status("mlops_grafana"),
        "pg_cpu": cpu_map["mlops_postgres"],
        "mlflow_cpu": cpu_map["mlops_mlflow"],
        "minio_cpu": cpu_map["mlops_minio"],
        "prometheus_cpu": cpu_map["mlops_prometheus"],
        "grafana_cpu": cpu_map["mlops_grafana"],
    }
