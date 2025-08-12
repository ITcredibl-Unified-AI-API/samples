import asyncio
import os

from itcredibl_enterprise.chaos import Chaos, maybe_fail
from itcredibl_enterprise.client import ITcrediblClient
from itcredibl_enterprise.console import header, kv_table
from itcredibl_enterprise.health import ProviderHealth
from itcredibl_enterprise.policies import RoutingPolicy

MODEL = os.getenv("ITCREDIBL_MODEL", "gpt-4o")
PROVIDERS = [
    p.strip()
    for p in os.getenv("ITCREDIBL_PROVIDERS", "openai,anthropic,groq").split(",")
    if p.strip()
]


async def try_provider(p: str) -> bool:
    c = ITcrediblClient()
    try:
        maybe_fail(p)
        r = await c.chat(
            [{"role": "user", "content": "Say 'All good'"}],
            model=MODEL,
            provider=p,
            temperature=0,
        )
        txt = (
            (r.get("choices", [{}])[0].get("message", {}) or {})
            .get("content", "")
            .strip()
        )
        kv_table({"provider": p, "ok": True, "text": txt[:60]})
        return True
    except Chaos as e:
        kv_table({"provider": p, "ok": False, "error": str(e)})
        return False
    finally:
        await c.aclose()


async def main():
    header("Chaos Failover — proving SLA continuity")
    order = [RoutingPolicy(allow=PROVIDERS).pick(PROVIDERS, ProviderHealth())] + [
        p for p in PROVIDERS if p != PROVIDERS[0]
    ]
    for p in order:
        ok = await try_provider(p)
        if ok:
            return


if __name__ == "__main__":
    asyncio.run(main())
