from __future__ import annotations

import time


class CircuitBreaker:
    def __init__(self, fail_threshold: int = 3, reset_seconds: int = 20):
        self.fail_threshold = fail_threshold
        self.reset_seconds = reset_seconds
        self.failures: dict[str, int] = {}
        self.open_until: dict[str, float] = {}

    def record_success(self, key: str):
        self.failures[key] = 0
        self.open_until.pop(key, None)

    def record_failure(self, key: str):
        self.failures[key] = self.failures.get(key, 0) + 1
        if self.failures[key] >= self.fail_threshold:
            self.open_until[key] = time.time() + self.reset_seconds

    def is_open(self, key: str) -> bool:
        until = self.open_until.get(key, 0)
        if until and time.time() > until:
            self.open_until.pop(key, None)
            self.failures[key] = 0
            return False
        return bool(until)
