import asyncio, os
from itcredibl_enterprise.console import header, kv_table
from itcredibl_enterprise.policies import RoutingPolicy
from itcredibl_enterprise.health import ProviderHealth

async def main():
    header("Data Residency Policy (demo)")
    residency = os.getenv("ITCREDIBL_RESIDENCY", "us")
    providers = [p.strip() for p in os.getenv("ITCREDIBL_PROVIDERS", "openai,anthropic,groq").split(",") if p.strip()]
    chosen = RoutingPolicy(allow=providers, residency=residency).pick(providers, ProviderHealth())
    kv_table({"residency": residency, "chosen": chosen}, title="Residency Selection")

if __name__ == "__main__":
    asyncio.run(main())