from __future__ import annotations

import os
from typing import Any

try:
    from datadog import initialize, statsd  # type: ignore
except Exception:  # pragma: no cover
    initialize = None
    statsd = None

_DD_ENABLED = bool(os.getenv("ITCREDIBL_DATADOG", "").strip())
if _DD_ENABLED and initialize:
    initialize()


def emit_metrics(event: dict[str, Any]) -> None:
    """Optional Datadog metrics. No-op if not configured.
    event = {
      operation, duration_ms, provider, model,
      tokens: {prompt, completion, total}, cost
    }
    """
    if not (_DD_ENABLED and statsd):
        return
    try:
        tags = [
            f"provider:{event.get('provider')}",
            f"model:{event.get('model')}",
            f"op:{event.get('operation')}",
        ]
        statsd.timing("itcredibl.op.duration", event.get("duration_ms", 0), tags=tags)
        tokens = event.get("tokens") or {}
        for k in ("prompt", "completion", "total"):
            v = tokens.get(k)
            if v is not None:
                statsd.gauge(f"itcredibl.tokens.{k}", v, tags=tags)
        cost = event.get("cost")
        if cost is not None:
            statsd.gauge("itcredibl.cost.usd", float(cost), tags=tags)
    except Exception:
        pass
