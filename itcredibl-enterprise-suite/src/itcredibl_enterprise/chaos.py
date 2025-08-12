from __future__ import annotations

import os
import random

_PROB = float(os.getenv("ITCREDIBL_CHAOS_PROB", "0"))
_TARGET = os.getenv("ITCREDIBL_CHAOS_ONLY", "").strip()  # e.g., "openai"


class Chaos(Exception):
    pass


def maybe_fail(provider: str):
    if _PROB <= 0:
        return
    if _TARGET and _TARGET != provider:
        return
    if random.random() < _PROB:
        raise Chaos(f"Chaos induced failure for {provider}")
