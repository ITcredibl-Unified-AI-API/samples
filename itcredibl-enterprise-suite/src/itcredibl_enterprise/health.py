import random
class ProviderHealth:
    def __init__(self): self._s = {}
    def score(self, provider: str) -> float:
        base = self._s.get(provider) or random.uniform(0.7, 0.99)
        s = max(0.0, min(1.0, base + random.uniform(-0.02, 0.02)))
        self._s[provider] = s
        return s