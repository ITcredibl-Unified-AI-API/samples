from datetime import datetime
from typing import Any


def log_event(event: str, detail: dict[str, Any]) -> dict[str, Any]:
    return {"ts": datetime.utcnow().isoformat() + "Z", "event": event, "detail": detail}
