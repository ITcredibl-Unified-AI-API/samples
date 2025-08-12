from __future__ import annotations

from typing import Any

from .health import ProviderHealth


class RoutingPolicy:
    def __init__(
        self,
        allow: list[str] | None = None,
        deny: list[str] | None = None,
        residency: str | None = None,
    ):
        self.allow = allow or []
        self.deny = deny or []
        self.residency = residency

    def pick(self, candidates: list[str], health: ProviderHealth) -> str:
        pool = [c for c in candidates if c not in self.deny]
        if self.allow:
            pool = [c for c in pool if c in self.allow]
        if not pool:
            pool = candidates[:]
        scored = sorted(
            ((p, health.score(p)) for p in pool), key=lambda x: x[1], reverse=True
        )
        return scored[0][0]


class CostPolicy:
    def __init__(self, max_cost: float = 0.02):
        self.max_cost = max_cost

    def allow(self, usage: dict[str, Any]) -> bool:
        cost = (usage or {}).get("cost")
        if cost is None:
            return True
        return float(cost) <= self.max_cost
