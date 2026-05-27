"""
app/metrics.py — simple in-memory observability metrics.

In production you'd push these to Prometheus, CloudWatch, Datadog etc.
Here we just keep counters and expose them via a /metrics endpoint.

Four metrics, same as Project 1's budget:
  1. requests_total          — every request that hits any endpoint
  2. requests_by_endpoint    — per-endpoint counts (useful for traffic shaping)
  3. songs_in_db             — set on demand from the DB
  4. errors_total            — every 4xx/5xx response
"""

from collections import defaultdict
from threading import Lock

# A Lock prevents two simultaneous requests from corrupting our counters.
# This is a real concurrency concern even in a tiny API.
_lock = Lock()

_state = {
    "requests_total":  0,
    "errors_total":    0,
    "requests_by_endpoint": defaultdict(int),
}


def record_request(endpoint: str) -> None:
    with _lock:
        _state["requests_total"] += 1
        _state["requests_by_endpoint"][endpoint] += 1


def record_error() -> None:
    with _lock:
        _state["errors_total"] += 1


def snapshot() -> dict:
    """Return a copy of the current metrics state."""
    with _lock:
        return {
            "requests_total": _state["requests_total"],
            "errors_total": _state["errors_total"],
            "requests_by_endpoint": dict(_state["requests_by_endpoint"]),
        }