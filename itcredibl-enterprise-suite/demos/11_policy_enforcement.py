import asyncio, os
from itcredibl_enterprise.client import ITcrediblClient
from itcredibl_enterprise.console import header, kv_table, box
from itcredibl_enterprise.policies import RoutingPolicy, CostPolicy
from itcredibl_enterprise.health import ProviderHealth

MODEL = os.getenv("ITCREDIBL_MODEL", "gpt-4o")
CANDIDATES = [p.strip() for p in os.getenv("ITCREDIBL_PROVIDERS", "openai,anthropic,groq").split(",") if p.strip()]

async def main():
    header("Policy-Based Smart Routing")
    health = ProviderHealth()
    chosen = RoutingPolicy(allow=CANDIDATES).pick(CANDIDATES, health)
    kv_table({"chosen": chosen}, title="Policy Decision")

    c = ITcrediblClient()
    r = await c.chat([{"role":"user","content":"In one line, explain policy-based routing."}], model=MODEL, provider=chosen, temperature=0)
    usage = r.get("usage", {})
    ok = CostPolicy(max_cost=float(os.getenv("ITCREDIBL_COST_CAP", "0.02"))).allow(usage)
    kv_table({"cost": usage.get("cost"), "allowed_under_cap": ok}, title="Cost Policy")
    text = (r.get("choices", [{}])[0].get("message", {}) or {}).get("content", "")
    box(text.strip() if ok else "Blocked due to cost cap", title="Assistant")
    await c.aclose()

if __name__ == "__main__":
    asyncio.run(main())