from __future__ import annotations

import os
from contextlib import contextmanager

_ENABLED = os.getenv("ITCREDIBL_TRACING", "").strip()
try:
    from opentelemetry import trace  # type: ignore
    from opentelemetry.sdk.trace import TracerProvider  # type: ignore
    from opentelemetry.sdk.trace.export import (  # type: ignore
        ConsoleSpanExporter,
        SimpleSpanProcessor,
    )

    _OTEL_OK = True
except Exception:  # pragma: no cover
    _OTEL_OK = False

if _ENABLED and _OTEL_OK:
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        SimpleSpanProcessor(ConsoleSpanExporter())
    )
_tracer = trace.get_tracer(__name__) if (_ENABLED and _OTEL_OK) else None


@contextmanager
def span(name: str):
    if _tracer is None:
        yield None
    else:
        with _tracer.start_as_current_span(name) as s:
            yield s
