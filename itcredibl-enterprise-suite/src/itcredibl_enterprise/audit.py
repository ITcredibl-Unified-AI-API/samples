from typing import Dict, Any
from datetime import datetime

def log_event(event: str, detail: Dict[str, Any]) -> Dict[str, Any]:
    return {"ts": datetime.utcnow().isoformat() + "Z", "event": event, "detail": detail}